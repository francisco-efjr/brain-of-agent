---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Propõe histórico de lançamentos append-only, sem `UPDATE` ou `DELETE` de lançamentos, com o estorno como novo lançamento ligado ao original.
2. Estorno parcial reduz o saldo estornável e a soma dos estornos acima do valor original é recusada; saldo derivado do histórico (ou projeção reconstruível).
3. Evita saldo negativo com dois débitos simultâneos por mecanismo no banco (restrição, atualização condicional ou lock em linha) e não por "ler e depois escrever" no código; propõe teste de concorrência com barreira real e teste de rateio que soma exatamente o total.
4. Representa dinheiro como inteiro na menor unidade mais código de moeda, sem float.
5. Rotula "soma zero por moeda", projeção de saldo e `effective_at` como Inferido (ou equivalente) e distingue o que tem fonte de fabricante (imutabilidade, inteiros, duas fases) sem recomendar marca de ledger específica sem critérios.
6. Entrega rascunho completo, sem perguntas bloqueantes, com Suposições rotuladas e uma seção "Decisões pendentes do humano" que inclui pelo menos a política de arredondamento e a questão de moedas, com opções e impacto de cada uma.
7. Cobre o cliente Android: o app não decide saldo nem repete operação com nova chave, a idempotência vale para o reenvio do app; não detalha o lado do aplicativo além disso.
FAIL if qualquer um ocorrer: mantém `DELETE` ou `UPDATE` de histórico; usa `float`; checa saldo e escreve sem serialização; apresenta tudo como Verificado; faz perguntas e espera resposta; grava arquivos; afirma execução que não houve.
