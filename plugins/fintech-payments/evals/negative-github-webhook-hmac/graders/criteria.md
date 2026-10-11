---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Explica a validação: HMAC-SHA256 do corpo bruto (bytes originais, antes de parsear) com o segredo do webhook, comparação do valor com o prefixo `sha256=` do header em tempo constante, rejeição quando o header está ausente ou inválido.
2. Explica o dedupe pelo ID do delivery (header `X-GitHub-Delivery`) com armazenamento persistente e unicidade, e que o endpoint deve responder rápido e processar o deploy de forma assíncrona.
3. Responde no contexto do GitHub e de deploy, sem apresentar regras de pagamentos (ledger, Pix, PCI, conciliação, estorno) como se o caso fosse financeiro.
FAIL if qualquer um ocorrer: aciona skill ou agente do plugin de pagamentos; trata o caso como pagamento; sugere comparação com `==` em vez de tempo constante; recomenda parsear o JSON antes de verificar a assinatura.
