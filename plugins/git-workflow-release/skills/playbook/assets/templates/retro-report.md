# Template: retro de git

Adaptado do `retro` do gstack (MIT, Copyright (c) 2026 Garry Tan), destilado. Todos os valores vêm de comandos rodados; valor indisponível é "indisponível", nunca zero ou estimativa. Sem ranking de pessoas em time pequeno.

| Campo | Valor |
| --- | --- |
| Janela | `--since "AAAA-MM-DDT00:00:00"` (alinhada à meia-noite local) |
| Referência analisada | `origin/<base>` (informe se for outra) |
| `git fetch` antes? | sim / falhou (avisar) |
| Guarda de base desatualizada | último commit da referência em ____ (anterior à janela? se sim, parar) |

## Métricas (comando usado em cada uma)

| Métrica | Valor | Comando ou fonte |
| --- | --- | --- |
| Commits | | `git rev-list --count` |
| Autores | | `git shortlog -sn` |
| Mix por tipo Conventional | | contagem por prefixo |
| Razão `fix` | | `fix` / total (acima de 50% é sinal de revisão fraca; Suposição) |
| Tamanho dos commits | menos de 100 / 100 a 500 / 500 a 1500 / 1500+ linhas | `git log --numstat` |
| Arquivos alterados 5+ vezes (hotspots) | | |
| Razão de testes | | linhas de teste / linhas adicionadas |
| PRs mesclados | | `gh pr list --state merged` (referência em commit não prova merge) |

## Observações (cada uma com commits como evidência)

1.
2.

## Pontos fortes

-

## Oportunidades

-

## Três ações para o próximo ciclo

1.
2.
3.
