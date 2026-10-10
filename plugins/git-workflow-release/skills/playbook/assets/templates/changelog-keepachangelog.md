# Template: CHANGELOG.md no formato Keep a Changelog 1.1.0

Formato de https://keepachangelog.com/en/1.1.0/ (Olivier Lacan, MIT), esqueleto próprio. Use **ou** este formato **ou** o changelog gerado por release-please, nunca os dois no mesmo arquivo. Entradas são escritas para o usuário final, não copiadas do log de commits. Nunca reescreva entradas antigas.

```markdown
# Changelog

Todas as mudanças relevantes deste projeto são documentadas aqui.
O formato segue o Keep a Changelog e o projeto adota Versionamento Semântico.

## [Unreleased]

### Added
- 

## [1.2.0] - AAAA-MM-DD

### Added
- Exportação de relatórios em CSV pela tela de pedidos.

### Changed
- O limite padrão de requisições por chave passou de 60 para 100 por minuto.

### Deprecated
- O parâmetro `legacy_mode` será removido na 2.0.

### Removed
- 

### Fixed
- Datas nulas não derrubam mais a listagem de pedidos.

### Security
- 

[Unreleased]: https://github.com/<org>/<repo>/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/<org>/<repo>/compare/v1.1.0...v1.2.0
```

Regras: seções vazias podem ser omitidas; `Unreleased` fica no topo e é movido para uma versão na release; datas em ISO 8601; links de comparação no rodapé; quebra de contrato aparece em Changed ou Removed com instrução de migração.
