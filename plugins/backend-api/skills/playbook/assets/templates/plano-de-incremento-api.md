# Plano de incremento de API

> Adaptado do template `plano-incremento.md` do brain-of-agent (conteúdo próprio do usuário, MIT), com campos de contrato, idempotência, paginação e compatibilidade. Use para funcionalidade de médio porte; correção localizada dispensa este plano (diff que cabe numa frase).

## Objetivo e baseline

Problema, consumidores e comportamento atual:
Critério de sucesso e fonte (requisito, ticket, regra):
Estado observado e reprodução (comando + saída):
Escopo, exclusões e autorização (o que pode mudar; ações externas só com autorização concreta):
Stack, versões, revisão e ambiente (conferidos em `go.mod`/`pyproject.toml`/`package.json`/`pom.xml`):

## Fatia vertical

Entrada → validação → autorização → regra → dados/integração → resposta ou erro. Descreva cada fronteira e sua falha/recuperação.

| Requisito | Alteração (arquivos) | Invariante | Contrato e compatibilidade | Oráculo / verificação |
| --- | --- | --- | --- | --- |
| [R1] | [rota, service, repositório, migração] | [ex.: pedido só visível ao dono] | [campo novo opcional; sem breaking] | [valor esperado calculado à parte; teste com 2 usuários] |

## Contrato

- Operações novas ou alteradas (método, caminho, `operationId`):
- Status por cenário e erro `application/problem+json` (`type` por cenário):
- Autenticação e escopo por operação (`security` explícita):
- Paginação (limite padrão e máximo, cursor, ordenação com desempate):
- Idempotência (operações com efeito; política escolhida: ver `politica-de-idempotencia.md`):
- Rate limit, cache/ETag e operação longa (202), quando aplicável:
- Classificação de compatibilidade de cada mudança (compatível ou breaking) e plano para consumidores:

## Plano e riscos

| Fase | Artefato utilizável | Risco | Mitigação | Critério de saída |
| --- | --- | --- | --- | --- |
| [1] | [spec + teste vermelho] | [ex.: consumidor desconhecido] | [campo opcional] | [validador de spec sem erro; teste falha pelo motivo certo] |

Dependências e decisões materiais (ADR quando houver):
Dados e migração (proposta de migração; execução em staging/produção é do humano; recuperação):
Timeout, duplicação, concorrência e autorização (teste de duas requisições concorrentes; dois usuários):

## Validação

Checks do projeto a executar, em ordem: tipos [cmd] · testes [cmd] · lint [cmd] · spec [cmd]:
Regressões necessárias e por quê:
Integrações reais x mocks (declare):
Efeitos persistidos a observar (GET seguinte, linha no banco, evento emitido uma vez):
Não executável e risco restante:

## Entrega

Como executar, configurar e observar:
Publicação e rollback somente dentro da autorização recebida:
Evidências (comando + saída), pendências e próximo passo:
Rótulos: Verificado · Inferido · Suposição · Não verificável
