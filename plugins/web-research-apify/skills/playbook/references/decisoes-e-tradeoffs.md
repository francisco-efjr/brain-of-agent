# Decisões e trade-offs

Use antes de conectar ou de planejar. Cada decisão traz a recomendação, o custo de escolher o outro lado e, quando cabe, a medição que mudaria a escolha. Validade: lido em 2026-10-13 (V-01 a V-34); o que depende de runtime é Suposição até o smoke test. Decisão material (difícil de reverter ou que muda quem pode gastar) vira registro curto no plano; as demais cabem em três linhas.

Sumário: 1. Árvore: Apify ou outra rota · 2. Hospedado ou stdio · 3. OAuth ou token · 4. P2 ou P3 · 5. `call-actor` ou tool direta · 6. MCP ou CLI · 7. `claude mcp add` ou conector claude.ai · 8. Apify ou WebFetch · 9. Plugin oficial ou este · 10. Haiku ou Sonnet no pesquisador · 11. Sessão principal ou agente · 12. Hook opcional · 13. Quando não usar Apify

## 1. Árvore: Apify ou outra rota (V-22)

1. A fonte é GitHub, Hacker News, dev.to ou documentação estática? **Sim:** rota gratuita (`gh api`, Algolia, API do dev.to, WebFetch). Pare.
2. É um fato sobre o próprio Apify, a API ou o Crawlee? **Sim:** `consultar-docs-apify` (grátis). Pare.
3. O WebFetch ou o WebSearch resolvem? **Sim:** use-os e cite a URL lida. Pare.
4. Falharam por bloqueio, JavaScript obrigatório ou ausência de API (Reddit, X, transcrição de YouTube, SERP estruturada, crawl de documentação com JavaScript)? **Sim:** Apify, com orçamento aprovado.
5. Há orçamento em dólares aprovado e as tools da Apify na sessão? **Não:** fallback gratuito com a lacuna declarada, e ofereça `conectar-apify`.

## 2. Hospedado ou stdio (V-01)

| | Hospedado (`https://mcp.apify.com`) | stdio (`npx @apify/actors-mcp-server`) |
| --- | --- | --- |
| Quando | Padrão do plugin (R-A, R-B) | Último recurso (R-F) |
| Prós | Sem Node local; OAuth; manutenção da Apify | Código auditável no pacote; funciona sem rede para o servidor |
| Contras | Código privado; muda a cada release; sem hash de definições | Node ≥ 22; `APIFY_TOKEN` no ambiente; lê `~/.apify/auth.json` sem avisar; `cmd /c` no Windows; cadeia de suprimentos npm |
| Mitigação | Registrar `serverInfo.version`; reconferir `tools/list` por release | Fixar a versão do pacote |

Recomendação: hospedado. Mude para stdio só se houver exigência de rede ou de auditoria do código, e com versão fixada.

## 3. OAuth ou token (V-15, V-16, V-29)

| | OAuth (R-A) | Token em variável de ambiente (R-C) |
| --- | --- | --- |
| Quando | Uso interativo | Headless, SSH, CI |
| Prós | Nada de segredo em arquivo; login do usuário | Funciona sem navegador |
| Contras | Precisa de navegador | Header manual **desliga** o fallback OAuth; expansão de `${APIFY_MCP_TOKEN}` não testada (H-09); escopo no `mcp.apify.com` não testado (H-10) |
| Regra | O assistente nunca pede token | Token **com escopo e expiração curta** (Inferido) em variável de nome próprio |

## 4. P2 ou P3 (V-04)

P2 (`?tools=actors,docs`) tem `call-actor`, o único caminho com teto em dólares. P3 (tools de Actor diretas) é mais curto de chamar, mas sem `callOptions`: sem teto e sem `timeout`. Escolha P3 só para consulta sem orçamento sensível e com humano supervisionando; **para pesquisa com orçamento, P2**. Medição que mudaria a escolha: se a tool direta passar a aceitar `callOptions` (conferir `tools/list` por release).

## 5. `call-actor` ou tool direta (V-04, V-05)

`call-actor` aceita `callOptions` (`maxTotalChargeUsd`, `timeout`, `memory`) e `waitSecs`. A tool direta chama `start(input, { memory })` e nada mais. Se o perfil só tem tools diretas, avise "sem teto em dólares" antes de qualquer chamada e prefira trocar para P2.

## 6. MCP ou CLI do Apify

| | MCP (P2) | CLI (`apify actors call/start`) |
| --- | --- | --- |
| Teto em dólares | `callOptions.maxTotalChargeUsd` (PPE) | **Sem flag de teto** (referência da CLI lida) |
| Credencial | OAuth ou variável de ambiente | `apify login --token TOKEN` (token na linha de comando) |
| Controle humano | `ask` do Claude Code | Prompt do Bash (aprovação por comando) |
| Quando | Pesquisa com orçamento | Se o usuário preferir rodar por conta própria (fallback); avise que não há teto |

## 7. `claude mcp add` ou conector do claude.ai (V-17)

Conector (R-D): vale também no claude.ai e aparece no Claude Code só com login de assinatura; conectores custom não são verificados pela Anthropic e podem trazer instruções ocultas; o nome das tools muda (`mcp__claude_ai_...`) e o `apify-researcher` (que lista `mcp__apify__...`) **não o enxerga**. `claude mcp add` (R-A) dá prefixo previsível e escopo explícito. **Não use os dois.** Se o usuário já tem o conector, use as tools dele pela sessão principal e peça para o orquestrador repassar o prefixo no prompt de delegação.

## 8. Apify ou WebFetch (V-08, V-21, V-22)

WebFetch é gratuito e basta para páginas estáticas e documentação. O Apify entra quando o WebFetch é bloqueado (reddit.com), exige JavaScript ou precisa de dados estruturados (SERP, transcrição, X). Para uma URL única bloqueada: tente WebFetch; só então `apify/web-fetch` (`url`, `formats`), sem credenciais em `headers`. O `apify/web-fetch` "bypasses anti-bot protection": o contorno exige decisão caso a caso do usuário (V-32).

## 9. Plugin oficial da Apify ou este plugin (V-18)

| | Oficial (`apify/apify-claude-code-plugin`) | `web-research-apify` |
| --- | --- | --- |
| Foco | Desenvolver, publicar e "actorizar" Actors | Usar o Apify como fonte de pesquisa |
| MCP | Ativo, sem `tools=` | Nenhum registrado; conexão por receita, com `tools=` fixo |
| Agente | Com `Bash`; CLI sem teto | Allowlist de `tools`; sem `Bash` |
| Custo | Confirmação só acima de US$ 20 estimados | Orçamento em dólares aprovado no chat; teto em `callOptions` |

Para pesquisa, este plugin e o MCP direto. Para desenvolver Actors, o oficial, sabendo dos riscos. **Não instale os dois juntos.**

## 10. Haiku ou Sonnet no pesquisador

- **Haiku** (padrão do `apify-researcher`): executa um **plano fechado** (Actor, `input` e `callOptions` em JSON); barato; alinhado ao método de pesquisa (coleta barata, validador mais forte).
- **Sonnet:** quando a delegação traz só a lista de Actors (o agente precisa decidir), quando o orçamento passa de US$ 1 ou quando o alvo é sensível.
- Em qualquer caso o agente não escolhe Actor fora do plano nem amplia o teto. O risco maior não é o modelo, é o agente herdar ferramentas demais (por isso a allowlist).

## 11. Sessão principal ou agente (V-26, V-28)

A coleta pode rodar na sessão principal (o `playbook` cobre) ou no `apify-researcher`. O agente isola o conteúdo bruto (quarentena) e devolve resumo; a sessão principal mantém o usuário no loop do `ask`. Se o agente não enxergar as tools (conector com outro nome, subagente que não herda ferramentas adiadas: H-02b), ele cai no modo gratuito e avisa; a coleta é então feita na sessão principal. `ask` em execução não interativa não é respondível (H-08).

## 12. Hook opcional (Suposição; não incluído)

Hook `PreToolUse` que nega `call-actor` sem `maxTotalChargeUsd` ou acima do orçamento: trava mecânica útil, porém código executável e **não testado**. O plugin não o traz. Se o usuário quiser, `/automation-integrations:writing-hook-guardrails`, em ambiente descartável. Hook é guardrail, não fronteira de segurança; o limite da conta continua sendo a última trava.

## 13. Quando não usar Apify

- Existe rota gratuita que resolve (seção 1).
- Não há orçamento em dólares aprovado (use só leitura gratuita).
- O alvo envolve pessoas físicas, contatos ou leads (fora do fluxo padrão).
- A necessidade é monitoramento recorrente (agendamento: `/automation-integrations:scheduling-headless-jobs`).
- É scraper com código próprio ou página estática (`/automation-integrations:responsible-scraping`).
- O Apify é desejado para desenvolver Actors (plugin oficial).
