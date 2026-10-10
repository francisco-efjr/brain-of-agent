# devops-cloud-infra — pistas do atlas global

Data: 2026-10-09 · Indexador do atlas (Claude Sonnet 5.5) · Origem: `docs/research/_global/*.validated.md` (IDs: AO, EC, CT, PC, CP, BR).
Pista é ponto de partida: reabrir a URL antes de citar. Princípios comuns: `docs/foundation/prompt-principles.md`.

## 1. Pistas aprovadas aplicáveis

| Pista | URL | Classe | O que aproveitar |
| --- | --- | --- | --- |
| GitHub Actions CI/CD best practices (CT-18) | https://github.com/github/awesome-copilot | B (7) | Pin por SHA completo; `permissions` mínimas; OIDC no lugar de credenciais longas; não imprimir segredos; cache com `hashFiles`; environments com aprovação e rollback. MIT; ~54 KB: destilar para ~30 linhas. Viés Azure. |
| Terraform instructions (CT-18) | https://github.com/github/awesome-copilot | B (6) | `sensitive = true`, módulos, `fmt`/`validate`/`tflint`/`trivy|checkov`, `.tftest.hcl`. Sem constraints de versão, lockfile ou state backend: acrescentar. |
| claude-code-action (AO-26) | https://github.com/anthropics/claude-code-action | A | Receita de prompt para CI: contexto + passos + `--allowedTools` restrito + destino do resultado; manutenção por cron com issue-resumo. MIT. |
| Hooks (AO-10) | https://code.claude.com/docs/en/hooks | A | Guardrail PreToolUse, gate Stop, contexto factual SessionStart. exit 2 bloqueia. |
| Segurança do Claude Code + auto mode (AO-23) | https://code.claude.com/docs/en/security | A | Escopo estreito, defesa em profundidade, revisor em contexto fresco. |
| Common workflows (AO-14) | https://code.claude.com/docs/en/common-workflows | A | Tarefas agendadas com critério de sucesso. |
| Blog "lessons from building Claude Code" (AO-31) | https://claude.dev/blog/lessons-from-building-claude-code-how-we-use-skills/ | A | Hooks sob demanda (`/careful`, `/freeze`); Gotchas. Verificado (2026-06-03). |
| vercel-labs/agent-skills (EC-07) | https://github.com/vercel-labs/agent-skills | A- | Formato de regras; relevância para deploy a confirmar. |
| wshobson/agents (EC-10) | https://github.com/wshobson/agents | B | Plugins `kubernetes-operations`, `cicd-automation`, `incident-response`: nomes citados; abrir. |
| Trail of Bits claude-code-config (EC-12) | https://github.com/trailofbits/claude-code-config | B | Sandbox, deny rules para credenciais, hooks que bloqueiam `rm -rf` e push na main, `.mcp.json` de projeto desativado. Sem licença declarada: destilar. |
| Hooks como guardrails (CP-19) | https://aitmpl.com/blog/secure-git-workflow/ | B | `terraform apply`, `kubectl delete`, migrate em prod bloqueados por `exit 2`; reescrever em stdlib, não rodar `npx`. |
| Power user tips (CP-14) | https://support.claude.com/en/articles/14554000-claude-code-power-user-tips | A | Mapa evento → uso; worktrees; PostCompact reinjeta regras. |
| How Anthropic teams use Claude Code (CP-15) | https://claude.com/blog/how-anthropic-teams-use-claude-code | B | Terraform plan explicado para aprovação. Não reverificado; de 2025-07-24. |
| Ronacher (CP-12) | https://lucumr.pocoo.org/2025/6/12/agentic-coding/ | B | Ferramentas idempotentes com pidfile e logs fixos. Docker com skip-permissions contraria a casa. |
| Amplifying (CP-24) | https://amplifying.ai/research/claude-code-picks | B | Railway 82% em Python: preferência do modelo, muda por versão. |
| GPT-5 guide: limiares de confirmação (PC-02) | https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide | A | Confirmar por risco. Arquivado. |
| Willison, lethal trifecta (PC-21) | https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ | A | Agentes com credenciais cloud: cuidado com a combinação de dados + conteúdo não confiável + saída. |
| ykdojo tips (CP-18) | https://github.com/ykdojo/claude-code-tips | B | Ambientes isolados para tarefas arriscadas. Licença NOASSERTION. |
| gstack `/guard`, `/land-and-deploy` (BR-19, BR-22) | https://github.com/garrytan/gstack | B | Pausar antes de destrutivo; "never force-push". |

## 2. Repositórios e arquivos a abrir
- `github/awesome-copilot/instructions/github-actions-ci-cd-best-practices.instructions.md`, `terraform.instructions.md`.
- `anthropics/claude-code-action` (exemplos de workflows).
- `trailofbits/claude-code-config` (settings, hooks, `.mcp.json`).
- `wshobson/agents/plugins/kubernetes-operations`, `cicd-automation`.
- Documentação de Docker, Kubernetes, Terraform/OpenTofu, AWS/GCP/Azure, Argo/Flux, FinOps não está no atlas: lente authoritative. Dockerfile best practices: sem pista aprovada.

## 3. Materiais oficiais Anthropic pertinentes
AO-10, AO-14, AO-23, AO-26, AO-31 (compilador C: saída de teste desenhada para o modelo), AO-12.

## 4. Padrões da comunidade
- Leitura livre, escrita confirmada; produção jamais conectada ao agente (CP-15, CP-22).
- Hooks de negação como exemplo documentado (CP-19).
- Pin por SHA, permissões mínimas, OIDC (CT-18).
- Worktrees por sessão e provar comportamento por diff main vs branch (CP-14).
- Plano de infra explicado para aprovação antes de aplicar (CP-15).

## 5. O que o brain-of-agent já oferece
- `brains/fullstack/references/entrega-e-operacao.md`, `brains/qa/references/dados-ambientes-ci.md`, `vendor/gstack/setup-deploy/SKILL.md`, `vendor/gstack/land-and-deploy/SKILL.md`.
- BR-19: sem alegação de conclusão sem evidência fresca; skills de push/deploy com `disable-model-invocation: true`.
- BR-22: `/careful`, `/guard`, `/freeze`; hook só como exemplo desativado.
- BR-03: modo `DEVOPS-COMPLETO`.

## 6. Lacunas e cuidados
- Sem fonte aprovada para Kubernetes/Helm, Docker, GitOps, blue-green/canary, FinOps, gestão de segredos além de GH Actions.
- Plugins não trazem hooks ativos nem `.mcp.json` ativo (regra 7 da casa).
- Nunca executar `terraform apply`, `kubectl` ou deploy sem autorização concreta.
