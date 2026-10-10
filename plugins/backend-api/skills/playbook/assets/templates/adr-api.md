# ADR [ID] — [decisão de API ou de serviço]

> Adaptado do template `adr.md` do brain-of-agent (MIT). Use só para decisão material: protocolo (REST, GraphQL, gRPC), versionamento, política de idempotência, modelo de autorização, formato de erro, estratégia de paginação. Decisão pequena vira uma linha no PR.

Estado: [proposta | aceita | substituída por ADR-X] · Data/revisão: [AAAA-MM-DD / commit]

## Contexto

Problema, consumidores (conhecidos ou públicos), restrições, requisitos, evidências, stack e versões existentes. O que o projeto já usa:

## Opções

| Opção | Benefício | Custo/risco | Compatibilidade com consumidores | Evidência (fonte, teste) |
| --- | --- | --- | --- | --- |
| A — [padrão existente] | | | | |
| B — [alternativa] | | | | |
| C — não fazer / adiar | | | | |

## Decisão

Opção escolhida e por quê. Hipóteses ainda não confirmadas (rótulo Suposição):

Políticas adotadas (preencha as que se aplicam):
- Versionamento (uma estratégia por API): [caminho | query | cabeçalho]; sem quebra dentro de uma versão.
- Erros: `application/problem+json` (RFC 9457); tabela em [caminho].
- Idempotência: [header, escopo, retenção, códigos]; ver `politica-de-idempotencia.md`.
- Paginação: [cursor opaco, limite padrão e máximo, ordenação com desempate].
- Autorização: [modelo; filtro por dono/tenant na consulta; 404 para recurso alheio].
- Tabela 400/422: [regra do projeto].

## Consequências

Complexidade, operação, dados, migração, segurança e testes afetados. Limites de reversibilidade e de recuperação (rollback de aplicação não desfaz schema nem dado transformado). Impacto em consumidores e plano de deprecação (`aviso-de-deprecacao.md`).

## Validação e revisão

Critérios observáveis, teste ou experimento que sustenta a escolha (comando + saída esperada):
Condição que exige reconsiderar a decisão:
Links para requisito, spec e artefatos:
Revisão: [humano | agente em contexto limpo — declare que não é validação independente]
