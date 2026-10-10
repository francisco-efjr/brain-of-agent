# Drift, release e plano de migração de tokens

Drift é a distância entre o que o sistema de tokens diz e o que o código faz. O checklist abaixo adapta a governança de design system do repositório `design-system-ops` (MIT, V-32; só o README foi lido) e as regras de projeto de V-21; a redação é própria. As buscas são de leitura e não alteram nada.

## Sumário

- [Checklist de drift](#checklist-de-drift)
- [Buscas por Grep](#buscas-por-grep)
- [Script opcional de variáveis CSS](#script-opcional-de-variáveis-css)
- [Regras de release](#regras-de-release)
- [Tabela de migração](#tabela-de-migração)
- [Exemplo de relatório](#exemplo-de-relatório)

## Checklist de drift

| Tipo | Sinal | Impacto típico |
| --- | --- | --- |
| Componente sem token | estilos do componente só com valores literais | médio |
| Valor fixo no código | `#hex`, `rgb(`, `px` de espaçamento ou raio fora dos arquivos de tokens | médio; alto se for cor de marca |
| Nome fora do padrão | `--blue-button-2`, `--newColor` | baixo a médio |
| Camada errada vazando | componente consumindo `color.primitive.*` | médio: quebra o tema |
| Referência desconhecida ou circular | `{color.semantic.text.main}` que não existe | alto: build quebra ou valor some |
| Gerado editado à mão | alteração em arquivo marcado "gerado" | alto: perde na próxima geração |
| Estado ausente | componente sem foco, desabilitado, carregando ou erro | médio a alto (acessibilidade) |
| Nota de acessibilidade ausente | sem teclado, papel ou contraste documentados | médio |
| Contraste semântico violado | par texto/fundo abaixo de 4,5:1 ou 3:1 | alto |

## Buscas por Grep

Escopo: `**/*.{css,scss,tsx,jsx,vue,svelte,html}`, excluindo `node_modules`, `dist`, `build` e a pasta de tokens/gerados (o objetivo é achar o que está **fora**). Na ferramenta `Grep`, escreva `|` para alternância (o `\|` de tabelas Markdown é só escape).

| O que achar | Padrão | Leitura |
| --- | --- | --- |
| Cores hex | `#[0-9a-fA-F]{3,8}\b` com `output_mode: count` | quantidade por arquivo; picos indicam componentes sem token |
| Cores funcionais | `(rgb\|rgba\|hsl\|hsla\|oklch)\(` | idem |
| Espaçamento literal | `(margin\|padding\|gap)[a-z-]*:\s*[0-9.]+(px\|rem)` | compare com a escala |
| Raio literal | `border-radius:\s*[0-9.]+(px\|rem)` | quantos valores distintos existem? |
| Sombras literais | `box-shadow:\s*[^v;]` | sombra que não começa por `var(` |
| Duração literal | `(transition\|animation)[a-z-]*:[^;]*[0-9.]+m?s` | compare com tokens de movimento |
| Uso de primitivo em componente | `var\(--color-primitive` ou `color\.primitive` fora de tokens | camada errada vazando |
| Variável definida | `--[a-z0-9-]+\s*:` | lista do que existe |
| Variável usada | `var\(--[a-z0-9-]+` | confronte com a lista definida |
| Marca de gerado | `(do not edit\|DO NOT EDIT\|auto-generated\|@generated)` | descobrir quais arquivos não editar |

Limites: utilitários do Tailwind, CSS-in-JS dinâmico e temas gerados em tempo de execução escapam dos padrões. Registre o comando exato e o escopo no relatório e nunca conclua "sem drift" a partir de zero acertos; diga "o padrão não encontrou ocorrências em X".

## Script opcional de variáveis CSS

Somente leitura, biblioteca padrão. Rode apenas com a autorização do usuário, num arquivo temporário fora do projeto, apontando para a pasta de CSS. Compara variáveis definidas e usadas.

```python
import re, sys, pathlib
raiz = pathlib.Path(sys.argv[1])
definidas, usadas = set(), set()
for p in raiz.rglob("*"):
    if p.suffix in {".css", ".scss", ".tsx", ".jsx", ".vue", ".svelte", ".html"} and "node_modules" not in p.parts:
        t = p.read_text(encoding="utf-8", errors="replace")
        definidas |= set(re.findall(r"(--[a-z0-9-]+)\s*:", t))
        usadas |= set(re.findall(r"var\((--[a-z0-9-]+)", t))
print("usadas e nunca definidas:", sorted(usadas - definidas))
print("definidas e nunca usadas:", sorted(definidas - usadas))
```

Variáveis definidas por bibliotecas externas e variáveis lidas por JavaScript geram falsos positivos; revise a lista antes de agir.

## Regras de release

| Mudança | Versão |
| --- | --- |
| Renomear ou remover token; mudar o significado de um token; remover prop ou variante de componente; mudar contrato de acessibilidade (por exemplo, tecla) | major |
| Token novo ou componente novo, compatível; prop opcional nova | minor |
| Ajuste de valor que mantém o significado (cor ligeiramente mais escura com contraste recalculado), correção de bug, documentação | patch |

Antes de qualquer major, publique um aviso de depreciação por pelo menos uma versão minor quando o ciclo do produto permitir, com o substituto. Um ajuste de cor de marca que muda a aparência de todo o produto é visível para o usuário final: trate como mudança que exige aprovação do dono da marca, mesmo sendo patch tecnicamente.

## Tabela de migração

Antes de renomear ou trocar token de marca, apresente a tabela e espere a confirmação do usuário.

| Nome antigo | Nome novo | Camada | Componentes e arquivos afetados | Ordem | Verificação |
| --- | --- | --- | --- | --- | --- |
| `--brand-green` | `color.semantic.action.primary.bg` | semântico | Button, Link, Badge (`src/ui/Button.css:12`, ...) | 1 | par com `action.primary.fg` ≥ 4,5:1 |
| `--gray-light` | `color.semantic.surface.canvas` | semântico | Layout, Card | 2 | contraste com `text.primary` |
| `--shadow-1` | `elevation.raised` | semântico | Card, Menu | 3 | comparação visual antes/depois (captura) |

Passos de execução (só com confirmação): (1) adicionar os nomes novos mantendo os antigos como alias depreciados; (2) migrar consumidores componente a componente; (3) remover os antigos em release major; (4) rodar o build de tokens e os testes do projeto, se existirem, e relatar o que rodou.

## Exemplo de relatório

```text
Fonte: tokens/tokens.json · Gerados: src/styles/tokens.css, src/tokens.ts (edição à mão proibida)
Inventário: 41 cores literais em 9 arquivos (maior: Checkout.css, 14); 23 valores de espaçamento fora da escala; 4 durações literais
Drift:
 D-01 | cor literal #0b5d4f em Button.css:12 e Link.css:8 | camada: componente | impacto: médio | usar color.semantic.action.primary.bg
 D-02 | Card.css:20 usa var(--color-primitive-slate-600) | camada errada | médio | usar color.semantic.text.secondary
 D-03 | referência {color.semantic.text.main} inexistente em tokens.json:44 | alto | corrigir para text.primary
Release sugerido: major (renomeações) ou minor se mantiver aliases depreciados
Contraste: text.primary/canvas 14,35:1 ok; text.secondary/canvas 6,42:1 ok; action.primary.fg/bg 7,80:1 ok (calculado)
Não verificado: build de tokens não executado; Storybook não aberto; Figma não consultado
Aguardando confirmação: 3 renomeações da tabela de migração
```
