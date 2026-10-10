# Fontes (bibliografia validada)

Todas as consultas e verificações foram feitas em **2026-10-10** (pesquisa e validação do segmento; o plugin não acessa a web). Classes: **A** = oficial/norma/mantenedor; **B** = repositório ou veículo reconhecido com ressalvas; **C** = comunidade/fornecedor/sinal. A nota entre parênteses (0–10) é a pontuação do validador. "Tratamento": **destilado** = redação própria, nenhum trecho copiado; **literal** = texto reproduzido com licença permissiva e atribuição. Neste plugin **nenhum trecho de terceiros é reproduzido de forma literal**; os textos reutilizáveis são redações do validador/construtor ou do próprio usuário (brain-of-agent, MIT).

A validação foi feita por modelo da mesma família do pesquisador: independência parcial; a nota é autoavaliação (média 84,8 nas 12 reescritas), não validação externa. Estrelas e licenças mudam: confira antes de depender.

## Sumário

- [Fontes primárias (Top 20)](#fontes-primárias-top-20)
- [Demais fontes](#demais-fontes)
- [Documentação do Claude Code usada](#documentação-do-claude-code-usada)
- [Conteúdo próprio e de terceiros incorporado](#conteúdo-próprio-e-de-terceiros-incorporado)
- [Rejeitadas ou rebaixadas](#rejeitadas-ou-rebaixadas)
- [Índice V → onde é usado](#índice-v--onde-é-usado)
- [Licenças e atribuições](#licenças-e-atribuições)

## Fontes primárias (Top 20)

Os livros SRE do Google aparecem como **CC BY-NC-ND 4.0** na pesquisa do segmento `devops-cloud-infra` (V-54 de lá, © 2017, Verificado lá); a validação deste segmento diz "licença não verificada". Tratamento adotado: CC BY-NC-ND (não derivar, não copiar).

| # | Título | URL | Classe | Licença | Consulta | Tratamento | V |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SRE Book, Service Level Objectives | https://sre.google/sre-book/service-level-objectives/ | A (8) | CC BY-NC-ND 4.0 (reportado) | 2026-10-10 | destilado | V-01, V-02 |
| 2 | SRE Workbook, Implementing SLOs | https://sre.google/workbook/implementing-slos/ | A (8) | idem | 2026-10-10 | destilado | V-01, V-02 |
| 3 | SRE Workbook, Alerting on SLOs | https://sre.google/workbook/alerting-on-slos/ | A (8) | idem | 2026-10-10 | destilado | V-03 |
| 4 | SRE Book, Monitoring Distributed Systems | https://sre.google/sre-book/monitoring-distributed-systems/ | A (8) | idem | 2026-10-10 | destilado | V-04 |
| 5 | SRE Book, Practical Alerting | https://sre.google/sre-book/practical-alerting/ | A (8) | idem | 2026-10-10 | destilado | V-05 |
| 6 | Prometheus, Alerting practices | https://prometheus.io/docs/practices/alerting/ | A (9) | não verificada | 2026-10-10 | destilado | V-05 |
| 7 | Prometheus, Naming e Instrumentation | https://prometheus.io/docs/practices/naming/ · https://prometheus.io/docs/practices/instrumentation/ | A (9) | não verificada | 2026-10-10 | destilado | V-11 |
| 8 | SRE Workbook, Incident Response | https://sre.google/workbook/incident-response/ | A (8) | CC BY-NC-ND (reportado) | 2026-10-10 | destilado | V-08 |
| 9 | SRE Book, Postmortem Culture | https://sre.google/sre-book/postmortem-culture/ | A (8) | idem | 2026-10-10 | destilado | V-07 |
| 10 | SRE Workbook, Canarying Releases | https://sre.google/workbook/canarying-releases/ | A (8) | idem | 2026-10-10 | destilado | V-09 |
| 11 | Claude Code, Monitoring usage (OpenTelemetry) | https://code.claude.com/docs/en/monitoring-usage | A (9) | docs Anthropic; não verificada | 2026-10-10 | destilado (último terço não lido) | V-13 |
| 12 | OpenTelemetry, Signals e Collector architecture | https://opentelemetry.io/docs/concepts/signals/ · https://opentelemetry.io/docs/collector/architecture/ | A (9) | não verificada | 2026-10-10 | destilado | V-12 |
| 13 | Anthropic Engineering, Building a C compiler (N. Carlini, 2026-02-05) | https://www.anthropic.com/engineering/building-c-compiler | A (9) | não verificada | 2026-10-10 | destilado | V-14 |
| 14 | SRE Book, Addressing Cascading Failures · Handling Overload | https://sre.google/sre-book/addressing-cascading-failures/ · https://sre.google/sre-book/handling-overload/ | A (8) | CC BY-NC-ND (reportado) | 2026-10-10 | destilado | V-22 |
| 15 | SRE Workbook, Managing Load | https://sre.google/workbook/managing-load/ | A (8) | idem | 2026-10-10 | destilado | V-23 |
| 16 | Grafana k6, Thresholds e Test types · Locust docs | https://grafana.com/docs/k6/latest/using-k6/thresholds/ · https://grafana.com/docs/k6/latest/testing-guides/test-types/ · https://docs.locust.io/en/stable/what-is-locust.html | A (8) k6; B (7) Locust | docs k6 não verificada; Locust MIT | 2026-10-10 | destilado. A URL antiga `.../load-test-types/` dá 404 | V-21 |
| 17 | obra/superpowers `systematic-debugging` (+ awesome-copilot `debug.agent.md`, wshobson `debugger.md`) | https://github.com/obra/superpowers | A (8) pelo padrão | MIT (297.057★, push 2026-10-10) | 2026-10-10 | padrão destilado com atribuição; redação própria | V-15 |
| 18 | Brendan Gregg, USE method · Flame Graphs | https://www.brendangregg.com/usemethod.html · https://www.brendangregg.com/flamegraphs.html | A (8) | não verificada | 2026-10-10 | destilado | V-06, V-25 |
| 19 | web.dev, Web Vitals (metas "bom"); artigos de LCP, INP e CLS (limiares "ruim") | https://web.dev/articles/vitals · https://web.dev/articles/lcp · https://web.dev/articles/inp · https://web.dev/articles/cls | A (9) | não verificada | 2026-10-10 | destilado | V-19 |
| 20 | Anthropic Cookbook, Managed agents SRE incident responder (2026-04-10) | https://platform.claude.com/cookbook/managed-agents-sre-incident-responder | B (7) | não verificada | 2026-10-10 | destilado; aprovação só por prompt no exemplo | V-17, V-18 |

## Demais fontes

| Fonte | URL | Classe | Licença | Consulta | Uso e tratamento | V |
| --- | --- | --- | --- | --- | --- | --- |
| SRE Book, Being On-Call | https://sre.google/sre-book/being-on-call/ | A (8) | CC BY-NC-ND (reportado) | 2026-10-10 | carga de plantão e toil; destilado | V-24 |
| Grafana, RED method (J. Dam, 2018-08-03; método de Tom Wilkie) | https://grafana.com/blog/the-red-method-how-to-instrument-your-services/ | B (7) | não verificada | 2026-10-10 | RED; destilado | V-06 |
| grafana/skills (`grafana-k6/k6`, `grafana-core/promql`, `grafana-core/alerting-irm`) | https://github.com/grafana/skills | B (6) | Apache-2.0 (282★) | 2026-10-10 | notas de PromQL e boa prática de carga; destilado + atribuição a Grafana Labs; referenciar como plugin à parte | V-27 |
| ollygarden/opentelemetry-agent-skills (`otel-upgrade`) | https://github.com/ollygarden/opentelemetry-agent-skills | B (6) | Apache-2.0 (106★) | 2026-10-10 | processo de upgrade; destilado + atribuição a OllyGarden | V-28 |
| garrytan/gstack (`canary`, `benchmark`) | https://github.com/garrytan/gstack | B (7/6) | MIT, Copyright (c) 2026 Garry Tan (135.780★) | 2026-10-10 | padrões destilados com atribuição; preâmbulo, telemetria e instaladores não reproduzidos | V-10, V-20 |
| wshobson/agents (`incident-responder`, `debugger`) | https://github.com/wshobson/agents | B (6) | MIT (40.318★) | 2026-10-10 | tabela de severidade P0–P3 (Suposição de aplicabilidade) | V-08, V-15 |
| github/awesome-copilot (`performance-optimization.instructions.md`, `debug.agent.md`) | https://github.com/github/awesome-copilot | B (6) | MIT (39.881★) | 2026-10-10 | checklist CWV (50+ regras; pontos contestáveis não copiados) | V-19, V-15 |
| Principles of Chaos | https://principlesofchaos.org/ | B (7) | não declarada | 2026-10-10 | passos do experimento; destilado | V-29 |
| Chaos Mesh docs | https://chaos-mesh.org/docs/ | B | docs CC-BY-4.0; software não declarado na página | 2026-10-10 | só citado; exige Kubernetes | V-29 |
| Hamel Husain, Evals FAQ (2026-09-18) | https://hamel.dev/blog/posts/evals-faq/ | B (6) | não verificada | 2026-10-10 | análise de erros em traces de LLM; destilado | V-30 |
| TabNews, Agent de incidentes (andersonlimadev) | https://www.tabnews.com.br/andersonlimadev/agent-de-incidentes-com-claude-code-investigar-sem-tocar-em-producao | C (4) | não verificada | 2026-10-10 | identidade somente leitura (PT-BR); destilado | V-16 |
| Arcade, Claude Code AI SRE (M. Chawla, 2026-04-17) | https://www.arcade.dev/blog/claude-code-ai-sre-oncall-workflows | C (4) | não verificada | 2026-10-10 | aprovação antes de escrita, auditoria; blog de fornecedor | V-16 |
| Mergify, markdown on-call (2026-04-14) · Anthropic, How teams use Claude Code (2025-07-24) | https://mergify.com/blog/markdown-file-oncall-cheat-code · https://claude.com/blog/how-anthropic-teams-use-claude-code | B (6) | não verificada | 2026-10-10 | runbooks como arquivos; "3x" é auto-relato e não entra | V-18 |
| claudecode-lab, logging e monitoring (2026-03-31) | https://claudecode-lab.com/en/blog/claude-code-logging-monitoring/ | C (4) | não verificada | 2026-10-10 | logging seguro (com correções); destilado | V-26 |
| Ronacher, Agentic coding (2025-06-12) | https://lucumr.pocoo.org/2025/6/12/agentic-coding/ | C (4) | não verificada | 2026-10-10 | log em arquivo, pidfile | V-14 |
| o11y-dev/opentelemetry-skill | https://github.com/o11y-dev/opentelemetry-skill | C (3) | Apache-2.0 (48★, v0.5.3) | 2026-10-10 | guardrails do Collector = **Suposição** | V-12 |
| VoltAgent/awesome-claude-code-subagents | https://github.com/VoltAgent/awesome-claude-code-subagents | C (prompt) / B (catálogo) | MIT (~25,6 mil★) | 2026-10-10 | só mapa de cobertura; `sre-engineer` nota 43 | n/a |
| PagerDuty incident-response-docs | https://response.pagerduty.com/ | pendente de leitura | Apache-2.0 (repositório, ~1,1 mil★) | 2026-10-10 | modelo de postmortem e "during an incident" **não lidos** (lacuna) | V-07 |

## Documentação do Claude Code usada

| Página | URL | Uso |
| --- | --- | --- |
| Plugins reference · Plugin marketplaces · Skills · Sub-agents · Settings | https://code.claude.com/docs/en/plugins-reference · https://code.claude.com/docs/en/plugin-marketplaces · https://code.claude.com/docs/en/skills · https://code.claude.com/docs/en/sub-agents · https://code.claude.com/docs/en/settings | Formato do plugin e semântica de `allowed-tools`/permissões (A; lidas na fundação da fábrica em 2026-10-09; **confirme na versão instalada**) |
| Índice geral da documentação | https://code.claude.com/docs/llms.txt | Ponto de partida para MCP e hooks |
| Claude Code power user tips (pista) | https://support.claude.com/en/articles/14554000-claude-code-power-user-tips | Pista de `PostCompact` (**Não verificada**) |

## Conteúdo próprio e de terceiros incorporado

| Origem | Licença | Onde entra | Tratamento |
| --- | --- | --- | --- |
| brain-of-agent `brains/fullstack/references/entrega-e-operacao.md` (https://github.com/francisco-efjr/brain-of-agent; a URL respondeu 404 sem autenticação em 2026-10-10, possivelmente repositório privado: Não verificável publicamente) | MIT (do usuário) | critério de serviço, caso 202/fila, rollout e reversão, checklist de entrega | adaptado |
| brain-of-agent `brains/qa/references/performance.md` | MIT (do usuário) | `performance-e-carga.md`, templates de relatório e k6 | adaptado; **não reverificado externamente** (Inferido onde indicado) |
| brain-of-agent `brains/fullstack/assets/templates/handoff-checkpoint.md` | MIT (do usuário) | `handoff-checkpoint-sre.md` | adaptado |
| brain-of-agent `brains/fullstack/references/protocolo-completo.md` | MIT (do usuário) | forma do modo `SRE-COMPLETO` e matriz de aplicabilidade | adaptado |
| gstack `canary/SKILL.md`, `benchmark/SKILL.md` (v1.91.27, commit `c285d88b…`) | MIT, Copyright (c) 2026 Garry Tan | `release-health`, `relatorio-canario.md`, regressão de performance | destilado com atribuição |

## Rejeitadas ou rebaixadas

Não usar como fonte de conteúdo: gstack `investigate` como skill (nota 40; só parâmetros), VoltAgent `sre-engineer` (nota 43), akin-ozer/cc-devops-skills (sem leitura), prepostmortem-skills (sem leitura, 1★), borghei/Claude-Skills (MIT + Commons Clause), claudecodeguides "resumo de Reddit" (sem links), SigNoz/dev.to (duplica V-13), Ask HN e Dan Luu (rebaixados a sinal; estimativas não reverificadas). Números de comunidade ("3x", "50%", "95% dos casos") não entram.

## Índice V → onde é usado

| V | Tema | Referência |
| --- | --- | --- |
| V-01, V-02 | SLO e política de error budget | `slo-error-budget.md` |
| V-03, V-04, V-05, V-06, V-27 | burn rate, sinais, alertas, USE/RED, PromQL | `alertas-e-sinais.md` |
| V-11, V-12, V-13, V-14, V-26, V-28, V-30 | métricas, Collector, telemetria do Claude Code, logs, upgrade, LLM | `telemetria-otel.md` |
| V-07, V-08, V-16, V-17, V-18, V-24 | incidente, postmortem, runbook, plantão | `incidentes-e-postmortem.md`, `slo-error-budget.md` |
| V-19, V-20, V-21, V-25 | CWV, regressão, carga, flame graph | `performance-e-carga.md` |
| V-09, V-10, V-22, V-23, V-29 | canário, pós-deploy, cascata, capacidade, caos | `resiliencia-canario-capacidade.md` |
| V-15 | causa raiz | `claude-md-snippets.md` (CM-14), skill `root-cause-investigation` |

## Licenças e atribuições

- gstack (Garry Tan), MIT: padrão de monitoramento pós-deploy e de regressão de performance, destilado.
- obra/superpowers, wshobson/agents, github/awesome-copilot, MIT: padrões de depuração e tabela de severidade, destilados.
- grafana/skills (Grafana Labs) e ollygarden/opentelemetry-agent-skills (OllyGarden), Apache-2.0: boas práticas de PromQL/k6 e processo de upgrade de OTel, destilados.
- Livros SRE do Google (CC BY-NC-ND), Prometheus, OpenTelemetry, k6, web.dev, Brendan Gregg: **apenas destilados**, com remissão à fonte.
- Conteúdo do brain-of-agent: MIT, do próprio autor do plugin.
