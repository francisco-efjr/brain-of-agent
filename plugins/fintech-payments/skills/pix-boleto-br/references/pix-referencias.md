# Pix: referências para integrar e testar

Sumário: 1. Fontes oficiais · 2. Schemas e endpoints (spec 2.10.0) · 3. Ciclo de vida do `txid` · 4. BR Code e CRC16 (executado) · 5. Webhook do Pix · 6. MED · 7. Open Finance · 8. Seeds a confirmar (herdados) · 9. Testes de borda

Rótulos: **Verificado** = lido na spec ou no manual do BCB pelo validador (V-43, V-44, V-65); **Inferido** = derivação do plugin; **Não verificado** = herdado do brain-of-agent (V-33) ou de imprensa. Conferido em 2026-10-10. A versão da spec muda: compare com a vigente e registre versão e data de leitura no código e no ADR (V-70).

## 1. Fontes oficiais

| Fonte | Uso | Observação |
| --- | --- | --- |
| `github.com/bacen/pix-api` (OpenAPI, Apache-2.0, versão 2.10.0) | schemas, endpoints, mensagens de erro | a spec é funcional; segurança fica nos manuais (V-31) |
| Manual de Padrões para Iniciação do Pix v2.10.0 (PDF do BCB, 123 páginas) | `txid` (5.3), BR Code (seção 2), segurança do PSP (Anexo II), cálculo de cobrança (Anexo III), Pix Automático (Anexo IV) | obtenha o PDF no site do BCB; a seção 2.6.3 traz um exemplo de QR estático com CRC `1D3D` (V-65) |
| Voto BCB 7/2026 | definição e calendário do MED 2.0 | só isso; não traz o prazo de 80 dias (V-64) |
| Manual de Segurança do Pix, Regulamento, DICT, Manual do BR Code, IN BCB 766 e 746, Resolução BCB 402 | limites, MED completo, regras do Pix Automático | **não obtidos**: lacuna; peça os PDFs vigentes ao usuário |

## 2. Schemas e endpoints (V-43, Verificado)

| Campo | Regra |
| --- | --- |
| `TxId` da cobrança | `[a-zA-Z0-9]{26,35}`; criado exclusivamente pelo recebedor; único por CPF/CNPJ do recebedor; validado pelo PSP |
| `EndToEndId` | 32 alfanuméricos |
| `DevolucaoId` | `[a-zA-Z0-9]{1,35}`, gerado pelo cliente; único por `e2eid` |
| Valores (`cob.valor.original`, `cobv.valor.original`, `Devolucao.valor`, `Pix.valor`) | string decimal `\d{1,10}\.\d{2}` |
| `valor.original` igual a zero | erro 400 (`CobOperacaoInvalida`), exceto Pix Saque (0.00 exigido) e Pix Troco (maior que 0.00) |
| Valor do Pix | original + saque + troco + multa + juros − abatimento − desconto |
| Expiração menor ou igual a zero em `PUT|PATCH /cob/{txid}` | erro 400; idem `cobv` |
| CNPJ nos schemas | `^[0-9A-Z]{14}$` (alfanumérico aceito desde a 2.9.0) |
| `chave` DICT | no máximo 77 caracteres |

Endpoints citados: `PUT|PATCH /cob/{txid}` e `cobv` (cobrança); `PUT /pix/{e2eid}/devolucao/{id}` (devolução); `PUT /webhook/{chave}` (registro do webhook). Não foram lidos: recorrência e Pix Automático (`rec`, `cobr`); não codifique contra eles sem ler.

Objeto `Devolucao`: obrigatórios `id`, `rtrId` (32), `valor`, `horario`, `status` (`EM_PROCESSAMENTO`, `DEVOLVIDO`, `NAO_REALIZADO`); `descricao` até 140. Erro `PixDevolucaoInvalida` (400) se o `id` já foi usado para aquele `e2eid`, se a soma com devoluções anteriores passa do Pix original ou se está fora da janela ("hoje estabelecida como 90 dias desde a liquidação").

## 3. Ciclo de vida do `txid` (Manual 5.3, Verificado)

- A cobrança é identificada unicamente pelo `txid`. O recebedor o envia ou delega ao PSP (só imediata).
- `CPF/CNPJ + txid` é único por PSP e **nunca se repete**, mesmo com a cobrança cancelada ou baixada.
- 26 a 35 caracteres A-Z, a-z, 0-9. Cobrança imediata e com vencimento não usam o mesmo `txid`.
- Razão registrada pelo manual: enviar o `txid` garante idempotência (evita duas cobranças para a mesma obrigação após falha de chamada); quando o PSP gera o `txid`, a idempotência não é garantida.
- QR estático: sem garantia de unicidade; a consistência fica com o recebedor.

Sugestão de geração (Inferido): `uuid4().hex` (32 caracteres hexadecimais) atende 26 a 35 e permanece único; guarde-o antes de chamar o PSP.

## 4. BR Code e CRC16 (V-65, Verificado no manual; vetor sintético executado em 2026-10-10)

Estrutura (EMV QR Code, modo apresentado pelo recebedor): objetos em TLV (`ID` de 2 dígitos, tamanho de 2 dígitos, valor). GUI do Pix `br.gov.bcb.pix` (14 caracteres) nos IDs raiz 26 a 51. Campo `63` (CRC16) com 4 caracteres, calculado com polinômio `0x1021` e valor inicial `0xFFFF`, sobre toda a string **incluindo** `6304`. **Estático:** chave válida no DICT é obrigatória; `txid`, texto livre e valor são opcionais. **Dinâmico:** subcampo `25` da Merchant Account Information com a URL (1 a 77 caracteres) do payload JSON; valor e `txid` não devem ser preenchidos e, se estiverem, são ignorados.

```python
def crc16(payload_sem_crc: str) -> str:
    """payload_sem_crc termina em '6304'. Devolve 4 hex maiúsculos (CRC-16/CCITT-FALSE)."""
    crc = 0xFFFF
    for b in payload_sem_crc.encode("ascii"):
        crc ^= b << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
    return f"{crc:04X}"

def validar_br_code(texto: str) -> bool:
    return len(texto) > 8 and texto[-8:-4] == "6304" and crc16(texto[:-4]) == texto[-4:].upper()
```

Vetores **sintéticos** (chave aleatória fictícia, recebedor fictício; calculados e conferidos por execução em Python 3.14):

| Caso | Payload | Esperado |
| --- | --- | --- |
| Positivo (estático, R$ 10,00) | `00020126580014br.gov.bcb.pix0136123e4567-e89b-12d3-a456-426614174000520400005303986540510.005802BR5910LOJA TESTE6009SAO PAULO62070503***63046BFD` | `validar_br_code` verdadeiro; CRC `6BFD` |
| Negativo (valor alterado de `10.00` para `10.01`, CRC mantido) | mesmo payload com `540510.01` e final `6BFD` | falso; o CRC calculado seria `D699` |
| Dinâmico com valor e `txid` preenchidos | MAI com `0014br.gov.bcb.pix2534pix.exemplo.test/qr/v2/cobv/ABC123` e campo `54` presente | valor e `txid` do QR ignorados; vale o payload obtido na URL |
| Dinâmico reutilizado | o mesmo BR Code exibido para dois pagadores | dois pagamentos podem chegar; a unicidade é do `txid` da cobrança, então o sistema concilia por `txid`/`e2eid` e trata o segundo como caso de negócio |

O payload do exemplo do Manual (seção 2.6.3, CRC `1D3D`) é o vetor positivo oficial: o usuário o extrai do PDF e o coloca na massa de teste; este plugin não o reproduz. Trocar qualquer caractere do payload altera o CRC.

## 5. Webhook do Pix (V-43, V-53, V-54)

`PUT /webhook/{chave}` com `webhookUrl` obrigatório. **Só Pix associados a um `txid` são notificados**, além de devoluções que atingem status final. O PSP chama `POST {webhookUrl}/pix`; o SLA é de cada PSP e pode agrupar Pix de uma chave; canal protegido por mTLS; o recebedor responde 200. Efí (exemplo de PSP): corpo com array `pix` (`endToEndId`, `txid`, `chave`, `valor`, `horario`, `infoPagador`, opcional `gnExtras`), timeout de 60 s, TLS 1.2 mínimo, `?ignorar=` evita o acréscimo de `/pix`; o IP exibido na documentação não deve ser fixado no código. Passos de recepção: `webhook-handler`.

## 6. MED (V-64)

**Verificado (voto BCB 7/2026, 20/01/2026):** MED em vigor desde novembro de 2021 para devolução de Pix com fundada suspeita de fraude; a Resolução BCB 493 (28/08/2025) incorporou melhorias; adoção facultativa desde 23/11/2025 e obrigatória a partir de 2/02/2026; a minuta insere o art. 113-A, que dispensa a instauração de processo de apuração por descumprimentos do art. 121 ocorridos entre 2/02 e 10/05/2026.
**Não verificável:** o prazo de 80 dias. Reportagens atribuem à IN BCB 766 a ampliação, a partir de 1º/09/2026, do prazo de contestação do recebedor de 30 para 80 dias e dizem que o da vítima já seria de 80 dias; nenhuma fonte oficial foi encontrada.
**Como modelar:** registro de estados de devolução com dois prazos separados, cada um com `prazo_fonte` e `status` (`verificado`, `nao_verificado`); teste de regressão com data fixa só para a regra de penalidade (2/02 a 10/05/2026).

## 7. Open Finance (V-45, V-69; requisitos Não verificados)

Checklist de 4 itens: (1) confirmar a versão vigente (a página lida era a FAPI-BR v2.1.0, "Updated 02/12/2025", data ambígua, e a navegação lista v2.2.0 e v2.2.1); (2) verificar `private_key_jwt`, PAR (Pushed Authorization Requests) e metadados de descoberta (OIDC Discovery e RFC 8414), exigidos na seção 5.1 lida; (3) não afirmar PKCE, JARM ou mTLS como exigência sem ler a seção correspondente; (4) registrar versão e data de leitura. Seções 5.2, 6, 7 e 8, DCR-BR, consentimento e iniciação de pagamento: lacuna.

## 8. Seeds a confirmar no regulamento vigente do BCB (herdados do brain, V-33; Não verificados)

| Tema | Valor herdado | Observação |
| --- | --- | --- |
| Tipos de chave | CPF, CNPJ, e-mail (até 77), telefone (`+5511987654321`), aleatória (UUID de 36) | 5 chaves por conta de pessoa física e 20 por pessoa jurídica |
| QR estático | `txid` de até 25 caracteres (ou `***`) | o manual não confirma o limite de 25 |
| `EndToEndId` | `E` + 8 dígitos do ISPB + `AAAAMMDDHHmm` em UTC + 11 alfanuméricos | só o comprimento de 32 está verificado; teste o parse da hora em UTC |
| Limite noturno | R$ 1.000,00 entre 20h e 6h | não consta no Manual de Iniciação |
| Dispositivo novo | R$ 200,00 por transação e R$ 1.000,00 por dia | idem |
| MED | contestação em até 80 dias | ver seção 6 |
| Pix Automático | agendamento 2 a 10 dias antes | idem; IN BCB 746 só em imprensa |
| Timeout | consultar o status pelo `EndToEndId` após 30 s | prática, não norma |

Use estes valores como "seed" nos casos de teste, citando a norma a conferir; nunca como oráculo de aceitação.

## 9. Testes de borda do Pix (V-43, V-48, V-33, V-65)

`txid` com 25, 26, 35 e 36 caracteres (recusar 25 e 36); reuso de `txid` após cancelamento (recusado); valor `0.00`, `10.0`, `10.001`, `10.00` (só o último válido para cobrança comum); devolução acima do saldo estornável, repetida com o mesmo `id`, e fora da janela; timeout na criação seguido de consulta por `txid`; webhook duplicado (mesmo `endToEndId`); QR com CRC inválido; dinâmico com valor preenchido; valor alterado entre a leitura e a confirmação; app fechado no meio do pagamento e reaberto; CNPJ alfanumérico como chave (`12ABC34501DE35` válido). Matriz completa: skill `payment-test-plan`.
