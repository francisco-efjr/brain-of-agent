# Ferramentas, servidores MCP e hooks recomendados (todos DESATIVADOS)

Nada neste arquivo é instalado, executado ou ativado pelo plugin: este plugin não distribui `hooks/`, `.mcp.json`, `.lsp.json` nem `bin/` (política da casa; um servidor MCP de plugin sobe sozinho ao habilitar o plugin, V-15). Aqui estão recomendações para **você** habilitar conscientemente, com JSON pronto, riscos e fonte. Versões ficam como `<VERSÃO-FIXADA>`: preencha **depois de ler o código** (A-01..A-08). Nomes de pacote e flags não observados nas fontes levam o rótulo Inferido.

Sumário: 1. Antes de habilitar qualquer coisa · 2. Catálogo · 3. `.mcp.json` documentado · 4. Comandos de CLI (Inferido) · 5. Hook documentado · 6. Permissões e settings de endurecimento · 7. Job headless · 8. Como desativar

## 1. Antes de habilitar qualquer coisa

1. Ler o SKILL.md/README, os scripts e as dependências (A-01, A-02); procurar rede, credenciais e instruções dirigidas à IA (A-03).
2. Fixar tag ou SHA; nunca `@latest`, `--yes` ou `curl | bash` (A-06).
3. Registrar licença e atribuição (A-07).
4. Testar em diretório/VM descartável, com credenciais de teste (A-05).
5. Saber como desativar **antes** de ativar (seção 8).
6. Conferir a trifecta da **combinação** de servidores que você terá ativos (R-06).

## 2. Catálogo

| Item | Licença / fonte | Para quê | Riscos principais | Status da evidência |
| --- | --- | --- | --- | --- |
| MCP Inspector | citado em V-12; repositório e licença **não verificados** | Testar cada tool antes de conectar a um cliente | Executa o servidor sob teste; use versão fixada, leia antes, ambiente descartável | Pacote `@modelcontextprotocol/inspector`: **Inferido** |
| Servidores de referência MCP (Fetch, Filesystem, Git, Memory, Time, Everything, Sequential Thinking) | Apache-2.0 (novos) / MIT (antigos), V-17 | Estudo de escopo mínimo e allowlist; Filesystem com diretórios permitidos | "Não prontos para produção"; Fetch traz conteúdo externo (injeção, perna 2); GitHub/PostgreSQL arquivados; Slack mantido por terceiro | Verificado (README) |
| `plugin-dev`, `mcp-server-dev`, `hookify`, `security-guidance`, `skill-creator`, `ralph-loop` | `claude-plugins-official` Apache-2.0; README do `plugin-dev` MIT (V-13) | Estudo e uso opcional; `hookify` cria regras `event/pattern/action` | Plugins instalam hooks, MCP e scripts: ler antes (A-xx); arquivos internos não lidos; loops por hook `Stop` sem sandbox geram custo | Verificado (árvore e READMEs) |
| claude-code-action | MIT (V-25) | Automação no GitHub (menção `@claude`, issue atribuída, `prompt` explícito) | Token e secrets; acionamento por texto de issue/PR (injeção); `docs/usage.md` e `docs/security.md` não lidos | Verificado (README); YAML **não** fornecido aqui |
| cc-safety-net (`kenryu42/claude-code-safety-net`) | MIT (V-24) | Inspiração e opção de hook de bloqueio (inclui `bash -c`/`python -c`) | Instalação recomendada usa `@latest` (não use); não é sandbox; falha aberta em configuração quebrada (Não reconferido) | Verificado (README); código não lido |
| gstack `/careful`, `/freeze`, `/guard` | MIT, Copyright (c) 2026 Garry Tan (V-29) | Padrão de skill com hook sob demanda | Escopo amplo (planejamento, design, QA); instalador `./setup` (Bun) não executar sem ler | Verificado (README) |
| ruler (`.ruler/`, `ruler.toml`) | MIT (V-28) | Fonte única de regras quando há mais de uma ferramenta | `ruler apply` sobrescreve arquivos; supply chain (`ruler revert` não cobre subagentes) | Verificado (README) |
| Trail of Bits `claude-code-config` | licença nula na API (V-21) | Leitura de baseline de endurecimento | Não copiar template | Verificado na página; exemplos não validados contra o schema atual de hooks |
| n8n (Error Trigger e afins) | Sustainable Use License (V-31) | Usar o produto conforme a licença | **Não** embutir texto/código; docs de fornecedor | Verificado (licença) |

## 3. `.mcp.json` documentado (você escreve, depois de ler o servidor)

Sem `-y`, sem `@latest`, segredos por `${VAR}`. Servidor de projeto exige aprovação em sessão interativa e **carrega sem perguntar em `-p`** (V-15).

```json
{
  "mcpServers": {
    "filesystem-leitura": {
      "command": "node",
      "args": ["<CAMINHO-DO-ENTRYPOINT-INSTALADO-E-REVISADO>", "<DIRETÓRIO-PERMITIDO>"],
      "env": {}
    },
    "exemplo-remoto": {
      "type": "http",
      "url": "https://<HOST-CONFIAVEL>/mcp",
      "headers": { "Authorization": "Bearer ${EXEMPLO_TOKEN}" }
    }
  }
}
```

Riscos e mitigação: `${EXEMPLO_TOKEN}` sem valor e sem padrão carrega o texto literal com aviso (V-15); tokens conhecidos (`ANTHROPIC_API_KEY` etc.) expandem como vazios em `url`/`headers` remotos; `headersHelper` roda comando de shell (revise); em CI/`-p`, use `disabledMcpjsonServers` ou `--strict-mcp-config`. O campo `type` e a forma remota do bloco são Inferido: confirme na página de MCP do Claude Code.

## 4. Comandos de CLI (Inferido; confirme com `claude mcp --help`)

Equivalentes ao JSON acima, para registrar um servidor sem editar arquivo:

```bash
claude mcp add <nome> -- node <CAMINHO-DO-ENTRYPOINT-REVISADO> <DIRETÓRIO-PERMITIDO>
claude mcp add --transport http <nome> https://<HOST-CONFIAVEL>/mcp
claude mcp list
claude mcp remove <nome>
claude mcp reset-project-choices     # redefine aprovações de servidores de projeto (V-15)
```

Plugins oficiais: `/plugin marketplace add anthropics/claude-plugins-official`, depois `/plugin install <plugin>@<NOME-DO-MARKETPLACE>`, onde `<NOME-DO-MARKETPLACE>` vem do `marketplace.json` do repositório (não verificado aqui). Leia o plugin antes (A-xx); ele pode trazer hooks e servidores MCP que sobem sozinhos.

## 5. Hook documentado (guardrail contra comandos destrutivos)

Script e testes completos em `hooks-e-guardrails.md`. Bloco de configuração (forma exec com `args`; `onFailure` exige v2.1.295+; valide na doc e na versão instalada: Inferido para o schema final):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "python", "args": ["<CAMINHO>/guard.py"], "timeout": 10, "onFailure": "block" }
        ]
      }
    ]
  }
}
```

Variações de interpretador: `python` pode não existir no PATH (Windows: `py`; Linux/macOS: `python3`). Regex não substitui sandbox (V-21); `rm -rf` em caminho absoluto dentro do projeto gera falso positivo (aceitável como guardrail; ajuste). Antes de editar qualquer `settings.json`, peça autorização.

## 6. Permissões e settings de endurecimento (rascunho; sintaxe de regras Inferido — confirme na doc de permissões)

```json
{
  "enableAllProjectMcpServers": false,
  "disabledMcpjsonServers": ["<SERVIDOR-NAO-APROVADO>"],
  "permissions": {
    "deny": ["Read(~/.ssh/**)", "Read(~/.aws/**)", "Read(./.env)", "Read(./.env.*)"]
  }
}
```

Limite verificado (V-21): regras deny para credenciais valem para as **ferramentas internas**; o Bash as contorna sem `/sandbox`. Para comandos destrutivos ou com rede, use sandbox, devcontainer ou VM. `enableAllProjectMcpServers: false` explícito importa porque `.mcp.json` vai para o git.

## 7. Job headless

Comando-base `claude -p --bare ...` e gate de erros: `jobs-workflows-e-scraping.md` seção 1; runbook: `assets/templates/runbook-job-agendado.md`. Agendar (cron, CI, Action) é decisão e ação do usuário.

## 8. Como desativar

| O que | Como |
| --- | --- |
| Servidor MCP de projeto | Remover do `.mcp.json`; `disabledMcpjsonServers`; `claude mcp remove <nome>`; em CI, `--strict-mcp-config` |
| Hook | Remover o bloco `hooks` do arquivo de settings (ou da skill) e reiniciar a sessão |
| Plugin de terceiro | Desabilitar/desinstalar o plugin; lembrar que hooks e MCP embutidos saem junto |
| Job agendado / Action | Remover a entrada do cron/CI/workflow; revogar secrets criados |

Fonte: V-12, V-13, V-15, V-17, V-21, V-24, V-25, V-28, V-29, V-31, V-32. Verificado em 2026-10-10 (itens V); campos marcados Inferido a conferir.
