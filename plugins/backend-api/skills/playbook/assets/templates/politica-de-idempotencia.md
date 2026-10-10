# Política de idempotência — [serviço/operação]

> Não há padrão publicado vencedor: o draft do header `Idempotency-Key` expirou em 18/04/2026 (V-16). Esta política é uma **decisão de contrato do projeto**; registre-a aqui e no OpenAPI. Base: V-15 (Stripe, AIP-155), V-16, V-31, V-35 e brain-of-agent (MIT). Valores abaixo são o default do plugin (rotule como **Suposição** se o usuário não decidiu).

| Item | Decisão |
| --- | --- |
| Operações cobertas | [POST /payments, POST /orders, ...] (não coberto: PUT/DELETE, idempotentes por semântica) |
| Risco se executar duas vezes | [cobrança duplicada; e-mail repetido; pedido duplicado] |
| Onde viaja a chave | [header `Idempotency-Key` (default) | `request_id` no corpo | `Repeatability-*`] |
| Formato e tamanho da chave | [UUID v4; até 255 caracteres; sem dado pessoal] |
| Escopo da chave | [usuário/tenant + operação + chave] (nunca global) |
| Fingerprint do pedido | [hash SHA-256 de método + caminho + corpo canônico relevante] |
| Armazenamento | [tabela `idempotency_keys` com PRIMARY KEY (scope_id, operation, key); estado `in_progress|completed`; status e corpo da resposta] |
| Atomicidade | [INSERT ... ON CONFLICT DO NOTHING; efeito na mesma transação do dado quando possível] |
| Retenção e limpeza | [24 h | outra; job de limpeza por `expires_at`]; documentada no OpenAPI |
| Chave ausente em operação que exige | [400 + problem+json] |
| Chave malformada | [400] |
| Mesma chave + mesmo corpo | [reproduz status, corpo e `Location` originais; sem novo efeito] |
| Mesma chave + corpo diferente | [422 (default) | erro da política] |
| Original em processamento | [409 | espera com prazo] |
| Falha de validação | [não consome a chave] |
| Falha de dependência após efeito | [política: salvar a resposta de erro (Stripe) | liberar a chave] |
| Linha `in_progress` órfã | [expira por timeout de lock de X s] |
| Efeito externo | [chave derivada estável enviada ao provedor; nunca nova por tentativa] |
| Segurança | [chave não revela dado; escopo por tenant impede colisão] |

## Testes obrigatórios

1. Primeira chamada cria o efeito. 2. Replay devolve a mesma resposta sem novo efeito. 3. **Duas requisições concorrentes** com a mesma chave produzem um único efeito. 4. Corpo divergente devolve o código da política. 5. Perda de resposta após aceitação seguida de retry. 6. Validação inválida não consome a chave. 7. Chave de outro tenant não colide. 8. Expiração libera a chave.

Rótulos: [Verificado | Inferido | Suposição]. Migração: proposta; executada apenas em banco de teste; staging/produção são do humano.
