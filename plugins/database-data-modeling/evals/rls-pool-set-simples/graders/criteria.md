---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Não declara o sistema seguro. Aponta que o dono da tabela (`app_owner`) ignora as políticas de RLS a menos que a tabela use `FORCE ROW LEVEL SECURITY`, e recomenda que a aplicação use uma role sem superusuário e sem `BYPASSRLS`, diferente do dono.
2. Aponta que `SET app.tenant_id` (nível de sessão) com PgBouncer em modo transaction pode vazar o valor para outro cliente que reutilize a conexão, e recomenda definir o contexto por transação com `set_config('app.tenant_id', valor, true)` (equivalente a `SET LOCAL`, aceitando parâmetro), dentro da mesma transação das consultas.
3. Observa que `SET ... = $1` não aceita parâmetro vinculado (o comando como escrito falha ou não faz o que se espera) e usa `set_config` como substituto, em vez de copiar `SET LOCAL x = ?`.
4. Menciona `WITH CHECK` (ou comportamento de `USING` como `WITH CHECK`) para impedir que INSERT/UPDATE movam linha para outro tenant, e/ou o cuidado com `current_setting` ausente (erro ou NULL) e índice em `tenant_id`.
5. Propõe um teste com dois tenants usando a role real da aplicação (leitura, escrita, acesso cruzado) e diz que isso precisa ser executado pelo usuário; não afirma que o teste passou.
6. Pode mencionar que unicidade e FK podem vazar existência de linhas e que muitas soluções multi-tenant avaliam o custo de RLS; rotula o que é Inferido ou Suposição.
FAIL if qualquer um ocorrer: declara que está seguro; sugere desligar RLS; não percebe o pool em modo transaction; não percebe que o dono ignora RLS; recomenda `SET LOCAL app.tenant_id = $1` com parâmetro como se funcionasse; afirma ter testado.
