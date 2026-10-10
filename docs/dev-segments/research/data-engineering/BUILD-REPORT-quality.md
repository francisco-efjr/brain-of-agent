# BUILD-REPORT qualidade — plugin data-engineering

Data: 2026-10-10 · Papel: validador independente de qualidade de prompt e conteúdo técnico · Plugin: `C:\Users\Francisco Edson\dev-segments\plugins\data-engineering`
Rótulos: Verificado = saída de ferramenta ou página lida nesta execução. Inferido = dedução de leitura. Suposição = premissa não checada. Não verificável = sem como checar aqui.

Declaração de independência: o validador é de outra execução que os construtores, mas da mesma família de modelos (Claude). A pontuação D1 a D12 é autoatribuída por leitura e não substitui medição: os evals continuam `designed_not_executed` (CLI local 2.1.128, abaixo do mínimo 2.1.269 do `claude plugin eval`).

## 1. Método

- Leitura integral: README, os 10 `SKILL.md`, os 5 agentes, as 29 entradas da biblioteca de prompts (P-01 a P-29, bem acima do mínimo de 10), as 12 referências do playbook, as 7 referências de skills, os 12 templates e os 13 casos de eval originais com todos os graders.
- Nota por artefato: média de D1 a D12 (0 a 5) vezes 20. Critérios de reprovação automática da rubrica checados em todos: nenhum ocorreu (sem segredo real, sem ação destrutiva autorizada, conteúdo externo tratado como dado, atribuições presentes, frontmatter válido, citações literais do brain-of-agent conferidas contra o snapshot).
- Conferência de fatos em fonte oficial (WebFetch, 2026-10-10): garantias de entrega do Flink (master), defaults do Spark 4.2.0, Airflow 3.3.2 (best practices), valores aceitos por `model` de subagente, campos ignorados em subagente de plugin, formato e mecânica do `claude plugin eval`, CVE-2025-55284 (corrigido na v1.0.4 segundo o post), `dbt-labs/dbt-agent-skills` (Apache-2.0, 731 estrelas, 14 skills), `--plugin-dir` (`claude --help` local).

## 2. Tabela arquivo, antes, depois, correções

| Arquivo | Antes | Depois | Correções |
| --- | --- | --- | --- |
| `README.md` | 85 | 88 | Alternativa `--plugin-dir` para instalar sem marketplace (flag verificada em `claude --help`); contagem de evals 16; limitação nova: casos de segurança só medem com `--allow-tools` em Linux ou WSL2 |
| `skills/playbook/SKILL.md` | 90 | 91 | Gotcha sobre a mecânica de `claude plugin eval` (`allowed_tools` só concede leitura). D9 (23 KB, tabela de 25 plugins) segue como ponto fraco aceito |
| `skills/prompts/SKILL.md` | 88 | 90 | `allowed-tools` em formato igual ao das demais skills (separado por espaço) |
| `skills/prompts/references/prompt-library.md` (29 prompts lidos) | 86 | 90 | P-03 realinhado aos 8 itens da skill de aceitação (antes divergia em 3 pontos) e com critérios do veredito; P-13 sem "PARAR" em caixa alta; P-24 com a redação clara dos tetos de tentativas |
| `skills/dbt-model-workflow/SKILL.md` | 87 | 88 | Sem mudança no corpo; ajuste no exemplo de apoio (ver referências) |
| `skills/pipeline-acceptance/SKILL.md` | 82 | 90 | Tabela de veredito tinha lacunas (itens 1 a 5 parcialmente verificados não caíam em nenhuma linha; precedência de REPROVADO sobre NÃO VERIFICÁVEL indefinida) e contradição com o caso de borda (sem contagem oficial da fonte): reescrita com precedência e regra do risco aceito por escrito; "em voz alta" trocado por instrução executável |
| `skills/airflow-dag-workflow/SKILL.md` | 87 | 89 | Limiar de confiança alinhado ao revisor (7 ou mais achado, 4 a 6 pergunta, abaixo de 4 descarte); antes era 6 |
| `skills/spark-streaming-review/SKILL.md` | 86 | 88 | Mesmo alinhamento de limiar de confiança |
| `skills/sql-review/SKILL.md` | 88 | 88 | Sem mudança necessária |
| `skills/text-to-sql-safe/SKILL.md` | 88 | 89 | Gotcha do nome de modelo do cookbook reescrito como Não verificado, com instrução acionável |
| `skills/data-contracts-quality/SKILL.md` | 88 | 88 | Sem mudança necessária |
| `skills/gated-pipeline-migration/SKILL.md` | 84 | 89 | Tetos de tentativa ("5 tentativas no projeto todo e, num loop adicional, 3") eram ambíguos: reescritos de forma operacional e replicados em `dbt.md`, no template de migração e em P-24 |
| `agents/data-pipeline-reviewer.md` | 90 | 90 | Sem mudança necessária (fonte do limiar de confiança) |
| `agents/analytics-reviewer.md` | 90 | 90 | Sem mudança necessária |
| `agents/pipeline-debugger.md` | 92 | 92 | Sem mudança necessária |
| `agents/data-pipeline-architect.md` | 88 | 88 | Sem mudança necessária |
| `agents/eval-judge.md` | 86 | 89 | Afirmação imprecisa sobre `model` ("só aceita aliases") corrigida: a documentação aceita alias ou ID completo, sempre modelos Claude |
| `skills/playbook/references/` (12 arquivos) | 88 | 90 | `checklist-completo.md` seção B renumerada para os mesmos 8 itens da skill e do template (eram 3 numerações diferentes); `seguranca-contexto-e-evals.md` com item 10 (mecânica real do eval) e correção do `model`; `dbt.md` com teto de tentativas claro |
| Referências das skills de tarefa (7 arquivos) | 87 | 89 | `exemplos-dbt.md`: premissa explícita no join do fato (`customer_id` e `created_at` podem não existir em order_items) |
| `skills/playbook/assets/templates/` (12 arquivos) | 86 | 89 | `relatorio-de-aceitacao-de-pipeline.md` realinhado ao canônico (8 itens); `plano-de-migracao-gated.md` com tetos claros; `cenario-de-eval.md` com aviso do formato oficial e de `--allow-tools` |
| `evals/` (13 casos originais, agora 16) | 68 | 86 | Ver seção 3 |

Média antes 86,4; depois 89,1; menor nota depois 86. Todos acima de 80, nenhum critério de reprovação automática.

## 3. Evals: defeitos encontrados e corrigidos (Verificado contra https://code.claude.com/docs/en/plugin-evals)

1. **Graders de restrição não mediam nada.** O README dizia que `Bash`, `Write` e `Edit` em `allowed_tools` liberavam as ferramentas "de propósito". A documentação diz o contrário: `allowed_tools` só concede leitura; as demais ficam removidas da sessão sem `--allow-tools`. Os graders `no-exec`, `no-write` e `no-edit` passariam sempre. Corrigido no `evals/README.md` (comando com `--allow-tools`, exigência de sandbox, Windows nativo sem backend: usar WSL2 ou Linux), no README do plugin, no playbook e na referência de segurança.
2. **`no-references-read` reprovaria o comportamento correto.** `tool_used` tem `min` padrão 1; o grader só tinha `max: 3`, então zero leituras de referência reprovava. Adicionado `min: 0`.
3. **Grader negativo não era pontuado.** Em execução de dois braços, todo `tool_used` sobre `Skill` fica fora da nota. `no-plugin-skill` recebeu `arm: both`. O README deixou de chamar esses graders de determinísticos sem ressalva.
4. **Sem cobertura de agentes nem de backfill.** Três casos novos: `backfill-janela-sem-execucao` (plano, `INSERT` cego, custo por `dry_run`, sem execução), `revisor-diff-sem-oraculo` (veredito diferente de APROVADO, `unique` ausente, `post_hook`, `accepted_values` chutado; grader `Agent` com `arm: with-only`) e `juiz-criterio-composto` (erro de critério composto e recusa de nota). Passam no verificador do repositório.
5. Senha fictícia do caso da DAG trocada por `senha_ficticia` (evita aparência de credencial real).
6. Comando de ablação do README conferido: `--ablation none|with-without`.

## 4. Fidelidade técnica

Verificado e sem correção necessária: tabela de garantias do Flink (fontes e sinks, incluindo OpenSearch, DynamoDB, Kinesis, Redis, sockets e Cassandra), defaults do Spark 4.2.0 (nove propriedades), Airflow 3.3.2 (`Variable.get` no topo gera chamada a cada parse sem cache; XCom pequeno; exemplos com `airflow.sdk`), recursos de dbt por versão citados (versões de modelo 1.5, `data_tests` e testes unitários 1.8, microbatch e snapshots em YAML 1.9: Inferido por conhecimento estável, rotulado como tal nos arquivos), CVE-2025-55284 e versão da correção, repositório `dbt-labs/dbt-agent-skills`.
Corrigido: `model` de subagente (alias ou ID completo, não só alias); mecânica do `claude plugin eval` (item 3 acima).
Observação (Inferido, sem correção): o catálogo ODCS 3.2.0 do esqueleto de contrato continua marcado "não validado"; a nota do Airflow sobre `catchup` ("o default mudou entre versões") não foi reconferida, pois a página de best practices não declara o default.

## 5. Direitos autorais e segurança

- Citações literais: duas, do brain-of-agent (MIT, do próprio autor), conferidas contra o snapshot (`dados-ambientes-ci.md` linha 210 e o contexto portátil), com atribuição. Demais fontes destiladas. Nenhuma cópia de licença restritiva.
- Segurança: nenhum fluxo autoriza produção, `--full-refresh`, `TRUNCATE`, `DROP`, backfill ou instalação sem confirmação; agentes só com `Read, Glob, Grep` (`eval-judge` só `Read`); conteúdo externo tratado como dado em todos os componentes; sem hooks, `.mcp.json`, `.lsp.json` ou `bin/`. `--dangerously-skip-permissions` aparece apenas como risco (sandbox descartável, nunca padrão).
- Sem CAPS de ameaça: as poucas maiúsculas restantes são vereditos (`REPROVADO`) e três "NÃO" de invariante de segurança em P-18, P-19 e P-27, aceitos pela rubrica.

## 6. Pendências

1. Executar os 16 evals com Claude Code 2.1.269 ou superior, em Linux ou WSL2, com `--allow-tools Write Edit Bash` para os três casos de segurança (Não verificável aqui).
2. Confirmar na primeira rodada o formato do campo do agente no JSON da chamada `Agent` (os regex `data-pipeline-reviewer` e `eval-judge` são Suposição).
3. Validar o esqueleto ODCS contra o JSON Schema 3.2.0 e reconferir `catchup` por versão do Airflow.
4. Decisão de design aberta (herdada do relatório estrutural): `model: inherit` nos cinco agentes versus `sonnet` previsto no SYNTHESIS para `analytics-reviewer` e `data-pipeline-architect`. Sem impacto de qualidade verificável.
5. D9 do `playbook`: a tabela de fronteiras com 25 plugins (cerca de 30 linhas) poderia ir para `references/`; mantida porque o desempate entre plugins é usado no roteamento. Limite de 300 linhas respeitado (166).
6. Cobertura de eval ainda ausente: `pipeline-debugger`, `data-pipeline-architect`, Dagster, dbt incremental e snapshots, Delta, origens mobile e web.

## 7. Verificações finais

- `python tools/verify_plugin.py plugins/data-engineering`: `RESULT: PASS` (10 skills, 5 agents, 16 evals, 102 arquivos). Verificado.
- `claude plugin validate plugins/data-engineering`: `Validation passed`. Verificado.
