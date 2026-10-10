# ADR [ID] — [workflow, agente, tool MCP, hook ou job para: PROCESSO]

Estado: [proposta/aceita/substituída] · Data/revisão: [AAAA-MM-DD / commit]
Adaptado de `adr.md` do brain-of-agent (Francisco Edson, MIT). Escreva ADR só para decisão material; critério de escolha: V-08 (workflow antes de agente; uma chamada antes de várias etapas).

## Contexto

Problema, restrições, volume, quem controla a entrada, dados envolvidos, tolerância a falha e a duplicata, custo de um erro, stack existente.

Quatro perguntas (V-08):
1. Os passos são conhecidos de antemão? [sim/não]
2. A decisão exige julgamento sobre entrada aberta? [sim/não]
3. O custo do erro é alto (exige verificação entre etapas ou aprovação humana)? [sim/não]
4. Uma chamada resolve? [sim/não]

## Opções

| Opção | Benefício | Custo/risco | Compatibilidade | Evidência |
| --- | --- | --- | --- | --- |
| A. Workflow/script determinístico | | | | |
| B. Workflow com um passo de LLM (schema de saída) | | | | |
| C. Agente com limite de passos e de custo | | | | |
| D. Tool MCP (+ skill) / hook / job `claude -p` | | | | |

## Decisão

Opção escolhida e por quê. Hipóteses ainda não confirmadas (rotule Suposição). Trifecta: [pernas presentes e a quebrada].

## Medição que justificaria subir de nível

Métrica, amostra e limiar (ex.: "extração correta em 30 documentos reais ≥ 95%") que, se não atingida pela opção escolhida, justifica adicionar etapa, ferramenta ou agente. Sem medição, não suba.

## Consequências

Complexidade, operação, dados, segurança, testes e custo recorrente. Limites de reversibilidade: reverter binário não desfaz e-mail enviado, cobrança ou conversão de dado; não prometa rollback de dados perdidos.

## Validação e revisão

Critérios observáveis, experimento ou teste que sustenta a escolha. Condição que exige reconsiderar a decisão (volume, custo, taxa de erro, mudança de provedor). Links: plano de integração, matriz de trifecta, fontes (V-xx).
