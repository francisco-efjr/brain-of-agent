# Relatório de EXPLAIN: [consulta ou endpoint]

Data: [AAAA-MM-DD] · Engine e versão: [ex.: PostgreSQL 16.x] · Origem do plano: [colado pelo usuário | executado em dev] · Ambiente do plano: [réplica | dev]

## 1. Consulta

```sql
[SQL com parâmetros reais ou representativos]
```

Frequência: [req/s] · latência-alvo: [ms] · volume das tabelas: [linhas]

## 2. Plano resumido

| Nó | Estimado (linhas) | Real (linhas) | loops | Tempo total do nó | Buffers (hit/read) | Observação |
| --- | --- | --- | --- | --- | --- | --- |

## 3. Diagnóstico

[Divergência estimado × real; Seq Scan em tabela grande; ordem de colunas; função em coluna; Sort em disco; N+1 fora do plano.]

## 4. Proposta

```sql
[CREATE INDEX CONCURRENTLY … (fora de transação) ou reescrita]
```

Efeito esperado: [Suposição; sem número inventado]. Custo de escrita e espaço: [descrever].

## 5. Medição antes/depois (preenchida pelo usuário)

| | Antes | Depois |
| --- | --- | --- |
| Tempo de execução | | |
| Buffers | | |
| Plano (nó principal) | | |

Comando a rodar nos dois casos: `EXPLAIN (ANALYZE, BUFFERS) [consulta];` (DML dentro de `BEGIN; … ROLLBACK;`, nunca em produção).

## 6. Riscos de escrita e próximos passos

[Impacto em INSERT/UPDATE; verificação de índice INVALID; novo plano com o mesmo volume.]
