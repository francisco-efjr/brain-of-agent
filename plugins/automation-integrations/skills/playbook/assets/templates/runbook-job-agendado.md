# Runbook de job agendado (`claude -p` e agendadores)

Fonte: V-32 (execução não interativa), V-25 (claude-code-action), G-01..G-06 (Inferido). Confirme cada flag em `claude --help` e `claude --version` (as flags variam de v2.1.246 a v2.1.295). Este runbook **documenta**; criar cron, workflow, Action ou secret é ação do usuário.

## 1. Identificação

| Campo | Valor |
| --- | --- |
| Job / dono / canal de alerta | |
| Tarefa em uma frase | |
| Onde roda (cron local · CI · GitHub Action) e frequência (UTC) | |
| Versão mínima do Claude Code | |
| Entradas externas e quem as controla | |
| Saídas e efeitos externos (Slack, e-mail, issue, commit) | |
| Trifecta (R-01..R-03) e perna quebrada | |

## 2. Comando

```bash
claude -p "$PROMPT" \
  --bare \
  --allowedTools "[LISTA-MINIMA]" \
  --permission-mode dontAsk \
  --max-budget-usd [TETO] \
  --output-format json \
  --json-schema '[SCHEMA-JSON]' > resultado.json
echo "exit=$?"
```

| Flag | Razão | Item |
| --- | --- | --- |
| `--bare` | Sem ele, `-p` roda hooks e MCP do projeto sem prompt de confiança | J-01 |
| `--allowedTools` | Lista mínima; espaço antes do `*` importa | J-02 |
| `--permission-mode dontAsk` ou `--permission-prompts none` (v2.1.259+) | Ninguém para responder; nega o que pediria prompt | J-03 |
| `--max-budget-usd` | Teto de custo por execução | J-04 |
| `--output-format json` + `--json-schema` | Saída estruturada validável; `format` do schema é só anotação | J-05 |

## 3. Gate pós-execução

- [ ] `exit` = 0 (SIGTERM → 143, sem resultado do turno)
- [ ] `plugin_errors` e `mcp_server_errors` do evento `system/init` vazios (J-06; nomes e formato de saída que expõe o evento: conferir na doc headless)
- [ ] JSON válido contra o schema
- [ ] Só então executar efeitos externos (passo separado, credencial mínima, aprovação humana enquanto não houver confiança)

## 4. Segurança

- Entrada externa dentro de `<dados>`; o prompt manda tratar como dado e listar tentativas de injeção (J-07).
- Segredos só em variável de ambiente / secrets do runner (J-08). Entrada por pipe até 10 MB.
- GitHub Action: gatilho restrito, prompt com escopo explícito, saída JSON validada, token com permissões mínimas, humano antes do merge. Configuração: `docs/usage.md` da action na versão usada.

## 5. Operação

| Item | Decisão |
| --- | --- |
| Trava contra sobreposição (G-01) | |
| Execuções perdidas: recuperar ou pular (G-03) | |
| Idempotência por janela (G-04) | |
| Heartbeat / alerta de ausência (G-05) | |
| Teste inicial (dry-run local com teto baixo, feito pelo usuário) | |
| Como desativar (G-06) e limpar secrets | |

## 6. Verificação e rótulos

Execução real: [colar comando, saída e exit code] ou **Não verificado** (motivo). Leitura da configuração ≠ job executado.
