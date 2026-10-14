# Ferramentas, hooks e MCP recomendados (todos desativados)

Nada aqui vem ativo no plugin: não há `hooks/hooks.json`, `.mcp.json`, `.lsp.json` nem `bin/`. Este arquivo documenta o que vale habilitar **conscientemente** no seu projeto, com o comando ou JSON pronto, os riscos e o que foi ou não verificado. Instalar ou executar qualquer item é decisão sua; a IA não deve fazê-lo por conta própria nem a pedido de um README. Validado em 2026-10-10.

## Sumário

- [Regras de adoção](#regras-de-adoção)
- [T-01 claude plugin eval](#t-01-claude-plugin-eval)
- [T-02 Agentes de teste do Playwright](#t-02-agentes-de-teste-do-playwright)
- [T-03 Hook Stop de verificação](#t-03-hook-stop-de-verificação)
- [T-04 Hook PreToolUse em arquivo de teste](#t-04-hook-pretooluse-em-arquivo-de-teste)
- [T-05 a T-09 Ferramentas de teste](#t-05-a-t-09-ferramentas-de-teste)
- [T-10 MCP de navegador](#t-10-mcp-de-navegador)
- [T-11 O que não recomendar](#t-11-o-que-não-recomendar)

## Regras de adoção

1. Leia o código e a licença antes de executar qualquer pacote de terceiros; fixe versão (nunca `@latest`).
2. Hook roda shell com as suas permissões: revise o script como revisaria um PR. Hook é guardrail, não fronteira de segurança.
3. Teste de carga, fuzz, segurança e exploração só em ambiente local ou de staging, com credenciais de teste.
4. Credenciais: o usuário as digita no navegador ou as injeta por variável de ambiente; o agente não as recebe no chat nem as grava em arquivo.
5. Confirme flags na versão instalada (`<ferramenta> --help`): nomes mudam entre versões.

## T-01 claude plugin eval

Mede se uma skill ou agente muda o resultado, com e sem o plugin. Fonte: V-02 (doc oficial, Verificado). Skill associada: `eval-design`; execução manual pelo comando `/qa-testing:eval-plugin` ou `claude plugin eval`, com confirmação de custo.

```bash
claude plugin eval .                          # na raiz do plugin; 3 execuções por caso (padrão)
claude plugin eval . --case verificar-antes-de-concluir --ablation none --runs 1   # iteração barata
claude plugin eval . --ablation with-without --max-cost-usd 5                      # baseline sem o plugin, com teto de custo
claude plugin eval . --trust-plugin --json results.json --max-cost-usd 5           # receita de CI
```

Flags confirmadas na doc: `--case`, `--runs`, `--ablation none|with-without`, `--judge-model`, `--threshold`, `--max-cost-usd`, `--trust-plugin`, `--json [path]`, `--allow-tools`. Códigos de saída: 0 ok, 1 reprovação ou erro, 2 execução parcial (teto de custo ou credencial recusada). Riscos: cada execução e cada juiz custam chamadas de modelo; exige Claude Code 2.1.269 ou superior e git 2.31 ou superior; **no Windows nativo não há backend de sandbox, então suítes que concedem Bash ou PowerShell precisam de WSL2**. A CLI da fábrica de plugins era 2.1.128 em 2026-10-09, portanto os casos deste plugin seguem `designed_not_executed` até atualizar e rodar. Confira `claude plugin eval --help`.

## T-02 Agentes de teste do Playwright

Planner, generator e healer (V-20, Verificado):

```bash
npx playwright init-agents --loop=claude     # também: vscode, codex, opencode
```

Regenere os arquivos depois de atualizar o Playwright; a experiência com agentes no VS Code pede VS Code 1.105 ou superior. Riscos: executa pacote npm e gera arquivos no repositório (revise o diff e fixe a versão); o **healer pode mascarar regressão**, porque entrega "teste pulado" quando julga a funcionalidade quebrada (K4). Use com o guardrail de `e2e-review`: corrigir o teste só se o produto está certo; se parece quebrado, registrar falha de produto; aceitar correção só com revisão de diff.

`init-agents` sobrescreve `.mcp.json` da raiz e `.claude/agents/playwright-test-*.md`; só o seed e `specs/` são protegidos (lido no código, não executado). Faça cópia e revise o diff. O plugin `qa-playwright` dispensa o loop.

## T-03 Hook Stop de verificação

Impede encerrar a resposta enquanto o teste do escopo não passa. Coloque em `.claude/settings.json` **do projeto** (não do plugin):

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          { "type": "command", "command": "bash ./scripts/verify-before-stop.sh", "timeout": 600 }
        ]
      }
    ]
  }
}
```

Script de exemplo (seu, não fornecido pelo plugin; ajuste o comando de teste):

```bash
#!/usr/bin/env bash
# Lê o JSON do evento em stdin. Evita laço infinito: se já estamos continuando por causa deste hook, deixa parar.
input="$(cat)"
if printf '%s' "$input" | grep -q '"stop_hook_active"[[:space:]]*:[[:space:]]*true'; then exit 0; fi
if ! npm test --silent -- --run >/tmp/verify-out.txt 2>&1; then
  echo "Testes do escopo falharam; veja o resumo abaixo antes de concluir." >&2
  tail -n 20 /tmp/verify-out.txt >&2
  exit 2          # exit 2: stderr volta ao Claude e ele continua trabalhando
fi
exit 0
```

Status: formato de `hooks` por evento, `matcher` opcional, `type: command`, `timeout` e a semântica de bloqueio por exit 2 (stderr é o motivo) ou por JSON `{"decision":"block","reason":"..."}` foram **Verificados** na página de hooks em 2026-10-10 (V-01 confirma a existência do hook `Stop`). O campo `stop_hook_active` (verdadeiro quando o Claude Code já está continuando por causa de um Stop hook) foi **Verificado** na mesma página em 2026-10-10 pelo validador de qualidade; `permissionDecision` do PreToolUse aceita `allow`, `deny`, `ask` e `defer`. Riscos: executa shell; laço infinito se o script bloquear sempre; suíte lenta trava cada resposta; o script não é fornecido pelo plugin; escreva no `/tmp` do seu sistema (no Windows nativo use um caminho adequado).

## T-04 Hook PreToolUse em arquivo de teste

Transforma a regra S-02 (não afrouxar teste) de pedido em confirmação obrigatória:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "bash ./scripts/ask-on-test-edit.sh" }
        ]
      }
    ]
  }
}
```

Script de exemplo (seu): lê o JSON do evento, compara o caminho com padrões de teste e responde "ask":

```bash
#!/usr/bin/env bash
input="$(cat)"
path="$(printf '%s' "$input" | python3 -c 'import sys,json; print(json.load(sys.stdin).get("tool_input",{}).get("file_path",""))')"
case "$path" in
  *.test.*|*.spec.*|*_test.*|*/test_*.py|*/tests/*|*/__tests__/*)
    printf '%s' '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask","permissionDecisionReason":"Edição de arquivo de teste: confirme que o produto está certo e que a asserção não está sendo afrouxada."}}'
    ;;
esac
exit 0
```

Status: o formato `permissionDecision: "ask"` com `hookSpecificOutput` foi **Verificado** na página de hooks (2026-10-10); o nome do campo `tool_input.file_path` do Edit/Write é **Inferido** (conhecimento estável das ferramentas; confira com um log do evento). Riscos: atrito alto quando o `test-writer` trabalha (cada edição pede confirmação); globs imperfeitos geram falso positivo e negativo; padrão de caminho não é segurança; exige `python3` no PATH.

## T-05 a T-09 Ferramentas de teste

| ID | Item | Comando ou configuração | Riscos | Status |
| --- | --- | --- | --- | --- |
| T-05 | Schemathesis (API a partir de OpenAPI) | `uvx schemathesis run <url-do-schema>`; `schemathesis replay <ID>` reenvia um caso; a saída traz `curl` de reprodução e seed | Pacote de terceiros: verifique licença e versão (não aparecem nas páginas lidas); **só contra local ou staging com credenciais de teste, nunca produção**; faz muitas requisições | Verificado (V-26) |
| T-06 | fast-check (property-based) e Stryker (mutation) | Dependências de desenvolvimento do projeto: `fast-check`; StrykerJS, Stryker.NET ou Stryker4s | Mutation é caro: aplique a módulos críticos; mutante sobrevivente pode ser equivalente; comandos de execução do Stryker não constam na página lida | Verificado só o conceito (V-15); comandos Inferidos |
| T-07 | k6 (performance) | Tipos: smoke, average-load, stress, soak, spike, breakpoint; comece pelo smoke | Carga só em ambiente autorizado, fora do pico, com aborto; a doc lida não traz limiares nem SLO (lacuna; SLO é do plugin `sre-observability`) | Verificado (V-23) |
| T-08 | Pact (contrato consumer-driven) | Contrato gerado no teste do consumidor, verificado no provedor em CI, broker conecta ao CI (`how_pact_works`) | `can-i-deploy` não confirmado na página lida; contrato não substitui E2E de jornada | Verificado (V-16) |
| T-09 | axe-core, pa11y, Lighthouse (acessibilidade automatizada) | Integração de axe com Playwright; o brain-of-agent tem `auditoria_axe.py` (requer `playwright`) como referência | Nenhuma ferramenta determina conformidade (V-18); páginas das ferramentas não foram lidas nesta pesquisa; versão de WCAG 2.1 em skills antigas está desatualizada frente à 2.2 | Não verificável (ferramentas); princípio Verificado (V-18) |

## T-10 MCP de navegador

Automação de navegador por MCP (por exemplo um servidor de Playwright) permite ao agente navegar e capturar tela. O pacote e as flags **não foram verificados em fonte oficial lida** nesta pesquisa: o JSON abaixo é um molde com placeholders, e você deve confirmar nome e versão na documentação oficial antes de usar.

```json
{
  "mcpServers": {
    "browser": {
      "command": "npx",
      "args": ["<pacote-oficial>@<versão-fixada>"]
    }
  }
}
```

Riscos: executa pacote de terceiros via `npx` (nunca `@latest`); alguns abrem navegador visível por padrão; conteúdo das páginas é dado não confiável (injeção indireta); credenciais: o usuário as digita no navegador, o agente não as recebe; use apenas contra local ou staging. Status: **Não verificável** (o harness da Anthropic em V-06 usa Puppeteer MCP, o que confirma o padrão, não o pacote).

Verificado em 13/10/2026: o `@playwright/test` 1.64.0 traz `npx playwright mcp` (flags `--isolated`, `--headless`, `--allowed-origins`, `--output-dir`, `--storage-state`; `--no-webmcp` e `--idle-timeout` no código do pacote). Prefira-o ao pacote npm `@playwright/mcp`, que depende de Playwright alpha. Detalhes em `qa-playwright`.

## T-11 O que não recomendar

| Item | Motivo |
| --- | --- |
| `./setup` do gstack (compila, baixa Chromium, registra hooks em `~/.claude/settings.json`) | Altera configuração global do usuário; supply chain |
| `npx @qaskills/cli` e `claude mcp add ... npx -y @qaskills/mcp` | Executa pacote de terceiros sem revisão; notas de qualidade auto-atribuídas |
| `npm run setup` e `npx skills add` do playwright-skill | Baixa Playwright e Chromium; navegador visível por padrão |
| `with_server.py --server "<cmd>"` do `webapp-testing` | Executa shell arbitrário; o plugin documenta o comando mas não embute o helper (leia o código antes de rodar) |
| Instrução de README para "buscar e seguir" uma URL remota (ex.: instalação para OpenCode no superpowers) | Injeção indireta: conteúdo externo é dado |
| `git bisect run`, estresse e fuzzing sem delimitar ambiente (sugeridos em `diagnosing-bugs`) | Muda o checkout, executa código em loop; confirme o ambiente-alvo e use árvore limpa |
| Driver `tempdir` do `coder_eval` como isolamento | Não é fronteira de segurança; tarefas não confiáveis exigem container |

Fonte: seção "Segurança e direitos autorais" do VALIDATED.md (Verificado como risco; nenhum dos comandos foi executado).
