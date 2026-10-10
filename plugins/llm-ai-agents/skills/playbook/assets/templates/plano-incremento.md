# Plano de incremento (aplicação LLM ou agente)

Adaptado de `brains/fullstack/assets/templates/plano-incremento.md` do repositório `francisco-efjr/brain-of-agent` (MIT, conteúdo do próprio autor), ajustado para trabalho com LLM. Use em projeto amplo: incrementos com critério de saída, sem gastar API, instalar ou agir externamente sem confirmação.

## Objetivo e baseline

Problema, usuário e comportamento atual:
Critério de sucesso e fonte (suíte, comando):
Estado observado e reprodução (transcrições lidas):
Escopo, exclusões e autorização (ações externas, gastos, produção):
Modelo-alvo, superfície, versão do SDK/CLI e data:

## Fatia vertical

Entrada do usuário → montagem do prompt/contexto → chamada ao modelo → ferramentas → validação em código → resultado observável. Descreva cada fronteira e sua falha e recuperação (timeout, `refusal`, `max_tokens`, tool com erro).

| Requisito | Alteração | Invariante | Contrato/compatibilidade | Verificação/oráculo |
| --- | --- | --- | --- | --- |

## Plano e riscos

| Fase | Artefato utilizável | Risco | Mitigação | Critério de saída |
| --- | --- | --- | --- | --- |

Cartão A/B/C do agente:
Dependências e decisões materiais (ADR):
Custo estimado (planilha, data dos preços) e tetos de iteração:
Dados pessoais, retenção e telemetria:

## Validação

Checks existentes a executar:
Suíte de avaliação: casos, graders, execuções, quem roda e custo:
Regressões necessárias e por quê:
Não executável e risco restante:

## Entrega

Como executar, configurar e observar:
Publicação, rollback e gasto somente dentro da autorização:
Evidências, pendências e próximo passo:
