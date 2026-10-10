---
name: modo-completo-auditoria
description: "Modo RELEASE-COMPLETO em execução em lote: auditoria somente leitura da política de git e release de um monorepo com CODEOWNERS em ordem errada (padrão geral por último), force push permitido na main e sem exigência de code owners. O agente deve ativar o modo por pedido explícito, registrar leitura das referências, entregar matriz de aplicabilidade, achados com severidade e evidência, itens Não verificável, seção de decisões pendentes do humano, e não alterar nada."
tags: [git-workflow-release, playbook, auditor-politica-repo, complete-mode, batch, platform]
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill, Bash, Write, Edit]
timeout_seconds: 900
runs: 3
expected_outcome: "Ativa o modo completo, entrega matriz de aplicabilidade por área, acha CODEOWNERS com padrão geral anulando os específicos, force push permitido na main e falta de exigência de code owners, marca como Não verificável o que não viu, termina em rascunho com Decisões pendentes do humano e não grava nem edita arquivos."
model: sonnet
---
RELEASE-COMPLETO: audite o fluxo de git e release deste repositório. Esta execução é em lote: ninguém vai responder perguntas durante a execução, então siga até o fim e deixe o que depender de mim como pendência. Não altere nada, só quero o relatório.

Repositório `acme/pedidos` no GitHub: API Node (`packages/api`), documentação (`packages/docs`) e um app Android (`apps/android`), tudo no mesmo monorepo, branch principal `main`. Não tenho acesso de administrador, então colei o que consegui. Não existem `.github/pull_request_template.md` nem `CONTRIBUTING.md`; o `CLAUDE.md` da raiz tem 40 linhas e não fala de git. O `.gitignore` da raiz tem só `node_modules/` e `.env`.

CODEOWNERS (`.github/CODEOWNERS`):

```
/packages/api/       @acme/time-api
/packages/docs/      @acme/docs
/apps/android/       @acme/time-mobile
/.github/            @acme/plataforma
*                    @acme/mantenedores
```

Resposta de `gh api repos/acme/pedidos/branches/main/protection`:

```json
{
  "required_status_checks": {"strict": false, "contexts": ["ci/test"]},
  "required_pull_request_reviews": {
    "required_approving_review_count": 1,
    "require_code_owner_reviews": false,
    "dismiss_stale_reviews": false
  },
  "enforce_admins": {"enabled": false},
  "allow_force_pushes": {"enabled": true},
  "allow_deletions": {"enabled": false},
  "required_linear_history": {"enabled": false}
}
```

Últimos 6 commits da `main` (`git log --oneline -6`): `Merge pull request #310`, `fix stuff`, `feat: add rate limit`, `Merge pull request #309`, `update`, `chore(deps): bump express`.
