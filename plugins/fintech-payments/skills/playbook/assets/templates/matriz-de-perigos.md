# Matriz de perigos de idempotência e pagamento

Derivada de V-02 (matriz de perigos que **bloqueia aprovação** se um perigo crítico aplicável não tiver os quatro itens: prevenção, detecção, dono da recuperação e teste). Copie, marque a coluna "Aplica?" e preencha. Linhas pré-preenchidas são os perigos da lista de rejeição (`padroes-e-antipadroes.md`) e dos estados de pagamento; acrescente os do seu fluxo.

Regra de aprovação: **crítico + aplicável + qualquer célula de prevenção/detecção/dono/teste vazia = bloqueado.** Perigo não aplicável exige uma linha de motivo.

| ID | Perigo | Crit. | Aplica? | Prevenção | Detecção | Dono da recuperação | Teste | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| H-01 | Cobrança dupla por retry/duplo clique | crítico | [sim/não + motivo] | [constraint `(escopo, chave)`; chave por intenção] | [alerta de duas cobranças por `order_id`] | [time de pagamentos + suporte] | [duplo clique, timeout+retry; contagem de linhas] | [ ] |
| H-02 | Mesma chave, corpo diferente aceito | crítico | [ ] | [fingerprint canônico] | [log de conflito] | [ ] | [R$ 100 depois R$ 150] | [ ] |
| H-03 | Timeout tratado como falha | crítico | [ ] | [estado `indeterminate` + consulta ao provedor] | [métrica de indeterminados] | [ ] | [timeout com sucesso tardio] | [ ] |
| H-04 | Chave nova a cada retry | crítico | [ ] | [chave persistida antes; fora do loop] | [revisão de código] | [ ] | [mesma chave em todas as tentativas] | [ ] |
| H-05 | Cache em memória / lock distribuído como única proteção | crítico | [ ] | [constraint no banco] | [auditoria de duplicatas] | [ ] | [duas instâncias concorrentes] | [ ] |
| H-06 | Retenção da chave menor que a janela de retry | alto | [ ] | [retenção ≥ janela do cliente e do provedor; tombstone] | [alerta de retry após expiração] | [ ] | [retry depois da expiração] | [ ] |
| H-07 | Webhook duplicado causa dois efeitos | crítico | [ ] | [inbox com unicidade do ID do evento] | [contador de duplicatas] | [ ] | [mesmo evento duas vezes] | [ ] |
| H-08 | Webhook forjado muda estado | crítico | [ ] | [assinatura sobre corpo bruto; V-50 se sem assinatura] | [4xx contabilizados] | [ ] | [assinatura forjada, corpo alterado] | [ ] |
| H-09 | Eventos fora de ordem corrompem o estado | alto | [ ] | [releitura + UPDATE condicional] | [transições inválidas na conciliação] | [ ] | [ordem invertida] | [ ] |
| H-10 | Mesmo ID de evento com digest diferente | alto | [ ] | [quarentena] | [alerta de quarentena] | [ ] | [digest divergente] | [ ] |
| H-11 | Pedido liberado por redirecionamento do cliente | crítico | [ ] | [evento verificado + consulta] | [pedidos "pagos" sem evento] | [ ] | [retorno forjado] | [ ] |
| H-12 | Sucesso tardio depois de retry sem compensação | alto | [ ] | [compensação registrada no ledger] | [conciliação] | [ ] | [sucesso após timeout] | [ ] |
| H-13 | Saldo negativo por corrida | crítico | [ ] | [`UPDATE ... WHERE saldo - x >= 0`] | [auditoria de reconstrução] | [ ] | [dois débitos de R$ 80 em R$ 100] | [ ] |
| H-14 | Estorno acima do original | crítico | [ ] | [saldo estornável] | [consulta de soma de estornos] | [ ] | [dois parciais acima do original] | [ ] |
| H-15 | Fonte de conciliação incompleta tratada como completa | alto | [ ] | [manifesto; `INCOMPLETE_SOURCE`] | [contagem vs cursor] | [ ] | [paginação truncada] | [ ] |
| H-16 | PAN/CVV/token/chave em log | crítico | [ ] | [redação; allowlist de campos] | [regex + Luhn nos logs de teste] | [ ] | [busca de PAN em logs] | [ ] |
| H-17 | Armazém de idempotência indisponível | alto | [ ] | [fail-closed ou fail-open com confirmação humana] | [alerta] | [ ] | [armazém fora] | [ ] |
| H-18 | Lease sem fencing (worker antigo escreve) | alto | [ ] | [fencing token] | [log de token rejeitado] | [ ] | [worker lento] | [ ] |
| H-19 | Idempotência do provedor assumida sem fonte | alto | [ ] | [matriz por provedor; "não documentado"] | [revisão] | [ ] | [n/a: pergunta ao fornecedor] | [ ] |
| H-20 | Agente aciona efeito financeiro sem confirmação | crítico | [ ] | [confirmação por ação; limites no código] | [log de confirmações] | [ ] | [pedido de reembolso em payload] | [ ] |
| H-21 | [seu perigo] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |

Legenda de status: **ok** (os quatro presentes e testados), **bloqueado** (crítico aplicável incompleto), **n/a** (motivo registrado). Sem teste executado, o status é **Não verificado**, não ok.
