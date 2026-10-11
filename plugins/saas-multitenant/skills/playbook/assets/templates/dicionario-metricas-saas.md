# Dicionário de métricas SaaS

Regra: a definição do produto é a do **Stripe Billing Analytics** (V-40) ou vem marcada como diferente, para conciliar com o Dashboard. Fórmulas do a16z (2015) entram como alternativa declarada. **Ativação** não tem fonte: defina por produto, com evento e janela, como Suposição. Moeda: [..] · Fuso do corte do dia: [America/Sao_Paulo | outro] · Desconto: [tratamento] · Trial: [tratamento].

| Métrica | Fórmula | Fonte | Janela | Desconto | Moeda | Trial | Observação |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MRR | soma do valor mensal normalizado das assinaturas `active` e `past_due`, sem impostos, planos gratuitos e cobrança por uso | Stripe | instantâneo | conforme configuração | [..] | item em trial sai | descontos e "ativo" são configuráveis; mudança leva 24 a 48 h |
| Crescimento de MRR | novo + reativação + expansão − contração − churn ± câmbio | Stripe | mês | | | | |
| Assinante ativo | MRR positivo em `active` ou `past_due`, contado uma vez | Stripe | instantâneo | | | | |
| Churn de assinantes | churn dos 30 dias ÷ (ativos de 30 dias atrás + novos) | Stripe | 30 dias | | | | `canceled` e `unpaid` viram churn |
| Receita perdida | MRR perdido + contração | Stripe | mês | | | | |
| ARPU | MRR ÷ ativos | Stripe | mês | | | | |
| LTV (Stripe) | ARPU ÷ churn de assinantes | Stripe | estimativa | | | | |
| LTV (a16z) | margem de contribuição × vida média (1 ÷ churn mensal) | a16z | | | | | declare qual fórmula |
| Conversão de trial | convertidos ÷ encerrados em 30 dias | Stripe | 30 dias | | | | pode passar de 100% |
| Retenção de receita por coorte | Stripe | Stripe | coorte | | | | pode passar de 100% |
| Churn bruto de receita | MRR perdido ÷ MRR inicial | a16z | período | | | | |
| Churn líquido de receita | (perdido − upsell) ÷ MRR inicial | a16z | período | | | | equivalente documentado de "NRR"; o termo NRR não aparece nas fontes lidas |
| ARR | sem taxas únicas e sem "bookings × 12" | a16z | | | | | |
| CAC / CMGR | a16z | a16z | | | | | |
| **Ativação** | [evento] dentro de [janela] após o cadastro | **Suposição** | [..] | n/a | n/a | n/a | defina com o produto |
| Usuário ativo | [definição explícita] | **Suposição** (a16z manda definir) | [..] | n/a | n/a | n/a | sem definição padrão |

Cobrança por uso fica fora do MRR da Stripe: se o produto é híbrido, defina "receita recorrente + uso" como métrica própria e marque como diferente. Dados atrasados de uso e reprocessamento idempotente: ver `references/entitlements-limites-uso.md`. Corte do dia no fuso do negócio, não em UTC (brain).
