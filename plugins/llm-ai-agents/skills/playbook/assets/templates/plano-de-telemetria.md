# Plano de telemetria de chamadas LLM

Fonte: V-33 (OpenTelemetry GenAI semconv, Langfuse, OpenLLMetry). A convenção está em status **Development**: nomes mudam. Copie os nomes de atributo do registro da versão que você adotar antes de gravar em código. Pipeline, SLO e alertas pertencem a `/sre-observability:playbook`.

- **Convenção e versão fixadas:** [repositório/commit/tag, data]
- **Backend escolhido:** [...] · **Um trace de ponta a ponta validado antes de expandir:** [sim/não]

## Estrutura

- Um **trace** por pedido do usuário; um **span** por chamada de modelo e um por chamada de tool.
- `session_id` em conversa multi-turno; `user_id` somente se necessário e permitido.
- Tags de versão do prompt e do modelo, para comparar regressões.

## Campos mínimos do span de modelo

| Campo | Atributo (conferir na versão adotada) | Obrigatório? |
| --- | --- | --- |
| Operação | `gen_ai.operation.name` | sim |
| Provedor | `gen_ai.provider.name` (`anthropic`) | sim |
| Modelo solicitado | `gen_ai.request.model` | se disponível |
| Tokens de entrada / saída | `gen_ai.usage.input_tokens` / `gen_ai.usage.output_tokens` | recomendado |
| Cache (leitura / escrita) | `gen_ai.usage.cache_read.input_tokens` / `gen_ai.usage.cache_write.input_tokens` | recomendado |
| Motivo de término | `gen_ai.response.finish_reasons` | recomendado |
| ID da resposta | `gen_ai.response.id` | recomendado |
| Tipo de erro | `error.type` | se houve erro |

Provedor Anthropic: o instrumentador soma leitura e escrita de cache em `gen_ai.usage.input_tokens`; tokens de raciocínio entram em `gen_ai.usage.output_tokens`. Métricas: `gen_ai.client.inference.usage.input_tokens`, `gen_ai.client.inference.usage.output_tokens`, `gen_ai.client.inference.duration` (histograma em segundos).

## Política de conteúdo

| Conteúdo | Padrão | Condição para ligar |
| --- | --- | --- |
| Prompt, resposta, instruções de sistema, argumentos e resultados de tools | **desligado** | consentimento, redação de dados pessoais, retenção definida |
| Custo | calculado dos tokens com a tabela de preços datada (nunca inventado) | n/a |

## Verificações

- [ ] Ambos os campos de cache aparecem; ambos zero indica prefixo variável ou abaixo do mínimo
- [ ] Erros de tool e `refusal`/`max_tokens` aparecem como estados distintos
- [ ] Nenhum segredo nem dado pessoal nos atributos
- [ ] Versão da convenção fixada em dependências
