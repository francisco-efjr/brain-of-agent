# Template: CHANGELOG (Keep a Changelog 1.1.0)

Fonte: Keep a Changelog 1.1.0, https://keepachangelog.com/en/1.1.0/ (MIT; estrutura adaptada com redação própria), V-13; Conventional Commits 1.0.0 (CC BY 3.0) para o efeito de versão, V-14. Changelog é para **humanos**: voz ativa, uma linha por entrada, "o que muda para quem usa". Nunca regenere nem apague entradas existentes; insira com edição exata. Não altere `VERSION` nem `package.json`: a versão é recomendação que o usuário confirma. Datas em ISO 8601, versão mais nova primeiro.

````markdown
# Changelog

Todas as mudanças relevantes deste projeto são registradas aqui.
O formato segue [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) e o projeto adota [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [Unreleased]

### Added
- [Novidade para quem usa, em uma linha.]

### Changed
- [Mudança de comportamento existente.]

### Deprecated
- [O que será removido e a alternativa.]

### Removed
- **Quebra:** [o que foi removido e o que usar no lugar.]

### Fixed
- [Defeito corrigido, descrito pelo sintoma que o usuário via.]

### Security
- [Correção de vulnerabilidade, sem detalhes exploráveis antes do aviso.]

## [X.Y.Z] - AAAA-MM-DD

### Added
- [...]

[Unreleased]: [URL DE COMPARAÇÃO: versão anterior...HEAD]
[X.Y.Z]: [URL DE COMPARAÇÃO OU DA TAG]
````

## Tabela de rastreio (entregue junto, fora do arquivo)

| Entrada | Tipo | Commit ou PR | Quebra? |
| --- | --- | --- | --- |
| [TEXTO] | Added | [HASH OU #N] | não |

## Regras

- Tipos: Added, Changed, Deprecated, Removed, Fixed, Security (em português, traduza todos ou nenhum; registre a escolha).
- `fix` = PATCH, `feat` = MINOR, `!` ou `BREAKING CHANGE:` = MAJOR (proposta, não ação).
- Omita `chore`, `ci`, `test` e `docs` triviais, salvo impacto para quem usa.
- Link de PR ou issue só se vier dos dados.
