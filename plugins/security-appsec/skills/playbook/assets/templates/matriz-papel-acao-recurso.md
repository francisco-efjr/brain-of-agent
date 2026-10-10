# Matriz papel × ação × recurso

Modelo para `access-control-review` e para testes de autorização (brain QA, Inferido; V-18). Monte com o dono do produto. Cada célula preenchida vira um caso de teste parametrizado. O esperado usa 401 (sem sessão), 403 ou 404 (negado; escolha um e seja consistente) e 200 (permitido). Teste de negação relê o recurso depois da tentativa.

## Massa mínima de teste

- Tenant A: usuário A1 (dono do recurso) e usuário A2 (mesmo tenant, sem relação com o recurso).
- Tenant B: usuário B1.
- Suporte S1 (cruza tenants por desenho, com auditoria) e Admin do tenant A (AdA).
- Dados sintéticos, ambiente próprio, autorização escrita se não for do time.

## Matriz

| Recurso / Ação | Anônimo | Dono (A1) | Outro usuário, mesmo tenant (A2) | Outro tenant (B1) | Suporte (S1) | Admin do tenant (AdA) |
| --- | --- | --- | --- | --- | --- | --- |
| pedido / ver | 401 | 200 | 404 | 404 | 200 (leitura) | 200 |
| pedido / alterar | 401 | 200 | 404 | 404 | 403 | 200 |
| pedido / cancelar | 401 | 200 | 404 | 404 | 403 | 200 |
| tenant / exportar pedidos | 401 | 403 | 403 | 403 | 403 | 200 só do próprio tenant |
| usuário / alterar papel | 401 | 403 | 403 | 403 | 403 | 200, exceto promover a si mesmo |

Os valores acima são o exemplo do brain QA; troque pela regra real do produto. Linhas adicionais: sub-recursos (`/pedidos/{id}/nota-fiscal`), downloads, exportações, filtros (`?clienteId=`), lotes, GraphQL, WebSocket.

## Casos derivados (por célula negada)

1. Identificador do recurso de outro usuário nas posições: caminho, query, corpo, cabeçalho.
2. Troca de método (GET para DELETE) em rota administrativa.
3. Mass assignment: enviar `papel`, `tenant_id`, `status` e reler.
4. Após DELETE ou PATCH negado, o recurso permanece intacto (releitura pelo dono).
5. Lista com filtro: o conteúdo da lista não contém itens de outro tenant (asserte o conteúdo, não só o status).

## Resultado

| Caso | Esperado | Obtido | Evidência (arquivo:linha ou saída) | Veredito (OK, VULN, VERIFY, não avaliado) |
| --- | --- | --- | --- | --- |
| <caso> | <status e releitura> | <preencher após execução> | <...> | <...> |

Status de execução: <lido no código | executado em homologação própria>. Sem execução, o veredito é "estático" e o teste fica como proposta.
