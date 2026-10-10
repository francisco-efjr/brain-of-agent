# Template: checklist de campo e de operação para documentação de API

Fonte: AIP-192 do Google (CC BY 4.0), em redação própria (V-41). O AIP é escrito para protobuf: o checklist vale em qualquer linguagem (OpenAPI, GraphQL, anotações); a sintaxe do AIP não. Todo serviço, método, mensagem, campo, enum e valor de enum tem descrição pública.

## Por campo

| Pergunta | Resposta (para cada campo) |
| --- | --- |
| O que é e como é usado? | |
| Unidade (centavos, segundos, bytes)? | |
| Formato e faixa de valores (regex, mínimo e máximo, enum)? | |
| Está sempre presente? Pode ser nulo? | |
| Qual o padrão quando omitido? | |
| Efeitos colaterais ao definir ou alterar? | |
| Erros comuns? | |

## Por operação

| Pergunta | Resposta |
| --- | --- |
| O que faz, em uma frase sem sujeito, na terceira pessoa do presente ("Cria um pedido sob o cliente informado.")? | |
| Quando é sucesso e quando é falha (códigos e corpo)? | |
| É idempotente? Como repetir com segurança? | |
| Autorização e escopo necessários? | |
| Limites (taxa, tamanho, paginação)? | |
| Exemplo real de requisição e resposta, ou marcado "ilustrativo"? | |

## Estilo do comentário

- CommonMark. No AIP/protobuf: sem títulos, tabelas ou HTML bruto no comentário, e sem arte ASCII (link para imagem). Em OpenAPI, siga as convenções do ecossistema.
- Primeira frase curta e sem sujeito.

## Deprecação

- `deprecated: true` (OpenAPI) e primeira linha "Deprecated:" com a alternativa ou o motivo.
- Entrada no changelog de API com data de remoção prevista, se houver.

## Changelog de API (tabela, estrutura inspirada na da Stripe, V-41)

| Mudança | Área afetada | Quebra? | Canal |
| --- | --- | --- | --- |
| [DESCRIÇÃO] | [RECURSO OU PRODUTO] | sim/não | estável/preview |

Quebra de compatibilidade é definida pelo plugin `backend-api`; aqui só se registra e se escreve.
