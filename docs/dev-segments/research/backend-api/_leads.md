# backend-api — pistas do atlas global

Data: 2026-10-09 · Indexador do atlas (Claude Sonnet 5.5) · Origem: `docs/research/_global/*.validated.md` (IDs: AO, EC, CT, PC, CP, BR).
Pista é ponto de partida: reabrir a URL antes de citar. "Dest." = destilar. Princípios comuns: `docs/foundation/prompt-principles.md`.

## 1. Pistas aprovadas aplicáveis

| Pista | URL | Classe | O que aproveitar |
| --- | --- | --- | --- |
| FastAPI production architecture (CT-07) | https://github.com/PatrickJS/awesome-cursorrules | B | Router → Service → Repository → ORM; handler fino; `response_model=`; exceções de domínio no router; `idempotency_key` em efeitos; consultas escopadas por `user_id`. CC0; trechos literais Verificados. Limites 400/600 LOC são opinião. |
| NestJS anti-hallucination (CT-08) | https://github.com/PatrickJS/awesome-cursorrules | B | Tabela "import banido → substituto → desde qual versão"; "se não tem certeza de que o pacote existe, não importe"; `synchronize: true` nunca em produção. CC0; trocar o tom de "OVERRIDE" por calmo e acrescentar `npm ls`. |
| security-and-owasp.instructions.md (CT-16) | https://github.com/github/awesome-copilot | B | Molde `ID · severidade · detecção · OWASP · correção`; webhook com assinatura verificada; "Never trust LLM output as safe". MIT, ~1.000 linhas: virar `references/`. |
| github/awesome-copilot (CT-14) | https://github.com/github/awesome-copilot | A | Plugins `*-mcp-development`, `openapi-to-application-*` (nomes citados pelo atlas, conteúdo não lido). |
| Writing tools for agents + define tools (AO-17) | https://www.anthropic.com/engineering/writing-tools-for-agents | A | Consolidar operações, namespacing, erros acionáveis; vale para desenhar APIs consumidas por agentes. |
| Equipping agents with Agent Skills (AO-19) | https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills | A | Scripts fora do contexto; skill como guia de onboarding. |
| anthropics/skills `mcp-builder`, `claude-api` (AO-28) | https://github.com/anthropics/skills | A | 10 perguntas de eval independentes; referência de API Claude. Conferir LICENSE da skill. |
| claude-code-security-review (AO-24) | https://github.com/anthropics/claude-code-security-review | A | Foco só no que a PR introduz, confiança > 80%, saída JSON (file, line, severity, category, exploit_scenario). MIT; atribuição obrigatória; exclusões (rate limiting) podem não servir. |
| Armin Ronacher, agentic coding (CP-12) | https://lucumr.pocoo.org/2025/6/12/agentic-coding/ | B | Checklist de ferramenta pronta para agente: rápida, saída curta, erros acionáveis, idempotente, logs em caminho fixo, timeout; CLI antes de MCP. Não reverificado; ignora a regra da casa sobre `--dangerously-skip-permissions`. |
| Amplifying (CP-24) | https://amplifying.ai/research/claude-code-picks | B | Declarar stack, ORM e auth; evitar auth e cripto próprios. |
| Dwyer SPEC (CP-25) | https://www.dwyer.co.za/static/claude-code-is-all-you-need.html | B | SPEC curto com verificação e2e; falhas relatadas (deps de 500MB, DB derrubado). |
| agent-os (EC-17) | https://github.com/buildermethods/agent-os | B | Extrair standards do próprio codebase e injetá-los; detalhes Suposição. MIT. |
| wshobson/agents (EC-10) | https://github.com/wshobson/agents | B | Plugins por domínio; `debugging-toolkit/agents/debugger.md` (5 passos) sem `tools`: corrigir ao destilar. |
| superpowers debugging (EC-01) | https://github.com/obra/superpowers | A | Causa raiz antes de corrigir; parar após 3 correções. |
| gstack `/review` e `/investigate` (BR-16, BR-17) | https://github.com/garrytan/gstack | B | Achado com severidade, confiança, `arquivo:linha`, cenário; Iron Law de causa raiz. |

## 2. Repositórios e arquivos a abrir
- `PatrickJS/awesome-cursorrules/rules/`: `fastapi-production-architecture-cursorrules-prompt-file.mdc`, `nestjs-anti-hallucination-cursorrules-prompt-file.mdc`, `security-devsecops-ssdls-appsec.mdc`.
- `github/awesome-copilot/instructions/security-and-owasp.instructions.md`, `code-review-generic.instructions.md`.
- `anthropics/skills/mcp-builder`, `claude-api`.
- `buildermethods/agent-os` comandos `/discover-standards`, `/inject-standards`.
- Documentação oficial de FastAPI, NestJS, Spring, Go, .NET, OpenAPI, OAuth2/OIDC, gRPC não está no atlas: lente authoritative do segmento. Para Go, Java, C#, Rust não há regra no atlas (lacuna).

## 3. Materiais oficiais Anthropic pertinentes
AO-17, AO-19, AO-24, AO-28, AO-06 (verificação, bug com repro e stack em AO-14), AO-22 (código com MCP). Docs: https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools.

## 4. Padrões da comunidade
- Handler fino, camadas verificadas por grep, escopo por `user_id` em toda consulta (CT-07).
- Idempotência obrigatória em efeitos; "single writer" por domínio (CT-07).
- Config por serviço tipado, falha explícita (CT-08).
- Ferramenta pronta para agente: saída curta, erros acionáveis, logs em caminho fixo (CP-12).
- Auth, cripto e flags próprios proibidos quando há biblioteca padrão (CP-24).

## 5. O que o brain-of-agent já oferece
- `brains/fullstack/references/backend-e-contratos.md` e `brains/qa/references/automacao-api.md` (próprios, MIT).
- BR-02 processo fullstack (atenção: `../qa/` relativo quebra em plugin; usar `${CLAUDE_PLUGIN_ROOT}`).
- BR-16/17: revisão e investigação; BR-21: checklist de arquitetura com idempotência e authz.
- BR-03: modo `BACKEND-COMPLETO`.

## 6. Lacunas e cuidados
- Atlas cobre bem Python/FastAPI e Node/NestJS; sem Go, Java/Spring, .NET, Rust, GraphQL, gRPC, versionamento de contrato.
- Regexes de detecção do OWASP são heurísticas.
- "OVERRIDE all other generation behavior" em arquivos comunitários: remover (injeção/tom).
- Contagem de linhas e plugins de wshobson e awesome-copilot não verificada além da raiz.
