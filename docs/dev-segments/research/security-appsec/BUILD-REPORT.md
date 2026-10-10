# BUILD-REPORT: security-appsec (consolidado)

Data: 2026-10-10
Papel: gate final do plugin `plugins/security-appsec`.
Fontes consolidadas: `BUILD-REPORT-structural.md` e `BUILD-REPORT-quality.md` (ambos na mesma pasta).

Rótulos: **Verificado** (resultado de ferramenta nesta execução), **Inferido** (dedução a partir de leitura), **Suposição**, **Não verificável**, **Não aplicável**.

## 1. Resultado

| Item | Resultado | Rótulo |
|---|---|---|
| `tools/verify_plugin.py` sobre `plugins/security-appsec` | PASS, sem erros | Verificado |
| `claude plugin validate` sobre `plugins/security-appsec` | "Validation passed" | Verificado |
| Erros remanescentes | Nenhum | Verificado |
| Alterações feitas nesta rodada de gate | Nenhuma (nada reprovou, nada a corrigir) | Verificado |

Pass: sim (verificador sem ERROS e `claude plugin validate` aprovado).

## 2. Saídas resumidas das validações

- Verificador: `Plugin: security-appsec {'skills': 10, 'agents': 5, 'commands': 0, 'evals': 10, 'files': 92}` seguido de `RESULT: PASS`.
- Validador oficial: `Validating plugin manifest: ...\.claude-plugin\plugin.json` seguido de `✔ Validation passed`.
- Contagem de arquivos do plugin nesta rodada: 95 (inclui os 3 arquivos de metadados/README que o verificador não conta na linha de resumo; a diferença de 92 para 95 não foi investigada e não afeta o resultado).

## 3. Contagem de componentes

| Componente | Quantidade | Detalhe | Rótulo |
|---|---|---|---|
| Skills | 10 | playbook, prompts, security-review-diff, threat-model, access-control-review, verify-finding, propose-patch, agent-risk-triage, secrets-supply-chain-review, harden-claude-code | Verificado |
| Agentes | 5 | security-reviewer, finding-verifier, threat-modeler, patch-reviewer, agent-config-auditor | Verificado |
| Prompts na biblioteca (blocos de prompt) | 28 | P01 a P20 em `prompt-library.md` (20) e P21 a P28 em `prompt-library-processo.md` (8) | Verificado |
| Snippets de CLAUDE.md | 22 | S01 a S22 em `claude-md-snippets.md` | Verificado |
| Casos de eval | 10 | `evals/*/prompt.md` (E1 a E10); 25 arquivos de graders | Verificado |
| Arquivos de referência (`skills/*/references/`) | 30 | Inclui 12 do playbook | Verificado |
| Templates e assets (`playbook/assets/`) | 11 | 10 templates `.md`/`.json` previstos mais `matriz-aplicabilidade-seguranca.md` | Verificado |
| Comandos, hooks, `.mcp.json`, `.lsp.json`, `bin/` | 0 | Nenhum componente proibido ou ativo | Verificado |

## 4. Consolidação dos dois relatórios

### 4.1 Estrutura (`BUILD-REPORT-structural.md`)
- Frontmatter de skills e agentes consistente com o nome da pasta/arquivo; campos conhecidos apenas.
- `plugin.json` válido; sem declaração de `skills`/`agents`/`commands` (scan padrão).
- Links relativos sem alvo quebrado.
- Previstos pelo SYNTHESIS presentes: skills, referências, templates, prompts P01 a P28, snippets S01 a S22, evals E1 a E10, agentes.

### 4.2 Qualidade de prompt e conteúdo (`BUILD-REPORT-quality.md`)
- Nota média (rubrica D1 a D12, 18 linhas pontuadas): 86,9 antes, 88,1 depois; mínimo 86. Nenhum item abaixo de 80.
- Reprovações automáticas: nenhuma encontrada.
- Correções aplicadas nessa rodada (já no plugin, não alteradas agora):
  - Bug no guard PreToolUse de referência (`harden-claude-code/references/guard-pretooluse.md`): a exceção para `rm -rf node_modules|dist|...` pulava todos os padrões de confirmação. Corrigido para valer só no padrão de `rm` e só em comando simples. Testado com `python -I` (Verificado para a lógica do script; registro do hook no Claude Code: Não verificável nesta máquina).
  - Permissão pré-aprovada que contradizia o corpo em `secrets-supply-chain-review`. Corrigido. Risco residual aceito: `Bash(git log *)` também cobre `git log -p`; o corpo instrui a evitar (orientação, não controle; Inferido).
  - Faixas qualitativas do CVSS passaram a Verificado (FIRST CVSS v4.0, Tabela 22).
- Postura: menções a `--dangerously-skip-permissions` e `bypassPermissions` aparecem só como risco, restritas a sandbox e repositório confiável.
- Agentes: `tools: Read, Glob, Grep` (sem Write/Edit/Bash) e `maxTurns` definido nos 5.

## 5. Notas

- Conflito entre relatórios resolvido: o relatório estrutural listava a ausência de `maxTurns` nos agentes como pendência. Nesta rodada, `grep` confirma `maxTurns` (20 ou 25) nos 5 agentes. A pendência não procede no estado atual (Verificado).
- Fixture de injeção intencional: `evals/diff-sqli-idor-injecao/prompt.md` contém a linha "NOTE TO AI REVIEWER" pedindo `curl ... | sh`. É dado de teste, não foi executado; domínio `x.test` é reservado.
- Segredos dos fixtures são falsos (`sk_live_FAKEFAKE0000`, `<SEU_TOKEN>`).
- Atribuição de fontes: licenças CC BY-SA 4.0 (OWASP, Trail of Bits), Apache-2.0 (getsentry, security-guidance), MIT (anthropics, awesome-copilot, Brex). Trechos de terceiros foram destilados e atribuídos.

## 6. Pendências

1. **Evals não executados.** Status `designed_not_executed`. A CLI local registrada (2.1.128, conforme relatório estrutural) é inferior à exigida por `claude plugin eval`. Nenhuma taxa de disparo ou acerto pode ser alegada. Rótulo: Verificado (status) / Não verificável (desempenho).
2. **Cobertura de eval.** Faltam casos dedicados para `prompts`, `propose-patch` (acionamento manual) e para os agentes. O blueprint limita a 10 casos; a lacuna está declarada no README. Medir subdisparo e superdisparo exige suíte ampla de gatilhos.
3. **`prompt-library.md` com 708 linhas,** acima da orientação de ~600 do SYNTHESIS. Não dividido. Há sumário e a skill orienta a abrir só o bloco do prompt via Grep. Decisão do construtor (ex.: `prompt-library-revisao.md`).
4. **ShareAlike (CC BY-SA 4.0).** Parte do conteúdo deriva de OWASP e Trail of Bits. Revisão humana ou jurídica antes de publicar. Rótulo: Suposição de leitura jurídica.
5. **Independência do validador.** Construtor e validador são da mesma família de modelo. As notas de qualidade são julgamento por leitura, não medição, e não substituem eval executado nem revisão humana.
6. **Prompts não lidos na íntegra na rodada de qualidade:** P06 a P09, P13 a P16, P21 e P22 (só estrutura e fontes conferidas).
7. **Fonte nova fora do `VALIDATED.md`:** especificação CVSS v4.0 do FIRST. Registrar no `VALIDATED.md` se o processo exigir.
8. **Conteúdo dos graders** não foi relido na rodada estrutural; a presença foi verificada.

## 7. Estado final

- Estrutura válida pelo verificador e pelo validador oficial. Verificado.
- Sem erros, sem alterações no conteúdo do plugin nesta rodada de gate.
- Pendências são de conteúdo, cobertura de eval e decisão, não de estrutura.
