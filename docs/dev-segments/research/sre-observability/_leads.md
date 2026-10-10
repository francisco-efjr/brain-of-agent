# sre-observability — pistas do atlas global

Data: 2026-10-09 · Indexador do atlas (Claude Sonnet 5.5) · Origem: `docs/research/_global/*.validated.md` (IDs: AO, EC, CT, PC, CP, BR).
Pista é ponto de partida: reabrir a URL antes de citar. Cobertura do atlas é fraca neste segmento. Princípios comuns: `docs/foundation/prompt-principles.md`.

## 1. Pistas aprovadas aplicáveis

| Pista | URL | Classe | O que aproveitar |
| --- | --- | --- | --- |
| superpowers `systematic-debugging` (EC-01) | https://github.com/obra/superpowers | A | Causa raiz antes de corrigir, 4 fases, rever a arquitetura após 3 correções falhas (Verificado). MIT. |
| wshobson/agents, `debugging-toolkit/agents/debugger.md` e `incident-response` (EC-10) | https://github.com/wshobson/agents | B | 5 passos (capturar, reproduzir, isolar, correção mínima, verificar) e saída com causa raiz, evidência, correção, teste, prevenção. Sem `tools`: restringir ao destilar. |
| VoltAgent subagents (EC-09) | https://github.com/VoltAgent/awesome-claude-code-subagents | B | Categorias de agentes (tag SRE); abrir `categories/`. Prompts longos. |
| gstack `plan-eng-review` (EC-11) | https://github.com/garrytan/gstack | B | Seção de performance e observabilidade. |
| `/investigate`, `/canary`, `/benchmark`, `/health` (BR-17, BR-24) | https://github.com/garrytan/gstack | B | Iron Law; 3 strikes; alerta após 2 checks consecutivos; comparar com baseline salvo. MIT, destilar com atribuição. |
| performance-optimization.instructions.md (CT-19) | https://github.com/github/awesome-copilot | B | LCP/INP/CLS e bundle; só frontend, sem backend/N+1. MIT. |
| Compilador C e teste desenhado para o modelo (AO-31) | https://www.anthropic.com/engineering/building-c-compiler | A | Console mínimo, log em arquivo, erros grep-áveis; relato da Anthropic. |
| Hamel e Shreya, AI Evals FAQ (PC-17) | https://hamel.dev/blog/posts/evals-faq/ | A | Observabilidade e análise de erros (60 a 80% do tempo); aplica a LLM em produção. |
| Chip Huyen (PC-19) | https://huyenchip.com/2025/01/07/agents.html | B | Plataforma GenAI: observabilidade e permissões. Não reverificado. |
| How Anthropic teams use Claude Code (CP-15) | https://claude.com/blog/how-anthropic-teams-use-claude-code | B | Casos de debugging de incidentes (equipes de infra); não reverificado. |
| Ronacher (CP-12) | https://lucumr.pocoo.org/2025/6/12/agentic-coding/ | B | Logs em caminho fixo, ferramentas idempotentes, timeouts. |
| Ask HN (CP-21) | https://news.ycombinator.com/item?id=46691243 | B | Logar para o agente "ver". |
| Dan Luu / Lars Faye (CP-20) | https://danluu.com/ai-coding/ | B | Fuzzing tende a vencer LLM na busca de bugs; variância alta. |
| Hooks e `PostCompact` (CP-14) | https://support.claude.com/en/articles/14554000-claude-code-power-user-tips | A | Reinjetar regras operacionais após compactação. |
| Common workflows, bug com repro (AO-14) | https://code.claude.com/docs/en/common-workflows | A | Bug com repro e stack; refactor incremental. |
| ADR/debug agents (CT-21) | https://github.com/github/awesome-copilot | B | "Always reproduce and understand the bug before attempting to fix it." MIT. |

## 2. Repositórios e arquivos a abrir
- `obra/superpowers/skills/systematic-debugging/SKILL.md`.
- `wshobson/agents/plugins/debugging-toolkit/agents/debugger.md`, `plugins/incident-response`.
- `github/awesome-copilot/agents/debug.agent.md`.
- `VoltAgent/awesome-claude-code-subagents/categories` (SRE, observabilidade).
- OpenTelemetry, Prometheus, Grafana, SRE Book, k6/Locust não estão no atlas: lente authoritative obrigatória.

## 3. Materiais oficiais Anthropic pertinentes
AO-31 (compilador C, lessons), AO-14, AO-06, AO-23. Nenhum material Anthropic aprovado trata SLO, alertas ou postmortem.

## 4. Padrões da comunidade
- Reproduzir antes de corrigir; hipóteses registradas; parar após 3 tentativas (EC-01, BR-17).
- Teste de regressão que falhava antes (CP-11, BR-17).
- Alerta só após checks consecutivos, comparação com baseline (BR-24).
- Logs e saída curtos, grep-áveis, para o agente consumir (AO-31, CP-12).
- Registrar comando + saída real, não "esperado" (CP-11).

## 5. O que o brain-of-agent já oferece
- `brains/fullstack/references/entrega-e-operacao.md`, `brains/qa/references/performance.md`, `vendor/gstack/canary/SKILL.md`, `vendor/gstack/benchmark/SKILL.md`.
- BR-17: Iron Law (linha ~393) e 3 strikes (linha ~588), Verificados no snapshot.
- BR-24: `/health`, `/canary`, `/benchmark`. BR-06/07: handoff e registro de evidências.
- BR-03: modo `SRE-COMPLETO`.

## 6. Lacunas e cuidados
- Sem fonte aprovada para SLI/SLO/error budget, alertas acionáveis, postmortem blameless, runbooks, capacidade, testes de carga, caos, OpenTelemetry.
- Skill de SRE/Terraform de Towards AI e AWS Fundamentals foi rejeitada (CP-30): não usar.
- Prompts de debugger com todas as tools herdadas: declarar `tools`.
- Nada de acessar sistemas de produção; incidentes reais exigem autorização e leitura somente.
