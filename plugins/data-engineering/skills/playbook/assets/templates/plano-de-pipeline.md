# Plano de pipeline: [NOME]

Uso: antes de implementar pipeline novo ou mudança estrutural. O agente `data-pipeline-architect` preenche; um humano aprova. Este plano não autoriza escrita em produção, execução de DAG nem backfill.
Rótulos: Verificado, Inferido, Suposição, Não verificável, Não aplicável. Campos sem resposta ficam como "Suposição: ..." ou "Pergunta: ...".
Base: V-04, V-18, V-20, V-22; formato de decisão inspirado nos modelos de ADR e de plano de incremento do brain-of-agent (MIT).

## 1. Objetivo e consumidores
- Resultado de negócio: [O QUE MUDA PARA QUEM]
- Consumidores (dashboards, modelos, times) e SLA de frescor: [LISTA]
- Dono do dado: [NOME OU PENDÊNCIA]

## 2. Fontes e volumes
| Fonte | Tipo (tabela, API, arquivo, tópico) | Volume (linhas/dia) | Limites (paginação, taxa) | Como obter a contagem da fonte |
| --- | --- | --- | --- | --- |
| [FONTE] | [TIPO] | [N] | [LIMITES] | [COMANDO OU CABEÇALHO] |

## 3. Ambiente e versões
dbt [VERSÃO] / adapter [ADAPTER] · orquestrador [AIRFLOW 2|3|DAGSTER|PREFECT] [VERSÃO] · Spark/Flink [VERSÃO] · warehouse [NOME] · target de dev: [NOME] · onde NÃO escrever: [PRODUÇÃO]

## 4. Desenho
- Escolha: [WORKFLOW COM CHECAGEM ENTRE ETAPAS | PARALELIZAÇÃO COM AMOSTRA | AGENTE COM TETO DE PASSOS] porque [MOTIVO EM UMA LINHA].
- Alternativa descartada: [ALTERNATIVA] porque [MOTIVO].
- Batch ou streaming: [ESCOLHA]; decisão que muda se o dado chegar mais cedo: [DECISÃO].

## 5. Camadas, grain e chaves
| Modelo/tabela | Camada | Grain (uma linha por...) | Chave | Materialização |
| --- | --- | --- | --- | --- |
| [NOME] | staging/intermediate/mart | [GRAIN] | [CHAVE] | [view/table/incremental] |

## 6. Estratégia de carga e reprocessamento
- Carga: [MERGE POR CHAVE | APAGAR INTERVALO E INSERIR | OVERWRITE DE PARTIÇÃO]; critério de "qual versão vence": [TIMESTAMP/VERSÃO].
- Dado atrasado: janela de reprocessamento de [N] dias porque [MOTIVO].
- Reprocessamento/backfill: ver `plano-de-backfill.md` (somente plano).

## 7. Garantias (obrigatório se houver streaming)
| Fonte | Estado | Sink | Garantia da fonte | Garantia do sink | Garantia ponta a ponta | Como testar (reinício, duplicidade) |
| --- | --- | --- | --- | --- | --- | --- |
| [FONTE] | [CHECKPOINT/ESTADO] | [SINK] | [EXACTLY-ONCE/AT-LEAST-ONCE] | [IDEM] | [IDEM] | [TESTE] |

## 8. Contrato e qualidade
- Contrato: ver `contrato-de-dados-odcs.md` (status: [rascunho|validado|não aplicável]).
- Regras:
| Regra | Ação (fail/drop/warn) | Contagem reportada em | Quarentena |
| --- | --- | --- | --- |
| [REGRA] | [AÇÃO] | [ONDE] | [DESTINO] |

## 9. Custo
Partição/cluster: [COLUNA]. Bytes estimados por execução: [dry_run: VALOR OU "não estimado"]. Limites de bytes/timeout: [VALORES].

## 10. Oráculo e verificação
- Critério de pronto: [CONTAGEM/MÉTRICA/FIXTURE QUE PROVA]
- Comando de verificação literal: `[COMANDO]`
- Segunda execução: [RESULTADO ESPERADO]

## 11. Incrementos com critério de saída
| # | Entrega | Critério de saída (comando e resultado esperado) | Gate humano antes de |
| --- | --- | --- | --- |
| 1 | [ENTREGA] | [CRITÉRIO] | [ESCRITA EM PRODUÇÃO/BACKFILL/MERGE] |

## 12. Decisão material (opcional; formato ADR)
Contexto · Opções consideradas · Decisão · Consequências · Reversibilidade · Quem decidiu e quando.

## 13. Riscos e itens não verificados
| Risco/item | Rótulo | Mitigação ou como verificar |
| --- | --- | --- |
| [ITEM] | [Inferido/Suposição/Não verificável] | [AÇÃO] |

## 14. Aprovação
Aprovado por: [NOME] em [DATA]. Escopo aprovado: [O QUE]. Fora do escopo: [O QUE].
