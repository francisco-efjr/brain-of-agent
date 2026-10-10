# Plano de backfill: [PIPELINE/TABELA]

Uso: pedido de reprocessar histórico. O resultado é um plano para aprovação humana; o plugin nunca executa backfill. Base: V-13, V-18, V-25 (a combinação é Inferido).
Rótulos: Verificado, Inferido, Suposição, Não verificável.

## 1. Escopo
- Tabela(s) afetada(s): [LISTA]
- Intervalo: [INÍCIO, FIM) em [FUSO]; granularidade da partição: [DIA|HORA|OUTRA]
- Motivo do backfill: [BUG|MUDANÇA DE REGRA|NOVA COLUNA|DADO ATRASADO]
- Consumidores que serão afetados enquanto o backfill roda: [LISTA]

## 2. Idempotência
- Estratégia: [MERGE POR CHAVE|APAGAR INTERVALO E INSERIR EM TRANSAÇÃO|OVERWRITE DE PARTIÇÃO]
- Critério de "qual versão vence": [TIMESTAMP/VERSÃO]
- Prova em dev: duas execuções do mesmo intervalo pequeno, contagem e soma de controle iguais. Resultado: [Verificado ou Não verificado]

## 3. Custo e carga
- Bytes estimados por partição (dry_run/EXPLAIN): [VALOR ou "pedir ao usuário"]; total: [VALOR]
- Limites de concorrência: `max_active_runs` [N], pools [NOME], limite na origem [LIMITE DA API/BANCO]
- Janela de execução (fora do pico): [HORÁRIO]

## 4. Ensaio em desenvolvimento
- Intervalo de ensaio: [2 A 3 PARTIÇÕES]; target: [NOME DO TARGET DE DEV]
- Comando proposto (não executado pelo plugin): `[COMANDO]`
- Critério de sucesso do ensaio: [CONTAGEM POR PARTIÇÃO IGUAL À DA FONTE]

## 5. Checagem pós-carga
| Verificação | Consulta | Esperado |
| --- | --- | --- |
| Contagem por partição origem vs destino | `[SQL]` | Igual, ou diferença explicada |
| Unicidade da chave | `[SQL]` | 0 duplicatas |
| Nulos em campos obrigatórios | `[SQL]` | 0 |
| Métrica de controle | `[SQL]` | [VALOR DE REFERÊNCIA] |

## 6. Rollback
- Como restaurar o intervalo anterior: [BACKUP|TIME TRAVEL DO WAREHOUSE|RECARGA DA FONTE]. Validado em: [DATA ou "não validado"].
- Limitação: rollback de código não restaura dado destruído.

## 7. Aprovação (obrigatória)
- Alvo exato e intervalo aprovados por: [NOME] em [DATA]
- Contagem de linhas afetadas estimada: [N]
- Quem executa: [NOME]; o agente não executa.

## 8. Riscos e não verificado
| Item | Rótulo | Observação |
| --- | --- | --- |
| [ITEM] | [ROTULO] | [OBS] |
