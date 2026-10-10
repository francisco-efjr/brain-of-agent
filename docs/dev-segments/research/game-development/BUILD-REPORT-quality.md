# BUILD-REPORT de qualidade: plugin game-development

Data: 2026-10-10. Plugin: `C:\Users\Francisco Edson\dev-segments\plugins\game-development` (0.1.0). Rubrica: `docs/foundation/prompt-quality-rubric.md` (D1 a D12, nota = média x 20).

**Independência:** o validador é um modelo Claude, da mesma família dos construtores. As notas abaixo são autoatribuídas por família de modelo e não substituem revisão humana nem execução dos evals (`designed_not_executed`).

## 1. Cobertura da revisão

| Escopo | Como foi lido |
| --- | --- |
| README, `playbook/SKILL.md`, 8 skills de tarefa, `prompts/SKILL.md`, 5 agentes, 3 comandos, `evals/README.md` | Leitura integral |
| Biblioteca de prompts | 15 de 33 lidos por inteiro: P-01, 02, 03, 04, 05, 06, 13, 14, 15, 18, 22, 23, 31, 32, 33 |
| Evals | 8 dos 12 casos originais lidos por inteiro (prompt e graders); 4 (`netcode-rpc-sem-validacao`, `qa-tipos-de-teste`, `unity-update-alocacao`, `unreal-lambda-diferida`) só pela tabela do README de evals |
| References do playbook | `ferramentas-e-mcp`, `unreal`, `nucleo-tecnico` (até autoridade de rede), `claude-md-snippets` (início) lidas; as demais conferidas por grep de segurança, tom e afirmações-chave |
| Templates | `contrato-de-pronto`, `features-json`, `claude-md-godot` lidos; os outros 16 não revisados um a um |
| References das skills de tarefa | Não lidas por inteiro; conferidas por grep (links, tom, afirmações de CLI) |

Verificações automáticas: sem CAPS ou ameaças (`NUNCA`, `MUST`, `CRITICAL`) fora de citação; nenhum `git commit`/`push`/`rm -rf` autorizado; descrições entre 117 e 866 caracteres; skills com no máximo 200 linhas.

## 2. Notas D1 a D12 (antes e depois)

Os blocos de justificativa seguem as dimensões; a nota de cada arquivo é a média x 20 arredondada.

| Arquivo | Antes | Depois | Correções |
| --- | --- | --- | --- |
| `README.md` | 84 | 88 | Frase obsoleta ("escritos em paralelo, confira a pasta") trocada por descrição real dos comandos e do que exige confirmação; status do `-runTests` atualizado |
| `skills/playbook/SKILL.md` | 90 | 91 | Gotcha 7 e linha de cobertura corrigidos (opções de CLI do Unity verificadas) |
| `skills/prompts/SKILL.md` | 90 | 90 | Gotcha de `-runTests` atualizado; nada mais a corrigir |
| Biblioteca de prompts (amostra de 15) | 91 | 91 | P-17 (nota de `-runTests`) atualizado; estrutura, variáveis, dados em tags, rótulos e limites de escrita já estavam corretos |
| `skills/game-verify-by-running/SKILL.md` | 87 | 91 | Linha do Unity: `-runTests -batchmode -projectPath -testPlatform -testResults` Verificados na doc do Test Framework 1.4 (antes "Não verificado, 404") |
| `skills/game-perf-audit/SKILL.md` | 90 | 90 | Sem alteração |
| `skills/game-qa-plan/SKILL.md` | 90 | 90 | Sem alteração |
| `skills/gdd-review/SKILL.md` | 88 | 91 | Tabela de vereditos e exemplo estavam em contradição (dependência inexistente aparecia em MAJOR e em NOT ASSESSED); alinhado a `rubrica-e-exemplos.md` e ao agente |
| `skills/godot-gdscript/SKILL.md` | 89 | 91 | Novo gotcha Verificado: sem `--check-only`, `-s` executa o script e exige `SceneTree` ou `MainLoop` |
| `skills/unity-csharp/SKILL.md` | 88 | 91 | `-runTests` Verificado; `FindObjectsByType` Verificado no 6000.0 (substituição de `FindObjectsOfType` segue Inferido) |
| `skills/unreal-cpp/SKILL.md` | 87 | 87 | Sem alteração; cobertura limitada pelas fontes (sem Blueprints, GAS, replicação), declarada |
| `skills/game-netcode-review/SKILL.md` | 91 | 91 | Sem alteração |
| `agents/game-engine-specialist.md` | 90 | 90 | Sem alteração |
| `agents/game-evaluator.md` | 90 | 90 | Gotcha de `-runTests` atualizado; `Bash` com contenção por instrução mantido e documentado |
| `agents/gameplay-programmer.md` | 91 | 91 | Sem alteração (grava só em `Caminhos autorizados`) |
| `agents/gameplay-reviewer.md` | 91 | 91 | Sem alteração (somente leitura) |
| `agents/gdd-reviewer.md` | 89 | 91 | Exemplo de Encaixe alinhado com a regra de NOT ASSESSED |
| `commands/verify.md` | 68 | 86 | Faltavam entrada vazia, política de permissão, formato de saída e proibição de instalar; adicionados |
| `commands/init-session.md` | 66 | 87 | Pedia `git log` com `allowed-tools` só de leitura de arquivos (inconsistente) e não tinha formato nem tratamento de dado externo; agora `Bash(git log:*)` e `Bash(git status:*)` pré-aprovados, passos, limites e saída definidos |
| `commands/playtest-report.md` | 70 | 86 | Entrada vazia, privacidade de participantes, separação bug x pain point e saída adicionadas |
| Evals (12 casos originais, depois 15) | 87 | 90 | 3 casos novos (ver seção 4); `evals/README.md` atualizado |

Média antes: 86,1. Média depois: 89,7. Menor nota depois: 86 (comandos). Nenhum item abaixo de 80. Nenhum critério de reprovação automática encontrado.

Resumo de D por grupo (depois): D1 e D6 fortes (descrições com gatilhos PT e EN, formatos de saída explícitos); D7 e D8 fortes (evidência colada, "não executei", revisores sem Write/Edit, conteúdo externo como dado); D9 o ponto mais fraco (playbook de 200 linhas com tabela de fronteiras de 26 plugins, parte deles ainda não publicados, e repetição de gotchas entre skills e references); D12 bom, com todas as incertezas rotuladas.

## 3. Fidelidade técnica

| Afirmação | Fonte consultada nesta validação | Resultado |
| --- | --- | --- |
| `-runTests`, `-testPlatform` (EditMode, PlayMode, BuildTarget; omitido roda Edit Mode), `-testResults` (XML NUnit), `-batchmode`, exemplo com `-projectPath` | https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/reference-command-line.html | Verificado. O plugin dizia "Não verificado (404)"; a URL antiga estava errada. Corrigido em 13 arquivos; nova linha V-21b em `fontes.md`. O comando continua não executado |
| Godot `--headless` = `--display-driver headless --audio-driver Dummy`; `--import` abre o editor, importa e sai; `--check-only` "com `--script`"; `--path` exige `project.godot` | https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html | Verificado. Novo: `-s` sem `--check-only` executa o script e exige herdar `SceneTree` ou `MainLoop`. A combinação `--headless` + `--check-only` segue Inferido |
| `TileMap` deprecated em favor de `TileMapLayer` | https://docs.godotengine.org/en/stable/classes/class_tilemap.html | Verificado ("Use multiple TileMapLayer nodes instead"). A página não diz a versão que depreciou: o plugin já tratava isso como não confirmado. A documentação `stable` lida está na série 4.7 |
| `FindObjectsByType` no Unity 6000.0 | ScriptReference 6000.0 | Existência Verificada; que substitui `FindObjectsOfType` não foi visto na página (segue Inferido) |
| Itens V-12 a V-21 do `VALIDATED.md` (move_and_slide e delta, NGO `HasAuthority`, 35% de folga em mobile, prefixos e lambdas da Epic, Gameplay Framework, custos US$ 9 e US$ 200) | Leitura do `VALIDATED.md`, comparada com o texto das skills | Coerente; os rótulos Inferido e Verificado batem com a fonte |
| Exemplos de código (Godot `Input.get_vector`, `@export`, `instantiate()`, NGO `[ServerRpc(RequireOwnership = false)]`, Unreal `CreateWeakLambda`) | Conhecimento estável das APIs, sem consulta online | Inferido; nada contradiz as páginas lidas |

Não conferido nesta validação: URL e data de cada linha de `fontes.md` (herdadas do `VALIDATED.md`), versão UE 5.8, números de estrelas de repositórios de terceiros, existência de `claude plugin eval` (o CLI local, 2.1.128, não o tem; o requisito 2.1.269 vem da fundação do projeto).

## 4. Componentes ausentes completados

- Evals novos (o `evals/README.md` listava essas lacunas):
  - `completo-auditoria-explicita`: keyword `GAMEDEV-COMPLETO` pedida pelo usuário, esperando matriz de aplicabilidade, áreas sem fonte validada rotuladas, auditoria somente leitura, resultado parcial por falta de arquivos; graders `criteria`, `skill-fired` (`playbook`), `no-write` (min 0, max 0).
  - `prompts-pedido-prompt-pronto`: pedido de prompt, não da tarefa; skill `prompts` dispara; variáveis ficam visíveis; sem diagnóstico inventado; graders `criteria`, `skill-fired`.
  - `en-unity-rpc-cheat`: disparo em inglês; ServerRpc com preço e dano do cliente e `RequireOwnership = false`; validação no Unity como boa prática (Inferido); graders `criteria` (em inglês, como o pedido), `skill-fired` (`game-netcode-review`).
- Casos negativos já existentes: `negativo-sql-ranking` (distante) e `near-miss-instalar-godot` (próximo), com `tool_used` `min: 0, max: 0`. Mantidos.
- Comandos: reescritos para ter entrada vazia, permissões coerentes, limites e saída.

## 5. Direitos autorais e segurança

- Nenhum trecho literal de terceiros encontrado nas partes lidas; README e `fontes.md` declaram destilação com redação própria e atribuição (MIT: Donchitos, godogen, GodotPrompter, GUT; Apache-2.0 na página: Unity-MCP; LGPL-3.0: só princípios).
- Sem segredos. Hooks e permissões aparecem apenas como JSON documentado e desativado em `ferramentas-e-mcp.md`, com riscos. `--dangerously-skip-permissions` só aparece como não recomendado, aceitável apenas em sandbox e repositório confiável.
- Revisores (`gameplay-reviewer`, `gdd-reviewer`, `game-engine-specialist`) com `Read, Glob, Grep`. `game-evaluator` tem `Bash` por necessidade (roda os comandos do contrato); a contenção é por instrução e por permissões padrão, o que o agente e o `ferramentas-e-mcp.md` declaram. `gameplay-programmer` grava só em `Caminhos autorizados`.
- Fluxos externos (commit, push, publicação, instalação, execução de script de init) exigem confirmação em todas as skills, agentes e comandos lidos.
- O fixture de prompt injection do eval `escopo-readme-injection` usa domínio reservado `example.invalid` e existe para ser ignorado; tratado como dado nesta revisão.
- Evals com PASS/FAIL observáveis: sim (graders `tool_used` determinísticos mais critérios `llm` em itens verificáveis). Os graders `no-write` e `no-exec` supõem que o runner casa o regex com o JSON da chamada; isso segue Não verificado.

## 6. Pendências

1. Executar `claude plugin eval` (Claude Code 2.1.269 ou superior) com 3 execuções por caso, ver se os graders `no-write` e `no-exec` detectam uma chamada proibida de teste e comparar com baseline sem plugin. Nada disso foi medido.
2. Rodar de verdade os comandos de engine (`--headless --import`, `--check-only` com `--headless`, GUT, `Unity.exe -runTests ...`) em projeto real; todos seguem não executados.
3. Revisão humana da família de modelos: validação feita por modelo Claude.
4. Revisar os 18 prompts da biblioteca e os 16 templates não lidos nesta rodada, e as references das skills de tarefa.
5. Candidatos a eval ainda sem caso: `game-evaluator` com e sem contrato, `gameplay-programmer` sem `Caminhos autorizados`, `/game-development:init-session`, GUT executando, projeto completo no modo `GAMEDEV-COMPLETO`.
6. Reduzir D9: avaliar mover a tabela de fronteiras do `playbook/SKILL.md` para uma referência e enxugar gotchas repetidos entre skills e references. Não feito para não reorganizar um arquivo estável sem medir o ganho.
7. Cobertura desigual declarada pelo próprio plugin (Unreal parcial; IA de jogo, assets, shaders, UI, publicação, ECS sem fonte); expandir só com fonte validada.

## 7. Verificações finais

```text
python tools/verify_plugin.py plugins/game-development  -> RESULT: PASS (10 skills, 5 agentes, 3 comandos, 15 evals, 114 arquivos)
claude plugin validate plugins/game-development          -> Validation passed
```
