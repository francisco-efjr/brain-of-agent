# Política de erros — [serviço]

> Contrato de erro único para todos os endpoints: `application/problem+json` (RFC 9457, que obsoleta a RFC 7807; V-14). Clientes e agentes decidem retry pelo erro, por isso o formato é estável e o conteúdo é seguro. Base: V-14, V-22, V-35 e brain-of-agent (MIT).

## Regras

1. `status` no corpo igual ao status HTTP real.
2. `type`: URI documentada e estável (clientes decidem por ela, não pelo texto); `title` estável.
3. `detail`: humano e útil, **sem** stack trace, SQL, hostname, caminho de arquivo, token ou dado pessoal.
4. Mesmo formato em todos os endpoints, inclusive 404 de rota, 405, 413, 415, 429 e exceção não prevista (500 genérico). JSON malformado devolve 400 nesse formato, nunca 500.
5. Extensões permitidas (ex.: `erros[]` com `campo` e `codigo`); clientes ignoram as desconhecidas.
6. Tabela 400 x 422 do projeto: [400 para sintaxe/tipo malformado; 422 para regra semântica violada | manter o padrão do framework e documentar].
7. Recurso alheio responde como inexistente (mesmo status, formato e tempo aproximado) quando a existência é sensível.
8. Testes comparam `type`/código, nunca o texto.

## Tabela exceção → status → type

| Exceção / condição | Status | `type` | `title` | Retry do cliente |
| --- | --- | --- | --- | --- |
| JSON malformado | 400 | [/erros/json-invalido] | Corpo da requisição inválido | não, até corrigir |
| Campo inválido (tipo, faixa) | [400 | 422] | [/erros/validacao] | Requisição inválida | não, até corrigir |
| Não autenticado | 401 (+ `WWW-Authenticate`) | [/erros/nao-autenticado] | Autenticação necessária | após renovar credencial |
| Sem permissão | 403 | [/erros/proibido] | Acesso negado | não |
| Não encontrado ou alheio | 404 | [/erros/nao-encontrado] | Recurso não encontrado | não |
| Conflito de estado / duplicidade | 409 | [/erros/conflito] | Conflito com o estado atual | depende do estado |
| Pré-condição falhou / exigida | 412 / 428 | [/erros/pre-condicao] | Pré-condição | reler e repetir |
| Corpo grande | 413 | [/erros/corpo-grande] | Corpo acima do limite | não |
| Tipo de mídia | 415 / 406 | [/erros/tipo-midia] | Tipo não suportado | não |
| Limite de taxa | 429 (+ `Retry-After`) | [/erros/limite-de-taxa] | Muitas requisições | sim, após `Retry-After` |
| Erro interno | 500 | [/erros/interno] | Erro interno | cuidado: só se idempotente |
| Dependência indisponível | 502 / 503 / 504 (+ `Retry-After` em 503) | [/erros/indisponivel] | Serviço indisponível | sim, com backoff e idempotência |

## Exemplo de corpo

```json
{
  "type": "https://api.exemplo.com.br/erros/validacao",
  "title": "Requisição inválida",
  "status": 422,
  "detail": "O campo itens[0].quantidade deve ser um inteiro entre 1 e 10000.",
  "instance": "/orders",
  "erros": [{ "campo": "itens[0].quantidade", "codigo": "fora_da_faixa" }]
}
```

## O que nunca entra em `detail`

Stack trace; SQL ou nome de tabela/coluna; hostname ou IP interno; caminho de arquivo; segredo, token ou chave; dado pessoal de terceiros; diferença que revele se um recurso alheio existe.

## Implementação por stack

Um único ponto central converte exceções: FastAPI (`exception_handler`), Nest (`ExceptionFilter`), Spring (`ProblemDetail`/`@ControllerAdvice`; lacuna de fonte), ASP.NET Core (`AddProblemDetails()` + `IExceptionHandler`, V-22), Go (middleware). Confirme a API na versão instalada.
