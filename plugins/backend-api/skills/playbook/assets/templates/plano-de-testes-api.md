# Plano de testes de API

> Base: `automacao-api.md` e templates de QA do brain-of-agent (MIT). Técnicas gerais de teste ficam em `/qa-testing:playbook`; aqui está o que é específico de API.

Escopo (endpoints, eventos, webhooks): [..] · Revisão/ambiente: [..] · Data: [..]
Ambiente permitido: [local | descartável | homologação com autorização: qual] · Produção: nunca
Dados semeados e oráculos (de onde vem o valor esperado): [..]
Perfis de usuário (mínimo 2, para isolamento): [A, B, admin, sem escopo]
Segredos: somente por variável de ambiente [nomes das variáveis]

## Riscos por endpoint (prioridade)

| Endpoint | Risco (falha → efeito) | Prioridade | Camada que prova |
| --- | --- | --- | --- |
| [POST /orders] | [duplicação → cobrança dupla] | alta | integração com banco real |

## Matriz de aspectos x endpoint

Aspectos (checklist por endpoint de `references/checklist-completo.md`): status e corpo · schema · headers · CORS · erro RFC 9457 · idempotência · paginação · filtros e ordenação · validação · authN x authZ · rate limit · versionamento · concorrência otimista · efeito colateral.

| Endpoint | Status/corpo | Schema | Erro | Idem. | Pagin. | Validação | AuthN/AuthZ | Concorr. | Efeito | Lacuna |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [..] | | | | | | | | | | |

## Estrutura

Cliente fino sem asserção · fábrica de dados com ID único · fixture de auth por sessão com dois usuários · schema para forma, asserção para valor · erro comparado por `type` · espera por condição com prazo.

## Contrato e fuzz

Estratégia: [Pact | OpenAPI + Schemathesis/Prism + diff de spec | schema primeiro]. Justificativa (tabela em `decisoes-e-tradeoffs.md`):
Fuzz/stateful: só em ambiente descartável e autorizado; cada falha vira teste de regressão mínimo.

## Eventos e webhooks

Duplicata (um efeito) · mensagem envenenada (DLQ com motivo; seguintes continuam) · ordem invertida · assinatura adulterada · timestamp fora da tolerância · consumo desde o início (`earliest`, grupo exclusivo).

## Critérios de saída

- Suíte roda em qualquer ordem e em paralelo; nenhum teste depende de ID, token ou sleep fixo.
- Ao menos uma asserção de efeito persistido por escrita.
- Bug: teste vermelho pelo motivo certo antes da correção.
- Comando para rodar: [cmd]. Resultado: [saída colada | NÃO EXECUTADO: motivo].
- Não testado e risco restante:
