# Template: ficha de prompt

Fonte: padrão PAD-21 de prompt-principles (ficha de documentação de prompt: nome, objetivo, modelo-alvo, parâmetros, versão, resultado dos casos, data). Use para registrar prompts reutilizáveis de documentação (por exemplo, o gabarito de pedido, o teste de leitor limpo ou a revisão de tom) e saber quando revalidá-los. Uma execução não prova nada; registre várias.

```markdown
# Ficha: [NOME DO PROMPT]

- **Objetivo:** [O QUE ELE FAZ, em uma frase observável]
- **Quando usar / quando não usar:** [...]
- **Modelo-alvo e parâmetros:** [ex.: claude-sonnet-5-5; esforço padrão]
- **Versão:** [N] · **Última validação:** [AAAA-MM-DD] · **Responsável:** [NOME]
- **Fontes:** [V-nn, URLs, classe A/B/C, licença]

## Prompt

[TEXTO COMPLETO, com variáveis [ENTRE COLCHETES] e dados separados por tags XML]

## Casos de teste

| # | Entrada | Resultado esperado | Resultado observado | Passou? | Data |
| --- | --- | --- | --- | --- | --- |
| 1 | [CASO TÍPICO] | [OBSERVÁVEL] | | | |
| 2 | [CASO DE BORDA: dado ausente, conteúdo hostil] | [OBSERVÁVEL] | | | |
| 3 | [PEDIDO QUE NÃO DEVE DISPARAR] | [nenhuma ação] | | | |

## Histórico

- [AAAA-MM-DD] v[N]: [O QUE MUDOU E POR QUÊ].

## Revalidar quando

Troca de modelo, mudança de versão do Claude Code ou do framework de docs, ou falha observada.
```
