# Plano de integração

Adaptado de `plano-incremento.md` do brain-of-agent (Francisco Edson, MIT). Preencha só o que muda a decisão; célula sem resposta vira `NV` (não verificável) com o motivo. Use em automações novas ou mudanças relevantes; para ajuste localizado, três linhas bastam.

## 1. Objetivo e baseline

- Problema, quem é afetado e comportamento atual:
- Critério de sucesso e como será medido (fonte):
- Estado observado e reprodução (comando, evento de exemplo):
- Escopo, exclusões e autorização (o que posso alterar; o que exige confirmação):
- Plataforma, versões e ambiente (local / staging / produção; o que posso executar):
- Forma escolhida: [workflow | agente com limite | tool MCP | hook | job `claude -p` | skill] — alternativas descartadas e por quê (ADR só se a decisão for material):

## 2. Fluxo A → B e fronteiras

`gatilho → verificação → dedupe → fila → efeito → resultado observável`. Descreva cada fronteira e sua falha/recuperação.

| Requisito | Alteração | Invariante | Contrato/compatibilidade | Verificação/oráculo |
| --- | --- | --- | --- | --- |
| | | | | |

## 3. Riscos de segurança (preencher `matriz-trifecta.md`)

- Lê dado privado? Lê conteúdo controlável por atacante? Pode enviar para fora? Perna quebrada:
- Credenciais (onde vivem, escopo mínimo, rotação):
- Combinação de servidores MCP ativos:

## 4. Contrato de falha

| Item | Decisão |
| --- | --- |
| Chave de idempotência (ID do evento/registro de origem) | |
| Retry: tentativas, backoff com jitter, `Retry-After` | |
| Classificação 4xx permanente × 5xx/429 transitório | |
| Destino de falha (fila de mortas / error workflow) e dono | |
| Reprocesso: quem, como, registro (`retry_of`) | |
| Timeouts e limites de taxa | |
| Cursor/janela (sync incremental) e reconciliação | |
| Heartbeat / alerta de ausência (jobs) | |

Mapa de falhas (por passo): o que acontece se falhar · quem é avisado · como reprocessar.

## 5. Plano por incrementos

| Fase | Artefato utilizável | Risco | Mitigação | Critério de saída |
| --- | --- | --- | --- | --- |
| | | | | |

Dependências e decisões materiais:
Dados/migração e limites de recuperação:
Timeout, duplicação, concorrência e autorização:

## 6. Validação

- Checks existentes a executar (comando literal):
- Replay/testes novos (assinatura inválida, duplicata, timestamp velho, falha forçada):
- Integrações reais e isolamento (credenciais de teste):
- Roteiro manual e efeitos persistidos:
- Não executável e risco restante (rótulo NV):

## 7. Entrega

- Como executar, configurar, observar e **desativar**:
- Publicação/rollback somente dentro da autorização (reverter binário não desfaz e-mail, cobrança ou conversão de dado):
- Evidências, pendências e próximo passo (use `handoff-checkpoint.md`):
