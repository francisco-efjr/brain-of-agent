# Stacks: índice, versão-alvo e o que conferir

Índice para `stack-conventions`. O detalhe por stack fica em `${CLAUDE_PLUGIN_ROOT}/skills/stack-conventions/references/stack-<nome>.md`; aqui estão a versão lida, os pontos de maior risco e as lacunas. Regra universal: **detecte a versão instalada** (`go.mod`, `pyproject.toml`/`requirements.txt`, `package.json`, `pom.xml`/`build.gradle`, `*.csproj`) e confira a doc dessa versão antes de afirmar API; nunca invente assinatura. Fontes: `V-nn` em `fontes.md`.

## Sumário

- [Resumo por stack](#resumo-por-stack)
- [FastAPI (Python)](#fastapi-python)
- [Go](#go)
- [NestJS e Node](#nestjs-e-node)
- [Spring](#spring)
- [ASP.NET Core](#aspnet-core)
- [GraphQL](#graphql)
- [Stacks sem referência](#stacks-sem-referência)
- [Comandos de verificação por camada](#comandos-de-verificação-por-camada)

## Resumo por stack

| Stack | Versão lida | Maior risco a conferir | Fonte |
| --- | --- | --- | --- |
| FastAPI | docs atuais (2026-10-10), sem número fixado | Dependência de auth que não valida o token; `response_model` ausente; filtro por dono; libs de auth antigas | V-21, V-23, V-29 |
| Go | Go 1.22 (blog de 13/02/2024) | Rotas sem método; erro ignorado com `_`; cliente HTTP sem timeout; corpo não fechado | V-18 |
| NestJS | docs atuais | Guard ausente em rota; ordem guards x pipes; `APP_GUARD` | V-19 |
| Spring Security | série 7.1.1 | `aud` não validado; `jwk-set-uri` sem `iss`; mapeamento de escopos | V-20 |
| ASP.NET Core | .NET 10 | `UseExceptionHandler` em produção; `IExceptionHandler` escrevendo resposta completa; ProblemDetails | V-22 |
| GraphQL | skill Apollo 1.0.2 | Nulabilidade, N+1, profundidade, autorização por campo | V-30, brain |

## FastAPI (Python)

- Camadas Router → Service → Repository → ORM/HTTP. Router sem import de `sqlalchemy`/`httpx`/`boto3`/models; service depende de Protocols e não importa request/response; handler curto (sem limite fixo de linhas, que é opinião) — V-23.
- `response_model` em todo endpoint; modelos `Create/Update/Response` separados (`from_attributes`); `response_model_include/exclude` **não** mudam o schema do OpenAPI — prefira classes separadas (V-21, V-29).
- `user_id` por dependência; **toda** consulta filtra por dono; recurso alheio responde como inexistente.
- `OAuth2PasswordBearer` não cria o endpoint de token nem valida o token (V-21): a dependência do projeto valida assinatura, `iss`, `aud`, `exp`.
- Exceção de domínio traduzida no router; restrição única no banco com rollback em `IntegrityError`; 401 x 403 coerentes.
- Testes: `httpx.AsyncClient` com `ASGITransport`, `dependency_overrides`; paginação com ordenação determinística.
- Migrações com Alembic em produção; `create_all` só em desenvolvimento.
- Lacunas: Django/DRF, validação por Pydantic v2 em profundidade.

## Go

- `go >= 1.22` no `go.mod`: use o `ServeMux` com método no padrão (`"GET /posts/{id}"`), `Request.PathValue`, `{name...}`, `{$}`; GET casa HEAD; o padrão mais específico vence e **sobreposição sem precedência dá pânico no registro** (V-18).
- Erro checado logo após a chamada; `fmt.Errorf("...: %w", err)`; `errors.Is/As`; não logar **e** retornar o mesmo erro.
- `http.Client{Timeout: ...}`; `defer resp.Body.Close()`; goroutine com caminho de saída (contexto/cancelamento).
- Testes table-driven; ferramentas `gofmt`, `go vet`, `golangci-lint`, `go test` (rodar as do projeto).
- `id := strings.TrimPrefix(r.URL.Path, ...)` concatenado em URL interna é SSRF/injeção de caminho: valide e escape.
- Lacunas: Chi/Gin/Echo, layout de projeto, validação, autenticação.

## NestJS e Node

- Guard com `CanActivate`; retornar `false` gera 403; metadata de papéis via `Reflector.createDecorator`/`@SetMetadata`; global por `APP_GUARD` (com injeção); ordem: middleware → guards → interceptors → pipes (a ordem entre interceptors e pipes não foi confirmada, V-19).
- Padrão: guard de autenticação anexa `request.user`; guard de papel lê a metadata.
- Antes de importar pacote: `npm ls <pacote>` e doc oficial (SN-13).
- Express/Fastify: lacuna; aplique só os princípios do playbook e rotule **Inferido**. `nodebestpractices` é CC-BY-SA-4.0: não reproduza.

## Spring

- Resource server: `issuer-uri` descobre as chaves e valida `iss`; `jwk-set-uri` sozinho não valida `iss`; só RS256 por padrão; valida `exp`, `nbf`, `iss` com tolerância de 60 s; **`aud` não é validado** sem `audiences` ou `JwtClaimValidator`; escopos `scope`/`scp` viram `SCOPE_<valor>` (V-20).
- Lacunas: `ProblemDetail`, Bean Validation, Actuator, Spring Boot em geral.

## ASP.NET Core

- `UseExceptionHandler` (convencionalmente fora de Development); `IExceptionHandler` via `AddExceptionHandler<T>()`, em ordem; `TryHandleAsync` retornando `true` encerra e **deve escrever a resposta completa** (senão 404); `AddProblemDetails()`; `UseStatusCodePagesWithReExecute` preserva o status, `WithRedirects` não.
- A partir do .NET 10 os diagnósticos de exceções tratadas são suprimidos por padrão.
- A doc cita RFC 7807 (obsoleta; use 9457) e um exemplo de `StatusCodeSelector` parece invertido: confira (V-22).
- Lacunas: Minimal APIs, estrutura de projeto, FluentValidation.

## GraphQL

Checklist em `contrato-erros-paginacao.md`, seção 6: nulabilidade intencional, conexão com `first`, mutação com `input`, depreciar antes de remover, erros em `errors` com HTTP 200, profundidade e complexidade, DataLoader, introspecção desligada em produção, autorização no resolver do campo, persisted queries como allowlist.

## Stacks sem referência

Rust (axum, tower, `thiserror`/`anyhow`), tRPC, Django REST Framework, Express/Fastify, Gin/Chi/Echo, Spring Boot avançado, ASP.NET Minimal APIs: **sem fonte validada**. Declare a lacuna ao usuário, aplique os princípios genéricos (contrato, erro, authz no servidor, idempotência, paginação, evidência) e rotule o resto **Inferido**. Pesquisa futura listada em `fontes.md`.

## Comandos de verificação por camada

Camadas por busca de import (adapte padrões e pastas; saída vazia significa sem violação; cada linha retornada é `arquivo:linha`):

```bash
# Python/FastAPI: router não importa infraestrutura nem models
grep -rEn "^(from|import) (sqlalchemy|httpx|boto3)|^from .*models" app/routers
# service não importa request/response do framework
grep -rEn "^from fastapi import .*(Request|Response)" app/services
# Go: handler não importa driver de banco
grep -rEn "\"database/sql\"|\"github.com/jackc/pgx" internal/http
```

O comando é uma heurística: confirme cada ocorrência lendo o trecho. Ferramentas do projeto (tipos, testes, lint, spec) rodam na ordem de `CLAUDE.md` (SN-03).

Validado em 2026-10-10. Versões mudam (Spring 7.x, Go, .NET 10, FastAPI): confira a instalada.
