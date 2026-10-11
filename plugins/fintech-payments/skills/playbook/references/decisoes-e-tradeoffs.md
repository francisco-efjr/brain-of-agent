# Decisões e trade-offs em pagamentos

Cada decisão traz opções, critério, recomendação do plugin (quando há) e condição de revisão. Use `assets/templates/adr-pagamentos.md` para registrar a que for material. Onde duas fontes divergem, a tabela de conflitos (seção 2) mostra a resolução adotada. O plugin **não recomenda marca** de PSP, ledger ou antifraude sem critérios do usuário.

## Sumário

1. Decisões de desenho
2. Conflitos entre fontes e resolução (K1 a K12)
3. Como decidir o que é material
4. Gotchas

## 1. Decisões de desenho

### D1. Estado atual x snapshot por efeito (webhook)

| Opção | Benefício | Custo/risco | Quando |
| --- | --- | --- | --- |
| Reler o recurso (estado atual) antes de agir | converge com eventos fora de ordem e duplicados; resiste a payload forjado | uma chamada extra por evento; depende da API do provedor | padrão para estado de pagamento (V-03, V-05) |
| Usar o snapshot do evento | sem chamada extra | pode estar obsoleto, forjado ou fora de ordem | só para efeito que depende do instante (ex.: auditar o que foi dito), nunca para mudar estado financeiro sozinho |

Recomendação: escolher **por efeito**, documentar e usar estado atual para dinheiro. Revisar se o limite de taxa da API do provedor impedir a releitura (então: fila com backoff, não snapshot).

### D2. Armazém de idempotência fora do ar: fail-closed x fail-open

| Opção | Benefício | Custo/risco |
| --- | --- | --- |
| **Fail-closed**: pausar/recusar a operação | nenhuma cobrança sem proteção | indisponibilidade da compra |
| **Fail-open**: seguir sem a proteção | disponibilidade | risco de duplicata |

Recomendação (V-01, Adyen 503/703): pausar e tentar de novo; operar sem a proteção só com **confirmação humana registrada** e conciliação reforçada no dia. Revisar quando o armazém tiver SLA mensurável.

### D3. `txid` do Pix: gerado pelo sistema x pelo PSP

| Opção | Benefício | Custo/risco |
| --- | --- | --- |
| Sistema envia o `txid` (26 a 35, único por recebedor, nunca reutilizado) | **idempotência da cobrança** garantida; reconciliação direta | exige gerar e persistir antes da chamada |
| PSP gera (só cobrança imediata) | menos código | idempotência **não** garantida após falha de chamada |

Recomendação: sistema gera (Manual v2.10.0 seção 5.3, V-44, Verificado). Se o PSP gerar, registre a limitação no ADR.

### D4. Ledger próprio x serviço de ledger

| Opção | Benefício | Custo/risco | Evidência |
| --- | --- | --- | --- |
| Tabelas próprias no banco da aplicação | controle total; transação única com o domínio; sem nova dependência | você garante invariantes (soma zero, append-only, saldo sob concorrência) | padrão do plugin (Inferido) |
| Banco/serviço de ledger (TigerBeetle, Formance, Modern Treasury, entre outros) | invariantes embutidos; performance de transferências | nova dependência operacional; escala do ativo difícil de mudar (TigerBeetle); modelo e idempotência variam por produto | TigerBeetle Verificado; Modern Treasury visão geral; Formance sem idempotência confirmada |

Critérios do usuário que decidem: volume de transferências por segundo, número de contas quentes, auditoria exigida, equipe operacional, necessidade de multi-moeda. O plugin não nomeia vencedor. Revisar quando a contenção em contas quentes ou o custo de manter invariantes superar o de uma dependência nova. Para escolha de banco, aprofunde em `/database-data-modeling:playbook`; arquitetura ampla, `/architecture-design:playbook`.

### D5. Saldo derivado x projeção persistida

| Opção | Benefício | Custo/risco |
| --- | --- | --- |
| Derivado a cada leitura | sempre correto | caro em contas com muito histórico |
| Projeção (tabela de saldos atualizada na transação dos lançamentos) | leitura barata; dá para impor `balance >= 0` com `UPDATE` condicional | precisa de política de invalidação e de reconstrução; auditoria agendada compara projeção x histórico |

Recomendação (Inferido, V-11): projeção atualizada **na mesma transação** + auditoria periódica de reconstrução. Lock somente em contas quentes.

### D6. Pix: cobrança imediata (`cob`) x com vencimento (`cobv`)

| Opção | Quando | Observação |
| --- | --- | --- |
| `cob` | pagamento na hora (checkout, QR dinâmico) | expiração em segundos; `txid` próprio |
| `cobv` | fatura com vencimento, juros, multa, desconto (Anexo III) | o mesmo `txid` não vale para `cob` e `cobv`; data limite de desconto em fim de semana vai ao primeiro dia útil seguinte |

### D7. Webhook x consulta periódica (polling)

Use **webhook para reatividade e consulta/conciliação para completude**; nenhum dos dois sozinho. Webhook perde evento (provedor pausa a fila, janela de retry acaba — Asaas pausa após 15 falhas, guarda 14 dias); polling atrasa e consome limite. A cadência da conciliação deve ser menor que a menor janela de reenvio/retenção em uso (V-67, Inferido).

### D8. SDK oficial x verificação manual de assinatura

Prefira o SDK oficial quando o manifesto não é documentado (Mercado Pago: **não** implemente HMAC manual até ler a especificação, V-04). Para Stripe e Adyen, o esquema é documentado: SDK ou implementação própria testada com vetores locais. Nunca "algoritmo genérico" (V-47).

### D9. Webhook em hospedagem sem mTLS (Pix/Efí)

| Opção | Risco |
| --- | --- |
| mTLS no seu endpoint | exige terminar TLS mútuo (proxy/ingress) |
| skip-mTLS com restrição de IP **e** HMAC na URL (usados em conjunto) | a Efí ainda envia o certificado; você deve garantir o remetente; IP muda: ler a doc vigente (V-53) |

Recomendação: mTLS quando possível; skip-mTLS apenas com os dois controles e o risco registrado no ADR.

### D10. 3DS: quando pedir

Por regulação (SCA/PSD2 e regimes semelhantes), soft decline do emissor, regra de risco. Em regiões onde é opcional, decida por risco e valor; mais atrito reduz conversão. Não há como desligar 3DS por API na Stripe. Nunca prometa liability shift (V-39, V-49). Brasil: regras de bandeira não verificadas.

### D11. Marketplace: tipo de conta e risco de fraude (Stripe Connect, V-41)

O dono da plataforma responde por fraude e disputas de contas **Express** e **Custom**; **Standard** minimiza o risco; onboarding hospedado reduz carga. Escolha o tipo com consciência do risco assumido. A mecânica financeira do split (lançamentos por recebedor, estorno e chargeback proporcionais, conciliação do repasse) é **Inferido** por falta de fonte V; regras comerciais do split (comissão, onboarding de seller) pertencem a `/ecommerce-marketplace:marketplace-split`.

### D12. Chargeback: aceitar x defender

Defender custa tempo e, no Adyen, pode escalar a pré-arbitragem/arbitragem (taxa de até USD 600); aceitar encerra em `Lost`. Registre a decisão com motivo e data; após `information_supplied` não se alteram documentos. Remova PAN e dados sensíveis do material. Prazos por bandeira: conferir.

### D13. Confirmação humana x autonomia do agente

Limiar de pergunta **baixo** para ferramenta que move dinheiro, **alto** para consulta. Instrução de autonomia ("não pergunte") não suspende a confirmação por ação. Limites de gasto e permissões são controle técnico (V-16, V-17).

## 2. Conflitos entre fontes e resolução

| # | Conflito | Posições | Resolução | Fonte |
| --- | --- | --- | --- | --- |
| K1 | Retenção da chave de idempotência | Stripe ≥ 24 h; Adyen 7 a 14 dias | tabela por provedor; nunca janela universal | V-01 |
| K2 | Onde está a assinatura e o que se assina | Stripe: header, `timestamp.payload`; Adyen padrão: no corpo, campos concatenados; Adyen outros: header `hmacsignature`; Mercado Pago: manifesto não documentado; Pagar.me: não documentada | matriz por provedor; "não documentado" onde for o caso; regra V-50 | V-03, V-47, V-04, V-37 |
| K3 | Representação de valor | Stripe/TigerBeetle: inteiro; Pix: string decimal; moneyproof: "decimal ou inteiros, nunca números JSON" (autocontraditória) | interno inteiro + ISO 4217; borda converte; "nunca ponto flutuante no JSON" | V-10, V-13, V-43 |
| K4 | Quem gera o `txid` | recebedor (idempotência) x PSP (sem idempotência) | preferir o sistema | V-44 |
| K5 | "Partida dobrada" e atomicidade | Formance/medici: múltiplos lançamentos somam zero; TigerBeetle: um débito, um crédito | pares débito/crédito atômicos no mesmo ledger e moeda; "soma zero" rotulada Inferido | V-11, V-46 |
| K6 | Chave em variável de ambiente | Stripe: cofre, env só como último recurso; prática comum: env | cofre quando houver; senão env; nunca código/log/cliente | V-41 |
| K7 | Exclusões padrão do security-review | exclui DoS, rate limiting, validação genérica, open redirect | instruções reincluem rate limiting e abuso de endpoint de pagamento/login/cartão | V-22 |
| K8 | Idempotência explícita x implícita no prompt | Clean-Backend removeu; falhou em modelo menor | sempre explícita em dinheiro | V-28 |
| K9 | Reembolso automático diante de EFW | ~40% viram disputa sem reembolso x "reembolsar tudo não é boa estratégia" | classificar caso a caso e registrar | V-09 |
| K10 | Fontes de confirmação financeira | OpenAI (arquivado, C) x Paymob (B) e Anthropic (permissões) | regra apoiada em Paymob e Anthropic | V-17 |
| K11 | Hooks de terceiros x plugin seguro | PagoKit, Mercado Pago, aitmpl executam shell | não instalar; documentar só o padrão genérico | V-19 |
| K12 | Números regulatórios do brain x manual do BCB | brain: R$ 1.000 noturno, R$ 200 dispositivo novo, MED 80 dias, agendamento 2 a 10 dias; manual v2.10.0 não os contém; spec: janela "hoje 90 dias" | herdados = "seed a confirmar"; 90 dias = "conferir na versão vigente" | V-33, V-44 |

## 3. Como decidir o que é material

Registre ADR quando a decisão: (1) muda o modelo de dados financeiro; (2) é cara de reverter (escala do ativo, escolha de ledger); (3) cria dependência de provedor; (4) assume risco regulatório; (5) abre exceção a um invariante (fail-open, skip-mTLS). Tudo o mais: decisão local no PR, com o motivo na descrição. Cada ADR: ≥ 2 opções, consequências, rótulos, verificação, condição de revisão, e a **versão e data de leitura** das especificações (V-70).

## 4. Gotchas

- Ledger de fabricante (TigerBeetle) não é regra geral; "soma zero" é derivação.
- A escala do ativo é difícil de mudar depois (TigerBeetle): decida cedo e com margem.
- "Ledger próprio" não dispensa auditoria de reconstrução.
- Não troque de PSP no meio de um incidente: a retenção e o esquema de assinatura mudam.
