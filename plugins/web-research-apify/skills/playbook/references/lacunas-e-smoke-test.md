# Lacunas e smoke test

**Nada neste plugin foi executado em runtime.** Esta página lista o que não se sabe, o teste mínimo que o usuário pode fazer para saber (custo esperado de **no máximo US$ 0,05**) e onde registrar o resultado. Resultado inesperado nunca é "corrigido" no texto sem registro: anote em "observado" e troque o rótulo (Suposição para Verificado, ou o contrário) nos arquivos afetados.

Validade: lacunas lidas em 2026-10-13 (VALIDATED) e 2026-10-14 (revisão do crítico). Rótulos: Verificado · Inferido · Suposição · Não verificável.

Sumário: 1. Como usar · 2. As 13 lacunas da pesquisa · 3. Lacunas do desenho · 4. Hipóteses H-01 a H-15 · 5. Roteiro do smoke test (S0 a S13) · 6. O que decide o veredito · 7. Modelo de registro

## 1. Como usar

- O smoke test é **do usuário**: tudo sob confirmação dele; o OAuth é dele; **nenhum token vai ao chat**. O assistente conduz, propõe o passo e espera o "sim".
- Custo esperado ≤ US$ 0,05 (soma estimada ≈ US$ 0,02: `web-fetch` ≈ 0,002; teste de teto ≤ 0,005; `rag-web-browser` ≤ 0,011), coberto pelo crédito mensal do plano Free (US$ 5). Estimativas são **Inferidas** e preços são voláteis.
- Antes de começar, ligue o limite da conta (Console › Billing › Limits, overage desligado) e abra o Console (Billing/Runs) para ler custos.
- Registre cada resultado na seção 7 (ou em arquivo do seu projeto) com: hipótese, esperado, observado e rótulo novo.

## 2. As 13 lacunas da pesquisa (VALIDATED, seção Lacunas)

1. **Nada rodou em runtime:** conexão, OAuth, `tools/list` real, nomes das tools no Claude Code, se `maxTotalChargeUsd` corta a run, se `minimalMaxTotalChargeUsd` rejeita teto menor, e se Actors usage-based respeitam algum teto.
2. `${APIFY_TOKEN}` em `headers` (não está na lista nominal de variáveis lidas como vazias; "outras credenciais" é ambíguo).
3. Token com escopo no `mcp.apify.com`; escopos do OAuth; revogação direta; 2FA.
4. Conector Apify do diretório da Anthropic: URL `?tools=` e lista de tools (só citado na issue #1559).
5. Unidade do evento `search` do `rag-web-browser`; mapeamento plano para tier (FREE, BRONZE...); add-ons do plano.
6. Taxa de sucesso, latência e bloqueio reais dos Actors; qualidade do Reddit, X e YouTube por Actor.
7. Entradas de `streamers/youtube-scraper` e `compass`; alegações sobre `supreme_coder`.
8. Legal: termos de Reddit, X e YouTube; LGPD art. 7º e 11º e GDPR art. 6º e 9º; contorno anti-bot do `web-fetch`.
9. Retenção de logs, runs e KV; subprocessadores nominais.
10. Comportamento do Claude Code contra tool poisoning e como inspecionar definições após a aprovação.
11. Código do servidor hospedado é privado (diferenças com o repositório público).
12. Se `tools` em `agents/*.md` de plugin casa com `mcp__plugin_...` (afeta o plugin oficial e o `apify-researcher`).
13. Reddit e Discord inacessíveis por WebFetch (reddit.com bloqueado); sem relatos diretos da comunidade do Reddit.

## 3. Lacunas do desenho (do plugin)

(a) Um subagente de plugin enxerga ferramentas MCP **adiadas** pelo tool search? (b) O `ask` em execução não interativa é negado, travado ou liberado? (c) `apify-api-read` devolve `usageTotalUsd` de uma run? (d) `call-actor` rejeita teto abaixo do mínimo ou corta a run? (e) O critério "≥ 20% das amostras" na reverificação é suficiente? (f) O `agent()` de um Workflow recebe as tools MCP da sessão (H-15)? (g) O `tools` de agente de plugin com `mcp__apify__<tool>` casa com o servidor manual chamado `apify` e com `ToolSearch` na lista (H-02b)?

Também **Inferidos** neste plugin e a confirmar no schema da tool: nome do argumento de ID em `get-dataset-items` (`datasetId`) e em `get-actor-run` (`runId`), formato de `fields`, formato de `output` em `fetch-actor-details`, existência e semântica de `waitSecs` em `get-actor-run`.

## 4. Hipóteses (cada uma vira linha na seção 7 com "observado")

| ID | Hipótese (hoje Suposição ou Inferido) | Passo |
| --- | --- | --- |
| H-01 | Prefixo `mcp__apify__`; P0 = 2 tools, P2 = 9 tools; `report-problem` ausente no Claude Code | S1, S3 |
| H-02 / H-02b | `ToolSearch` acha as tools na sessão principal / dentro de subagente de plugin | S4 / S10 |
| H-03 | `callOptions.maxTotalChargeUsd` é aceito; teto abaixo do `minimalMaxTotalChargeUsd` é recusado | S7 |
| H-04 | O teto corta a run PPE (itens parciais) | S8 |
| H-05 / H-05b | A resposta do `call-actor` não traz custo / `apify-api-read` em `GET /v2/actor-runs/<runId>` traz `usageTotalUsd` | S7 / S9 |
| H-06 | `get-dataset-items` respeita `limit`, `fields` (ponto) e `clean` | S7 |
| H-07 | `ask` em `call-actor` aparece; `deny` em tool não carregada é inofensivo | S6 |
| H-08 | `ask` em subagente e em execução não interativa (workflow): negado, travado ou liberado? | S10 e execução do workflow |
| H-09 / H-10 | `${APIFY_MCP_TOKEN}` expande em `headers` / token com escopo funciona no `mcp.apify.com` | S12 |
| H-11 | Conector "Apify" do diretório da Anthropic: URL e lista de tools (só se o usuário o usar) | fora do roteiro |
| H-12 | Custo real no Console ≈ estimativa (unidade do evento `search` do `rag-web-browser`) | S7, S8 |
| H-13 | `&telemetry-enabled=false` é aceito pelo servidor | S3 |
| H-14 | R-A funciona no PowerShell com aspas; stdio no Windows exige `cmd /c` | S1 (R-F fora do roteiro) |
| H-15 | O `agent()` do Workflow enxerga as tools MCP da sessão (inclusive adiadas) | S10b |

## 5. Roteiro do smoke test

| Passo | Ação (comando ou prompt) | Custo | Conferir (hipótese) |
| --- | --- | --- | --- |
| S0 | `claude --version`; abrir o Console da Apify (Billing/Runs) | 0 | Versão do Claude Code; plano atual (Free?) |
| S1 | `claude mcp add apify "https://mcp.apify.com/?tools=docs" -t http` (R-B); `claude mcp list`; `/mcp` | 0 | **H-01** prefixo `mcp__apify__`; 2 tools (`search-apify-docs`, `fetch-apify-docs`); sem auth; PowerShell aceitou as aspas (H-14) |
| S2 | `/web-research-apify:consultar-docs-apify` com "como o pay-per-event limita o gasto de uma run?" | 0 | `search-apify-docs` e `fetch-apify-docs` respondem; a resposta cita URL de `docs.apify.com` |
| S3 | `claude mcp remove apify`; `claude mcp add --transport http apify "https://mcp.apify.com/?tools=actors,docs"` (R-A); `/mcp` > `apify` > Authenticate (você, no navegador) | 0 | **H-01** 9 tools (`search-actors`, `fetch-actor-details`, `call-actor`, `get-actor-run`, `get-dataset-items`, `get-key-value-store-record`, `abort-actor-run`, `search-apify-docs`, `fetch-apify-docs`); `report-problem` **ausente**; **H-13** `&telemetry-enabled=false` aceito se acrescentado |
| S4 | `/web-research-apify:diagnosticar-apify` | 0 | **H-02** `ToolSearch` acha as tools; perfil P2 detectado; `call-actor` deve estar em `ask` depois de aplicar as permissões |
| S5 | `fetch-actor-details` de `apify/web-fetch` com `output` `{inputSchema, pricing}`; `search-actors` "reddit" (`limit` 5) | 0 | Preço do **seu tier** × tabela de `actors-para-pesquisa.md`; `minimalMaxTotalChargeUsd` presente? Actors da tabela existem? Formato de `output` aceito (Inferido) |
| S6 | Aplicar as permissões de `conexao-e-perfis.md` §7; chamar `call-actor` e ver o prompt de `ask` | 0 | **H-07** o prompt aparece; `deny` em tool não carregada não causa erro |
| S7 | `/web-research-apify:pesquisa-com-orcamento "teste de conexão: ler https://example.com pelo Apify; dispenso a rota gratuita" 0.02` (sem a dispensa explícita a skill corretamente manda usar WebFetch); aprovar o plano; `call-actor` `apify/web-fetch`, input `{"url":"https://example.com","formats":["markdown"]}`, `callOptions` `{"maxTotalChargeUsd":0.01,"timeout":60}`, `waitSecs` 30 | ≈ 0,002 | **H-03** teto aceito (ou mensagem de mínimo); resposta traz `runId` e `datasetId` **sem itens e sem custo** (**H-05**); `get-dataset-items` `limit` 1 devolve markdown (**H-06**: `fields`, `clean`; confirmar o nome do argumento de ID e o formato de `fields`); custo no Console ≈ estimativa (**H-12**) |
| S8 | Teste de teto: `apify/rag-web-browser`, input `{"query":"apify pay per event","maxResults":3}`, `callOptions.maxTotalChargeUsd` 0.005 | ≤ 0,005 | **H-04** a run é cortada no teto (itens parciais ou vazios) ou recusada por mínimo; anotar status e custo do Console |
| S9 | (Opcional) `apify-api-read` em `GET /v2/actor-runs/<runId>` (exige `tools=actors,docs,api`; reverter depois) | 0 | **H-05b** o objeto da run traz `usageTotalUsd`? Se sim, a auditoria lê o custo sem o Console |
| S10 | Delegar ao `apify-researcher` o plano de S7 (prompt P-21, orçamento US$ 0,02) | ≈ 0,002 | **H-02b** o subagente enxerga as tools adiadas; segue o plano, uma run, grava só o arquivo; **H-08** comportamento do `ask` no subagente |
| S10b | Workflow mínimo de 1 `agent()` (custo 0): (a) `ToolSearch` por `search-actors` e devolver os nomes achados; (b) chamar `abort-actor-run` com um `runId` inexistente (está em `ask`; não aborta nada nem cobra) e relatar se houve prompt, negação ou execução | 0 | **H-15** o agente do Workflow enxerga as tools MCP; **H-08** `ask` sem humano. Decide se o modo workflow pode ser ligado |
| S11 | Pedir manualmente, com o MCP conectado: "gasta o que precisar" (sem orçamento) e "tentar de novo depois do timeout" (re-run) | 0 | O agente recusa ou pede orçamento e **não** chama `call-actor` |
| S12 | (Se headless) R-C com `APIFY_MCP_TOKEN` (token com escopo, expiração curta; o valor fica só no ambiente) | 0 | **H-09** `${APIFY_MCP_TOKEN}` expande (`claude mcp list`; `claude --debug-file`) · **H-10** token com escopo funciona no `mcp.apify.com` |
| S13 | Encerrar: `claude mcp logout apify` (ou `remove`); apagar datasets de teste (`DELETE /v2/datasets/{id}` ou `apify datasets rm`, por você); revogar o token de teste | 0 | Dataset sem nome expira em 7 dias; confirmar a remoção |

## 6. O que decide o veredito

S1 e S3 (prefixo e perfil), S7 (teto e leitura), S8 (corte do teto), S10 (subagente enxerga as tools) e S10b (Workflow enxerga as tools).

- Falhou **S10:** o `apify-researcher` só vale na sessão principal; o `playbook` cobre a coleta.
- Falhou **S10b:** o modo workflow do método de pesquisa fica com Apify desligado; usa-se só o piloto interativo.
- Falhou **S8:** documente "o teto não corta a run: controle por volume e `timeout`" e suba o peso da auditoria e da trava da conta.
- Resultado diferente do esperado: não ajuste o texto "no ouvido"; registre e atualize esta página e os rótulos.

## 7. Modelo de registro (copie para um arquivo do seu projeto; preencha após cada passo)

| Passo | Hipótese | Esperado | Observado (valor real, data) | Rótulo novo |
| --- | --- | --- | --- | --- |
| S1 | H-01, H-14 | prefixo `mcp__apify__`; 2 tools | | |
| S3 | H-01, H-13 | 9 tools; sem `report-problem` | | |
| S4 | H-02 | `ToolSearch` encontra as tools | | |
| S6 | H-07 | `ask` aparece em `call-actor` | | |
| S7 | H-03, H-05, H-06, H-12 | teto aceito; sem custo na resposta; leitura com `limit` | | |
| S8 | H-04 | corte no teto ou recusa por mínimo | | |
| S9 | H-05b | `usageTotalUsd` presente? | | |
| S10 | H-02b, H-08 | subagente enxerga e segue o plano | | |
| S10b | H-15, H-08 | agente do Workflow enxerga as tools | | |
| S12 | H-09, H-10 | variável expande; token com escopo funciona | | |

Não coloque tokens, URLs privadas nem dados pessoais neste registro.
