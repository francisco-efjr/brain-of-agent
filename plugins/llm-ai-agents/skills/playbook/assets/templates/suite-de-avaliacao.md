# Suíte de avaliação

Fontes: V-09 (Anthropic, "Demystifying evals") e brain-of-agent `ia-e-llm.md` (MIT, adaptado). Status obrigatório até alguém rodar: **projetada, não executada**.

- **Sistema avaliado (modelo, prompt/versão, ferramentas, ambiente):** [...] · **Data:** [...]
- **Produto:** [classificador / extração / RAG / agente / skill ou plugin]
- **Falhas críticas (separadas da nota global):** [ex.: inventar dado, vazar dado de outro tenant, declarar teste não executado]
- **Conjuntos:** desenvolvimento [N] · regressão [N] · validação reservada [N, nunca usada para editar] · produção monitorada [amostra autorizada e minimizada]
- **Meta de tamanho:** 20 a 50 tarefas de falhas reais, com casos positivos e negativos

## Casos

| ID | Entrada | Contexto | Permissões | Esperado | Falhas críticas | Método (regex / tool_used / file_exists / rubrica 0-1-2 / juiz binário) | Segmento | Origem (falha real, pré-lançamento, sintético) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [id] | [...] | [...] | [...] | [...] | [...] | [...] | [...] | [...] |

Inclua perguntas respondíveis (recusa indevida conta como falha) e ao menos um caso negativo. O executor recebe entrada e artefatos; o avaliador recebe critérios; não entregue o esperado ao executor.

## Exemplo de caso (JSON, ilustrativo)

```json
{
  "id": "rag-politica-ausente",
  "input": "Quanto custa cancelar meu plano?",
  "context": [{"id": "doc-1", "text": "O plano mensal custa R$ 40."}],
  "permissions": ["read_context"],
  "expected": "Informar que o contexto não contém a taxa de cancelamento; pedir a política aplicável.",
  "critical_failures": ["Inventar taxa", "Citar trecho inexistente"],
  "grading": ["revisão factual por trecho", "rastreio de citações"]
}
```

## Protocolo (congelar antes da rodada)

Conjunto, rubrica, versão, modelo e configuração, ferramentas, orçamento, regra de parada. Baseline e candidata nas mesmas condições, ambientes limpos. Execuções por caso: [N]. Métricas: sucesso por tentativa (com denominador), pass@k, pass^k, falhas críticas por tipo, p50/p95 de latência, custo por tarefa concluída.

## Resultado

| Versão | Casos únicos | Tentativas | Sucesso por tentativa | pass^k | Falhas críticas | Custo | Observações |
| --- | --- | --- | --- | --- | --- | --- | --- |

Incerteza: 27/30 é 90% segundo aquele juiz e aquela amostra (Wilson 95% ≈ 74% a 97%); zero falhas em 30 não prova risco zero (regra 3/n ≈ 10%). Sem rótulo humano: "avaliação por IA". Sem execução: "caso projetado".
