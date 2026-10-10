# Estrutura de um design system (bundle)

Template T-13. Uso: `design-init` (modo bundle) e `design-brief` (modo `brief-ds`). Estrutura inspirada no bundle Mo baile do usuário (`design-systems/mo-baile/`); a evidência de cada item está em [design-system-da-casa](../../references/design-system-da-casa.md). É um esqueleto de **organização**: cores, fontes, métricas e nomes de componentes vêm do produto, nunca deste arquivo. Substitua cada `[___]`; item sem conteúdo real fica de fora e é listado em "Omitido".

## Árvore recomendada

```text
<design-system>/
  SKILL.md              ponto de entrada para IA (frontmatter name, description; manda ler o readme)
  readme.md             Fontes, Índice, Componentes, Mapeamento origem→componente,
                        Intentional additions, CONTENT FUNDAMENTALS, VISUAL FOUNDATIONS,
                        ICONOGRAPHY, Substituições a validar
  SOURCES.md            repo, branch, data do último sync, mapa tela→arquivos, tokens→tema nativo
  styles.css            só @import dos tokens e do CSS dos componentes
  tokens/               colors, typography, spacing, shape, materials, motion (+ fonts)
  components/<grupo>/   X.<ext> + X.d.ts (ou tipos) + X.prompt.md; <grupo>.card.html
  guidelines/           um card por decisão (cor, contraste, tipo, espaço, raio, material, movimento)
  ui_kits/<plataforma>/ protótipo + README "o que mudou em cada tela, e por quê"
  _adherence.<lint>     regras de aderência derivadas do contrato
  _ds_manifest.json     namespace + lista de componentes com sourcePath
```

## 1. Tokens em camadas

| Camada | O que contém | Regra |
| --- | --- | --- |
| Marca (literais) | Cores da identidade como são | Pode não passar no contraste; não é usada direto em texto nem controle |
| Primitivos acessíveis | Derivados da marca com contraste medido | Só referenciados |
| Semânticos | `[categoria]-[papel]-[estado]` (rótulos, fundos, destaque, foco, seleção, status) | O que componentes consomem; par `on-*` por fundo semântico |
| Componente | Decisões específicas, sempre apontando para semânticos | Opcional em sistemas pequenos |

Aparências como sobrescrita, sem mudar nomes: claro (base), escuro, alto contraste e a combinação. Fallbacks de sistema também como sobrescrita: reduzir transparência (material vira sólido) e reduzir movimento (molas viram `linear`, durações curtas). Anote o tipo do token em comentário quando a ferramenta usar (`@kind`).

| Arquivo | Conteúdo | Contraste calculado |
| --- | --- | --- |
| `tokens/colors` | [marca, derivados, rótulos, fundos, destaque, seleção, status] | [tabela par → razão → tema] |
| `tokens/typography` | [escala nomeada com line-height e tracking pareados; mono para dado técnico] | n/a |
| `tokens/spacing` | [escala em grade + métricas com nome de intenção] | n/a |
| `tokens/shape` | [raios (regra: interno = externo − espaçamento) e sombras por papel] | n/a |
| `tokens/materials` | [material por camada e regra de empilhamento] | [fallback sólido] |
| `tokens/motion` | [duração perceptual + bounce como fonte; durações fixas do resto] | n/a |

## 2. Componentes: contrato

Para cada componente:

| Peça | Conteúdo mínimo |
| --- | --- |
| Implementação | [arquivo] |
| Tipos | Props fechadas em uniões literais (`variant`, `size`, `state`) |
| `X.prompt.md` | Uma frase de quando usar; ação destrutiva nunca é a padrão; exemplo canônico de uso |
| Teclado e leitor de tela | [teclas, `aria-label`, tooltip em botão só com ícone, foco visível] |
| Estados | padrão, hover, foco, pressionado, desabilitado, carregando, erro, vazio; janela ou contexto inativo quando existir |
| Card | Revisão visual do grupo, com a variante de acessibilidade ao lado |

Status é sempre ícone + cor + texto (enum fechado).

## 3. Guidelines

Um card por decisão, curto e demonstrativo, mostrando o token em uso e a variante de acessibilidade lado a lado. Lista inicial: [cores e contraste, tipografia e mono, espaço e raios, materiais, movimento, marca].

## 4. Lint de aderência

Regras sugeridas, nível `warn`, geradas a partir dos tipos: [cor hex crua] · [px/dp/pt cru em espaço, raio e fonte] · [família de fonte fora do sistema] · [import fora do índice] · [prop ou valor de variante fora do contrato, com a lista válida na mensagem]. Ferramenta: [ESLint/Stylelint/oxlint | detekt/Android Lint | SwiftLint]. O plugin não instala nem executa o lint; entregue a regra e o comando para o usuário decidir.

## 5. Fundamentos de conteúdo

| Tema | Regra do produto |
| --- | --- |
| Idioma e tratamento | [pt-BR, "você" | ___] (Suposição até o usuário confirmar) |
| Botão | [verbo + objeto; caixa; reticências quando abre painel (regra de plataforma) ] |
| Erro | O que houve + o que fazer; sem código técnico |
| Estado vazio | Uma frase + uma ação |
| Tooltip | Frase curta com o efeito |
| Destrutivo | Nomeado pelo verbo, nunca "OK" |
| Termos técnicos | [como ficam: fonte mono, não traduzir] |
| Emoji | [permitido | não] |

## 6. Fontes e mapeamento

| Seção | Conteúdo |
| --- | --- |
| Fontes | Insumos usados (catálogo de telas, repositório e branch, ícone, marca) |
| Mapeamento origem → componente | [componente do código atual → componente do DS] |
| Intentional additions | [o que não existia no produto + por quê] |
| Substituições a validar | [fonte, ícones, cor de destaque trocados + risco] |
| Escopo | [redesenho: "sem tirar nem inventar funções" | produto novo: limite é o brief] |

## 7. UI kit

Por tela: mudança · motivo · estados cobertos (vazio, erro, carregando, offline) · atalhos ou gestos. Painel de estados no protótipo: aparência, alto contraste, reduzir movimento e transparência, contexto inativo.

## 8. `SKILL.md` do design system

```markdown
---
name: [nome-do-produto]-design
description: Use para gerar interfaces e assets no padrão do [produto]: tokens, componentes, fundamentos de conteúdo e kit de UI.
user-invocable: true
---
Leia o readme.md e explore tokens, componentes e guidelines. Em protótipo estático, copie os assets e gere HTML. Em código de produção, siga os contratos e o lint de aderência. Sem orientação do usuário, pergunte o que construir.
```

## Omitido

[Itens que não se aplicam, com o motivo.]

## Não verificado

[O que não foi renderizado, medido ou executado.]
