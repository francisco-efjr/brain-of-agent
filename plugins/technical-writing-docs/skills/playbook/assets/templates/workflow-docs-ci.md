# Template: workflow de CI de documentação (privilégio mínimo)

Fontes: V-37 (Vale), V-38 (markdownlint), V-39 (lychee), V-40 (GitHub Pages). **Rótulos:** estrutura dos jobs Verificada nas fontes; `permissions` mínimas, `pull_request` em fork e fixação por SHA são práticas Inferidas (conferir o template atual do GitHub); `--offline` via `args` da lychee-action Inferido; versões exatas de `actions/checkout`, `upload-pages-artifact` e `deploy-pages` **Não verificadas**. Entregue como texto; alterar CI pede confirmação do usuário. Não executado.

```yaml
name: docs

on:
  pull_request:                 # não use pull_request_target em PR de fork
    paths: ["docs/**", "**/*.md", ".vale.ini", ".markdownlint.json"]
  push:
    branches: [main]            # troque pelo branch padrão do repositório
  schedule:
    - cron: "0 6 * * 1"         # links externos, uma vez por semana

permissions: {}                 # negar por padrão; cada job declara o que precisa

jobs:
  lint:                          # roda em PR
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@<SHA fixado>          # conferir versão atual
      - name: Vale
        uses: vale-cli/vale-action@<SHA fixado>      # v3.0.0 em 2026-08-03
        with:
          files: docs
          config: .vale.ini
          filter_mode: added
          fail_on_error: false
      - name: markdownlint
        run: "[COMANDO DO PROJETO, p. ex. o script de lint de docs com a dependência fixada]"
        # comando exato do markdownlint-cli2 em CI: Não verificado
      - name: Links locais e âncoras (offline)
        uses: lycheeverse/lychee-action@<SHA fixado> # v2.9.0 em 2026-07-09
        with:
          args: --offline --include-fragments anchor-only "docs/**/*.md" README.md
          fail: true
      - name: Build sem deploy
        run: "[COMANDO DE BUILD DO FRAMEWORK DE DOCS]"

  links-externos:                # agendado; não bloqueia PR
    if: github.event_name == 'schedule'
    runs-on: ubuntu-latest
    permissions:
      contents: read
      issues: write
    steps:
      - uses: actions/checkout@<SHA fixado>
      - id: lychee
        uses: lycheeverse/lychee-action@<SHA fixado>
        with:
          args: --cache "docs/**/*.md" README.md
          fail: false
          output: lychee/relatorio.md
      - uses: peter-evans/create-issue-from-file@<SHA fixado>   # action de terceiro: revisar antes
        if: steps.lychee.outputs.exit_code != 0
        with:
          title: Relatório de links externos quebrados
          content-filepath: lychee/relatorio.md

  deploy:                        # só no branch padrão; o deploy é pulado em PR
    if: github.event_name == 'push'
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pages: write
      id-token: write
    environment:
      name: github-pages         # ambiente protegido: só o branch padrão publica
    steps:
      - uses: actions/checkout@<SHA fixado>
      - name: Build
        run: "[COMANDO DE BUILD DO FRAMEWORK DE DOCS]"
      - uses: actions/upload-pages-artifact@<SHA fixado>   # versão: Não verificada
        with:
          path: "[PASTA DE SAÍDA DO BUILD]"
      - uses: actions/deploy-pages@<SHA fixado>            # versão: Não verificada
```

## Notas de segurança

- Fixe actions de terceiros por SHA completo com comentário da versão (o README da lychee-action recomenda). O README chama de SHA-256 um hash de 40 caracteres: é SHA-1; use o hash de commit.
- Nenhum segredo em jobs de PR de fork. Link externo nunca bloqueia PR.
- `output` e `exit_code` da lychee-action: confira os nomes de output na versão que você fixar (Não verificado).
- Pages: o ambiente `github-pages` é criado automaticamente; configure a regra de proteção para só o branch padrão publicar.
- Relate o que rodou e o que não rodou; não afirme que passou sem a saída.
