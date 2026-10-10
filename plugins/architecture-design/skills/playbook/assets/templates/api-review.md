<!-- Revisão de contrato de API. Contrato e decisão aqui; implementação em framework em /backend-api:playbook. -->
# Revisão de API: [nome e versão]

Data: [AAAA-MM-DD] · Consumidores: [quem, frequência, restrições] · Contrato: [OpenAPI / texto]

## Checklist
| Item | Resp. | Nota |
| --- | --- | --- |
| Recursos com nomes de substantivo no plural, hierarquia rasa | | |
| Métodos e status coerentes (200, 201+Location, 202, 204, 400, 401, 403, 404, 409, 412, 422, 429) | | |
| PUT e DELETE idempotentes | | |
| POST com efeito: `Idempotency-Key` definida (escopo, TTL, resposta repetida) | | |
| Operação longa: 202 + recurso de status | | |
| Paginação por cursor em coleção grande ou mutável | | |
| Filtros, ordenação e respostas parciais documentados | | |
| Concorrência: ETag e `If-Match`, 412 | | |
| Evolução: mudanças aditivas; depreciação com prazo; expandir, migrar, contrair | | |
| Versionamento escolhido e registrado em ADR | | |
| Autorização por objeto | | |
| Trace context e ID de correlação | | |
| Contrato passa por lint (usuário executa) | | |

## Modelo de erro (RFC 9457, application/problem+json)
```json
{
  "type": "https://example.com/problems/[tipo-estavel]",
  "title": "[título curto]",
  "status": 422,
  "detail": "[explicação sem dado sensível nem stack trace]",
  "instance": "[caminho ou ID da requisição]",
  "errors": [ { "field": "[caminho]", "detail": "[regra violada]" } ]
}
```

## Exemplos obrigatórios
- Requisição e resposta de paginação: [..]
- Requisição e resposta de erro de validação: [..]
- Repetição com a mesma `Idempotency-Key`: [..]

## Achados
| ID | Sev. | Conf. | Local | Cenário | Ação |
| --- | --- | --- | --- | --- | --- |
| ARQ-nn | | | | | |

## Pendências e Suposições
[..]
