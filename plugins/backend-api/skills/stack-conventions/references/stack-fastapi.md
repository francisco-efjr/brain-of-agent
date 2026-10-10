# FastAPI: checklist, padrões e verificação por busca

Fontes (Verificado em 2026-10-10 salvo indicação): FastAPI tutorial de segurança e `response_model` (V-21, https://fastapi.tiangolo.com/tutorial/security/first-steps/ e .../response-model/); skill `fastapi-patterns` de everything-claude-code (V-29, MIT, destilada); regras de camadas do awesome-cursorrules (V-23, CC0, destiladas; sem texto literal); OWASP (V-09, V-10). Código abaixo é redação própria. **Confirme a versão instalada de FastAPI, Starlette, Pydantic e SQLAlchemy** antes de aplicar (`pip show fastapi pydantic sqlalchemy`); nomes e tipos de erro de validação mudam entre versões maiores.

## Sumário

1. Checklist
2. Estrutura e camadas
3. Autenticação que valida de verdade
4. Erros em RFC 9457
5. Modelos de entrada e saída
6. Serviço, unicidade e idempotência
7. Paginação por cursor
8. Testes
9. Verificação por busca
10. Lacunas

## 1. Checklist

- [ ] Camadas Router → Service → Repository → ORM/HTTP, importando só para baixo (V-23).
- [ ] Router sem importar `sqlalchemy`, `httpx`, `boto3` nem `models`/`repositories`; handler curto, sem regra de negócio.
- [ ] Service depende de `Protocol`s (portas) e não importa `request`/`response` do framework.
- [ ] `response_model` em **todo** endpoint; modelos de entrada e de saída separados (`UserIn`/`UserOut`). `response_model_include/exclude` **não** alteram o schema do OpenAPI (V-21): prefira classes separadas.
- [ ] `user_id`/`tenant_id` vem da dependência de autenticação e filtra **toda** consulta; nunca do corpo (V-23).
- [ ] A dependência de auth **valida** o token (algoritmo, `iss`, `aud`, `exp`); o tutorial só extrai o header (V-21).
- [ ] Exceção de domínio no service; o router (ou handler global) traduz para o status da tabela do projeto; corpo `application/problem+json`.
- [ ] Restrição única no banco; `IntegrityError` com `rollback` e erro de domínio (V-29): checar antes de inserir não evita corrida.
- [ ] 401 (sem credencial válida) x 403 (sem permissão) coerentes; recurso alheio 404.
- [ ] Paginação com ordenação determinística (desempate por `id`) e limite máximo.
- [ ] Migrações com Alembic em produção; `create_all` só em desenvolvimento (V-29).
- [ ] Configuração por `pydantic-settings`; segredos por ambiente; app com `lifespan` para recursos (engine, clientes).
- [ ] Senhas com Argon2 ou bcrypt por biblioteca; `python-jose` e `passlib` têm manutenção fraca (Inferido): confirme o estado atual e prefira PyJWT e bcrypt/pwdlib/argon2.
- [ ] Login e reset com rate limit (o exemplo de V-29 não tinha).

## 2. Estrutura e camadas

```text
app/
  main.py            # fábrica do app, lifespan, handlers de erro
  deps.py            # Annotated[...] de dependências (usuário, serviço, sessão)
  routers/orders.py  # só HTTP: parse, chama service, devolve DTO
  services/orders.py # regra de negócio; levanta exceções de domínio
  repositories/orders.py  # única camada que fala com ORM
  schemas/orders.py  # OrderCreate (in), OrderOut (out)
  models/orders.py   # ORM
```

Handler fino (≈ 10 linhas, sem limite numérico imposto: o limite é opinião, conflito C15 do playbook):

```python
@router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(
    body: OrderCreate,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[OrderService, Depends(get_order_service)],
):
    return service.create(owner_id=user.id, data=body)
```

## 3. Autenticação que valida de verdade

`OAuth2PasswordBearer(tokenUrl=...)` não cria o endpoint de token e só extrai o header (V-21). A validação é do projeto:

```python
from typing import Annotated
from uuid import UUID

import jwt                                   # PyJWT
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")   # extrai Authorization: Bearer ...

def get_current_user(token: Annotated[str, Depends(oauth2)]) -> User:
    try:
        claims = jwt.decode(
            token, key=settings.jwt_public_key,
            algorithms=["RS256"], audience=settings.jwt_audience, issuer=settings.jwt_issuer,
            options={"require": ["exp", "iss", "aud", "sub"]},
        )
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="invalid credentials",
                            headers={"WWW-Authenticate": "Bearer"})
    return User(id=UUID(claims["sub"]), scopes=set(claims.get("scope", "").split()))
```

Escopo: dependência adicional (`require_scope("orders:write")`) que levanta 403. Autorização **por objeto** fica no repositório/service (`WHERE owner_id = :user_id`). Checklist JWT completo: `${CLAUDE_PLUGIN_ROOT}/skills/api-security-review/references/jwt-oauth.md`.

## 4. Erros em RFC 9457

```python
from http import HTTPStatus

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()
BASE = "https://api.exemplo.com.br/problems"

def problem(status_code: int, slug: str, title: str, detail: str | None = None, **ext) -> JSONResponse:
    corpo = {"type": f"{BASE}/{slug}", "title": title, "status": status_code, **ext}
    if detail:
        corpo["detail"] = detail
    return JSONResponse(corpo, status_code=status_code, media_type="application/problem+json")

class DomainError(Exception):
    status, slug, title = 400, "domain-error", "Domain error"

class OrderNotFound(DomainError):
    status, slug, title = 404, "order-not-found", "Order not found"

@app.exception_handler(DomainError)
async def domain_handler(request, exc: DomainError):
    return problem(exc.status, exc.slug, exc.title, str(exc) or None)

@app.exception_handler(RequestValidationError)
async def validation_handler(request, exc: RequestValidationError):
    erros = exc.errors()
    if any(e["type"] == "json_invalid" for e in erros):          # JSON malformado: 400, não 422
        return problem(400, "malformed-json", "Malformed JSON body")
    campos = [{"field": ".".join(str(p) for p in e["loc"][1:]), "code": e["type"]} for e in erros]
    return problem(422, "validation", "Request validation failed", errors=campos)  # sem ecoar "input"

@app.exception_handler(StarletteHTTPException)
async def http_handler(request, exc: StarletteHTTPException):
    # about:blank + título = frase do status HTTP (RFC 9457); mantém WWW-Authenticate do 401
    return JSONResponse(
        {"type": "about:blank", "title": HTTPStatus(exc.status_code).phrase, "status": exc.status_code},
        status_code=exc.status_code, media_type="application/problem+json", headers=exc.headers)
```

Pontos: (1) por padrão o FastAPI responde **422** em validação e o corpo padrão **ecoa o `input`** recebido: o handler acima não ecoa. (2) 400 x 422 é decisão do projeto; mantenha uma só tabela (conflito C1 do playbook). (3) O tipo `json_invalid` vem do Pydantic v2: confirme na versão instalada. (4) Um handler `Exception` genérico devolve 500 sem stack trace/SQL, registrando o detalhe no log, não na resposta.

## 5. Modelos de entrada e saída

```python
from pydantic import BaseModel, ConfigDict, Field

class OrderCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")          # campo desconhecido: rejeitado (decisão de contrato)
    items: list[OrderItemIn] = Field(min_length=1, max_length=100)
    note: str | None = Field(default=None, max_length=500)

class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    status: str
    total: str                                         # dinheiro como string decimal
    created_at: datetime
# OrderOut não tem owner_id, hash nem campos internos.
```

Atribuição em massa acontece quando a entidade recebe `**body.model_dump()` com campos privilegiados: mantenha `OrderCreate` sem `owner_id`, `status`, `total`.

## 6. Serviço, unicidade e idempotência

```python
def create(self, owner_id: UUID, data: OrderCreate) -> Order:
    try:
        order = self.repo.add(owner_id=owner_id, data=data)
        self.session.commit()
    except IntegrityError as exc:                      # restrição única no banco (ex.: referência externa)
        self.session.rollback()
        raise DuplicateOrder() from exc
    return order
```

Operação com efeito (cobrança, envio, criação via POST) aceita chave de idempotência com unicidade no banco: `${CLAUDE_PLUGIN_ROOT}/skills/idempotency-and-resilience/references/politicas-idempotencia.md`.

## 7. Paginação por cursor

```python
stmt = (select(Order).where(Order.owner_id == user_id)
        .order_by(Order.created_at.desc(), Order.id.desc()).limit(page_size + 1))
if cursor:                                              # cursor decodificado = (created_at, id)
    stmt = stmt.where(tuple_(Order.created_at, Order.id) < tuple_(c_created, c_id))
```

Busque `page_size + 1` para saber se há próxima página. O token é opaco (ex.: base64 de JSON **assinado**); base64 transparente não protege e o token **nunca** concede autorização: o filtro de dono continua na consulta (V-34). `page_size` com padrão e máximo; negativo é 400.

## 8. Testes

```python
import pytest
from httpx import ASGITransport, AsyncClient

@pytest.mark.anyio                                      # ou pytest-asyncio, conforme o projeto
async def test_recurso_alheio_e_404(app, token_a, id_pedido_de_b):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get(f"/orders/{id_pedido_de_b}", headers={"Authorization": f"Bearer {token_a}"})
    assert r.status_code == 404
    assert r.headers["content-type"].startswith("application/problem+json")
```

`app.dependency_overrides[get_current_user] = ...` acelera testes, mas não substitui um teste com **tokens reais** de dois perfis (guard mal ligado passa despercebido). Mais em `${CLAUDE_PLUGIN_ROOT}/skills/api-test-suite/references/exemplos-pytest-httpx.md`.

## 9. Verificação por busca

Heurísticas: confirme lendo o arquivo antes de reportar.

```bash
grep -rEn "^\s*(from|import)\s+(sqlalchemy|httpx|boto3)" app/routers
grep -rEn "^\s*from\s+app\.(models|repositories)" app/routers
grep -rEn "^\s*(from|import)\s+(fastapi|starlette)" app/services
grep -rEn "@(router|app)\.(get|post|put|patch|delete)\(" app | grep -v "response_model"
grep -rEn "create_all|python-jose|passlib|\bjose\b" app pyproject.toml requirements*.txt
```

(A quarta linha lista endpoints **sem** `response_model` na mesma linha; `response_model` pode estar em linha seguinte: leia antes de reportar.)

## 10. Lacunas

Django/DRF, Flask, tRPC e validação por biblioteca fora do Pydantic não têm referência neste plugin. Pydantic v1 x v2: confirme a versão; este arquivo assume v2.
