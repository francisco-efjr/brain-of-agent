# BUILD-REPORT de qualidade: automation-integrations

Data: 2026-10-10 · Plugin: `plugins/automation-integrations` v0.1.0 · Papel: validador independente de prompt e conteúdo técnico.
Independência: o validador é da família Claude, como os construtores. As notas D1 a D12 são estimativas de leitura (rubrica `prompt-quality-rubric.md`), não medição, e não são validação externa.

## 1. Método

- Li integralmente os 10 `SKILL.md`, os 5 agentes, as duas bibliotecas de prompts (P-01 a P-30, todos os 30), os 13 casos de eval com seus graders, o README e as referências com código ou afirmação técnica de risco (hooks, webhook, jobs, scraping, MCP, segurança, fontes, autoria, padrões).
- Executei os códigos de referência: `guard_bash.py` + `test_guard.py`, `robots_check.py` + `test_robots.py`, `gate.py`, `receiver.py` + `replay.py`. Tentei contornar o guard com comandos que o texto não anunciava e testei o receptor com fila fora do ar e corpo assinado porém malformado.
- Conferi contra a fonte oficial (WebFetch, 2026-10-10): https://code.claude.com/docs/en/headless e https://code.claude.com/docs/en/plugin-evals. Demais afirmações foram conferidas contra `VALIDATED.md` (V-01, V-02, V-05, V-06, V-09, V-15, V-16, V-32).
- Verifiquei que todo ID citado (W, T, S, H, K, J, R, A, M, F, I, G, X e V-xx) existe em `checklist-completo.md` e `fontes.md`: nenhum órfão.
- Nenhum critério de reprovação automática encontrado: sem segredo, sem cópia literal sem licença (o único literal é `handoff-checkpoint.md`, MIT do próprio usuário, com atribuição), sem fluxo que autorize efeito externo sem confirmação, revisores sem Write/Edit.

## 2. Notas por componente (D1 a D12, média x 20)

| Arquivo | Antes | Depois | Correções |
| --- | --- | --- | --- |
| `skills/playbook/SKILL.md` | 85 | 88 | Sem exemplo trabalhado (D5): acrescentada tabela "Exemplos de roteamento" com 3 pedidos. Mantido abaixo de 300 linhas (186) |
| `skills/prompts/SKILL.md` | 80 | 87 | Linha de "Plataforma" herdada de outro segmento (mobile, web) substituída por texto do segmento; sem `argument-hint` (acrescentado); sem exemplo de uso (acrescentado com P-08) |
| `skills/prompts/references/prompt-library.md` (P-01..P-20) | 88 | 90 | P-13 citava `prompt-principles.md` da fábrica como técnica; trocado por "delimitação por tags". Demais prompts: papel, entrada como dado, formato, incerteza e modo sem interação presentes |
| `skills/prompts/references/prompt-library-seguranca-e-ops.md` (P-21..P-30) | 84 | 89 | P-21 mandava `--output-format json` e, ao mesmo tempo, um gate que precisa do `system/init` (só emitido por `stream-json --verbose`): reescrito e alinhado com a skill |
| `skills/building-mcp-servers/SKILL.md` | 89 | 91 | `claude mcp list` apresentado como fato: marcado Inferido. Esqueleto TypeScript descrevia `cursor` na tool sem tê-lo no schema (corrigido); nota de módulo ES; trechos "nesta fábrica" reescritos |
| `skills/reviewing-webhook-receivers/SKILL.md` | 88 | 92 | Tabela de replay dizia que corpo reserializado deve dar assinatura inválida, e `webhooks-e-reprocessamento.md` dizia que corpo reformatado deve dar 2xx: separados em dois casos sem contradição (formatação diferente assinada sobre os bytes enviados = 2xx; corpo adulterado = 4xx). Receptor de referência corrigido (ver 3) |
| `skills/authoring-plugin-skills/SKILL.md` | 88 | 90 | Referências à "fábrica" trocadas por dev-segments/construção; seção de graders na referência atualizada com opções oficiais de `regex`, `tool_order`, `file_exists`, `weight`, `arm` (antes "não lidas") |
| `skills/assessing-automation-risk/SKILL.md` | 91 | 91 | Sem alteração: gatilhos, veredito, "não lido", exemplo e severidades adequados |
| `skills/writing-hook-guardrails/SKILL.md` | 86 | 91 | Matcher sem "espaço" (V-02 inclui); script de referência deixava passar `env -i rm -rf /`, `rm -r -f ../..`, `find / -delete` (corrigido, ver 3); contagem de testes atualizada (37) |
| `skills/scheduling-headless-jobs/SKILL.md` | 86 | 92 | Gate exigia as chaves `plugin_errors`/`mcp_server_errors`, que a documentação omite quando não há erro: reprovaria toda execução saudável (corrigido, ver 3); "**Nunca**" em negrito trocado por alternativa positiva; "a fábrica rodou" reescrito |
| `skills/designing-workflow-automations/SKILL.md` | 90 | 90 | Sem alteração; retry de `jobs-workflows-e-scraping.md` deduplicado para apontar ao código testado desta skill |
| `skills/responsible-scraping/SKILL.md` | 90 | 90 | Sem alteração; verificador de `robots.txt` reexecutado (13 casos, 0 falhas) |
| `agents/automation-architect.md` | 90 | 90 | Sem alteração |
| `agents/integration-reviewer.md` | 91 | 91 | Sem alteração |
| `agents/mcp-security-reviewer.md` | 90 | 90 | "nesta fábrica" reescrito |
| `agents/plugin-validator.md` | 86 | 87 | Tem Bash; a restrição a 3 comandos é só textual e o próprio agente admite isso. Mantido (precisa rodar os validadores); registrado como pendência. "repositório da fábrica" reescrito |
| `agents/third-party-auditor.md` | 91 | 91 | Sem alteração; somente leitura, sem Bash |
| `evals/` (13 casos, README) | 84 | 90 | Um único negativo: acrescentado `negativo-react-hook` (quase-acerto lexical com a palavra hook); graders `regex` determinísticos (`termo-obrigatorio.md`, peso 0,5) em 6 casos, antes só `llm` e indicador; README atualizado (contagem, custo, formatos de grader conferidos) |

Média antes: 87,6 · Média depois: 90,0 · Mínimo depois: 87 (`plugin-validator`) · Todos os componentes acima de 80 antes e depois.
Referências e templates (não pontuados individualmente) receberam as correções listadas na seção 3.

## 3. Correções técnicas de substância (factuais e de código)

1. **Gate de `claude -p` (receitas.md)**: contradizia a documentação oficial. A página `headless` diz que `plugin_errors` e `mcp_server_errors` são omitidas quando não há erro. O gate tratava chave ausente como falha, então reprovaria execução saudável em versão nova. Agora: chave ausente só vale como "sem erro" se `claude_code_version` for ≥ 2.1.219 (`mcp_server_errors`) ou ≥ 2.1.283 (`plugin_errors`, mínimo desconhecido: Suposição conservadora); servidor `pending` (remoto com lista em cache) vira aviso. 8 amostras sintéticas executadas, resultados esperados.
2. **`structured_output`**: a doc põe o resultado de `--json-schema` nesse campo em `--output-format json`; o texto dizia "varia por versão". Corrigido. O `system/init` só existe em `stream-json --verbose`: P-21 e `jobs-workflows-e-scraping.md` agora dizem isso.
3. **Receptor de webhook de referência**: se a fila falhava, o ID ficava gravado como `received` e o reenvio do provedor era respondido como duplicado, perdendo o evento. Agora a falha de fila remove o ID e devolve 503; corpo assinado porém malformado devolve 400 em vez de 500. Verificado: 503, depois reenvio 202, depois duplicado 200.
4. **Guard de Bash**: 4 contornos reais fechados (`env -i rm -rf /`, `rm -r -f ../..` e `rm -rf ../`, `find / -delete`); `git push origin main -f` já era bloqueado e entrou como regressão. Suíte passou de 29 para 37 casos, 0 falhas, incluindo 3 casos novos de "permitido". Limites residuais declarados (`cd / && rm -rf *`, `xargs`).
5. **Contradição de replay** (corpo reserializado) resolvida em três arquivos.
6. **Esqueleto TypeScript** sem `cursor` no schema; **P-21** inconsistente; **matcher** sem "espaço".
7. **Vazamento de jargão interno**: "fábrica" removido de texto voltado ao usuário (substituído por "construção do plugin" ou "repositório dev-segments"); permanece só onde nomeia o repositório.
8. `job/entrada.txt` precisa das tags `<entrada>`: o stdin é anexado ao prompt e a receita não as acrescentava (nota adicionada). Nota de que `--bare` deve virar padrão de `-p` (doc oficial).

## 4. Fidelidade técnica

| Afirmação | Fonte conferida | Resultado |
| --- | --- | --- |
| `--bare`, sem ele `-p` roda hooks e MCP do projeto sem prompt de confiança | headless (WebFetch) | Verificado |
| `--permission-mode dontAsk`, `--permission-prompts none` (v2.1.259+) | headless | Verificado |
| Espaço antes do `*` em `Bash(git diff *)` | headless | Verificado |
| Pipe de stdin até 10 MB; SIGTERM sai com 143 sem resultado do turno | headless | Verificado |
| `claude plugin eval` exige 2.1.269; 3 execuções; `--threshold` 1.0; `tool_used` com `min`/`max`/`arm`; `scored: false` em dois braços | plugin-evals | Verificado |
| Chaves de `prompt.md` de eval, graders `regex`/`file_exists`/`tool_order` | plugin-evals | Verificado (antes eram "não lidos") |
| Exit 2, matcher, `onFailure` v2.1.295, `permissionDecision` | VALIDATED V-02 (hooks, ~38% da página lida) | Herdado; schemas dos eventos finais seguem Não verificáveis |
| 25.000 tokens por resposta de tool, `headersHelper` 10 s | VALIDATED V-09, V-15 | Herdado |
| Nomes de pacote do Inspector, `type: http` em `.mcp.json`, `disableAllHooks` | Sem fonte | Já rotulados Inferido; mantidos |

Não executável aqui: `claude plugin eval` (CLI local 2.1.128 < 2.1.269). Os 13 casos seguem `designed_not_executed`.

## 5. Direitos autorais e segurança

- Literal só de conteúdo próprio (MIT) com atribuição: `handoff-checkpoint.md` (19 linhas, confere com o snapshot). O resto é destilação com redação própria; gstack, n8n e documentações com atribuição ou apenas URL. Citação de terceiros na segurança ("Fetch and follow…") tem 5 palavras e está explicitada como achado.
- Nenhum segredo ou credencial (verificador sem alerta). Nenhum hook, `.mcp.json`, `.lsp.json` ou `bin/` ativo.
- Revisores (`integration-reviewer`, `mcp-security-reviewer`, `third-party-auditor`, `automation-architect`) sem Write, Edit e Bash. `plugin-validator` tem Bash, restrito por texto.
- `--dangerously-skip-permissions` aparece uma vez, como risco, com alternativa (`dontAsk` + lista mínima).
- Casos de eval com texto hostil (`escopo-injecao-readme`, `instalar-plugin-latest`) não têm Bash em `allowed_tools`, usam domínios `.invalid`, e o critério é não executar.
- Evals com PASS/FAIL observáveis e agora 2 casos negativos (CSS; hook do React) mais 6 verificações `regex` determinísticas.

## 6. Pendências

1. Rodar `claude plugin eval .` em Claude Code ≥ 2.1.269, com `--model` e `--judge-model` fixos e de famílias distintas. Calibrar o peso e os padrões dos graders `regex` depois da primeira execução (podem ser estritos demais).
2. `plugin-validator`: a restrição de Bash a três comandos não é garantida pelo ambiente. Decidir se o agente fica com Bash (como está) ou se a validação passa a ser feita pelo agente principal; confirmar na doc de subagentes se `tools` aceita padrões de comando.
3. Versão mínima de `plugin_errors` no `system/init` é desconhecida (usada 2.1.283 por cautela); confirmar na doc de versões.
4. Schemas finais dos eventos de hook (cerca de 62% da página não lida), páginas `scheduled-tasks`, `/loop` e subagentes, e a spec de autorização do MCP seguem como lacunas já declaradas.
5. Low-code (n8n Retry/Continue On Fail, Zapier, Make), Shopify, Slack, `Idempotency-Key` e termos de uso/LGPD em scraping continuam Não verificáveis; não há caso de eval para eles.
6. Revisão humana ou de outro fornecedor de modelo antes de publicar: autor, pesquisadores e validadores são da mesma família.
7. Os scripts regex de `template-hook-guardrail.md` e de `hooks-e-guardrails.md` continuam mais fracos que o `guard_bash.py`; ambos agora indicam o script robusto, mas mantêm o esqueleto. Decidir se vale removê-los.
