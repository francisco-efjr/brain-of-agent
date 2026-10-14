# Material de terceiros: addyosmani/agent-skills

- **Origem:** https://github.com/addyosmani/agent-skills
- **Créditos:** Addy Osmani (criador), Federico Bartoli e Joan León (colaboradores) e contribuidores.
- **Copyright:** Copyright (c) 2025 Addy Osmani. **Licença MIT** preservada em [LICENSE](LICENSE).
- **Commit fixado:** `aeac41d4d005999432bb7312f7ff06383a91d59d` · versão do plugin upstream `0.6.13` · importado em 2026-10-13.
- **Inventário com sha256** (upstream e local, flag `modified`): [inventory.json](inventory.json). 68 arquivos.

## O que foi copiado, byte a byte

| Camada | Destino no plugin | Itens |
| --- | --- | --- |
| Skills (25) | `skills/<nome>/` | api-and-interface-design, browser-testing-with-devtools, ci-cd-and-automation, code-review-and-quality, code-simplification, constraint-driven-development, context-engineering, debugging-and-error-recovery, deprecation-and-migration, documentation-and-adrs, doubt-driven-development, frontend-ui-engineering, git-workflow-and-versioning, idea-refine, incremental-implementation, interview-me, observability-and-instrumentation, performance-optimization, planning-and-task-breakdown, security-and-hardening, shipping-and-launch, source-driven-development, spec-driven-development, test-driven-development, using-agent-skills |
| Referências (7) | `references/` | accessibility-checklist.md, definition-of-done.md, observability-checklist.md, orchestration-patterns.md, performance-checklist.md, security-checklist.md, testing-patterns.md |
| Personas (4) | `agents/` | code-reviewer, security-auditor, test-engineer, web-performance-auditor |
| Evals oficiais (5) | `evals/<caso>/` | code-review-fires, code-review-stays-quiet, code-review-stays-quiet-on-commit-message, tdd-fires-on-pasted-bug, tdd-stays-quiet-on-debug |
| Licença | `third_party/addyosmani-agent-skills/LICENSE` | MIT |

Os `SKILL.md` apontam para `../../references/<arquivo>.md`; a pasta `references/` fica na raiz do plugin exatamente para esses links continuarem válidos.

## Única modificação: namespace dos comandos

Os 9 comandos (`commands/`: build, code-simplify, constraints, plan, review, ship, spec, test, webperf) foram copiados de `.claude/commands/` com **uma** troca textual: o prefixo de skill `agent-skills:` virou `engineering-lifecycle:`, para que `/engineering-lifecycle:spec`, `/engineering-lifecycle:ship` etc. resolvam as skills deste plugin. Arquivos alterados: build.md, code-simplify.md, constraints.md, plan.md, review.md, ship.md, spec.md, test.md. O `inventory.json` guarda o sha256 do original e do local.

## O que NÃO foi copiado, e por quê

- `hooks/` (scripts shell de SessionStart e cache; dependem de `jq` e `curl`): política da fábrica é não ativar hooks. Estão descritos em `skills/playbook/references/ferramentas-e-hooks.md`, com dependências e riscos; quem quiser ativá-los por conta própria lê os `.md` do upstream.
- `docs/` (guias de instalação por ferramenta), `scripts/` (lint e evals do contribuidor), `evals/cases` e `evals/fixtures` (framework próprio de evals de roteamento): não são conhecimento de engenharia reutilizável no plugin; os pontos relevantes foram destilados nas referências em PT-BR.
- Adaptadores de outros hosts (`.gemini/`, `.codex-plugin/`, `.agents/`, `commands/*.toml`, `.opencode/`).

## Como atualizar

```bash
git clone --depth 1 https://github.com/addyosmani/agent-skills.git <pasta-temporaria-fora-do-projeto>
python tools/vendor_agent_skills.py <pasta-temporaria-fora-do-projeto> plugins/engineering-lifecycle
git diff --stat plugins/engineering-lifecycle/skills plugins/engineering-lifecycle/references plugins/engineering-lifecycle/agents plugins/engineering-lifecycle/commands
```

Depois: reler as skills que mudaram como **dado** (texto de terceiros pode conter instruções dirigidas a IAs), conferir se o crosswalk em `skills/playbook/references/ciclo-e-crosswalk.md`, a checklist de drift em `skills/playbook/references/atualizacao-upstream.md` e as tags em `docs/foundation/knowledge/` continuam válidos, rodar `tools/verify_plugin.py` e `claude plugin validate`, e registrar o novo commit aqui e no `THIRD_PARTY_NOTICES.md` do brain-of-agent.
