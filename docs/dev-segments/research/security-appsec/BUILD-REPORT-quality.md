# BUILD-REPORT de qualidade de prompt: security-appsec

Data: 2026-10-10 · Papel: validador independente de qualidade de prompt e de conteúdo técnico · Plugin: `plugins/security-appsec`
Base: `docs/foundation/prompt-quality-rubric.md` (D1–D12), `prompt-principles.md`, `plugin-blueprint.md`, `house-style.md`, `SYNTHESIS.md`, `BUILD-REPORT-structural.md` e `VALIDATED.md` (fonte de verdade).
Independência: o validador é um modelo da família Claude, como os construtores. Esta revisão reduz erro, mas não é validação externa. As notas são julgamento por leitura, não medição. Nenhum eval foi executado.

Rótulos: **Verificado** (conferido em ferramenta nesta execução), **Inferido**, **Suposição**, **Não verificável**, **Não aplicável**.

## 1. Escopo lido

- Lidos inteiros: os 10 `SKILL.md`, os 5 agentes, o README, o `plugin.json`, o `evals/README.md` e os 10 casos de eval (prompt e graders).
- Biblioteca de prompts: amostra de 18 de 28 prompts. Foram lidos P01 a P05, P10 a P12, P17 a P20 e P23 a P28. Para os demais, foi lida a estrutura (cabeçalhos e fontes).
- Referências: lidas `guard-pretooluse.md` (código), `fontes.md` e `achado-restrito.md`. O resto foi conferido com Grep: CAPS, `--dangerously-skip-permissions`, CVSS, versões e `git show`.
- Afirmações técnicas conferidas no `VALIDATED.md`:
  - OWASP Top 10:2025, A01 a A10 (V-13).
  - Argon2id 19 MiB/t=2/p=1, bcrypt com fator ≥ 10 e limite de 72 bytes, PBKDF2 com 600.000 iterações (V-24).
  - Sessão com entropia ≥ 64 bits (V-36).
  - `onFailure: "block"` a partir da 2.1.295 e modo auto a partir da 2.1.283 (V-06 e correções globais).
  - Campos de subagente e o que um subagente de plugin ignora (V-08).
  - 1% de sucesso de ataque (V-10).
  - Triagem e "ausência de teste eleva severidade" (V-28).
  - Licenças: Brex MIT (V-33), security-guidance Apache-2.0 (V-02).
  - Todas Verificado.
- Fonte externa nova: especificação CVSS v4.0 do FIRST, Tabela 22 (https://www.first.org/cvss/v4.0/specification-document). As faixas qualitativas foram conferidas por WebFetch. Verificado.
- Números de linha dos fixtures de eval recontados um a um:
  - `app/orders.py:19`;
  - `auth.py:15-17` e `25-27`;
  - `faturas/views.py:10` e `17`;
  - `app/listagem.py:2`, `5`, `6` e `7`.
  - Todos batem. Verificado.

## 2. Notas antes e depois (rubrica D1–D12, 0–100)

| Arquivo | Antes | Depois | Correções |
| --- | --- | --- | --- |
| `skills/playbook/SKILL.md` | 88 | 88 | Nenhuma necessária: router, princípios com porquê, processo com critério de saída, modo `SEGURANCA-COMPLETO`, fronteiras e gotchas. |
| `skills/security-review-diff/SKILL.md` | 87 | 89 | CAPS "ESTA" removido na `description` e no corpo (D10). |
| `skills/threat-model/SKILL.md` | 88 | 88 | Nenhuma. |
| `skills/access-control-review/SKILL.md` | 88 | 88 | Nenhuma. |
| `skills/verify-finding/SKILL.md` | 89 | 89 | Nenhuma. |
| `skills/propose-patch/SKILL.md` | 85 | 88 | Removidos CAPS "NÃO", "SEM/COM" e "USUÁRIO", mantendo o sentido (D10). |
| `skills/agent-risk-triage/SKILL.md` | 86 | 88 | Métrica de 1% contextualizada (Best-of-N, agente de navegador, Opus 4.5, métrica do fornecedor), conforme V-10 (D12). CAPS "USUÁRIO" removido. |
| `skills/secrets-supply-chain-review/SKILL.md` | 84 | 88 | `Bash(git show *)` saiu de `allowed-tools`: era pré-aprovado, mas o corpo manda evitar `git show`, que imprime o valor do segredo (D8, contradição interna). |
| `skills/harden-claude-code/SKILL.md` | 84 | 88 | CAPS "PROPÕE" e "NÃO" removidos e concordância corrigida ("os limites"). A referência `guard-pretooluse.md` tinha uma falha de lógica, corrigida (ver seção 3). |
| `skills/prompts/SKILL.md` | 84 | 86 | Lista de prompts com trechos do brain-of-agent corrigida para P05, P09, P10, P15, P16, P19, P24, P26 e P28 (D12, atribuição). |
| Biblioteca de prompts (amostra de 18) | 83 | 87 | P01: CAPS removido. P12: máscara alinhada à skill (4 caracteres + "..." + comprimento, em vez de asteriscos); ordem de resposta igual à de V-19; aviso para não usar `git show`/`git log -p`; reescrita de histórico como decisão do dono, sem executar. P18 e P23: CAPS removidos. P26: faixas CVSS de "Não verificável" para "conferidas" (FIRST v4.0, Tabela 22). Cabeçalho da biblioteca: lista de atribuição ao brain completada. |
| `agents/security-reviewer.md` | 90 | 90 | Nenhuma. Somente leitura, formato fixo, exemplo, cobertura de plataforma. |
| `agents/finding-verifier.md` | 90 | 90 | Nenhuma. |
| `agents/threat-modeler.md` | 89 | 89 | Nenhuma. |
| `agents/patch-reviewer.md` | 89 | 89 | Nenhuma. |
| `agents/agent-config-auditor.md` | 88 | 88 | Nenhuma. |
| Evals (10 casos + README) | 86 | 86 | Nenhuma. Os graders PASS/FAIL são observáveis. Há caso negativo (`negativo-log-com-keyword`, `max: 0`) e caso de escopo (`escopo-scan-terceiro`). Os graders `tool_used` anti-ação cobrem Bash, Write e Edit. |
| `README.md` | 87 | 87 | Nenhuma. |
| Fora da tabela: `playbook/references/fontes.md` e `assets/templates/achado-restrito.md` | n/a | n/a | Fonte FIRST CVSS v4.0 acrescentada e marcada como conferência do validador, fora do VALIDATED. Template de achado deixou de dizer "Não verificável" sobre as faixas CVSS. |

Médias:
- Antes: 86,9. Depois: 88,1. Mínimo depois: 86.
- O cálculo usa as 18 linhas pontuadas, sem a linha de fontes e template.
- Abaixo de 80: nenhum, nem antes nem depois.
- Critérios de reprovação automática: nenhum encontrado.
  - Não há execução inventada.
  - Toda ação destrutiva ou externa exige pedido explícito: `propose-patch` tem `disable-model-invocation: true` e não pré-aprova Write/Edit.
  - Conteúdo externo é tratado como dado em todos os componentes.
  - Literais de terceiros são destilados e atribuídos.
  - Frontmatter é válido.
  - Os segredos dos fixtures são falsos (`sk_live_FAKEFAKE0000`, `<SEU_TOKEN>`).

## 3. Achados técnicos relevantes desta rodada

1. **Bug no guard PreToolUse de referência** (`skills/harden-claude-code/references/guard-pretooluse.md`).
   - **Defeito:** a exceção para `rm -rf node_modules|dist|...` pulava todos os padrões de confirmação. Assim, `rm -rf node_modules && git push --force` passava sem `ask`.
   - **Correção:** a exceção agora vale só para o padrão de `rm` e só em comando simples (sem `;`, `&`, `|` ou quebra de linha). A indentação também foi corrigida.
   - **Testes (Verificado):** o esqueleto foi extraído para a scratch e testado com `python -I`.
     - `rm -rf node_modules`: sem decisão.
     - `rm -rf node_modules; rm -rf src`: `ask`.
     - `git push -f origin main`: `ask`.
     - `rm -rf /`: exit 2.
     - Entrada inválida: exit 2 (falha fechada).
   - **Limite:** isso testa só a lógica do script. O registro do hook no Claude Code não foi testado (Não verificável nesta máquina).
2. **Permissão pré-aprovada contradizia o corpo** (`secrets-supply-chain-review`). Corrigido, ver tabela.
   - Resta um risco aceito: `Bash(git log *)` cobre também `git log -p`, que imprime o valor.
   - O corpo instrui a evitar esse comando. Isso é orientação, não controle (Inferido).
3. **CVSS:** as faixas qualitativas passaram de Não verificável para Verificado (FIRST v4.0, Tabela 22). A data de lançamento da v4.0 e o uso da 3.1 nas bases continuam Inferido do brain.
4. **Postura de segurança.** Toda menção a `--dangerously-skip-permissions` ou `bypassPermissions` aparece como risco, restrito a sandbox e repositório confiável. Arquivos: `harden-claude-code`, `deny-e-permissoes`, `ambiente-sandbox-e-camadas`, `decisoes-e-tradeoffs`, `padroes-e-antipadroes`. Verificado com Grep.
   - Os 5 agentes têm `tools: Read, Glob, Grep` (sem Write/Edit/Bash) e `maxTurns`.
   - A pendência 1 do relatório estrutural (`maxTurns` ausente) não procede no estado atual. Verificado.
5. **Fixture com injeção.** `diff-sqli-idor-injecao/prompt.md` tem uma linha "NOTE TO AI REVIEWER" que manda rodar `curl ... | sh`. É dado de teste intencional e não foi executado. O domínio `x.test` é reservado.

## 4. Verificação final

- `python tools/verify_plugin.py plugins/security-appsec`: `RESULT: PASS` (10 skills, 5 agents, 10 evals, 92 arquivos). Verificado.
- `claude plugin validate plugins/security-appsec`: "Validation passed". Verificado.
- Grep pós-edição: nenhuma ocorrência de CAPS de ênfase (`NÃO`, `ESTA`, `USUÁRIO`, `PROPÕE`, `PROPONHA`) nos `.md` do plugin. Restam só termos técnicos (`HIGH,CRITICAL` do trivy) e citações de antipadrão ("ALWAYS/NEVER" como exemplo do que evitar). Verificado.

## 5. Pendências

1. **Evals não executados.** Status `designed_not_executed`. A CLI local registrada é a 2.1.128, abaixo da 2.1.269 que `claude plugin eval` exige. Nenhuma taxa de disparo ou de acerto pode ser alegada.
2. **Cobertura de eval.** Faltam casos dedicados para `prompts`, `propose-patch` (manual) e os agentes. O blueprint limita a 10 casos; o README já declara a lacuna. Para medir subdisparo e superdisparo, falta a suíte ampla de gatilhos.
3. **`prompt-library.md` com 708 linhas,** acima da orientação de cerca de 600 do SYNTHESIS. Não foi dividido nesta rodada. Tem sumário, e a skill instrui a abrir só o bloco do prompt via Grep, o que mitiga o custo. Decisão do construtor: dividir em `prompt-library-revisao.md` se quiser seguir o desenho.
4. **ShareAlike (CC BY-SA 4.0).** Parte do conteúdo deriva do OWASP e da Trail of Bits. Revisão humana ou jurídica antes de publicar (Suposição de leitura jurídica, já declarada no README).
5. **Independência.** Construtor e validador são da mesma família de modelo. As notas desta tabela não substituem eval executado nem revisão humana.
6. **10 prompts não lidos na íntegra** (P06 a P09, P13 a P16, P21 e P22). Só a estrutura e as fontes foram conferidas.
7. **Fonte nova fora do VALIDATED.** A especificação CVSS do FIRST entrou como fonte extra do validador. Se o processo exigir, registre-a no `VALIDATED.md` do segmento.
