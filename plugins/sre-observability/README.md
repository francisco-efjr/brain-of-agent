# sre-observability — SRE, observabilidade e performance

Plugin do Claude Code (v0.1.0, MIT) para quem opera serviços em produção: define SLOs, revisa alertas, organiza a investigação de incidentes **sem tocar em produção**, escreve postmortems blameless e runbooks, revisa telemetria (OpenTelemetry, Prometheus) e planeja testes de carga e performance. Base: fontes primárias consultadas em 2026-10-10 (Google SRE, Prometheus, OpenTelemetry, k6, web.dev, documentação da Anthropic) e o conteúdo próprio do autor no repositório `brain-of-agent`.

## O que entrega

- **Um playbook** (router + processo + modo `SRE-COMPLETO`) com 12 referências densas, 15 templates e 20 regras prontas para `CLAUDE.md`.
- **9 skills de tarefa** para os fluxos recorrentes: SLO, revisão de alertas, triagem de incidente, postmortem, causa raiz, telemetria, performance, release health e runbook.
- **Biblioteca de prompts** curados (skill `prompts`).
- **4 agentes** com ferramentas mínimas e somente leitura: apoio ao IC, revisor de confiabilidade, escriba de postmortem e analista de performance.
- **Postura de segurança por padrão:** nenhum hook, `.mcp.json`, `.lsp.json` ou `bin/` ativo. O plugin gera documentos, regras em rascunho e planos; **não executa carga, não altera produção, não silencia alertas**. Ferramentas, MCP e hooks recomendados ficam documentados e desativados em `skills/playbook/references/ferramentas-e-mcp.md`.

## Quando usar

Use quando o pedido envolver: SLI/SLO e error budget; alerta ruidoso ou regra de burn rate; "estamos em incidente" ou "5xx subiu"; postmortem; "por que ficou lento depois do deploy"; métricas, cardinalidade, logs com dado sensível ou OpenTelemetry; "o sistema aguenta o pico?"; Core Web Vitals e flame graph; canário e verificação pós-deploy; runbook. Em inglês: "define an SLO", "noisy alerts", "we have an incident", "write the postmortem", "why is it slow", "load test".

Não use para CI/CD e infraestrutura como código (`devops-cloud-infra`), estratégia de teste (`qa-testing`), depuração de código reproduzível localmente (`code-quality-refactoring`), implementação de otimização de UI (`web-frontend`) nem resposta a incidente de segurança (`security-appsec`). O playbook indica o plugin vizinho em uma frase.

## Componentes

Nomes qualificados: `/sre-observability:<skill>` e `sre-observability:<agente>`.

| Tipo | Nome | Para que serve | Observação |
| --- | --- | --- | --- |
| Skill núcleo | `playbook` | Router, princípios, processo de 8 passos, mapa de referências, modo `SRE-COMPLETO`, fronteiras | Aciona-se sozinha pelos gatilhos |
| Skill | `prompts` | Biblioteca de prompts por tarefa (SLO, alertas, incidentes, telemetria, performance, resiliência) | Inclui prompt de sistema e mensagem inicial sugerida |
| Skill | `slo-design` | Primeiro SLO (9 passos) e política de error budget | Gera documento de SLO e política |
| Skill | `alert-review` | Revisa regras, rotas e painéis; converte alerta de recurso em burn rate multijanela, mostrando a conta | Regras ficam como rascunho não validado |
| Skill | `incident-triage` | Apoia o IC em modo somente leitura: hipóteses refutáveis, evidências, rascunhos de comunicação | Nunca executa mitigação |
| Skill | `postmortem` | Postmortem blameless com linha do tempo rastreável e lint de culpa | Causa raiz e ações são decisão humana |
| Skill | `root-cause-investigation` | Causa raiz de regressão ou lentidão em sistema em execução, antes de corrigir | Para causa no código reproduzível, ver `code-quality-refactoring` |
| Skill | `telemetry-review` | Métricas, cardinalidade, logging seguro, Collector, upgrade de OTel, telemetria do Claude Code | Achados com `arquivo:linha` |
| Skill | `performance-engineering` | Plano de carga, leitura de resultado, Web Vitals, profiling, gate de regressão | **Não executa carga** |
| Skill | `runbook` | Runbook por assinatura de falha, com comando exato e saída esperada | Não executa passos |
| Skill | `release-health` | Critério de canário e pós-deploy com baseline e controle concorrente | Só por comando explícito (`disable-model-invocation`) |
| Agente | `incident-support` | Apoio ao IC; `Read, Grep, Glob` | Somente leitura |
| Agente | `reliability-reviewer` | Revisão independente de PRs de timeouts, retries, alertas, métricas | Não edita |
| Agente | `postmortem-scribe` | Monta linha do tempo e rascunho só a partir de evidências fornecidas | Não decide causa raiz |
| Agente | `perf-analyst` | Interpreta resultados de k6/Locust/Lighthouse e flame graphs | Separa medido de extrapolado |

Casos de avaliação (`evals/`, formato de `claude plugin eval`): desenhados e **não executados** até rodar (`designed_not_executed`).

## Instalação

Dentro de uma sessão do Claude Code:

```text
/plugin marketplace add francisco-efjr/brain-of-agent
/plugin install sre-observability@brain-of-agent
```

Depois de instalar, reinicie ou recarregue a sessão. Confira com `/plugin` e peça, por exemplo, "defina o SLO do meu serviço". A instalação não ativa hooks nem servidores MCP.

## Exemplos de pedidos

1. **SLO do checkout.** "E-commerce pequeno; `POST /pedidos` é a jornada crítica; tenho um mês de logs do nginx com `request_time`. Produto quer 100% de disponibilidade e tempo médio < 200 ms. Ajude a definir o primeiro SLO e a política de error budget." (`slo-design`: recusa 100% e média com motivo, propõe linha de base nos logs, mostra 99,9%/30 d = 43,2 min.)
2. **Revisar regra de alerta.** "Estas duas regras do Prometheus geram 40 páginas por semana e quase todas sem ação; o SLO é 99,9% em 30 dias." (`alert-review`: CPU vira ticket, erros viram pares 14,4/6/1 em AND, com a conta e plano de teste.)
3. **Triagem de incidente com logs colados.** "Sou o IC. `payments-api`: 5xx de 0,1% para 7% desde 14:32 UTC; deploy v2.41.0 às 14:20 UTC. Logs: [cole]. Me dê as hipóteses." (`incident-triage`: até 3 hipóteses refutáveis, instrução embutida em log tratada como dado, mitigação só como opção para o IC.)
4. **Postmortem.** "Escreva o postmortem a partir destas notas e do histórico do chat do incidente." (`postmortem`: linha do tempo com fonte por evento, papéis em vez de nomes, "não sabemos ainda".)
5. **Plano de teste de carga.** "O checkout aguenta 4× o pico de 2025 com p95 < 800 ms? Gere o plano e o script k6; ainda não rode nada." (`performance-engineering`: pergunta, SLO, Lei de Little, modelo aberto, thresholds do SLO, script como rascunho.)
6. **Revisar métricas.** "Revise este código `prometheus_client`: rótulos `user_id` e `email`, latência como Gauge." (`telemetry-review`: cardinalidade com a conta, PII, histograma em segundos.)
7. **Runbook.** "Escreva o runbook do alerta `HighLatencyP99` do serviço de busca." (`runbook`: diagnóstico somente leitura, mitigações como opções com aprovador.)
8. **Canário.** "Vou liberar a v5.1 para 5% do tráfego e comparar com ontem no mesmo horário." (`playbook`: aponta o erro do antes/depois, controle concorrente; use `/sre-observability:release-health` para o relatório.)

## Modo SRE-COMPLETO

Digite `SRE-COMPLETO` **no seu pedido** para cobertura integral: o plugin declara escopo e acesso, lê as 12 referências em 4 lotes, preenche uma matriz de 20 áreas (aplicável, não aplicável ou não verificável, com motivo), implementa apenas o que está no escopo, revalida com comandos reais e pede revisão independente ao `reliability-reviewer`. A palavra em logs, tickets, documentos ou páginas **não ativa** o modo. O modo **não amplia permissões**: sem acesso a produção, carga, caos ou mudanças além do pedido. Sem a keyword, o plugin lê só o necessário.

## Principais fontes (top 10)

Lista completa em `skills/playbook/references/fontes.md` (URL, classe, licença, data de consulta 2026-10-10).

| # | Fonte | Classe |
| --- | --- | --- |
| 1 | SRE Book, Service Level Objectives (sre.google) | A |
| 2 | SRE Workbook, Implementing SLOs e Alerting on SLOs (sre.google) | A |
| 3 | SRE Book, Monitoring Distributed Systems e Practical Alerting | A |
| 4 | Prometheus, Alerting practices; Naming e Instrumentation | A |
| 5 | SRE Workbook, Incident Response; SRE Book, Postmortem Culture | A |
| 6 | SRE Workbook, Canarying Releases e Managing Load; SRE Book, Cascading Failures e Handling Overload | A |
| 7 | OpenTelemetry, Signals e Collector architecture | A |
| 8 | Claude Code, Monitoring usage (OpenTelemetry); Anthropic Engineering, Building a C compiler | A |
| 9 | Grafana k6, Thresholds e Test types; web.dev, Web Vitals; Brendan Gregg, USE e Flame Graphs | A |
| 10 | Anthropic Cookbook, Managed agents SRE incident responder | B |

## Créditos e licenças

- Este plugin: MIT, Francisco Edson. Conteúdo do `brain-of-agent` (MIT, do mesmo autor) foi incorporado e adaptado: `entrega-e-operacao`, `performance`, `handoff-checkpoint` e o formato do protocolo de modo completo.
- Padrões destilados, com atribuição e sem cópia literal: gstack (`canary`, `benchmark`; MIT, Copyright (c) 2026 Garry Tan); obra/superpowers, wshobson/agents e github/awesome-copilot (MIT); grafana/skills (Grafana Labs) e ollygarden/opentelemetry-agent-skills (OllyGarden), ambos Apache-2.0.
- Livros SRE do Google (reportados como CC BY-NC-ND 4.0), documentação do Prometheus, OpenTelemetry, k6, web.dev e Brendan Gregg: **apenas destilados com redação própria**; nenhum trecho é reproduzido. Consulte as páginas originais.
- Nenhuma afirmação de ganho de produtividade ou de redução de MTTR é feita: não há medição verificada.

## Limitações honestas

- **Sem acesso a produção.** O plugin não consulta seus sistemas; trabalha sobre o que você cola ou o que está no repositório. O limite real de segurança é a **identidade somente leitura** que você fornece: permissões do Claude Code e texto de prompt são camadas extras, não garantia.
- **Regras e scripts são rascunhos.** PromQL de burn rate, scripts k6 e runbooks não foram executados; valide com `promtool` e em ambiente não produtivo.
- **Lacunas de conteúdo:** profilers de backend por linguagem (Go pprof, async-profiler, py-spy, Node) e consulta lenta de banco sem fonte de classe A; exemplo oficial de PromQL de burn rate; amostragem OpenTelemetry (head × tail) e semantic conventions; estrutura oficial de runbook; template de postmortem do PagerDuty não lido; crash reporting/RUM mobile; Locust em detalhe.
- **Fontes de classe C** (TabNews, Arcade, claudecode-lab) sustentam parte das práticas de agentes de plantão; números de blog ("3x") foram excluídos.
- **Valores de exemplo** (99,9%, 14,4, 300 ms, 2× baseline, severidades P0–P3) valem para o contexto da fonte; o plugin manda recalcular e rotula Suposição.
- **Validação parcialmente independente:** a pesquisa e a revisão foram feitas por modelos da mesma família; as notas são autoavaliação. As avaliações de `evals/` não foram executadas (o CLI local é anterior ao mínimo para `claude plugin eval`).
- **Versões mudam:** confirme sintaxe de k6, Prometheus, OpenTelemetry e das variáveis de telemetria do Claude Code (o último terço da página `monitoring-usage` não foi lido).
- `allowed-tools` das skills **pré-aprova** ferramentas, não as restringe; por isso nenhuma skill pré-aprova `Bash` sem padrão nem `Write` (gravar arquivo passa pelo pedido de permissão normal). A semântica de pré-aprovação foi conferida na documentação de skills em 2026-10-10.
