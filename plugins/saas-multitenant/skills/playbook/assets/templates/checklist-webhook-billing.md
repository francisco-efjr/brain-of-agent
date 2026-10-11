# Checklist de webhook de billing

Base: `V-03` (Stripe), `V-50` e `V-66` (provedor com token em header, como o Asaas). Para cada item: ok, falha ou não verificado, com `arquivo:linha`. Sem execução: "leitura de código, nenhum teste executado". Nunca cole `whsec_`, `sk_`, token ou chave reais neste documento.

Provedor: [Stripe | Asaas | outro] · Versão da API/SDK (do lockfile): [..] · Arquivo do handler: [..]

## A. Handler (Stripe: assinatura do corpo)

| # | Item | Estado | Evidência |
| --- | --- | --- | --- |
| 1 | Corpo bruto lido sem parser antes da verificação (nenhum `express.json()` antes da rota) | | |
| 2 | `Stripe-Signature` verificada com o segredo do cofre; falha responde 400; tolerância padrão de 5 minutos, nunca 0 | | |
| 3 | `event.id` inserido em tabela com UNIQUE antes de agir; duplicado responde 200 sem efeito | | |
| 4 | Resposta 2xx **antes** da lógica pesada; processamento em fila; sem redirecionamento 3xx | | |
| 5 | Worker relê o objeto atual na API; não confia no payload nem na ordem (`created` não ordena) | | |
| 6 | Tenant resolvido por `customer` / `metadata.tenant_id`; sem tenant mapeado: registrar e alertar | | |
| 7 | Contexto de tenant na mesma transação que grava o resultado (`set_config(..., true)`) | | |
| 8 | Política de status aplicada (`invoice.paid` não é "ativo" com política "todas as faturas") | | |
| 9 | Erro transitório responde 5xx; erro permanente vai para DLQ com motivo; reprocessamento existe | | |
| 10 | Só os eventos usados estão assinados; eventos de risco tratados se aplicável | | |
| 11 | `invoice.finalization_failed` com alerta | | |
| 12 | Segredo rotacionável (até 24 h de sobreposição); rota isenta de CSRF; HTTPS | | |

## B. Variante: provedor com token estático em header (Asaas)

| # | Item | Estado | Evidência |
| --- | --- | --- | --- |
| 1 | Comparação de `asaas-access-token` com segredo do cofre (tempo constante); a API key não é usada como token | | |
| 2 | Registrado que **não há assinatura do corpo**: replay mitigado por `id` UNIQUE + allowlist de IP, não impedido | | |
| 3 | `id` do evento em UNIQUE antes de agir; repetido responde 200 sem efeito | | |
| 4 | Responde **somente HTTP 200**, em até 10 s; processamento fora da requisição | | |
| 5 | Rota HTTPS direta (301, 302, 307, 308 não são seguidos) | | |
| 6 | Alerta de fila interrompida (15 falhas consecutivas) antes dos 14 dias de retenção | | |
| 7 | Allowlist de IPs testada em **produção e sandbox** | | |
| 8 | Mapeamento evento → estado de acesso testado no sandbox por cenário (criar, pagar, atrasar, inativar, remover); evento de cancelamento **observado**, não presumido | | |

## C. Testes obrigatórios

| Teste | Comando | Resultado (saída colada) | Rótulo |
| --- | --- | --- | --- |
| Evento duplicado | | | |
| Fora de ordem (`invoice.paid` antes de `customer.subscription.created`) | | | |
| Assinatura/token inválido | | | |
| Corpo alterado | | | |
| Dois workers concorrentes no mesmo evento | | | |
| Worker cai entre gravar e ACK | | | |
| Contagem de linhas no banco depois do retry (não só a resposta) | | | |

## D. Decisões de produto pendentes

`past_due`: [..] · `paused`: [..] · Tolerância de acesso: [..] · Quem é avisado em falha: [..]
