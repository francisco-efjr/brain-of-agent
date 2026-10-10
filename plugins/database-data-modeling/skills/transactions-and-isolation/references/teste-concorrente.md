# Teste de concorrência coordenado

Base: brain `dados-e-migracoes.md` (MIT, Brain of Agent: "iniciar duas vendas coordenadas, confirmar no máximo uma aceitação, estoque não negativo... Não usar apenas duas chamadas sequenciais") e V-08/V-09 (comportamento por engine). Código ilustrativo (Python 3, pytest, psycopg 3): adaptar ao stack e executar **somente em banco de teste descartável**, nunca em produção ou réplica compartilhada. Esta skill não executa o teste.

Sumário
1. O que o teste precisa provar
2. Esqueleto com barreira (PostgreSQL)
3. Entrelaçamento determinístico (demonstrar a anomalia)
4. Testar o código real, não uma cópia
5. Outras engines e ORMs
6. Interpretar o resultado

## 1. O que o teste precisa provar

- Concorrência **real**: sessões distintas (conexões distintas) liberadas ao mesmo tempo por uma barreira. Duas chamadas em sequência na mesma conexão não são concorrência.
- Invariante observável: com estoque 1 e N compras de 1, no máximo uma aceita; estoque final >= 0; nenhum erro não tratado.
- Vermelho confirmado: o teste **falha no código atual** e passa no corrigido. Se nunca falha no código ruim, ele não prova nada: aumente threads/rodadas ou adicione ponto de sincronização.
- Repetição: condições de corrida são probabilísticas; rode centenas de rodadas.

## 2. Esqueleto com barreira (PostgreSQL)

Tabela de teste: `items(id int primary key, stock int not null)` **sem** `CHECK (stock >= 0)` quando o objetivo é expor o código ingênuo (com o CHECK o código ruim falha com erro de constraint; também é um resultado válido, só que diferente).

```python
import os, threading
import psycopg
import pytest

DSN = os.environ["TEST_DATABASE_URL"]        # banco de teste descartável; nunca produção

def vender_ingenuo(conn, item_id, qty):      # código ruim: checa e depois escreve
    (stock,) = conn.execute("SELECT stock FROM items WHERE id = %s", (item_id,)).fetchone()
    if stock >= qty:
        conn.execute("UPDATE items SET stock = stock - %s WHERE id = %s", (qty, item_id))
        return True
    return False

def vender_atomico(conn, item_id, qty):      # código corrigido: UPDATE condicional
    cur = conn.execute(
        "UPDATE items SET stock = stock - %s WHERE id = %s AND stock >= %s", (qty, item_id, qty)
    )
    return cur.rowcount == 1

def rodada(vender, n_threads=8, estoque_inicial=1):
    with psycopg.connect(DSN, autocommit=True) as c:
        c.execute("INSERT INTO items (id, stock) VALUES (1, %s) "
                  "ON CONFLICT (id) DO UPDATE SET stock = EXCLUDED.stock", (estoque_inicial,))
    barreira = threading.Barrier(n_threads)
    aceitas, erros = [], []

    def worker():
        try:
            with psycopg.connect(DSN) as conn:        # sai do with = COMMIT (ou ROLLBACK se houver exceção)
                barreira.wait(timeout=10)             # todos disparam juntos
                aceitas.append(vender(conn, 1, 1))
        except Exception as exc:                      # registrar, não engolir
            erros.append(repr(exc))

    ts = [threading.Thread(target=worker) for _ in range(n_threads)]
    for t in ts: t.start()
    for t in ts: t.join()
    with psycopg.connect(DSN, autocommit=True) as c:
        final = c.execute("SELECT stock FROM items WHERE id = 1").fetchone()[0]
    return sum(1 for a in aceitas if a), final, erros

def test_atomico_no_maximo_uma_aceitacao_e_estoque_nao_negativo():
    for _ in range(200):
        aceitas, final, erros = rodada(vender_atomico)
        assert not erros
        assert aceitas <= 1 and final >= 0

@pytest.mark.xfail(reason="demonstra a falha do check-then-act em READ COMMITTED", strict=False)
def test_ingenuo_viola_a_invariante():
    violou = False
    for _ in range(200):
        aceitas, final, _ = rodada(vender_ingenuo)
        if aceitas > 1 or final < 0:
            violou = True
            break
    assert not violou          # esperado falhar (xfail) em READ COMMITTED sob concorrência real
```

Notas:
- `Barrier` libera as threads no mesmo instante; o primeiro `execute` de cada uma competirá de verdade no servidor.
- `autocommit=True` só na conexão de preparação/consulta; nas conexões das threads, a transação implícita dura até o `with` terminar.
- Com `SERIALIZABLE`/`REPEATABLE READ` no PostgreSQL, adicione tratamento de `psycopg.errors.SerializationFailure` e conte as tentativas: o resultado correto é "no máximo uma aceitação, alguns retries", não "zero erros" (V-08).

## 3. Entrelaçamento determinístico (demonstrar a anomalia)

Para mostrar a falha sem depender de sorte, controle a ordem com duas conexões em um único fluxo (ainda são sessões distintas):

```python
a = psycopg.connect(DSN); b = psycopg.connect(DSN)       # duas sessões, transações abertas
(sa,) = a.execute("SELECT stock FROM items WHERE id = 1").fetchone()   # A lê 1
(sb,) = b.execute("SELECT stock FROM items WHERE id = 1").fetchone()   # B lê 1
a.execute("UPDATE items SET stock = stock - 1 WHERE id = 1"); a.commit()
b.execute("UPDATE items SET stock = stock - 1 WHERE id = 1"); b.commit()
# estoque final: -1  (READ COMMITTED; sem CHECK)
```

Serve para ilustrar o antes/depois no relatório. Não substitui o teste da seção 2, porque o UPDATE condicional bloqueia quem chega depois e exige threads para ser exercitado.

## 4. Testar o código real, não uma cópia

- Chame a função de produção (serviço/repositório) a partir das threads, com conexões de um pool de teste. Teste de uma cópia local do SQL não prova o código.
- Se o código real tem janela estreita entre leitura e escrita, crie um **ponto de sincronização injetável** (callback/hook de teste) entre as duas etapas; por exemplo, um parâmetro opcional `antes_de_escrever` que a produção deixa vazio. Em teste, a barreira entra ali e a falha vira determinística.
- ORM em Django: use `TransactionTestCase` (o `TestCase` embrulha tudo numa transação e esconde a concorrência) e feche conexões das threads ao terminar (Inferido; confirmar na versão).
- Isole dados por rodada (ids únicos) ou recrie a linha a cada rodada, para uma rodada não contaminar a seguinte.

## 5. Outras engines e ORMs

| Engine | Adaptação |
| --- | --- |
| MySQL/InnoDB | Mesmo esqueleto com o driver de MySQL; confirme `SELECT @@transaction_isolation`; lembre que o padrão é REPEATABLE READ (V-09): o `SELECT` simples lê o snapshot, o `UPDATE` age sobre o dado atual. Rode também com `FOR UPDATE` para comparar |
| SQL Server | Driver próprio; comparar com RCSI ligado e desligado (V-09); `UPDLOCK` no lugar de `FOR UPDATE` (Inferido) |
| SQLite | Um escritor por vez: o teste costuma mostrar `database is locked` em vez de anomalia; configure `busy_timeout` e trate o erro (sem fonte validada, L-08) |
| MongoDB, DynamoDB, Redis | Sem fonte validada (L-07); o princípio de teste (concorrência real + invariante) vale; use operações atômicas do próprio armazenamento |
| ORMs | Use a API de transação do ORM dentro de cada thread; um `Session`/`EntityManager` por thread |

## 6. Interpretar o resultado

| Observação | Leitura |
| --- | --- |
| Código ingênuo nunca viola em 200 rodadas | Contenção insuficiente ou janela curta demais: aumente threads/rodadas ou use o ponto de sincronização; sem violação reproduzida, não afirme que "não há bug" (Suposição) |
| Código corrigido viola uma vez | Correção insuficiente ou invariante mal expressa; não aceite como "flaky" |
| Muitos `40001` no corrigido com SERIALIZABLE | Esperado; meça a taxa e ajuste o retry (V-08) |
| `deadlock detected` | Ordem de locks inconsistente: padronize (ver `correcoes-e-retry.md`, seção 2) |
| Timeout na barreira | Alguma thread falhou antes de chegar: leia `erros` |

Relate sempre: engine/versão/nível, número de threads e rodadas, taxa de violações e de retries, e quem executou. Se o usuário ainda não rodou, escreva "teste proposto, não executado".
