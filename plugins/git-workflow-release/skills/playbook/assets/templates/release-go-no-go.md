# Template: go/no-go de release (versão enxuta, centrada em git)

Adaptado do checklist de go/no-go do brain-of-agent (conteúdo próprio do autor, MIT). Mantém só o que o git, o GitHub e o changelog conseguem provar. Itens de funcional, regressão, desempenho, segurança, dados, observabilidade e comunicação: use o template completo do plugin `qa-testing` e registre aqui apenas **quem responde** por eles.

Como usar: Status = OK, PENDENTE, FALHOU ou N/A (N/A exige motivo em Evidência). Evidência = comando, SHA, hora ou link verificável; "testado" sem evidência é PENDENTE. Itens com (*) são bloqueantes: PENDENTE ou FALHOU = NO-GO, salvo aceite formal registrado no parecer. Risco residual em linguagem de negócio.

| Campo | Valor |
| --- | --- |
| Release / versão | |
| SHA candidato | |
| Data e janela | |
| Responsável pelo checklist | |
| Decisores | |

## 1. Verificação de CI

| # | Item | Status | Evidência | Risco residual |
| --- | --- | --- | --- | --- |
| C1 (*) | Base atualizada com o remoto e árvore limpa | | `git rev-parse HEAD` vs `git ls-remote origin <base>` | |
| C2 (*) | CI verde para o SHA exato (sem checks = Não verificável) | | `gh run list --json headSha,conclusion` | |
| C3 | Checks não obrigatórios que falham estão listados | | | |

## 2. Versão e changelog

| # | Item | Status | Evidência | Risco residual |
| --- | --- | --- | --- | --- |
| V1 (*) | Commits desde a última tag classificados; versão coerente com o maior impacto | | `git log <tag>..HEAD` | |
| V2 (*) | Quebra de contrato com `!` ou `BREAKING CHANGE`; sem isso = FALHOU | | | |
| V3 (*) | CHANGELOG com entrada da versão, data e links; `Unreleased` movido; um gerador só | | | |
| V4 | Arquivos de versão consistentes entre si (comparação numérica) | | | |
| V5 | Commits fora do padrão listados como invisíveis (se release-please) | | | |

## 3. Tag e Release

| # | Item | Status | Evidência | Risco residual |
| --- | --- | --- | --- | --- |
| T1 (*) | Nome da tag livre; nenhuma tag existente será movida | | `git ls-remote --tags origin <tag>` | |
| T2 | Plano de tag anotada ou assinada e verificação | | `git tag -v` | |
| T3 | GitHub Release em rascunho com ativos e `.github/release.yml` | | `gh release view` | |
| T4 | Proteção de branch e code owners aplicáveis | | | |

## 4. Rollback

| # | Item | Status | Evidência | Risco residual |
| --- | --- | --- | --- | --- |
| B1 (*) | Rollback documentado pela forma do merge (dois pais `-m 1`, squash, rebase-merge com intervalo) | | `rollback-plan.md` | |
| B2 | Efeitos irreversíveis mapeados (migração de dados, e-mails, cobranças) com plano de correção para frente | | | |
| B3 | Versão corretiva `vX.Y.Z+1` prevista se a tag já existir | | | |

## 5. Comunicação e responsáveis pelos itens não git

| Área | Quem responde | Onde está a evidência |
| --- | --- | --- |
| Funcional e regressão | | |
| Desempenho e capacidade | | |
| Segurança | | |
| Dados e migração | | |
| Observabilidade e deploy | | |
| Notas de versão / comunicação | | |

## Parecer

**Recomendação:** GO / GO com condições / NO-GO

**Resumo:** (2 a 3 linhas para quem não vai ler o checklist)

**Verificado:** (evidências principais, com comando e hora)

**Não verificado:** (o que ficou de fora e por quê)

**Riscos residuais aceitos:**

| Risco (se... então...) | Probabilidade | Como detectamos | Contorno | Aceito por | Data |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

**Condições para GO:** (condição verificável + dono)

**Decisão:**

| Decisor | Papel | Decisão | Data e hora |
| --- | --- | --- | --- |
| | | | |

Este parecer não afirma deploy nem saúde em produção; isso é de `devops-cloud-infra` e `sre-observability`.
