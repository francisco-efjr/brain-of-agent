# Esqueleto de tokens em três camadas (DTCG 2025.10)

Template T-05. Uso: `design-tokens`. Formato: Design Tokens Format Module 2025.10, **relatório final de comunidade (2025-10-28), não padrão W3C**; o rascunho de 2026-09 diz "preview, não implemente". Fixe a versão no nome do arquivo, em `$description` de grupo ou na configuração do build; a spec 2025.10 não define `$schema` na raiz (conferido em 2026-10-10), então não acrescente esse campo nem invente URL de schema.

**Sintaxe dos valores: Verificado para `color`, `dimension` e `duration`** (leitura da spec em 2026-10-10; tipos compostos e modos não verificados). Este esqueleto usa a forma estruturada de 2025.10 (cor como objeto com `colorSpace`, `components` e `hex` opcional; dimensão e duração como `{ value, unit }`). Rascunhos anteriores usavam string (`"#0F766E"`, `"16px"`). Confira a seção de tipos do relatório e ajuste ao que o build do projeto aceita antes de gerar o arquivo.

## Regras

1. Camadas: **primitivo** (valor bruto) → **semântico** (função, referencia primitivo com `{}`) → **componente** (referencia semântico). Componentes nunca usam valor cru nem primitivo.
2. Referência `{grupo.token}` aponta só para tokens completos. Referência desconhecida ou circular é **erro**.
3. Nome pela função (`color.text.default`), não pela aparência.
4. Dark mode é um modo da coleção semântica, sem mudar nomes (neste formato: um arquivo ou conjunto por tema que redefine os semânticos; confira como o build do projeto resolve temas).
5. Arquivos gerados (CSS, TS) nunca são editados à mão; `tokens.json` é a fonte.
6. Depreciação: `$deprecated` no nome antigo durante a migração; remova na major seguinte.

## Esqueleto

```json
{
  "$description": "Tokens de [produto]. Formato DTCG 2025.10 (relatório de comunidade, não padrão W3C).",
  "color": {
    "$type": "color",
    "primitive": {
      "white":   { "$value": { "colorSpace": "srgb", "components": [1, 1, 1], "hex": "#FFFFFF" } },
      "ink-900": { "$value": { "colorSpace": "srgb", "components": [0.102, 0.11, 0.118], "hex": "#1A1C1E" } },
      "teal-600": { "$value": { "colorSpace": "srgb", "components": [0.059, 0.463, 0.431], "hex": "#0F766E" } }
    },
    "text": {
      "default": { "$value": "{color.primitive.ink-900}", "$description": "Texto principal. 17,09:1 sobre color.surface.default." }
    },
    "surface": {
      "default": { "$value": "{color.primitive.white}" }
    },
    "action": {
      "primary": { "$value": "{color.primitive.teal-600}", "$description": "Fundo de ação primária. Texto sobre ela: 5,47:1 com color.primitive.white." }
    }
  },
  "space": {
    "$type": "dimension",
    "primitive": {
      "2": { "$value": { "value": 8, "unit": "px" } },
      "3": { "$value": { "value": 12, "unit": "px" } },
      "4": { "$value": { "value": 16, "unit": "px" } }
    },
    "inset": {
      "md": { "$value": "{space.primitive.4}" }
    }
  },
  "motion": {
    "$type": "duration",
    "fast": { "$value": { "value": 150, "unit": "ms" } }
  },
  "button": {
    "primary": {
      "background": { "$type": "color", "$value": "{color.action.primary}" },
      "padding":    { "$type": "dimension", "$value": "{space.inset.md}" }
    }
  }
}
```

## Verificação antes de entregar

- [ ] Toda referência `{...}` resolve para um token existente e completo; nenhuma circular.
- [ ] Nenhum componente referencia `*.primitive.*` ou valor cru.
- [ ] Contraste dos pares semânticos calculado pela fórmula WCAG, em todos os temas, e registrado em `$description` ou no relatório.
- [ ] Versão do formato declarada no arquivo ou no README.
- [ ] Nenhuma ferramenta foi instalada ou executada sem autorização; o que rodou e o que não pôde rodar está relatado.
