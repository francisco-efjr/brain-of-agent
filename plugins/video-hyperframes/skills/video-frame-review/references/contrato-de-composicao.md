# Contrato de composição HyperFrames: armadilhas silenciosas

Base: HyperFrames (HeyGen, Apache-2.0), commit `bf4cf860fbd26a7d51938c5f11987c335d4e848a`: `hyperframes-core/references/` (`data-attributes`, `determinism-rules`, `sub-compositions`, `tracks-and-clips`, `minimal-composition`), `frame-worker-core.md`, `packages/lint/src/rules/composition.ts` e `docs/prompting/*` (V-49 a V-53, V-57, V-69), destilado com redação própria. Rótulo geral: **Verificado** (texto lido); o comportamento em render não foi executado. Código vence documentação: onde a doc diverge do código, vale o código (V-53).

Sumário: 1 Raiz e clips · 2 Tempo · 3 Mídia · 4 Timeline e determinismo · 5 Sub-composições · 6 Doutrina da rota faceless · 7 Sintoma -> causa · 8 Exemplo mínimo · 9 O que o lint já cobre.

## 1. Raiz e clips

- **Raiz:** `data-composition-id` único e igual à chave de `window.__timelines`; `data-width` e `data-height` obrigatórios; `data-duration` é a duração de render em segundos, **lida uma vez na compilação, antes dos scripts**; `data-fps` opcional. A raiz fica `position: relative`, com dimensões em pixels. `data-start="0"` na raiz é convenção.
- **Clip:** `data-start` é o que torna o elemento "temporizado". `data-duration` é obrigatório em `div` e em sub-composição; imagem sem duração vale 3 s; vídeo e áudio usam a duração da mídia. `data-track-index` é só faixa do Studio (o render ignora; as camadas saem por `z-index`).
- **`class="clip"` é convenção, não requisito:** o runtime seleciona `[data-start]` e o lint `timed_element_missing_clip_class` é aviso. Docs que dizem "obrigatório" estão defasados. **Regra do plugin:** escreva sempre `class="clip"` nos elementos temporizados (exceto `<video>` e `<audio>`), nunca anime `display`, `visibility` ou `autoAlpha` neles e ponha o fundo de tela cheia numa camada `clip`, não no `#root` (`gsap_animates_clip_element`).
- Filhos diretos da raiz com `data-start` recebem layout absoluto automático; os demais precisam de `position: absolute; inset: 0`.

## 2. Tempo

- **Janela semiaberta** `[start, start + duration)`: a última pose deve terminar **antes** do `data-duration`.
- **Referências relativas** (`data-start="intro - 0.5"`): os espaços em volta do operador são obrigatórios. Referência não resolvida, ciclo ou alvo sem duração **resolvem em silêncio** para 0 ou para o início do alvo, e a busca é global no documento. O lint não verifica isso: confira à mão o alvo de cada referência.
- `data-duration` de sub-composição hospedeira é a janela visível: uma timeline mais curta segura o último quadro; uma janela mais curta que o conteúdo termina a cena.

## 3. Mídia

- `<audio>` sem `id` fica **mudo** (`media_missing_id`). `crossorigin` em mídia é erro.
- `<video>` com som leva `data-has-audio`; sem som leva `muted` (`video_missing_muted`).
- `<video data-start>` dentro de wrapper com `data-start` é erro (`video_nested_in_timed_element`).
- Nunca chame `play`, `pause` ou `seek` na mídia; anime mídia do host só pela timeline principal, em tempo global.

## 4. Timeline e determinismo

- `gsap.timeline({ paused: true })` registrada em `window.__timelines["<id>"]` **só depois** de terminar o build (build assíncrono em `document.fonts.ready` é suportado). Registrar cedo = timeline vazia tratada como pronta. Com 2 ou mais timelines registradas, uma chave diferente do id **congela o render em t=0**. Não chame `tl.play()` e não use tweens vazios para fixar duração (use `data-duration`).
- Proibido: `Date.now()`, `performance.now()`, `Math.random()` sem semente, rede para ativo obrigatório em tempo de render, estado de hover, scroll ou foco, `repeat: -1` sem raiz de duração finita (`gsap_infinite_repeat` vira aviso). Dado ao vivo também não: o que o vídeo precisa saber já está presente antes do render.
- Não anime a mesma propriedade do mesmo elemento em várias timelines. Evite transform CSS e `x`/`y` do GSAP no mesmo elemento (`gsap_css_transform_conflict`).
- **Seek frio:** um `gsap.fromTo` cujo destino não traz `opacity: 1` pode ficar **invisível** num worker de render que faz seek direto (`gsap_cold_seek_hidden_fromto_missing_reveal`). Não esconda o estado inicial com `tl.set(...)` em t=0 dentro da timeline (`gsap_timeline_set_initial_hide`): use `gsap.set` fora da timeline ou CSS. `fromTo` mostra o estado inicial **antes** de começar; elemento que deve estar ausente até o cue precisa de `to()` com keyframes, `tl.set()` de duração zero na fronteira do beat ou a própria janela do clip. Prefira `gsap.fromTo` a `gsap.from`.
- Workers paralelos não renderizam bit a bit idênticos: para comparar quadros com exatidão, `--workers 1`.
- O lint usa denylist, não allowlist de propriedades: ausência de aviso não prova que uma propriedade é segura.

## 5. Sub-composições (o formato dos quadros do faceless)

- Só o conteúdo de `<template>` é clonado; tudo fora (inclusive `<head>`) é descartado. `<style>` e `<script>` ficam **dentro** do `<template>`.
- O `data-composition-id` do host, o id interno do arquivo e a chave de `window.__timelines` são o mesmo valor (sintoma de erro: "Sub-composition timelines not registered after 45000ms").
- Estilize a raiz por `#root`, nunca por classe (`subcomposition_root_styled_by_class`). Não faça `master.add(child)`. A timeline de uma sub-composição não alcança elemento do host.
- Cada worker de quadro entrega um único fragmento `<template>`, prefixa ids e classes com o `frame_id`, não cria saída (só o último quadro assenta) e não opera a CLI. A lista de 15 itens de autoverificação está em `frame-worker-core.md` oficial; leia lá em vez de copiar.

## 6. Doutrina de motion da rota faceless (normativa; vale sobre o guia geral)

Ease suave `power3` como padrão (`expo.out` em chegada rápida); sem `back.out`, `bounce.out` ou `elastic.out` como padrão (overshoot só como exceção explícita); reveals sequenciais na metade final, no cue, e não tudo nos primeiros 25%; **sem "respiração" nem pan lento ocioso**; no quadro parado, no máximo um jitter sutil de baixa amplitude; seams como cortes casados em velocidade; proibidos `repeat`/`yoyo` infinitos, `Math.random`, `Date.now`, entradas sem `fromTo`, CSS transition e keyframes soltos. Os trechos "idle/breathing" do guia geral não se aplicam aqui.

## 7. Sintoma -> causa provável -> onde olhar

| Sintoma | Causa provável | Onde olhar |
| --- | --- | --- |
| Render congela em t=0 | 2 ou mais timelines registradas e chave diferente do id; timeline registrada antes do build | `window.__timelines[...]` no final de cada arquivo |
| "Sub-composition timelines not registered" | Id do host, id interno e chave divergem | `data-composition-id` no `index.html` e no `<template>` |
| Elemento some ou nunca aparece | `fromTo` sem `opacity: 1` no destino; `data-start` relativo não resolvido virou 0; fim da janela antes da pose | Tweens do elemento; `data-start` e `data-duration` do clip |
| Áudio mudo | `<audio>` sem `id`; `crossorigin` | Tags `<audio>` |
| Fundo cobre todo o conteúdo | Fundo de tela cheia no `#root` ou sem camada `clip` | CSS da raiz e primeira camada |
| Quadro colapsado ou vazio | Sem `class="clip"` e sem layout absoluto | Estilo do filho direto da raiz |
| `check` persiste depois da 1ª correção | Erro de lint que impede o navegador (`browserSkipped`) ou causa não vista | Saída completa do `check`; chamar o `composition-reviewer` |
| `text_box_overflow` de 1 a 4 px em legenda | Falso positivo conhecido | Ignore se não citar `#el-NN-*` |

## 8. Exemplo mínimo standalone (adaptado de HyperFrames, HeyGen, Apache-2.0)

Os quadros reais do faceless são sub-composições com `<template>` (seção 5), não este formato. A doc usa `gsap@3.14.2` e o compilador usa 3.15.0 por padrão; ambos chegam por `cdn.jsdelivr.net` (rede necessária na compilação do `check` e do `render`). Não foi renderizado.

```html
<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      body { margin: 0; background: #0b0f14; }
      #root { position: relative; width: 100%; height: 100%; overflow: hidden; }
      .clip { position: absolute; inset: 0; display: grid; place-items: center; }
      h1 { margin: 0; color: #fff; font: 700 96px system-ui, sans-serif; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0"
         data-width="1920" data-height="1080" data-duration="4">
      <section id="cena-1" class="clip" data-start="0" data-duration="4" data-track-index="1">
        <h1 id="cena-1-titulo">Agentes em orquestração</h1>
      </section>
    </div>
    <script>
      const tl = gsap.timeline({ paused: true });
      tl.fromTo("#cena-1-titulo", { y: 40, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.6, ease: "power3.out" }, 0.2);
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
```

## 9. O que o lint já cobre (não repita à mão) e o que ele não vê

Cobre, entre outros: `root_missing_composition_id`, `subcomposition_root_styled_by_class`, `timed_element_missing_clip_class`, `css_transition_used`, `gsap_css_transform_conflict`, `gsap_infinite_repeat`, `gsap_animates_clip_element`, `gsap_cold_seek_hidden_fromto_missing_reveal`, `gsap_timeline_set_initial_hide`, `media_missing_id`, `video_missing_muted`, `video_nested_in_timed_element`, `font_family_without_font_face`. **Não vê:** referências relativas de `data-start` (resolvem em silêncio), janelas semiabertas, timeline registrada cedo demais, intenção de movimento. Esses são o trabalho do `composition-reviewer`, quando houver sintoma.
