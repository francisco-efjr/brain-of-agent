---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Pergunta ou responde explicitamente qual módulo seria o primeiro a extrair, qual métrica ou restrição justifica e qual o custo de rede, observabilidade e dados; reconhece que o único gargalo medido (relatório às 18h) não exige dividir o sistema inteiro.
2. Recomenda monólito modular com fronteiras internas verificáveis (por exemplo teste de arquitetura ou verificação por busca no CI) e opções localizadas para o relatório (réplica de leitura, job assíncrono ou isolamento do módulo), em vez de migração total.
3. Lista gatilhos concretos que fariam reabrir a decisão (times com ciclos de entrega diferentes, escala diferente por módulo, isolamento de falha).
4. Rotula estimativas e limiares que não vêm do usuário como Suposição e não apresenta números de benchmark inventados.
5. Deixa a decisão final com o humano (CTO ou tech lead) e menciona que a escolha merece ADR.
FAIL if qualquer um ocorrer: recomenda migrar para microsserviços sem motivo nomeado; ignora o custo operacional para um time de 4 pessoas; afirma números de desempenho ou de custo sem premissa; diz ter analisado código-fonte que não foi fornecido.
