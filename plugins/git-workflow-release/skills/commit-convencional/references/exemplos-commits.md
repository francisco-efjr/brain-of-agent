# Exemplos de commits (commit-convencional)

Sumário: 1 Tipos e efeito em SemVer · 2 Assuntos bons e maus · 3 Divisão passo a passo · 4 Corpo e rodapés · 5 Quebra de contrato · 6 Revert · 7 Monorepo · 8 Fontes.

Conferido em 2026-10-10. Os exemplos são fictícios (números de issue, hashes e valores ilustrativos). Tipos além de `feat` e `fix` são convenção de projeto: a especificação não os define (V-18). Texto destilado de Conventional Commits 1.0.0 (CC BY 3.0, https://www.conventionalcommits.org/en/v1.0.0/) com redação própria.

## 1. Tipos e efeito em SemVer

| Tipo | Use quando | Efeito na versão (com release-please/semantic-release) |
| --- | --- | --- |
| `feat` | Funcionalidade nova visível a quem consome | MINOR |
| `fix` | Correção de comportamento errado | PATCH |
| `perf` | Mesmo comportamento, mais rápido ou mais leve | em geral PATCH; depende da ferramenta |
| `refactor` | Reorganiza código sem mudar comportamento | nenhum |
| `docs` | Só documentação | nenhum |
| `test` | Só testes | nenhum |
| `build`, `ci` | Sistema de build, dependências, pipeline | nenhum |
| `chore` | Manutenção que não cabe acima | nenhum |
| `revert` | Desfaz commit anterior | conforme o que desfaz |
| qualquer tipo + `!` ou rodapé `BREAKING CHANGE:` | Quebra de contrato público | MAJOR |

`style` (formatação sem efeito visível) existe na convenção Angular; use só se o repositório já usa. Mudança visual para o usuário não é `style`.

## 2. Assuntos bons e maus

| Mau | Por quê | Bom |
| --- | --- | --- |
| `fix bug` | Não diz qual (exemplo de má descrição em V-30) | `fix(checkout): reject expired coupons at order creation` |
| `Phase 1` | Descreve etapa, não mudança | `feat(export): add CSV export for order list` |
| `update stuff` | Vazio de informação | `refactor(auth): extract token refresh into its own module` |
| `Fixed the login.` | Passado, ponto final | `fix(auth): keep session after token refresh` |
| `feat: add feature that lets users export their data to CSV and JSON with filters` | Mais de 72 caracteres | `feat(export): add CSV and JSON export with filters` |
| `WIP` | Não entra em histórico compartilhado | commit local e depois squash com `rebase-seguro` |

Regra de bolso: o assunto completa a frase "Se aplicado, este commit vai ...". Idioma e caixa seguem o histórico do repositório.

## 3. Divisão passo a passo (diff misto)

Entrada (`git status --short`):

```text
 M src/api/rate.ts
 M src/api/rate.test.ts
 M README.md
 M package-lock.json
 M ui/Button.css
```

Raciocínio:
1. `rate.ts` e `rate.test.ts`: mesmo assunto, vão juntos (teste com o código).
2. `README.md`: se descreve o limite de taxa, é documentação do mesmo assunto, mas é revisada por outras pessoas; commit `docs` separado, depois do `feat`, ou junto se a equipe prefere (decida pelo histórico).
3. `package-lock.json` sem `package.json` alterado: suspeito (instalação acidental). Pergunte; se foi acidente, `git restore package-lock.json` só com a confirmação da pessoa.
4. `ui/Button.css`: outro assunto. Commit à parte ou fora desta rodada.

Plano:

| Grupo | Arquivos | Mensagem | Comando |
| --- | --- | --- | --- |
| 1 | `src/api/rate.ts`, `src/api/rate.test.ts` | `feat(api): add rate limiting to public endpoints` | `git add src/api/rate.ts src/api/rate.test.ts` |
| 2 | `README.md` | `docs(api): document rate limit headers` | `git add README.md` |
| 3 | `ui/Button.css` | `fix(ui): raise contrast of primary button` (se for contraste) | `git add ui/Button.css` |

Fora até esclarecer: `package-lock.json`.

Verificação: rode lint e testes uma vez na árvore completa antes do grupo 1; em seguida confira que a ordem dos commits não deixa um commit intermediário sem compilar (dependência antes de quem a usa). Para checar todos de uma vez, a pessoa pode rodar depois `git rebase --exec '<comando de teste>' <base>` (Inferido: recurso padrão do rebase, não testado aqui); isso é do `rebase-seguro`.

## 4. Corpo e rodapés

```text
fix(billing): round invoice totals half-up before tax

Totals were rounded after tax, so a 10 percent rate on 0.05 produced
a one-cent difference from the payment provider. Rounding before tax
matches the provider and keeps the invoice reproducible.

Refs: #482
```

- Primeira linha: o quê. Corpo: por quê, alternativa descartada, limitação conhecida. O diff já mostra o como.
- Linha em branco entre assunto e corpo; corpo com linhas de até cerca de 72 caracteres (convenção).
- Rodapés usam `Token: valor` (`Refs: #482`, `Reviewed-by: ...`). Não invente número de issue: se não foi informado, omita o rodapé.
- `Release-As: 2.0.0` só quando a pessoa pedir para forçar a versão com release-please, e vai no corpo do commit (V-33).

## 5. Quebra de contrato

```text
feat(api)!: remove /v1/orders endpoint

BREAKING CHANGE: clients must call /v2/orders. /v1/orders returned
prices as strings; /v2/orders returns integers in cents.
```

Quebra é qualquer mudança que faz um consumidor correto deixar de funcionar: rota removida, campo renomeado, exit code alterado, flag removida, formato de arquivo incompatível. Em 0.y.z a convenção permite qualquer mudança, mas registre mesmo assim para o changelog (V-31). Dúvida sobre ser quebra: pergunte; é o dado que decide MAJOR em `release-cut`.

## 6. Revert

```text
revert: feat(export): add CSV export for order list

This reverts commit a1b2c3d. The export times out above 50k rows.
```

Prefira `git revert <sha>` (cria o commit com mensagem padrão; complete o motivo no corpo). Em histórico publicado é a opção segura (V-24). Reverter um merge exige `-m 1` e tem efeitos sobre merges futuros: use `rebase-seguro`.

## 7. Monorepo

- Escopo igual ao nome do pacote: `feat(api): ...`, `fix(web): ...`. Commit que toca dois pacotes costuma ser dois commits; se não for possível separar, escopo do pacote principal e menção no corpo.
- Se o CLAUDE.md da raiz manda prefixo simples (`api: add rate limiting`, exemplo oficial em V-13), siga o do repositório e não use os dois formatos.
- Ferramentas por pacote (release-please em modo manifesto, Changesets) dependem desse escopo ou de arquivos separados: não mude a convenção por conta própria (lacuna G3: comandos não confirmados).

## 8. Fontes

- Conventional Commits 1.0.0, CC BY 3.0 (V-18, classe B).
- Google eng-practices, descrições de CL (CC-BY 3.0; V-30, classe B): assunto curto, imperativo, corpo com o porquê.
- Exemplo oficial de prefixo de pacote: https://code.claude.com/docs/en/large-codebases (V-13, classe A; documentação da Anthropic, só destilada).
- Gstack `ship` (MIT): ordem de commits bisectáveis; processo destilado, sem cópia.
