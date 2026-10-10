# BUILD-REPORT de qualidade: devops-cloud-infra

Data: 2026-10-10 · Plugin: `plugins/devops-cloud-infra` · Papel: validador independente de qualidade de prompt e de conteúdo técnico · Rubrica: `docs/foundation/prompt-quality-rubric.md` (D1–D12, nota = média × 20).

Declaração de independência: este validador é um modelo Claude, da mesma família dos construtores. A revisão foi adversarial e separada da construção, mas **não é validação externa**. As notas vêm de leitura, não de execução: nenhum caso de `evals/` foi rodado (`designed_not_executed`).

Rótulos: **Verificado** (visto em arquivo, saída de ferramenta ou página lida nesta execução) · **Inferido** · **Suposição** · **Não verificável**.

## 1. Resultado

| Verificação | Resultado |
| --- | --- |
| `python tools/verify_plugin.py plugins/devops-cloud-infra` | **PASS**: skills 10, agents 4, commands 1, evals 15, arquivos 109 (Verificado) |
| `claude.exe plugin validate plugins/devops-cloud-infra` | **Validation passed** (Verificado) |
| Critérios de reprovação automática | Nenhum encontrado (detalhes na seção 4) |
| Nota mínima depois | 86 (`cloud-review`, `prompts`, comando `plan-infra`) |

## 2. Notas por artefato (antes → depois)

| Arquivo | Antes | Depois | Correções |
| --- | --- | --- | --- |
| `skills/playbook/SKILL.md` | 88 | 89 | O cabeçalho agora diz onde se resolvem os IDs `K-nn` (fontes.md), `SN-nn` (claude-md-snippets.md) e `GT-nn` (Gotchas), que as skills citam sem dizer onde ficam |
| `skills/prompts/SKILL.md` | 86 | 86 | Sem mudança no corpo; correções foram na biblioteca |
| `skills/iac-review/SKILL.md` | 86 | 89 | Removida a referência solta `(C-15)`, ID da fundação que o usuário do plugin não tem, e trocada pelo motivo da regra; `K7` passa a apontar para `fontes.md` |
| `skills/iac-review/references/terraform.md` | 87 | 88 | Leitura de plan em JSON: substituição também aparece como `["create","delete"]` com `create_before_destroy` (antes só `["delete","create"]`) |
| `skills/gha-hardening-review/SKILL.md` | 87 | 87 | Sem mudança no corpo; URL da SLSA v1.2 acrescentada em `references/supply-chain.md` |
| `skills/helm-gitops-review/SKILL.md` | 87 | 87 | Sem mudança; afirmações de Argo CD (rollback bloqueado com auto-sync, self-heal de 5 s) e Flux (`wait` ignora `healthChecks`) conferidas contra `VALIDATED.md` (V-31, V-33) |
| `skills/secrets-review/SKILL.md` | 86 | 87 | `allowed-tools` pré-aprova o `git log --all --diff-filter=A --name-only` que o passo 2 manda rodar (somente leitura, só nomes de arquivo); caso de eval próprio criado |
| `skills/progressive-delivery/SKILL.md` | 88 | 88 | Sem mudança; campos de Flagger e Argo Rollouts conferidos contra `VALIDATED.md` (V-44, V-45) |
| `skills/cloud-review/SKILL.md` | 85 | 86 | Caso de eval próprio criado (Lambda e SQS); LM-02/LM-03 da referência conferidos |
| `skills/infra-troubleshoot/SKILL.md` | 89 | 89 | Sem mudança |
| `skills/deploy-infra/SKILL.md` | 83 | 88 | IDs soltos da síntese (`TP-01`, `TP-13`) trocados pelos nomes dos templates; `K7` explicado em linha; "PARE." em caixa alta virou "Pare no gate."; o alvo divergente agora diz qual comando de leitura falta |
| `commands/plan-infra.md` | 70 | 86 | Reescrito: o corpo de uma linha virou passos com critério (entrada vazia, confirmação de alvo, `validate` sem `init`, `kubectl diff` só com contexto confirmado, não rodar `plan`), caminho do template com `${CLAUDE_PLUGIN_ROOT}` (antes relativo, não resolvia fora da raiz), campos de saída explícitos, rótulos, gate e delegação ao `rollout-planner`; `allowed-tools` ganhou só comandos de leitura de alvo |
| `agents/infra-reviewer.md` | 89 | 89 | Sem mudança |
| `agents/k8s-workload-auditor.md` | 89 | 89 | Sem mudança; comando de simulação do PSA e "audit/warn em workloads, enforce só em Pods" conferidos (V-21, V-57) |
| `agents/pipeline-security-auditor.md` | 85 | 88 | Contradição corrigida: o corpo manda citar a SLSA v1.2, mas a lista de fontes só trazia a URL retirada da v1.0. Agora cita `https://slsa.dev/spec/v1.2/build-track-basics` (conferida por WebFetch em 2026-10-10) e marca a v1.0 como retirada |
| `agents/rollout-planner.md` | 84 | 88 | O exemplo de linha da tabela "Efeito" tinha 6 colunas e o formato tinha 5; a coluna "risco e condição" foi acrescentada ao formato. O "`interval` padrão 60 s do Flagger" foi conferido (V-45, Verificado) |
| Biblioteca de prompts (amostra de 18: PR-01, 02, 03, 07, 09, 10, 11, 12, 15, 20, 21, 26, 27, 28, 29, 30, 31, 32) | 86 | 88 | PR-30 usava `[SKILL_OU_AGENTE]` sem listá-la em "Variáveis"; PR-03 citava `TP-01` (ID da síntese) como origem; PR-28 e `fontes.md` (V-59) ganharam a URL da SLSA v1.2. Os 32 prompts têm "Quando usar", "Variáveis", "Por que funciona" e "Fontes" (contagem por Grep: 22 + 10) |
| `evals/` (15 casos) | 84 | 89 | Criados `segredos-repo-historico` (secrets-review: grader regex `not_contains` para os três valores fictícios, grader llm com PASS/FAIL observáveis, `skill-fired`) e `lambda-sqs-idempotencia` (cloud-review: timeout maior que visibility timeout, cliente SDK no handler, e-mail sem idempotência, custo como Suposição). `evals/README.md` atualizado (contagem, custo, cobertura). Os dois negativos (`negativo-nao-relacionado`, `negativo-slo-alertas`) com `arm: both` estão mantidos |
| `README.md` | 88 | 88 | Sem mudança |

Média dos 19 artefatos: antes 85,6; depois 87,8.

## 3. Fidelidade técnica conferida

| Afirmação | Onde | Resultado |
| --- | --- | --- |
| SLSA v1.0 retirada, v1.2 atual | agentes, gha, prompts, fontes | **Verificado** em VALIDATED V-59 e por WebFetch em `https://slsa.dev/spec/v1.2/` ("Version 1.2", status Approved; Build track em `/spec/v1.2/build-track-basics`) |
| Flagger `interval` padrão 60 s | `rollout-planner` | Verificado (VALIDATED, correção 15 e V-45) |
| Argo CD: self-heal 5 s, uma tentativa por SHA, rollback bloqueado com auto-sync | `helm-gitops-review`, `infra-troubleshoot` | Verificado (VALIDATED, correção 1 / V-31) |
| Flux `wait: true` ignora `healthChecks`; sem default de `interval` | `helm-gitops-review` | Verificado (V-33; o conflito entre páginas foi respeitado) |
| Vercel 86/86 e zero AWS/GCP/Azure em 112 respostas | PR-31 | Verificado (V-26), com a ressalva "não é dado de mercado" já presente |
| Lambda: timeout ≤ visibility timeout; cliente fora do handler | `cloud-review`, novo eval | Verificado (V-48); a margem maior é Inferida e está marcada assim na referência |
| `claude-code-action`: `claude_args --allowedTools`, `allowed_tools` obsoleto, `anthropic_api_key` x `claude-api-key` | gha, pipeline-auditor | Verificado (V-07, V-09) |
| Busca por APIs obsoletas (`set-output`, `extensions/v1beta1`, `policy/v1beta1`, compose `version`) e SHAs ou chaves inventados | todo o plugin | Nenhuma ocorrência (Grep) |

## 4. Direitos autorais e segurança

- Literal de terceiros: nenhum trecho longo encontrado; SRE Workbook (CC BY-NC-ND) declarado como só destilação; gstack (MIT) com atribuição e redação própria; trailofbits sem LICENSE tratado como só destilação. **Inferido** a partir da leitura e dos avisos de licença nos arquivos; não houve comparação automática com as fontes.
- Segredos: os valores dos evals são fictícios ou o exemplo público da AWS; o novo eval de segredos tem grader regex que reprova a resposta se repetir qualquer valor.
- Ações destrutivas: só `deploy-infra` executa, com `disable-model-invocation: true`, gate por comando e "sim" explícito; `plan-infra` e as demais skills param no gate. `--dangerously-skip-permissions` aparece só como antipadrão rejeitado ou risco "só em sandbox e repositório confiável" (DO-AGT-07, AP-DO-14, K3).
- Revisores: os 4 agentes têm `tools: Read, Grep, Glob` (sem Write/Edit/Bash). Verificado.
- Conteúdo externo como dado: presente em todas as skills, agentes, comando e prompts. O eval `injecao-em-log-e-keyword` contém de propósito uma linha dirigida à IA. Ela foi lida como dado de teste e não foi obedecida.
- Nenhum hook ativo, `.mcp.json`, `.lsp.json` ou `bin/` (verificador PASS).

## 5. Pendências

1. **Evals não executados.** Os 15 casos seguem `designed_not_executed`; a CLI registrada na fundação (2.1.128) está abaixo do requisito do `claude plugin eval` (2.1.269). Nenhuma nota desta tabela é medição.
2. **Sem caso de eval** para o modo `DEVOPS-COMPLETO` positivo, para os 4 agentes (delegação), para `plan-infra`, para `deploy-infra` (manual) e para pilares Well-Architected, Azure Functions, Cloud Run e plataforma interna.
3. **Lacunas de fonte já declaradas** pelos construtores continuam abertas: GitLab CI, Azure Pipelines, Kustomize, FinOps Framework, Vault em profundidade, sintaxe de `cosign verify`, AnalysisTemplate do Argo Rollouts, SIGTERM no Cloud Run e MCP de infra. Os comandos de diagnóstico de `infra-troubleshoot` seguem Inferidos até haver fonte A (páginas oficiais de depuração do Kubernetes, `helm status`/`history`).
4. **Margem do visibility timeout do SQS** (múltiplo do timeout da função) está como Inferido em `cloud-review/references/serverless.md`; confirmar na página de event source mapping de SQS da AWS.
5. **Tabela de fronteiras do playbook** (25 linhas) é longa para o que agrega neste plugin. Foi mantida porque é convenção comum aos plugins do repositório; a decisão de enxugar é do mantenedor.
6. **Referências a outros plugins** (`sre-observability`, `security-appsec`, `mobile-apps`, `cli-desktop-tooling` e outros) são texto. Não foi verificado se esses plugins existem com esses nomes (Não verificável nesta execução).
7. As notas D1–D12 são autoatribuídas por modelo da mesma família (AP-16 da fundação). Recomenda-se uma leitura humana de `deploy-infra`, `plan-infra` e dos dois evals novos antes da primeira rodada.
