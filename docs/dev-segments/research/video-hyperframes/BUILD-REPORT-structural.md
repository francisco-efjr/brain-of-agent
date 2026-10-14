# BUILD-REPORT estrutural: video-hyperframes

Data: 2026-10-13. Escopo: validação estrutural de `plugins/video-hyperframes`. Conteúdo de skills, agentes e referências não foi reescrito. Nada do HyperFrames foi executado; o invólucro `hf.ps1` e os demais blocos PowerShell foram só analisados sintaticamente (parser do PowerShell, sem executar).

## 1. Resumo

- Veredito estrutural: **aprovado**. `verify_plugin.py` e `claude plugin validate` passam, sem nenhum aviso.
- Todos os componentes previstos no SYNTHESIS (seção 4) existem; nenhum ausente, nenhum arquivo vazio ou placeholder.
- Duas correções pontuais em defeitos que os validadores oficiais não detectam (flag inexistente no README; comando de exemplo que não parseia no PowerShell).
- Pendências são de design, de ferramenta compartilhada ou de decisão do dono (seção 5). Nenhuma delas reprova o plugin.

## 2. Contagens

| Item | Previsto (SYNTHESIS) | Encontrado |
| --- | --- | --- |
| Skills | 10 (`playbook`, `prompts` + 8 de tarefa) | 10 |
| Agentes | 5, somente leitura | 5 (`tools: Read, Grep, Glob`) |
| Comandos (`commands/`) | 0 | 0 |
| Referências do playbook | 10 | 10 |
| Templates TP-01 a TP-10 | 10 | 10 |
| Prompts VP-01 a VP-32 | 32 | 32 (8 + 11 + 13 em 3 arquivos) |
| Snippets VS01 a VS19 | 19 | 19 (linhas da tabela de `claude-md-snippets.md`) |
| Evals | 10 | 10 (`prompt.md` e `graders/` em todos; 3 graders negativos com `min: 0`, `max: 0`) |
| Arquivos | — | 76 no total (74 `.md` + `plugin.json` + `evals/.gitignore`) |
| Links relativos | — | 115 verificados, 0 quebrados |
| Descrições (`>-`) | < 1024 caracteres | skills 453 a 958; agentes 337 a 408; todas em `>-` |
| Playbook `SKILL.md` | ≤ 300 linhas | 228 |
| Blocos PowerShell em `.md` | — | 12; 0 erros de parse após a correção 2 |

## 3. Saídas das validações

- `python tools/verify_plugin.py plugins/video-hyperframes`, antes e depois das correções: `Plugin: video-hyperframes {'skills': 10, 'agents': 5, 'commands': 0, 'evals': 10, 'files': 74}` e `RESULT: PASS`, sem ERROR nem WARNING.
- `claude plugin validate plugins/video-hyperframes`, antes e depois: `✔ Validation passed`, sem avisos.
- Verificação complementar (somente leitura, script no scratchpad): frontmatter de todos os SKILL.md e agentes; `name` igual à pasta; `description` em `>-`; `disable-model-invocation: true` apenas em `video-toolchain-setup` e `video-render-deliver`; nenhum `.ps1`, `.sh`, `.mjs`, `.py`, `.exe` ou `.js`; nenhum `hooks/`, `bin/`, `.mcp.json`, `.lsp.json` ou `CLAUDE.md`; nenhuma ferramenta `Write`, `Edit` ou `Bash` nos agentes.

## 4. Correções feitas

1. `plugins/video-hyperframes/README.md`, linha 62: removida a flag `--strict` de `claude plugin validate <pasta-do-plugin> --strict`. O CLI instalado (2.1.128) responde `error: unknown option '--strict'` (verificado). O comando agora é `claude plugin validate <pasta-do-plugin>`.
2. `plugins/video-hyperframes/skills/playbook/assets/templates/hf-sessao.ps1.md`, exemplo "5. Como usar", linha 146: `--preset <nome>` virou `--preset "<nome>"`. Sem aspas, o PowerShell acusa `Operador '<' reservado para uso futuro` (verificado com `Parser::ParseInput`). Após a correção, os 12 blocos PowerShell do plugin parseiam com 0 erros.

Nenhum arquivo foi criado dentro do plugin. Nenhum conteúdo de skill, agente ou referência foi reescrito.

## 5. Comparação com o SYNTHESIS e pendências

Componentes previstos ausentes: **nenhum**. Os 10 skills, 5 agentes, 10 referências, 10 templates, 32 prompts VP, 19 snippets VS e 10 evals estão presentes.

Arquivos vazios ou placeholder: **nenhum**. O menor `.md` tem 70 bytes (grader `no-open-env.md`, de conteúdo válido). Não há `TODO`, `FIXME`, `XXX`, `placeholder` nem `PREENCHER`; a única ocorrência de "TBD" é a sigla "JTBD".

Pendências, não corrigidas (cada uma exige decisão ou está fora do plugin):

1. **`tools/verify_plugin.py` não mede descrições em bloco `>-`.** O parser lê o valor como o literal `>-` (2 caracteres), então uma descrição acima de 1024 caracteres passaria em silêncio. A ferramenta é compartilhada por todos os plugins, por isso a correção fica com o coordenador. Também não cobre: `.ps1` fora de lugar, ferramentas de agentes, `disable-model-invocation` e `min`/`max` dos graders. Nesta etapa, as medições foram feitas à mão.
2. **Modelo dos agentes.** Os 5 agentes têm `model: inherit`. O SYNTHESIS (4.5) previa `sonnet` para `frame-reviewer`, `composition-reviewer` e `fact-privacy-checker`, e `haiku` para `execution-security-auditor`. Não alterado: é decisão de custo.
3. **Sumário ausente em 2 arquivos acima de 100 linhas** (contrato do SYNTHESIS 4.10): `skills/playbook/assets/templates/hf-sessao.ps1.md` (190 linhas) e `skills/video-brief-interview/references/roteiro-oficial-de-perguntas.md` (111 linhas). Os demais 12 têm sumário. Não alterado, por ser formatação.
4. **Rastreabilidade dos IDs `V-nn`.** O plugin cita `V-nn` e `VALIDATED.md` (em 5 SKILL.md, no playbook e em vários references), além de caminhos internos como `docs/research/video-hyperframes/` e `brain-of-agent/ORCHESTRATOR.md`. Esses arquivos não viajam com o plugin, então quem instala não consegue resolver os IDs. Não são links quebrados, pois estão em crase. Os nomes de arquivos do upstream (`frame-worker-core.md`, `intent-interview.md`, `tts.md` etc.) dependem das skills oficiais do HyperFrames, que o README já lista como pré-requisito.
5. **Evals não executáveis nesta máquina.** O CLI 2.1.128 não tem o subcomando `claude plugin eval`, que exige Claude Code 2.1.269 ou superior. Já está anotado em `README.md` e `evals/README.md`. Estado: não verificável aqui.
6. **Nome `hf-sessao.ps1.md`.** Contém `.ps1` no nome, mas é texto `.md` (TP-06, nome previsto pelo SYNTHESIS). Não é executável. Mantido.
7. **Marketplace.** Não existe `dev-segments/.claude-plugin/marketplace.json`. A entrada de `video-hyperframes` ainda não foi adicionada; é pendência do coordenador (SYNTHESIS 4.10).
8. **Cor `#0b0f14`** em `skills/video-frame-review/references/contrato-de-composicao.md`, linha 71 (CSS de exemplo, fundo do `body`). Não está entre os valores do dono listados (`#1B2A3A`, `#C2456E`, "Mo baile"); mantido como exemplo genérico.
9. **Não executado por política:** teste `-DryRun` do invólucro (roda o CLI do HyperFrames), render, `claude plugin eval`. Só houve parse sintático.
10. **Conteúdo não revisado nesta etapa:** o VP-03 precisa de um quadro de exemplo completo (D5 do crítico), e a rubrica de prompts fica para o validador de qualidade.

## 6. Varredura de dados pessoais e de valores do dono

- "Francisco Edson" aparece só em `plugin.json` (`author`) e nos créditos do README (linha 115). Permitido.
- `francisco-efjr` aparece no comando de instalação do marketplace (README, linhas 58 e 62) e nos créditos. É o handle público do repositório, conforme a convenção do blueprint. Mantido.
- Caminhos `C:\Users\...` no plugin (15 ocorrências) são placeholders (`<usuario>`) ou padrões de detecção usados pelos agentes e pelos evals. Nenhum é caminho real.
- `#1B2A3A`, `#C2456E` e "Mo baile": **0 ocorrências**.

## 7. Referências cruzadas

- Tabela de intenções e README: todos os componentes citados existem (10 skills, 5 agentes, comandos `/video-hyperframes:video-toolchain-setup` e `/video-hyperframes:video-render-deliver`).
- As 28 referências a `/<slug>:playbook` de outros plugins existem em `plugins/`.
- Nomes de rotas do upstream (`motion-graphics`, `pr-to-video`, `talking-head-recut` etc.) aparecem como "Rota oficial" ou "Fora da v1", não como componentes do plugin.

## 8. Limites desta verificação

- Nenhum comportamento em runtime das skills e dos agentes foi testado.
- Links externos (`fontes.md`, URLs da documentação) não foram verificados na rede.
- O parse do PowerShell confirma só a sintaxe; não confirma o comportamento dos comandos.
