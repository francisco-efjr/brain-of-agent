# Matriz da trifecta letal

Uma linha por automação, agente ou combinação de servidores MCP. Fonte: V-20 (heurística de design, classe B), V-14. Auditar a **combinação** de servidores, não cada um isolado (R-06).

| Automação / agente | R-01 Lê dado privado? (quais) | R-02 Lê conteúdo externo? (fonte) | R-03 Pode enviar para fora? (canal) | Três "sim"? | Perna quebrada (R-04) | O que sai é registrado antes? (R-05) | Evidência |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Ex.: fluxo n8n "responder cliente" | sim (CRM) | sim (e-mail de cliente) | sim (e-mail de saída) | **sim** | resposta vira rascunho com aprovação humana | sim (log do rascunho) | fluxo exportado, nó "Aprovar" |
| | | | | | | | |

## Formas de quebrar uma perna

1. **Remover a saída** (perna 3): o resultado fica em sistema interno; nada de HTTP/e-mail/imagem remota/link.
2. **Separar em dois agentes sem acesso cruzado:** um lê o conteúdo hostil sem dados privados e devolve campos validados por schema; o outro tem os dados e nunca vê o texto bruto.
3. **Aprovação humana antes do envio** (perna 3), com o conteúdo exato visível ao aprovador.
4. Reduzir o dado privado ao mínimo (perna 1) ou torná-lo inacessível ao passo que lê conteúdo externo.

## Combinação de servidores MCP ativos

| Servidor | Perna(s) que adiciona | Aprovado por (A-xx) | Versão fixada |
| --- | --- | --- | --- |
| | | | |

Servidor que traz conteúdo da web (Fetch, navegador) = perna 2; servidor com e-mail/HTTP/chat = perna 3; banco/arquivos/CRM = perna 1. Guardrails de produto não substituem quebrar a perna (V-20). Rótulo: Inferido onde a matriz foi preenchida por leitura de configuração e não por teste.
