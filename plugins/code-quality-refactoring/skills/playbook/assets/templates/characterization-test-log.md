# Log de testes de caracterização

Trecho: [arquivo:função]  ·  Data: [AAAA-MM-DD]  ·  Comando: [comando de testes]

Procedimento: escolher entradas relevantes (incluindo bordas e erros), escrever o teste com expectativa provisória, rodar, fixar a saída real como expectativa, nomear pelo comportamento observado, marcar o que parece bug sem corrigi-lo.

| # | Entrada | Expectativa provisória | Saída real (colada) | Nome do teste (comportamento observado) | Possível defeito? | Follow-up |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `calcular_frete(0, 10)` | 0 | 0 | `peso_zero_devolve_zero` | não | |
| 2 | `calcular_frete(5.04, 50)` | 15.08 | 15.1 | `arredonda_para_uma_casa` | sim: perde centavos ("comportamento atual, possível defeito") | corrigir em mudança própria, com aprovação |

Os dois exemplos acima ilustram o preenchimento; a coluna "Saída real" só vale depois de rodar o teste.

Fechamento:
- Testes que protegem regra de negócio (manter): [lista]
- Testes que só prendem detalhe de implementação (propor remover, sem remover): [lista]
- Limites: caracterização fixa também os bugs e não substitui a especificação.
