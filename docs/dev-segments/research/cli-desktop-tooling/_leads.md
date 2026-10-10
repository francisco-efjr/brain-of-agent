# cli-desktop-tooling — pistas do atlas global

Data: 2026-10-09 · Indexador do atlas (Claude Sonnet 5.5) · Origem: `docs/research/_global/*.validated.md` (IDs: AO, EC, CT, PC, CP, BR).
Pista é ponto de partida: reabrir a URL antes de citar. Princípios comuns: `docs/foundation/prompt-principles.md`.

## 1. Pistas aprovadas aplicáveis

| Pista | URL | Classe | O que aproveitar |
| --- | --- | --- | --- |
| Ronacher, agentic coding (CP-12) | https://lucumr.pocoo.org/2025/6/12/agentic-coding/ | B | Checklist de CLI pronta para agente: rápida, saída curta, erros acionáveis, idempotente, logs em caminho fixo, timeout; CLI antes de MCP. Não reverificado. |
| gstack `/devex-review`, `/plan-devex-review` (BR-25) | https://github.com/garrytan/gstack | B | Roteiro TTHW: instalar só pelo README, cronometrar, registrar atritos, erros acionáveis, desinstalação limpa. Única fonte do segmento no brain. |
| AGENTS.md (CT-01) | https://agents.md/ | A | Documentar comandos exatos e limites para ferramentas; esqueleto. |
| Compatibilidade entre ecossistemas (CT-27) | https://github.com/intellectronica/ruler | B | Regras para AGENTS.md portátil; ruler MIT, 2.941★ (Verificado). Detalhes: continue.dev, kiro.dev, geminicli.com (instável), zed.dev, junie.jetbrains.com, ampcode.com, opencode.ai. |
| Trail of Bits config e skills (EC-12) | https://github.com/trailofbits/claude-code-config | B | Sandbox, deny rules, hooks que bloqueiam `rm -rf`; guardrail, não fronteira. skills: CC-BY-SA-4.0, destilar. |
| claude-plugins-official, `claude-code-setup`, `mcp-server-dev` (AO-30, EC-05) | https://github.com/anthropics/claude-plugins-official | A | Referência oficial de formato; ferramentas de DX. Apache-2.0. |
| Thariq, dicas de skills (CP-07) | https://raw.githubusercontent.com/shanraisshan/claude-code-best-practice/main/tips/claude-thariq-tips-17-mar-26.md | A | Scripts reutilizáveis; dados persistentes em pasta estável do plugin. |
| Boris Cherny setup (CP-01) | https://news.ycombinator.com/item?id=46470017 | A | Fluxos diários viram skill versionada; allowlist em settings. |
| Dwyer SPEC (CP-25) | https://www.dwyer.co.za/static/claude-code-is-all-you-need.html | B | CLI pequena em SPEC curta com verificação e2e. Falhas relatadas (deps de 500MB). |
| Bitcraze (CP-27) | https://www.bitcraze.io/?p=14780 | B | CLI com subcomandos one-shot e saída curta. |
| Writing tools for agents (AO-17) | https://www.anthropic.com/engineering/writing-tools-for-agents | A | Boas práticas de interface para ferramentas consumidas por agentes (aplica a CLI). |
| Prompting best practices (AO-01) | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | A | Escopo e confirmação de ações destrutivas. |
| Context engineering e Claude 5 rules (PC-27) | https://claude.dev/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models/ | A | Descrição simples de tool. |
| GPT-4.1 prompting guide (PC-01) | https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide | A | Tools pelo campo `tools`; adaptar. MIT (cookbook). |
| AGENTS.md hygiene (CT-02, CT-29) | https://fabiensanglard.net/agent.md/index.html | B | Regra de ambiente (flox, uv, pnpm) vale mais que dez de estilo. |
| ECC (EC-13) | https://github.com/affaan-m/ECC | B | Paridade Windows limitada; instalador executa código: não rodar. |

## 2. Repositórios e arquivos a abrir
- `intellectronica/ruler`, `agentsmd/agents.md`.
- `garrytan/gstack` skills de devex (no snapshot do brain).
- `anthropics/claude-plugins-official/plugins/claude-code-setup`, `mcp-server-dev`.
- clig.dev (citado como "não verificado" no brain), docs do Electron/Tauri/.NET, guias PowerShell: não estão no atlas; lente authoritative.

## 3. Materiais oficiais Anthropic pertinentes
AO-17, AO-30, AO-31 (skills lessons), AO-07 (memória), AO-08 (skills no Claude Code), AO-12; https://code.claude.com/docs/en/plugins para empacotamento de ferramentas.

## 4. Padrões da comunidade
- CLI antes de MCP; logs em caminho fixo no CLAUDE.md (CP-12).
- Instalação cronometrada pelo README para medir DX (BR-25).
- Hooks de segurança como exemplo documentado (CP-19, EC-12).
- Windows: symlink é frágil; ponte `@AGENTS.md` (CT-04).

## 5. O que o brain-of-agent já oferece
- `vendor/gstack/devex-review/SKILL.md` e `plan-devex-review/SKILL.md`.
- BR-13 (router + registry, 64 entradas), BR-25 (TTHW), BR-26 (modelo de segurança de automação).
- BR-10: scripts stdlib com chamada por caminho explícito.
- BR-03: modo `TOOLING-COMPLETO`.

## 6. Lacunas e cuidados
- Sem fonte aprovada para design de CLI (clig.dev), TUI, Electron/Tauri/.NET/Qt, empacotamento, assinatura de código, auto-update, PowerShell.
- Matriz de ecossistemas (CT-27): linhas goose/Augment/Factory/Devin Não verificadas.
- Instalação de ferramentas de terceiros por README exige autorização explícita.
