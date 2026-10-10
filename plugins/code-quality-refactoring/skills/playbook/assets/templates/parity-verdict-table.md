# Tabela de veredito de paridade

Migração: [origem] -> [destino]  ·  Data: [AAAA-MM-DD]  ·  Juiz: [comando]

Critérios: PROVADO = testes rodados do zero nos dois lados e saídas iguais nos cenários listados · PARCIALMENTE PROVADO = falta evidência (máximo quando o sistema antigo não roda) · NÃO PROVADO = sem evidência ou com diferença de saída.

| Módulo | Cenários rodados nos dois lados | Resultado original | Resultado novo | Veredito | Pendências |
| --- | --- | --- | --- | --- | --- |
| [módulo] | [cenário 1; cenário 2] | [saída/hash] | [saída/hash] | PROVADO / PARCIALMENTE PROVADO / NÃO PROVADO | [diferença de saída = pendência] |

Resumo: [N] provados, [N] parcialmente provados, [N] não provados.
Nada é declarado migrado sem o juiz rodado do zero sobre o resultado final. Evidência: [comando, saída, data].
