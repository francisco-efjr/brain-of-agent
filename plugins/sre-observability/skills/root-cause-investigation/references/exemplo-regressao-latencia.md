# Exemplo: p95 de `GET /search` foi de 180 ms para 900 ms depois do deploy

Cenário fictício. O usuário propõe subir o timeout do cliente de 1 s para 3 s. Rótulos: Verificado = visto na saída colada; Inferido = dedução.

## Entrada

Diff do deploy (trecho) e `service.py`:

```python
def search(q):
    items = db.query("SELECT id FROM products WHERE name ILIKE %s LIMIT 50", [f"%{q}%"])
    result = []
    for item in items:                       # introduzido no deploy de ontem
        detail = db.query("SELECT * FROM product_detail WHERE product_id = %s", [item.id])
        result.append(merge(item, detail))
    return result
```

## Por que não subir o timeout

Timeout maior não encurta a consulta: segura conexões por mais tempo, aumenta a fila e, com retries no cliente, multiplica a carga sobre o banco (V-22). A lentidão passa a parecer "dentro do limite" e a regressão fica escondida.

## Passos aplicados

1. **Reproduzir.** Com um ambiente local ou de staging e 50 resultados, cole o comando e a saída. Exemplo de medição determinística (sintaxe do contador depende da stack; aqui, log de consultas do ORM ou `pg_stat_statements`, Inferido):

   ```text
   GET /search?q=notebook  ->  consultas SQL por requisição: 51  (esperado antes do deploy: 1)
   ```
2. **Mudanças.** `git diff v2.40.0..v2.41.0 -- service.py` mostra o laço novo. Outras mudanças do deploy (dependências, config) listadas e descartadas ou mantidas.
3. **Comparar com o caso que funciona.** Trace da v2.40.0: 1 span SQL; trace da v2.41.0: 51 spans SQL quase iguais (padrão N+1). Verificado se o trace foi colado; senão Inferido.
4. **Hipótese única.** "O laço faz uma consulta por item (N+1) e a latência cresce com o tamanho da lista." Teste mínimo: reduzir `LIMIT` de 50 para 5 e medir; a latência deve cair quase proporcionalmente (previsão refutável).
5. **Teste que falha antes.**

   ```python
   def test_search_usa_uma_consulta(db_counter):
       with db_counter() as c:
           search("notebook")
       assert c.count <= 2   # falha hoje (51), passa depois do JOIN ou do IN em lote
   ```
6. **Correção mínima.** Uma consulta com `JOIN` (ou `WHERE product_id = ANY(%s)`), mantendo a ordem e o limite. Rodar a suíte e repetir a medição de latência no mesmo volume.
7. **Prevenção.** Gate determinístico de número de consultas por requisição no CI; alerta de latência por burn rate (`alert-review`).

## Saída esperada (resumo)

- Causa raiz: N+1 introduzido no deploy (Verificado se contagem e diff foram colados).
- Correção: arquivo e diff; teste que falhava com 51 consultas e passa com 1.
- Não verificado: efeito em produção sob o tráfego real; confirmar com percentis do mesmo horário depois do deploy da correção.
- Resposta ao pedido original: subir o timeout não é recomendado e foi explicado.
