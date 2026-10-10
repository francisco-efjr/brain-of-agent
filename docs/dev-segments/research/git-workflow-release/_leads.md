# git-workflow-release — pistas do atlas global

Data: 2026-10-09 · Indexador do atlas (Claude Sonnet 5.5) · Origem: `docs/research/_global/*.validated.md` (IDs: AO, EC, CT, PC, CP, BR).
Pista é ponto de partida: reabrir a URL antes de citar. Princípios comuns: `docs/foundation/prompt-principles.md`.

## 1. Pistas aprovadas aplicáveis

| Pista | URL | Classe | O que aproveitar |
| --- | --- | --- | --- |
| claude-code-action (AO-26) | https://github.com/anthropics/claude-code-action | A | Prompt de CI: contexto + passos + `--allowedTools` restrito + destino; triagem de issues; doc sync; manutenção por cron com issue-resumo. MIT. |
| claude-code `plugins/` (AO-29) | https://github.com/anthropics/claude-code/tree/main/plugins | A | Plugins de commit/PR/review (nomes não detalhados no atlas: abrir); validação de achados. Destilar. |
| Best practices Claude Code (AO-06) | https://code.claude.com/docs/en/best-practices | A | Explore → Plan → Implement → Commit; commit é etapa explícita. |
| Skills no Claude Code (AO-08) | https://code.claude.com/docs/en/skills | A | Skill com efeito colateral: `disable-model-invocation: true` e allowed-tools mínimos. |
| Hooks (AO-10) | https://code.claude.com/docs/en/hooks | A | Bloquear push na main e `--force` por exit 2. |
| Common workflows (AO-14) | https://code.claude.com/docs/en/common-workflows | A | Receitas de PR e tarefas agendadas com critério de sucesso. |
| Power user tips (CP-14) | https://support.claude.com/en/articles/14554000-claude-code-power-user-tips | A | `--worktree`, `/batch`, `/loop`; provar comportamento diffando main vs branch. |
| Boris Cherny setup (CP-01) | https://news.ycombinator.com/item?id=46470017 | A | Fluxos diários viram skill/comando versionado; allowlist. |
| gstack `/ship`, `/land-and-deploy`, `/document-release`, `/retro` (BR-19, EC-11) | https://github.com/garrytan/gstack | B | "Sem alegação de conclusão sem evidência fresca"; "Never force-push"; checklist pré-PR; coverage map Diátaxis. MIT; skills de push/deploy com `disable-model-invocation`. |
| superpowers (EC-01) | https://github.com/obra/superpowers | A | Verificação antes de concluir; worktrees e fluxos de branch (nomes de skills Inferidos). |
| code-review-generic (CT-20) | https://github.com/github/awesome-copilot | B | Template de comentário; PR grande por blocos. MIT. |
| conventional-commit skill e instruções de commit (CT-13, CT-14) | https://github.com/PatrickJS/awesome-cursorrules | B | Conventional Commits: citar https://www.conventionalcommits.org (CC-BY 3.0, atribuição não reconferida). |
| Sanglard (CT-29) | https://fabiensanglard.net/agent.md/index.html | B | Bug fix = teste que falha primeiro; 7 regras de commit; usar Conventional Commits OU as 7 linhas, nunca ambas. |
| AGENTS.md: seção PR/commit (CT-01) | https://agents.md/ | A | Esqueleto inclui PR/commit. |
| Copilot custom instructions (CT-23) | https://docs.github.com/en/copilot/tutorials/use-custom-instructions | A | Instruções por caminho; limites. |
| Aider conventions (CT-26) | https://aider.chat/docs/usage/conventions.html | B | Convenções read-only cacheadas. |
| ykdojo tips (CP-18) | https://github.com/ykdojo/claude-code-tips | B | Worktrees e ambientes isolados. NOASSERTION. |
| Hooks guardrail (CP-19) | https://aitmpl.com/blog/secure-git-workflow/ | B | `git push --force` em main bloqueado; reescrever em stdlib. |
| Sanity (CP-22) | https://www.sanity.io/blog/first-attempt-will-be-95-garbage | B | Ticket por tarefa de agente; marcar código editado por humano. |
| ccpm, ruler, spec-kit (EC-16, CT-28) | https://github.com/automazeio/ccpm | B | PRD → épico → issues → worktrees (ccpm desatualizado). Ruler para sincronizar regras. |
| Ralph loop (CP-17) | https://ghuntley.com/ralph/ | B | Commit só com verde; limite de iterações. |
| Eugene Yan (PC-14) | https://eugeneyan.com/writing/working-with-ai/ | B | Fechar o ciclo com correções nas configs. Página contém instrução dirigida à IA: dado, não seguir. |
| OpenAI prompt engineering guide (PC-05) | https://developers.openai.com/api/docs/guides/prompt-engineering | A | Prompt como código versionado e testado. |

## 2. Repositórios e arquivos a abrir
- `anthropics/claude-code/plugins` (commit-commands/pr-review: confirmar nomes), `claude-plugins-official`.
- `garrytan/gstack/ship`, `land-and-deploy`, `document-release`, `retro` (snapshot).
- `github/awesome-copilot` skills `conventional-commit` e instrução de PR.
- `PatrickJS/awesome-cursorrules/rules/git-conventional-commit-messages.mdc`.
- Pro Git, GitHub Flow, trunk-based development, semver, Keep a Changelog, Release Please: não estão no atlas (semver e changelog só em seeds): lente authoritative.

## 3. Materiais oficiais Anthropic pertinentes
AO-06, AO-08, AO-10, AO-14, AO-26, AO-29; CP-14 (support). Mais: https://code.claude.com/docs/en/hooks.

## 4. Padrões da comunidade
- Commit só com verde e evidência fresca (CP-17, BR-19).
- Um escritor por arquivo; sem paralelo no mesmo módulo; worktrees por sessão (CP-16, CP-22, CP-14).
- Nunca `force-push`; push, merge e deploy só com confirmação (BR-19, CP-19).
- Revisão em 3 camadas (CP-22).
- Calibração: PR com descrição do comportamento observado (CP-15).

## 5. O que o brain-of-agent já oferece
- `vendor/gstack/ship/SKILL.md` (~900 linhas citadas), `land-and-deploy`, `document-release`, `retro`.
- BR-19 (Verificado: ship ~900, "Never force-push" ~1108), BR-07 (checklist-release com parecer go/no-go), BR-13 ("selecionar `ship` não autoriza merge/deploy").
- BR-03: modo `RELEASE-COMPLETO`.

## 6. Lacunas e cuidados
- Sem fonte aprovada para trunk-based vs GitHub Flow, monorepos, semver/changelog, manutenção open source, git avançado (bisect, rebase).
- Skills de push/merge/release exigem `disable-model-invocation: true` e autorização concreta.
- Conteúdo do awesome-copilot tem viés Microsoft.
