# BUILD-REPORT: plugin mobile-apps

Data: 2026-10-10. Plugin: `C:\Users\Francisco Edson\dev-segments\plugins\mobile-apps`.
Consolida: `BUILD-REPORT-structural.md` (validação estrutural) e `BUILD-REPORT-quality.md` (validação de qualidade).
Gate final executado nesta rodada. Nenhum arquivo do plugin foi alterado nesta rodada.

## 1. Resultado do gate

| Verificação | Comando | Resultado |
| --- | --- | --- |
| Verificador do repositório | `python tools/verify_plugin.py plugins/mobile-apps` | `RESULT: PASS`, sem linhas de erro ou aviso (Verificado) |
| Validador oficial | `claude.exe plugin validate plugins/mobile-apps` | `Validation passed` (Verificado) |

Situação: pass = true. O verificador não reportou ERROS, e o validador oficial passou.

## 2. Contagens

| Componente | Quantidade | Origem da contagem |
| --- | --- | --- |
| Skills de tarefa | 9 | `skills/mobile-*/SKILL.md` (Verificado) |
| Skills de apoio | 2 (`playbook`, `prompts`) | `skills/playbook/SKILL.md`, `skills/prompts/SKILL.md` (Verificado) |
| Total de skills | 11 | verificador (Verificado) |
| Agentes | 5 | `agents/*.md` (Verificado) |
| Comandos | 0 | verificador (Verificado) |
| Prompts na biblioteca (blocos de prompt) | 33 | seções `## P-NN` em `skills/prompts/references/prompt-library.md` (Verificado) |
| Casos de eval | 11 | `evals/*/prompt.md`, com graders; ver `evals/README.md` (Verificado pelo verificador e pela revisão de qualidade) |
| Arquivos de referência | 31 | arquivos sob pastas `references/` (Verificado por contagem) |
| Templates do playbook | 18 | `skills/playbook/assets/templates/` (Verificado) |
| Arquivos no total | 107 | contagem do verificador (Verificado). Uma contagem simples com `find` dá 109, pela inclusão de metadados e do `.gitignore` das evals. Diferença de contagem, sem erro. |

## 3. Correções

Nenhuma correção nesta rodada do gate. Ambos os validadores passaram sem mudanças.

Correções já feitas nas etapas anteriores, registradas nos relatórios de origem:

- Estrutural: link quebrado em `skills/mobile-store-release-check/SKILL.md` (passo 5) apontava para `prompts-release.md`, inexistente. Trocado por `prompt-library.md`, seção `P-26` (Verificado).
- Qualidade: `allowed-tools` substituído pelo entendimento correto de pré-aprovação. `disallowed-tools: Write, Edit, NotebookEdit` foi acrescentado às skills de auditoria e planejamento. A semântica foi documentada no playbook e no README (Verificado pela leitura da fonte oficial de skills, em 2026-10-10).
- Qualidade: evals `no-exec` e `no-publish` casavam a entrada inteira do Bash, o que gerava falso FAIL. Agora casam só o campo `command`. `no-full-reading` ganhou regex para caminho do Windows (Verificado por testes com entradas sintéticas).
- Qualidade: caso de eval reserva `ios-sem-mac-windows` criado (11º caso).
- Qualidade: 12 regras de acessibilidade do SwiftUI completadas com atribuição MIT (Verificado pela leitura da fonte).

## 4. Notas de qualidade

- Média antes: 86,7. Média depois: 88,3. Mínimo depois: 86 (`mobile-build-troubleshoot`). Nenhum artefato abaixo de 80. Nenhum critério de reprovação automática encontrado (Inferido: julgamento por leitura com a rubrica D1–D12, não medição).
- Independência parcial: os construtores e o validador são da mesma família de modelos.
- Nenhum eval foi executado (`designed_not_executed`).
- Segurança: nenhum segredo no plugin. Ações externas (publicação, submit, promoção de trilha) exigem ficha confirmada no chat. Revisores e auditores não têm Write, Edit nem Bash. Nenhum hook, `.mcp.json`, `.lsp.json` ou `bin/` ativo.
- `--dangerously-skip-permissions` aparece apenas como risco, com allowlist como alternativa e sandbox descartável como única exceção (Verificado pela busca no plugin).
- Direitos autorais: o único bloco literal de terceiros (P-03) é texto do próprio validador (V-49). As regras do SwiftUI Pro foram resumidas com redação própria e atribuição (licença MIT, Paul Hudson).

## 5. Pendências

1. Executar `claude plugin eval .` com 3 execuções por caso. Exige Claude Code 2.1.269 ou superior (a instalação local registrada é 2.1.128). Na primeira rodada, confirmar que os graders `tool_used` comparam o regex com a entrada serializada em JSON (Não verificado).
2. `disallowed-tools` vale só até a próxima mensagem do usuário. Para garantia em auditorias de várias mensagens, usar regras `deny` no projeto. Decisão do usuário.
3. Atualizar a seção 4.2 de `docs/research/mobile-apps/SYNTHESIS.md` para refletir o arquivo único `prompt-library.md`, no lugar dos seis `prompts-*.md` previstos. Decisão tomada: não criar os seis arquivos. Documento de pesquisa, não editado nesta rodada.
4. Casos de eval ainda ausentes para `mobile-test-strategy`, `mobile-pr-reviewer` e para o pedido de `MOBILE-COMPLETO`.
5. Referências externas `references/accessibility.md` e `references/stability.md` citadas em `checklist-completo.md`, `ios-swift.md` e `prompt-library.md` (V-11). `accessibility.md` foi incorporado com resumo. `stability.md` está resumido via V-11. Confirmar se ainda há citações a esses caminhos como arquivos do plugin.
6. Lacunas de fonte herdadas, sem mudança: acessibilidade em RN e Flutter, payload de push, MASVS (níveis e IDs), navegação, conflito no CloudKit e energia no iOS.

## 6. Saídas resumidas das validações

```
verify_plugin.py plugins/mobile-apps
Plugin: mobile-apps  {'skills': 11, 'agents': 5, 'commands': 0, 'evals': 11, 'files': 107}
RESULT: PASS

claude plugin validate plugins/mobile-apps
Validating plugin manifest: .../plugins/mobile-apps/.claude-plugin/plugin.json
Validation passed
```

## 7. Rótulos

- Verificado: resultados dos dois validadores nesta rodada, contagens de skills, agentes, evals, prompts, templates, referências e arquivos, e as correções citadas.
- Inferido: nota média e julgamento de qualidade (leitura, não medição).
- Não verificado: execução dos evals e comportamento dos graders `tool_used` em entrada real.
- Não aplicável: execução do plugin em sessão real.
