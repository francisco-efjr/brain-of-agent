# Checklist completo de pagamentos

Use por operação. Cada item tem ID, severidade se falhar (C = CRITICAL, W = WARNING), como detectar (leitura com Grep ou teste) e fonte. Itens sem fonte de fabricante levam **(I)** = Inferido. Marque cada item como **atendido (com `arquivo:linha`)**, **não atendido**, **Não verificado** ou **Não aplicável**. Nunca marque PASS sem evidência.

## Sumário

1. Como usar e escala de severidade
2. Cobrança (criar pagamento)
3. Captura e autorização
4. Estorno (refund)
5. Repasse e transferência (payout)
6. Pix (cobrança, pagamento, devolução)
7. Boleto
8. Receptor de webhook
9. Checklist de serviço (qualquer backend de pagamento)
10. Trilha de auditoria
11. Casos mínimos de teste com oráculo
12. Gates de entrega

## 1. Como usar e escala

- **CRITICAL**: explorável ou perde/duplica dinheiro; corrigir antes do merge. **WARNING**: corrigir na sprint. **PASS**: verificado, com a evidência. **Não verificado**: não conseguiu verificar; nunca em PASS (V-15, V-26, V-35).
- Em dúvida, não reporte como CRITICAL: rebaixe para "Não verificado" e diga o que faltou (C-15).
- Regras de provedor só valem se o código usar aquele provedor, e com aviso de conferir a documentação atual.

## 2. Cobrança (criar pagamento)

| ID | Item | Sev. | Detecção | Fonte |
| --- | --- | --- | --- | --- |
| CB-01 | Chave de idempotência gerada uma vez por intenção de negócio e persistida **antes** da chamada | C | Grep `Idempotency-Key`/`idempotency`; chave criada fora do loop de retry | V-01, V-02 |
| CB-02 | Reserva atômica por constraint de unicidade no escopo (conta + operação + chave), não "checar e inserir" | C | tabela com `PRIMARY KEY`/`UNIQUE`; teste de duas requisições concorrentes | V-02 |
| CB-03 | Mesma chave com corpo diferente gera conflito registrado | C | teste com R$ 100,00 e depois R$ 150,00 | V-01, V-33 |
| CB-04 | Timeout tratado como desconhecido: consulta ao provedor antes de reenviar; sem chave nova | C | revisar o `catch` de timeout | V-12 |
| CB-05 | Valor inteiro na menor unidade + moeda ISO 4217; sem float; mínimo e máximo por moeda validados | C | Grep `float`, `parseFloat`, `* 100`, `Number(`; tipo da coluna | V-10 |
| CB-06 | Referência externa (`order_id`) em todo pedido | W | campo na criação | V-15 |
| CB-07 | Chamada externa fora de transação com lock; intenção persistida e commit antes de chamar | C | chamada HTTP dentro de `BEGIN ... COMMIT` | V-11 (I) |
| CB-08 | Pedido só vira pago por evento verificado + releitura; nunca por redirecionamento do cliente | C | rota de retorno (`return_url`/`back_url`) consulta a API | V-14, V-15 |
| CB-09 | Autorização: usuário só cria cobrança no próprio recurso (IDOR) | C | teste com dois usuários | V-26 (I) |
| CB-10 | Rate limiting e limite de tentativas de cartão | W | middleware no endpoint | V-22 |
| CB-11 | Resposta sensível reexibida (replay) só após reautorizar; sem PAN/token em `response` salvo | W | colunas da tabela de idempotência | V-02 |

## 3. Captura e autorização

| ID | Item | Sev. | Detecção | Fonte |
| --- | --- | --- | --- | --- |
| CA-01 | Estados separados: autorizado, capturado, liquidado; valores autorizado/capturado/estornado fora do status | W | modelo de dados | V-12 |
| CA-02 | Captura com chave de idempotência própria | C | header na captura | V-01 |
| CA-03 | Captura parcial e múltipla: soma ≤ autorizado | C | teste | V-33 |
| CA-04 | Janela de captura do provedor conhecida (conferir) e expiração tratada com `void` no ledger | W | config; documentação do provedor | V-46 (I) |
| CA-05 | 3DS: resultado, ECI e fluxo guardados por tentativa; nenhuma promessa de liability shift em UI/contrato | W | colunas; Grep "responsabilidade", "chargeback" em textos | V-39, V-49 |
| CA-06 | Pedido não fica "pago" sem autenticação concluída, nem preso em "aguardando" | W | teste: desafio abandonado, timeout | brain |
| CA-07 | Autenticação 3DS de carteira/off-session tratada (pode não suportar) | W | caminho de erro | V-39 |

## 4. Estorno (refund)

| ID | Item | Sev. | Detecção | Fonte |
| --- | --- | --- | --- | --- |
| ES-01 | Chave de idempotência no estorno | C | header | V-01, V-57 |
| ES-02 | Saldo estornável controlado: parcial reduz; soma acima do original recusada | C | teste: dois parciais somando mais que o original | V-33 |
| ES-03 | Estorno = lançamento ligado ao original (nunca `DELETE`/`UPDATE` de pagamento) | C | Grep `DELETE FROM payments` | V-11, V-46 |
| ES-04 | Autorização por objeto e reautenticação em estorno | C | teste IDOR; fluxo de reauth (I) | V-26 (I) |
| ES-05 | Disputa aberta bloqueia estorno manual fora do processo | W | consulta ao estado da disputa antes de estornar | V-09 |
| ES-06 | Pix: `id` de devolução por `e2eid`; janela da spec vigente | C | Grep `devolucao` | V-43, V-48 |
| ES-07 | Webhook de estorno com dedupe e releitura | C | ver seção 8 | V-03 |
| ES-08 | Estorno conciliado contra o extrato | W | relatório de conciliação | V-07 |
| ES-09 | "Reembolsar tudo automaticamente" diante de alerta antecipado não é regra fixa: decisão registrada caso a caso | W | política do produto | V-09 |

## 5. Repasse e transferência (payout)

| ID | Item | Sev. | Detecção | Fonte |
| --- | --- | --- | --- | --- |
| RP-01 | Idempotência por repasse; reexecução do job não duplica | C | teste: rodar o job duas vezes | V-01, brain |
| RP-02 | Confirmação humana por ação com conta, modo, operação, valor e moeda quando um agente aciona | C | fluxo de aprovação | V-14, V-17 |
| RP-03 | Limites de valor e de frequência por controle técnico, não por prompt | C | validação no código | V-16 |
| RP-04 | Payout conciliado linha a linha (`balance_transactions` por payout; paginação completa) | W | relatório | V-07 |
| RP-05 | Payouts manuais conciliados pela empresa | W | processo | V-07 |
| RP-06 | Marketplace: lançamentos por recebedor, estorno e chargeback proporcionais (mecânica do split, **Inferido**) | W | ledger | revisão do crítico |

## 6. Pix (cobrança, pagamento, devolução)

Use o checklist de 8 itens de `pix-boleto-cartao-br.md` (V-48) e acrescente:

| ID | Item | Sev. | Detecção | Fonte |
| --- | --- | --- | --- | --- |
| PX-01 | `txid` gerado no sistema (26 a 35 alfanuméricos), único, nunca reutilizado | C | Grep `txid` | V-44 |
| PX-02 | `valor.original` string decimal `\d{1,10}\.\d{2}`; conversão na borda; sem float | C | testes `"10.00"`, `"10.0"`, `"10.001"` | V-43 |
| PX-03 | Webhook autenticado conforme o PSP (mTLS); dedupe por `e2eid`; releitura antes de creditar | C | seção 8 | V-53, V-54 |
| PX-04 | Timeout: consultar `txid` (cobrança) ou `EndToEndId` (pagamento) antes de reenviar | C | `catch` | V-12, V-33 |
| PX-05 | BR Code: CRC16 validado antes de exibir; dinâmico sem valor/`txid`; não tratado como de uso único | W | função de validação; teste com payload alterado | V-65 |
| PX-06 | Números regulatórios (limites, MED, Pix Automático) configuráveis e rotulados "seed a confirmar" | W | Grep valores fixos `1000`, `200`, `80` | V-33, V-64 |
| PX-07 | Versão e data de leitura da spec/manual registradas | W | comentário/ADR | V-70 (I) |

## 7. Boleto

| ID | Item | Sev. | Detecção | Fonte |
| --- | --- | --- | --- | --- |
| BL-01 | Cada `limit_date` de desconto anterior ao vencimento (validação local) | W | teste | V-36 |
| BL-02 | Juros e multa só se o contrato com o PSP permitir | W | config | V-36 |
| BL-03 | Gravar `due_at` e `nosso_numero` **devolvidos** | W | persistência | V-36 |
| BL-04 | Linha digitável é texto (zeros à esquerda); buscar de novo se valor/vencimento mudar | W | tipo da coluna; fluxo | V-52, brain |
| BL-05 | Não liberar produto na criação; esperar confirmação de pagamento | C | fluxo de entrega | V-52 |
| BL-06 | Timeout: consultar cobranças existentes antes de recriar | C | `catch` | V-52 (I) |
| BL-07 | Boleto vencido há mais de 60 dias (Pagar.me): nova cobrança | W | política | V-36 |
| BL-08 | Fator de vencimento com reinício de 2025 tratado (**Não verificado** contra norma) | W | teste 21/02 e 22/02/2025 | brain |
| BL-09 | Horário devolvido testado contra o fuso do negócio | W | teste | V-36 |

## 8. Receptor de webhook

| ID | Item | Sev. | Detecção | Fonte |
| --- | --- | --- | --- | --- |
| WH-01 | Assinatura verificada sobre o **corpo bruto** antes de parsear; tolerância > 0 | C | middleware de JSON antes da rota? `JSON.stringify(req.body)`? | V-03 |
| WH-02 | Provedor sem assinatura documentada: tratado como não autenticado, só ID aceito, releitura | C | tabela de provedores | V-50 |
| WH-03 | Dedupe persistido por ID do evento (constraint); não em memória | C | `Set` local? | V-03, V-05 |
| WH-04 | Mesmo ID, digest diferente → quarentena | W | coluna `digest` | V-05 |
| WH-05 | 2xx antes de lógica pesada; fila; varredura | W | fluxo | V-03 |
| WH-06 | Releitura do recurso antes de agir; ordem não confiável (`created`) | C | handler | V-03 |
| WH-07 | Segredo por endpoint e por modo; rotação com janela; comparação em tempo constante | W | config | V-03, V-47 |
| WH-08 | Rota isenta de CSRF | W | middleware | V-03 |
| WH-09 | Log sem payload sensível; ID de correlação | W | logs | V-23 |
| WH-10 | Roteiro de testes hostis existe e foi executado (ou "Não executado") | W | suíte | V-05, V-06 |

## 9. Checklist de serviço (qualquer backend de pagamento; Clean-Backend, V-28)

| ID | Item | Sev. | Detecção |
| --- | --- | --- | --- |
| SV-01 | Prazo (timeout) em toda chamada de E/S, inclusive banco | C | Grep clientes HTTP/DB sem timeout |
| SV-02 | Circuit breaker **antes** de retry; retry só em operação idempotente, com backoff e jitter | W | config de retry |
| SV-03 | Tombstones filtrados em toda leitura (registros "apagados" logicamente) | W | consultas |
| SV-04 | Trabalho não aguardado fora do caminho da requisição (fila/outbox) | W | handlers |
| SV-05 | Contadores emitidos: falha de webhook, divergência de conciliação, fila pausada | W | métricas |
| SV-06 | Rotas versionadas desde o início; deploy separado de liberação | W | rotas/flags |
| SV-07 | Idempotência **explícita** no prompt e no checklist (modelo menor falha onde o maior acerta) | C | revisão do prompt do agente |
| SV-08 | Segredos só em cofre/variável de ambiente; `.env` ignorado | C | `.gitignore`; Grep de chaves |

## 10. Trilha de auditoria (cobre o item "auditoria" do escopo)

| ID | Item | Sev. | Detecção | Fonte |
| --- | --- | --- | --- | --- |
| AU-01 | Cada transição de estado registra quem, quando, origem (comando/evento/consulta/extrato), evidência e motivo | C | tabela de eventos/estados | V-12, V-13 |
| AU-02 | Ajuste de conciliação e estorno manual: classificação, revisão, aprovação humana vinculada | C | relatório de conciliação | V-08 |
| AU-03 | ID de correlação ponta a ponta (pedido → intenção → tentativa → evento → ledger) | W | logs/colunas | V-13, V-23 |
| AU-04 | Logs sem PAN, CVV, token, chave; sanitizados contra log injection | C | regex + Luhn nos logs de teste | V-23 |
| AU-05 | Trilha imutável (append-only; sem UPDATE/DELETE para o app) | C | permissões do banco | V-11 (I) |
| AU-06 | Acesso a dado sensível, uso e rotação de chave, import/export registrados | W | logs | V-23 |
| AU-07 | Retenção definida (conferir norma; o Manual do Pix exige ao PSP logs de API por pelo menos 1 ano — não transponha sem ler) | W | política | V-44; **Não verificado** |
| AU-08 | Ações de agentes (quem pediu, qual confirmação) registradas | W | log de confirmações | V-17 (I) |

## 11. Casos mínimos de teste com oráculo (brain-of-agent, `dominios.md`, MIT, adaptado; números regulatórios Não verificados)

O defeito caro aqui é silencioso e aparece na conciliação semanas depois. **O oráculo é um cálculo independente ou o extrato da outra ponta, nunca o valor que o próprio sistema mostra.**

| Risco | Caso | Esperado | Oráculo |
| --- | --- | --- | --- |
| Cobrança dupla | duplo clique; reenviar com a mesma chave; timeout seguido de retry | uma cobrança; a segunda chamada devolve o resultado da primeira | contagem de linhas no banco |
| Chave mal escopada | mesma chave com corpo diferente | recusa explícita (conflito) | linha de conflito registrada |
| Arredondamento | R$ 100,00 em 3 parcelas; R$ 10,00 rateado em 3 itens | 33,34 + 33,33 + 33,33; soma igual ao total | cálculo independente |
| Float | `0.1 + 0.2` em cálculo de valor | inteiros ou decimal exato | teste de propriedade |
| Regra de arredondamento | juros de 1% a.m. sobre R$ 333,33 por 17 dias | conferido por planilha com a regra escrita | planilha |
| Conciliação | pedido pago x liquidação no extrato | casa por ID; divergência gera alerta | extrato do provedor |
| Estorno | total, parcial, dois parciais acima do original | parcial reduz o saldo estornável; soma acima recusada | ledger |
| Chargeback | contestação depois do repasse | débito registrado, pedido marcado, prazo visível | ledger + disputa |
| Limites | limite diário R$ 5.000,00: 4.999,99 + 0,01; depois 0,01 | aceita até 5.000,00; recusa 5.000,01 com mensagem do limite | regra escrita |
| Virada do limite | 23:59:59 e 00:00:00 no fuso do cliente | contador zera no fuso da regra (em geral America/Sao_Paulo) | relógio fixo |
| Antifraude | 10 tentativas em 1 minuto com cartões diferentes no mesmo dispositivo | bloqueio ou desafio; caminho de recuperação | log do motor |
| Concorrência de saldo | dois débitos de R$ 80,00 em conta com R$ 100,00 | um aprova, um recusa; saldo nunca negativo | saldo derivado do histórico |

Armadilhas: testar o retry sem contar linhas; `float` no próprio teste; esquecer que o webhook também chega duplicado e fora de ordem (`pagamento.aprovado` antes de `pagamento.criado`). Teste de mutação manual: desligue a constraint e confirme que o teste de retry falha.

## 12. Gates de entrega

Mude para "pronto" só se: nenhum CRITICAL aberto; cada PASS com evidência; "Não verificado" listado com o que conferir; revisão do mesmo modelo declarada como não independente; versões e datas de especificações registradas; nenhum segredo ou PAN em evidência. Caso contrário, veredito "precisa de ajustes", "bloqueado" ou "parcial" (`assets/templates/relatorio-revisao-pagamentos.md`).
