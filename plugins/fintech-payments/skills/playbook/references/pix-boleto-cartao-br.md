# Pix, boleto, cartão e Open Finance (Brasil)

Base: V-31, V-33, V-36, V-38, V-43, V-44, V-45, V-48, V-52, V-53, V-54, V-64, V-65, V-69 e o brain-of-agent (`dominios.md`, MIT). **Regra do segmento:** o que não está marcado Verificado aqui é Inferido, herdado do brain ("seed a confirmar no regulamento vigente do BCB") ou Não verificável. Nenhum número regulatório abaixo é oráculo de teste sem conferir a fonte vigente. Redação própria; código do plugin (MIT).

## Sumário

1. Pix: o que está verificado
2. Checklist de integração Pix (8 itens, V-48)
3. Schemas e valores
4. Devolução e MED
5. Webhook e notificação Pix
6. Segurança do PSP (Anexo II)
7. BR Code (Pix copia e cola) e CRC16
8. Números herdados (seed a confirmar)
9. Boleto
10. Cartão
11. Open Finance Brasil
12. Gotchas

## 1. Pix: o que está verificado

Fontes de classe A: spec OpenAPI oficial `bacen/pix-api` (Apache-2.0, versão 2.10.0, V-31, V-43) e **Manual de Padrões para Iniciação do Pix v2.10.0** (123 páginas, metadados de 19/08/2026, V-44). A API é a **especificação funcional** (cobrança imediata `cob`, com vencimento `cobv`, recorrência, devolução, webhook); a segurança fica nos manuais. **Não obtidos**: Manual de Segurança do Pix, Regulamento Pix (limites, DICT), IN BCB 766, Manual do BR Code (arranjos do SPB). Versão e data de leitura: registre no código e no ADR (SN-21).

## 2. Checklist de integração Pix (V-48, derivado de V-31, V-43, V-44; itens 5 e 6 combinam com V-01 e V-33, parte Inferido)

| # | Item | Marque: atendido / não / Não verificado + ponto do código |
| --- | --- | --- |
| 1 | `txid` gerado no sistema: 26 a 35 caracteres alfanuméricos, único por recebedor, **nunca reutilizado** (nem após cancelamento ou baixa); mapeamento com o pedido persistido **antes** de chamar o PSP. Se o PSP gerar o `txid`, registre que a idempotência não está garantida | |
| 2 | Decisão `cob` x `cobv` antes de codificar; o mesmo `txid` não vale para os dois | |
| 3 | Valor como **string decimal** com duas casas (`10.00`); conversão de e para inteiro na borda; zero é erro (exceto Pix Saque) | |
| 4 | Devolução: `id` (1 a 35) por `e2eid`; recusar acima do saldo estornável e fora da janela da spec vigente (90 dias na 2.10.0, **conferir**); acompanhar o status até `DEVOLVIDO` ou `NAO_REALIZADO` | |
| 5 | Webhook: callback só avisa Pix com `txid` e devoluções finalizadas; responder 200; deduplicar por `e2eid`; reler a cobrança na API; conciliar por extrato; mTLS conforme o PSP | |
| 6 | Timeout ao criar a cobrança: consultar pelo `txid` antes de reenviar | |
| 7 | Segurança: TLS 1.2+, OAuth 2.0 com mTLS (token vinculado ao certificado), certificado fora do código e do log, rotação planejada | |
| 8 | Limites, MED e Pix Automático: não codificar números sem ler Regulamento e Manual vigentes | |

## 3. Schemas e valores (V-43, A; lidos no `openapi.yaml` 2.10.0)

| Campo | Regra |
| --- | --- |
| `TxId` da cobrança | `[a-zA-Z0-9]{26,35}`, criado exclusivamente pelo recebedor, único por CPF/CNPJ do recebedor, validado pelo PSP. O padrão `{1,35}` aparece só no filtro de consulta e no campo `txid` do Pix recebido (QR estático não passa pela API) |
| `EndToEndId` | 32 alfanuméricos. Composição `E` + ISPB (8) + `AAAAMMDDHHmm` em UTC + 11 alfanuméricos: **herdada do brain, Não verificada** — teste o parse (hora em UTC, não em Brasília) e use-o como chave de conciliação |
| `DevolucaoId` | `[a-zA-Z0-9]{1,35}`, gerado pelo cliente; único por `e2eid` |
| Valores (`cob.valor.original`, `cobv.valor.original`, `Devolucao.valor`, `Pix.valor`) | strings decimais `\d{1,10}\.\d{2}` |
| Valor zero | `PUT/PATCH /cob/{txid}` e `cobv`: `valor.original` igual a zero → 400 `CobOperacaoInvalida`; expiração menor ou igual a zero também. Exceções: Pix Saque exige `valor.original` 0.00; Pix Troco exige maior que 0.00 |
| Valor do Pix | soma de original, saque e troco, mais multa e juros, menos abatimento e desconto |
| Chave DICT | no máximo 77 caracteres |
| CNPJ | schemas aceitam `^[0-9A-Z]{14}$` (alfanumérico) desde a 2.9.0; a data de julho de 2026 (herdada) **não foi confirmada** |
| Devolução, objeto | obrigatórios `id`, `rtrId` (32), `valor`, `horario`, `status`; `descricao` até 140 |

Cálculo de abatimento, desconto, juros e multa de `cobv` está no Anexo III do Manual; data limite de desconto em fim de semana ou feriado vai ao primeiro dia útil seguinte. Teste: pagar antes, no dia e depois do vencimento; vencimento em feriado municipal (o PSP do pagador envia data prevista de pagamento e código do município — brain, Não verificado).

## 4. Devolução e MED

- `PUT /pix/{e2eid}/devolucao/{id}`. Erro `PixDevolucaoInvalida` (400) se o `id` já foi usado para aquele `e2eid`, se a soma com devoluções anteriores passar do Pix original ou se estiver fora da janela "hoje estabelecida como 90 dias desde a liquidação" (texto da spec; **conferir na versão vigente**).
- **MED** (V-64): o voto BCB 7/2026 (20/01/2026) sustenta apenas definição e calendário: MED em vigor desde novembro de 2021 para devolução de Pix com fundada suspeita de fraude; a Resolução BCB 493 (28/08/2025) incorporou melhorias; adoção facultativa desde 23/11/2025 e obrigatória desde 02/02/2026; a minuta insere o art. 113-A (dispensa de apuração por descumprimentos do art. 121 entre 02/02 e 10/05/2026).
- **O prazo de 80 dias do MED segue Não verificável** (reportagens atribuem à IN BCB 766 a ampliação do prazo de contestação do recebedor de 30 para 80 dias a partir de 01/09/2026; nenhuma fonte oficial lida). Não publique como regra. Modele **dois prazos separados** (vítima e recebedor), cada um com `prazo_fonte` e `status` (`nao_verificado`), e deixe o valor configurável.
- Teste de regressão com data fixa só para a regra de penalidade (02/02 a 10/05/2026), não para o prazo de 80 dias.

## 5. Webhook e notificação Pix

- `PUT /webhook/{chave}` registra `webhookUrl`; **só Pix associados a um `txid` são notificados**; o PSP chama `POST {webhookUrl}/pix` para Pix com `txid` e para devoluções em status final; o SLA é do PSP e pode agrupar Pix de uma chave; o canal é protegido por mTLS; o recebedor responde 200.
- **Efí** (V-53): o servidor exige o certificado público da Efí; a Efí faz uma requisição sem certificado (recuse) e outra com; TLS 1.2 mínimo; `?ignorar=` evita o acréscimo de `/pix` à URL; `x-skip-mtls-checking` para hospedagem sem mTLS — então restrinja por IP e HMAC na URL (usados em conjunto), lendo o IP vigente na doc a cada integração; timeout de 60 s; reenvio manual `POST /v2/gn/webhook/reenviar`; corpo com array `pix` (`endToEndId`, `txid`, `chave`, `valor`, `horario`, `infoPagador`, opcional `gnExtras`). Registre o risco de usar skip-mTLS.
- **Checklist de recepção (V-54, Inferido):** (1) autenticar a origem conforme o PSP; (2) persistir o evento antes do 2xx; (3) deduplicar por `endToEndId` e `txid`; (4) **não creditar saldo só pela notificação**: reconsultar `txid` ou `EndToEndId` pela API autenticada; (5) tratar `gnExtras` como dado auxiliar (tarifa ou split), nunca como base de valor.

## 6. Segurança do PSP (Manual v2.10.0, Anexo II 3.1, V-44, A)

TLS 1.2 ou superior com forward secrecy; OAuth 2.0 (client credentials) com mTLS (RFC 8705), tokens vinculados ao certificado e conferência do thumbprint; sem certificados autoassinados do cliente; onboarding em ambiente logado com canal seguro; escopos por perfil; alta disponibilidade; confidencialidade e integridade em trânsito e repouso; **logs de auditoria por pelo menos 1 ano** (requisito do PSP, não transponha ao seu sistema sem ler a norma); `client_ID` vinculado ao CPF/CNPJ do recebedor; webhooks sobre canal mTLS. Recomendações do manual: OWASP API Security Top 10, CWE Top 25, análise periódica de vulnerabilidades, homologação de clientes, troca periódica de certificados e credenciais.

## 7. BR Code (Pix copia e cola) e CRC16 (V-65, A, Manual v2.10.0 seção 2)

- Baseado em EMV QR Code (modo apresentado pelo recebedor); GUI `br.gov.bcb.pix` nos IDs raiz 26 a 51; campo 63 (CRC16) com 4 caracteres, polinômio `0x1021`, valor inicial `0xFFFF`, calculado **incluindo "6304"** (ID e tamanho); a ordem dos objetos altera o CRC.
- **Estático**: chave DICT válida obrigatória; `txid`, texto livre e valor opcionais; a criação do QR estático não faz parte da API Pix. **Dinâmico**: subcampo 25 com a URL (1 a 77 caracteres) do payload JSON; **valor e `txid` não devem ser preenchidos e, se estiverem, são ignorados** (prevalece o payload da URL); **um mesmo BR Code dinâmico pode ser reutilizado para vários pagamentos** — a unicidade fica no `txid` da cobrança.
- Valide o CRC **antes de exibir**. O copia e cola prova integridade, não a identidade do recebedor (**Inferido**): confira chave e nome pelo DICT ou pela API do PSP.

```python
def crc16_ccitt_false(s: str) -> str:
    crc = 0xFFFF
    for ch in s.encode("ascii"):
        crc ^= ch << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
    return f"{crc:04X}"

def br_code_ok(payload: str) -> bool:
    return len(payload) > 8 and payload[-8:-4] == "6304" and crc16_ccitt_false(payload[:-4]) == payload[-4:].upper()
```

Conferido pelo construtor (2026-10-11): `crc16_ccitt_false("123456789") == "29B1"` (valor de verificação padrão do CRC-16/CCITT-FALSE). O exemplo do Manual (seção 2.6.3, CRC `1D3D`) foi reproduzido pelo validador (V-65); **o payload não é copiado aqui**: use-o como vetor positivo e uma versão com um caractere alterado como negativo (o validador obteve `4438` ao alterar um caractere).

## 8. Números herdados do brain (seed a confirmar no regulamento vigente do BCB)

**Não aparecem no Manual de Iniciação v2.10.0 e não têm fonte lida**: limite noturno de R$ 1.000,00 (20h às 6h; cliente pode mudar o início para 22h; aumento vale após 24 a 48 h, redução é imediata); R$ 200,00 por transação e R$ 1.000,00 por dia em dispositivo novo; MED de 80 dias; agendamento do Pix Automático 2 a 10 dias antes; 5 chaves por conta de pessoa física e 20 por pessoa jurídica; tipos de chave (CPF 11 dígitos, CNPJ 14 posições, e-mail até 77, telefone `+5511987654321`, aleatória UUID de 36); `txid` do QR estático até 25 caracteres (ou `***`); timeout de 30 s. Use como caso de teste rotulado, nunca como regra de produto. Pix Automático: a IN BCB 746 e a Resolução BCB 402 foram vistas só em imprensa; nenhum limite lido (R-gap2-16 rejeitado como regra). O Manual traz o fluxo de cobrança recorrente (`/cobr`, janela de agendamento) no Anexo IV, não os limites.

## 9. Boleto

**Lacuna normativa:** norma de registro, CIP e fator de vencimento (BCB/Febraban) **não foram lidas**; boleto do Mercado Pago, idem. O que segue é de documentação de PSP (classe B) e do brain (Não verificado).

**Pagar.me (V-36, B):** `boleto` dentro de `payment`; `due_at` opcional; `instructions` até 256 caracteres; `interest` e `fine` opcionais, com `days`, `type` (`flat` ou `percentage`) e `amount` obrigatórios se enviados — **só para clientes com integração PSP**, não gateway; `discount` com `type` e `rules` em ordem crescente de `limit_date`, cada data (AAAA-MM-DD) **anterior** ao `due_at`; `document_number` até 16; `nosso_numero` identifica o boleto na conta (a tabela não diz se é opcional); o boleto pode ser acessado até 60 dias após o vencimento. **Não reverificado**: unidades de `amount` em juros/multa, horário devolvido diferente do enviado, dados obrigatórios do registrado.

Checklist de criação (V-36): (1) validar localmente que cada `limit_date` é anterior ao vencimento; (2) enviar juros e multa só se o contrato com o PSP permitir; (3) gravar `due_at` e `nosso_numero` **devolvidos**, nunca os enviados; (4) boleto vencido há mais de 60 dias é inacessível: prever nova cobrança; (5) confirmar com o PSP quem gera o `nosso_numero`; (6) testar o horário devolvido contra o fuso do negócio.

**Asaas (V-52, A):** `POST /v3/payments` com `billingType` `BOLETO`; guarde `id`, `invoiceUrl`, `bankSlipUrl`, `status`; `GET /v3/payments/{id}/identificationField` para a linha digitável, **buscada de novo sempre que valor ou vencimento mudar**; não libere produto só pela criação — espere `PAYMENT_CONFIRMED` / `PAYMENT_RECEIVED` (também `PAYMENT_OVERDUE`, `PAYMENT_REFUNDED`); em timeout, consulte as cobranças existentes antes de recriar (usar referência externa como chave de consulta é **Inferido**); idempotência do POST não documentada.

**Casos de teste herdados do brain (Não verificados contra norma):**

| Tema | Caso | Esperado |
| --- | --- | --- |
| Formatos | código de barras (44 posições) x linha digitável (47 dígitos em cobrança; 48 em arrecadação/convênio, que começa com 8) | aceita os dois; converte sem perder dígito |
| Dígitos verificadores | alterar um dígito de cada campo | módulo 10 por campo na linha digitável; DV geral do código de barras em módulo 11; erro aponta o campo |
| Fator de vencimento | boletos vencendo em 21/02/2025 e 22/02/2025 | o fator conta dias desde 07/10/1997, chegou a 9999 em 21/02/2025 e reiniciou em 1000 em 22/02/2025 (a aritmética de datas foi conferida pelo construtor: 07/10/1997 + 9999 dias = 21/02/2025; a norma segue não lida) |
| Ambiguidade do fator | fator 1000 | pode ser 03/07/2000 ou 22/02/2025; resolver para o ciclo mais próximo da data atual |
| Valor | R$ 0,01; R$ 99.999.999,99; sem valor | campo de valor com 10 posições; zeros pedem digitação |
| Vencimento em dia não útil | sábado ou feriado da praça | pago no próximo dia útil sem multa |

Armadilha: guardar a linha digitável como número (perde zeros à esquerda) ou calcular a data do fator sem o reinício (boleto aparece vencido há 25 anos). Linha digitável é **texto**.

## 10. Cartão

- **Luhn** antes de chamar o gateway: dígito trocado é recusado no cliente, sem chamada. Cartões de teste são **do gateway** e não valem em outro; os da Stripe herdados do brain (`4242 4242 4242 4242` aprova, `4000 0000 0000 0002` recusa genérico, `4000 0000 0000 9995` saldo insuficiente, `4000 0027 6000 3184` exige 3DS) devem ser conferidos na documentação de teste vigente.
- **Parcelamento**: valor mínimo de parcela; parcelado pela loja (sem juros) x pelo emissor (com juros); soma das parcelas = total (use `allocate`); troca de parcelas depois de cupom; estorno de compra parcelada.
- **Tokenização e cartão salvo**: cartão expirado, removido, de outro usuário (IDOR com o token). Cartão salvo/recorrência/COF e EMVCo: **sem fonte lida** (L12, L15).
- **PCI DSS**: a página do PCI SSC lista "PCI DSS v4.0.1" (V-29); PA-DSS aparece como aposentado. **Nenhum número de requisito é verificado**. A data de 31/03/2025 e os requisitos 6.4.3 e 11.6.1 vêm do brain e do conhecimento do validador e são **Não verificados com ferramenta**. O que vira caso de teste (princípio): PAN completo nunca em log, URL, analytics ou print; exibição mascarada; CVV nunca armazenado depois da autorização; ambiente de teste sem cartão real.

Teste barato e eficaz — PAN em log (regex + Luhn):

```python
import re
PAN = re.compile(r"\b(?:\d[ -]?){12,18}\d\b")

def luhn_ok(digits: str) -> bool:
    total = 0
    for i, ch in enumerate(reversed(digits)):
        d = int(ch)
        if i % 2:
            d = d * 2 - (9 if d * 2 > 9 else 0)
        total += d
    return total % 10 == 0

def pans_in(text: str) -> list[str]:
    cands = (re.sub(r"[ -]", "", m.group()) for m in PAN.finditer(text))
    return [c for c in cands if 13 <= len(c) <= 19 and luhn_ok(c)]
# Conferido: pans_in("card 4242 4242 4242 4242 ok") == ["4242424242424242"]
```

## 11. Open Finance Brasil (V-45, V-69; requisitos **Não verificados**)

Estrutura do portal (`openfinancebrasil.atlassian.net/wiki/spaces/OF/overview`): Especificações de APIs, Especificações de Integração, Segurança, Diretrizes Técnicas e Operacionais, Certificação de Conformidade, Requisitos não Funcionais, Histórico de Alterações. A navegação lista FAPI-BR v2.2.1 (histórico v2.2.0, v2.1.0, v2.0.0, v1.0.0), DCR-BR v2.1.0, CIBA-BR v2.1.0-beta2 e Webhook v1.3.0 (página de 15/05/2023). Da FAPI-BR v2.1.0 só a seção 5.1 foi lida: o servidor de autorização "shall" autenticar clientes com `private_key_jwt`, exigir PAR e publicar metadados de descoberta (OIDC Discovery e RFC 8414). Checklist de 4 itens: (1) confirmar a versão vigente; (2) verificar `private_key_jwt`, PAR e descoberta; (3) **não** afirmar PKCE, JARM ou mTLS sem ler a seção correspondente; (4) registrar versão e data de leitura (a página é v2.1.0 "Updated 02/12/2025", data ambígua). Consentimento e iniciação de pagamento: lacuna (L8).

## 12. Gotchas

- `txid` 1 a 35 x 26 a 35: confusão clássica; QR estático não garante unicidade do `txid` (a consistência fica com o recebedor).
- `expires_in` da Pagar.me aparece como string no exemplo e é inteiro no tipo; unidades de `flat`/`percentage` não reverificadas; Pagar.me Pix só para contas com gateway Pagar.me.
- Pix expirado libera a reserva de estoque (caso do brain para e-commerce): detalhes em `/ecommerce-marketplace:estoque-reserva-pedido`.
- Caso hostil de QR: CRC inválido, QR de outro recebedor colado no checkout, valor alterado entre a leitura e a confirmação, app fechado no meio do pagamento e reaberto.
- Dados de teste: CPF/CNPJ gerado com DV correto pode pertencer a alguém real; só em teste, nunca para consultar bases externas.
- Para regras de aprovação de PSP e de adquirente, o contrato com o PSP manda; este material não substitui homologação.
