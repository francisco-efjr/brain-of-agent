# Fontes do plugin game-development

Bibliografia validada. Classe A = oficial (Anthropic, mantenedor da engine ou da norma); B = autor reconhecido ou repositório com sinais; C = relato de praticante ou comunidade, só como ideia ou caso negativo. Consulta de todas: **2026-10-10** (pesquisa por modelos `claude-haiku-5-5`, validação por `claude-sonnet-5-5`: mesma família, sem revisão humana; a única exceção é o guia de hooks, reaberto pelo construtor na mesma data). "Licença: não verificada" significa que o conteúdo do plugin é **destilação com redação própria**, sem texto copiado. IDs `V-nn` referem-se ao VALIDATED do segmento. Estrelas e forks são sinais de interesse, não de eficácia.

## Sumário

- [Anthropic e Claude Code](#anthropic-e-claude-code)
- [Engines: Godot](#engines-godot)
- [Engines: Unity](#engines-unity)
- [Engines: Unreal](#engines-unreal)
- [Padrões de programação de jogos](#padrões-de-programação-de-jogos)
- [Design, QA e playtest](#design-qa-e-playtest)
- [Repositórios e práticas B](#repositórios-e-práticas-b)
- [Comunidade classe C](#comunidade-classe-c)
- [Base própria e terceiros incorporados](#base-própria-e-terceiros-incorporados)
- [Dados de repositório](#dados-de-repositório)
- [Rejeitadas ou sem aproveitamento](#rejeitadas-ou-sem-aproveitamento)
- [Lacunas de pesquisa](#lacunas-de-pesquisa)

## Anthropic e Claude Code

| V | Título | URL | Classe | Licença | Uso no plugin |
| --- | --- | --- | --- | --- | --- |
| V-01 | Claude Code: best practices | https://code.claude.com/docs/en/best-practices | A | não verificada | verificação executável, explorar-planejar-implementar, CLAUDE.md enxuto, revisor adversarial |
| V-02 | Claude Code: memory | https://code.claude.com/docs/en/memory | A | não verificada | abaixo de 200 linhas, regras com `paths`, `CLAUDE.local.md`, hook como garantia |
| V-03 | Claude Code: sub-agents | https://code.claude.com/docs/en/sub-agents | A | não verificada | campos, precedência, plugin ignora `hooks`/`mcpServers`/`permissionMode`, mínimo privilégio |
| (construtor) | Claude Code: guia de hooks | https://code.claude.com/docs/en/hooks-guide | A | não verificada | estrutura do hook `PreToolUse`/`PostToolUse`, exit 2, `tool_input.file_path` (T-06, T-07) |
| V-04 | Effective harnesses for long-running agents (26/11/2025) | https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | A | não verificada | `features.json` com `passes`, rotina de sessão, init |
| V-05 | Harness design for long-running apps (24/03/2026) | https://www.anthropic.com/engineering/harness-design-long-running-apps | A | não verificada | contrato, avaliador cético, limiar por critério, custos |
| V-06 | Demystifying evals for AI agents (09/01/2026) | https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | A | não verificada | 20 a 50 tarefas de falhas reais, graders, casos negativos |
| V-07 | Agent Skills: best practices | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices | A | não verificada | limites de frontmatter, tamanho, avaliações |
| V-08 | skill-creator (anthropics/skills) | https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md | A | Apache-2.0 (LICENSE.txt da pasta); campo `license` do repositório `null` | ciclo com e sem skill, matriz de gatilho; scripts não executados |
| V-09 | Claude prompting best practices | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | A | não verificada | XML, documentos no topo, citações primeiro, tom calmo |
| V-10 | Building a C compiler (05/02/2026, N. Carlini) | https://www.anthropic.com/engineering/building-c-compiler | A | não verificada | saída curta, amostra rápida, oráculo (analogia a jogos: Inferido) |

## Engines: Godot

| V | Título | URL | Classe | Licença | Uso |
| --- | --- | --- | --- | --- | --- |
| V-11 | GDScript style guide | https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_styleguide.html | A | não verificada | nomes, ordem de membros, tipagem |
| V-12 | Godot: command line tutorial | https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html | A | não verificada | `--headless`, `--import`, `--check-only`, `--path`; `--script` exige script herdando `SceneTree` ou `MainLoop` ao executar (relido em 2026-10-10) |
| V-12 | GUT: docs e Command-Line | https://gut.readthedocs.io/en/latest/ · https://gut.readthedocs.io/en/latest/Command-Line.html | B | MIT | `gut_cmdln.gd`, exit code |
| V-13 | Godot: general optimization | https://docs.godotengine.org/en/stable/tutorials/performance/general_optimization.html | A | não verificada | medir, bisseção, V-Sync off |
| V-14 | Godot: physics introduction | https://docs.godotengine.org/en/stable/tutorials/physics/physics_introduction.html | A | não verificada | `_physics_process`, `move_and_slide()`, camadas |
| V-15 | Godot: high-level multiplayer | https://docs.godotengine.org/en/stable/tutorials/networking/high_level_multiplayer.html | A | não verificada | autoridade, validação de RPC |
| V-32 | Godot: classe TileMap | https://docs.godotengine.org/en/stable/classes/class_tilemap.html | A | não verificada | depreciação em favor de `TileMapLayer` |

## Engines: Unity

| V | Título | URL | Classe | Licença | Uso |
| --- | --- | --- | --- | --- | --- |
| V-15 | NGO: authority (2.7) | https://docs.unity3d.com/Packages/com.unity.netcode.gameobjects@2.7/manual/terms-concepts/authority.html | A | não verificada | uma autoridade por `NetworkObject`, `HasAuthority` |
| V-15 | NGO: ownership (2.5) | https://docs.unity3d.com/Packages/com.unity.netcode.gameobjects@2.5/manual/basics/ownership.html | A | não verificada | servidor decide spawn e despawn |
| V-16 | Unity 6000.0: programming best practices | https://docs.unity3d.com/6000.0/Documentation/Manual/programming-best-practices.html | A | não verificada | alocação, ciclo de vida, `Awaitable`, threads |
| V-17 | Unity: best practices for profiling game performance | https://unity.com/how-to/best-practices-for-profiling-game-performance | A | não verificada | ms por quadro, 33,33/16,66 ms, CPU vs GPU, 35% livre em mobile |
| V-18 | Unity: architect game code with ScriptableObjects (jan/2020) | https://unity.com/how-to/architect-game-code-scriptable-objects | B | não verificada | variáveis e eventos em assets; fonte antiga |
| V-21 | Unity Test Framework 1.4 | https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/index.html | A | não verificada | EditMode/PlayMode; a página antiga de CLI deu 404 na pesquisa original |
| V-21b | Unity Test Framework 1.4: command-line reference (conferida na validação de qualidade, 2026-10-10) | https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/reference-command-line.html | A | não verificada | `-runTests`, `-testPlatform`, `-testResults`, `-batchmode` |
| V-31 | Unity-MCP: CLAUDE.md | https://github.com/IvanMurzak/Unity-MCP/blob/main/Unity-MCP-Plugin/CLAUDE.md | B | Apache-2.0 (página) | regras com editor via MCP |
| V-31 | CLAUDE.md for Unity (D. Reimer, 26/02/2026) | https://devinreimer.substack.com/p/building-a-solid-claudemd-for-unity | B | © do autor: só destilar | regras subjetivas segundo o autor |
| V-33 | Unity plugin for Claude Code (09/09/2026) | https://unity.com/blog/unity-plugin-for-claude-code | B (promocional) | não verificada | lista de domínios; sem regras |

## Engines: Unreal

| V | Título | URL | Classe | Licença | Uso |
| --- | --- | --- | --- | --- | --- |
| V-19 | Epic C++ coding standard for Unreal Engine (UE 5.8) | https://dev.epicgames.com/documentation/en-us/unreal-engine/epic-cplusplus-coding-standard-for-unreal-engine | A | não verificada | prefixos, lambdas diferidas, enums, namespaces |
| V-20 | Unreal: Gameplay Framework | https://dev.epicgames.com/documentation/en-us/unreal-engine/gameplay-framework-in-unreal-engine | A | não verificada | onde cada dado mora |
| V-34 | quodsoler/unreal-engine-skills | https://github.com/quodsoler/unreal-engine-skills | B | MIT | formato de skill de engine com versão e deprecados |

## Padrões de programação de jogos

| V | Título | URL | Classe | Licença | Uso |
| --- | --- | --- | --- | --- | --- |
| V-14 | Game Loop (R. Nystrom, *Game Programming Patterns*) | https://gameprogrammingpatterns.com/game-loop.html | B | © 2009-2021 do autor: só destilar | passo fixo, interpolação, teto de iterações |
| V-14 | Fix Your Timestep (G. Fiedler, 10/06/2004) | https://gafferongames.com/post/fix_your_timestep/ | B | © do autor: só destilar | acumulador, teto de 0,25 s, `alpha` |

## Design, QA e playtest

| V | Título | URL | Classe | Licença | Uso |
| --- | --- | --- | --- | --- | --- |
| V-26 | qa-plan (Donchitos) | https://raw.githubusercontent.com/Donchitos/Claude-Code-Game-Studios/main/.claude/skills/qa-plan/SKILL.md | B | MIT | tipos de teste |
| V-27 | design-review (Donchitos) | https://raw.githubusercontent.com/Donchitos/Claude-Code-Game-Studios/main/.claude/skills/design-review/SKILL.md | B | MIT | rubrica de GDD em 4 dimensões |
| V-25 | perf-profile (Donchitos) | https://raw.githubusercontent.com/Donchitos/Claude-Code-Game-Studios/main/.claude/skills/perf-profile/SKILL.md | B | MIT | auditoria com orçamentos, NÃO AVALIADO |
| V-28 | playtest-report (Donchitos) | https://raw.githubusercontent.com/Donchitos/Claude-Code-Game-Studios/main/.claude/skills/playtest-report/SKILL.md | B | MIT | relatório que separa bug de pain point |
| V-28 | Level Design Book: playtesting | https://book.leveldesignbook.com/process/blockout/playtesting | B | não verificada | observar mais que perguntar |
| V-28 | Meta: playtest planning | https://developers.meta.com/horizon/resources/playtest-planning-survey-script/ | B | não verificada | plano, papéis, consentimento |
| V-28 | IXDF: playtesting | https://ixdf.org/literature/topics/playtesting | B | não verificada | "5 a 8 jogadores" (referência comercial) |

## Repositórios e práticas B

| V | Título | URL | Classe | Licença | Uso |
| --- | --- | --- | --- | --- | --- |
| V-22, V-23, V-24 | Donchitos/Claude-Code-Game-Studios (CLAUDE.md, agentes `gameplay-programmer` e `godot-specialist`) | https://github.com/Donchitos/Claude-Code-Game-Studios | B | MIT | protocolo "perguntar antes de gravar", padrões de agentes; 12 hooks **não** adotados |
| V-29 | htdt/godogen | https://github.com/htdt/godogen | B | MIT | só o padrão de critério de aceite por execução; **não instalar** |
| V-30 | Porting a 1993 Amiga game to Godot (Babylonian Twins, 01/09/2026) | https://babyloniantwins.com/blog/porting-a-1993-amiga-game-to-godot/ | B | © do autor: só destilar | sondas, checks headless, oráculo |

## Comunidade classe C

| V | Título | URL | Classe | Licença | Uso |
| --- | --- | --- | --- | --- | --- |
| V-35 | wshobson/agents (plugin game-development) | https://github.com/wshobson/agents | B/C | MIT | só referência; "Aspects" do ECS não verificado |
| V-35 | jame581/GodotPrompter | https://github.com/jame581/GodotPrompter | B/C | MIT | índice de domínios; hook `SessionStart` não adotado |
| V-35 | thedivergentai/GD-Agentic-Skills | https://github.com/thedivergentai/GD-Agentic-Skills | C | LGPL-3.0 | só princípios; `npx` não adotado |
| V-35 | Zate/cc-godot | https://github.com/Zate/cc-godot | C | MIT (README) | só referência; hook e `.mcp.json` não adotados |
| V-35 | PatrickJS/awesome-cursorrules | https://github.com/PatrickJS/awesome-cursorrules | C | CC0-1.0 (API) | sem Godot nem Unreal |
| V-36 | davila7/claude-code-templates (agente `unity-game-developer`) | https://github.com/davila7/claude-code-templates | C | MIT (página) | caso negativo |
| V-36 | dev.to (Lucca Sanwald, 22/06/2025) e mirror de Reddit r/ClaudeAI | URLs exatas não registradas no VALIDATED | C | © dos autores | anti-padrões de jogo inteiro numa tarefa |

## Base própria e terceiros incorporados

| Item | Origem | Licença | Uso |
| --- | --- | --- | --- |
| brain-of-agent: `handoff-checkpoint`, `plano-incremento`, `adr`, `protocolo-completo`, `testes-e-debugging` (fullstack), `bug-report`, `charter-exploratorio`, `checklist-release` (qa) | francisco-efjr/brain-of-agent (snapshot em `docs/foundation/brain-of-agent-snapshot/`) | MIT, texto próprio do usuário | templates e processo, adaptados a jogos |
| gstack (Garry Tan) | `vendor/gstack` do snapshot | MIT, Copyright (c) 2026 Garry Tan | inspiração de processo, sem cópia em bloco |

## Dados de repositório

Observados em 2026-10-10 pela API pública (V-08, V-22, V-29, V-34, V-35): anthropics/skills 180.246 estrelas e 21.331 forks; Donchitos 26.049 estrelas, 3.696 forks, MIT, 63 issues abertas, 49 agentes, 74 skills, 12 hooks, push em 2026-10-08; wshobson/agents 40.318 estrelas (do marketplace inteiro); godogen 7.079 estrelas, MIT; GodotPrompter 806 estrelas, 56 skills; GD-Agentic 823 estrelas; quodsoler 363 estrelas, 27 skills; Unity-MCP cerca de 4,4 mil estrelas. Popularidade alta **sem evidência independente de eficácia**.

## Rejeitadas ou sem aproveitamento

BlueBirdBack/godot-cursorrules (último push em 2025-03-25, formato legado); thepromptshelf.dev (sem autoria, conteúdo em massa); vegcale.com (afiliados); claudecodeguides.com (números de economia sem fonte); Summer Engine (fornecedor; só a frase sobre limites do headless foi confirmada); cryptorabea Unity; pluginagentmarketplace (licença personalizada); overlook-game-framework; GDQuest (classe C, texto antigo); agenda do GDC (HTTP 403); Medium "testes passam, jogo injogável" (HTTP 403, nunca lida); comentário isolado do HN. O acervo `anthropics/skills` não tem skill de jogos (V-08).

## Lacunas de pesquisa

IA de jogo (FSM, behavior tree; pista Game AI Pro Vol. 1 cap. 6 e 10, gratuito, sem redistribuição, não lido); pipeline de assets; shaders; UI de jogo; publicação e export; criação de GDD, balanceamento e economia; ECS/DOTS (documentação oficial de Entities); Unreal Blueprints, GAS e replicação; Unity por CLI em versões fora do Test Framework 1.4 (as opções `-runTests` e `-testPlatform` foram lidas na doc 1.4); física em Unity e Unreal; playtest automatizado e rede determinística; Reddit oficial, X, YouTube e palestras do GDC. Novas skills só quando houver fonte validada.
