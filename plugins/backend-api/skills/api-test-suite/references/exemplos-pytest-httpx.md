# Suíte de API em Python: pytest + httpx + Pydantic

Origem: brain-of-agent, `brains/qa/references/automacao-api.md` (autor Francisco Edson / francisco-efjr, licença MIT; conteúdo próprio do usuário, incorporado e adaptado). Código de exemplo: confira as APIs das bibliotecas na versão instalada no projeto (as versões não foram reverificadas nesta cadeia: **Inferido**). Exemplos nunca devem rodar contra produção; credenciais entram por variável de ambiente.

Use como molde quando o projeto é Python (FastAPI, Django, Flask) ou quando não há suíte de API ainda. O raciocínio (cliente fino, fábrica de dados, dois usuários, oráculo independente) vale para qualquer linguagem.

## Sumário

- Estrutura de uma suíte de API
- Exemplo: pytest + httpx + Pydantic
- Variações úteis para FastAPI (final do arquivo)

## Estrutura de uma suíte de API

- **Cliente fino:** um método por operação que devolve a resposta crua, sem
  asserção nem exceção em 4xx — senão os testes negativos ficam impossíveis.
- **Fábrica de dados:** cada teste cria o que usa, com identificador único,
  para rodar em paralelo e em qualquer ordem; limpa o que criou ou usa ambiente
  descartável.
- **Schema:** JSON Schema, Pydantic ou Zod provam a forma; os valores de
  negócio são conferidos à parte.
- **Autenticação por fixture:** token obtido uma vez por sessão com
  credenciais do ambiente (variáveis do CI, cofre); dois usuários de teste
  para provar isolamento.

## Exemplo: pytest + httpx + Pydantic

```python
# tests/api/conftest.py
import os
import uuid

import httpx
import pytest
from pydantic import BaseModel, ConfigDict

BASE_URL = os.environ["API_BASE_URL"]  # ex.: https://homolog.exemplo.com.br/api/v1


class Pedido(BaseModel):
    model_config = ConfigDict(extra="ignore")  # campo novo na resposta não é quebra
    id: uuid.UUID
    status: str
    total: str  # dinheiro como string decimal, ex.: "49.90"


class Problema(BaseModel):  # RFC 9457
    type: str
    title: str
    status: int
    detail: str | None = None


def novo_pedido(**campos) -> dict:
    # "CAFE-500G" custa 24,95 na massa semeada do ambiente: é o oráculo do total
    return {"referencia": f"teste-{uuid.uuid4().hex[:12]}",
            "itens": [{"sku": "CAFE-500G", "quantidade": 2}]} | campos


def _cliente(usuario_env: str, senha_env: str):
    with httpx.Client(base_url=BASE_URL, timeout=10) as anonimo:
        r = anonimo.post("/auth/token", json={"usuario": os.environ[usuario_env],
                                              "senha": os.environ[senha_env]})
    r.raise_for_status()
    token = r.json()["access_token"]
    return httpx.Client(base_url=BASE_URL, timeout=10, headers={"Authorization": f"Bearer {token}"})


@pytest.fixture(scope="session")
def api():
    with _cliente("API_USUARIO_A", "API_SENHA_A") as cliente:
        yield cliente


@pytest.fixture(scope="session")
def api_outro_cliente():
    with _cliente("API_USUARIO_B", "API_SENHA_B") as cliente:
        yield cliente
```

```python
# tests/api/test_pedidos.py
import uuid

import pytest

from .conftest import Pedido, Problema, novo_pedido


def criar(api, corpo, chave=None):
    return api.post("/pedidos", json=corpo, headers={"Idempotency-Key": chave or str(uuid.uuid4())})


def test_cria_pedido_calcula_total_e_persiste(api):
    r = criar(api, novo_pedido())

    assert r.status_code == 201, r.text
    pedido = Pedido.model_validate(r.json())
    assert (pedido.status, pedido.total) == ("PENDENTE", "49.90")  # 2 × 24,95
    assert r.headers["location"].endswith(f"/pedidos/{pedido.id}")
    lido = api.get(f"/pedidos/{pedido.id}")  # efeito colateral: foi gravado de fato
    assert lido.status_code == 200 and Pedido.model_validate(lido.json()) == pedido


def test_mesma_idempotency_key_nao_cria_segundo_pedido(api):
    chave, corpo = str(uuid.uuid4()), novo_pedido()
    primeira, segunda = criar(api, corpo, chave), criar(api, corpo, chave)

    assert primeira.status_code == segunda.status_code == 201
    assert segunda.json()["id"] == primeira.json()["id"]
    assert len(api.get("/pedidos", params={"referencia": corpo["referencia"]}).json()["itens"]) == 1


@pytest.mark.parametrize("quantidade", [0, -1, 2.5, None, 10_001])  # contrato: inteiro de 1 a 10.000
def test_quantidade_invalida_retorna_problem_details_e_nao_grava(api, quantidade):
    corpo = novo_pedido(itens=[{"sku": "CAFE-500G", "quantidade": quantidade}])
    r = criar(api, corpo)

    assert r.status_code == 422
    assert r.headers["content-type"].startswith("application/problem+json")
    problema = Problema.model_validate(r.json())
    assert problema.status == 422 and problema.type.endswith("/validacao")  # código, não texto
    assert api.get("/pedidos", params={"referencia": corpo["referencia"]}).json()["itens"] == []


def test_pedido_de_outro_cliente_e_indistinguivel_de_inexistente(api, api_outro_cliente):
    alheio_id = criar(api, novo_pedido()).json()["id"]
    alheio = api_outro_cliente.get(f"/pedidos/{alheio_id}")
    inexistente = api_outro_cliente.get(f"/pedidos/{uuid.uuid4()}")

    assert alheio.status_code == inexistente.status_code == 404
    assert alheio.json().keys() == inexistente.json().keys()
```

Rode com `pytest tests/api -n auto` (pytest-xdist); a referência única por
teste é o que permite o paralelismo.

## Variações úteis para FastAPI (testes em processo)

Sem subir servidor, com sobrescrita de dependências (V-29; conferir a versão instalada de FastAPI e httpx):

```python
import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.deps import get_current_user

@pytest.fixture
async def cliente_a():
    app.dependency_overrides[get_current_user] = lambda: Usuario(id=USUARIO_A, tenant=TENANT_1)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()
```

`pytest-asyncio` (ou `anyio`) é necessário para fixtures assíncronas; configure o modo conforme o projeto. Teste de autorização por **perfil real** (dois usuários, escopos diferentes) além do override, para não esconder um guard mal ligado. O banco do teste é descartável; migrações aplicadas por Alembic no setup da sessão, não `create_all` (só aceitável em desenvolvimento, V-29).
