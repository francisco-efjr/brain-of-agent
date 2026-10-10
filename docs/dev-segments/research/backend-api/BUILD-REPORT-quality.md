# BUILD-REPORT de qualidade — backend-api

Data: 2026-10-10. Escopo: qualidade de prompt e fidelidade técnica de todo o plugin `plugins/backend-api` (README, playbook e referências, skills de tarefa, agentes, biblioteca de prompts, evals). Rubrica: `docs/foundation/prompt-quality-rubric.md` (D1–D12, 0–100).

Independência: o validador é um modelo da família Claude (Opus 5.5), diferente do construtor, mas da mesma família. A revisão é adversarial, porém **não equivale a validação externa**. As notas são leitura crítica, não medição: nenhum eval foi executado.

## 1. Método

1. Leitura integral: 10 `SKILL.md`, 5 agentes, README, `evals/` inteiro (12 casos, 41 arquivos de grader/prompt, README), `integracao-api-llm.md`, trechos de `fontes.md`, template `aviso-de-deprecacao.md`.
2. Biblioteca de prompts: 13 prompts amostrados e lidos inteiros (PR-01, 02, 04, 08, 13, 14, 17, 20, 23, 29, 30, 31, 32); os 32 IDs conferidos no sumário.
3. Referências restantes: varredura por `Grep` (placeholders, CAPS/absolutos, `--dangerously-skip-permissions`, exemplos de JWT, timeouts Go, pool SQLAlchemy, Dredd/RFC/Confluent).
4. Fidelidade técnica conferida na fonte (WebFetch, 2026-10-10):
   - https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools: tabela de `tool_choice` (`any`/`tool` dão 400 em Opus 5.5, Sonnet 5.5, Fable 5.1 e Mythos 5.1 e falham com extended thinking manual), "explicação, não raciocínio" (`reasoning_extraction`), regex de `name`, custo de `input_examples`. **Verificado**.
   - https://www.rfc-editor.org/rfc/rfc9745.html: `Deprecation` (Standards Track, março/2025), valor `@<epoch>`, relação de link `deprecation`, `Sunset` não anterior ao `Deprecation`. **Verificado**.
   - https://www.rfc-editor.org/rfc/rfc8594.html: `Sunset` (Informational, maio/2019), valor HTTP-date. **Verificado**.
   - https://github.com/apiaryio/dredd: arquivado em 08/11/2024. **Verificado**.
   - https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html: compatibilidade padrão `BACKWARD`. **Verificado**.
   - Demais afirmações (Stripe v1/v2, AIP-155/158, RFC 9700, RFC 8725, drafts IETF, Go 1.22 `ServeMux`, Spring `aud`, FastAPI tutorial): conferidas contra `VALIDATED.md` (fonte de verdade); coerentes.
5. Correções aplicadas direto nos arquivos; verificador e validador oficial rodados no fim.

## 2. Notas antes e depois

| Arquivo | Antes | Depois | Correções |
| --- | --- | --- | --- |
| `skills/playbook/SKILL.md` | 91 | 91 | Nenhuma. Forte em D2, D3, D7, D8. Ressalva D9: a tabela de fronteiras (26 linhas) é carregada a cada disparo (ver pendências) |
| `skills/prompts/SKILL.md` | 87 | 89 | ID interno `TP-08` (não resolvível) trocado por `handoff-checkpoint.md` |
| `skills/api-contract-design/SKILL.md` | 91 | 91 | Nenhuma |
| `skills/api-security-review/SKILL.md` | 92 | 92 | Nenhuma |
| `skills/idempotency-and-resilience/SKILL.md` | 91 | 91 | Nenhuma |
| `skills/api-test-suite/SKILL.md` | 89 | 91 | `-n auto` declarado como dependente de pytest-xdist; RFC 9745/8594 e Dredd passam de Inferido para Verificado com data |
| `skills/backend-debugging/SKILL.md` | 90 | 90 | Nenhuma |
| `skills/agent-tool-design/SKILL.md` | 90 | 92 | Gotcha de `tool_choice` reconferido e completado (thinking manual também bloqueia; chamada forçada pula o thinking; alternativa structured outputs) |
| `skills/stack-conventions/SKILL.md` | 89 | 89 | Nenhuma |
| `skills/backend-claude-md-setup/SKILL.md` | 88 | 88 | Nenhuma (gate de confirmação do diff e `disable-model-invocation` corretos) |
| `agents/api-security-reviewer.md` | 92 | 92 | Nenhuma (somente leitura, exclusões de diff, formato fixo, caso sem achado) |
| `agents/api-contract-reviewer.md` | 90 | 92 | Formatos de `Deprecation`/`Sunset`/`Link` e modo `BACKWARD` do Confluent agora Verificados e explícitos |
| `agents/backend-architect.md` | 90 | 90 | Nenhuma |
| `agents/backend-debugger.md` | 90 | 90 | Nenhuma |
| `agents/api-test-engineer.md` | 88 | 91 | `--shuffle` (flag inexistente no pytest) trocado por flags reais por ferramenta (`pytest -n auto` com xdist, `go test -shuffle=on`, `vitest --sequence.shuffle`, `jest --randomize`), com aviso de conferir na versão; Dredd Verificado |
| Biblioteca de prompts (13 amostrados) | 88 | 89 | Rótulo de Dredd corrigido em PR-19; demais prompts com papel, contexto com porquê, critério de pronto com comando, linha de regras e fonte com classe |
| `evals/` (12 casos + README) | 86 | 88 | Grader de `idempotencia-pagamento` deixou de exigir 409/400 literais (agora aceita código declarado como decisão do projeto, coerente com a skill); README registra a versão local reconferida (2.1.128 em 2026-10-10) |
| `README.md` | 88 | 90 | Limitação "fatos não reverificados" atualizada: Dredd, RFC 9745/8594 e `BACKWARD` reverificados; gRPC 4 MB e SQS FIFO seguem Inferido |
| Referências e templates do playbook | — | — | `fontes.md`: seção de fatos reverificados com URLs; caminhos do brain-of-agent corrigidos para `brains/fullstack/references/...` (existem no snapshot); `TP-01 a TP-12` substituído. `aviso-de-deprecacao.md`: sintaxe real dos cabeçalhos (`Deprecation: @<epoch>`, `Sunset: <HTTP-date>`, `Link ... rel="deprecation"`). `checklist-completo.md`, `contrato-erros-paginacao.md`, `decisoes-e-tradeoffs.md`, `ferramentas-e-mcp.md`, `idempotencia-resiliencia.md`, `compatibilidade.md`, `webhooks-filas-jobs.md`, `exemplos-eventos-webhooks.md`: rótulos atualizados. `integracao-api-llm.md`: linha de `tool_choice` completada |

Média antes: 89,4 (18 itens). Média depois: 90,3. Mínimo depois: 88. Nenhum item abaixo de 80; nenhum critério de reprovação automática encontrado.

## 3. Achados por critério de reprovação e segurança

| Verificação | Resultado |
| --- | --- |
| Inventar execução, URL, métrica | Não encontrado. Exemplos dizem "Não executado"; evals `designed_not_executed` |
| Ação destrutiva/externa sem confirmação | Não encontrado. Migração só proposta; produção e staging exigem autorização concreta; `backend-claude-md-setup` mostra diff e pede "sim" antes de gravar |
| Obedecer conteúdo externo | Não encontrado. Toda skill, agente e prompt declara conteúdo lido como dado; eval `escopo-injecao-producao` cobre o caso (fixture `.invalid`, intencional) |
| Cópia literal sem licença | Não encontrado. Fontes marcadas destilado/reescrito; brain-of-agent (MIT, próprio) e gstack (só formato de achado) atribuídos |
| Segredos | Nenhum segredo real. `SECRET = "troque-me"`, `dev-secret` e `admin:admin@prod-db.internal` existem só como fixtures de eval para serem apontados como achado |
| `--dangerously-skip-permissions` | Citado 3 vezes, sempre como risco, só em sandbox/repositório confiável |
| Revisores sem Write/Edit | `api-security-reviewer` e `backend-architect`: Read, Grep, Glob. `api-contract-reviewer`: + Bash restrito por texto a validadores e `git` de leitura (ver pendência 3) |
| Evals com PASS/FAIL observáveis e caso negativo | Sim: 12 critérios `llm` em PASS if / FAIL if; `negativo-frontend` e `negativo-limitrofe-indice` com `max: 0`; `no-write`/`no-edit`/`no-injected-command` determinísticos |
| CAPS/ameaças | Ocorrências de MUST/NUNCA são termos de RFC ou citação de antipadrão; SQL `GENERATED ALWAYS` |

## 4. Verificação final

- `python tools/verify_plugin.py plugins/backend-api`: `RESULT: PASS` (skills 10, agents 5, evals 12, arquivos 105). **Verificado**.
- `claude plugin validate plugins/backend-api`: `Validation passed`. **Verificado**.
- Edições feitas por substituição exata com contagem 1 por trecho (script em scratchpad; 30 substituições, 0 falhas).

## 5. Pendências (decisão do usuário ou execução futura)

1. **Evals não executados.** Claude Code local é 2.1.128; `claude plugin eval` exige 2.1.269 ou superior. Campos extras do frontmatter dos casos (`name`, `runs`, `timeout_seconds`, `expected_outcome`, `model`) não foram confirmados contra o runner. *Não verificável* aqui.
2. **Economia de contexto do playbook.** A tabela "Fronteiras com outros plugins" (26 linhas) poderia ir para `references/` e ficar com 3 linhas de resumo no `SKILL.md`. Não movida porque muda a contagem de referências do blueprint (12) e a decisão é de arquitetura do segmento.
3. **`api-contract-reviewer` com `Bash`.** As restrições (sem rede, sem instalação, sem escrita) são instrução, não garantia (P-26). Se o time quiser garantia, use regras `deny` de permissão no projeto ou remova `Bash` do agente (perde a execução local de oasdiff/Spectral/buf).
4. **`allowed-tools` com `Edit, Write`** em `api-contract-design`, `idempotency-and-resilience`, `api-test-suite`, `backend-debugging` e `agent-tool-design` pré-aprovam escrita local enquanto a skill está ativa. É coerente com "implementar dentro do escopo" do estilo da casa, mas um time que prefira confirmar cada escrita deve remover `Edit, Write` dessas listas.
5. **`backend-claude-md-setup` sem eval.** Por ter `disable-model-invocation: true`, não há caso de disparo; um caso com invocação explícita depende de suporte do runner a comando no `prompt.md` (não verificado).
6. **Fatos ainda Inferido:** limite padrão de 4 MB por mensagem gRPC (varia por implementação), janela de 5 min de deduplicação do SQS FIFO, equivalências gRPC↔HTTP, sintaxe de Pact/Schemathesis/Prism nas versões atuais. Reconferir antes de citar como fato.
7. **Referências não lidas na íntegra** neste passe (lidas por amostragem e `Grep`): `stack-*.md`, `exemplos-*.md`, `openapi-checklist.md`, `politicas-idempotencia.md`, `webhooks-filas-jobs.md`. Nenhum problema encontrado nas amostras; leitura integral fica para uma próxima revisão.
