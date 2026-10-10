# Esqueleto de tokens em três camadas (DTCG 2025.10)

Formato: relatório final do W3C Design Tokens Community Group, versão 2025.10, de 2025-10-28 (https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/). **Não é padrão W3C** nem está na trilha de padrões; um rascunho posterior (2026-09-08) se declara preview. Fixe 2025.10 e confirme a versão estável antes de depender dela num build (V-20).

O que foi verificado em 2026-10-10, na leitura dos primeiros 100 mil de 113 mil caracteres da spec: `dimension` é objeto `{ "value": número, "unit": "px" | "rem" }`; `duration` é objeto `{ "value": número, "unit": "ms" | "s" }`; `fontFamily` é string ou lista de strings; `fontWeight` é número de 1 a 1000 ou alias; `cubicBezier` é lista de 4 números (x entre 0 e 1); `color` é definido por módulo à parte, e os exemplos usam `colorSpace` e `components` (com `hex` opcional); alias usa chaves `{caminho.do.token}`; `$ref` com JSON Pointer também é permitido; extensões `.tokens` ou `.tokens.json`; mídia `application/design-tokens+json`. A spec não define `$schema` na raiz. O trecho final (13 mil caracteres) não foi lido. Campos de tokens compostos (typography, shadow, border) e modos/temas não foram verificados: confira na spec antes de usar.

## Sumário

- [Esqueleto](#esqueleto)
- [Regras](#regras)
- [Camadas e nomes](#camadas-e-nomes)
- [Temas e modo escuro](#temas-e-modo-escuro)
- [Validação sem instalar nada](#validação-sem-instalar-nada)

## Esqueleto

Paleta do exemplo [design-brief](${CLAUDE_PLUGIN_ROOT}/skills/design-brief/references/exemplo-plano.md) (fictícia). Componentes do canal sRGB entre 0 e 1 (hex dividido por 255, 4 casas); `hex` acompanha os exemplos da spec como conveniência de leitura, não substitui `components`.

```json
{
  "color": {
    "$type": "color",
    "primitive": {
      "ink-900":   { "$value": { "colorSpace": "srgb", "components": [0.0784, 0.1529, 0.1686], "hex": "#14272b" } },
      "slate-600": { "$value": { "colorSpace": "srgb", "components": [0.2902, 0.3647, 0.3804], "hex": "#4a5d61" } },
      "moss-700":  { "$value": { "colorSpace": "srgb", "components": [0.0431, 0.3647, 0.3098], "hex": "#0b5d4f" } },
      "sun-400":   { "$value": { "colorSpace": "srgb", "components": [1, 0.7725, 0.2392], "hex": "#ffc53d" } },
      "red-700":   { "$value": { "colorSpace": "srgb", "components": [0.7059, 0.1373, 0.0941], "hex": "#b42318" } },
      "sand-50":   { "$value": { "colorSpace": "srgb", "components": [0.9529, 0.9686, 0.9647], "hex": "#f3f7f6" } },
      "white":     { "$value": { "colorSpace": "srgb", "components": [1, 1, 1], "hex": "#ffffff" } }
    },
    "semantic": {
      "text": {
        "primary":   { "$value": "{color.primitive.ink-900}", "$description": "Texto principal; 14,35:1 sobre canvas" },
        "secondary": { "$value": "{color.primitive.slate-600}" },
        "danger":    { "$value": "{color.primitive.red-700}" }
      },
      "surface": {
        "canvas": { "$value": "{color.primitive.sand-50}" },
        "raised": { "$value": "{color.primitive.white}" }
      },
      "action": {
        "primary": {
          "bg":    { "$value": "{color.primitive.moss-700}" },
          "fg":    { "$value": "{color.primitive.white}", "$description": "7,80:1 sobre action.primary.bg" }
        }
      },
      "accent": { "highlight": { "$value": "{color.primitive.sun-400}", "$description": "Decorativo; nunca texto nem borda única" } }
    }
  },
  "space": {
    "$type": "dimension",
    "primitive": {
      "2": { "$value": { "value": 0.5, "unit": "rem" } },
      "4": { "$value": { "value": 1,   "unit": "rem" } }
    },
    "semantic": {
      "inline-md": { "$value": "{space.primitive.2}" },
      "stack-lg":  { "$value": "{space.primitive.4}" }
    }
  },
  "motion": {
    "duration": {
      "short": { "$type": "duration", "$value": { "value": 200, "unit": "ms" } }
    },
    "easing": {
      "exit": { "$type": "cubicBezier", "$value": [0, 0, 0.2, 1] }
    }
  },
  "font": {
    "family": {
      "body": { "$type": "fontFamily", "$value": ["Atkinson Hyperlegible", "system-ui", "sans-serif"] }
    },
    "weight": {
      "bold": { "$type": "fontWeight", "$value": 700 }
    }
  },
  "button": {
    "primary": {
      "bg": { "$type": "color", "$value": "{color.semantic.action.primary.bg}" },
      "fg": { "$type": "color", "$value": "{color.semantic.action.primary.fg}" }
    }
  }
}
```

Observações do exemplo:

- `$type` num grupo vale para os tokens abaixo dele; `$type` no token vale só para ele.
- A camada de componente (`button.primary.*`) aponta para semânticos, nunca para primitivos.
- Os números de contraste nas descrições foram calculados com a fórmula WCAG ([contraste-wcag](contraste-wcag.md)); recalcule se a cor mudar.
- A razão 1,25 de escala, 200 ms e a curva `[0, 0, 0.2, 1]` são escolhas do exemplo (regras de polegar, Inferido), não normas.

## Regras

1. **Componente nunca usa valor cru nem primitivo.** Só semântico ou token de componente.
2. **Semântico referencia primitivo** (ou outro semântico); primitivo contém o valor.
3. **Referência circular ou para token inexistente é erro.** Cada `{...}` precisa resolver para um token completo (não para um grupo).
4. **Nomes por papel** (`action.primary.bg`), com ordem estável `categoria.papel.variante.propriedade`; evite aparência (`red`) em semânticos.
5. **Depreciação antes de remoção:** marque `$deprecated` (propriedade reservada da spec; confira nela o tipo de valor aceito) e registre o substituto em `$description`; mantenha o token por uma versão minor, no mínimo.
6. **Arquivos gerados** (CSS, TS, plataformas) saem de um build a partir desta fonte e nunca são editados à mão; a lista de caminhos editáveis exclui a saída.
7. **Descrição** (`$description`) só onde esclarece o uso ou registra uma medição; não repita o nome.

## Camadas e nomes

| Camada | Exemplo | Quem usa | Pode mudar valor? |
| --- | --- | --- | --- |
| Primitivo | `color.primitive.moss-700` | só outros tokens | sim, com revisão de contraste dos semânticos que o referenciam |
| Semântico | `color.semantic.action.primary.bg` | designers e componentes | sim (patch/minor); renomear é major |
| Componente | `button.primary.bg` | o próprio componente | sim; é a camada mais volátil |

Quando o sistema é pequeno, a camada de componente pode ser dispensada; o Figma a considera útil em sistemas maiores e a ordem entre semântico e componente é flexível (V-21).

## Temas e modo escuro

- No Figma, o modo escuro é um modo da coleção semântica, sem mudar os nomes; primitivos podem ficar ocultos na publicação.
- No JSON, uma convenção possível: um arquivo de semânticos por tema (`semantic.light.tokens.json`, `semantic.dark.tokens.json`) apontando para os mesmos nomes. Suposição: a spec 2025.10 não teve a parte de temas verificada aqui; confirme antes de afirmar que o formato "suporta modos".
- Recalcule o contraste de cada par semântico no escuro; dark mode não é inversão de lightness.

## Validação sem instalar nada

1. Liste os tokens definidos (caminhos completos) e os `{...}` usados; todo usado deve estar definido.
2. Construa o grafo de referências e procure ciclos à mão ou com um script curto de biblioteca padrão que o usuário aprove.
3. Compare valores de `components` com o hex (hex/255) para detectar discrepância.
4. Para conversão a CSS ou outras plataformas existem ferramentas (por exemplo Style Dictionary), mas licença e versão atuais não foram verificadas aqui: não instalar nem executar sem pedido do usuário e versão fixada.
