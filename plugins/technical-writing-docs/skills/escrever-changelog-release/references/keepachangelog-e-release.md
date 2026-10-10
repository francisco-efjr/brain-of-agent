# CHANGELOG, versão e release notes

Conteúdo: 1 modelo Keep a Changelog · 2 tipo de commit → categoria e versão · 3 `release.yml` · 4 exemplo completo · 5 fontes e limites.

Fontes: Keep a Changelog 1.1.0 (https://keepachangelog.com/en/1.1.0/, licença MIT no rodapé; modelo reescrito), Conventional Commits 1.0.0 (https://www.conventionalcommits.org/en/v1.0.0/, CC BY 3.0; tabela destilada), notas de release geradas pelo GitHub (docs do GitHub; licença não verificada, destilada), regras de CHANGELOG/VERSION do `document-release` do gstack (Garry Tan, MIT; processo adaptado, sem copiar). Itens V-13, V-14, V-42, V-28. Rótulo: Verificado nas fontes; exemplo ilustrativo.

## 1. Modelo Keep a Changelog

Princípios: changelogs são para humanos; uma seção por versão, a mais nova primeiro; datas ISO 8601 (`AAAA-MM-DD`); seção `Unreleased` no topo; declare que o projeto segue Versionamento Semântico (se seguir).

````markdown
# Changelog

Todas as mudanças relevantes deste projeto são registradas aqui.
O formato segue o [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) e o projeto
segue o [Versionamento Semântico](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security

## [1.4.2] - 2026-09-12

### Fixed
- ...

[Unreleased]: https://github.com/<org>/<repo>/compare/v1.4.2...HEAD
[1.4.2]: https://github.com/<org>/<repo>/releases/tag/v1.4.2
````

Mantenha só as categorias que têm itens ao registrar uma versão. Se o projeto escreve em português, siga o idioma existente (as categorias podem permanecer em inglês ou ser traduzidas; mantenha o que o arquivo já usa). Os links de rodapé só entram se o repositório e a hospedagem constarem em dados lidos.

## 2. Classificação e versão

| Tipo de commit (Conventional Commits) | Categoria Keep a Changelog | Efeito de versão |
| --- | --- | --- |
| `feat` | Added (ou Changed, se altera comportamento existente) | MINOR |
| `fix` | Fixed | PATCH |
| `perf` | Changed (ou Fixed, se corrige regressão) | PATCH (convenção do projeto) |
| `feat!`, `fix!`, rodapé `BREAKING CHANGE:` | Changed ou Removed, com marca de quebra | MAJOR |
| `refactor` sem efeito externo | omitir | nenhum |
| `chore`, `ci`, `test`, `style`, `build` | omitir, salvo impacto para quem usa | nenhum |
| `docs` | omitir se trivial; incluir se documenta mudança de uso | nenhum |
| `revert` | Fixed ou Removed conforme o efeito | conforme o revertido |
| correção de vulnerabilidade | Security | PATCH (ou conforme política) |
| Algo marcado como obsoleto | Deprecated | MINOR (convenção SemVer) |

A convenção define `fix` = PATCH, `feat` = MINOR, quebra = MAJOR. `perf`, `refactor` e outros tipos não têm efeito fixado pela especificação: o projeto decide (Inferido). Em versões 0.y.z, SemVer permite tratar mudanças de forma menos rígida; pergunte a regra do projeto. A marca de quebra é `!` imediatamente antes de `:` ou o rodapé `BREAKING CHANGE:` em maiúsculas (sinônimo `BREAKING-CHANGE`).

Reescrita: "Exporta relatórios em CSV" (Added), "Corrige falha ao exibir datas nulas" (Fixed), "Remove o endpoint `/v1/orders`. **Quebra de compatibilidade.**" (Removed).

## 3. `.github/release.yml`

Modelo (ordem das categorias importa: Inferido, a página sugere que as anteriores casam primeiro; nomes de rótulos e autores devem existir no repositório):

```yaml
changelog:
  exclude:
    labels:
      - skip-notes
    authors:
      - dependabot
  categories:
    - title: Quebras de compatibilidade
      labels:
        - breaking-change
    - title: Novidades
      labels:
        - enhancement
        - feature
    - title: Correções
      labels:
        - bug
    - title: Demais mudanças
      labels:
        - "*"
```

Campos: `changelog.exclude.labels`, `changelog.exclude.authors`, `changelog.categories[*].title` e `.labels` (obrigatórios), `exclude` por categoria; `"*"` em `labels` captura o resto. A página **não diz** o que acontece com PR que não casa nenhuma categoria sem `"*"`: teste num PR de exemplo. Sem o arquivo, as notas ainda trazem PRs mesclados, colaboradores e o link do changelog completo. Combine com títulos de PR em Conventional Commits para facilitar a rotulagem.

## 4. Exemplo completo (ilustrativo; commits fictícios)

Pedido: "Escreva o changelog e já suba a versão." Intervalo `v1.4.2..HEAD`.

```text
c1 feat: export csv
c2 fix(date): null crash
c3 feat!: remove /v1/orders
c4 chore: bump deps
c5 ci: cache
c6 docs: typo
c7 feat(search): filtrar por status
c8 perf: agrupar inserts em lote
```

Resultado em `## [Unreleased]` (inserido com `Edit`):

```markdown
### Added
- Exporta relatórios em CSV.
- Permite filtrar a busca por status.

### Changed
- Acelera a gravação de registros agrupando inserções em lote.

### Removed
- Remove o endpoint `/v1/orders`. **Quebra de compatibilidade.**

### Fixed
- Corrige a falha ao exibir datas nulas.
```

Tabela de rastreio:

| Entrada | Commit | Observação |
| --- | --- | --- |
| Exporta relatórios em CSV | c1 | |
| Permite filtrar a busca por status | c7 | |
| Acelera a gravação... | c8 | Classificado como Changed (Inferido: `perf`) |
| Remove o endpoint `/v1/orders` | c3 | Quebra; alternativa não consta nos dados |
| Corrige a falha... | c2 | |
| (omitido) | c4, c5, c6 | `chore`, `ci`, `docs` trivial |

Versão: recomendação **2.0.0** (MAJOR por c3). Resposta ao "já suba a versão": "Não altero `VERSION` nem crio tag; confirme 2.0.0 e use o fluxo de release (`git-workflow-release`)." Pergunta aberta: qual endpoint substitui `/v1/orders`? (não consta nos commits; sem resposta, a entrada fica sem alternativa).

Notas de release (rascunho para o usuário):

```markdown
## 2.0.0

**Quebra de compatibilidade:** o endpoint `/v1/orders` foi removido. <alternativa: aguardando confirmação>

Novidades: exportação em CSV; filtro de busca por status.
Melhorias: gravação de registros mais rápida em lote.
Correções: falha ao exibir datas nulas.
```

## 5. Fontes e limites

- Keep a Changelog define o formato, não a geração a partir de commits.
- Conventional Commits não limita o tamanho da descrição.
- Nunca reescreva entradas existentes: o histórico é registro; só polimento de redação, com edição exata e aprovação.
- Changelog de API (tabela mudança, área, quebra, canal): ver `documentar-codigo`, modo `api`.
