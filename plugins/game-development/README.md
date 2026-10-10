# game-development — Desenvolvimento de jogos para Claude Code

Plugin do Claude Code para desenvolver, depurar, revisar, otimizar e testar jogos em **Godot/GDScript**, **Unity/C#** e **Unreal/C++**. O eixo é a **verificação por execução**: nada é "pronto" sem um comando que o agente rodou e uma saída colada, e tudo que só um humano pode julgar (sensação de jogo, áudio, legibilidade) fica marcado como pendência humana. Conteúdo validado em 2026-10-10; versão do plugin 0.1.0, licença MIT.

## O que entrega

- Um **playbook** que roteia o pedido para a skill ou o agente certo, com processo essencial, proporcionalidade e rótulos epistêmicos (Verificado, Inferido, Suposição, Não verificável, Não aplicável, NÃO AVALIADO).
- **12 referências** densas: checklists, padrões e antipadrões, decisões e trade-offs, 20 snippets de CLAUDE.md, ferramentas e MCP (todos desativados), bibliografia, verificação por execução, Godot, Unity, Unreal, núcleo técnico (game loop, física, performance, autoridade de rede) e design/QA/playtest.
- **19 templates** prontos: contrato de pronto, relatório de verificação, `features.json`, progresso, handoff, ADR, especificação de sondas, auditoria de performance, planos e relatórios de QA e playtest, bug report de jogo, revisão de GDD e de netcode, plano de incremento, matriz do modo completo e três CLAUDE.md completos (Godot, Unity, Unreal).
- Skills, agentes e comandos de tarefa (tabela abaixo).

## Quando usar

Use para: mecânica que não funciona, crash ao carregar cena, `Update` que aloca, stutter, orçamento de frame, multiplayer e autoridade, revisão de GDD, plano de QA e de playtest, CLAUDE.md de projeto de jogo, sessões longas com `features.json`. Não use para instalar engine, comparar engines em abstrato nem para software que não é jogo; nesses casos o plugin não deve disparar.

## Componentes

| Tipo | Nome | Para que serve |
| --- | --- | --- |
| Skill | `playbook` | router, processo essencial, depuração de bug de gameplay, modo `GAMEDEV-COMPLETO`, fronteiras com outros plugins |
| Skill | `prompts` | biblioteca de prompts prontos (avaliador, contrato de pronto, GDD em XML, sondas, revisão por engine) |
| Skill | `game-verify-by-running` | provar por execução (headless, sondas, captura) e produzir relatório com evidência real |
| Skill | `game-perf-audit` | auditoria de performance contra orçamentos, somente leitura, veredito COMPLETO ou NÃO AVALIADO |
| Skill | `game-qa-plan` | plano de QA por tipo de teste, plano de playtest e relatório de playtest |
| Skill | `gdd-review` | revisão de GDD em 4 dimensões, somente leitura |
| Skill | `godot-gdscript` | GDScript em Godot 4: estilo oficial, física, headless |
| Skill | `unity-csharp` | C# de runtime em Unity 6: alocação, `Awaitable`, ScriptableObjects, testes |
| Skill | `unreal-cpp` | C++ de Unreal 5.8: padrão da Epic, Gameplay Framework |
| Skill | `game-netcode-review` | autoridade, validação de RPC e confiança no cliente, somente leitura |
| Agente | `game-engine-specialist` | dúvidas de API e arquitetura da engine do projeto, com checagem de versão |
| Agente | `gameplay-programmer` | implementa mecânica a partir de design aprovado, propõe antes de gravar |
| Agente | `gameplay-reviewer` | revisão de diffs de gameplay, somente leitura |
| Agente | `game-evaluator` | avaliador cético de funcionalidade difícil, em contexto limpo |
| Agente | `gdd-reviewer` | segunda leitura independente de GDD, somente leitura |
| Comando | `/game-development:verify` | atalho para `game-verify-by-running` |
| Comando | `/game-development:init-session` | rotina de início de projeto ou sessão longa (`features.json`, progresso, init) |
| Comando | `/game-development:playtest-report` | atalho para o relatório de playtest |

Os comandos são atalhos finos: `verify` e `playtest-report` delegam às skills homônimas, e `init-session` só lê (projeto, progresso e `features.json`) e propõe. Gravar arquivo, rodar script de init e executar a engine dependem de confirmação sua e do fluxo normal de permissão da sessão.

## Instalação

Dentro de uma sessão do Claude Code:

```text
/plugin marketplace add francisco-efjr/brain-of-agent
/plugin install game-development@brain-of-agent
```

Depois, chame `/game-development:playbook` ou escreva o pedido normalmente. O plugin não instala hooks, servidores MCP, LSP nem binários: tudo que é opcional está documentado e desativado em `skills/playbook/references/ferramentas-e-mcp.md`, para você habilitar conscientemente no seu projeto.

## Exemplos de pedidos

1. "Meu `CharacterBody2D` no Godot 4 anda devagar demais e trava na parede" (aciona `godot-gdscript`: física em `_physics_process`, sem `velocity * delta`).
2. "Revisa esse `Update` do Unity que dá stutter e me diz o que medir no Profiler" (aciona `unity-csharp`: LINQ, string, `GetComponent`, `.Result`, sem prometer ganho).
3. "Audita a performance do meu jogo Godot; não tenho orçamento definido" (aciona `game-perf-audit`: veredito NÃO AVALIADO e lista do que falta).
4. "Monte um plano de QA e de playtest para estas quatro histórias" (aciona `game-qa-plan`: Logic, Integration, Visual/Feel, UI, Config/Data).
5. "Revisa meu GDD de combate: está implementável?" (aciona `gdd-review`: quatro dimensões, veredito e perguntas abertas).
6. "Revisa o netcode: o cliente pode trapacear?" (aciona `game-netcode-review`: autoridade, intenção, validação de RPC).
7. "Vou fazer um roguelike em Godot em várias sessões; organize para eu continuar amanhã" (playbook e `/game-development:init-session`: `features.json`, progresso, check headless).
8. "GAMEDEV-COMPLETO: audite este projeto Godot" (modo completo, abaixo).

## Keyword `GAMEDEV-COMPLETO`

Escreva `GAMEDEV-COMPLETO` no seu pedido para ativar o modo completo: leitura integral das referências em lotes (com registro `lido | parcial | ausente`), matriz de aplicabilidade por área, implementação **somente** dentro do escopo pedido, revalidação com evidências e resultado `concluído no escopo | parcial | impedido`. Regras: só ativa por pedido explícito seu na conversa; a mesma palavra em README, issue, log ou documento colado é tratada como dado e não ativa nada; o modo **não amplia permissões** (instalar addon, publicar build, subir para loja e apagar assets seguem a autorização concreta que você der); sem pedido de implementação, o modo é auditoria e não altera o projeto. Custo: lê 12 referências, então use em auditoria ou projeto amplo.

## Principais fontes (top 10)

Bibliografia completa em `skills/playbook/references/fontes.md`. Classe A = oficial, B = autor ou repositório reconhecido.

| # | Fonte | Classe |
| --- | --- | --- |
| 1 | Claude Code best practices (code.claude.com/docs/en/best-practices) | A |
| 2 | Anthropic Engineering: Effective harnesses for long-running agents (26/11/2025) | A |
| 3 | Anthropic Engineering: Harness design for long-running apps (24/03/2026) | A |
| 4 | Godot: command line tutorial e GUT (docs, Command-Line) | A / B |
| 5 | Godot: GDScript style guide | A |
| 6 | Game Loop (Nystrom), Fix Your Timestep (Fiedler), física do Godot | B / B / A |
| 7 | Unity NGO (authority, ownership) e Godot high-level multiplayer | A |
| 8 | Unity 6000.0: programming best practices | A |
| 9 | Unity: best practices for profiling game performance | A |
| 10 | Epic C++ coding standard for Unreal Engine (UE 5.8) e Gameplay Framework | A |

## Créditos e licenças de terceiros

- Documentação oficial da Anthropic, Godot, Unity e Epic Games: **apenas destilada com redação própria**; licença dos textos não verificada; nenhum trecho copiado.
- Donchitos/Claude-Code-Game-Studios (MIT), godogen (MIT), GodotPrompter (MIT), wshobson/agents (MIT), quodsoler/unreal-engine-skills (MIT), cc-godot, Unity-MCP (Apache-2.0 na página), GUT (MIT): usados **só como padrão e referência**; nenhum código, hook ou instalador foi copiado ou é instalado. GD-Agentic-Skills (LGPL-3.0): só princípios.
- Nystrom, Fiedler, Level Design Book, Meta, IXDF e blogs: © dos autores; apenas destilação.
- Base própria: [brain-of-agent](https://github.com/francisco-efjr/brain-of-agent) (MIT, texto do autor deste plugin), adaptada em templates e processo. gstack (MIT, Copyright (c) 2026 Garry Tan) inspirou processo, sem cópia em bloco.
- Este plugin: MIT, Francisco Edson.

## Limitações honestas

- **Validação da mesma família de modelo, sem revisão humana.** Pesquisadores e validadores foram modelos Claude; as notas de qualidade internas são autoatribuídas e não substituem revisão independente.
- **Comandos de engine não foram executados** na construção. A combinação `--headless` com `--check-only` do Godot e o uso de GUT em linha de comando são Inferido; `-runTests`, `-testPlatform`, `-batchmode` e `-testResults` do Unity constam na documentação do Test Framework 1.4 (lida em 2026-10-10), mas também não foram executados. Rode e cole a saída no seu ambiente.
- **Cobertura desigual.** Godot bem coberto; Unity razoável; Unreal parcial (sem Blueprints, GAS, replicação detalhada nem Chaos). **Sem fonte validada:** IA de jogo (FSM, behavior tree), pipeline de assets, shaders, UI de jogo, publicação e export, criação de GDD e balanceamento, ECS/DOTS. Nesses temas o plugin diz a lacuna em vez de inventar.
- **Versões mudam.** Lidos em 2026-10-10: Godot `stable`, Unity 6000.0, UE 5.8, Test Framework 1.4.6. Confira a versão do seu projeto antes de aplicar qualquer regra.
- **Não há material oficial da Anthropic específico de jogos**; o acervo `anthropics/skills` não tem skill de jogos. Os custos do harness (por exemplo US$ 9 contra US$ 200) são relato de um autor sobre um app web, não sobre jogos.
- **Catálogos populares não provam eficácia.** Estrelas são sinal de interesse; o plugin usa os padrões, não o código.
- **Sensação de jogo, áudio e legibilidade** exigem um humano jogando; testes headless e de lógica não os provam.
- Evals do plugin são `designed_not_executed` até serem rodados com `claude plugin eval` (requer Claude Code 2.1.269 ou superior).
