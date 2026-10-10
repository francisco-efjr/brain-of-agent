# Template: `.github/release.yml` e notas de GitHub Release

Fonte: documentação do GitHub sobre releases e notas geradas automaticamente (V-34), redação própria. Com a opção "releases imutáveis" habilitada no repositório ou na organização, a release publicada trava ativos e tag (título e notas continuam editáveis); sem a opção, o mesmo cuidado vale como boa prática: crie em rascunho, anexe todos os ativos, gere e revise as notas, só então publique.

## `.github/release.yml`

```yaml
changelog:
  exclude:
    labels:
      - dependencies
      - skip-changelog
    authors:
      - dependabot[bot]
  categories:
    - title: Mudanças incompatíveis
      labels:
        - breaking-change
    - title: Novidades
      labels:
        - enhancement
        - feature
    - title: Correções
      labels:
        - bug
    - title: Documentação
      labels:
        - documentation
    - title: Outras mudanças
      labels:
        - "*"
```

Os rótulos devem existir no repositório. `*` é o coringa. Confira a sintaxe vigente na documentação antes de adotar.

## Modelo de notas (revise o texto gerado antes de publicar)

```markdown
## Destaques
- 

## Mudanças incompatíveis e migração
- (o que muda, para quem, como migrar)

## Correções
- 

## Agradecimentos
- @usuario

**Comparação completa:** https://github.com/<org>/<repo>/compare/vX.Y.Z-1...vX.Y.Z
```

Checklist: [ ] rascunho criado a partir da tag existente; [ ] todos os ativos anexados; [ ] notas geradas (`--generate-notes` ou botão "Generate release notes") e revisadas; [ ] pré-release marcada se for `-rc.N`; [ ] publicar só após confirmação.
