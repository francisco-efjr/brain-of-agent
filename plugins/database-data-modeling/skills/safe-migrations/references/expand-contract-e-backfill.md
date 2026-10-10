# Expand, migrate, contract e backfill seguro

Conferido em 2026-10-10 contra V-20 (Fowler "Parallel Change" e Stripe "Online migrations": só destilação, direitos reservados), V-21 (pgroll, Apache-2.0, conceito), V-36 (revisão em camadas), V-38 (idempotência e validação pós-escrita; regras PySpark CC0 reescritas), V-10/V-11 e o brain `dados-e-migracoes.md` (MIT, Brain of Agent: seção "Expandir, migrar, contrair" adaptada). Código é ilustrativo: adaptar e testar na engine do projeto, sempre em ambiente não produtivo primeiro.

Sumário
1. Por que existe
2. As seis fases (saída e rollback por fase)
3. Exemplo completo: renomear `users.name` para `users.full_name`
4. Backfill: regras e script
5. Escrita dupla e reconciliação
6. Variantes: tipo, remoção, tabela nova
7. Critério de interrupção
8. Revisão em camadas

## 1. Por que existe

Durante um deploy, versões antigas e novas da aplicação rodam ao mesmo tempo (blue/green, rolling, réplicas que reiniciam em momentos diferentes). Um DDL destrutivo ou incompatível quebra a versão antiga. Rollback de código também não desfaz schema nem dado transformado. O padrão separa a mudança em passos compatíveis com as duas versões (V-20, brain).

## 2. As seis fases

| # | Fase | O que fazer | Saída verificável (critério para avançar) | Rollback |
| --- | --- | --- | --- | --- |
| 1 | **Expand** | Criar a estrutura nova sem remover a antiga; aplicação passa a escrever nas duas | Escrita dupla sem erro por N dias (N combinado) | Parar a escrita nova; estrutura nova fica ociosa |
| 2 | **Backfill** | Copiar o histórico em lotes, fora de transação longa, idempotente | Contagem e amostra conferidas (seção 4) | Interromper o job; reexecutar é seguro |
| 3 | **Verificação** | Comparar as leituras das duas fontes, sem alterar a resposta ao usuário | Divergência abaixo do limite acordado (idealmente zero) | Corrigir o backfill/escrita e repetir |
| 4 | **Migrate (leitura)** | Trocar a leitura para o novo caminho por feature flag, em fração crescente | Métricas estáveis em cada faixa (erro, latência, divergência) | Voltar a flag |
| 5 | **Contract (escrita)** | Trocar a escrita para o novo caminho; deixar o código legado lançar erro por um ciclo | Nenhum acesso ao caminho antigo nos logs | Reativar escrita dupla (se o código legado ainda existe) |
| 6 | **Limpeza** | Remover coluna/tabela/trigger/view antiga em **migração separada**, depois da janela de observação; registrar o que foi removido | Backup lógico guardado; janela cumprida; consumidores confirmados | Só restauração de backup (por isso o backup e a janela) |

Notas: a fase 6 é a única irreversível sem restauração. As fases 1 a 5 devem estar em implantações separadas quando houver versões coexistindo. Em equipes pequenas sem flag, as fases 4 e 5 viram dois deploys com monitoramento entre eles.

## 3. Exemplo completo: renomear `users.name` -> `users.full_name` (PostgreSQL)

Contexto: tabela `users` com 30 milhões de linhas, tráfego 24x7. Um `ALTER TABLE ... RENAME COLUMN` quebraria instantaneamente a versão antiga da aplicação; um autogenerate que gerou drop+add perderia os dados (V-30).

**Fase 1 (expand).** Migração:
```sql
SET lock_timeout = '5s';
ALTER TABLE users ADD COLUMN full_name TEXT;       -- nulável, sem default: metadado
```
Aplicação v2: ao inserir/atualizar, grava `name` **e** `full_name` na mesma instrução (mesma linha, mesma transação: atômico); lê `COALESCE(full_name, name)`.
```sql
UPDATE users SET name = $1, full_name = $1 WHERE id = $2;
```

**Fase 2 (backfill).** Job da seção 4 preenche `full_name = name` onde `full_name IS NULL`.

**Fase 3 (verificação).**
```sql
SELECT
  count(*) FILTER (WHERE full_name IS NULL AND name IS NOT NULL)            AS faltando,
  count(*) FILTER (WHERE full_name IS NOT NULL AND full_name IS DISTINCT FROM name) AS divergentes
FROM users;          -- em tabela grande, rode em réplica ou por faixa de id
```
Critério: `faltando = 0` e `divergentes` dentro do limite (zero, se a escrita dupla é atômica).

**Fase 4 (migrate leitura).** Aplicação v3: lê `full_name` por flag; mede divergência com amostragem de comparação.

**Fase 5 (contract escrita).** Aplicação v4: grava só `full_name`. Se algum código ainda escreve `name`, ele deve falhar alto (log de erro) por um ciclo para ser encontrado.

**Fase 6 (limpeza).** Duas migrações separadas, depois da janela:
```sql
-- (a) opcional antes de remover: tornar full_name obrigatório pelo caminho seguro (checklist-postgres.md 4.1)
-- (b) remover a coluna antiga
SET lock_timeout = '5s';
ALTER TABLE users DROP COLUMN name;     -- metadado, ACCESS EXCLUSIVE breve; irreversível sem backup
```
Antes disso: backup lógico de `users(id, name)`.

## 4. Backfill: regras e script

Regras (V-38, brain, V-20):
1. **Lotes pequenos por faixa de PK** (milhares de linhas), uma transação curta por lote: transação longa segura locks e atrasa vacuum e réplica.
2. **Idempotente**: reexecutar não muda o resultado nem dobra efeito (`WHERE full_name IS NULL`).
3. **Não sobrescreve dado mais novo**: se a aplicação já grava o campo novo, o backfill só preenche ausentes; se a transformação se aplica a valores existentes, defina o critério de conflito (timestamp ou versão) explicitamente, em vez de "deduplicar às cegas" como remédio (V-38).
4. **Retomável**: checkpoint do último id processado em arquivo ou tabela de controle.
5. **Observável**: log por lote (faixa, linhas atualizadas, duração); critério de parada (seção 7).
6. **Respeitoso com a produção**: pausa entre lotes; pausa automática se lag de réplica ou espera de locks passar do limite.
7. **Conexão direta**, papel de migração, `lock_timeout` curto e `statement_timeout` por lote.

Script de exemplo (Python 3 + psycopg 3). Roda **apenas onde o usuário decidir**, primeiro em cópia; a skill não o executa.

```python
import os, time
from pathlib import Path
import psycopg

BATCH = 5000                       # ponto de partida (Inferido); ajuste pela duração medida no ensaio
PAUSE_S = 0.2
CHECKPOINT = Path("backfill_users_full_name.ckpt")

def read_ckpt() -> int:
    return int(CHECKPOINT.read_text()) if CHECKPOINT.exists() else 0

dsn = os.environ["MIGRATION_DATABASE_URL"]       # conexão direta; nunca imprimir
last_id = read_ckpt()
with psycopg.connect(dsn, autocommit=True) as conn:   # autocommit: cada execute é uma transação curta
    conn.execute("SET lock_timeout = '2s'")
    conn.execute("SET statement_timeout = '30s'")
    while True:
        upper = conn.execute(
            "SELECT max(id) FROM (SELECT id FROM users WHERE id > %s ORDER BY id LIMIT %s) s",
            (last_id, BATCH),
        ).fetchone()[0]
        if upper is None:
            break
        cur = conn.execute(
            "UPDATE users SET full_name = name "
            "WHERE id > %s AND id <= %s AND full_name IS NULL AND name IS NOT NULL",
            (last_id, upper),
        )
        print(f"ids ({last_id}, {upper}] -> {cur.rowcount} linhas")
        last_id = upper
        CHECKPOINT.write_text(str(last_id))
        time.sleep(PAUSE_S)
```

Lag de réplica (consulta de leitura na primária) para decidir pausas: `SELECT max(extract(epoch FROM replay_lag)) FROM pg_stat_replication;` (coluna `replay_lag` existe a partir do PostgreSQL 10; Inferido). Se acima do limite, durma mais antes do próximo lote.

Validação pós-escrita (V-38; compartilhada com o segmento data-engineering): contagem origem x destino, ausência de NULL/duplicata onde a regra exige, e **rodar duas vezes** para provar idempotência.

## 5. Escrita dupla e reconciliação

- Duas colunas na mesma linha, na mesma instrução: atômico. Sem necessidade de reconciliação além da verificação.
- Duas tabelas ou dois armazenamentos (outra tabela, outro banco, fila, cache): a escrita dupla **não é atômica**; sempre haverá janelas de divergência. Exige: ordem de escrita definida (fonte da verdade primeiro), reconciliação periódica (job que compara e corrige), métrica de divergência, e a decisão do que prevalece (V-20, brain).
- Stripe descreve escrita dupla com fração crescente enquanto monitora métricas, depois troca os caminhos de leitura, depois de escrita, e só então remove os dados antigos (V-20); a infraestrutura de backfill deles (jobs offline em Hadoop) é específica: adapte o princípio, não a ferramenta.
- Triggers que sincronizam as colunas são uma opção (o pgroll usa triggers bidirecionais e views versionadas, V-21: PostgreSQL apenas, custo de triggers e views, ferramenta de terceiros que o usuário avalia). Teste o caso em que as duas colunas mudam na mesma instrução.

## 6. Variantes

| Mudança | Esboço (revisar com `db-migration-planner`) | Atenção |
| --- | --- | --- |
| `int` -> `bigint` em coluna comum | coluna nova `bigint`, escrita dupla, backfill, índices `CONCURRENTLY` na nova, troca de leitura, remoção | PK/FK/sequência exigem passos extras (troca de PK sob lock curto): Inferido, ensaiar |
| Dividir coluna em duas | duas colunas novas, backfill com a função de divisão, validar com amostra | regra de parsing é de negócio: casos de borda no ensaio |
| Mover coluna para outra tabela | tabela nova com FK, escrita dupla, backfill, leitura por JOIN | lag/ordem entre tabelas, reconciliação (seção 5) |
| Remover coluna | só fase 6 após parar de ler/escrever | `SELECT *` em statements preparados pode quebrar; backup lógico antes |
| Trocar engine / particionar tabela existente | migração para tabela particionada nova + backfill + troca | ver P-18 e `migracoes-e-locks.md` (particionamento, V-13) |

## 7. Critério de interrupção

Interrompa a fase e acione o rollback correspondente se qualquer condição ocorrer (valores numéricos definidos no plano, não improvisados):
- lock ou transação esperando acima do orçamento;
- taxa de erro da aplicação acima do limite acordado;
- divergência de contagem/valores acima do limite;
- lag de réplica ou espaço em disco acima do limite;
- backfill sem progresso (taxa de linhas/s abaixo do mínimo) ou reiniciando do começo (checkpoint falhou).

## 8. Revisão em camadas

Três olhares sobre o plano (V-36): primeiro `db-reviewer` (contexto limpo, somente leitura), depois um engenheiro com foco em regra de negócio, depois um colega. Declare que o primeiro é revisão do mesmo modelo, não validação externa.
