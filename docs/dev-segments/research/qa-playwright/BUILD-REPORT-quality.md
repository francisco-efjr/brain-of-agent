# qa-playwright: relatório de qualidade do build

Data: 2026-10-13 · Validador: Claude Opus 5.5 (`claude-opus-5-5`) · Objeto: `plugins/qa-playwright/` (75 arquivos contados pelo `verify_plugin.py`), escrito por 3 construtores Claude Sonnet 5.5 em paralelo.

**Independência.** Esta é uma revisão da **mesma família de modelos** que pesquisou, desenhou, criticou e construiu o plugin. Ela reduz erro de leitura, de contagem e de coerência, mas **não é validação externa**. As notas abaixo são autoatribuídas por leitura; nenhuma eval foi executada (`designed_not_executed`) e nenhum comando npm, npx ou Playwright foi rodado nesta revisão.

**Método.** Leitura integral dos 75 arquivos do plugin e de `prompt-quality-rubric.md`, `plugin-blueprint.md`, `plugin-format-spec.md`, `house-style.md`, `SYNTHESIS.md` (Parecer do crítico e seção 8 como regra), `VERIFICACAO-ORQUESTRADOR.md` (X-01..X-26) e trechos de `VALIDATED.md`. Conferência mecânica de todos os links relativos e caminhos `${CLAUDE_PLUGIN_ROOT}/...` (0 quebrados), dos arquivos de outros plugins citados (`qa-testing`, `backend-api`, `mobile-apps`: todos existem) e de padrões proibidos (`@latest`, `networkidle`, `waitForTimeout` em código, `--with-deps`, `Bash(npx playwright:*)`, `\|` no `--grep`).

## 1. Notas D1–D12 (depois das correções)

Escala 0–5 por dimensão; nota = média × 20. Nenhum componente cai em critério de reprovação automática.

| Componente | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | D11 | D12 | Média | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `skills/playbook` | 5 | 5 | 5 | 5 | 4 | 5 | 5 | 5 | 4 | 5 | 4 | 5 | 4,75 | **95** |
| `feature-inventory` | 5 | 4 | 5 | 5 | 4 | 5 | 4 | 4 | 5 | 5 | 4 | 4 | 4,50 | **90** |
| `harness-setup` | 4 | 5 | 5 | 5 | 4 | 5 | 5 | 5 | 4 | 5 | 4 | 5 | 4,67 | **93** |
| `explore-feature` | 5 | 5 | 5 | 5 | 4 | 5 | 5 | 5 | 4 | 5 | 4 | 5 | 4,75 | **95** |
| `write-specs` | 5 | 5 | 5 | 5 | 4 | 5 | 5 | 4 | 5 | 5 | 4 | 5 | 4,75 | **95** |
| `api-and-network` | 5 | 5 | 5 | 5 | 4 | 4 | 4 | 4 | 5 | 5 | 4 | 4 | 4,50 | **90** |
| `visual-a11y-responsive` | 5 | 5 | 5 | 5 | 4 | 4 | 4 | 5 | 5 | 5 | 4 | 4 | 4,58 | **92** |
| `failure-triage` | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 4 | 5 | 5 | 4 | 4,83 | **97** |
| `evidence-report` | 5 | 5 | 5 | 5 | 4 | 5 | 5 | 5 | 5 | 5 | 4 | 5 | 4,83 | **97** |
| `non-web-systems` | 5 | 5 | 5 | 5 | 5 | 5 | 4 | 5 | 4 | 5 | 4 | 4 | 4,67 | **93** |
| `skills/prompts` | 5 | 4 | 5 | 5 | 4 | 5 | 4 | 4 | 5 | 5 | 4 | 4 | 4,50 | **90** |
| agente `feature-explorer` | 5 | 5 | 5 | 5 | 4 | 5 | 5 | 4 | 4 | 5 | 5 | 5 | 4,75 | **95** |
| agente `spec-writer` | 5 | 5 | 5 | 5 | 4 | 5 | 5 | 4 | 5 | 5 | 4 | 5 | 4,75 | **95** |
| agente `spec-reviewer` | 5 | 5 | 5 | 5 | 4 | 5 | 5 | 5 | 5 | 5 | 5 | 4 | 4,83 | **97** |
| agente `failure-triager` | 5 | 5 | 5 | 5 | 4 | 5 | 5 | 4 | 5 | 5 | 5 | 5 | 4,83 | **97** |
| agente `matrix-auditor` | 5 | 5 | 5 | 5 | 4 | 5 | 5 | 4 | 5 | 5 | 5 | 5 | 4,83 | **97** |
| **Média dos 16** | | | | | | | | | | | | | | **94,3** |

Menor nota: **90** (`feature-inventory`, `api-and-network`, `prompts`). Meta (≥ 80 em todos) atingida.

Justificativa das notas abaixo de 5, por padrão recorrente:
- **D5 (exemplos) = 4** em quase todos: os exemplos estão em `references/` (bom para D9), e o corpo traz só o formato de saída. Nota 5 em `failure-triage` (caso completo mais contraexemplo) e `non-web-systems` (laço de polling em bash e PowerShell).
- **D8 = 4** nos agentes com `Bash` e nas skills que pré-aprovam `Bash(npx playwright test:*)`: o campo `tools` e o prefixo não restringem subcomandos nem flags; o limite é por instrução. Está declarado em todos, mas não é barreira técnica.
- **D9 = 4** onde há sobreposição moderada com uma referência (playbook × `seguranca-e-evidencia`; `explore-feature` × `exploracao-cli`; `non-web-systems` × `escopo-e-stacks`; `harness-setup` × `versoes-e-instalacao`).
- **D11 = 4** onde a skill cobre ambiguidade e falta de dado, mas não toda falha de ferramenta (servidor que não sobe, comando que muda de nome).
- **D12 = 4** onde resta afirmação técnica relevante só Inferida ou Não verificada, embora rotulada: GraphQL e casos de borda de rede (`api-and-network`), iOS e `pull` no PowerShell (`non-web-systems`), opções de `toHaveScreenshot` não reexecutadas (`visual`), casamento de `allowed-tools` com comando prefixado por `E2E_RUN=` (`failure-triage`), padrões de `Grep` não testados (`spec-reviewer`).

Antes das correções, as notas de D12 eram mais baixas (3 a 4) em `explore-feature`, `harness-setup`, `write-specs`, `evidence-report`, os três agentes que executam e a `prompts`, porque marcavam como Inferido ou "não exercitado" o que X-22..X-26 já tinham verificado. O `failure-triager` tinha D8 = 3 pela incoerência descrita na correção 8.

## 2. Coerência entre os três construtores

- **Nomes:** as 11 skills, os 5 agentes, os 9 templates (T-01..T-09) e as 12 referências citados existem com o nome do desenho. Os 22 prompts (P-01..P-22) batem entre `prompts/SKILL.md` e `prompt-library.md`. Checklists CP, CI, CE, CS-01..CS-20, CG, CF, CD, CM e guardrails G-01..G-35 são consistentes entre playbook, checklist, skills e agentes.
- **Regras sem contradição:** healer só propõe (skill, agente, playbook, prompts P-11/P-12, G-24); `state-load` por caminho, nunca leitura de `playwright/.auth/`; `E2E_RUN` com `Remove-Item` no PowerShell e prefixos `triagem-`/`auditoria-`; teto de 15 e 8 com `PLAYWRIGHT-COMPLETO` sem teto; coluna Prova (`spec-estável` × `exploração`); só `evidence-report` muda status, aplicada pelo agente principal, e o `matrix-auditor` confere; mesma lista de flags proibidas dentro dos prefixos. A única incoerência real era a do `failure-triager` (correção 8).
- **Desenho aprovado preservado:** nenhuma mudança de arquitetura, nome, ciclo ou papel.

## 3. Correções feitas

1. `skills/playbook/references/exploracao-cli.md` → tabela de comandos ganhou a linha **Verificado (X-23, X-26)** com `-s=`, `state-load` + `goto`, `open --device`, `snapshot`/`screenshot --filename` em subpasta, `requests` e `request <n>`, `resize`, `set-color-scheme`, `find --regex "<padrão>"` e `eval --raw`; a linha "só no `--help`" ficou só com o que segue sem execução.
2. `exploracao-cli.md` → "Login sem senha no contexto" passou de Inferido (S-22) a **Verificado (X-23a–d)**, com o eco literal do `fill` e o fluxo `open` → `state-load` → `goto`; a afirmação negativa (estado de uma porta não vale na outra) continua Inferida.
3. `exploracao-cli.md` → sintaxe base: `-s=` em todos os comandos, `--filename` com subpasta, a armadilha `find "x" --regex` (erro) contra `find --regex "<padrão>"`, e `--raw` verificado.
4. `skills/explore-feature/SKILL.md` → tabela de comandos reescrita com o status real (antes marcava oito comandos verificados como "ainda não exercitados"); `fill` de senha de Inferido para Verificado (X-23); `requests` no passo 4; origem com X-23 e X-26.
5. `agents/feature-explorer.md` → parágrafo de estado de verificação atualizado com X-23 e X-26.
6. `agents/spec-writer.md` → gate (X-24) e login (X-23) deixam de ser "ainda Inferido"; `--grep` sem barra invertida explícito.
7. `agents/matrix-auditor.md` → `results.json`: `stats` verificado (X-24), campos por teste seguem a conferir; regra para `stats.unexpected` e `stats.flaky` acima de zero.
8. `agents/failure-triager.md` → a lista de Bash permitidos tinha só a reexecução única, mas o passo 1 mandava rodar `--repeat-each=5`: incoerência resolvida (permitido com outro `E2E_RUN`).
9. `skills/evidence-report/SKILL.md` → `results.json` com `stats` verificado (X-24) no passo 2 e no rodapé.
10. `skills/playbook/references/config-execucao-e-ci.md` → `stats` do `results.json` (X-24); `testMatch` padrão sem `*.setup.ts` (X-25); estado por porta verificado (X-23); gate verificado (X-24) com aviso de que as cópias do `--repeat-each` e os 2 workers rodam em paralelo; porta livre depois da execução (X-24); filtro posicional verificado **só no Git Bash** (o texto dizia "PowerShell e Git Bash"); `--with-deps` só no runner da CI; gate com login marcado como não exercitado, com conduta.
11. `skills/playbook/references/versoes-e-instalacao.md` → `-E` sem `^` e `npm ci` reprodutível verificados (X-22); antes, "S-02 ainda é item de smoke".
12. `skills/playbook/references/seguranca-e-evidencia.md` → eco do `fill` e ausência de trace com `trace: 'off'` verificados (X-23).
13. `skills/playbook/references/decisoes-e-tradeoffs.md` → risco remanescente "login Inferido até o S-22" atualizado; siglas S- e X-; a tabela "Papéis da rodada", cópia literal da do playbook, virou um parágrafo com o porquê e o ponteiro (cerca de 10 linhas a menos).
14. `escopo-e-stacks.md`, `rede-tempo-visual-a11y.md`, `skills/visual-a11y-responsive/SKILL.md` e `prompt-library.md` (P-17) → `open --device`, `resize` e `set-color-scheme` de "não exercitados" para Verificado (X-26), com o código que cada um gera.
15. `skills/harness-setup/SKILL.md` → X-22 no passo 4, X-23 no passo 9 e no rodapé; o bloco PowerShell não remove mais `E2E_USER`/`E2E_PASSWORD` que o usuário exportou (só o que o agente definiu) e explica por que `E2E_PORT` e `E2E_REUSE` esquecidos fariam o gate reutilizar a instância de exploração.
16. `skills/playbook/SKILL.md` → bloco de comandos cita X-16 e X-24 e marca o filtro posicional como Git Bash; o gotcha do `fill` cita X-23.
17. `README.md` → removida a nota de construção que vazou ("as partes do plugin são escritas em paralelo... ausente"); X-01..X-26; limitações reescritas (instalação, login e gate verificados; pendências S-05, S-14, S-19, S-24 e login com outro mecanismo de sessão; lista de comandos da CLI exercitados; risco do prefixo com variável de ambiente).
18. `skills/playbook/references/fontes.md` → linhas X-22..X-26, data e condições do segundo smoke, filtro posicional no Git Bash, V-02 cobrindo X-22..X-26.
19. `skills/prompts/references/prompt-library.md` → fontes do P-06 (X-23) e texto e fontes do P-17 (X-26).
20. `skills/explore-feature/references/exemplo-nota-de-exploracao.md` → `requests` verificado (X-26), com o formato real da saída.
21. `skills/write-specs/references/exemplo-spec-comentado.md` e `skills/write-specs/SKILL.md` → resultado real do gate (X-24: efeito 5/5 vermelho, borda 5/5 verde) e aviso de paralelismo para contador global.
22. `assets/templates/playwright.config.ts` → marcas "Proposta" do login trocadas por X-23; X-25 no projeto sem login; o cabeçalho diz o que segue não verificado (S-09: `msedge` e `chromium` sem download).
23. `assets/templates/F-NN-slug.spec.ts` → o comentário do contador global inclui as cópias do próprio teste no gate; gate verificado; filtro posicional marcado como Git Bash.
24. `assets/templates/auth.setup.ts` → nota de verificação (X-23) e lembrete de ajustar rota, rótulos e estado final.
25. `assets/templates/github-actions-e2e.yml` → comentário: `--with-deps` roda com sudo só no runner Linux efêmero; na máquina local continua exigindo confirmação (G-12).
26. `skills/playbook/references/checklist-completo.md` → CG-01/CG-02 com X-24; CG-08 citava R-26 (risco do `--reporter`) como fonte de "`--list` não é execução", trocado por house #2 e PR-04; CE-03 com `goto` e X-23; CP-03 com X-22.
27. `skills/api-and-network/references/exemplos-request-route.md` e `rede-tempo-visual-a11y.md` → títulos fora da convenção (`@api` num teste com `page`; `@a11y`) trocados por `@ui`: o `--grep "@ui|@api"` os classificaria errado ou os perderia.
28. `skills/playbook/references/claude-md-snippets.md` → bloco P-02 alinhado ao da `prompt-library` (linha do modo completo contra keyword em documento); Q-06 cita X-23.
29. `skills/api-and-network/SKILL.md` → pré-checagem 5 com casos de borda (só backend de produção, sem token de teste, contrato desconhecido, Service Worker que escapa da rota).
30. `skills/prompts/SKILL.md` → exemplo curto de entrega de prompt (formato das 2 a 4 linhas).
31. `evals/android-nativo-na/graders/criteria.md` → o item 2 passa a aceitar a menção à rota `adb` verificada noutro AVD (X-21), para não reprovar uma resposta correta que segue o próprio plugin.

## 4. Achados não corrigidos (com motivo)

1. **`allowed-tools: Bash(npx playwright test:*)` contra comandos com variável na frente** (`E2E_RUN=<id> npx playwright test ...`; no PowerShell, `$env:E2E_RUN=...; npx ...`). É provável que o prefixo não case e o Claude Code peça permissão. Não verificado (exigiria rodar o Claude Code); a correção mudaria o desenho da evidência por execução (DO-12). Registrado no README como Não verificado.
2. **Gate, evidência e reexecução do auditor com login** (`E2E_AUTH=1` mais `--grep "F-NN"`): não se sabe se o filtro deixa de fora o teste do projeto `setup`. Não exercitado em X-22..X-26 (X-23 rodou `--project=setup` sozinho; X-24 rodou o gate sem login). Deixei a conduta em `config-execucao-e-ci.md`; a decisão de desenho é do orquestrador depois de um smoke.
3. **Sintaxe do `lock`** para recurso global não aparece em nenhum template; o plugin manda usá-lo (V-34) sem exemplo de código. Não escrevi a sintaxe porque ela não foi conferida no 1.64.0.
4. **Duplicação moderada mantida:** tabela de tipos de sistema em `non-web-systems` × `escopo-e-stacks`; P-02 em `prompt-library` e em `claude-md-snippets`; resumo de segurança no playbook × G-01..G-35. Cada skill carrega sozinha; o custo é de dezenas de linhas, não de arquivos inteiros.
5. **`plugin.json` com `repository` do `brain-of-agent`**, enquanto os outros plugins omitem o campo e a spec de formato cita `dev-segments`. Válido e sem efeito técnico; é decisão de publicação.
6. **Linha 12 do playbook** ("se uma parte não existir na instalação, registre ausente") nasceu da construção em paralelo, mas é robustez útil (instalação parcial, modo B). Mantida.
7. **Cobertura de evals incompleta e já declarada** em `evals/README.md`: sem caso positivo de `PLAYWRIGHT-COMPLETO`, sem caso de delegação para os agentes, sem caso para `api-and-network`, `visual-a11y-responsive`, `evidence-report`, `harness-setup` e `prompts`. Criar casos novos fica para depois da primeira execução das evals.
8. **Itens ainda não verificados e rotulados no plugin:** `--fail-on-flaky-tests` (S-05), filtro posicional no PowerShell, URL com `&` no PowerShell via `npx`, `--debug=cli` com `attach` (L-1), `PW_CHANNEL=msedge`/`chromium` (S-09), MCP num cliente real, CLI contra Electron e extensão, `pull` do `adb` no PowerShell, XCUITest, Detox, Patrol.

## 5. Riscos remanescentes

- **Revisão da mesma família de modelos**; notas autoatribuídas até alguém rodar `claude plugin eval` com baseline (a CLI da fábrica é 2.1.128; a eval exige 2.1.269 ou superior).
- **Login verificado só no sistema-demo** (cookie `HttpOnly`, sessão em servidor). Sessão em `sessionStorage`, token em memória, SSO e MFA não foram exercitados; SSO, MFA e CAPTCHA ficam `Bloqueado` por regra.
- **Gate sob paralelismo com estado global:** as cópias do `--repeat-each=5` e os 2 workers rodam em paralelo; o template afirma delta, mas um contador global ainda pode colidir. A mitigação (`lock`, conta por teste, banco por instância) depende do sistema.
- **Limites por instrução:** prefixos pré-aprovados e `tools` de agente não barram flags perigosas; a matriz em Markdown continua editável pelo modelo (defesa de processo: `evidence-report` escreve, `matrix-auditor` confere).
- **Custo e teto não medidos** (S-14): 15/8 é ponto de partida.
- **Rodada completa com os agentes não simulada** (S-24); harness em projeto não-JS não exercitado (S-19).
- **Leitura concorrente:** um agente de dogfood leu o plugin durante esta revisão; algumas edições aconteceram nesse intervalo. Cada edição foi atômica por arquivo, mas uma leitura feita no meio pode ter visto rótulos antigos.

## 6. Verificadores

Rodados depois de todas as correções:

```text
python tools/verify_plugin.py plugins/qa-playwright
Plugin: qa-playwright  {'skills': 11, 'agents': 5, 'commands': 0, 'evals': 10, 'files': 75}
RESULT: PASS

claude.exe plugin validate plugins/qa-playwright
✔ Validation passed
```

## 7. Veredito

**APROVADO.** Os 16 componentes avaliados ficam entre 90 e 97 (média 94,3), sem critério de reprovação automática, sem contradição entre playbook, skills e agentes, com os comandos, a config e o PowerShell coerentes com X-03..X-26, e com os rótulos atualizados para Verificado onde X-22..X-26 provam. As ressalvas da seção 5 estão declaradas no próprio plugin (README e referências) como Inferido ou Não verificado. Este veredito é de uma revisão da mesma família de modelos, não de validação externa; ele não substitui a execução das evals nem a rodada simulada S-24.

Validado em: 2026-10-13 · Claude Opus 5.5 (`claude-opus-5-5`) · sem executar npm, npx nem scripts do Playwright.
