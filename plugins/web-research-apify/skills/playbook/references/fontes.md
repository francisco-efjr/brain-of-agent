# Fontes e bibliografia — Pesquisa web com o Apify MCP

Consulta: 2026-10-13 (leitura pelo validador; a página de Billing foi lida pelo crítico em 2026-10-14). Todas as páginas e repositórios abaixo foram lidos por pesquisadores e reconferidos por um validador (modelos Claude de portes diferentes: a independência é parcial, pois todos são da família Claude). **Nada foi executado em runtime**: nenhum token, conta, instalação, `claude mcp add` nem Actor. Toda recomendação do plugin cita um item `V-xx` desta lista ou é marcada como Inferido.

Sumário: 1. Como ler · 2. Top 15 · 3. Demais fontes lidas · 4. Rejeitadas · 5. Índice V-01 a V-34 · 6. Créditos e licenças · 7. Onde conferir versões e preços

## 1. Como ler

- **Classe A**: documentação oficial, norma ou mantenedor do produto. **B**: autor ou empresa reconhecida, ou repositório com uso comprovado. **C**: só descoberta. A pontuação entre parênteses segue a rubrica de fonte da casa.
- **Licença** é a observada pelo validador. Para páginas de documentação a licença **não foi verificada**: o plugin só **destila** (redação própria) e cita a URL. Código do `apify-mcp-server` (MIT) permitiria trechos curtos com atribuição; o plugin não copia código.
- **Volátil** = preço, Actor, versão ou lista de tools: confirme no dia.
- Estrelas, contagem de usuários e datas são de 2026-10-13 e servem de sinal, nunca de prova de qualidade.

## 2. Top 15 (ordenadas por utilidade vezes autoridade)

| # | Fonte | URL | Classe | Licença | Por que importa | Itens |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `apify/apify-mcp-server` (README, `src/`, package.json, CHANGELOG, `evals/README.md`); ★ 11 019, v0.18.0 de 2026-10-13, commit `9ad785a6aa` | https://github.com/apify/apify-mcp-server | A (10) | MIT | Fonte de verdade de tools, `tools=`, auto-injeção, `callOptions`, telemetria; evals como modelo | V-01 a V-06, V-10, V-11, V-13, V-14 |
| 2 | Apify docs: integração MCP | https://docs.apify.com/platform/integrations/mcp | A (9) | não verificada (destilar) | Conexão, `tools`, limite de 30 req/s; ressalva: Node ≥ 18 e `report-problem` desatualizados | V-01, V-02, V-05 |
| 3 | Claude Code docs: MCP | https://code.claude.com/docs/en/mcp | A | termos do site (destilar) | `claude mcp add`, escopos, expansão de env, limites de saída e timeouts, conectores claude.ai, nomes de tool, tool search | V-06, V-15 a V-17, V-34 |
| 4 | Claude Code docs: permissions e settings-reference | https://code.claude.com/docs/en/permissions | A (9) | termos do site (destilar) | `deny`, `ask`, `allow`; sintaxe `mcp__servidor__tool` | V-19 |
| 5 | Apify docs: pay-per-event e API Run Actor | https://docs.apify.com/platform/actors/publishing/monetize/pay-per-event · https://docs.apify.com/api/v2/act-runs-post | A (10) | não verificada (destilar) | Teto PPE (`Actor.charge`, aborto), `maxTotalChargeUsd` | V-05 |
| 6 | API pública da Store: `https://api.apify.com/v2/acts/<owner>~<name>` e `/builds/default` | https://api.apify.com/v2/acts/apify~web-fetch | A (9), **volátil** | dado público | Preços por evento, schemas e dono reais | V-20, V-21, V-24 |
| 7 | Issues do `apify-mcp-server` (#1429, #1403, #1559, #1558, #1524, #1446, #1401) | https://github.com/apify/apify-mcp-server/issues | A (9) | MIT (repo) | Limitações vivas: custo invisível, `maxItems` legado, `nextStep` que pede re-run | V-33 |
| 8 | `apify/apify-claude-code-plugin` v1.0.2 | https://github.com/apify/apify-claude-code-plugin | A/B (8) | Apache-2.0 | Decisão de coexistência: MCP ativo, `Bash`, CLI sem teto | V-18 |
| 9 | OWASP LLM01:2025 Prompt Injection | https://genai.owasp.org/llmrisk/llm01-prompt-injection/ | A (9) | não verificada (destilar) | 7 mitigações aplicadas a dataset, README, `nextStep` e `TIP` | V-26 |
| 10 | Simon Willison, "The lethal trifecta" (2025-06-16) | https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ | B (7) | blog (destilar) | Modelo de risco: dados privados, conteúdo não confiável, saída externa | V-28 |
| 11 | Invariant Labs (tool poisoning), OWASP MCP03, exploit roundup Q3-2026 | https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks · https://genai.owasp.org/2026/10/08/genai-and-agentic-ai-exploit-roundup-q3-2026/ | A/B (8) | não verificada (destilar) | Tool poisoning, rug pull, caso Deadbugz | V-27 |
| 12 | Apify docs: tokens (integrations/api, agent-onboarding) | https://docs.apify.com/platform/integrations/api · https://docs.apify.com/get-started/agent-onboarding | A (9) | não verificada (destilar) | Tipos de token, escopo, expiração, rotação (24 h), `Authorization` | V-29 |
| 13 | Apify docs: permissões de Actor, AUP, privacidade, apagar dataset, CLI | https://docs.apify.com/platform/actors/running/permissions · https://docs.apify.com/legal/acceptable-use-policy · https://docs.apify.com/api/v2/dataset-delete | A (9) / B (6) | não verificada (destilar) | Permissão limitada versus total, retenção, exclusão, AUP | V-30 a V-32 |
| 14 | Claude: conectores custom (Suporte) | https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp | A (9) | termos do site (destilar) | Receita R-D; aviso de conectores não verificados | V-17 |
| 15 | Apify: preços | https://apify.com/pricing | B (6), volátil | n/a | Plano Free (US$ 5 por mês de uso), CU por plano | V-23 |

## 3. Demais fontes lidas (2026-10-13)

- `github.com/apify/apify-mcp-server` (commit `9ad785a6aa`; releases; CHANGELOG; `server.json`; `Dockerfile`; `AGENTS.md`; `SECURITY.md`; `DEVELOPMENT.md`).
- Apify docs: `docs.apify.com/integrations/claude-code-cli`, `docs.apify.com/integrations/claude-desktop.md`, `docs.apify.com/platform/actors/development/quick-start/build-with-ai`, `docs.apify.com/platform/storage/dataset`, `docs.apify.com/legal/privacy-policy`, `docs.apify.com/cli/docs/reference`, `apify.com/apify/website-content-crawler`, e (lida pelo crítico em 2026-10-14) `docs.apify.com/platform/console/billing`.
- Claude Code: `code.claude.com/docs/en/{mcp,permissions,settings-reference,security,discover-plugins}`.
- Modelo de segurança do MCP: `modelcontextprotocol.io` (security best practices); `github.com/anthropics/claude-code/issues/9594` e `/20061` (Windows `cmd /c`).
- Rotas gratuitas: `hn.algolia.com/api/v1/search`, `dev.to/api/articles`, `gh api`.
- Issue `apify-mcp-server` #166 (excesso de tools; **fechada**) para V-34.
- RFC 9309 (Robots Exclusion Protocol) e LGPD art. 5º I (por resultado de busca; o acesso direto ao Planalto falhou).

## 4. Rejeitadas como fonte ou como regra

| Item | Motivo |
| --- | --- |
| `use-apify.com`, `anythingmcp.com`, `lagrowthmachine.com` | Terceiros promocionais ou wrappers |
| Threads de preço de Discord e Trustpilot (custos de US$ 46 e 456) | Relatos unilaterais, lidos só por snippet; não verificáveis |
| Blogs com "96 a 99% menos tokens" | Título de post, não evidência |
| Blog sobre conectores MCP de Actors | Sentido inverso (Actors acessando apps); irrelevante para pesquisa |
| Viés do servidor ("prefer Actors with higher usage", "assume scraping is appropriate") | Rejeitado como **regra**: conflita com checagem de finalidade, termos e dados pessoais |
| `?token=` na URL | Rejeitado como recomendação: existe só no servidor de desenvolvimento local |
| Actors como tools diretas como controle de custo | Rebaixado: sem `callOptions` |

## 5. Índice V-01 a V-34

| Item | Tema | Fonte principal | Classe |
| --- | --- | --- | --- |
| V-01 | Servidor hospedado, stdio, versões e requisitos | README, package.json, server.json, docs integração MCP | A |
| V-02 | Parâmetros de URL, `tools=` e conjunto padrão | README, `src/dev_server.ts`, docs | A |
| V-03 | Auto-injeção, tools sem categoria, nomes aposentados | `tools_loader.ts`, `registry.ts`, `const.ts`, CHANGELOG | A |
| V-04 | Perfis P0 a P3 (derivado; a recomendação é Inferida) | Código e `tool_dispatch.ts` | A (fatos) |
| V-05 | Executar Actors e controlar gasto | `call_actor.ts`, docs MCP, agent-onboarding, PPE, act-runs-post | A |
| V-06 | Ler resultados, paginação e limites | `src/tools/storage/*`, docs do Claude Code | A |
| V-07 | Descoberta de Actors | `search_actors.ts`, `fetch_actor_details.ts` | A |
| V-08 | Roteamento de fontes e prompt de pesquisa | `server-instructions/index.ts` | A/B |
| V-09 | Docs Apify e Crawlee como fonte | `src/tools/docs/*` | A |
| V-10 | Resources MCP, API genérica, operações de conta (fora do escopo) | README, `src/tools/api/*` | A |
| V-11 | Telemetria e `report-problem` | README, `const.ts`, `telemetry.ts` | A |
| V-12 | Pagamento agêntico (AGI, x402, Skyfire) | README, `payments/const.ts` | A/B |
| V-13 | Velocidade de mudança e nomes obsoletos | CHANGELOG, package.json | A |
| V-14 | Evals do repositório como modelo | `evals/README.md` | A |
| V-15 | Receita OAuth | Docs Claude Code e Apify | A |
| V-16 | Receita token por variável de ambiente | Docs Claude Code, `DEVELOPMENT.md` | A com ressalvas |
| V-17 | Conector claude.ai e conectores no Claude Code | Suporte da Anthropic, docs Claude Code | A |
| V-18 | Plugin oficial da Apify | Repositório `apify/apify-claude-code-plugin` | A/B |
| V-19 | Permissões do Claude Code | Docs permissions e settings | A |
| V-20 | Actors de base: `rag-web-browser`, `web-fetch`, SERP, crawler | API pública da Store | A, volátil |
| V-21 | Actors sociais: Reddit, YouTube, X | API pública da Store | B |
| V-22 | Quando não usar Apify | HN Algolia, `gh api`, dev.to | A/B |
| V-23 | Planos e créditos | apify.com/pricing | B, volátil |
| V-24 | Orçamento e checklist de custo | Derivado | A |
| V-25 | Citação, proveniência e reverificação | Derivado (rubricas da casa) | A |
| V-26 | Injeção e texto dirigido à IA | OWASP LLM01, docs Claude Code, issue #1559 | A |
| V-27 | Tool poisoning, rug pull, cadeia de suprimentos | Invariant, OWASP MCP03, roundup Q3-2026 | A/B |
| V-28 | "Lethal trifecta" com Apify | Simon Willison | B |
| V-29 | Tokens: tipos, escopo, expiração, rotação | Docs Apify | A |
| V-30 | Permissões de Actor e Actors de terceiros | Docs Apify, `const.ts`, issue #1446 | A |
| V-31 | Retenção, exclusão e privacidade | Docs Apify | A |
| V-32 | Legal e dados pessoais | AUP, RFC 9309, LGPD (busca) | B |
| V-33 | Issues abertas de 2026 | Issues do repositório | A |
| V-34 | Excesso de tools e economia de contexto | Issue #166 (fechada), docs Claude Code | B |

O arquivo de origem (`VALIDATED.md`) e a síntese ficam na fábrica `dev-segments`, em `docs/research/web-research-apify/`; este índice basta para localizar a fonte primária de cada afirmação.

## 6. Créditos e licenças

| Projeto | Licença | Uso neste plugin |
| --- | --- | --- |
| `apify/apify-mcp-server` | MIT | Só fonte de leitura; nenhum código copiado |
| `apify/apify-claude-code-plugin` | Apache-2.0 | Só fonte de leitura e decisão de coexistência; nenhum código copiado |
| Documentação da Apify, do Claude Code e da Anthropic | Licença não verificada | Destilada com redação própria, com URL |
| OWASP, Invariant Labs, Simon Willison | Textos de terceiros | Destilados com redação própria, com URL |

**Não afiliado à Apify.** Apify e Actors são marcas e produtos de terceiros. O plugin não redistribui conteúdo nem binário da Apify.

## 7. Onde conferir versões e preços

- Versão do servidor: releases e `package.json` em https://github.com/apify/apify-mcp-server (cite "release" e "em desenvolvimento" separadamente, como 0.18.0 e 0.18.1).
- Lista de tools: o `tools/list` real da sua conexão (`catalogo-de-tools.md`, seção 9).
- Preço e schema de um Actor: `fetch-actor-details` no dia, ou GET público `https://api.apify.com/v2/acts/<owner>~<name>`.
- Planos: https://apify.com/pricing. Limite da conta: Console › Billing › Limits.
- Claude Code: `claude --version` e https://code.claude.com/docs.
