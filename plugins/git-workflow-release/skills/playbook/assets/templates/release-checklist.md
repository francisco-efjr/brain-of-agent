# Template: checklist de release manual

Use quando **não** há release-please nem changesets. Cada ação externa (push, tag, release) só com confirmação por escrito, uma de cada vez, com o comando exato mostrado antes. Rótulos: Verificado / Inferido / Suposição / Não verificável.

| Campo | Valor |
| --- | --- |
| Projeto / repositório | |
| Versão proposta | |
| Última tag | |
| Branch base | |
| Responsável | |

## Preparar

- [ ] Na base, árvore limpa, `git fetch` feito: `git status --short` vazio.
- [ ] CI verde **para o SHA** `____` (recibo: comando, resultado, hora). Sem CI: Não verificável, decisão registrada.
- [ ] Commits desde a tag: `git log <tag>..HEAD --oneline`, agrupados por tipo; commits fora do padrão listados.
- [ ] Versão pela tabela SemVer, com justificativa. Confirmação para MINOR, MAJOR e 0.y.z que quebra: ______
- [ ] Branch `release/vX.Y.Z`; CHANGELOG (entrada para o usuário, data, links) e arquivo de versão numa mudança só; commit `chore(release): vX.Y.Z`.
- [ ] PR de release aberto em rascunho; merge humano.

## Publicar (confirmar cada item)

- [ ] Base relida; SHA de release: ______
- [ ] Tag anotada `git tag -a vX.Y.Z -m "..."` (ou `-s`); `git tag -v vX.Y.Z` ok.
- [ ] Push da tag: `git push origin vX.Y.Z` (confirmado em: ______)
- [ ] GitHub Release em rascunho; **todos** os ativos anexados; notas geradas e revisadas; só então publicar (com releases imutáveis habilitadas, a release publicada trava ativos e tag).

## Verificar

- [ ] `git ls-remote --tags origin vX.Y.Z` devolve o SHA esperado.
- [ ] `gh release view vX.Y.Z` lista a release.
- [ ] Veredito: PREPARADA / MESCLADA / TAGUEADA / PUBLICADA / NÃO VERIFICADA (qual evidência falta): ______

## Fora deste plugin

Publicação em gerenciador de pacotes e deploy: `devops-cloud-infra`, `cli-desktop-tooling`.

## Rollback

Nunca mover ou recriar tag publicada. Corrigir com `vX.Y.Z+1` contendo `git revert` do problema (ver `rollback-plan.md`).
