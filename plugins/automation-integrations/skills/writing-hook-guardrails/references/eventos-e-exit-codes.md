# Hooks: eventos, exit codes, matcher e saída estruturada

Fonte: referência oficial de hooks (https://code.claude.com/docs/en/hooks), lida só em parte pelo validador (cerca de 38% dos 262 mil caracteres; V-02). O que está marcado Verificado foi conferido em 2026-10-10 em `VALIDATED.md`; o que está marcado Inferido é conhecimento estável do formato, não relido nesta rodada. A doc oficial prevalece sobre blogs: um blog de apoio citava 27 eventos e a doc lista 33 (C-02), então **confira a lista contra a versão instalada** em vez de decorar um número. Redação própria.

Sumário: 1. Exit codes por evento · 2. Matcher · 3. Saída estruturada do PreToolUse · 4. Entrada (stdin) · 5. onFailure · 6. Hooks em plugin · 7. Lacunas.

## 1. Exit codes (Verificado, V-02)

| Código | Efeito |
| --- | --- |
| 0 | sucesso; stdout pode conter JSON de decisão |
| 2 | **bloqueia** nos eventos bloqueáveis abaixo; stderr volta ao modelo como motivo |
| qualquer outro (inclusive 1) | erro **não bloqueante**: a ação segue |

| Eventos em que exit 2 bloqueia | Eventos em que não bloqueia |
| --- | --- |
| `PreToolUse`, `UserPromptSubmit`, `UserPromptExpansion`, `Stop`, `SubagentStop`, `TeammateIdle`, `TaskCreated`, `TaskCompleted`, `ConfigChange` (exceto `policy_settings`), `PreCompact`, `PreModelSwitch`, `Elicitation`, `ElicitationResult`, `PostToolBatch`, `WorktreeCreate`, `WorktreeRemove` | `PostToolUse`, `PostToolUseFailure`, `PermissionDenied`, `Notification`, `SessionStart` |

`PermissionRequest`: o exit 2 não é honrado; use o objeto `decision` na saída (V-02). Para impedir uma ferramenta antes de rodar, o evento é `PreToolUse`; `PostToolUse` roda depois e não desfaz nada.

## 2. Matcher (Verificado, V-02)

- `*`, vazio ou ausente: todas as ocorrências do evento.
- Só letras, dígitos, `_`, `-`, espaço, vírgula e barra vertical: lista exata de nomes, por exemplo `Bash` ou `Edit|Write`.
- Qualquer outro caractere: regex JavaScript **não ancorada**.
- MCP: `mcp__servidor__.*`; `mcp__servidor` sozinho **não casa**.

Como o regex não é ancorado, `Bash.*` e `Bash` têm efeitos diferentes conforme a forma; prefira lista exata quando possível e teste.

## 3. Saída estruturada do PreToolUse (Verificado em V-02; forma exata Inferida)

Quando quiser pedir confirmação em vez de negar:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "ask",
    "permissionDecisionReason": "git push --force detectado. Confirme o branch e use --force-with-lease."
  }
}
```

`permissionDecision`: `allow`, `deny`, `ask`, `defer` (V-02). O JSON vai no stdout com exit 0. Qualquer texto extra no stdout (mensagem do perfil do shell, `print` de depuração) pode quebrar o parse e a decisão se perde.

Escolha: bloqueio absoluto (dano irrecuperável) com exit 2 ou `deny`; "cuidado" (reversível mas arriscado) com `ask`; aviso informativo sem bloqueio com exit 0 e mensagem em `additionalContext` (campo Inferido; confirme).

## 4. Entrada (stdin) — Inferido, conhecimento estável; confirme na sua versão

JSON com campos como `session_id`, `cwd`, `hook_event_name`, `tool_name` e `tool_input` (para `Bash`, `tool_input.command`; para `Edit`/`Write`, `tool_input.file_path`). Em subagentes, `agent_id` e `agent_type` estão presentes (Verificado, V-02: hooks de settings, de política gerenciada e de plugins também rodam dentro de subagentes). Inspecione um evento real gravando o stdin em arquivo num hook de teste (em ambiente descartável) antes de assumir nomes de campo.

## 5. `onFailure` (Verificado, V-02)

- `"onFailure": "block"` (v2.1.295 ou superior; padrão `continue`): falha, timeout ou saída inválida do hook **bloqueiam** a ação.
- Não vale para `Stop`, `SubagentStop`, `TaskCompleted`, `TeammateIdle` nem para hooks assíncronos.
- Use em regras de segurança (falha aberta é o pior modo de um guardrail); evite em hooks de conveniência (formatador), que travariam o fluxo.

## 6. Hooks em plugin (Verificado, V-02/V-01)

- `hooks/hooks.json` do plugin tem o invólucro `"hooks"` no topo.
- `${CLAUDE_PLUGIN_ROOT}` vale em `command` e `args`; a forma exec com `args` é a recomendada.
- `${user_config.*}` não vale em hook de shell: use `args` ou a variável `CLAUDE_PLUGIN_OPTION_<KEY>`.
- Dados persistentes em `${CLAUDE_PLUGIN_DATA}` (sobrevive a atualizações), não em `${CLAUDE_PLUGIN_ROOT}`.
- Política deste marketplace: plugins **não** trazem `hooks/hooks.json` ativo; o hook é documentado e o usuário o instala.
- Hook "sob demanda" via frontmatter de skill (`hooks`) vale da invocação da skill até o fim da sessão (V-05).

## 7. Lacunas declaradas

Schemas dos eventos finais (`SubagentStop`, `WorktreeCreate`, `PermissionRequest`), tipos de hook `http`, `mcp_tool` e `prompt`, e a contagem oficial de eventos não foram lidos (V-02, lacuna 4). Para qualquer um deles, leia a seção correspondente da doc na sua versão e rotule Não verificado até testar.
