# Template: `.vale.ini` e job de Vale em PR

Fonte: Vale (MIT, v3.24.0 em 2026-10-01) e `vale-cli/vale-action` (MIT, v3.0.0 em 2026-08-03), V-37. Entregue como texto; alterar CI do repositório pede confirmação do usuário. Estilos baixados por `vale sync` têm licenças próprias. Estilos em inglês (Google, Microsoft) geram ruído em português: ajuste (Suposição).

## `.vale.ini`

```ini
StylesPath = styles
MinAlertLevel = warning
Packages = Google
Vocab = Projeto

[*.md]
BasedOnStyles = Vale, Google
```

- Vocabulário do projeto em `styles/config/vocabularies/Projeto/accept.txt` (um termo por linha) em vez de desligar regras (estrutura de pastas do Vale: confirme na documentação da sua versão).
- Uma seção posterior que casa **substitui** `BasedOnStyles`, não soma: repita os estilos desejados.
- Tipos de regra para estilo próprio: existence, substitution, occurrence, repetition, consistency, conditional, capitalization, metric, readability, spelling, sequence, script.

Regra de exemplo (palavras de enchimento; `styles/Projeto/Enchimento.yml`):

```yaml
extends: existence
message: "Evite '%s' em passos e referência."
level: warning
ignorecase: true
tokens:
  - simplesmente
  - basta
  - seamless
  - robust
```

## Job de PR

```yaml
# .github/workflows/docs-vale.yml  (fragmento: veja workflow-docs-ci.md para o conjunto)
name: docs-vale
on:
  pull_request:
    paths: ["docs/**", "**/*.md", ".vale.ini"]
permissions:
  contents: read        # permissões extras dependem do reporter escolhido: confira o README da action
jobs:
  vale:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<SHA fixado>   # conferir versão atual
      - uses: vale-cli/vale-action@<SHA fixado>   # v3.0.0 em 2026-08-03; fixar por SHA
        with:
          files: docs
          config: .vale.ini
          filter_mode: added        # só acusa linhas novas
          fail_on_error: false      # troque para true depois de limpar o histórico
```

Inputs verificados da action: `files` (padrão `all`), `reporter` (`github-pr-check`, `github-pr-review`, `github-check`), `fail_on_error` (padrão `false`), `config`, `filter_mode` (padrão `added`), `version` (padrão `latest`, mínimo 2.16.0). O repositório mudou de `errata-ai/vale-action` para `vale-cli/vale-action`.

Não executado: nenhum destes arquivos foi rodado.
