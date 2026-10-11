# Boleto: checklist de integração e casos de teste

Sumário: 1. O que está e o que não está verificado · 2. Campos da Pagar.me (V-36) · 3. Fluxo Asaas (V-52) · 4. Casos herdados do brain (Não verificados) · 5. Resolvedor de fator de vencimento · 6. Perguntas ao PSP

Conferido em 2026-10-10. A norma de boleto (registro, CIP, fator de vencimento) é lacuna: nenhuma fonte Febraban ou BCB foi lida. Tudo na seção 4 vem do brain-of-agent (conteúdo próprio do usuário, MIT, atribuição no README do plugin) e é **Não verificado** contra norma; a aritmética do fator foi conferida por cálculo, o que não prova a regra da norma.

## 1. Quem diz o quê

| Tema | Fonte | Rótulo |
| --- | --- | --- |
| Campos de criação, juros, multa, desconto | documentação Pagar.me (V-36) | Verificado (página sem data; unidades de `amount` não reverificadas) |
| Fluxo de criação, linha digitável, eventos | documentação Asaas (V-52) | Verificado |
| Formatos, DV, fator, valores | brain-of-agent (V-33) | Não verificado |
| Registro de boleto, CIP, regras de baixa | nenhuma fonte lida | lacuna |
| Boleto do Mercado Pago | nenhuma fonte lida | lacuna |

## 2. Pagar.me: campos e regras (V-36)

- `boleto` dentro de `payment`; `due_at` opcional (data-hora); `instructions` até 256 caracteres; `document_number` até 16 caracteres.
- `interest` e `fine` opcionais; se enviados, `days`, `type` (`flat` ou `percentage`) e `amount` são obrigatórios. Valem **apenas para clientes com integração PSP** (liquidação pela Pagar.me), não para integração só gateway.
- `discount` com `type` e `rules` em ordem crescente de `limit_date`; cada data (AAAA-MM-DD) **anterior** ao `due_at`.
- `nosso_numero` identifica o boleto de forma única na conta; a tabela não diz se é opcional.
- O boleto pode ser acessado até 60 dias após o vencimento.
- Não reverificado: unidades de `amount` em juros e multa; horário devolvido diferente do enviado; dados obrigatórios do boleto registrado.

Checklist de criação: (1) `limit_date` de cada regra de desconto menor que `due_at`, validado localmente; (2) juros e multa só com contrato PSP; (3) gravar `due_at` e `nosso_numero` devolvidos; (4) vencido há mais de 60 dias é inacessível: segunda via é nova cobrança; (5) perguntar ao PSP quem gera o `nosso_numero`; (6) testar o horário devolvido contra o fuso de negócio; (7) idempotência e eventos de webhook do boleto: não documentados nas páginas lidas (ver `webhook-handler`, regra V-50).

## 3. Asaas: fluxo de cobrança por boleto (V-52)

1. `POST /v3/payments` com `billingType` igual a `BOLETO`. Guarde `id` (consulta e conciliação), `invoiceUrl`, `bankSlipUrl`, `status`.
2. `GET /v3/payments/{id}/identificationField` devolve a linha digitável; busque de novo sempre que valor ou vencimento mudar, antes de apresentá-la.
3. Não libere produto só pela criação; aguarde a confirmação. Eventos: `PAYMENT_CONFIRMED`, `PAYMENT_RECEIVED`, `PAYMENT_OVERDUE`, `PAYMENT_REFUNDED`.
4. Em timeout ou resposta inconclusiva, consulte as cobranças existentes antes de repetir a criação (usar a referência externa como chave de consulta é **Inferido**; a página não nomeia o campo). Idempotência do POST não documentada.

## 4. Casos herdados do brain (Não verificados)

| Tema | O que testar | Esperado (herdado) |
| --- | --- | --- |
| Formatos | código de barras (44 posições) e linha digitável (47 dígitos em cobrança; 48 em arrecadação/convênio, que começa com 8) | aceita os dois; converte um no outro sem perder dígito |
| Dígitos verificadores | alterar um dígito de cada campo | linha digitável usa módulo 10 por campo; DV geral do código de barras, módulo 11; o erro aponta o campo |
| Fator de vencimento | boletos vencendo em 21/02/2025 e 22/02/2025 | o fator conta dias desde 07/10/1997; chegou a 9999 em 21/02/2025 e reiniciou em 1000 em 22/02/2025 |
| Ambiguidade | fator 1000 | pode ser 03/07/2000 ou 22/02/2025; resolver para o ciclo mais próximo da data atual, nunca para 2000 |
| Valor | R$ 0,01; R$ 99.999.999,99; boleto sem valor | campo de valor com 10 posições; sem valor (zeros) pede digitação |
| Vencimento em dia não útil | vence no sábado ou feriado da praça | pago no próximo dia útil sem multa |

Armadilha: guardar a linha digitável como número (perde zeros à esquerda) ou calcular a data do fator com a base antiga sem o reinício (o boleto aparece vencido há 25 anos). Feriados são dado configurável por praça, não lista fixa no código.

## 5. Resolvedor de fator de vencimento (executado em 2026-10-10)

```python
from datetime import date, timedelta
BASE, CICLO = date(1997, 10, 7), 9000     # fator 1000..9999, depois volta a 1000 (regra herdada: Não verificada)

def data_do_fator(fator: int, referencia: date) -> date:
    """Escolhe o ciclo cuja data fica mais próxima da data de referência."""
    if not 1000 <= fator <= 9999:
        raise ValueError("fator fora de 1000..9999")
    candidatos = [BASE + timedelta(days=fator + k * CICLO) for k in range(4)]
    return min(candidatos, key=lambda d: abs((d - referencia).days))
```

Saídas observadas com referência 2026-10-11: fator 9999 dá 2025-02-21; fator 1000 dá 2025-02-22; fator 1001 dá 2025-02-23. Com referência 2000-06-01, fator 1000 dá 2000-07-03. Use a data do próprio boleto, os dados do PSP e a norma como oráculo final; esta função só reproduz a regra herdada.

## 6. Perguntas ao PSP

- Quem gera o `nosso_numero`? É devolvido na criação?
- Juros, multa e desconto: unidades de `amount`, base de cálculo e se o contrato os permite.
- Qual o evento de webhook de boleto pago e como é autenticado? Existe idempotência na criação?
- Quanto tempo o boleto vencido continua acessível? Como emitir segunda via?
- O horário de `due_at` devolvido muda em relação ao enviado (fuso)?
