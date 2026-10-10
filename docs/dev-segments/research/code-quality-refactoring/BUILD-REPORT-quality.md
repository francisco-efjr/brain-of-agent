# BUILD-REPORT-quality: code-quality-refactoring

Data: 2026-10-10 · Validador: Claude Opus 5.5, em contexto de validação de prompt, com a rubrica `docs/foundation/prompt-quality-rubric.md` (D1–D12, 0–100).
Independência: os construtores eram outro modelo, mas da mesma família (Anthropic). A revisão é só parcialmente independente. As notas são julgamento por leitura, não medição (AP-16). Nenhum eval foi executado.

## Escopo lido

- Os 10 `SKILL.md`, os 5 agentes, `README.md` e `plugin.json`.
- A biblioteca de prompts inteira (34 prompts). A amostra pontuada em detalhe teve 15 prompts: PL-01, 02, 04, 05, 06, 07, 09, 12, 14, 15, 17, 27, 29, 33 e 34.
- Os 12 casos de eval (prompt e graders), `evals/README.md` e `.gitignore`.
- Referências conferidas por Grep e leitura parcial: `pontuacao-e-exemplo.md`, `transformacoes.md` (seção 6.1), `ferramentas-e-mcp.md` (CI, hooks, riscos) e `claude-md-snippets.md` (permissões).
- Fontes de apoio: `SYNTHESIS.md` (4.4, 4.5, 4.8), `VALIDATED.md` (V-10 a V-13, V-39, V-40, lacunas) e `BUILD-REPORT-structural.md` (pendências 1 a 6).

## Fidelidade técnica conferida (2026-10-10)

| Afirmação | Fonte aberta ou execução | Resultado |
| --- | --- | --- |
| `allowed-tools` pré-aprova e `disallowed-tools` remove ferramentas | https://code.claude.com/docs/en/skills | **Confirmado.** `allowed-tools` vale só no turno que invoca a skill e não restringe nada. `disallowed-tools` tira as ferramentas até a próxima mensagem. As skills já usavam isso certo. O README dizia que a sintaxe "não foi verificada" e foi corrigido. |
| Regra `Bash(git diff *)` e casamento por subcomando | https://code.claude.com/docs/en/permissions | **Confirmado.** O espaço antes de `*` é a forma documentada, e `:*` é equivalente. Compostos com `&&` e `\|` são checados por subcomando. Achado novo: `Bash(git diff *)` também casa `git diff --output=<arquivo>`, que grava arquivo. Virou gotcha em `review-diff`. |
| Dependabot espera 3 dias por padrão, exceto em atualizações de segurança (V-40, PL-29, `migration-parity`) | https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/about-dependabot-version-updates | **Confirmado:** a página fala em "cooldown period of 3 days" e diz que o padrão não vale para atualizações de segurança. |
| `sum()` diverge do laço `+=` com floats (Python 3.12 ou superior) | Executado em Python 3.14.4 | **Confirmado:** `0.9999999999999999` contra `1.0`. |
| Limiar de mais de 5 arquivos do `/investigate` | `brain-of-agent-snapshot/vendor/gstack/investigate/SKILL.md:619` | **Confirmado.** |
| Régua e pesos do painel (22/18/28/13/9) | `vendor/gstack/health/SKILL.md:498-524` | **Confirmado** (GBrain retirado). |
| Números de linha citados nos graders (Android 31 e 33; injeção 11; null-deref 13) | Contagem a partir dos cabeçalhos `@@` dos fixtures | **Confirmado.** |
| Modelos atuais "Sonnet 5.5, Fable 5.1, Haiku 5.5" | VALIDATED V-11 (página lida pelo validador da pesquisa) | Não reaberto; consistente com a fonte. |

## Notas por artefato

| Arquivo | Antes | Depois | Correções |
| --- | --- | --- | --- |
| `skills/playbook/SKILL.md` | 88 | 88 | Sem mudança. Tem papel, princípios com o porquê, processo, proporcionalidade, mapa, rótulos, segurança, modo COMPLETO e fronteiras. |
| `skills/review-diff/SKILL.md` | 87 | 90 | D11: faltava o caminho para quando a ferramenta `Agent` não existe (caso dos evals que só permitem Read/Glob/Grep/Skill). Agora revisão e refutação acontecem no próprio contexto, com aviso de independência reduzida. D8/D12: gotcha sobre o alcance de `allowed-tools`/`disallowed-tools` e sobre `git diff --output`. |
| `skills/debug-causa-raiz/SKILL.md` | 89 | 89 | Sem mudança. Contadores distintos, teste antes da correção e limiar de 5 arquivos verificado. |
| `skills/refactor-seguro/SKILL.md` | 88 | 88 | Sem mudança. |
| `skills/simplify-safe/SKILL.md` | 82 | 87 | D5: o exemplo se contradizia ("laço virou sum()" e depois "mantive o laço") e misturava "Inferido" com "confirmado". Agora o laço é mantido pela razão verificada, e o exemplo está marcado como ilustrativo. |
| `skills/migration-parity/SKILL.md` | 88 | 88 | Sem mudança. Dependabot reconferido. |
| `skills/tech-debt-triage/SKILL.md` | 88 | 88 | Sem mudança. A semântica de `disallowed-tools` ("pede na mensagem seguinte") bate com a doc. |
| `skills/code-health-report/SKILL.md` | 87 | 87 | Sem mudança. Régua e pesos conferidos no snapshot. |
| `skills/codebase-onboarding/SKILL.md` | 88 | 88 | Sem mudança. |
| `skills/prompts/SKILL.md` | 85 | 88 | Tabela arquivo → prompts depois da divisão da biblioteca. D11: se o ID não for achado, diz isso e não reescreve prompt de memória. |
| Biblioteca de prompts (amostra de 15) | 84 | 87 | D3/D12: PL-15 juntava "3 hipóteses ou correções falhas" e contradizia o resto do plugin (2 correções falhas, 3 hipóteses refutadas). Agora tem dois contadores. D9: a biblioteca de 656 linhas foi dividida conforme o `SYNTHESIS.md` 4.5 (`prompt-library.md` como índice mestre com PL-01 a 04 e 32 a 34, mais `prompts-revisao.md`, `prompts-debug.md`, `prompts-refatoracao.md` e `prompts-legado-e-divida.md`). O texto não mudou, e cada arquivo aponta para as convenções e as atribuições. |
| `agents/code-reviewer.md` | 89 | 89 | Sem mudança. `tools: Read, Grep, Glob`, formato fixo, modo sem interação, injeção tratada como achado. |
| `agents/finding-validator.md` | 88 | 88 | Sem mudança. |
| `agents/debugger.md` | 86 | 86 | Sem mudança. `Bash` amplo é risco declarado e mitigado por contrato. Sem Write/Edit. |
| `agents/refactor-planner.md` | 88 | 88 | Sem mudança. |
| `agents/codebase-mapper.md` | 88 | 88 | Sem mudança. |
| Evals (12 casos + README) | 82 | 87 | D7: em `health-report-no-tools`, o critério 1 exigia "nota de tipos abaixo da de lint". Pela régua da própria skill, 3 erros dão 7 e 7 avisos dão 4, então uma execução fiel à skill **reprovaria**. O critério agora pede a régua declarada e aplicada de forma coerente. O critério 3 dizia "2 de 4 categorias", e a skill usa 5: corrigido. README ganhou a seção "Por que 12 casos", com decisão e ordem de corte. |
| `README.md` | 84 | 87 | D12: semântica verificada de `allowed-tools`/`disallowed-tools`. A frase "comandos não foram executados" contradizia os moldes Verificado das referências e foi trocada pelo que de fato foi executado. `model: inherit` agora aparece como divergência do plano. |

Média antes: 86,6 · média depois: 87,8 (18 linhas da tabela) · mínimo depois: 86 (`debugger`). Nenhum critério de reprovação automática foi encontrado: não há execução inventada, ação externa sem confirmação, obediência a conteúdo externo, cópia sem licença, frontmatter inválido nem segredos.

## Direitos autorais e segurança

- Literais de terceiros: só os rótulos de Conventional Comments (CC BY 3.0, atribuídos em PL-11, `code-reviewer` e `revisao-de-codigo.md`). obra/superpowers (MIT) e gstack (MIT) aparecem como ideia reescrita, com atribuição. Repositórios proprietários (`anthropics/claude-code/plugins/*`) foram só destilados.
- Revisores (`code-reviewer`, `finding-validator`, `refactor-planner`, `codebase-mapper`) estão sem Write/Edit/Bash. O `debugger` tem Bash, sem Write/Edit.
- Skills de revisão e de triagem usam `disallowed-tools: Write, Edit, NotebookEdit`. As skills com efeito amplo (`migration-parity`, `code-health-report`) usam `disable-model-invocation: true`.
- Push, comentário em PR, commit e instalação exigem pedido explícito. `--dangerously-skip-permissions` aparece só como risco, restrito a sandbox. Hooks, CI e MCP ficam só documentados e desativados.
- Evals: os PASS/FAIL são observáveis. Há caso negativo (`negative-near-miss-qa`, `min: 0`, `max: 0`) e um caso de injeção com graders determinísticos `no-injected-command` e `no-write`. O fixture de injeção usa o domínio reservado `.invalid`.

## Pendências estruturais herdadas: como ficaram

1. **12 casos de eval contra 6 a 10.** Decidido manter, com justificativa e ordem de corte registradas em `evals/README.md`. Reversível pelo usuário.
2. **Subtemas da biblioteca de prompts.** Criados os quatro arquivos previstos no `SYNTHESIS.md` 4.5 (resolvido).
3. **`model: inherit` contra `sonnet`/`haiku` do plano.** Mantido `inherit`, porque trocar é decisão de custo sem medição. A divergência está declarada no README. Pendente de medição.
4. **Cobertura de evals** (sem caso para `simplify-safe`, `QUALIDADE-COMPLETO` e os quatro agentes). Continua pendente e declarada.
5. **Evals não executados.** Pendente: exigem Claude Code 2.1.269 ou superior, e a fundação registra 2.1.128.
6. **Crédito a `testes-e-debugging.md`.** Não exige ação.

## Pendências

- Rodar `claude plugin eval .` com `--ablation` (3 execuções por caso) numa CLI 2.1.269 ou superior e ler os transcripts. O caso `review-android-lifecycle-batch` tem o grader `reviewer-agent-used`, cujo nome de ferramenta e formato de input ainda não foram verificados.
- Medir `model: inherit` contra `sonnet`/`haiku` nos agentes antes de mudar.
- Acrescentar casos para `simplify-safe` (disparo), `QUALIDADE-COMPLETO` e delegação ao `debugger` e ao `refactor-planner` quando houver orçamento, cortando um caso para não passar de 12.
- Lacunas de fonte da pesquisa continuam abertas: guias oficiais de upgrade por framework, licença do OpenRewrite, ESLint/Sonar/mypy.

## Verificação final

- `python tools/verify_plugin.py plugins/code-quality-refactoring`: RESULT: PASS (10 skills, 5 agentes, 12 evals, 91 arquivos).
- `claude.exe plugin validate plugins/code-quality-refactoring`: Validation passed.
- Checagem de links relativos e de `${CLAUDE_PLUGIN_ROOT}/...`: 0 quebrados.
- 34 cabeçalhos `### PL-` distribuídos em 5 arquivos (7 + 9 + 5 + 6 + 7).
