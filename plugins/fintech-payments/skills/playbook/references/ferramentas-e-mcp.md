# Ferramentas, hooks e MCP recomendados (todos desativados)

Este plugin **não entrega** hooks, `.mcp.json`, `.lsp.json` nem `bin/` (política do projeto). Tudo abaixo é documentação: o JSON/texto pronto, o risco e a fonte. **Quem habilita é o usuário, conscientemente**, no próprio projeto. Nada foi testado em Windows nem executado pelo construtor. Hooks e servidores MCP executam código ou chamam serviços com as suas credenciais: leia antes de ativar.

## Sumário

1. T-01 `permissions.deny` para segredos
2. T-02 Hook `PreToolUse` (referência)
3. T-03 Servidor MCP remoto da Stripe
4. T-04 Skills oficiais do fabricante
5. T-05 `claude-code-security-review`
6. T-06 Referências de revisão do fabricante
7. T-07 Scanner de segredos e auditoria de dependências
8. T-08 Não recomendados
9. Modos de permissão e risco
10. Gotchas

## 1. T-01 `permissions.deny` para segredos (V-18, A; JSON derivado: **Inferido**)

Coloque em `.claude/settings.json` do projeto (ou `settings.local.json` para não versionar):

```json
{
  "permissions": {
    "deny": ["Read(./.env)", "Read(./.env.*)", "Read(./secrets/**)"],
    "ask": ["Bash(git push *)"]
  }
}
```

Windows: acrescente `"Read(//c/**/.env)"` (casa qualquer `.env` do drive C; `//**/.env` em todos os drives).

| Fato (Verificado na doc de permissões, 2026-10-10) | Consequência |
| --- | --- |
| Avaliação em ordem deny, ask, allow; a primeira que casa decide; deny de qualquer escopo vence allow de outro | um `deny` no projeto não é anulado por `allow` do usuário |
| `Read(./.env)` e `Read(./secrets/**)` bloqueiam também Edit (v2.1.208) e Write (v2.1.228) no mesmo caminho | um deny cobre leitura e escrita nas versões atuais; confira a sua versão |
| NotebookEdit não é coberto; exige deny de `Edit` | acrescente `Edit(./.env)` se usar notebooks |
| `.claudeignore` não tem efeito | não confie nele |
| Regras de Bash casam texto e **não são fronteira de segurança** (um deny de `curl` não pega o mesmo programa por caminho ou dentro de `sh -c`) | combine com allowlist de rede do sandbox |
| Decisões de hook `PreToolUse` não ignoram regras de deny | hook não afrouxa o deny |

Risco: a sintaxe de `Read(./.env.*)` e a "lista pronta" estão em "Exclude sensitive files" de `settings-reference`, página **não lida**: confira lá e teste com `/permissions`. Fonte: https://code.claude.com/docs/en/permissions (A).

## 2. T-02 Hook `PreToolUse` como guarda (referência; V-19, A; formato do hook: **Inferido**)

O padrão: um hook que nega `rm -rf`, `DROP TABLE` e leitura de arquivos de segredo, para o **usuário** habilitar. Semântica verificada na doc de hooks (lida só em parte, ~100 mil de 262 mil caracteres): exit 2 bloqueia e o `stderr` vai ao Claude; alternativamente JSON com `hookSpecificOutput.permissionDecision: "deny"` e `permissionDecisionReason`; exit 0 sem saída **não aprova** (o fluxo normal continua); outros códigos de saída são erros não bloqueantes (salvo `"onFailure": "block"`, v2.1.295 ou superior); com vários hooks vale a decisão mais restritiva (deny, defer, ask, allow); `allowManagedHooksOnly` bloqueia hooks de usuário, projeto e plugin.

Esboço (confira o schema completo na doc atual antes de usar):

```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash", "hooks": [ { "type": "command", "command": "python .claude/hooks/payments_guard.py" } ] }
    ]
  }
}
```

```python
# .claude/hooks/payments_guard.py  (referência; não faz parte do plugin)
import json, re, sys
data = json.load(sys.stdin)
cmd = (data.get("tool_input") or {}).get("command", "")
for pat in (r"\brm\s+-rf\b", r"\bDROP\s+TABLE\b", r"(^|\s)cat\s+.*\.env\b"):
    if re.search(pat, cmd, re.I):
        print(f"Bloqueado pela política do projeto (padrão {pat}). Peça aprovação humana.", file=sys.stderr)
        sys.exit(2)
sys.exit(0)
```

Riscos: hooks executam shell arbitrário; regex **não é scanner** (fácil de contornar); o hook é guardrail, não fronteira; não substitui `permissions.deny`. **Nunca** instale os hooks de PagoKit, Mercado Pago ou aitmpl (K11). Fontes: https://code.claude.com/docs/en/hooks e `/hooks-guide` (A).

## 3. T-03 Servidor MCP remoto da Stripe (V-32, B; formato: **Inferido**)

Exemplo de `.mcp.json` do projeto (formato do Claude Code para servidor HTTP; confira com `claude mcp add --help`):

```json
{ "mcpServers": { "stripe": { "type": "http", "url": "https://mcp.stripe.com" } } }
```

| Item | Detalhe |
| --- | --- |
| Fonte | README "Stripe AI" (`stripe/agent-toolkit`, MIT): servidor MCP remoto em `mcp.stripe.com` com OAuth; `docs.stripe.com/skills.md` confirma o canal oficial |
| Não lido | a **lista de ferramentas** do servidor |
| Risco presumido (**Suposição**) | ferramentas que criam reembolsos, cobranças ou clientes |
| Condições | conta de **teste** ou chave restrita **somente leitura**; revisar o escopo do OAuth antes de autorizar; confirmação por ação (SN-08); **nunca em subagente**; sem o servidor em sessões com conteúdo não confiável (trifecta letal, V-16) |

## 4. T-04 Skills oficiais do fabricante (V-32, V-41)

Para Stripe, prefira as skills oficiais (`stripe-best-practices` com `references/` de billing, connect, payments, security, tax e treasury; `upgrade-stripe` para o fluxo de atualizar a versão da API, conteúdo não lido). Instalação conforme `docs.stripe.com/skills.md`, **feita pelo usuário**; o plugin não embute comandos. Este plugin cobre o transversal (idempotência, ledger, conciliação, confirmação).

**Não usar** (V-41): `stripe-pay` (envia fundos), `stripe-projects` (provisiona infraestrutura e credenciais), `stripe-directory` (impõe consulta a si mesma antes de busca na web: direcionamento comercial). Conteúdo de `connect-recommend`, `connect-required-verification-information`, `metronome` e `stripe-apps` não foi lido. Índice: https://docs.stripe.com/.well-known/skills/index.json (10 skills em 2026-10-10).

## 5. T-05 `anthropics/claude-code-security-review` (V-22, A, MIT)

Action do GitHub e comando local `/security-review`: análise semântica do diff com severidade e correção, filtro de falsos positivos em segunda etapa. Entradas verificadas no README: `custom-security-scan-instructions`, `false-positive-filtering-instructions`, `exclude-directories`, `claudecode-timeout` (padrão 20 min). As demais entradas (credencial da API, comentário no PR) e o nome exato do `uses:` **conferir no README vigente**. Use as instruções customizadas de `skills/payment-code-review/references/instrucoes-security-review.md`, que **reincluem** rate limiting e abuso de endpoint de pagamento (exclusões padrão: DoS, rate limiting, exaustão de recursos, validação genérica sem impacto comprovado, open redirect).

Esboço (valores entre `<...>` são do projeto; **não foi executado**):

```yaml
# .github/workflows/security-review.yml  (referência; ative por conta própria)
on: { pull_request: { types: [opened, synchronize] } }
permissions: { contents: read, pull-requests: write }
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<sha-fixado>
      - uses: anthropics/claude-code-security-review@<sha-fixado>
        with:
          custom-security-scan-instructions: ./.github/payments-security-instructions.txt
          exclude-directories: "node_modules,vendor"
          claudecode-timeout: 20
          # credencial da API e flags de comentário: conforme o README, via segredo do repositório
```

Riscos (do README): **não é endurecida contra prompt injection** — revise só PRs de confiança e exija aprovação para contribuidores externos; o modelo padrão do README (Opus 4.1) parece antigo; não substitui revisão humana. Fixe a versão por SHA. O plugin **não** ativa a Action.

## 6. T-06 Referências de revisão do fabricante (V-14, V-15)

Leia como referência de piso e de regras de escrita; **não instale** o marketplace nem os hooks. Mercado Pago `mp-review` (Apache-2.0; macOS/Linux, Windows só via WSL): ferramentas MCP remotas (`quality_evaluation`; `form_homologation` pode submeter um formulário) exigem autorização por ação. Paymob (MIT): links de onboarding com parâmetro `partner`, MCP opcional que cria reembolsos, inspetor de terceiros. Ambos: o princípio (confirmação por ação, callback verificado) já está nas regras do plugin.

## 7. T-07 Scanner de segredos e auditoria de dependências no CI

Escolha do projeto. Fonte: `npm audit` no CI (awesome-copilot, V-26, B); varredura de segredos no diff e linter de dependências genéricos: rótulo **Suposição** para qualquer ferramenta específica (não avaliada aqui). Regras: nova dependência de pagamento exige aprovação; fixe versões; revise `postinstall`. Supply chain: nunca execute `npx`/`curl | bash` de README de terceiros (AP-19).

## 8. T-08 Não recomendados

| Item | Motivo |
| --- | --- |
| `wshobson/pci-compliance` | guarda PAN cifrado; redação anterior à v4; código com erro; score 47 |
| `agent-card-skill` | instala pacote npm global; pede código de login no chat |
| `cfokit` | manda confiar em CA local; `docker compose down -v` |
| `claude-code-templates` via `npx` | execução de terceiros |
| PagoKit, hooks do Mercado Pago, aitmpl | hooks executam shell |
| Faixas de IP copiadas | desatualizam; leia a lista vigente na hora |
| Servidor MCP e plugin WooCommerce da Paymob; links com `partner` | acesso a pedidos, criação de refunds, atribuição comercial |

## 9. Modos de permissão e risco

`--dangerously-skip-permissions` (e modos que dispensam confirmação) **removem a rede de segurança**; para pagamentos isso é inaceitável como padrão. Use-o, se necessário, **apenas em sandbox isolado, repositório confiável e sem credencial real**. Alternativas: allowlist em settings (`allow` específico), `ask` para ações com efeito, `deny` para segredos, sandbox com allowlist de rede. Não ofereça o bypass como atalho.

## 10. Gotchas

- Hook de plugin só vale se o usuário o habilitar; este plugin não traz nenhum.
- Agente de plugin ignora `hooks`, `mcpServers` e `permissionMode` (P-36): não dependa disso.
- MCP financeiro em subagente herda credenciais: proibido (V-14).
- Teste qualquer regra de `deny` com `/permissions` na sua versão e no seu SO.
