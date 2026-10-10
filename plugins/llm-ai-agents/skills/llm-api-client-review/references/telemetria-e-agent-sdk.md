# Telemetria de chamadas LLM e Agent SDK sem supervisão

Base: V-33 (OpenTelemetry GenAI semconv, Langfuse, OpenLLMetry), V-39 (superfícies de agente, Agent SDK), V-13, V-38. Conferido em 2026-10-10. A convenção OpenTelemetry GenAI está em status **Development**: nomes de atributo mudam. Fixe a versão e copie os nomes do registro da versão adotada (`docs/registry`) antes de gravar em código. Cookbook `observability` da Anthropic: um único arquivo (`usage_cost_api.ipynb`), conteúdo não lido.

## Plano mínimo de telemetria (V-33, redação própria)

1. Um span por chamada de modelo e um por chamada de tool; um trace por pedido do usuário; `session_id` em toda conversa multi-turno.
2. Campos mínimos do span de modelo: operação, provedor, modelo solicitado, tokens de entrada e de saída (somando cache onde a convenção do provedor mandar), leitura e escrita de cache, motivo de término, id da resposta, tipo de erro.
3. Latência pelo histograma de duração; custo calculado a partir dos tokens com a tabela de preços datada (ver `llm-decision-gates`), nunca inventado.
4. Conteúdo de prompt e resposta fica desligado por padrão; ligar só com consentimento, redação de dados pessoais e retenção definida.
5. Marcar em tags a versão do prompt e do modelo para comparar regressões.
6. Fixar a versão da convenção usada.
7. Antes de expandir, validar um trace de ponta a ponta no backend escolhido.

## Atributos do span de inferência (página `client-inference.md`, status Development)

| Atributo | Obrigatoriedade | Observação |
| --- | --- | --- |
| `gen_ai.operation.name` | obrigatório | Tipo de operação |
| `gen_ai.provider.name` | obrigatório | Para Anthropic, o valor é `anthropic` |
| `gen_ai.request.model` | obrigatório se disponível | Modelo solicitado |
| `gen_ai.usage.input_tokens` | recomendado | Anthropic reporta tokens de cache fora de `input_tokens`: o instrumentador soma leitura e escrita de cache |
| `gen_ai.usage.output_tokens` | recomendado | Tokens de raciocínio entram aqui |
| `gen_ai.usage.cache_read.input_tokens` | recomendado | Leitura de cache |
| `gen_ai.usage.cache_write.input_tokens` | recomendado | Escrita de cache |
| `gen_ai.response.finish_reasons` | recomendado | Motivo de término |
| `gen_ai.response.id` | recomendado | ID da resposta |
| `error.type` | obrigatório se houve erro | Um dos poucos atributos estáveis, junto de `server.port` e `server.address` |

Métricas definidas na mesma página: `gen_ai.client.inference.usage.input_tokens`, `gen_ai.client.inference.usage.output_tokens` e `gen_ai.client.inference.duration` (histograma em segundos). Convenção do provedor Anthropic: span do tipo CLIENT; nome do span `{gen_ai.operation.name} {gen_ai.request.model}`. Conteúdo de mensagens, instruções de sistema, argumentos e resultados de tools são opt-in e podem conter dados pessoais ("não capturar por padrão").

Fontes: https://github.com/open-telemetry/semantic-conventions-genai (Apache-2.0, 421 estrelas, último commit 2026-10-09; docs em `docs/gen-ai/`) e aviso de migração em https://opentelemetry.io/docs/specs/semconv/gen-ai/.

## Ferramentas de backend (V-33, classe B)

| Ferramenta | Licença / leitura | Ressalva |
| --- | --- | --- |
| Langfuse | MIT, 35.581 estrelas, commit de 2026-10-09 | Modelo de dados: trace = uma requisição; observations aninháveis; session agrupa traces de conversa; `user_id`, `session_id`, `tags` e `metadata` propagam. Score e custo **não verificados** na página lida |
| OpenLLMetry | Apache-2.0, 7.480 estrelas, commit de 2026-10-06 | Instrumenta provedores (inclui Anthropic), bancos vetoriais, frameworks e MCP; o README diz que o SDK não coleta telemetria e manda usar a versão 0.49.2 ou superior |

Nenhuma instalação sem revisão: dependências de telemetria executam código no seu processo e podem enviar dados para fora.

## O que procurar no código (Grep)

- `gen_ai`, `opentelemetry`, `langfuse`, `traceloop` (existe instrumentação?).
- Logs que gravam `messages` ou o texto da resposta (conteúdo em log sem consentimento).
- Pontos onde `usage` é lido (os dois campos de cache são registrados?).
- Retries e fallbacks sem span (invisíveis no custo).

## Agent SDK e superfícies (V-39)

Quatro caminhos: Agent SDK (biblioteca Python e TypeScript que roda o binário do Claude Code, com ferramentas embutidas, hooks, subagentes, MCP, permissões e sessões), CLI, SDK cliente (laço seu ou do tool runner beta) e Managed Agents (a Anthropic hospeda o laço). Para outras linguagens: CLI em subprocesso com `-p` e `--output-format json`.

Agente sem supervisão (checklist):

- [ ] Limite de turnos (`max_turns`) e de orçamento (`max_budget_usd`); a receita de revisão agendada do cookbook usa `permission_mode="dontAsk"`, `max_turns` e `max_budget_usd`. Confirme os nomes na documentação do SDK; as páginas de agent loop, hooks e permissões do SDK não foram lidas.
- [ ] Modo de permissão restritivo e allowlist mínima; sem `bypassPermissions`/`--dangerously-skip-permissions` como padrão. Quando citado, é risco, só em sandbox descartável e repositório confiável.
- [ ] Hooks de segurança para o que deve valer sempre (hook roda com as permissões do usuário; não é fronteira de segurança).
- [ ] Sandbox; segredos fora do contexto do agente.
- [ ] Autenticação por chave de API em produto de terceiros; terceiros não podem oferecer login claude.ai nem limites próprios sem aprovação.
- [ ] Marca: "Claude Code" não é permitida em produto de terceiros; permitidos "Claude Agent" ou "{Seu agente} Powered by Claude".
- [ ] Os cookbooks exigem `ANTHROPIC_API_KEY` (e `GITHUB_TOKEN` na receita com Docker): não execute sem revisão.

Índice de exemplos oficiais (conteúdo dos notebooks não lido): https://github.com/anthropics/claude-cookbooks (pastas `tool_use`, `claude_agent_sdk`, `observability`, `cost_optimization`; MIT).
