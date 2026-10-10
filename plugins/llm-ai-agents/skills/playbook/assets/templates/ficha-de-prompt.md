# Ficha de prompt

Base: PAD-21 e C-18 (prompt-principles). Uma ficha por prompt versionado (system prompt, template, prompt de agente, juiz). Guarde ao lado do arquivo do prompt.

| Campo | Valor |
| --- | --- |
| Nome e arquivo | |
| Objetivo (uma frase, resultado esperado) | |
| Modelo-alvo e data de conferência | |
| Parâmetros (`effort`, temperatura, `max_tokens`, saída estruturada) | manter padrão salvo ganho medido |
| Versão | |
| Dono | |
| Entradas esperadas e formato de saída | |
| Ferramentas disponíveis e confirmações exigidas | |
| Cartão A/B/C (se for agente) | link |
| Suíte de regressão e comando | |
| Resultado dos casos (data, denominador, falhas críticas) | |
| Mudanças desde a versão anterior (e a falha real que as motivou) | |
| Limitações conhecidas e Suposições | |

## Regras

- Ao trocar de modelo, reexecute a suíte antes de aceitar a troca; resultados antigos não valem para o novo.
- Regra nova entra após falha observada, com a origem e a data.
- Sem execução: escreva "projetado, não executado". Autoavaliação do mesmo modelo não é validação independente.
