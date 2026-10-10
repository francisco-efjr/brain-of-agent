# Autorização por objeto, função, propriedade e tenant

Base da skill `access-control-review`. Fontes: V-18 (OWASP Authorization Cheat Sheet, CC BY-SA 4.0, destilado), V-15 (API1, API3, API5), V-13 (A01), brain QA e fullstack (Inferido). O tratamento de tenant é Inferido: a página OWASP lida não tem seção dedicada a multi-tenant e menciona só que RBAC serve mal e que ABAC/ReBAC ajudam.

## Sumário

1. Princípios
2. Checklist de revisão (6 itens de V-18 e extensões)
3. Matriz papel por ação por recurso
4. Onde trocar IDs
5. BOLA, BOPLA e BFLA
6. Tenant
7. 403 ou 404
8. Mass assignment
9. Testes de negação
10. Roteiro de revisão por rota
11. Exemplo

## 1. Princípios

- Autenticação não é autorização: saber quem é não diz o que pode fazer. Exemplo do brain: `GET /documentos/123` exige token válido, mas busca por ID sem tenant; qualquer usuário autenticado lê documento de outro cliente.
- Negar por padrão e justificar cada permissão (V-18).
- Verificar em toda requisição, inclusive AJAX, de forma global (filtro ou middleware), para que uma rota nova não nasça sem checagem.
- IDOR: checar acesso ao objeto específico; checar o tipo do objeto não basta. Referências indiretas por usuário ou sessão ajudam.
- O cliente nunca decide: papel, tenant, dono e preço não vêm do corpo ou do cabeçalho como autoridade.
- ABAC/ReBAC são preferíveis a RBAC em cenários grandes ou multi-tenant (V-18).
- Falha de autorização termina em estado seguro e é registrada sem expor detalhe ao cliente.

## 2. Checklist de revisão

- [ ] Cada rota ou ação checa autorização no servidor antes de qualquer leitura.
- [ ] A checagem é por objeto, não só por tipo de objeto.
- [ ] O identificador do objeto é derivado da sessão ou validado contra ela.
- [ ] Em código multi-tenant, toda consulta filtra pelo tenant (Inferido).
- [ ] Há teste que prova negação entre usuários e entre tenants.
- [ ] Falha de autorização termina em estado seguro e é registrada sem expor detalhe ao cliente.
- [ ] Extensões (brain, Inferido): cache, fila, export, busca e relatório também levam o tenant; função administrativa não acessível por troca de método; campos protegidos não graváveis.

## 3. Matriz papel por ação por recurso

Monte com o dono do produto; cada célula vira um caso de teste (template em `assets/templates/matriz-papel-acao-recurso.md`). Exemplo (brain QA, Inferido):

| Ação | Anônimo | Dono | Outro usuário (mesmo tenant) | Outro tenant | Suporte | Admin do tenant |
| --- | --- | --- | --- | --- | --- | --- |
| Ver pedido | 401 | 200 | 404 | 404 | 200 (leitura) | 200 |
| Cancelar pedido pendente | 401 | 200 | 404 | 404 | 403 | 200 |
| Exportar pedidos do tenant | 401 | 403 | 403 | 403 | 403 | 200, só do próprio tenant |
| Alterar papel de usuário | 401 | 403 | 403 | 403 | 403 | 200, exceto promover a si mesmo |

Massa mínima de teste: dois usuários no tenant A, um no tenant B e um admin. SaaS sem teste entre tenants carrega o maior risco sem verificação.

## 4. Onde trocar IDs

Caminho, query, corpo, cabeçalho, sub-recursos (`/pedidos/{id}/nota-fiscal`), downloads, exportações, filtros (`?clienteId=`), lotes, GraphQL e WebSocket. Em revisão de código, procure cada um destes pontos de entrada, não só as rotas REST principais.

## 5. BOLA, BOPLA e BFLA (API Top 10 2023)

- **API1 BOLA** (nível de objeto): usuário B usa o ID de um objeto de A em GET, PUT, PATCH, DELETE e sub-recursos. Esperado: 403 ou 404, nada de A no corpo, objeto intacto.
- **API3 BOPLA** (nível de propriedade): leitura traz campo que o papel não deveria ver (hash, documento completo, campo interno); escrita altera campo protegido (`papel`, `saldo`, `tenant_id`, `status`). Esperado: campo ausente; escrita ignorada ou 400/422.
- **API5 BFLA** (nível de função): usuário comum chama rota administrativa; troca de método (GET para DELETE). Esperado: 403. Esconder o botão não protege a rota: teste a API, não a tela.

## 6. Tenant

Todo código multi-tenant segue estas regras (Inferido de IDOR mais ABAC):

1. O tenant vem da sessão, nunca do cliente. Se a rota recebe `tenant_id`, valide-o contra o da sessão e prefira não recebê-lo.
2. Toda consulta filtra por tenant: no código de acesso a dados, num escopo padrão do ORM, ou por política do banco (RLS é feature do banco; o plugin `/database-data-modeling:playbook` trata). Revise as consultas de exceção (`raw`, `unscoped`, `IgnoreQueryFilters`) uma a uma.
3. Cache, fila, tarefa agendada, export, busca e relatório: o tenant faz parte da chave ou do payload verificado. Um cache global por ID de objeto vaza entre tenants.
4. Identificadores previsíveis ou globais (autoincremento) tornam o IDOR mais barato, mas UUID não é controle.
5. Suporte e administração interna: papel de suporte cruza tenants por desenho; exija auditoria e escopo mínimo.
6. Teste de negação entre tenants é obrigatório; sem ele, "isolamento" é Suposição.

## 7. 403 ou 404

Qualquer um serve se for consistente: 404 não revela que o recurso existe. Inaceitável é 200, inclusive 200 com lista vazia quando a regra deveria ser negação e o filtro é a única proteção: asserte sobre o conteúdo e, após um DELETE negado, confirme que o recurso ainda existe. Mensagens de erro não devem revelar existência sensível sem necessidade.

## 8. Mass assignment

Detecção: `Model(**request.json)`, `update(request.body)`, `Object.assign(user, req.body)`, `@RequestBody` ligado direto à entidade. Correção: lista de campos graváveis por papel; DTO de entrada. Teste: envie campos extras (`papel`, `tenant_id`, `status`) e releia o recurso; o status 200 não prova nada, o estado relido prova.

## 9. Testes de negação

Sentinelas: o teste relê o recurso depois da tentativa e afirma que não mudou; não confia no status HTTP. Esboço (pytest; ilustrativo, não executado; ajuste rotas e campos ao contrato; baseado no brain QA):

```python
@pytest.mark.parametrize("metodo, corpo", [("GET", None), ("PATCH", {"descricao": "alterado por B"}), ("DELETE", None)])
def test_outro_tenant_nao_acessa_pedido_alheio(base_url, usuario_a, usuario_b, pedido_de_a, metodo, corpo):
    url = f"{base_url}/api/pedidos/{pedido_de_a['id']}"
    r = usuario_b.request(metodo, url, json=corpo, timeout=10)
    assert r.status_code in (403, 404)
    assert pedido_de_a["descricao"] not in r.text            # nada vaza no corpo do erro
    atual = usuario_a.get(url, timeout=10)                    # o efeito é o que importa
    assert atual.status_code == 200 and atual.json()["descricao"] == pedido_de_a["descricao"]
```

Testes de massa: `test_cliente_nao_se_promove_por_campo_extra` envia `papel: admin` e `tenant_id: outro` e relê o perfil. Execução ativa só em ambiente próprio com dados sintéticos.

## 10. Roteiro de revisão por rota

Para cada rota, handler, consulta, fila ou export no escopo, preencha:

| Campo | Pergunta |
| --- | --- |
| Rota | método e caminho |
| Checagem no servidor | existe antes da leitura? global ou por rota? |
| Por objeto | busca já escopada ao dono? |
| Tenant | consulta e cache filtram pelo tenant da sessão? |
| Campos | resposta e escrita respeitam o papel? |
| Veredito | OK, achado (VULN), VERIFY ou não avaliada |

## 11. Exemplo

Entrada: duas views Django que listam faturas por status; `list` filtra por `status` e `get(pk=pk)` sem `org_id`.
Saída esperada: VULN-001 A01/API1 em `invoices/views.py` (lista sem filtro de tenant; Alta, estático suportado); VULN-002 (`get(pk=)` sem escopo); correção: `Invoice.objects.filter(org_id=request.user.org_id, ...)` ou manager escopado; teste de negação entre tenants que relê a fatura. Rótulo: tenant como categoria dedicada é Inferido de IDOR mais ABAC. Não diga "seguro porque há login".
