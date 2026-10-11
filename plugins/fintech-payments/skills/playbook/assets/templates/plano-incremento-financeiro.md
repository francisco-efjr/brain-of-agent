# Plano de incremento financeiro

Adaptado do template `plano-incremento` do brain-of-agent (MIT, conteúdo do usuário). Preencha antes de implementar; para correção localizada, basta a seção "Objetivo" e "Validação". Campos entre colchetes são para preencher; remova o que não se aplicar com motivo.

## Objetivo e baseline

- Problema, usuário e comportamento atual: [descreva em 2 a 4 linhas]
- Critério de sucesso e fonte do critério: [ex.: "uma cobrança por intenção, provada por contagem de linhas"]
- Estado observado e reprodução (comando e saída, ou "não reproduzido"): [ ]
- Operação e canal: [cobrança | captura | estorno | repasse | Pix cob/cobv | boleto | webhook] · [cartão | Pix | boleto]
- Provedor, versão da API e **modo** (teste ou produção): [ ] · [teste]
- Especificações lidas (nome, versão, data de leitura): [ex.: Manual do Pix 2.10.0, 2026-10-11]
- Escopo, exclusões e autorização: [o que será alterado] / **fora do escopo:** produção, chaves reais, dados reais, `.env`, push/deploy, [outros]
- Stack, revisão do repositório e ambiente: [ ]

## Invariantes (marque os aplicáveis)

| Invariante | Aplica? | Como será garantido | Oráculo |
| --- | --- | --- | --- |
| Dinheiro = inteiro na menor unidade + ISO 4217; sem float | [sim/não] | [tipo `Money`; conversão na borda] | [teste de propriedade; cálculo independente] |
| Idempotência: chave por intenção, persistida antes da chamada | [ ] | [constraint `(escopo, chave)`] | [contagem de linhas] |
| Timeout = desconhecido; consulta antes de reenviar | [ ] | [estado `indeterminate`] | [teste de timeout + retry] |
| Webhook: assinatura, dedupe, releitura | [ ] | [inbox + fila] | [roteiro hostil] |
| Histórico append-only; estorno ligado ao original | [ ] | [sem UPDATE/DELETE] | [auditoria de soma zero] |
| Conciliação bilateral por partição | [ ] | [job diário] | [`relatorio-conciliacao.md`] |

## Fatia vertical

Entrada → validação → idempotência → máquina de estados → provedor → ledger/outbox → resposta. Descreva cada fronteira e sua falha/recuperação (`tabela-estados-pagamento.md`).

| Requisito | Alteração | Invariante | Contrato/compatibilidade | Verificação/oráculo |
| --- | --- | --- | --- | --- |
| [ ] | [ ] | [ ] | [ ] | [ ] |

## Plano e riscos

| Fase | Artefato utilizável | Risco | Mitigação | Critério de saída |
| --- | --- | --- | --- | --- |
| [1] | [ ] | [ ] | [ ] | [comando + resultado esperado] |

- Decisões materiais (ADR): [link ou "nenhuma"]
- Dados/migração e limites de recuperação: [migração só proposta; execução em staging/produção por humano]
- Timeout, duplicação, concorrência, ordem de eventos e autorização: [como cada um é tratado]
- Fuso do negócio e virada do dia: [ ]

## Validação

- Checks existentes a executar (comandos literais): [ ]
- Testes novos (nível: unidade/integração/contrato) e **por que o teste falha sem a proteção**: [ ]
- Integrações reais e isolamento: nenhuma chamada a provedor real; assinaturas geradas localmente; dados sintéticos
- Não executável e risco restante: [ ]

## Confirmações exigidas (antes de agir)

- [ ] Efeito financeiro real, estorno ou alteração de cliente: conta, modo, operação, valor, moeda e "sim" explícito, por ação.
- [ ] Publicação, push, deploy, migração em ambiente compartilhado: autorização concreta.

## Entrega

- Como executar, configurar e observar: [ ]
- Evidências (comando e saída), pendências, **lista "Não verificado"** e próximo passo: [ ]
