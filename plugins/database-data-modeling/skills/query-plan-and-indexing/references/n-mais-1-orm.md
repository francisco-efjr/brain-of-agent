# N+1 em ORM: detectar e corrigir

Conhecimento estável do domínio (Inferido), sem item V-nn dedicado nesta base; a necessidade de medir antes de afirmar ganho vem de V-31 e V-07. Nomes de API conferidos de memória: **confirme na doc da versão do ORM instalada** antes de aplicar. Caso de eval relacionado: E-14.

Sumário
1. O que é e como reconhecer
2. Como contar consultas por requisição
3. Correções por ORM
4. Quando JOIN, quando carga em lote
5. Verificação antes/depois

## 1. O que é e como reconhecer

N+1: uma consulta carrega N linhas e, para cada uma, o código dispara outra consulta (acesso a relação "preguiçosa"). Sinais no código:

```python
# Django: 1 consulta para pedidos + N para o cliente de cada um
for order in Order.objects.filter(status="paid"):
    print(order.customer.name)          # acesso à FK dentro do loop
```

Sinais no log: dezenas de `SELECT ... WHERE id = ?` idênticas, apenas com ids diferentes, dentro da mesma requisição. No plano de uma consulta isolada nada parece errado; o problema aparece no **número** de round trips.

## 2. Como contar consultas por requisição

Ative o log de SQL do ORM **em ambiente de desenvolvimento/teste** e conte por requisição (nomes a conferir na versão):

| ORM | Como logar SQL |
| --- | --- |
| Django | logger `django.db.backends` em nível DEBUG (com `DEBUG=True`), ou `connection.queries` em teste; `assertNumQueries` em testes |
| SQLAlchemy | `create_engine(..., echo=True)` ou eventos `before_cursor_execute` |
| Rails (ActiveRecord) | log de desenvolvimento já mostra as consultas; gem de detecção como Bullet (terceiros, avaliar antes) |
| Prisma | opção `log: ['query']` no `PrismaClient` |
| TypeORM | `logging: true` (ou `['query']`) no `DataSource` |
| Entity Framework Core | `LogTo(...)` no `DbContextOptionsBuilder` |
| Hibernate/JPA | propriedade `hibernate.show_sql` / log de `org.hibernate.SQL` |

Peça ao usuário: "rode a requisição lenta com o log de SQL ligado e cole as consultas (sem dados pessoais)". Se não puder, o rótulo é Suposição.

## 3. Correções por ORM

Objetivo: trocar N consultas por 1 ou 2.

| ORM | Relação N-para-1 (FK) | Relação 1-para-N / N-para-N |
| --- | --- | --- |
| Django | `select_related("customer")` (JOIN) | `prefetch_related("items")` (2 consultas, `IN`) |
| SQLAlchemy | `joinedload(Order.customer)` | `selectinload(Order.items)` |
| Rails | `includes(:customer)` / `eager_load` | `includes(:items)` / `preload` |
| Prisma | `include: { customer: true }` | `include: { items: true }` |
| TypeORM | `relations: ["customer"]` ou `leftJoinAndSelect` | `relations: ["items"]` ou `leftJoinAndSelect` |
| Entity Framework Core | `.Include(o => o.Customer)` | `.Include(o => o.Items)` (considere `AsSplitQuery()` para evitar explosão cartesiana, conferir) |
| Hibernate/JPA | `JOIN FETCH` / `@EntityGraph` | `@BatchSize` ou `JOIN FETCH` com cuidado de paginação |

Carga em lote manual (qualquer stack): coletar os ids, uma consulta `WHERE id = ANY($1)` (PostgreSQL) ou `IN (...)` parametrizado, montar um mapa id -> linha e juntar em memória.

## 4. Quando JOIN, quando carga em lote

- **JOIN** (uma consulta): relação N-para-1 ou 1-para-1; poucas colunas; cuidado com multiplicação de linhas em 1-para-N (resultado cartesiano).
- **Carga em lote** (2 consultas): 1-para-N com muitos filhos; evita repetir colunas do pai em cada filho.
- **Paginação + 1-para-N + JOIN**: o `LIMIT` incide sobre linhas multiplicadas, não sobre pais; pagine os pais primeiro e carregue os filhos em lote depois.
- Eager loading de relação que a tela não usa piora o desempenho: carregue só o necessário.

## 5. Verificação antes/depois

1. Antes: número de consultas por requisição e tempo total (do usuário). Rótulo Verificado se colado; senão Suposição.
2. Aplique a correção.
3. Depois: mesmas medições. Registre no relatório (template `relatorio-explain`).
4. Teste automatizado que fixa o limite (`assertNumQueries` no Django; contadores de consulta em outros ORMs) evita regressão.
5. Se, depois da correção, as consultas restantes ainda forem lentas, volte ao fluxo de plano (`ler-plano-postgres.md`).
