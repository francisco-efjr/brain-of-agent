# Ficha de endpoint — [MÉTODO] [/caminho]

> Preencha antes de implementar e mantenha junto da spec. Campo desconhecido fica como "a confirmar", nunca inventado. Fontes: V-11, V-14, V-34, V-35 (`skills/playbook/references/fontes.md`).

| Campo | Conteúdo |
| --- | --- |
| `operationId` / versão da API | [createOrder] / [v1] |
| Finalidade e regra de negócio | [uma frase; fonte da regra] |
| Consumidores | [conhecidos | públicos/desconhecidos] |
| Autenticação e escopo | [Bearer JWT; escopo orders:write] — `security` explícita na operação |
| Autorização por objeto | [dono = user_id; tenant; 404 para alheio] |
| Request: caminho, query, header | [tipos, limites, enums fechados] |
| Request: corpo | [schema; obrigatório x opcional; ausente x null; campos desconhecidos: rejeitar | ignorar] |
| Dinheiro, data, fuso | [string decimal | centavos; ISO 8601 com fuso] |
| Respostas por status | [201 + Location; 400; 401; 403; 404; 409; 413; 415; 422; 429; 5xx] |
| Erro | [`application/problem+json`; `type` por cenário; `detail` sem dado sensível] |
| Paginação | [cursor opaco; limite padrão/máximo; ordenação com desempate] |
| Idempotência | [header; escopo; retenção; códigos] ou "naturalmente idempotente (PUT/DELETE)" |
| Concorrência | [ETag/If-Match: 412/428; 409 de regra] |
| Rate limit | [chave de credencial validada; 429 + Retry-After] |
| Cache | [Cache-Control: private | no-store; ETag] |
| Operação longa | [202 + monitor + Retry-After] ou "n/a" |
| Efeitos colaterais | [linha no banco; evento emitido uma vez; chamada externa com timeout] |
| Compatibilidade | [mudança compatível | breaking; plano] |
| Testes e oráculos | [positivo com valor independente; negativos de authz, validação, duplicata, concorrência; efeito persistido] |
| Rótulos | [Verificado | Inferido | Suposição | Não verificável] por linha relevante |

Exemplo de request e response realistas (conferidos contra os serializers reais):

```http
[MÉTODO] [/caminho] ...
```
