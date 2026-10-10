# Detectores por Grep: pistas verificáveis

Uso: a ferramenta `Grep` (ripgrep, regex do Rust) roda sem instalar nada e sem alterar arquivos. Cada acerto é uma pista sobre o **markup**, não prova de como a página renderiza. Leia as linhas ao redor antes de registrar o achado e rotule: acerto confirmado em contexto = `arquivo:linha` com Verificado (no código); efeito visual = Inferido até haver captura.

Limitação: o ripgrep padrão não tem lookahead nem lookbehind, então "tag sem atributo X" é feito listando as tags e conferindo. Estilo gerado por CSS-in-JS, utilitários do Tailwind e valores calculados em tempo de execução escapam de várias regras; diga isso no relatório.

Este padrão ("regras determinísticas + julgamento do modelo") vem do projeto Impeccable (Apache-2.0, V-24); as regras abaixo são redação própria e não executam nem instalam o detector dele.

## Sumário

- [Padrões](#padrões)
- [Como registrar um acerto](#como-registrar-um-acerto)
- [Contagens úteis](#contagens-úteis)

## Padrões

Atenção: na tabela, `\|` é só o escape do Markdown para a barra vertical; no campo `pattern` do `Grep` escreva `|` (alternância). `\|` casaria uma barra literal.

Escopo sugerido: `glob` `**/*.{css,scss,html,jsx,tsx,vue,svelte}`, excluindo `node_modules`, `dist` e `build`.

| Pista | Padrão (`Grep`) | Categoria | O que confirmar no contexto |
| --- | --- | --- | --- |
| Foco removido | `outline:\s*(none\|0)\b` | 5 | existe `:focus-visible` ou `box-shadow` substituto no mesmo seletor? |
| Transição em tudo | `transition(-property)?:\s*all\b` | 7 | trocar por propriedades explícitas |
| Zoom bloqueado | `user-scalable\s*=\s*no\|maximum-scale\s*=\s*1\b` | 6 | viola a possibilidade de ampliar (WCAG 1.4.4) |
| `tabindex` positivo | `tabindex\s*=\s*["']?[1-9]` | 5 | quebra a ordem de foco |
| Div clicável | `<(div\|span)[^>]*(onClick\|onclick\|@click)` | 5 | tem `role`, `tabindex` e teclado? Quase sempre deveria ser `<button>` |
| Lorem ipsum | `-i` `lorem ipsum` | 8 | texto de preenchimento em tela entregue |
| Cor literal | `#[0-9a-fA-F]{3,8}\b` | 3 | fora do arquivo de tokens indica drift (contar por arquivo) |
| Fonte pequena | `font-size:\s*(?:[0-9]\|1[01])px` | 2 | corpo abaixo de 12 px; rótulo pequeno só se for legenda |
| Gradiente roxo | `-i` `(linear\|radial)-gradient\([^)]*(purple\|violet\|indigo\|#[6-8][0-9a-f]{2}[0-9a-f]{3})` | 9 | heurística fraca; confirmar o tom visualmente |
| Borda lateral de acento | `border-left:\s*[2-6]px\s+solid` | 9 | em cartão arredondado vira sinal de template |
| Texto sempre centrado | `text-align:\s*center` | 9 | contar; muitos acertos em títulos, descrições e cartões |
| Movimento reduzido ausente | `prefers-reduced-motion` | 7 | se há `animation` ou `transition` e a contagem de `prefers-reduced-motion` é zero, é achado |
| Animação | `@keyframes\|animation:\|transition:` | 7 | listar para conferir propósito |
| Imagem | `<img\b[^>]*>` | 6 e a11y | conferir `alt`, `width`, `height` e `loading` linha a linha |
| Placeholder como rótulo | `<input\b[^>]*placeholder=` | 5 e a11y | há `<label for>` ou `aria-label`? Conferir o campo |
| Foco automático | `autoFocus\|autofocus` | 6 | no celular abre o teclado e rouba o contexto |
| Emoji decorativo | `[\x{1F300}-\x{1FAFF}]` | 9 | em títulos e marcadores; ícone de status com texto é aceitável |
| Texto de herói genérico | `-i` `(bem-vindo\s+(a\|ao)\|welcome to\|unlock the power\|libere o poder\|solução completa)` | 8 e 9 | confirmar que é o texto do herói |
| Reticências por três pontos | `\.\.\.` em strings de interface | 2 | polimento: preferir `…` em "Salvando…" |
| Viewport meta ausente | listar `<meta name="viewport"` | 6 | ausência em HTML completo é achado |

Para estrutura de títulos, liste a sequência com `Grep -o` por `<h[1-6]\b` e compare níveis na ordem do arquivo; em componentes o contexto de uso decide.

## Como registrar um acerto

```text
UI-07 | estados | alto | Verificado no código: src/styles/button.css:41 `outline: none` sem :focus-visible no seletor .btn
       Efeito visual: Inferido (sem captura). Correção: `.btn:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 2px; }`
```

Sempre indique qual parte é Verificado (o que o arquivo diz) e qual é Inferido (como renderiza).

## Contagens úteis

- Cores literais por arquivo: `Grep` com `output_mode: count` no padrão de hex; muitos valores únicos fora de `tokens` apontam para drift (veja a skill `design-tokens`).
- Famílias tipográficas: `font-family:` com `output_mode: content`, e conferir quantas distintas.
- Raios: `border-radius:` para ver se há um valor único aplicado a tudo.

Contagens por `Grep` são piso: não acham valores injetados por JavaScript, temas gerados ou utilitários. Nunca declare "não há problema" só porque o padrão não acertou; diga "o padrão não encontrou ocorrências nos arquivos X".
