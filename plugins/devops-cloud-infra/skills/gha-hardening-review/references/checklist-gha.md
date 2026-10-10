# Checklist de hardening de workflows do GitHub Actions (GH-nn)

Base: guia oficial "Security hardening for GitHub Actions" (V-01, classe A), `docs/security.md` do claude-code-action (V-08) e o brain `dados-ambientes-ci` (gates honestos). Destilação com redação própria; conferido em 2026-10-10. Rótulo "Inferido" marca o que vem de conhecimento estável do domínio e não de V.

## Sumário

- [Itens GH-01 a GH-13](#itens)
- [Contextos controlados por terceiros](#contextos-controlados-por-terceiros)
- [Exemplo anotado](#exemplo-anotado)
- [Como obter um SHA sem inventar](#como-obter-um-sha)

## Itens

| ID | Verificar | Detectar | Sev. | Fonte |
| --- | --- | --- | --- | --- |
| GH-01 | toda action de terceiros fixada por SHA completo de 40 caracteres, com a versão em comentário (`# v4.2.2`); tag e branch são mutáveis, só o SHA é release imutável | `uses:` sem `@[0-9a-f]{40}` | Alto; Crítico se o job recebe segredo | V-01 |
| GH-02 | `permissions:` no topo com `contents: read`; elevação por job (`pull-requests: write`, `id-token: write`) só onde precisa | ausência de `permissions`; `write-all` | Alto | V-01 |
| GH-03 | nenhum campo controlado por usuário direto em `run:`; passar por `env:` e referenciar como variável do shell | Grep em `\$\{\{\s*(github\.event\.|github\.head_ref|inputs\.)` e leitura do contexto | Crítico | V-01 |
| GH-04 | `pull_request_target` e `workflow_run` só quando necessário e **sem** checkout do head do PR na raiz (rodam com segredos e token da base) | `pull_request_target`, `workflow_run` + `ref:` apontando para o PR | Crítico | V-01, V-08, brain |
| GH-05 | OIDC no lugar de chave longa de nuvem (`id-token: write` + role com condição de repositório/branch) | `AWS_SECRET_ACCESS_KEY`, `credentials_json` | Alto | V-01 |
| GH-06 | produção em `environment` com revisores obrigatórios e restrição de branch; segredos de produção só ali | `environment:` ausente no job de deploy | Alto; a configuração em si é Não verificável pelo YAML | V-01 |
| GH-07 | segredo só no step que precisa; nunca em `echo`, em `with:` de action sem pin ou em job que executa código do PR | `secrets\.` no escopo de `env:` do job | Alto | V-01 |
| GH-08 | cache por `hashFiles(lockfile)` com `restore-keys`; nunca `github.run_id` na chave primária | `key:` com `run_id` | Médio | V-01, K15 |
| GH-09 | `timeout-minutes` em todo job; `concurrency` por ref para CI e `cancel-in-progress: false` para deploy | ausência | Médio | V-01, brain |
| GH-10 | CODEOWNERS cobrindo `.github/workflows/`; Dependabot para o ecossistema `github-actions` | `.github/CODEOWNERS`, `.github/dependabot.yml` | Médio | V-01 |
| GH-11 | runners self-hosted quase nunca em repositório público; preferir efêmeros | `runs-on: self-hosted` | Alto em repositório público | V-01 |
| GH-12 | gates verdadeiros: sem `\|\| true` e `continue-on-error` em testes; "zero testes coletados", shard ausente e job cancelado não contam como verde | Grep `\|\| true`, `continue-on-error` | Alto | brain `dados-ambientes-ci` |
| GH-13 | promover o artefato testado (mesmo digest) em vez de recompilar; cache não é prova de integridade | job de deploy com novo `build` | Médio | brain |
| GH-14 | uso de `claude-code-action`: ver [agente-em-ci.md](agente-em-ci.md) | `anthropics/claude-code-action` | Alto se amplo | V-07, V-08 |

Fora do YAML (Não verificável sem acesso ao repositório): regras de proteção de branch, revisores do environment, política de aprovação de PR de fork, segredos configurados, permissões padrão do token em Settings.

## Contextos controlados por terceiros

Fonte V-01 cita título de PR, corpo de issue e nome de branch. Como lista de busca, acrescente (Inferido, conhecimento estável): `github.event.comment.body`, `github.event.pull_request.body`, `github.event.pull_request.head.ref`, `github.event.head_commit.message`, `github.head_ref` e `inputs.*` de `workflow_dispatch`.

Onde a expressão aparece decide o risco:

- `run:` e `script:` de `actions/github-script`: o valor é colado no código antes da execução. **Injetável.**
- `env:`: o valor chega como variável de ambiente; o shell não o interpreta como código se você a usar entre aspas (`"$PR_TITLE"`). Seguro como padrão.
- `if:` e `with:` de action confiável: em geral sem execução de shell; confira o que a action faz com o valor.

## Exemplo anotado

Entrada (`.github/workflows/pr.yml`, didático):

```yaml
name: ci
on:
  pull_request_target:
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.head.sha }}
      - run: echo "PR: ${{ github.event.pull_request.title }}"
      - run: npm ci && npm test
        env:
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
      - uses: some-org/deploy-action@main
        with:
          key: ${{ secrets.DEPLOY_KEY }}
```

| ID | Sev. | Linha | Evidência | Correção | Rótulo |
| --- | --- | --- | --- | --- | --- |
| GH-04 | Crítico | 3, 9-10 | `pull_request_target` com checkout do head do PR: código do PR roda com segredos e token da base | usar `pull_request`; se imprescindível, checkout em subdiretório e sem segredos no job que executa o código | Verificado |
| GH-03 | Crítico | 11 | título do PR dentro de `run:` | `env: PR_TITLE: ${{ ... }}` e `echo "PR: $PR_TITLE"` | Verificado |
| GH-07 | Crítico | 12-14 | `NPM_TOKEN` exposto a `npm test` do código do PR | remover; testes de PR rodam sem segredo | Verificado |
| GH-01 | Alto | 8, 15 | `@v4` e `@main` (mutáveis); a segunda recebe `DEPLOY_KEY` | SHA completo; deploy em workflow separado em `push` na branch principal | Verificado |
| GH-02 | Alto | (ausente) | sem `permissions` | `permissions: contents: read` no topo | Verificado; padrão do repositório: Não verificável |
| GH-09 | Médio | (ausente) | sem `timeout-minutes` nem `concurrency` | acrescentar | Verificado |

Versão corrigida (SHAs são entradas: veja a próxima seção; a ordem das etapas de deploy fica fora deste workflow):

```yaml
name: ci
on:
  pull_request:
permissions:
  contents: read
concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true
jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@<sha-de-40-caracteres> # v4.x.y
      - env:
          PR_TITLE: ${{ github.event.pull_request.title }}
        run: echo "PR: $PR_TITLE"
      - run: npm ci && npm test
```

## Como obter um SHA

Não invente SHA. Para uma tag de action: `git ls-remote https://github.com/<dono>/<repo> "refs/tags/<tag>*"`. Em tag anotada, use a linha com sufixo `^{}` (commit desreferenciado); em tag leve só há uma linha. Confirme na página da release e escreva a versão no comentário para o Dependabot e para humanos (Inferido: conhecimento de Git; V-01 só estabelece o SHA como forma imutável).

Dependabot para actions:

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

CODEOWNERS: `/.github/workflows/ @sua-org/plataforma` (substitua pelo time real).
