# Template: `.github/release.yml` (notas de release geradas pelo GitHub)

Fonte: documentação do GitHub sobre notas de release geradas (V-42), https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes. Campos verificados: `changelog.exclude.labels`, `changelog.exclude.authors`, `changelog.categories[*].title` e `.labels` (obrigatórios), `exclude` por categoria, `"*"` como categoria de captura. Alterar este arquivo muda a configuração do repositório: só com pedido explícito do usuário. As notas geradas são **rascunho**: revise antes de publicar e escreva o texto voltado ao usuário a partir de "o que muda para quem usa".

```yaml
# .github/release.yml
changelog:
  exclude:
    labels:
      - skip-notes
    authors:
      - dependabot   # confira o nome exato do autor de bot nos PRs do repositório (Inferido)
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

## Avisos

- A ordem das categorias importa (Inferido: as anteriores casam primeiro). Coloque "Quebras de compatibilidade" no topo.
- **Não está documentado o que acontece com um PR que não casa nenhuma categoria quando não há `*`.** Teste num repositório de exemplo antes de depender disso.
- Os nomes dos rótulos (`breaking-change`, `enhancement`, `feature`, `bug`, `skip-notes`) devem existir no repositório; ajuste ao padrão do projeto.
- Combine com títulos de PR no padrão Conventional Commits (V-14) e com o CHANGELOG (Keep a Changelog, V-13).
- Corte de versão, tag e publicação são do plugin `git-workflow-release`.
