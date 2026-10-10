# Decisões, trade-offs e fronteiras

Conflitos entre fontes (K1 a K15) com a resolução adotada, árvores de decisão curtas e a tabela de fronteiras com os demais plugins. Consulta às fontes: 2026-10-10.

## Sumário

- [Conflitos e resolução](#conflitos-e-resolução)
- [Árvores de decisão](#árvores-de-decisão)
- [Fronteiras com outros plugins](#fronteiras-com-outros-plugins)

## Conflitos e resolução

| ID | Conflito | Resolução no plugin | Itens |
| --- | --- | --- | --- |
| K1 | `for:`: Prometheus e "Practical Alerting" recomendam; o Workbook desaconselha em alerta de SLO | Burn rate multijanela **sem** `for:` para SLO; `for:` ≥ 2 ciclos para alerta de recurso | V-03, V-05 |
| K2 | Aprovação de produção: cookbook (por prompt) × TabNews/Arcade (identidade/ferramenta) × handler fixo no notebook | Camadas: identidade somente leitura > aprovação no sistema > permissões do Claude Code > texto do prompt; o plugin só entrega a última | V-16, V-17, AP-11 |
| K3 | Limiar de canário fixo (gstack: 2×, 50%/500 ms, 25% de bundle) × controle concorrente e SLIs (Workbook) | Controle concorrente e SLIs do SLO; números do gstack viram **exemplo, Suposição**, relativos ao baseline próprio | V-09, V-10, V-20 |
| K4 | "2 checagens consecutivas" (gstack) × burn rate multijanela | Não competem: 2 checagens filtram ruído de **polling sintético**; burn rate filtra **alerta de SLO** | V-03, V-10 |
| K5 | Tentativas: 3 (superpowers, gstack) × 2 (site rejeitado) × 5 arquivos (gstack) | 3 tentativas falhas ⇒ parar e re-planejar; > 5 arquivos ⇒ pedir confirmação (Suposição, escolha do autor) | V-15 |
| K6 | Ferramentas do agente de debug: awesome-copilot (`runInTerminal`, `editFiles`) × cookbook/TabNews (somente leitura) | `tools` declaradas e mínimas; incidente: `Read, Grep, Glob`; mutação fora do plugin | V-15, V-08 |
| K7 | Tabela de severidade P0–P3 (wshobson) × Workbook (não define) | Exemplo editável (Suposição); a organização define | V-08 |
| K8 | Papéis: Workbook IC/OL/CL × SRE Book (acrescenta Planning Lead) | IC/OL/CL como núcleo; Planning Lead opcional (≥ 3 pessoas ou incidente longo); OL é o único que muda o sistema | V-08, devops V-54 |
| K9 | Lab × campo em web performance | Campo (p75, mobile × desktop) decide; laboratório só diagnóstico/regressão; Lighthouse em modo de navegação não mede INP (timespan mede só interações roteirizadas) | V-19 |
| K10 | Locust (fechado por padrão) × k6 `*-arrival-rate` (aberto) | Aberto para site/API públicos; fechado para população fixa; vigiar coordinated omission e `dropped_iterations` | brain (Inferido) |
| K11 | Mediana de 3 execuções: gstack (opcional) × brain/CI (3–5 e mediana) | Mediana quando houver ruído; runner compartilhado ⇒ repetir 3–5 vezes; ausência registrada como ausência | V-20, brain |
| K12 | Runbook no `CLAUDE.md` (Mergify) × CLAUDE.md < 200 linhas × arquivo por assinatura (cookbook) | Um arquivo por assinatura no repositório; CLAUDE.md só aponta | V-18, P-37 |
| K13 | Limiares "ruim" de CWV ausentes da página /vitals, presentes nos artigos de LCP, INP e CLS do web.dev (conferido 2026-10-10) e em awesome-copilot | "Bom" e "ruim" Verificados no web.dev | V-19 |
| K14 | Console enxuto para o agente × telemetria rica para humanos | Dois canais: resumo no console, detalhe em arquivo; em produção, telemetria completa **com redação e sem conteúdo de prompt** | V-14, V-13, V-26 |
| K15 | "3x mais rápido" com runbooks (blog Anthropic) e "50% erradas" (Dan Luu) | Nenhum número entra: auto-relato e estimativa | V-18, V-16 |

## Árvores de decisão

**Página × ticket × dashboard**

```text
Há impacto no usuário agora, ou o budget esgota em horas?   → sim: PÁGINA (burn rate rápido)
O budget esgota em dias, ou o recurso falta em dias?        → sim: TICKET (burn rate lento / alerta de recurso)
É contexto para depurar?                                    → sim: DASHBOARD
Ninguém age quando dispara?                                 → apague ou rebaixe
```

**SLO × SLA.** Existe consequência explícita (contrato, multa, crédito) para o descumprimento? Sim ⇒ SLA (e o SLO interno deve ser mais apertado). Não ⇒ SLO. (V-01)

**Blue-green × canário**

| Critério | Blue-green | Canário |
| --- | --- | --- |
| Exposição | Tudo de uma vez após a troca | Gradual, pequeno percentual primeiro |
| Reversão | Rápida (volta o tráfego) | Rápida (zera o canário) |
| Custo | Ambiente duplicado | Menor |
| Condição | Estado compartilhado compatível | **Duas versões convivendo** e métricas confiáveis por versão |
| Limita gasto de budget | Não | Sim (canário pequeno) |

Se o schema ou o protocolo não permite duas versões simultâneas, canário não se aplica: use blue-green com janela e plano de correção para frente.

**Modelo aberto × fechado.** Quem chega independentemente do tempo de resposta (site, API pública, app)? Aberto. População fixa que só envia após a resposta (200 atendentes, pool de workers)? Fechado, com think time realista. Em dúvida: aberto, e vigie `dropped_iterations`.

**Head × tail sampling (lacuna; Suposição).** Head decide no início do trace: barato e simples, mas descarta sem saber se o trace terá erro ou lentidão. Tail decide com o trace completo: mantém erros e lentos, mas exige buffer, memória e roteamento de todos os spans do mesmo trace para o mesmo coletor. Não há fonte A lida neste segmento; confirme na documentação do Collector.

**Mediana × passada única.** Ambiente dedicado e estável ⇒ uma passada pode bastar; runner compartilhado ou métrica ruidosa ⇒ repetir 3–5 vezes e usar a mediana; nunca reprovar por uma execução isolada (K11).

**Causa no código ou no sistema em execução?** Reproduz localmente com teste unitário/stack trace ⇒ `code-quality-refactoring:debug-causa-raiz`. Sintoma só aparece em produção/telemetria, regressão pós-deploy, incidente ou performance ⇒ `root-cause-investigation` aqui.

## Fronteiras com outros plugins

Regra geral: em sobreposição, o plugin dono do **artefato** atua; o outro apenas aponta (uma frase). Cite como `/<slug>:playbook`. "Aqui" = `sre-observability`.

| Segmento (`/<slug>:playbook`) | Aqui | Lá | Desempate |
| --- | --- | --- | --- |
| product-discovery-specs | NFR de confiabilidade vira SLO/SLI mensurável; SLO como critério de aceite | Descoberta, PRD, histórias | "requisito não funcional de disponibilidade/latência" ⇒ SLO aqui |
| architecture-design | Medir e operar resiliência; capacidade; modos de falha na operação | Desenho de arquitetura, DDD, ADR, escolha de padrões de resiliência no projeto | "desenhar" ⇒ lá; "operar, medir, alertar" ⇒ aqui |
| web-frontend | Metas CWV, RUM em produção, interpretação de campo, regressão | Implementar a otimização no código de UI | "otimizar componente/bundle" ⇒ lá; "p75 de campo, SLO de UX" ⇒ aqui |
| backend-api | SLO/alertas/trace de API; revisão de timeouts/retries/shedding; capacidade | Design de API, contratos, implementação, logs estruturados como princípio | "implementar endpoint/retry-after" ⇒ lá |
| mobile-apps | SLO de backend do app (crash/RUM mobile: lacuna aqui) | Android vitals, perfil de plataforma | "métrica nativa de plataforma" ⇒ lá |
| database-data-modeling | Triagem de incidente de banco; capacidade; SLI de dados | Modelagem, índices, EXPLAIN, locks | "consulta lenta/lock" ⇒ lá; "o banco causa incidente" ⇒ triagem aqui, diagnóstico lá |
| data-engineering | SLO de frescor/completude de pipeline; alerta de pipeline | Orquestração, qualidade de dados, DAGs | "SLO de frescor" ⇒ aqui |
| data-science-ml | Monitoramento do serviço de inferência (RED, SLO) | Treino, drift, avaliação de modelo | "latência/erro do endpoint do modelo" ⇒ aqui |
| llm-ai-agents | Telemetria, SLO, alertas e incidentes de apps LLM; análise de erros em traces | Convenções OTel GenAI, prompts, evals, agentes | "atributos gen_ai" ⇒ lá; "alertar, medir custo/latência" ⇒ aqui |
| devops-cloud-infra | Incidente, papéis, postmortem blameless, runbooks, SLO/SLI, alertas, on-call; critérios de saúde do canário | CI/CD, IaC, K8s, GitOps, rollout técnico, `infra-troubleshoot` | "postmortem/IC" ⇒ aqui; "pod não sobe/pipeline falhou" ⇒ lá |
| security-appsec | Logging sem dado sensível, alertas que disparam, telemetria do agente | Ameaças, SAST/DAST, OWASP, segredos | "incidente de segurança" ⇒ lá (resposta); aqui só papéis e linha do tempo |
| qa-testing | Limiares/SLO de teste de carga, canário, shift-right, caos em produção | Estratégia de teste, flaky, E2E, massa de dados | "teste de carga" ⇒ estratégia lá; thresholds/SLO/execução segura aqui |
| code-quality-refactoring | Regressão de produção com telemetria; postmortem | `debug-causa-raiz` (causa no código reproduzível), refatoração | "causa no código, repro local" ⇒ lá |
| ux-ui-design | INP/CLS como metas de percepção em campo | Heurísticas, design | n/a |
| technical-writing-docs | Conteúdo operacional do runbook (comandos, lógica, escalonamento), SLO, postmortem | Estrutura e redação do runbook como texto | "escrever claramente" ⇒ lá; "qual comando/o que faz" ⇒ aqui |
| game-development | Telemetria/SLO de servidores de jogo (genérico) | Engines, builds | Não aplicável na maior parte |
| systems-embedded-iot | Telemetria de frotas na nuvem (genérico) | Firmware, OTA | Não aplicável na maior parte |
| cli-desktop-tooling | Telemetria opt-in de CLI (V-13 como exemplo de privacidade) | Empacotamento, auto-update | n/a |
| blockchain-web3 | SLO de nós/RPC (genérico) | Contratos, chaves | Não aplicável na maior parte |
| automation-integrations | Alerta e confiabilidade de integrações/webhooks; política de retry (V-22) | Fluxos no-code, conectores | "retry de webhook" ⇒ ambos |
| git-workflow-release | Saúde pós-deploy, SLO, runbook de rollback de serviço | Branching, `revert`, versionamento | `rollback-plan` de lá aponta para o runbook daqui |
| saas-multitenant | SLO por tenant; cardinalidade do rótulo `tenant_id` (V-11) | Isolamento, planos, cobrança | "rótulo tenant" ⇒ regra aqui; modelo lá |
| fintech-payments | SLO e alertas de fluxo de pagamento; reconciliação como SLI de correção | Regras de pagamento, PCI, ledger | "pagamento fora do ar" ⇒ incidente aqui |
| ecommerce-marketplace | Capacidade de pico, SLO de checkout, teste de carga | Catálogo, carrinho, regras de negócio | "aguenta o pico" ⇒ aqui |
