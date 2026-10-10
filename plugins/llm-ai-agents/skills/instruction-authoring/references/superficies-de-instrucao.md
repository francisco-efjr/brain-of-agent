# Onde colocar cada instrução no Claude Code

Base: V-40 (documentação de skills, comandos, hooks e plugins, mais o post oficial de 18/06/2026 sobre os sete métodos de instrução), V-21 (memória), V-19 (subagentes). Conferido em 2026-10-10 na versão documentada na época; campos e eventos mudam: confirme em https://code.claude.com/docs/en/hooks e https://code.claude.com/docs/en/skills antes de gravar configuração.

## Árvore de decisão

| Pergunta | Se sim | Custo de contexto |
| --- | --- | --- |
| Isto precisa acontecer sempre, sem depender do julgamento do modelo? | Hook (determinístico) ou permissão | Baixo |
| É um fato do projeto que vale em toda sessão (comando de build, convenção que diverge do padrão, armadilha)? | CLAUDE.md curto (raiz abaixo de 200 linhas) | Em toda sessão |
| Só vale ao mexer numa área do repositório? | Regra em `.claude/rules/` com escopo de caminho | Só quando a área é tocada |
| É um procedimento que o modelo escolhe usar quando o caso aparece? | Skill, com gatilho na `description` | Nome e descrição sempre; corpo na invocação |
| É uma tarefa lateral que encheria o contexto principal (pesquisa, revisão, leitura volumosa)? | Subagente (devolve resumo) | Isolado |
| É uma ação com efeito colateral que o usuário dispara (deploy, envio, migração)? | Skill ou comando com `disable-model-invocation: true` | Só na invocação |

Outras superfícies do post oficial (V-40): estilos de saída (substituem o prompt de sistema padrão e podem perder instruções de engenharia; usar com parcimônia) e acréscimo ao prompt de sistema por flag. Essas duas vêm só do post, não da documentação lida: **Não verificado** na documentação.

## Regras de bolso

- Para limites rígidos, hooks e permissões superam o CLAUDE.md (V-40).
- Instrução em duas superfícies diverge com o tempo: decida um dono por regra.
- Regra que se aplica a 1 de cada 10 sessões é skill ou regra com caminho, não CLAUDE.md.
- Memória automática carrega as primeiras 200 linhas ou 25 KB; confirme com `/memory` ou `/context` o que de fato foi carregado (V-21).

## Hooks: fatos úteis para decidir (V-40, Verificado em texto da documentação)

| Fato | Detalhe |
| --- | --- |
| Quantidade de eventos | 33 listados na referência (SessionStart, UserPromptSubmit, PreToolUse, PermissionRequest, PostToolUse, Stop, SubagentStop, PreCompact, entre outros) |
| Exit code 2 bloqueia | PreToolUse, UserPromptSubmit, UserPromptExpansion, Stop, SubagentStop, TeammateIdle, TaskCreated, TaskCompleted, ConfigChange (exceto `policy_settings`), PreCompact, PreModelSwitch, Elicitation, ElicitationResult, WorktreeCreate, WorktreeRemove, PostToolBatch |
| Exit code 2 não bloqueia | PostToolUse, PostToolUseFailure, PermissionDenied, Notification e outros; em PermissionRequest não é respeitado (negar pelo objeto `decision`) |
| Outros códigos de saída | Erro não bloqueante |
| Falha de hook bloqueante | `onFailure: "block"` faz a falha bloquear a ação, em hooks `command` e `http`, a partir da versão 2.1.295 |
| Negação robusta | `PreToolUse` com `permissionDecision: "deny"` bloqueia até em `bypassPermissions` |
| Segurança | O que o hook executa roda com as permissões do usuário: não é fronteira de segurança |

Limite do que foi lido: a referência de hooks tem cerca de 262 mil caracteres e só os primeiros 100 mil foram lidos; os schemas de entrada/saída por evento **não** foram lidos. O único hook pronto do plugin é o exemplo desativado de `PreToolUse` em `${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/ferramentas-e-mcp.md`, conferido no guia de hooks. Para outro evento, leia a página do evento na versão instalada e registre o trecho usado.

## Exemplos de classificação

| Regra do usuário | Superfície | Motivo |
| --- | --- | --- |
| "Nunca fazer commit de `.env`" | Hook PreToolUse (e `.gitignore`) | Precisa valer sempre; frase em CLAUDE.md é só pedido |
| "Rode `npm test -- --run` antes de encerrar" | CLAUDE.md (1 linha) | Fato de fluxo em toda sessão |
| "Formatar com 2 espaços" | Linter/formatter + hook opcional | Código já decide; texto vira ruído |
| "Como fazer migração de schema do módulo billing" | Regra com escopo `billing/**` ou skill | Só vale em uma área |
| "Revisar PR de segurança" | Skill + subagente revisor somente leitura | Procedimento sob demanda; contexto isolado |
| "Publicar release" | Skill com `disable-model-invocation: true` | Efeito externo; só por comando explícito |

## Conflitos de nome e precedência (V-40)

Skills: enterprise > pessoal > projeto; skill > arquivo de comando; skills de plugin têm prefixo `/plugin:skill`. Subagentes: configuração gerenciada, flag `--agents`, `.claude/agents/`, `~/.claude/agents/`, plugin (menor precedência) (V-19). Comandos e skills foram unificados: `.claude/commands/x.md` e `.claude/skills/x/SKILL.md` criam `/x`; a documentação recomenda skill para trabalho novo.
