# game-development — pistas do atlas global

Data: 2026-10-09 · Indexador do atlas (Claude Sonnet 5.5) · Origem: `docs/research/_global/*.validated.md` (IDs: AO, EC, CT, PC, CP, BR).
Segmento com a pior cobertura do atlas: pistas são poucas e fracas. Princípios comuns: `docs/foundation/prompt-principles.md`.

## 1. Pistas aprovadas aplicáveis

| Pista | URL | Classe | O que aproveitar |
| --- | --- | --- | --- |
| htdt/godogen (EC-21) | https://github.com/htdt/godogen | B (6) | Ideia: pipeline Godot gerado por skills com assets e engine. MIT; ~7,1k★ (HTML); HN 337 pts em 2026-03-16. Executa engine e gera assets: não executar; conteúdo não lido. |
| wshobson/agents, `game-development` (EC-10) | https://github.com/wshobson/agents | B | Plugin citado pelo atlas; abrir e verificar. MIT. |
| Harnesses para apps longos (AO-20) | https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | A | `features.json` com `passes`, rotina de início de sessão, avaliador cético; transferível a jogos longos. Também: https://www.anthropic.com/engineering/harness-design-long-running-apps |
| awesome-cursorrules (CT-06) | https://github.com/PatrickJS/awesome-cursorrules | B | O atlas anota "game-development fraco (sem Godot/Unreal)". Anti-exemplo `unity-cursor-ai-c-…`: regra de projeto único. Só calibração negativa. |
| Compilador C (AO-31) | https://www.anthropic.com/engineering/building-c-compiler | A | Testes e saída desenhados para o modelo; relato de projeto longo. |
| Prompting best practices (AO-01) | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | A | Estado em JSON + git para tarefas longas. |
| awesome-copilot (CT-14) | https://github.com/github/awesome-copilot | A | Atlas diz que cobre 24 de 25 segmentos; game-dev não detalhado: abrir. |
| Sanity (CP-22) | https://www.sanity.io/blog/first-attempt-will-be-95-garbage | B | Sem sessões paralelas no mesmo módulo. |
| Ronacher (CP-12) | https://lucumr.pocoo.org/2025/6/12/agentic-coding/ | B | Ferramentas com saída curta e logs em caminho fixo, úteis para engines. |
| Bitcraze, loop com hardware (CP-27) | https://www.bitcraze.io/?p=14780 | B (5) | Padrão de CLI curto para ciclo build → observar; analogia para engines (Inferido). |
| Willison (CP-11) | https://simonwillison.net/guides/agentic-engineering-patterns/ | B | Screenshots e testes agentic como evidência de gameplay. |

## 2. Repositórios e arquivos a abrir
- `htdt/godogen` (README e skills; sem executar).
- `wshobson/agents/plugins/game-development`.
- Documentação oficial de Unity, Unreal, Godot, GDC talks, game design (GDD, balanceamento) não está no atlas: lente authoritative integral.
- Reddit r/gamedev e dev.to/Godot: o atlas rejeitou os achados (CP-28); novas buscas devem ser independentes.

## 3. Materiais oficiais Anthropic pertinentes
AO-20 (harness), AO-31, AO-01, AO-06. Nenhum material Anthropic específico de jogos foi aprovado.

## 4. Padrões da comunidade
- Nenhum padrão aprovado. Princípios de mobile/embarcados podem transferir: separar terminal e engine, declarar limites do agente (Inferido).
- Verificação por captura de tela não prova persistência (BR-04).

## 5. O que o brain-of-agent já oferece
- `brain_refs` vazio em `segments.json`: sem brain específico (BR transversais: game-dev praticamente nulo).
- Reaproveitáveis de forma transversal: BR-04 (rótulos), BR-06/07 (templates de handoff e plano), BR-18 (tiers por risco), BR-24 (`/benchmark` para performance).
- BR-03: modo `GAMEDEV-COMPLETO`.

## 6. Lacunas e cuidados
- Sem fonte para Unity/C#, Unreal/Blueprints, Godot/GDScript, ECS, netcode, shaders, pipeline de assets, playtesting, publicação.
- godogen executa engine e gera assets: apenas documentar.
- Exigir pesquisa própria nas três lentes; esperar volume baixo e rotular tudo.
