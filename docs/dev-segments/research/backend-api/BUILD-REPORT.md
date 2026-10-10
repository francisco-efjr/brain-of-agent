# BUILD-REPORT — backend-api

Data: 2026-10-10.
Plugin: `C:\Users\Francisco Edson\dev-segments\plugins\backend-api`.
Fontes consolidadas: `BUILD-REPORT-structural.md` (validação estrutural) e `BUILD-REPORT-quality.md` (revisão de qualidade de prompt e fidelidade técnica).
Gate final executado nesta sessão pelo verificador e pelo validador oficial.

## 1. Resultado do gate

| Verificação | Resultado | Rótulo |
| --- | --- | --- |
| `python tools/verify_plugin.py plugins/backend-api` | `RESULT: PASS` (skills 10, agents 5, evals 12, arquivos 105); sem ERROS | Verificado |
| `claude plugin validate plugins/backend-api` | `Validation passed` (manifesto `.claude-plugin/plugin.json`) | Verificado |

Pass: **sim**. Nenhum erro remanescente; não houve necessidade de correção nesta rodada de gate.

## 2. Contagem de componentes

| Componente | Quantidade | Observação |
| --- | --- | --- |
| Skills (`skills/*/SKILL.md`) | 10 | playbook, prompts, api-contract-design, api-security-review, idempotency-and-resilience, api-test-suite, backend-debugging, agent-tool-design, stack-conventions, backend-claude-md-setup |
| Agentes (`agents/*.md`) | 5 | api-security-reviewer, api-contract-reviewer, backend-architect, backend-debugger, api-test-engineer |
| Prompts na biblioteca (blocos PR-01 a PR-32) | 32 | IDs distintos encontrados em `skills/`; conferidos no sumário de `skills/prompts/references/` |
| Casos de eval (`evals/`) | 12 | cada um com `prompt.md` e `graders/`; README em `evals/README.md` |
| Arquivos de referência (pastas `references/`) | 35 | playbook 12, stack-conventions 6, prompts 2, demais skills o restante |
| Templates (`skills/playbook/assets/templates/`) | 12 | |
| Arquivos totais contados pelo verificador | 105 | |

Rótulo: **Verificado** para skills, agentes, evals, referências, templates e arquivos (contagem direta). **Verificado** para os 32 IDs PR-xx.

## 3. Correções aplicadas (consolidado das duas rodadas)

### 3.1 Estruturais

| Arquivo | Problema | Correção |
| --- | --- | --- |
| `README.md` (linha 11) | Caminho `references/ferramentas-e-mcp.md` não resolvia a partir da raiz | `skills/playbook/references/ferramentas-e-mcp.md` |
| `README.md` (tabela de componentes e limitações) | Diziam 10 evals; a pasta tem 12 | "12 casos" nos dois pontos |
| `skills/playbook/assets/templates/ficha-de-endpoint.md` | Referência `references/fontes.md` relativa errada | `skills/playbook/references/fontes.md` |

### 3.2 Qualidade (rodada de revisão)

| Arquivo | Correção resumida |
| --- | --- |
| `skills/prompts/SKILL.md` | ID interno `TP-08` (não resolvível) trocado por `handoff-checkpoint.md` |
| `skills/api-test-suite/SKILL.md` | `-n auto` declarado como dependente de pytest-xdist; RFC 9745/8594 e Dredd de Inferido para Verificado com data |
| `skills/agent-tool-design/SKILL.md` | Gotcha de `tool_choice` reconferido e completado (thinking manual também bloqueia; alternativa com structured outputs) |
| `agents/api-contract-reviewer.md` | Formatos de `Deprecation`, `Sunset`, `Link` e modo `BACKWARD` do Confluent explícitos e Verificados |
| `agents/api-test-engineer.md` | Flag `--shuffle` inexistente no pytest trocada por flags reais por ferramenta, com aviso de conferir na versão; Dredd Verificado |
| Biblioteca de prompts | Rótulo de Dredd corrigido em PR-19 |
| `evals/` (grader de `idempotencia-pagamento`) | Passou a aceitar código de erro declarado como decisão do projeto, coerente com a skill; README registra versão local reconferida |
| `README.md` | Limitação "fatos não reverificados" atualizada (Dredd, RFC 9745/8594 e `BACKWARD` reverificados) |
| `skills/playbook/references/fontes.md` e `integracao-api-llm.md` | Seção de fatos reverificados com URLs; caminhos do brain-of-agent corrigidos; linha de `tool_choice` completada |
| `templates/aviso-de-deprecacao.md` | Sintaxe real dos cabeçalhos: `Deprecation: @<epoch>`, `Sunset: <HTTP-date>`, `Link ... rel="deprecation"` |

Total aproximado: 30 substituições exatas (contagem 1 por trecho), 0 falhas, segundo a rodada de qualidade. Nenhum conteúdo grande foi reescrito. Não foram criados hooks, `.mcp.json`, `.lsp.json` nem `bin/`.

## 4. Notas de qualidade

- Notas de revisão (rubrica D1–D12, 0–100): média antes 89,4; média depois **90,3**; mínimo depois 88; nenhum item abaixo de 80 (18 itens avaliados). Rótulo: **Não verificável** como medição, pois é leitura crítica de um validador da mesma família do construtor, não validação externa.
- Verificações de segurança e de fabricação (agregado das duas rodadas): nenhum número, execução ou URL inventado encontrado; nenhuma ação destrutiva sem confirmação; nenhuma obediência a conteúdo externo; nenhuma cópia literal sem licença; nenhum segredo real (valores como `troque-me`, `dev-secret` e `admin:admin@prod-db.internal` são fixtures de eval para serem apontados como achado).
- `--dangerously-skip-permissions` aparece 3 vezes, sempre como risco e somente para sandbox ou repositório confiável.
- Revisores somente leitura: `api-security-reviewer` e `backend-architect` têm apenas Read, Grep e Glob. `api-contract-reviewer` tem Bash restrito por instrução textual (ver pendência 3).
- Fidelidade técnica conferida na fonte (WebFetch, 2026-10-10): documentação de tool use da Claude API (`tool_choice`, `reasoning_extraction`, regex de `name`), RFC 9745 (Deprecation), RFC 8594 (Sunset), arquivamento do Dredd em 08/11/2024 e compatibilidade padrão `BACKWARD` do Confluent. Rótulo: **Verificado**. Demais afirmações foram conferidas contra `VALIDATED.md` e marcadas como coerentes.
- Ressalva de consistência: o estado `designed_not_executed` aparece uma vez, em `evals/README.md`, e não em cada caso individual. A informação vale para o conjunto, mas não está replicada por caso. Rótulo: **Verificado** (busca por texto).

## 5. Saídas resumidas das validações

```
verify_plugin.py: Plugin: backend-api {'skills': 10, 'agents': 5, 'commands': 0, 'evals': 12, 'files': 105}
                  RESULT: PASS  (exit 0)

claude plugin validate: Validating plugin manifest: ...\plugins\backend-api\.claude-plugin\plugin.json
                        ✔ Validation passed  (exit 0)
```

## 6. Pendências

Pendências herdadas das duas rodadas. Nenhuma bloqueia o gate estrutural.

1. **Evals não executados.** O Claude Code local é 2.1.128; `claude plugin eval` exige 2.1.269 ou superior. Campos extras do frontmatter dos casos (`name`, `runs`, `timeout_seconds`, `expected_outcome`, `model`) não foram confirmados contra o runner. Rótulo: **Não verificável** nesta sessão.
2. **Economia de contexto do playbook.** A tabela "Fronteiras com outros plugins" (26 linhas) poderia ir para `references/`, com resumo de 3 linhas no `SKILL.md`. Não foi movida porque altera a contagem de referências do blueprint (12). Decisão de arquitetura do segmento.
3. **`api-contract-reviewer` com Bash.** As restrições (sem rede, sem instalação, sem escrita) são instrução, não garantia. Para garantia, usar regras `deny` de permissão no projeto ou remover Bash, o que perde a execução local de oasdiff, Spectral e buf.
4. **`allowed-tools` com `Edit, Write`** em `api-contract-design`, `idempotency-and-resilience`, `api-test-suite`, `backend-debugging` e `agent-tool-design`. Pré-aprovam escrita local enquanto a skill está ativa. Times que preferirem confirmar cada escrita devem remover `Edit, Write` dessas listas.
5. **`backend-claude-md-setup` sem eval.** Com `disable-model-invocation: true`, não há caso de disparo. Um caso com invocação explícita depende de suporte do runner a comando no `prompt.md` (não verificado).
6. **Fatos ainda Inferido:** limite padrão de 4 MB por mensagem gRPC (varia por implementação), janela de 5 min de deduplicação do SQS FIFO, equivalências gRPC↔HTTP, sintaxe de Pact, Schemathesis e Prism nas versões atuais. Reconferir antes de citar como fato.
7. **Referências não lidas na íntegra** na rodada de qualidade (lidas por amostragem e Grep): `stack-*.md`, `exemplos-*.md`, `openapi-checklist.md`, `politicas-idempotencia.md`, `webhooks-filas-jobs.md`. Leitura integral fica para próxima revisão.
8. **Citações de `fontes.md` ao repositório brain-of-agent** (ex.: `references/protocolo-completo.md`) são caminhos externos usados como citação, não links internos. Confirmar com o validador de qualidade.
9. **Hook de proteção de arquivos** (documentado em `ferramentas-e-mcp.md`) não foi executado e segue desativado por política.

## 7. Limites desta consolidação

- **Verificado:** estrutura, links `${CLAUDE_PLUGIN_ROOT}/...` (varredura sem quebras após correções), contagens e saídas dos dois validadores.
- **Não verificável:** qualidade de conteúdo como medição externa, e execução dos evals.
- **Não aplicável:** execução de hooks ou do plugin em runtime (plugin mantido sem hooks ativos).
