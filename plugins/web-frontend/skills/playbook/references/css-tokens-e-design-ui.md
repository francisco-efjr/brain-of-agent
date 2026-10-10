# CSS, tokens, direção de design e acabamento de interface

Tailwind v4, tokens semânticos, o fluxo de design em três fases, o piso de qualidade verificável, critérios de acabamento e diretrizes de interface. Leia em `design-ui`, em redesenho, em design system em código e em revisão visual. Conferido em 2026-10-10 (V-01 a V-03, V-12, V-23, V-35, V-43, V-53, V-54, brain `apple-design.md`).

## Sumário

- [Precedência: o brief e o projeto vencem](#precedência-o-brief-e-o-projeto-vencem)
- [Direção de design em três fases](#direção-de-design-em-três-fases)
- [Bloco ui_direction para prompts de sistema](#bloco-ui_direction-para-prompts-de-sistema)
- [Piso de qualidade verificável](#piso-de-qualidade-verificável)
- [Saída genérica de IA: lista configurável](#saída-genérica-de-ia-lista-configurável)
- [Tailwind v4: tokens e responsividade](#tailwind-v4-tokens-e-responsividade)
- [Tokens semânticos e DTCG](#tokens-semânticos-e-dtcg)
- [Movimento e prefers-reduced-motion](#movimento-e-prefers-reduced-motion)
- [shadcn/ui e propriedade de primitivos](#shadcnui-e-propriedade-de-primitivos)
- [Qualidade de acabamento: critérios locais](#qualidade-de-acabamento-critérios-locais)
- [Diretrizes de interface](#diretrizes-de-interface)
- [Lacunas](#lacunas)

## Precedência: o brief e o projeto vencem

O brief do usuário, o `DESIGN.md` e os tokens do projeto sempre vencem qualquer regra estética deste plugin, inclusive quando pedem um visual da lista de "saída genérica" (V-01, V-35). Diga o trade-off uma vez e siga o pedido. A orientação estética vale só em tarefas de UI e mora em skill (`design-ui`); tokens e stack do projeto moram no CLAUDE.md (V-02). O plugin não mede qualidade visual (Não verificável); estética e UX são decisão humana, e o agente produz capturas e notas como insumo (V-62).

## Direção de design em três fases

Destilação com redação própria de `frontend-design` (anthropics/skills, Apache-2.0; V-01) e do blog de design da Anthropic (V-02):

1. **Brief.** Três linhas: assunto, público e tarefa principal. Se o pedido não traz, proponha e confirme antes de desenhar. Tokens ou marca do projeto, se existirem, valem.
2. **Plano antes do código.** 4 a 6 cores nomeadas (hex), papéis tipográficos (por exemplo título, corpo, rótulo, dado), conceito de layout (uma frase e um wireframe ASCII por opção) e 3 princípios específicos do brief. Releia o plano e marque cada decisão que você tomaria para qualquer página parecida; troque essas por escolhas derivadas do assunto e registre "mudei X porque Y". Modelo: `../assets/templates/plano-ui.md`.
3. **Build e crítica.** Construa seguindo o plano; capture a tela em mobile e desktop, liste o que remover e remova pelo menos um elemento decorativo; relate com evidência (caminhos das capturas, comandos rodados).

Altitude do prompt (V-02): dê direção e critérios verificáveis (papéis tipográficos, contraste, quantidade de acentos) e deixe os valores finais (hex, famílias) para o plano revisado; nem valores fixos soltos nem vagueza.

Uma ou duas famílias tipográficas e linhas de texto abaixo de cerca de 80 caracteres; estrutura visual é informação (numeração 01/02/03 só para sequência real); movimento não pedido só como um momento orquestrado de entrada (V-01). Cuidado com especificidade de CSS que cancela `padding` e `margin` (V-01).

## Bloco ui_direction para prompts de sistema

Para um subagente ou projeto que gera UI sem a skill completa (reescrito a partir de V-03; a seção de estética da documentação cita explicitamente Opus 4.5 e 4.6, então confira a página do modelo-alvo antes de reaproveitar o tom):

```text
<ui_direction>
Antes de estilizar, escreva o assunto, o público e a tarefa principal da tela.
Escolha tipografia, cor e movimento a partir do assunto, não do que você usaria em qualquer projeto.
Cores como variáveis CSS: uma dominante e poucos acentos fortes.
Movimento: um momento orquestrado de entrada em CSS; fora isso, só resposta a ação do usuário.
Respeite prefers-reduced-motion. Antes de concluir, abra a tela em 320 px e em desktop,
capture screenshots e relate o que verificou.
</ui_direction>
```

## Piso de qualidade verificável

Todo item abaixo tem uma verificação concreta (V-01, V-16, V-23):

| Item | Verificação |
| --- | --- |
| Responsivo até 320 px sem rolagem horizontal | captura em 320 px; `document.documentElement.scrollWidth <= clientWidth` |
| Foco visível em todo controle | percorrer com Tab e capturar |
| Contraste mínimo de texto normal 4,5:1 | medir no estado e fundo reais, não estimar pela imagem |
| Contrapartida de movimento | cada `animation` e `transition` tem regra em `prefers-reduced-motion: reduce` |
| Paleta harmônica e hierarquia legível | revisão humana (Não verificável por máquina) |
| Conteúdo real ou plausível, incluindo extremos | nomes longos, listas vazias e com milhares de itens; sem lorem ipsum que esconda overflow |

## Saída genérica de IA: lista configurável

Calibração de 2026, não lei; envelhece e nunca vence o brief (V-01, V-35; inspirada também na lista "slop" do gstack `design-html`, MIT, Garry Tan, e em impeccable, Apache-2.0, Paul Bakaus; redação própria). Trate cada item como pergunta: "isto veio do assunto ou do hábito?"

- Fontes padrão usadas por reflexo (Arial, Inter) e gradiente roxo-azul sobre branco.
- Paleta creme com serifa e terracota; ou quase-preto com um único acento neon; ou layout de jornal, aplicados por moda.
- Kit de cartões SaaS idênticos, cartão dentro de cartão, grade de três colunas de "features".
- Tudo centralizado sem hierarquia; hero com linha de métricas ("10k+ usuários"); kicker ou bloco de ícone acima de cada título.
- Cinza sobre fundo colorido; preto ou cinza puro sem tom; easing com bounce.
- Blobs, ondas e padrões decorativos que o conteúdo não pede; brilho nas bordas; ponto pulsante de status.
- CTA genérico ("Começar agora", "Saiba mais") quando o verbo e o objeto reais existem; emoji como elemento visual; depoimentos genéricos; fotos de banco como placeholder.

Regra de escrita de interface (V-01): CTA com verbo e objeto ("Criar conta"), mensagem de erro que explica como corrigir. Um detector automático limpo é evidência, não prova de qualidade visual nem de acessibilidade (V-35): inspecione em vários viewports.

## Tailwind v4: tokens e responsividade

Fonte: Tailwind v4.3 (theme e responsive design) e MDN container queries (V-53, Verificado). **Confirme a versão no `package.json`**: v3 usa `tailwind.config.*`; v4 usa CSS com `@theme` (V-43). Um modelo por projeto; se houver mistura, proponha plano de migração.

- Variáveis em `@theme` geram utilitários por namespace: `--color-*`, `--font-*`, `--text-*`, `--font-weight-*`, `--breakpoint-*`, `--container-*`, `--radius-*`, `--shadow-*` e outros. `--color-*: initial` limpa o namespace.
- `@theme inline` quando a variável referencia outra; `@theme static` gera todas as variáveis, senão só as usadas entram; `:root` para variável que não gera utilitário.
- Exemplo de token em `oklch`, nome semântico acima do primitivo (por exemplo `--color-surface` apontando para um valor de paleta; Inferido). Não duplique a mesma cor em `:root`.

```css
@import "tailwindcss";

@theme {
  --color-*: initial;                       /* limpa a paleta padrão */
  --color-ink: oklch(0.22 0.02 260);
  --color-paper: oklch(0.98 0.005 90);
  --color-accent: oklch(0.62 0.19 35);
  --font-display: "Nome da Fonte", serif;   /* exemplo; escolha pelo assunto */
  --breakpoint-3xl: 120rem;
}
```

- Breakpoints padrão: `sm` 40rem, `md` 48rem, `lg` 64rem, `xl` 80rem, `2xl` 96rem. Classe sem prefixo vale para todas as telas (mobile primeiro); prefixo só para ampliar. `max-*` e intervalo (`md:max-xl:flex`) existem.
- Container queries: `@container` no pai, `@md:` no filho; `@max-md:`; nomeado `@container/main` com `@sm/main:`; `@container-size` para unidades de bloco como `cqb`. Tamanhos de container começam em `@3xs` (16rem). MDN: `container-type` aceita `size`, `inline-size`, `normal`; unidades `cqw`, `cqh`, `cqi`, `cqb`, `cqmin`, `cqmax`.
- Componente reutilizável usa `@container`; layout de página usa breakpoint (Inferido de "componentes mais portáteis").
- A compatibilidade por navegador não foi lida: confira a tabela do MDN antes de depender de recurso novo (Não verificável nesta pesquisa).

## Tokens semânticos e DTCG

Tokens expressam função (`--color-surface`, `--color-danger`), não aparência; cores literais espalhadas não são um design system (brain). O DTCG (https://www.designtokens.org/tr/drafts/format/) é rascunho de 08 set 2026, declara que não é padrão W3C; a última versão publicada é a 2025.10 (V-54). Use só como vocabulário para trocar tokens com design: `$value`, `$type`, `$description`, `$deprecated`, `$extensions`, grupos, alias entre tokens e proibição de referência circular. O formato do projeto (CSS `@theme`) prevalece. Pipeline de tokens para código (Style Dictionary) não foi lido: Não verificado.

## Movimento e prefers-reduced-motion

Fonte: MDN (modificada em 10 jun 2026; V-23). Valores `no-preference` e `reduce`; mantenha a animação normal e sobrescreva dentro de `@media (prefers-reduced-motion: reduce)`; o exemplo do MDN troca uma animação de escala por uma de opacidade, justificando pelo risco vestibular. Regra: toda `animation` e `transition` tem contrapartida em `reduce` (opacidade ou instantâneo). Movimento que comunica estado sobrevive em forma reduzida (Inferido: o MDN fala em minimizar movimento não essencial).

```css
.toast { animation: slide-in 240ms ease-out; }
@media (prefers-reduced-motion: reduce) {
  .toast { animation: fade-in 120ms linear; }
}
```

## shadcn/ui e propriedade de primitivos

Prática de blog classe C (V-43), sustentada por regra de manutenção comum; verifique contra a documentação atual do shadcn/ui e do Tailwind. O estudo de preferência de V-34 indica que agentes tendem a escolher shadcn/ui e Tailwind quando a stack não é declarada (modelos antigos; efeito de declarar é Inferido).

- Primitivos em `src/components/ui` e UI de produto em `src/components/app`; primitivos não recebem lógica de produto (wrapper em `app/`).
- Busque no código antes de criar `Button` ou `Card`; drift de componentes base é o risco.
- Dialog sempre com título e descrição (nome acessível).
- Com React Hook Form e Zod, siga o padrão que o projeto já usa; screenshot antes de aceitar mudança visual.

## Qualidade de acabamento: critérios locais

Adaptado do brain-of-agent (`apple-design.md`, MIT, conteúdo do autor). Apple é a preferência de acabamento do autor, não um ranking comprovado nem norma para a web; adote integração, consistência e cuidado com a interação, preservando a identidade e a plataforma do produto. Não copie métricas do arquivo de inspiração (13 pt, margens de 20 pt, alvo de 20x20 pt) nem nomes de releases; não imponha moldura de Mac nem Liquid Glass na web (isso vai para `/mobile-apps:playbook` e `/ux-ui-design:playbook`). Fontes citadas no brain e não relidas aqui: Human Interface Guidelines da Apple.

Sete critérios locais de revisão (não são citações normativas):

1. Inventário original mapeado ao novo fluxo: nenhuma função some por estética; propostas novas ficam identificadas.
2. Toda ação tem comportamento, feedback, estado e recuperação definidos.
3. Tokens semânticos expressam função, variantes e consistência.
4. Protótipo e aplicação implementada são diferentes: um botão navegável não comprova salvamento, permissão ou integração.
5. Acessibilidade é comportamento verificável, não acabamento.
6. Movimento explica mudança e admite interrupção e redução.
7. A tela tem dados reais ou plausíveis, extremos e falhas, sem lorem ipsum que mascare overflow ou hierarquia.

Matriz de estados por componente e roteiro de 7 passos: `../assets/templates/matriz-estados-componente.md`. Checklist de aceite: `checklist-completo.md`. Na web, widgets personalizados seguem os padrões do APG (https://www.w3.org/WAI/ARIA/apg/patterns/); semântica HTML primeiro.

Exemplo (lista de clientes): pedido "tornar a lista consistente e acessível num sistema web existente". Não troque a stack nem adicione moldura de janela. Inventarie busca, filtro, ordenação, seleção e ações; implemente semântica, estados vazio, carregando e erro, foco ao fechar diálogo e tratamento de resposta obsoleta; teste por teclado, em viewport estreito e com nomes longos; registre persistência e autorização na API separadamente da avaliação visual.

## Diretrizes de interface

Destilado localmente das categorias do `web-interface-guidelines` da Vercel (licença MIT, "Copyright (c) 2025 Vercel Labs", LICENSE lido; V-12) para substituir a prática rejeitada de buscar as regras por URL em runtime. Exemplos confirmados no texto da fonte: botão só com ícone precisa de rótulo acessível; `outline: none` só com substituto de foco; tipo e `autocomplete` corretos em inputs. As demais linhas são conhecimento estável do domínio, não transcrição da fonte (Inferido). Saída de revisão: `arquivo:linha - regra - correção`.

| Categoria | Regras |
| --- | --- |
| Foco | Todo controle tem foco visível; `outline: none` só com substituto equivalente; use `:focus-visible` para evitar anel em clique de mouse. |
| Formulários | `type` e `autocomplete` corretos; `label` ligado; colar não é bloqueado em campos de senha e código; botão de envio mostra pendência. |
| Animação | Só `transform` e `opacity`; contrapartida em `prefers-reduced-motion`; nada que bloqueia a interação. |
| Tipografia | Uma ou duas famílias; linha abaixo de cerca de 80 caracteres; números alinhados em tabelas (`font-variant-numeric: tabular-nums`). |
| Imagens | Dimensões declaradas; `alt` descritivo ou vazio quando decorativa; acima da dobra sem lazy-load. |
| Navegação e estado | URL reflete filtros e abas compartilháveis; voltar e avançar preservam estado; ação destrutiva pede confirmação ou permite desfazer. |
| Toque | Alvo mínimo de 24 px CSS (44 px quando possível); sem depender de hover. |
| Dark mode | Tokens por tema; `color-scheme` declarado; contraste medido nos dois temas. |
| i18n | Texto não concatenado; datas, números e moedas com `Intl`; contêineres toleram texto 30% mais longo (Suposição). |
| Hidratação | Valores iniciais iguais no servidor e no cliente; sem `window` no render. |
| Copy | Verbo e objeto no botão; erro diz como corrigir; sem jargão interno. |

## Lacunas

Storybook para design system e documentação de componentes, pipeline de tokens, compatibilidade por navegador de container queries e a leitura integral do `web-interface-guidelines` ficaram fora da pesquisa. Trate como Não verificado.
