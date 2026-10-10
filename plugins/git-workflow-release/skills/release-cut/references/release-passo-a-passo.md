# Release passo a passo (release-cut)

Sumário: 1 Tabela de versão com casos · 2 API pública · 3 Changelog (Keep a Changelog) · 4 Notas e `release.yml` · 5 Tag · 6 Com release-please · 7 Com Changesets · 8 Go/no-go resumido · 9 Fontes.

Conferido em 2026-10-10. Texto destilado com redação própria de SemVer 2.0.0 (CC BY 3.0, V-31), Keep a Changelog 1.1.0 (MIT, V-32), release-please (Apache-2.0, V-33), docs do GitHub (V-34) e manual do Git (V-25). Exemplos fictícios.

## 1. Tabela de versão com casos

| O que mudou desde a última tag | Versão | Justificativa |
| --- | --- | --- |
| Só `fix` e `docs` | PATCH (1.4.2 para 1.4.3) | Correções compatíveis |
| `feat` e `fix` | MINOR (1.4.2 para 1.5.0) | Funcionalidade compatível nova |
| Qualquer `feat!` ou `BREAKING CHANGE:` | MAJOR (1.4.2 para 2.0.0) | Quebra a API pública |
| Funcionalidade marcada como obsoleta, sem remover | MINOR | SemVer: depreciar é mudança compatível que pede aviso |
| Remoção de algo antes depreciado | MAJOR | Remoção quebra consumidor que ainda usava |
| Só `refactor`, `test`, `chore`, `ci`, `build` | Sem release, ou PATCH se afeta o artefato publicado | Sem mudança de contrato |
| 0.y.z com mudança que quebra | Em geral sobe o MINOR (0.3.1 para 0.4.0) | SemVer diz que em 0.y.z qualquer coisa pode mudar; subir o MINOR é convenção comum, não regra. Confirme com a pessoa e com a ferramenta de release |
| Candidata | `2.0.0-rc.1`, depois `-rc.2`, depois `2.0.0` | Pré-lançamento tem precedência menor que a versão final; `+build` não conta |
| Decidir 1.0.0 | Só com confirmação | 1.0.0 declara a API pública e o compromisso de compatibilidade |

Caso E6 (para treino): desde `v1.4.2` há `feat: add export`, `fix: null date`, `feat!: remove /v1/orders`, `docs: ...`. A quebra decide: **2.0.0**, não 1.5.0. Peça confirmação de MAJOR. Contagem de linhas nunca entra na decisão.

Atenção: o rótulo do commit pode estar errado. Um `fix` que muda o formato de resposta quebra consumidor; um `feat!` que só mexe em API interna não quebra. Confira o diff dos arquivos da API pública antes de confirmar a classe.

## 2. Definir a API pública

SemVer só funciona se a API pública é declarada. Procure em README, docs e arquivos de exportação (`exports` do `package.json`, `__all__`, rotas OpenAPI, flags da CLI, formato de arquivo). Sem declaração: pergunte e registre a resposta no relatório (Suposição até a pessoa confirmar). Itens típicos: funções e classes exportadas, rotas e payloads, flags e códigos de saída da CLI, esquema de configuração, formato de dados em disco.

## 3. Changelog (Keep a Changelog)

Princípio (V-32): changelog é para pessoas, não um despejo do `git log`. Estrutura: `Unreleased` no topo; cada versão com data; seções Added, Changed, Deprecated, Removed, Fixed, Security; declaração de que o projeto segue SemVer; links de comparação no rodapé.

```markdown
# Changelog

Todas as mudanças relevantes deste projeto ficam aqui. O formato segue
[Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) e o projeto
adota o [Versionamento Semântico](https://semver.org/).

## [Unreleased]

## [2.0.0] - 2026-10-10

### Removed
- Endpoint `/v1/orders`. Use `/v2/orders`; os preços agora são inteiros em centavos.

### Added
- Exportação de pedidos em CSV na tela de listagem.

### Fixed
- Datas nulas não derrubam mais a geração de relatórios.

[Unreleased]: https://github.com/<dono>/<repo>/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/<dono>/<repo>/compare/v1.4.2...v2.0.0
```

Regras de redação:
- Escreva o efeito para o usuário ("Datas nulas não derrubam mais..."), não o ato do desenvolvedor ("corrige null em date.ts").
- Toda quebra aparece em Removed ou Changed com o caminho de migração em uma linha.
- Uma linha por mudança relevante; refatoração interna, CI e testes não entram.
- Links de comparação saem de `git remote get-url origin` (confirme dono e repositório); a data é a da release; a ordem é a mais recente primeiro.
- Edite com correspondência exata e não reescreva entradas antigas (processo do `document-release`, gstack, MIT).
- Com release-please o arquivo é gerado e o formato é outro; não misture (V-32 ressalva, V-33).

## 4. Notas da GitHub Release e `.github/release.yml`

Notas geradas (`--generate-notes`) servem de rascunho; revise: destaques (o que o usuário ganha), quebras e migração, agradecimentos. `.github/release.yml` controla as categorias das notas geradas (V-34). Os nomes de label abaixo são exemplos: use os do repositório.

```yaml
changelog:
  exclude:
    labels:
      - ignore-for-release
    authors:
      - dependabot
  categories:
    - title: Mudanças que quebram
      labels:
        - breaking-change
    - title: Novidades
      labels:
        - enhancement
    - title: Correções
      labels:
        - bug
    - title: Outras mudanças
      labels:
        - "*"
```

Ordem segura (V-34): criar como rascunho; anexar todos os ativos (binários, checksums, SBOM se houver); gerar e revisar notas; só então publicar. Depois de publicada, ativos e tag não mudam; título e notas continuam editáveis.

## 5. Tag

```bash
git tag -a v2.0.0 -m "v2.0.0" <sha-de-release>     # anotada
git tag -s v2.0.0 -m "v2.0.0" <sha-de-release>     # assinada (exige chave configurada)
git cat-file -t v2.0.0                             # "tag" = anotada; "commit" = leve (errado para release)
git tag -v v2.0.0                                  # verifica assinatura (só tags assinadas)
git push origin v2.0.0                             # só essa tag; confirmação
git ls-remote --tags origin v2.0.0                 # duas linhas: objeto da tag e v2.0.0^{} -> commit de release
```

Nunca mova a tag depois de publicada; o Git não muda tags "pelas costas" dos usuários e o manual manda usar outro nome (V-25). Use `git push origin <tag>` e não `git push --tags`.

## 6. Com release-please

O que a skill confere no PR de release (V-33):
- A versão proposta bate com a sua leitura dos commits (quebra gera MAJOR). Se não bate, o motivo costuma ser commit fora do padrão (invisível) ou `!` esquecido.
- O CHANGELOG gerado cita as mudanças esperadas; commits fora do padrão não aparecem e podem merecer um commit corretivo com `Release-As: x.y.z` **no corpo**.
- CI do PR de release verde para o SHA do PR.
- Política de merge: squash é a recomendação do projeto (o título do PR vira o commit que o release-please lê).
- Depois do merge do PR de release, tag e GitHub Release nascem pela ação (`googleapis/release-please-action`); verifique com `git ls-remote --tags` e `gh release view`. O rótulo `autorelease: published` não é aplicado automaticamente.
- O release-please não publica em gerenciadores de pacote.

Configuração de monorepo (modo manifesto) e conteúdo da ação não foram lidos (lacuna): não escreva YAML a partir de memória; leia `docs/manifest-releaser.md` do repositório do projeto antes.

## 7. Com Changesets

Cada PR que altera um pacote público traz um arquivo em `.changeset/` dizendo o tipo de bump (V-35); em passo separado as versões e changelogs são gerados e só pacotes alterados são publicados. Os comandos (`add`, `version`, `publish`) **não foram confirmados** na fonte lida: consulte a documentação oficial antes de sugerir ou rodar qualquer um.

## 8. Go/no-go resumido (itens do agente `auditor-release`)

| # | Item | Bloqueante |
| --- | --- | --- |
| 1 | Base atualizada e árvore limpa | Sim |
| 2 | CI verde para o SHA exato (sem checks = Não verificável) | Sim |
| 3 | Versão coerente com o maior impacto; quebra sem `!` = FALHOU | Sim |
| 4 | Commits fora do padrão listados (com release-please) | Não |
| 5 | CHANGELOG com a versão, data e links | Sim |
| 6 | Arquivos de versão consistentes (comparação numérica) | Não |
| 7 | Tag livre, nenhuma tag movida, anotada ou assinada | Sim |
| 8 | Release em rascunho, ativos previstos | Não |
| 9 | Proteção de branch e donos de código | Não |
| 10 | Plano de rollback pela forma do merge | Sim |
| 11 | Documentação da superfície pública nova | Não |
| 12 | Itens de QA fora do git (funcional, regressão, desempenho, segurança, dados) | Quem responde, registrado |

## 9. Fontes

- SemVer 2.0.0, Tom Preston-Werner, CC BY 3.0 (https://semver.org/; V-31, classe A).
- Keep a Changelog 1.1.0, Olivier Lacan, MIT (https://keepachangelog.com/en/1.1.0/; V-32, classe B).
- release-please, googleapis, Apache-2.0 (https://github.com/googleapis/release-please; V-33, classe A); não é produto oficial do Google, segundo o README.
- GitHub Docs: Managing releases e Automatically generated release notes (V-34, classe B).
- Manual do Git: `git-tag` (V-25, classe B). Changesets, MIT (V-35, classe B).
- gstack `land-and-deploy` e `document-release` (MIT, Garry Tan): veredito, deriva de versão e regra de não regravar o CHANGELOG, destilados.
