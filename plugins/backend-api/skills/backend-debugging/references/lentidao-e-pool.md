# Lentidão, N+1 e pool de conexões: medir antes de mudar

Conhecimento estável do domínio (sem fonte V específica: **Inferido**) somado à regra de V-25 (evidência antes de correção) e de V-04 (verificação executável). Confira APIs na versão instalada de cada biblioteca. Índice, plano de execução e tuning de banco pertencem a `database-data-modeling`; aqui você prova **onde** está o custo.

## Sumário

1. Medidas mínimas
2. Contador de consultas e teste de N+1
3. Pool de conexões
4. Causas frequentes e prova de cada uma
5. Prova do ganho

## 1. Medidas mínimas

Sem estas quatro medidas não se otimiza nada:

| Medida | Como obter | Pergunta que responde |
| --- | --- | --- |
| Tempo por requisição (p50, p95 se houver) | log estruturado do framework, middleware de tempo | é lento sempre ou só na cauda? |
| Consultas por requisição | contador (seção 2) ou log de SQL em ambiente local | o tempo vem de muitas consultas pequenas? |
| Tempo em dependência externa | timer em volta de cada chamada HTTP/gRPC | o gargalo está fora do seu código? |
| Uso do pool de conexões | métricas do pool; `pg_stat_activity` em banco de teste | requisições esperam por conexão? |

Meça no ambiente local ou de teste, com a **mesma carga** antes e depois. Gerar carga contra ambiente compartilhado exige autorização.

## 2. Contador de consultas e teste de N+1

N+1: uma consulta para a lista e uma por item (lazy loading, resolver GraphQL sem DataLoader, laço que consulta dentro). Prova por contagem: a mesma rota com 1 e com 50 itens deve executar praticamente o mesmo número de consultas.

SQLAlchemy (confira a versão instalada):

```python
from contextlib import contextmanager
from sqlalchemy import event

@contextmanager
def contar_consultas(engine):
    contagem = {"n": 0}
    def antes(conn, cursor, statement, parameters, context, executemany):
        contagem["n"] += 1
    event.listen(engine, "before_cursor_execute", antes)
    try:
        yield contagem
    finally:
        event.remove(engine, "before_cursor_execute", antes)

def test_listagem_nao_tem_n_mais_1(cliente, engine, criar_pedidos):
    criar_pedidos(1)
    with contar_consultas(engine) as c1:
        cliente.get("/pedidos")
    criar_pedidos(49)
    with contar_consultas(engine) as c50:
        cliente.get("/pedidos?page_size=50")
    assert c50["n"] <= c1["n"] + 1, f"consultas cresceram: {c1['n']} -> {c50['n']}"
```

Outras stacks: Django `django.test.utils.CaptureQueriesContext` / `assertNumQueries`; Hibernate/JPA estatísticas (`hibernate.generate_statistics`) ou datasource proxy; Prisma log de queries; EF Core logging de comandos; Go `database/sql` com wrapper de driver. A ferramenta muda, a lógica (1 item x 50 itens) não.

Correções típicas (escolha pela causa provada): carregamento antecipado (`selectinload`/`joinedload`, `select_related`/`prefetch_related`, `include`), consulta em lote por `IN`, DataLoader no GraphQL, projeção só dos campos usados, paginação.

## 3. Pool de conexões

Regra aritmética: `processos x (pool_size + max_overflow)` não pode ultrapassar `max_connections` do banco (menos as reservadas). Cada engine/pool novo cria seu próprio pool: **engine por requisição** é bug clássico.

```python
# errado: pool novo por chamada, conexão nunca devolvida
def get_db():
    return create_engine(DB_URL).connect()

# certo: um engine por processo; sessão por requisição, sempre devolvida
engine = create_engine(DB_URL, pool_size=10, max_overflow=5, pool_timeout=10, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    with SessionLocal() as sessao:
        yield sessao
```

Outras stacks: Node `pg.Pool` com `max` e `pool.query` (ou `client.release()` em `finally`); Go `db.SetMaxOpenConns`, `SetMaxIdleConns`, `SetConnMaxLifetime` e sempre fechar `rows`; Spring HikariCP `maximumPoolSize` e `connectionTimeout`; .NET reutilizar `DbContext` por escopo e não criar conexão por laço. Valores concretos dependem da carga e do banco: calcule, meça e documente.

Sinal de esgotamento: erro de "too many connections"/"remaining connection slots", requisições presas em `pool_timeout`, latência que cresce com a concorrência mas não com a CPU.

## 4. Causas frequentes e prova de cada uma

| Sintoma | Hipótese | Prova mínima |
| --- | --- | --- |
| 500 só sob carga, erro de conexões | pool/engine por requisição, conexão vazando | contar conexões ativas após N requisições; deve ficar constante |
| Lista lenta e cresce com o tamanho | N+1 | contador de consultas 1 x 50 |
| Lento só em produção | dado maior, índice ausente, plano diferente | `EXPLAIN` em cópia de teste com volume realista (delegar a `database-data-modeling`) |
| Cauda longa (p99 alto, p50 normal) | dependência externa lenta, lock, GC, cold start | timers por salto; logs com request id |
| Timeout intermitente após deploy | pool menor, timeout por salto mal dividido, DNS | comparar configuração antes/depois; orçamento de timeout por salto |
| Lento com muitos itens por resposta | serialização, resposta sem paginação | tamanho da resposta e tempo de serialização; paginar |
| Resposta inconsistente entre instâncias | cache local por processo ou relógio | versão/hora por instância; chave de cache com escopo |

## 5. Prova do ganho

Repita a mesma medida, mesma carga, mesmo ambiente: tabela antes x depois (tempo, consultas, conexões). Sem número, o relatório diz "ganho não medido". Um teste de regressão fixa o comportamento (contador de consultas constante, conexões constantes). Não use tetos de latência apertados em teste funcional (intermitência); percentis ficam no teste de performance (`qa-testing`).
