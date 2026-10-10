# Relatório de aceitação de pipeline: [PIPELINE OU MODELO]

Uso: skill `pipeline-acceptance` (invocação explícita) e agente `data-pipeline-reviewer`. Base: V-05. "Build passou" e "N testes ok" não são evidência de corretude.
Target de execução: [NOME DO TARGET DE DEV] (confirmado como desenvolvimento por: [QUEM/COMO]). Produção ou desconhecido: parar e perguntar.

## Itens
| # | Verificação | Status (Verificado, Não verificado ou Reprovado) | Comando e evidência |
| --- | --- | --- | --- |
| 1 | Contagem origem = destino, por partição e por execução; total baixado = total informado pela fonte (paginação, limite, 429) | [STATUS] | Origem: [N] (`[COMANDO/CABEÇALHO]`) · Destino: [N] (`[SQL]`) · Páginas: [N] · limite: [VALOR] |
| 2 | Campos da origem = colunas de cada tabela | [STATUS] | Origem: [N CAMPOS] · Tabela [T]: [N COLUNAS] · Diferenças: [LISTA E DECISÃO REGISTRADA] |
| 3 | Segunda execução idêntica não falha nem duplica (consentimento por execução) | [STATUS] | Contagem após 1ª: [N] · após 2ª: [N] · soma de controle: [VALOR] |
| 4 | Chaves únicas e não nulas nos dados carregados | [STATUS] | `[SQL group by having count(*) > 1]` → [RESULTADO] · nulos → [RESULTADO] |
| 5 | SCD2: `check_cols`/`updated_at` cobre campos historicamente relevantes | [STATUS ou Não aplicável: motivo] | Campos relevantes: [LISTA] · configurados: [LISTA] |
| 6 | `warn` tratado como pendência com número | [STATUS] | [LISTA warn: NOME → CONTAGEM] |
| 7 | Métrica conferida à mão ou contra relatório estabelecido, com amostra ou invariante por entidade | [STATUS] | [CÁLCULO E FONTE] |
| 8 | O que não foi verificado, com motivo | [STATUS] | Ver seção "Não verificado" |

## Veredito
`[APROVADO | APROVADO COM PENDÊNCIAS | REPROVADO | NÃO VERIFICÁVEL]` porque [MOTIVO EM UMA LINHA].

## Pendências
| Pendência | Contagem | Dono | Prazo |
| --- | --- | --- | --- |
| [ITEM] | [N] | [NOME] | [DATA] |

## Não verificado
- [ITEM E MOTIVO]

## Riscos e próximo passo
- [RISCO]
- Próximo passo: [AÇÃO]

## Manifesto de execução
Ver `manifesto-de-execucao.md` (preencher e colar aqui os campos usados).

Teto: três falhas de execução seguidas encerram a tentativa; reavalie a abordagem com o usuário.
