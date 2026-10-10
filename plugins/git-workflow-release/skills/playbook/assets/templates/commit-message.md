# Template: mensagem de commit

Formato Conventional Commits 1.0.0 (https://www.conventionalcommits.org/en/v1.0.0/, CC BY 3.0; adaptado). Use este formato só se o repositório já o adota ou o time decidiu adotá-lo; um estilo por repositório.

```text
tipo(escopo)!: descrição no imperativo, até 72 caracteres, sem ponto final

Corpo (opcional): o que mudou e por quê. O diff já mostra o como.
Explique o problema, a abordagem e limitações conhecidas.

BREAKING CHANGE: impacto para quem consome a API ou a CLI e como migrar
Refs: #123
Release-As: 2.0.0
```

## Tipos

| Tipo | Uso | Efeito de versão (SemVer / release-please) |
| --- | --- | --- |
| `feat` | Funcionalidade nova | MINOR |
| `fix` | Correção | PATCH |
| `docs`, `test`, `ci`, `build`, `chore` | Sem mudança de comportamento do produto | Sem release |
| `refactor`, `perf` | Reestruturação, desempenho | Conforme a política do projeto |
| `revert` | Reversão | Conforme o commit revertido |
| `tipo!` ou rodapé `BREAKING CHANGE:` | Quebra de contrato | MAJOR |

A especificação só exige `feat` e `fix`; o conjunto completo é decisão do projeto. `BREAKING CHANGE` em maiúsculas. `Release-As: x.y.z` vai no **corpo** do commit (release-please) e força a versão.

## Bons e ruins

| Ruim | Bom |
| --- | --- |
| `Fix bug` | `fix(cart): keep discount when item quantity changes` |
| `feat: Added new feature for users.` | `feat(auth): add passwordless login by email link` |
| `update stuff` | `refactor(billing): extract tax calculation into pure function` |
| `fix: remove /v1/orders` | `feat(api)!: remove /v1/orders` com `BREAKING CHANGE: use /v2/orders` |

## Regras

- Monorepo: escopo ou prefixo é o pacote (`api: add rate limiting`).
- Sem `--amend` e sem `--no-verify`. Hook falhou: corrija a causa e faça commit novo.
- Um assunto por commit; teste junto do código; cada commit funciona sozinho.
