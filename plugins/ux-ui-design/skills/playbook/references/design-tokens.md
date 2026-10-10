# Design tokens: três camadas, DTCG, DESIGN.md, drift e release

Como estruturar, auditar e migrar tokens sem instalar nem executar ferramentas de terceiros. Fontes: DTCG 2025.10 (V-20), Figma Help (V-21), design.md em alpha (V-23), governança de design system (V-32), Style Dictionary só como referência (V-22), Storybook (V-37) e o critério 3 de qualidade do brain (tokens semânticos). A escrita de tokens em código (`@theme`, variáveis CSS) pertence a `/web-frontend:playbook`; aqui ficam arquitetura, auditoria de drift e plano de migração.

## Sumário

- [Três camadas](#três-camadas)
- [Regras de projeto](#regras-de-projeto)
- [Formato DTCG 2025.10](#formato-dtcg-202510)
- [DESIGN.md (alpha)](#designmd-alpha)
- [Drift e release](#drift-e-release)
- [Dark mode e temas](#dark-mode-e-temas)
- [Contraste dos pares semânticos](#contraste-dos-pares-semânticos)
- [Protocolo de renomeação](#protocolo-de-renomeação)
- [Figma e Style Dictionary](#figma-e-style-dictionary)
- [Defeitos de um exemplo popular](#defeitos-de-um-exemplo-popular)

## Três camadas

| Camada | Papel | Exemplo | Quem consome |
| --- | --- | --- | --- |
| Primitivo | Valor bruto nomeado pela escala, sem significado de uso | `color.teal.600`, `space.4` | Só outros tokens, por referência |
| Semântico | Função na interface, estável entre temas | `color.action.primary`, `color.text.default`, `space.inset.md` | Componentes e telas |
| Componente | Ajuste específico, útil em sistemas maiores | `button.primary.background` | O próprio componente |

O Figma recomenda exatamente esta divisão (primitivos só como referência, semânticos aplicados pelo designer, específicos de componente quando o sistema cresce), coleções "Primitives" e "Tokens" e ocultar os primitivos da publicação (V-21). A ordem semântico/componente é flexível; a regra fixa é **o componente nunca usa valor cru nem primitivo**.

## Regras de projeto

1. Fonte única: `tokens.json` (ou o arquivo de tokens do projeto). Arquivos gerados (CSS, TS) nunca são editados à mão e entram na lista de caminhos permitidos só como saída do build.
2. Nome descreve função, não aparência (`color.feedback.error`, não `color.red`), para o tema poder mudar sem renomear.
3. Todo valor cru (hex, px, ms) fora do arquivo de tokens é achado. Duas escalas paralelas são achado.
4. Componente novo: props tipadas, todos os estados (hover, foco, desabilitado, carregando, erro), operação por teclado, nota de acessibilidade e story. O estado de carregamento mantém o foco e anuncia o texto.
5. Antes de renomear ou trocar token de marca, liste nomes antigos e novos e os componentes afetados e espere confirmação.
6. Rode o build e o lint de tokens do projeto só se existirem, com autorização; relate o que rodou e o que não pôde rodar.

## Formato DTCG 2025.10

Relatório final de comunidade de 2025-10-28 (https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/): **não é padrão W3C** e não está na trilha de padrões, embora o texto de status use também o rótulo "Candidate Recommendation" (conflito interno). A página de rascunho (2026-09-08) diz "preview, não implemente" e cita 2025.10 como a última publicada. Cite sempre "relatório final de comunidade 2025.10, não padrão W3C" e fixe a versão.

Propriedades reservadas confirmadas (V-20): `$value` (obrigatória), `$type`, `$description`, `$extensions`, `$deprecated`, `$extends`, `$root`, `$ref` (JSON Pointer, RFC 6901). Referência por chave `{grupo.token}` só a tokens completos. Tipos: `color`, `dimension`, `fontFamily`, `fontWeight`, `duration`, `cubicBezier`, `number` e compostos (`strokeStyle`, `border`, `transition`, `shadow`, `gradient`, `typography`). Extensão `.tokens` ou `.tokens.json`; tipo de mídia `application/design-tokens+json`.

**Sintaxe dos valores: Inferido.** O relatório 2025.10 representa `color` como objeto (`colorSpace`, `components`, opcionalmente `alpha` e `hex`) e `dimension`/`duration` como objeto `{ "value": n, "unit": "px" }`; rascunhos anteriores aceitavam string (`"#0F766E"`, `"16px"`). VALIDATED não detalhou isso: confira a seção de tipos do relatório antes de gerar o arquivo e declare qual sintaxe usou. Esqueleto completo em `assets/templates/tokens-3-camadas.md`. Regras de verificação: nenhuma referência desconhecida; referência circular é erro; semântico referencia primitivo.

## DESIGN.md (alpha)

Formato do repositório google-labs-code/design.md (Apache-2.0, README declara **alpha**: especificação, schema e CLI mudam; fixe a versão). Front matter YAML de tokens mais as oito seções na ordem canônica: Overview, Colors, Typography, Layout, Elevation & Depth, Shapes, Components, Do's and Don'ts; cada seção com tokens e justificativa em prosa. A CLI tem `lint` (11 regras; sai com 1 em erro), `diff`, `export` (json-tailwind, css-tailwind, dtcg) e `spec`. Ressalvas:

- O exemplo de saída do `lint` na documentação afirma 15,42:1 para #FFFFFF sobre #1A1C1E; a fórmula WCAG dá 17,09:1. Nunca use a mensagem do linter como oráculo de contraste.
- Nenhuma CLI foi executada para este plugin; não a rode sem versão fixada e autorização (ver `ferramentas-e-mcp.md`).
- Bloco de CLAUDE.md que fecha o ciclo: "consulte `DESIGN.md` ao gerar ou alterar UI; não invente cores, fontes ou espaçamentos fora dele; mudanças de token passam por revisão" (CM-15).
- Decisões de design duráveis ficam em arquivo versionado, separadas de fatos do produto (contexto do produto num arquivo, direção visual em outro): o agente consulta antes de gerar ou auditar (V-23, V-24).

## Drift e release

Checklist de drift (V-32, V-21), para o `design-system-auditor`:

| Achado | Como detectar | Camada |
| --- | --- | --- |
| Componente sem token | Grep de `#[0-9a-fA-F]{3,8}`, `rgb(`, `\d+px` em arquivos de componente | componente |
| Valor fixo no código | Mesmo Grep fora de `tokens.*` e do tema | qualquer |
| Nome fora do padrão | Token que não segue `categoria.função.variante` | qualquer |
| Token da camada errada vazando | Componente usando primitivo (`color.teal.600`) | componente |
| Referência desconhecida ou circular | Percorrer `{...}` no JSON | tokens |
| Arquivo gerado editado à mão | Comparar com a saída do build, se o projeto tiver | gerado |
| Estados ou nota de acessibilidade ausentes | Story sem foco, desabilitado, erro | componente |

Release (semver): quebra de API de componente ou de token (remover, renomear, mudar o significado, mudar o tipo) ⇒ **major**; token ou variante nova compatível ⇒ minor; correção de valor sem mudar a API ⇒ patch. Mudança de valor de token de marca é visual para todo consumidor: trate como no mínimo minor e avise.

## Dark mode e temas

Dark mode é um **modo da coleção semântica**, sem mudar nomes (Figma Help, V-21): `color.text.default` aponta para primitivos diferentes por modo. Superfícies escuras usam elevação, não só inversão de luminosidade; texto levemente abaixo de branco puro e acento um pouco menos saturado são regras de polegar (Inferido; origem gstack). Calcule o contraste dos pares **nos dois modos**. Internacionalização e RTL: sem fonte validada (lacuna); declare quando o produto exigir.

## Contraste dos pares semânticos

Tabela para colar no relatório (valores calculados pela fórmula WCAG em 2026-10-10; Verificado, cálculo):

| Par (primeiro plano / fundo) | Razão | Uso |
| --- | --- | --- |
| #1A1C1E / #FFFFFF | 17,09:1 | texto principal |
| #0F766E / #FFFFFF | 5,47:1 | ação primária e links (passa AA) |
| #FFFFFF / #0F766E | 5,47:1 | texto sobre botão primário |
| #B45309 / #FFFFFF | 5,02:1 | aviso (texto) |
| #B42318 / #FFFFFF | 6,57:1 | erro (texto) |
| #667085 / #FFFFFF | 4,97:1 | texto secundário |
| #98A2B3 / #FFFFFF | 2,58:1 | reprova; só decoração sem informação |

Estes valores são exemplos de método, não paleta recomendada: a marca existente vence.

## Protocolo de renomeação

1. Relatório por padrão; nada é editado até a confirmação.
2. Tabela: nome antigo → nome novo → componentes e telas afetados → tipo de release.
3. Ordem de migração: adicionar o novo nome apontando para o mesmo valor (alias), migrar consumidores, marcar o antigo com `$deprecated`, remover na major seguinte.
4. Depois: build e lint de tokens do projeto, se houver e autorizados; senão "Não verificado".

## Figma e Style Dictionary

- Figma: comparação é **somente relatório**; não altere tokens a partir do export. Servidores MCP com ferramentas de escrita podem renomear variáveis e criar tokens no arquivo (V-32): não usar sem pedido concreto a cada vez. Documentação oficial de Dev Mode, REST de variáveis e MCP do Figma: lacuna, Não verificado.
- Style Dictionary (https://styledictionary.com/): a página declara compatibilidade com DTCG e saídas para iOS, Android, CSS e JS, mas não declara licença nem versão atual (V-22). Uso neste plugin: referência de arquitetura "tokens são fonte única; saídas são geradas". Não instalar nem executar; valide licença e versão no repositório antes de adotar.

## Defeitos de um exemplo popular

O blog `claudecode-lab` sobre design system (V-21, classe C) serve só como exemplo de arquitetura. Defeitos encontrados na leitura: a lista de pastas editáveis omite `src/tokens.ts`, que o próprio build gera; um botão secundário usa valor cru `bg-gray-50` contra o conselho do texto; o estado `loading` com `disabled` tira o botão do foco e o spinner `aria-hidden` não anuncia texto; o baseline visual com `--update-snapshots` não avisa sobre diferença entre sistemas operacionais e fontes; Storybook e testes visuais não foram executados pelo autor. Não copie o código.
