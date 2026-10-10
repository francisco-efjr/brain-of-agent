# Releases e versionamento

SemVer, changelog, release-please, GitHub Releases, fluxo manual, veredito honesto, deriva de versão, auditoria de docs e retro de git. Fontes por ID em [fontes.md](fontes.md). Deploy e publicação em gerenciadores de pacotes ficam fora deste plugin (`devops-cloud-infra`, `cli-desktop-tooling`).

## Sumário

1. SemVer: tabela de decisão
2. Changelog: humano ou gerado
3. release-please
4. GitHub Releases e notas
5. Changesets
6. Fluxo manual de release (10 passos)
7. Veredito honesto pós-merge
8. Deriva de versão entre branches
9. Auditoria de docs com mapa de cobertura
10. Retro de git
11. Gotchas
12. Hotfix e backport para versão mantida

## 1. SemVer: tabela de decisão (V-31, Tom Preston-Werner, CC BY 3.0)

| Mudança | Bump | Observação |
| --- | --- | --- |
| Quebra da API pública (incompatível) | MAJOR | Declare o que é API pública; sem declaração, a decisão é sua e deve ser explícita |
| Funcionalidade nova compatível | MINOR | |
| Correção compatível | PATCH | |
| Só candidata a release | `-rc.N` (pré-release, hífen) | Precedência: pré-release é menor que a versão normal |
| `0.y.z` | Qualquer mudança pode quebrar | Convém avisar quando quebrar |
| Metadados `+build` | Ignorados na precedência | |

Regras do plugin:
- A versão sai do **contrato público**, não de contagem de linhas. O `ship` do gstack decide por quantidade de linhas e usa 4 dígitos; este plugin não importa isso (C5).
- Propor sempre, com os commits que sustentam; **pedir confirmação para MINOR, MAJOR e para qualquer 0.y.z que quebre**. Esse gate de MINOR e MAJOR é o do `ship` (GS-ship Step 12) e foi confirmado no arquivo local; a página do SemVer não o exige.
- Versão lançada não pode ser modificada (V-31): correção vira nova versão.
- Com Conventional Commits: `fix` → PATCH, `feat` → MINOR, `!` ou `BREAKING CHANGE` → MAJOR; `docs`, `chore`, `ci`, `test`, `build` não geram release (V-33).

Exemplo: tag anterior `v1.4.2`; commits `feat: add export`, `fix: null date`, `feat!: remove /v1/orders`, `docs: ...` → **2.0.0** (há `feat!`), não 1.5.0. Peça confirmação do MAJOR.

## 2. Changelog: humano ou gerado

| Critério | Humano (Keep a Changelog 1.1.0, MIT, V-32) | Gerado (release-please, V-33) |
| --- | --- | --- |
| Formato | `Unreleased` no topo; Added, Changed, Deprecated, Removed, Fixed, Security; declara adesão ao SemVer | Formato próprio da ferramenta (diferente do KaC) |
| Quem escreve | Pessoa, para o usuário final | Ferramenta, a partir dos commits |
| Exige | Disciplina na escrita | Conventional Commits em todo commit |
| Decisão | Produto com público externo e mudanças que merecem narrativa | Muitos commits regulares, equipe disciplinada |

Regras: "Don't let your friends dump git logs into changelogs" (V-32, citação curta). **Nunca dois geradores no mesmo arquivo.** Com release-please, a skill confere o PR de release e não edita o CHANGELOG. Nunca reescreva entradas antigas; use edição exata só da entrada nova (GS-doc).

## 3. release-please (V-33, Apache-2.0, "not an official Google product")

- Mantém um PR de release que se atualiza a cada merge; mesclar o PR cria tag e release.
- `fix:` → patch, `feat:` → minor, `feat!:` ou `BREAKING CHANGE` → major. `Release-As: 2.0.0` no **corpo** do commit força a versão.
- Recomenda **squash merge**. Commits fora do padrão ficam invisíveis.
- Labels: `autorelease: pending` e `tagged` são aplicados; o label `autorelease: published` **não** é aplicado automaticamente.
- **Não publica** em gerenciadores de pacotes. A ação é `googleapis/release-please-action`; seu conteúdo e a configuração de monorepo (manifesto) não foram lidos (G3).

## 4. GitHub Releases e notas (V-34)

- Release a partir de tag existente ou nova; **rascunho**; "Generate release notes"; marcar como última ou deixar o GitHub decidir por SemVer; caixa de pré-release.
- **Releases imutáveis (opção que se habilita por repositório ou organização; Verificado em docs.github.com, 2026-10-10):** com a opção ligada, depois de publicada não se alteram ativos nem se move ou apaga a tag; título, notas e status de pré-release continuam editáveis. Sem a opção, nada impede mexer, mas quem baixou a versão já confiou nela. Portanto: criar rascunho, anexar **todos** os ativos, gerar e revisar notas, só então publicar.
- `.github/release.yml` define `changelog.exclude` (labels e autores) e `categories` (título e labels, `*` coringa). Modelo em `assets/templates/release-notes-and-release-yml.md`.
- A página não diz quem pode criar releases (Não verificável).

## 5. Changesets (V-35, MIT)

Cada PR que muda pacote público traz um arquivo de changeset com o tipo de bump; versões e changelog saem de um passo separado; publica-se só o que mudou. Comandos `add`, `version`, `publish` não foram confirmados na página lida: consulte a documentação oficial antes de escrever workflow (G3).

## 6. Fluxo manual de release (skill `release-cut`)

Modelo preenchível: `assets/templates/release-checklist.md`. Cada ação externa pede confirmação por escrito, uma de cada vez.

1. **Modo:** há `release-please-config.json`, `.release-please-manifest.json` ou `.changeset/`? Com automação, confira o PR gerado e oriente o merge; não edite o CHANGELOG.
2. **Pré-requisitos:** na branch base, árvore limpa, `git fetch` feito, CI verde **para o SHA exato** com recibo. Sem CI: Não verificável; peça decisão.
3. **Última tag:** `git describe --tags --abbrev=0` (falha sem tags: primeira release; proponha 0.1.0 ou 1.0.0 e pergunte se a API pública está declarada). `git describe` ignora tags leves.
4. **Commits desde a tag:** `git log <tag>..HEAD --oneline`, agrupados por tipo; commits fora do padrão em lista "invisíveis para a automação".
5. **Versão** pela tabela da seção 1, com justificativa; confirmação para MINOR e MAJOR.
6. **Branch `release/vX.Y.Z`:** entrada do CHANGELOG (seção 2) e arquivo de versão numa mudança só; commit `chore(release): vX.Y.Z`; PR (skill `criar-pr`); o merge é humano.
7. **Depois do merge:** releia a base e confirme o SHA de release. Com confirmação: (a) `git tag -a vX.Y.Z -m "..."` (ou `-s`) e `git tag -v`; (b) push da tag (comando exato mostrado); (c) GitHub Release em rascunho, ativos anexados, notas revisadas, então publicar.
8. **Verificar:** `git ls-remote --tags origin vX.Y.Z` com o SHA esperado; `gh release view vX.Y.Z`.
9. **Veredito** (seção 7) e relatório: versão, justificativa, tag, SHA, link, pendências.
10. **Opcional:** agente `auditor-release` antes do passo 6 para go/no-go; auditoria de docs (seção 9) se a superfície pública mudou.

Rollback: nunca mover ou recriar tag publicada; corrija com `vX.Y.Z+1` contendo o `git revert` do problema ([historia-e-git-avancado.md](historia-e-git-avancado.md), seção 8).

## 7. Veredito honesto pós-merge (GS-land Step 9 e BA-entrega, adaptados)

Preparar, mesclar, tag, publicar, implantar e verificar são estados diferentes. Escolha o **primeiro** que casar e nunca infira um do outro (merge ou HTTP 200 não provam deploy):

| Evidência | Veredito |
| --- | --- |
| PR de release aberto, nada mesclado | PREPARADA |
| PR mesclado, tag inexistente | MESCLADA |
| Tag criada e verificada (`git tag -v`/`ls-remote` com o SHA esperado) | TAGUEADA |
| GitHub Release publicada e listada (`gh release view`) | PUBLICADA |
| Falta qualquer evidência acima | NÃO VERIFICADA (diga qual evidência falta) |
| Rollback pedido e não confirmado | ROLLBACK PENDENTE |

Deploy, canário e saúde em produção: o gstack só declara "implantado e verificado" com deploy do SHA correto e canário saudável. Isso é de `devops-cloud-infra` e `sre-observability`. Distinção de BA-entrega: preparar release, publicar artefato, implantar, habilitar e verificar produção são ações separadas; keyword de modo não amplia permissão. Rollback de binário não desfaz e-mail enviado, cobrança ou migração de dados: sinalize irreversibilidade.

## 8. Deriva de versão entre branches (GS-land Step 3.4, destilado)

Antes de mesclar PR que altera arquivo de versão, compare a versão do PR com a da base e com a de outras branches em voo **numericamente por componente**, não como texto: `1.10.0` é maior que `1.9.0`, mas em ordem lexical é menor. Versão ausente ou ilegível de um lado é "indisponível", não "verde". Se a versão do PR ficou abaixo do próximo número livre, pare e reconcilie arquivo de versão, lockfile, CHANGELOG e título; não faça bump automático (versões duplicadas sobrescrevem notas de outra branch). Projeto sem fonte de versão: Não aplicável.

## 9. Auditoria de docs com mapa de cobertura (GS-doc Step 1.5, MIT, destilado)

Só quando a superfície pública muda ou a pessoa pede; informa lacunas, não gera páginas (C13).

1. Extraia do diff a superfície pública: funções, comandos, flags, endpoints, variáveis de ambiente.
2. Cruze com a documentação existente e monte o mapa entidade × {referência, how-to, tutorial, explicação} (estrutura Diátaxis). Modelo: `assets/templates/docs-coverage-map.md`.
3. Zero cobertura = lacuna crítica; só referência = lacuna comum. Relate como dívida de documentação.
4. Correções factuais diretas podem ser aplicadas; mudança narrativa, de segurança ou remoção vira pergunta. Diagramas desatualizados apenas sinalizados.
5. Nunca regravar o CHANGELOG nem mudar a versão sem perguntar. Toda doc deve ser alcançável a partir do README ou do CLAUDE.md. A escrita é do plugin `technical-writing-docs`.

## 10. Retro de git (GS-retro, MIT, destilado; skill/prompt P-26)

Modelo: `assets/templates/retro-report.md`.

- **Janela alinhada à meia-noite local:** `git log --since "AAAA-MM-DDT00:00:00"`; sem o sufixo o Git usa a hora atual do relógio.
- `git fetch` antes; se o fetch falhar, avise. Guarda de base desatualizada: se o último commit da referência é anterior à janela, a base provavelmente está velha ou a data de hoje está errada; pare e confirme.
- Métricas: commits, autores, mix por tipo Conventional, razão `fix` (> 50% é sinal de revisão fraca, regra do gstack, Suposição), tamanho de commit em faixas (< 100, 100–500, 500–1500, 1500+ linhas), arquivos alterados 5 vezes ou mais (hotspots), razão de testes, sessões por intervalo de ~45 min.
- PRs mesclados vêm do `gh`, não de menção em commits. Valor indisponível é "indisponível", não zero. Nada de inventar números.
- Sem ranking de pessoas em time pequeno (o gstack faz leaderboard e streak; não importado). Observações sempre com commits como evidência; termine com 3 ações.

## 11. Gotchas

- `git describe` falha sem tags e ignora tags leves.
- `Release-As:` vai no corpo; título não conta.
- `autorelease: published` não é automático.
- Squash merge descarta a granularidade interna do PR; PRs pequenos compensam.
- Release do GitHub publicada com a opção de releases imutáveis ligada trava ativos e tag: anexe tudo em rascunho antes.
- Pré-release `-rc.N` não substitui a versão final.
- Monorepo: manifesto do release-please e changesets têm lacunas (G3); não implemente sem ler a documentação.

## 12. Hotfix e backport para versão mantida (lacuna G2 reduzida)

Quando uma correção precisa sair numa linha antiga (por exemplo `release/1.x`) sem levar as funcionalidades novas da principal. Rótulo: `git cherry-pick -x` e `-m` Verificados localmente com git 2.54.0 (2026-10-10; `-x` acrescenta a linha "(cherry picked from commit ...)" à mensagem); o fluxo é conhecimento estável de Git, **Inferido**, sem fonte A ou B lida. Release-please com várias branches de manutenção não foi lido: confira a documentação dele antes de automatizar.

1. **Corrija primeiro na principal**, com teste que falha antes e passa depois (V-17), via PR. Assim a correção não se perde na próxima versão.
2. **Branch de backport** a partir da linha mantida, em nome próprio (`backport/<assunto>-1.x`); criar a branch é local, publicar é confirmação.
3. **Traga a correção** com `git cherry-pick -x <sha>`. A forma do merge na principal decide o comando: squash é um commit só; merge commit exige `-m 1`; rebase-merge pede o intervalo, do mais antigo ao mais novo. Conflito: `resolver-conflitos` (em cherry-pick, "ours" é a branch atual).
4. **Teste na branch de manutenção**, não na principal: o mesmo teste de regressão e a suíte do módulo, com o comando e o código de saída colados.
5. **PR para a branch de manutenção**, com a referência ao PR original e o motivo de a correção ser segura de portar.
6. **Versão:** correção compatível vira PATCH da linha mantida (por exemplo `v1.4.3`, mesmo que a principal esteja em 2.x). A tag segue as regras de `release-cut` (anotada, uma confirmação por ação externa); o fluxo automático da skill assume a branch principal e **não cobre** release branches, então conduza esse passo manualmente e declare a limitação.
7. **Não desfaça um hotfix publicado** movendo a tag: publique o PATCH seguinte.

