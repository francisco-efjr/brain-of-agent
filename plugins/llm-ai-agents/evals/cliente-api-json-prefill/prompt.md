---
name: cliente-api-json-prefill
description: "Mede se o plugin revisa código cliente da API que usa prefill para forçar JSON, trocando por saída estruturada, tratando refusal e max_tokens, avisando que mudar o formato invalida o cache e sem afirmar que executou."
tags: [llm-ai-agents, llm-api-client-review]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Troca o prefill por output_config.format com json_schema e additionalProperties false, trata stop_reason refusal e max_tokens antes do json.loads, avisa que mudar o formato invalida o cache de prompt, aponta o parâmetro beta output_format como obsoleto, não inventa parâmetros e diz que não executou o código."
model: sonnet
---
Esse trecho em Python às vezes quebra com JSONDecodeError em produção, uns 2% das chamadas. Revisa e me diz o que mudar. Usamos o SDK oficial da Anthropic em Python e o modelo claude-sonnet-5-5.

```python
import json
import anthropic

client = anthropic.Anthropic()

def extrair_pedido(texto: str) -> dict:
    resp = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=300,
        system="Extraia do texto o nome do cliente e o valor do pedido. Responda só com JSON.",
        messages=[
            {"role": "user", "content": texto},
            {"role": "assistant", "content": "{"},
        ],
    )
    return json.loads("{" + resp.content[0].text)
```
