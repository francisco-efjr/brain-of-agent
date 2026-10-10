# Exemplo: `runbooks/5xx.md` (modelo; não validado contra sistema vivo)

Exemplo fictício para um serviço `checkout` em Kubernetes com Prometheus. Os alvos estão em `[COLCHETES]`; substitua pelos reais. Os comandos são de leitura e vêm de conhecimento estável de Kubernetes e Prometheus: rótulo **Inferido** (confirme com `kubectl version` e a documentação da sua versão). Estrutura própria a partir de V-18 e do cookbook de SRE da Anthropic (nomes `5xx.md`, `oom.md`, `latency.md`).

````markdown
# Runbook: 5xx elevado em checkout

Alerta de origem: CheckoutErrorBudgetBurnFast, CheckoutErrorBudgetBurnSlow
Dono: [equipe de checkout] · Última revisão: [AAAA-MM-DD] · Alteração apenas por PR
Impacto: clientes veem erro ao criar pedido. Severidade sugerida: P1 (exemplo, Suposição; use a tabela da organização)

## 0. Antes de começar
- Papéis: IC [quem], OL [quem muda o sistema], CL [comunicação]. Use `incident-triage` se houver usuário afetado agora.
- Contexto de cluster correto: `kubectl config current-context` -> esperado: `[contexto de produção]`.
- Credenciais: identidade somente leitura para o diagnóstico. Mitigações exigem o OL.

## 1. Diagnóstico (somente leitura, onda 1 em paralelo)
| # | Verificação | Comando ou consulta | Esperado se saudável | O que concluir |
| --- | --- | --- | --- | --- |
| 1.1 | Taxa de erro atual | `sum(rate(http_requests_total{job="checkout",code=~"5.."}[5m])) / sum(rate(http_requests_total{job="checkout"}[5m]))` | menor que 0,001 | Acima de 0,0144 por mais de 5 min confirma queima rápida |
| 1.2 | Mudanças recentes | `kubectl rollout history deployment/checkout -n [ns]` | revisão antiga estável | Revisão nova nos últimos 60 min: suspeitar do deploy |
| 1.3 | Estado dos pods | `kubectl get pods -n [ns] -l app=checkout` | todos `Running`, `RESTARTS` estável | `CrashLoopBackOff`/`OOMKilled`: ver `oom.md` |
| 1.4 | Erros recentes | `kubectl logs deployment/checkout -n [ns] --since=15m` (contar as linhas `ERROR` da saída) | número baixo e estável | Pico: abrir amostra e agrupar por motivo |
| 1.5 | Dependência | Latência do banco no painel [link] | dentro da faixa do SLO | Banco lento: hipótese de dependência |

## 2. Hipóteses (até 3, onda 2: cruze 1.1 a 1.5)
- H1 Deploy recente: previsão: erros começam junto à revisão nova; refuta: pods da revisão antiga também falham.
- H2 Dependência lenta (banco): previsão: timeouts nos logs e latência alta no painel; refuta: banco normal.
- H3 Pico de tráfego: previsão: taxa de requisições acima do normal; refuta: tráfego normal.

## 3. Mitigações (exigem decisão humana: OL executa, IC aprova)
| Opção | Pré-condição | Comando | Efeito e risco | Reversão | Aprovador |
| --- | --- | --- | --- | --- | --- |
| Rollback do deploy | H1 suportada; migração compatível com a versão anterior | `kubectl rollout undo deployment/checkout -n [ns]` | Volta a revisão anterior; migração de schema e e-mails já enviados não revertem | Novo deploy da revisão atual | IC |
| Desligar flag [nome] | Flag nova ligada junto ao início do erro | [comando da ferramenta de flags] | Remove a funcionalidade nova | Religar a flag | IC |

## 4. Verificação de recuperação
Consulta 1.1 menor que 0,001 por 15 min consecutivos e painel de SLO sem queima. Só então declarar mitigado.

## 5. Escalonamento
- Sem hipótese suportada em 30 min ou impacto crescente: acionar [plantão da plataforma] pelo canal [nome].
- Suspeita de perda de dados: acionar [dono de dados] e o plugin/processo de segurança, se houver exposição.

## 6. Histórico
Atualizar este arquivo por PR após cada incidente que o usar (o que faltou, comando que mudou).
````

## Lint aplicado a este exemplo

- Comandos de diagnóstico: todos com esperado e conclusão. Itens não validados: marcados Inferido no cabeçalho.
- Diagnóstico e mitigação separados; toda mitigação tem aprovador (papel), risco e reversão.
- Sem segredo; sem nome de pessoa; alvos em colchetes.
- `rollout undo` aparece apenas na seção 3.
