# Fontes (bibliografia validada)

Todas as URLs abaixo foram abertas pelo validador do segmento em **2026-10-10** (coluna "Consulta"), com leitura via resumo de modelo pequeno e perguntas dirigidas; este plugin não reabriu cada página, exceto `https://code.claude.com/docs/en/hooks-guide`, relida em 2026-10-10 para `ferramentas-e-mcp.md`. Classe A = documentação oficial ou norma; B = autor ou projeto reconhecido; C = sinal de prática. O número entre parênteses é a pontuação 0 a 10 da rubrica de fontes. "Licença" descreve a licença **identificada**; sem licença identificada, o plugin só destila (redação própria) e cita a URL. Nenhum trecho literal de terceiros foi copiado; o único texto reaproveitado quase literalmente é o do brain-of-agent (conteúdo próprio do usuário, MIT), com atribuição.

## Sumário

- [Como ler e como citar](#como-ler-e-como-citar)
- [Classe A](#classe-a)
- [Classe B](#classe-b)
- [Classe C](#classe-c)
- [Conteúdo próprio e workflows de terceiros](#conteúdo-próprio-e-workflows-de-terceiros)
- [Fatos que vêm do brain e não foram reverificados](#fatos-que-vêm-do-brain-e-não-foram-reverificados)
- [Rejeitados e rebaixados](#rejeitados-e-rebaixados)
- [Lacunas conhecidas](#lacunas-conhecidas)

## Como ler e como citar

- `V-nn` aponta para o item correspondente do consolidado de pesquisa deste segmento; cite-o ao justificar uma recomendação.
- Versões, flags, IDs de modelo e tabelas de compatibilidade mudam. Confirme na versão instalada (`<ferramenta> --version`, `--help`) e na página oficial antes de copiar um comando ou número.
- Números de blogs e relatos (percentuais, contagens) são convenções dos autores; se citar, inclua a fonte e a ressalva.
- Estrelas e forks vêm do HTML das páginas em 2026-10-10; **a data do último commit não foi observada para nenhum repositório** (API do GitHub indisponível). Estrela não prova qualidade.
- Revisões feitas por modelos da família Claude têm independência parcial: não equivalem a validação externa.

## Classe A

| Item | Título | URL | Licença | Consulta | Uso no plugin |
| --- | --- | --- | --- | --- | --- |
| V-01 (9) | Writing tools for agents (Anthropic Engineering, 11/09/2025) | https://www.anthropic.com/engineering/writing-tools-for-agents | não declarada; destilado | 2026-10-10 | `agent-tool-design`, `agentes-e-llm.md`; limite de 25.000 tokens vale por padrão só no Claude Code |
| V-02 (9) | Define tools (documentação da Claude API) | https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools | doc oficial; destilado | 2026-10-10 | Descrição em 4 frases, `input_examples`, regra de `tool_choice` por modelo (tabela muda) |
| V-03 (9) | Strict tool use | https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use | doc oficial; destilado | 2026-10-10 | `strict: true` em tools que mutam; subconjunto de schema não lido |
| V-04 (9) | Claude Code best practices | https://code.claude.com/docs/en/best-practices | doc oficial; destilado | 2026-10-10 | Verificação executável, plano, CLAUDE.md curto, revisor em contexto limpo, hooks |
| V-05 (9) | Sub-agents (Claude Code) | https://code.claude.com/docs/en/sub-agents | doc oficial; destilado | 2026-10-10 | Formato de agente; `permissionMode` ignorado em subagentes de plugin |
| V-06 (8) | anthropics/skills: mcp-builder | https://raw.githubusercontent.com/anthropics/skills/main/skills/mcp-builder/SKILL.md | Apache-2.0 (LICENSE.txt da skill); destilado | 2026-10-10 | 4 fases, anotações MCP, avaliação de 10 perguntas |
| V-07 (8) | anthropics/skills: claude-api | https://raw.githubusercontent.com/anthropics/skills/main/skills/claude-api/SKILL.md | repositório sem licença única; LICENSE desta skill não lido; destilado | 2026-10-10 | Checklist de endpoint que chama a API do modelo |
| V-08 (8) | claude-code-security-review | https://github.com/anthropics/claude-code-security-review | MIT | 2026-10-10 | Revisão só do diff, exclusões de falso positivo, aviso de que não é endurecida contra injeção |
| V-09 (8) | OWASP API Security Top 10 (2023) | https://api-security.owasp.org/editions/2023/en/0x11-t10 | não verificada; destilado | 2026-10-10 | Grade API1 a API10; textos de prevenção não lidos em detalhe |
| V-10 (8) | OWASP REST Security Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html | não verificada; destilado | 2026-10-10 | Hardening por tópico (JWT, API key, validação, headers, CORS, erros) |
| V-11 (8) | OpenAPI Specification 3.1.1 (24/10/2024) | https://spec.openapis.org/oas/v3.1.1 | Apache-2.0 | 2026-10-10 | Campos obrigatórios, semântica de `security`; existem 3.2.0 e 3.2.1; ~60% do texto não lido |
| V-12 (9) | RFC 9700: OAuth 2.0 Security BCP (jan/2025) | https://datatracker.ietf.org/doc/html/rfc9700 | IETF; destilado | 2026-10-10 | PKCE, redirect exato, implicit SHOULD NOT, password MUST NOT; ~35% não lido |
| V-13 (9) | RFC 8725: JWT BCP (2020) | https://www.rfc-editor.org/rfc/rfc8725 | IETF; destilado | 2026-10-10 | Algoritmo fixo, `none`, `iss`/`aud`, `kid`, `jku`; não trata `exp`/`nbf` |
| V-14 (9) | RFC 9457: Problem Details for HTTP APIs | https://www.rfc-editor.org/rfc/rfc9457.html | IETF; destilado | 2026-10-10 | Contrato de erro; obsoleta a RFC 7807 |
| V-15 (8) | Idempotência: Stripe e Google AIP-155 | https://docs.stripe.com/api/idempotent_requests · https://google.aip.dev/155 | Stripe: destilar apenas; AIP: não verificada | 2026-10-10 | Semântica de chave, replay, conflito, retenção; Stripe v1 e v2 diferem |
| V-17 (8) | gRPC: status codes | https://grpc.io/docs/guides/status-codes/ | não declarada; destilado | 2026-10-10 | 17 códigos, quais só a aplicação gera, política de retry; sem mapeamento HTTP na página |
| V-34 (8) | Google AIP-158: Pagination | https://google.aip.dev/158 | não verificada; destilado | 2026-10-10 | `page_size`/`page_token` opaco, fim por token vazio, paginar desde o início |
| V-35 (8) | Azure REST API Guidelines (`azure/Guidelines.md`, branch vNext) | https://raw.githubusercontent.com/microsoft/api-guidelines/vNext/azure/Guidelines.md | CC BY 4.0 (atribuição: Microsoft); destilado | 2026-10-10 | Versionamento, `nextLink`, operações longas, repetibilidade, ETag, erro. O `Guidelines.md` da raiz está depreciado |
| V-36 (9) | RFC 9111: HTTP Caching (2022) | https://www.rfc-editor.org/rfc/rfc9111 | IETF; destilado | 2026-10-10 | `Cache-Control`, revalidação, invalidação; só o resumo de seções foi conferido |

## Classe B

| Item | Título | URL | Licença | Consulta | Uso no plugin |
| --- | --- | --- | --- | --- | --- |
| V-16 (5) | Idempotency-Key HTTP header (draft-07, **expirado em 18/04/2026**, não é RFC) | https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-idempotency-key-header | draft IETF; destilado | 2026-10-10 | Códigos 400/422/409 como opção de política, nunca como padrão publicado |
| V-18 (7) | Go: routing enhancements (13/02/2024) e go.instructions | https://go.dev/blog/routing-enhancements · https://raw.githubusercontent.com/github/awesome-copilot/main/instructions/go.instructions.md | blog: não verificada; instructions: MIT | 2026-10-10 | `stack-go.md`: padrões com método, `PathValue`, erros, timeouts |
| V-19 (7) | NestJS: Guards | https://docs.nestjs.com/guards | licença do texto não verificada; destilado | 2026-10-10 | RBAC com `CanActivate`, `APP_GUARD`, ordem de execução |
| V-20 (7) | Spring Security: resource server com JWT (série 7.1.1) | https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html | não verificada; destilado | 2026-10-10 | `issuer-uri`, RS256 padrão, `aud` não validado por padrão, `SCOPE_*` |
| V-21 (6) | FastAPI: security first steps e response model | https://fastapi.tiangolo.com/tutorial/security/first-steps/ · https://fastapi.tiangolo.com/tutorial/response-model/ | não verificada; destilado | 2026-10-10 | O tutorial de segurança não valida o token; DTOs In/Out separados |
| V-22 (6) | ASP.NET Core error handling (.NET 10) e aspnet-rest-apis | https://learn.microsoft.com/en-us/aspnet/core/fundamentals/error-handling · https://raw.githubusercontent.com/github/awesome-copilot/main/instructions/aspnet-rest-apis.instructions.md | doc: não verificada; instructions: MIT | 2026-10-10 | `IExceptionHandler`, `AddProblemDetails()`; a doc cita RFC 7807 |
| V-23 (6) | FastAPI production architecture (awesome-cursorrules) | https://raw.githubusercontent.com/PatrickJS/awesome-cursorrules/main/rules/fastapi-production-architecture-cursorrules-prompt-file.mdc | CC0-1.0 | 2026-10-10 | Camadas verificáveis por grep; limites de linhas (opinião) ficam de fora |
| V-24 (6) | awesome-copilot: security-and-owasp e code-review-generic | https://raw.githubusercontent.com/github/awesome-copilot/main/instructions/security-and-owasp.instructions.md · https://raw.githubusercontent.com/github/awesome-copilot/main/instructions/code-review-generic.instructions.md | MIT | 2026-10-10 | Molde de achado e severidades; webhook sem assinatura = CRITICAL (AP4) |
| V-25 (6) | Depuração em 4 fases (obra/superpowers) e debugger (wshobson) | https://raw.githubusercontent.com/obra/superpowers/main/skills/systematic-debugging/SKILL.md · https://raw.githubusercontent.com/wshobson/agents/main/plugins/debugging-toolkit/agents/debugger.md | MIT (ambos) | 2026-10-10 | Causa raiz antes de corrigir; parar após 3 falhas (convenção); reescrito sem CAPS |
| V-26 (5) | backend-architect (wshobson) | https://raw.githubusercontent.com/wshobson/agents/main/plugins/backend-development/agents/backend-architect.md | MIT | 2026-10-10 | Checklist de entregáveis e fronteiras de delegação; original sem `tools` |
| V-29 (6) | fastapi-patterns (everything-claude-code) | https://raw.githubusercontent.com/affaan-m/everything-claude-code/main/skills/fastapi-patterns/SKILL.md | MIT | 2026-10-10 | Estrutura, testes com `httpx.AsyncClient`, restrição única; usa libs de auth pouco mantidas |
| V-30 (5) | graphql-schema (apollographql/skills, v1.0.2) | https://raw.githubusercontent.com/apollographql/skills/main/skills/graphql-schema/SKILL.md | MIT | 2026-10-10 | Nulabilidade, conexão, `input` único, depreciar antes de remover; só schema |
| V-32 (6) | Prompt de documentação de API (GitHub Docs) | https://docs.github.com/en/copilot/tutorials/customization-library/prompt-files/document-api | não verificada; reescrito | 2026-10-10 | Base do PR-05 (OpenAPI 3.1 + validador como critério de saída) |
| V-33 (6) | IETF ratelimit-headers (rev. 11, 23/05/2026, expira 24/11/2026) e guia de rate limiting | https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-ratelimit-headers · https://claudecode-lab.com/en/blog/claude-code-rate-limiting/ | draft IETF; blog classe C | 2026-10-10 | `RateLimit`/`RateLimit-Policy` (draft), 429, chave de credencial validada; o demo do blog usa `x-api-key` não validado |
| V-39 (6) | Checklist de confiança para regras de terceiros (HN e Mozilla cq) | https://news.ycombinator.com/item?id=47491466 · https://blog.mozilla.ai/cq-stack-overflow-for-agents/ | discussão; destilado | 2026-10-10 | Aceitar regra/prompt de terceiros (PR-32); leitura via resumo |

## Classe C

| Item | Título | URL | Licença | Consulta | Uso no plugin |
| --- | --- | --- | --- | --- | --- |
| V-27 (4) | Baseline DevSecOps (awesome-cursorrules) | https://raw.githubusercontent.com/PatrickJS/awesome-cursorrules/main/rules/security-devsecops-ssdls-appsec.mdc | CC0 | 2026-10-10 | Argon2 ou bcrypt, sem auth própria, sem segredo em log (SN-19), corroborado por V-10 |
| V-28 (4) | Agentic coding: scripts e ferramentas para agentes (Armin Ronacher, 12/06/2025) | https://lucumr.pocoo.org/2025/6/12/agentic-coding/ | não declarada; destilado | 2026-10-10 | Scripts com timeout, saída curta, erro que orienta; opinião de autor, sem métrica |
| V-31 (4) | Prompt de idempotência (mejba.me, abril/2026) | https://www.mejba.me/prompts/api-idempotency-keys-design-implementation | não declarada; **reescrito** (nota original 70, reescrito 84) | 2026-10-10 | PR-04; códigos 422/409 vêm do draft expirado: decisão do projeto |
| V-37 (3) | claude-md-templates (abhishekray07) | https://github.com/abhishekray07/claude-md-templates | MIT | 2026-10-10 | Bloco de CLAUDE.md e laço "proponha uma linha"; eficácia alegada sem medição, corroborado por V-04 |
| V-38 (3) | Claude Code para times Django/FastAPI (First AI Movers, 15/04/2026) | https://radar.firstaimovers.com/claude-code-backend-teams-python-django-fastapi-2026.md | não declarada; destilado | 2026-10-10 | Política de migração (agente propõe, humano executa); números de produtividade descartados |

## Conteúdo próprio e workflows de terceiros

| Origem | Licença | Onde entra |
| --- | --- | --- |
| `francisco-efjr/brain-of-agent`, commit 0d025fb (snapshot de 09/10/2026): `brains/fullstack/references/backend-e-contratos.md`, `brains/qa/references/automacao-api.md`, `brains/fullstack/SKILL.md`, `brains/fullstack/references/protocolo-completo.md`, `seguranca-e-privacidade.md`, `dados-e-migracoes.md` e `testes-e-debugging.md` da mesma pasta (caminhos do repositório brain-of-agent, não do plugin) e templates `adr`, `plano-incremento`, `handoff-checkpoint`, `checklist-fullstack-completo` | MIT (conteúdo próprio do usuário) | Checklists por endpoint e de serviço, tabela de status HTTP, tabelas de teste de contrato, webhooks, mensageria, templates de `assets/templates/`; adaptados ao formato de plugin |
| gstack `/review` (garrytan/gstack, `vendor/gstack`) | MIT | Apenas o formato de achado `[CRITICAL\|INFORMATIONAL] (confidence: N/10) arquivo:linha — descrição`; nenhum bloco copiado; o comportamento do original (consulta a serviço externo, auto-escolha, Edit/Write) não foi importado |
| Fontes consultadas pelo brain em 2026-10-09 e não reabertas aqui: MDN HTTP request methods (`https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Methods`), OpenAPI "latest" (`https://spec.openapis.org/oas/latest.html`), OWASP ASVS (`https://owasp.org/www-project-application-security-verification-standard/`), PostgreSQL transaction isolation e ALTER TABLE (`https://www.postgresql.org/docs/current/transaction-iso.html`, `https://www.postgresql.org/docs/current/sql-altertable.html`), Playwright best practices (`https://playwright.dev/docs/best-practices`) | docs de produto; destilado | Contexto de dados e de teste; tratar como Inferido até reconferir |

## Fatos que vêm do brain

Reverificados em 2026-10-10 pelo validador de qualidade (agora **Verificado**): Dredd arquivado em 08/11/2024 (https://github.com/apiaryio/dredd); RFC 9745 `Deprecation`, Standards Track, março/2025, valor `@<epoch>` e relação de link `deprecation` (https://www.rfc-editor.org/rfc/rfc9745.html); RFC 8594 `Sunset`, Informational, maio/2019, valor HTTP-date (https://www.rfc-editor.org/rfc/rfc8594.html); modo `BACKWARD` padrão do Confluent Schema Registry (https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html); tabela de `tool_choice` por modelo de V-02 reconferida na mesma data.

Seguem **Inferido**: limite de 4 MB por mensagem em gRPC (varia por implementação); janela de deduplicação de 5 minutos do SQS FIFO; equivalências gRPC para HTTP (a página oficial não traz mapeamento). Confirme na fonte antes de afirmar como fato em uma entrega.

## Rejeitados e rebaixados

| Item | Decisão | Motivo |
| --- | --- | --- |
| NestJS anti-hallucination (awesome-cursorrules) | Rejeitado | Contém "OVERRIDE all other generation behavior"; imports banidos sem fonte. Só a ideia de checar o pacote com `npm ls` foi reescrita (SN-13) |
| VoltAgent api-designer / backend-developer | Rebaixado, não usado | `tools` amplas; "delivery package" com números fictícios que um agente copiaria como resultado |
| gstack `/review` | Só o formato de achado | Pode consultar serviço externo, escolhe opção sozinho, `allowed-tools` com Edit/Write |
| davila7 node-api CLAUDE.md, agent-os, CLAUDE.md "do tiangolo" via thepromptshelf, heyuan110 sobre CLAUDE.md, dev.to (prompt de API), lowcode/phosailabs | Rejeitados ou rebaixados | Atribuição não confirmada, números sem estudo, RFC 7807 obsoleta, persona genérica ou conteúdo não lido |
| Fowler, Richardson Maturity Model | Vocabulário (C) | Nível 3 (HATEOAS) não é teste de conformidade nem critério deste plugin |
| `nodebestpractices` | Não reproduzir | CC-BY-SA-4.0 (compartilha igual); só destilar a ideia, sem copiar |

## Lacunas conhecidas

O plugin cobre estes temas com conhecimento estável marcado **Inferido** ou os declara ausentes. Alvos de pesquisa posterior, URLs a confirmar:

1. Filas, jobs, outbox, retries com backoff e jitter (AWS Builders' Library, docs de Celery/BullMQ/Sidekiq, Azure Architecture Center, microservices.io).
2. Observabilidade: W3C Trace Context, convenções semânticas HTTP do OpenTelemetry, OWASP Logging Cheat Sheet.
3. Cache de aplicação (cache-aside, invalidação, stampede, Redis). Só HTTP caching (V-36) e ETag (V-35) têm fonte.
4. Webhooks como padrão (Standard Webhooks; assinaturas HMAC de Stripe e GitHub).
5. Rust (axum, tower, thiserror/anyhow), tRPC, Django REST Framework, Express/Fastify, Gin/Chi/Echo, Spring Boot (`ProblemDetail`, Bean Validation, Actuator), ASP.NET Minimal APIs.
6. Validação por biblioteca (Pydantic v2, Zod, Bean Validation) e OWASP Input Validation Cheat Sheet.
7. Teste de contrato e property-based: fontes oficiais de Pact e Schemathesis não lidas; só o brain.
8. Diff de contrato: oasdiff e Spectral por menção; regras de compatibilidade do Google (AIP-180 e vizinhas) a confirmar.
9. Autorização avançada (ABAC, ReBAC, RLS, OIDC Core), GraphQL operacional (DataLoader, autorização em resolvers).
10. Evidência de comunidade: apenas Hacker News foi lido; Reddit, X, YouTube e Medium não.
11. Hooks: um único exemplo oficial (arquivos protegidos) foi verificado; nenhum exemplo testado para migrações ou OpenAPI.
12. Página de boas práticas de skills da plataforma (`platform.claude.com`) não aberta: valide o formato das skills contra ela.

Validado em: 2026-10-10 · modelo-alvo: claude-sonnet-5-5 · reconfira versões (OpenAPI 3.1 x 3.2, Spring 7.x, Go 1.22+, drafts IETF, tabela de `tool_choice`) antes de publicar.
