# Checklist de webhook por provedor

Uso: um quadro por provedor integrado. Preencha a partir da documentação **atual** do provedor (data de leitura), não de memória; célula sem fonte = "Não verificado". Referência de valores já lidos: [pagamentos-webhooks-split.md](../../references/pagamentos-webhooks-split.md).

## 1. Provedor
- Nome: [PROVEDOR] · API/versão: [X] · Ambientes: teste [URL] · produção [URL] · Data de leitura: [AAAA-MM-DD] · Link: [URL DA DOC]

## 2. Contrato do provedor
| Item | Valor | Rótulo | Fonte |
| --- | --- | --- | --- |
| Autenticação (HMAC corpo bruto / token estático / mTLS) | [X] | | |
| Cabeçalho e formato (hex/base64), string assinada | [X] | | |
| Tolerância de timestamp | [X] | | |
| Prazo de resposta | [X s] | | |
| Reentrega (intervalo, nº de tentativas) | [X] | | |
| Retenção/descarte (dias, tentativas) | [X] | | |
| Ordem garantida? | [sim/não] | | |
| ID para dedupe | [campo] | | |
| Lista de IPs oficial | [sim/não] | | |
| Eventos tratados | [LISTA] | | |

## 3. Os 10 itens (OK / Falha / Não verificado) com evidência
| # | Item | Status | Evidência (arquivo:linha, teste, saída) |
| --- | --- | --- | --- |
| 1 | Assinatura sobre o corpo bruto antes de parsear | | |
| 2 | Tempo constante; formato inválido = falha limpa | | |
| 3 | Recência do timestamp | | |
| 4 | `event_id` único no banco; duplicata = 2xx sem efeito | | |
| 5 | 2xx rápido + fila | | |
| 6 | Sem dependência de ordem; estado atual pela API | | |
| 7 | Pedido só após evento verificado; divergência = retido | | |
| 8 | Reconciliação periódica por API | | |
| 9 | Rotação de segredo; segredos de teste ≠ produção | | |
| 10 | Teste local com encaminhador oficial e dados sintéticos | | |

## 4. Idempotência de saída
- Chave por intenção de compra: [SIM/NÃO] · hash do corpo: [SIM/NÃO] · retenção: [PRAZO] · conflito de corpo = erro: [SIM/NÃO]

## 5. Testes que provam
- [ ] Assinatura inválida rejeitada · [ ] corpo reescrito detectado · [ ] mesmo `event_id` 2× = 1 efeito (contagem de linhas) · [ ] entregas simultâneas · [ ] divergência de valor = retido · [ ] falha da fila não perde evento · [ ] reconciliação acha evento perdido

## 6. Alertas operacionais
- Fila pausada ou webhook desativado: [COMO É DETECTADO] · Expiração de credencial: [DATA E ALERTA]

## 7. Lacunas e riscos
- [O QUE NÃO FOI VERIFICADO] · Próximo passo: [AÇÃO]
