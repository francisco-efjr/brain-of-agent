---
data: 2026-11-19
tags: [llm-ai-agents, seguranca-hardening, automation-integrations]
plugins: [llm-ai-agents, security-appsec, cli-desktop-tooling]
agentes: [llm-ai-agents:agent-architect, llm-ai-agents:agent-security-reviewer, security-appsec:security-reviewer]
contexto: "IA local fraca (OpenJarvis + Ollama) operando um PC Windows só por ferramentas MCP locais com as regras embutidas"
tipo_de_sessao: implementacao
modelo: claude-opus-5-5
---
# Modelo fraco segue padrões quando o padrão vira ferramenta: servidor MCP local como camada de SO

Origem: `local-ai-core/so/`, com servidor MCP em Python puro, 37 testes e 27 fontes diretas. Detalhes em `local-ai-core/so/PESQUISA-SO.md`.

## Boas práticas confirmadas
- [Verificado] Para modelo local fraco, regra no prompt não basta: catálogo fechado de ações, risco calculado por código e aprovação humana numa janela do sistema, fora do modelo. Motivo: o modelo não precisa lembrar a regra nem consegue aprovar por si. Evidência: testes de `tests/test_so_mcp.py` (recusa, R3, bloqueio, realidade mudou, disjuntor).
- [Verificado no código] O OpenJarvis liga servidor MCP externo por `[tools.mcp] servers` (JSON ou arquivo), com `command`/`args` ou `url`, e `tools.enabled` filtra as ferramentas MCP pelo nome. Motivo: dá para tirar `shell_exec` e deixar só o servidor. Evidência: `core/config.py`, `mcp/loader.py`, `system/builder.py` do OpenJarvis.
- [Verificado no código] Parâmetro vindo do modelo vai por variável de ambiente e o script vai por `-EncodedCommand`. Motivo: nome de serviço ou caminho nunca vira código.
- [Verificado na documentação] Consulta livre de PowerShell só de leitura com três cercas: lista de permitidos em Python, árvore sintática do PowerShell (`Parser.ParseInput`) e ConstrainedLanguage.

## Armadilhas
- [Verificado no código] O OpenJarvis descarta as anotações MCP (`readOnlyHint` etc.) → a política não pode depender delas → tudo no servidor.
- [Verificado no código] O stdio do OpenJarvis lê o pipe na codificação local do Windows → acentos em UTF-8 chegam errados → saída do servidor só em ASCII (`\uXXXX`).
- [Verificado no código] `[Environment]::SetEnvironmentVariable` no .NET Framework grava string como REG_SZ → regravar o PATH por ela troca REG_EXPAND_SZ e fixa caminhos → ler com `DoNotExpandEnvironmentNames` e gravar como `ExpandString`. A referência do Windows tinha o trecho errado e foi corrigida.
- [Verificado] Valor vazio em variável de ambiente some no Windows, e `(P 'X')` vira `$null` → chamar método nele quebra o script → converter com `[string]` antes. Achado pelo teste que confere os parâmetros usados por cada script.
- [Inferido] Processo filho que herda o stdin do servidor MCP pode consumir o canal → todo subprocesso com `stdin=DEVNULL`.

## Pesquisa
| Fonte (URL) | Classe | Acesso | Achado |
| --- | --- | --- | --- |
| https://modelcontextprotocol.io/specification/2025-11-25/basic/transports | A | 2026-11-19 | stdio: uma mensagem por linha |
| https://github.com/open-jarvis/OpenJarvis/blob/main/src/openjarvis/mcp/client.py | A | 2026-11-19 | Anotações descartadas, prazo de 600 s |
| https://github.com/microsoft/referencesource/blob/master/mscorlib/system/environment.cs | A | 2026-11-19 | `SetValue(nome, valor)` no PATH |
| https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_language_modes | A | 2026-11-19 | ConstrainedLanguage |
| https://github.com/akitaonrails/ai-memory/blob/main/companions/ai-memory-ts/schema/tools.json | A | 2026-11-19 | Parâmetros do ai-memory |

## Lacunas
- Os scripts PowerShell não rodaram num Windows real; a conferência é o `--autoteste` no PC do usuário.
- Não há tag para "IA local / OpenJarvis" (lacuna já registrada no tema memória).

## Promoção sugerida
- `llm-ai-agents` / `## Gotchas`: para modelo pequeno, troque regra no prompt por ferramenta com política em código e aprovação fora do modelo.
- `cli-desktop-tooling` / playbook: PATH do usuário pelo registro com `ExpandString`, nunca por `SetEnvironmentVariable`.
