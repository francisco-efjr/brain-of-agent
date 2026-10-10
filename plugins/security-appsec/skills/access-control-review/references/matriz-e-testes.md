# Matriz papel x ação x recurso, padrões de busca e testes de negação

Fontes: OWASP Authorization Cheat Sheet (CC BY-SA 4.0, V-18) e API Security Top 10 2023 (V-15), em redação própria; matriz e teste de negação adaptados do brain-of-agent QA (`brains/qa/references/seguranca.md`, MIT, conteúdo próprio do usuário; os exemplos de teste "não foram executados" lá e continuam não executados aqui). Padrões de busca por framework são conhecimento estável (Inferido): confirme a sintaxe na versão do projeto. Conferido em 2026-10-10.

## Sumário

1. Padrões de busca por framework
2. Matriz papel x ação x recurso
3. Onde trocar identificadores
4. Teste de negação (exemplo)
5. Mass assignment: teste
6. GraphQL, WebSocket, exports, jobs
7. Respostas: 403, 404 e lista vazia

## 1. Padrões de busca por framework (candidatos, não achados)

| Framework | Busca por objeto sem dono/tenant (candidato) | Onde procurar a checagem |
| --- | --- | --- |
| Django / DRF | `objects.get\(pk=`, `get_object_or_404\(\w+, pk=` sem `org_id=`/`owner=`; `queryset = \w+\.objects\.all\(\)` | `permission_classes`, `get_queryset`, `has_object_permission`, mixins |
| Flask / SQLAlchemy | `\.query\.get\(`, `filter_by\(id=` sem `user_id`/`org_id` | decoradores (`login_required`, `roles_required`), `before_request` |
| Express / Node | `findById\(req\.params`, `findOne\(\{ ?_?id: ?req\.`, `where: \{ id: req\.params` sem `tenantId` | middlewares `app.use`, `router.use`, guards, `casl`/`accesscontrol` |
| NestJS | `findOne\(id\)` em serviço chamado por controller sem `@UseGuards` | `@UseGuards`, `@Roles`, políticas, interceptors |
| Rails | `\.find\(params\[:id\]\)` em vez de `current_user\.\w+\.find` | `before_action`, Pundit (`authorize`), CanCanCan (`load_and_authorize_resource`) |
| Spring | `findById\(` em controller sem `@PreAuthorize` | `@PreAuthorize`, `SecurityFilterChain`, `@PostAuthorize` |
| Laravel | `Model::find\(\$id\)`, `findOrFail\(\$id\)` sem escopo | Policies (`authorize`), Gates, global scopes |
| ASP.NET | `FindAsync\(id\)` em action sem `[Authorize]` | `[Authorize(Policy=...)]`, handlers de requisito, filtros |
| GraphQL | resolvers que buscam por `args.id` | diretivas/middleware por campo, `context.user` |

Sinais gerais de ausência: rota sem decorador que as vizinhas têm; `AllowAny`, `permitAll`, `@Public`, `skipAuth`, `csrf_exempt` em rota que lê ou altera dado de usuário; lista de exceções do middleware global (`publicRoutes`, `excludePaths`) que cresceu no diff.

## 2. Matriz papel x ação x recurso

Preencha com o esperado, a partir da regra de negócio (pergunte ao dono do produto o que não estiver claro; célula sem regra é Suposição). Exemplo do brain-of-agent QA, adaptado:

| Ação | Anônimo | Dono | Outro usuário (mesmo tenant) | Outro tenant | Suporte | Admin do tenant |
| --- | --- | --- | --- | --- | --- | --- |
| Ver pedido | 401 | 200 | 404 | 404 | 200 (leitura) | 200 |
| Cancelar pedido pendente | 401 | 200 | 404 | 404 | 403 | 200 |
| Exportar pedidos do tenant | 401 | 403 | 403 | 403 | 403 | 200, só do próprio tenant |
| Alterar papel de usuário | 401 | 403 | 403 | 403 | 403 | 200, exceto promover a si mesmo |

Massa mínima para testar: dois usuários no tenant A, um no tenant B e um admin. SaaS sem teste entre tenants carrega seu maior risco sem verificação.

## 3. Onde trocar identificadores

Caminho, query, corpo, cabeçalhos, sub-recursos (`/pedidos/{id}/nota-fiscal`), downloads, exportações, filtros (`?clienteId=`), operações em lote (lista de IDs: um ID alheio na lista), GraphQL (argumentos e campos aninhados) e mensagens WebSocket. Em revisão estática, procure cada um desses pontos no código e confirme que o ID passa pela mesma checagem.

## 4. Teste de negação (exemplo)

pytest + requests contra homologação, contas sintéticas, credenciais do ambiente. Adaptado de brain-of-agent QA (MIT). Não executado; ajuste rotas e campos ao contrato.

```python
import pytest

@pytest.mark.parametrize("metodo, corpo", [("GET", None), ("PATCH", {"descricao": "alterado por B"}), ("DELETE", None)])
def test_outro_tenant_nao_acessa_pedido_alheio(base_url, usuario_a, usuario_b, pedido_de_a, metodo, corpo):
    url = f"{base_url}/api/pedidos/{pedido_de_a['id']}"
    r = usuario_b.request(metodo, url, json=corpo, timeout=10)
    assert r.status_code in (403, 404), f"{metodo} devolveu {r.status_code}"
    assert pedido_de_a["descricao"] not in r.text      # nada vaza no corpo do erro
    atual = usuario_a.get(url, timeout=10)             # o efeito é o que importa
    assert atual.status_code == 200 and atual.json()["descricao"] == pedido_de_a["descricao"]
```

As fixtures (`usuario_a` no tenant A, `usuario_b` no tenant B, `pedido_de_a` criado e removido pelo teste) vêm de variáveis de ambiente do ambiente de teste; nunca grave credenciais no repositório. O que esse teste prova: o outro tenant é negado em três métodos, a resposta não vaza o conteúdo e o objeto de A permanece intacto.

## 5. Mass assignment: teste

Envie campos extras e releia o recurso; o status 200 não prova nada, o estado relido prova.

```python
def test_cliente_nao_se_promove_por_campo_extra(base_url, usuario_a):
    usuario_a.patch(f"{base_url}/api/usuarios/me", timeout=10,
                    json={"nome": "Ana Teste", "papel": "admin", "tenant_id": "outro"})
    eu = usuario_a.get(f"{base_url}/api/usuarios/me", timeout=10).json()
    assert eu["papel"] == "cliente" and eu["tenant_id"] != "outro"
```

Correção típica (para o `propose-patch`): lista de campos aceitos por rota (allowlist) e esquema separado para entrada e saída.

## 6. GraphQL, WebSocket, exports, jobs

- GraphQL: autorização por campo e por objeto no resolver; consultas aninhadas (`user { orders { customer } }`) cruzam donos; profundidade e custo limitados; introspecção em produção é decisão consciente.
- WebSocket: a autorização acontece no handshake e também em cada mensagem que referencia um recurso; canal por tenant/objeto não é escolhido só pelo cliente.
- Exports e relatórios: rodam com o escopo do solicitante, não do job; arquivo gerado fica em caminho não adivinhável E exige autorização para baixar; link assinado tem expiração curta.
- Jobs e filas: o payload carrega o tenant e o executor o reaplica; um job não "esquece" o filtro porque roda fora da requisição.
- Cache: a chave inclui tenant e usuário (ou papel) quando a resposta depende deles.

## 7. Respostas: 403, 404 e lista vazia

- 403 e 404 são ambos aceitáveis se consistentes: 404 não revela que o recurso existe. 200 com dado alheio nunca é.
- Lista vazia por filtro automático por tenant é aceitável se o filtro é a regra declarada; um teste deve provar que o dado do outro tenant existe e não aparece.
- Após um DELETE negado, confirme que o recurso ainda existe.
- Falha de autorização: mensagem genérica ao cliente; detalhe (usuário, recurso, regra) no log do servidor, sem dados sensíveis.
