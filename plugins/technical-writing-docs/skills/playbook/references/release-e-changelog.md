# Changelog, versão e release notes

Validado em 2026-10-10 (V-13, V-14, V-28, V-41, V-42; regras de GS-rel, MIT, Copyright (c) 2026 Garry Tan). Keep a Changelog 1.1.0: MIT. Conventional Commits 1.0.0: CC BY 3.0 (atribuição ao projeto Conventional Commits). Aqui só o **texto**; cortar versão, criar tag e publicar é do plugin `git-workflow-release`.

## Sumário

1. Keep a Changelog: modelo e regras
2. Commits convencionais → efeito de versão
3. Do intervalo de commits à entrada
4. Regras absolutas de edição
5. Release notes do GitHub e `release.yml`
6. Changelog de API
7. Fronteira com git-workflow-release

## 1. Keep a Changelog: modelo e regras (V-13)

Princípios: changelog é para **humanos**; uma seção por versão, a mais nova primeiro; datas em ISO 8601 (`AAAA-MM-DD`); declare que segue SemVer; mantenha `## [Unreleased]` no topo. Seis tipos: Added, Changed, Deprecated, Removed, Fixed, Security. Em português, mantenha os nomes dos tipos em inglês se o projeto já usa assim (consistência com ferramentas), ou traduza todos (Adicionado, Alterado, Obsoleto, Removido, Corrigido, Segurança) e registre a escolha. Template: [changelog-keepachangelog](../assets/templates/changelog-keepachangelog.md).

Cada entrada: uma linha, voz ativa, responde "o que muda para quem usa". Link de PR ou issue só se vier dos dados (nunca inventado). Changelog não é despejo do `git log`.

## 2. Commits convencionais → efeito de versão (V-14)

Estrutura: `<tipo>[escopo opcional]: <descrição>`, corpo e rodapés separados por linha em branco.

| Sinal no commit | Efeito SemVer | Observação |
| --- | --- | --- |
| `fix` | PATCH | |
| `feat` | MINOR | |
| `!` imediatamente antes de `:` ou rodapé `BREAKING CHANGE:` | MAJOR | `BREAKING CHANGE` em maiúsculas (sinônimo `BREAKING-CHANGE`) é a exceção à regra de que a caixa não diferencia |
| `docs`, `chore`, `ci`, `test`, `refactor`... | sem efeito implícito | Entram no changelog só se mudam algo para quem usa |

A norma não limita o tamanho da descrição. Versão é **recomendação** que o usuário confirma; não altere `VERSION`, `package.json` nem crie tag (GS-rel: nunca subir VERSION sem perguntar).

## 3. Do intervalo de commits à entrada

Exemplo (hipotético, intervalo `v1.4.2..HEAD`):

| Commit | Decisão | Entrada resultante |
| --- | --- | --- |
| `feat: export csv` | Added | "Exporta relatórios em CSV pelo botão Exportar." |
| `fix(date): null crash` | Fixed | "Corrige o travamento ao abrir pedidos sem data." |
| `feat!: remove /v1/orders` | Removed + quebra | "**Quebra:** remove o endpoint `/v1/orders`; use `/v2/orders`." |
| `chore: bump deps`, `ci: cache`, `docs: typo` | omitir | sem impacto para quem usa |

Versão recomendada: 2.0.0 (há quebra), **como proposta** a confirmar. Tabela de rastreio obrigatória: `entrada → commit/PR`, cobrindo 100% das entradas novas.

Passos: (1) detectar `CHANGELOG.md`, `.github/release.yml` e histórico convencional e seguir o formato existente; (2) obter o intervalo, e perguntar o ponto de partida se `git describe` falhar por falta de tags; repositório sem commits: pare; (3) classificar; (4) reescrever; (5) inserir com edição exata em `[Unreleased]` ou em seção nova datada; (6) apresentar a versão recomendada; (7) oferecer o modelo de `release.yml` como texto.

Comandos de leitura úteis (somente leitura): `git log <intervalo> --oneline`, `git tag --list`, `git describe --tags`. Não use `git log --output=<arquivo>` (grava em disco).

## 4. Regras absolutas de edição (GS-rel, adaptadas)

- Nunca sobrescreva, substitua ou regenere entradas existentes do CHANGELOG; só polir redação com edição de texto exato, nunca `Write` sobre o arquivo inteiro.
- Nunca suba a versão sem pedir.
- Leia o arquivo inteiro antes de editar; cada edição com resumo de uma linha.
- Correção factual clara derivada do diff (caminho, contagem, nome) pode ser aplicada com diff listado; **pergunte** antes de remover conteúdo, mudar narrativa, tocar segurança ou mexer em CHANGELOG ou ADR existente (C-08).
- Dívida de documentação vai no corpo do PR (`## Dívida de documentação`), não em silêncio.

## 5. Release notes do GitHub e `release.yml` (V-42)

Sem o arquivo, as notas geradas trazem PRs mesclados, colaboradores e o link do changelog completo. Com `.github/release.yml`: `changelog.exclude.labels` e `changelog.exclude.authors`; `changelog.categories[*].title` e `.labels` obrigatórios; `exclude.labels` e `exclude.authors` por categoria; `"*"` em `labels` é a categoria de captura; a ordem das categorias importa (Inferido: as primeiras casam antes). **Comportamento de PR que não casa categoria alguma sem `*` não está documentado: teste.** Revise o texto gerado antes de publicar. Texto voltado ao usuário: escreva você (ou revise) a partir de "o que muda para quem usa"; as notas geradas são rascunho e lista de PRs (C-12). Combine com títulos de PR no padrão Conventional Commits. Modelo: [release-yml](../assets/templates/release-yml.md).

Exemplos oficiais de release notes voltadas ao usuário além de GitHub e Stripe não foram encontrados (G-07). A página `developers.google.com/style/release-notes` é o changelog do próprio guia, não orientação.

## 6. Changelog de API (V-41)

Quebra de compatibilidade marcada em tabela (mudança, área afetada, quebra sim/não, canal estável/preview) e deprecação com alternativa; ver [codigo-e-api](codigo-e-api.md), seção 9.

## 7. Fronteira com git-workflow-release

- Changelog **dentro** de um corte de release → `/git-workflow-release:playbook` (`release-cut`). Changelog avulso, sem corte → `escrever-changelog-release`. (Regra proposta; Suposição até alinhamento entre os plugins.)
- Política de commits, `release.yml` como configuração do repositório, tag e publicação: lá.
- O mapa de cobertura de docs do PR tem um só dono: `auditor-de-docs` (aqui).
