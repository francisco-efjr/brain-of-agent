# Esqueleto de DESIGN.md (formato Google Labs, versão alpha)

Fonte do formato: https://github.com/google-labs-code/design.md (Apache-2.0; V-23). Conferido em 2026-10-10 no README: o formato está em versão **alpha** (spec, schema e CLI em evolução). O exemplo abaixo é redação própria sobre uma marca fictícia; os valores vêm do exemplo [design-brief](${CLAUDE_PLUGIN_ROOT}/skills/design-brief/references/exemplo-plano.md) e não devem ser copiados para outro projeto.

## Sumário

- [Schema do front matter](#schema-do-front-matter)
- [Seções canônicas](#seções-canônicas)
- [Exemplo completo](#exemplo-completo)
- [Regras de preenchimento](#regras-de-preenchimento)
- [Lint e exportação (não executados pela skill)](#lint-e-exportação-não-executados-pela-skill)

## Schema do front matter

Campos do README (todos conferidos em 2026-10-10):

| Campo | Obrigatório | Conteúdo |
| --- | --- | --- |
| `version` | não | atualmente `alpha` |
| `name` | sim | nome do design system |
| `description` | não | uma frase |
| `omitted` | não | seções deixadas de fora de propósito |
| `colors` | recomendado | tokens de cor (qualquer formato de cor CSS); inclua `primary` |
| `typography` | recomendado | objetos com `fontFamily`, `fontSize`, `fontWeight`, `lineHeight`, `letterSpacing`, `fontFeature`, `fontVariation` |
| `rounded` | opcional | dimensões de raio |
| `spacing` | opcional | dimensões ou números |
| `components` | opcional | componentes nomeados com sub-tokens como `backgroundColor`, `textColor`, `rounded`, `padding` |

Referência a token: chaves e caminho com ponto, por exemplo `{colors.primary}`. Variantes (hover, pressionado) são entradas de componente separadas, com nomes relacionados (`button-primary`, `button-primary-hover`).

## Seções canônicas

As seções são opcionais, mas as presentes seguem esta ordem:

1. Overview (alias: Brand & Style)
2. Colors
3. Typography
4. Layout (alias: Layout & Spacing)
5. Elevation & Depth (alias: Elevation)
6. Shapes
7. Components
8. Do's and Don'ts

## Exemplo completo

````markdown
---
version: alpha
name: Clínica Vet Bairro Novo
description: Landing de clínica veterinária de bairro, mobile primeiro.
omitted:
  - Elevation & Depth
colors:
  primary: "#0B5D4F"
  on-primary: "#FFFFFF"
  ink: "#14272B"
  muted: "#4A5D61"
  canvas: "#F3F7F6"
  surface: "#FFFFFF"
  highlight: "#FFC53D"
  danger: "#B42318"
typography:
  heading:
    fontFamily: Bricolage Grotesque
    fontSize: 1.75rem
    fontWeight: 700
    lineHeight: 1.15
  body:
    fontFamily: Atkinson Hyperlegible
    fontSize: 1.0625rem
    fontWeight: 400
    lineHeight: 1.55
rounded:
  control: 8px
  card: 12px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 48px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.control}"
    padding: 12px 20px
  button-primary-hover:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.control}"
    padding: 12px 20px
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.card}"
    padding: 24px
---

## Overview

Clínica de bairro para tutores de cães e gatos que acessam pelo celular. A pessoa deve lembrar que é perto, cuidadosa e responde rápido. Superfície: Persuade. Uma ação em toda a página: agendar pelo WhatsApp.

## Colors

- `primary` (#0B5D4F): única cor de ação e de foco. Texto branco sobre ela: 7,80:1 (calculado).
- `ink` (#14272B) sobre `canvas` (#F3F7F6): 14,35:1. `muted` (#4A5D61) sobre `canvas`: 6,42:1.
- `highlight` (#FFC53D): apenas decorativo, em selos e marca-texto; sobre `canvas` tem 1,46:1, então nunca é texto nem a única borda de um componente. `ink` sobre `highlight`: 9,82:1.
- `danger` (#B42318) sobre `surface`: 6,57:1; o erro também leva ícone e texto, nunca só cor.

## Typography

Títulos em Bricolage Grotesque 700, corpo em Atkinson Hyperlegible 17 px com linha 1,55 e medida de 60 a 70 caracteres. Duas famílias, pesos 400 e 700. Licença e disponibilidade das fontes a confirmar antes do uso.

## Layout

Mobile primeiro, coluna única até 768 px. Escala de espaçamento de 4 px (`xs` a `xl`). Alvos de toque de 44 px; barra de ação fixa no rodapé do celular, com `scroll-padding` igual à altura dela para o foco nunca ficar escondido.

## Shapes

Raio 8 px em botões e campos, 12 px em cartões; pílula apenas em selos. A hierarquia de raios é intencional: nem tudo tem o mesmo raio.

## Components

`button-primary` é o único botão de destaque; `button-primary-hover` escurece para `ink`. `card` agrupa serviço ou membro da equipe. Estados obrigatórios de todo componente interativo: foco visível (contorno 2 px em `primary`, deslocamento 2 px), desabilitado, carregando, erro.

## Do's and Don'ts

- Faça: foto real da equipe, endereço e horário acima da dobra, textos de erro com o que fazer.
- Faça: calcule contraste de qualquer cor nova antes de usá-la.
- Não faça: usar `highlight` como texto ou botão; gradiente roxo; três cartões idênticos com ícone em círculo; depoimentos sem fonte.
- Não faça: inventar horários, preços ou prazos na interface.
````

## Regras de preenchimento

1. **Cada valor tem origem**: o código, o guia de marca ou uma resposta aprovada do usuário. Valor sem origem não entra.
2. **Prosa específica**: papel da cor, razão da escala, regra de uso. Adjetivos genéricos ("moderno", "limpo") não são especificação.
3. **Contraste calculado** pela fórmula WCAG e anotado ao lado do token ([contraste-wcag](${CLAUDE_PLUGIN_ROOT}/skills/design-tokens/references/contraste-wcag.md)).
4. **Seção sem conteúdo real** vai em `omitted`, não preenchida com texto vazio.
5. **Tokens de componente** referenciam tokens básicos por `{...}`; não repita hex dentro de `components`.
6. **Versão**: mantenha `version: alpha` e revise o arquivo quando o formato mudar.
7. **Um DESIGN.md por produto**. Em monorepo, um por pacote de UI, com o caminho no CLAUDE.md.

## Lint e exportação (não executados pela skill)

- CLI do formato: pacote `@google/design.md`. Comandos do README: `lint` (valida a estrutura; saída JSON por padrão; sai com código 1 em erro), `diff` (compara dois arquivos e sinaliza regressões), `export` (formatos `json-tailwind`, `css-tailwind`, `tailwind` e `dtcg`) e `spec` (imprime a especificação, com `--rules` para as regras).
- Onze regras de lint: erro `broken-ref`; avisos `missing-primary`, `contrast-ratio`, `orphaned-tokens`, `missing-typography`, `section-order`, `unknown-key`, `token-like-ignored`; informativas `token-summary`, `missing-sections`, `omitted-rules`.
- Riscos: alpha (mudanças sem aviso); `npx` baixa e executa código de terceiros; exemplo de saída do lint com contraste inconsistente com a fórmula WCAG; nome e versão do pacote devem ser conferidos no registro. Se o usuário decidir rodar, use versão fixada num projeto descartável e trate a saída como pista, não como prova.
- No Windows PowerShell, o README indica a forma `npx -p @google/design.md designmd` para evitar falha de resolução do comando (conferido; confirme na versão que fixar).
