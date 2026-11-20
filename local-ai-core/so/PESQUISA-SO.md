# Pesquisa: modo SO (camada de ferramentas por MCP local)

Data: 2026-11-19 · Pesquisador: Claude Opus 5.5 (Claude Code) · Fontes diretas: 27 (especificação MCP, código-fonte do OpenJarvis, do ai-memory e do .NET Framework, documentação da Microsoft) · Base da casa reaproveitada: as pesquisas dos temas Windows (98 fontes), memória (41) e automação (25).

Pedido do dono: o modelo local é fraco, então ele precisa saber os padrões e sempre usá-los, rodando tudo localmente, com MCP, e ser muito bom em ferramentas locais, agindo "como um SO puro".

## 1. Achados principais

1. **Prompt não é trava; ferramenta é.** A pesquisa do tema Windows já mostrava que o OpenJarvis aceita `enforce_tool_confirmation`, mas não aplica, e que `shell_exec` aprova sozinho fora do `jarvis chat` (O-04). Com um modelo fraco, a regra precisa morar no código da ferramenta, não no texto do prompt. Daí o desenho: catálogo fechado de ações, risco calculado por código e aprovação humana fora do modelo.
2. **O OpenJarvis conecta servidores MCP externos, mas só o código diz como.** As páginas de MCP da documentação (`user-guide/mcp/` e as da API de `mcp`) dão 404, e as que abrem só citam a chave `servers` (O-01 a O-03). No código (C-01 a C-03): `[tools.mcp] servers` aceita JSON na linha ou o caminho de um arquivo .json. Cada servidor tem `name`, `command` e `args` (stdio) ou `url` e `token` (HTTP), além de `include_tools` e `exclude_tools`. Não há `env` nem `cwd`.
3. **`tools.enabled` filtra também as ferramentas MCP.** Com a lista preenchida, só entram as ferramentas cujo nome está nela (C-03). Isso permite deixar `shell_exec` de fora e ficar só com o servidor SO.
4. **O cliente do OpenJarvis descarta as anotações MCP.** `readOnlyHint`, `destructiveHint` e afins não chegam ao agente; o `ToolSpec` guarda só nome, descrição e parâmetros, com prazo de 600 s (C-04). Por isso a política inteira fica no servidor.
5. **Codificação do pipe.** O transporte stdio do OpenJarvis abre o processo em modo texto, com a codificação local do Windows (C-05). Servidor que escreve UTF-8 com acentos seria lido errado; a saída do servidor SO é só ASCII (`\uXXXX`). O cliente envia `protocolVersion` 2025-03-26 e manda o JSON com escape ASCII (C-04, C-06).
6. **O formato stdio do MCP é simples.** Uma mensagem JSON-RPC por linha, sem quebra de linha dentro, nada além de mensagens MCP no stdout e logs no stderr. Erro de ferramenta volta como resultado com `isError`, para o modelo corrigir; erro de protocolo (ferramenta desconhecida) volta como erro JSON-RPC (M-01 a M-03). A versão 2026-07-28 tira o handshake e põe a versão em cada pedido (M-04 a M-06); o OpenJarvis ainda usa o handshake.
7. **Aprovação que o modelo não forja.** A janela `Popup` do Windows devolve 6 (Sim), 7 (Não) ou -1 (prazo esgotado), com botão padrão Não e sempre na frente (W-02). R3 usa uma janela em que é preciso digitar CONFIRMO. Sem resposta, a resposta é não.
8. **Administrador só pelo UAC.** `Start-Process -Verb RunAs -Wait -PassThru` roda elevado e espera (W-05). A página não documenta o erro quando o usuário cancela o UAC; o servidor trata qualquer falha ali como recusa.
9. **Consulta livre com três cercas.** A árvore sintática do próprio PowerShell (`Parser.ParseInput`, W-08) permite conferir cada comando, alias e método antes de rodar. O modo ConstrainedLanguage só deixa chamar métodos de tipos permitidos (W-03). A Microsoft diz que mudar o modo pelo `$ExecutionContext` é útil para experimentar, então ele é camada extra, não a fronteira.
10. **O trecho de PATH da referência do Windows estava errado.** No .NET Framework, `SetEnvironmentVariable` grava com `SetValue(nome, valor)` e uma string vira REG_SZ (N-01, N-02). Ler e regravar o PATH por essa API troca REG_EXPAND_SZ por REG_SZ e fixa caminhos expandidos. A página da API confirma o aviso WM_SETTINGCHANGE, mas não fala do tipo (W-01). Correção: ler com `DoNotExpandEnvironmentNames` e gravar como `ExpandString`. O servidor faz assim, e o §23 da REFERENCIA-WINDOWS foi corrigido.
11. **Lixeira por API, com limite.** `FileSystem.DeleteFile` com `SendToRecycleBin` manda para a Lixeira; as opções de interface não valem em aplicações não interativas, como serviços (W-06). Daí: só disco local, e volume grande sobe para R3.
12. **Agendador.** O limite de tempo padrão é de três dias segundo o exemplo da página, embora a tabela diga "None" (W-07). O servidor sempre define 30 minutos e `IgnoreNew`, como o tema automação já pedia.
13. **winget.** `--exact`, `--source`, `--silent`, `--disable-interactivity`, `--accept-package-agreements` e `--accept-source-agreements` existem no `install` (W-04). O servidor não aceita termos de fonte sozinho; a licença do pacote só é aceita quando você aprova na janela.
14. **ai-memory pelo MCP local.** O esquema das ferramentas (A-01) dá os parâmetros exatos: `memory_write_page` (path e body obrigatórios, com title, tier, tags, workspace e project), `memory_query` (query), `memory_handoff_begin` (summary) e `memory_briefing`. O transporte é HTTP em 127.0.0.1:49374 (base da casa, tema memória).

## 2. Validação da esteira no modo SO

| Passo | No modo SO | Evidência |
| --- | --- | --- |
| 0 Classificar | Regra de risco por ação, em código | Achado 1; classes do CORE-WINDOWS |
| 1 Estruturar e observar | `so_planejar` lê o estado antes de decidir | Base Windows (observar antes de agir) |
| 2 a 4 Visão | O modelo escolhe uma ação de um catálogo fechado | Achado 1 |
| 5 e 6 Conceber e produzir | Roteiro fixo e backup preparado | Base Windows e automação |
| 7 Testar de novo | `-WhatIf` ou descrição exata do efeito | Base Windows |
| 8 Validar o escopo | Relê o estado e pede aprovação humana na janela | Achados 7 e 8 |
| 9 Implementar | Uma ação por plano; elevação só pelo UAC | Achado 8 |
| 10 Verificar e registrar | Relê o efeito; plano e JSONL guardados | Base automação (observabilidade) |

O estudo acrescenta uma correção ao desenho anterior: **a aprovação passa do chat para o sistema**. No modo prompt, o "sim" vinha do chat e dependia do modo do OpenJarvis; no modo SO, R2 e R3 sempre abrem a janela do Windows, mesmo no `jarvis ask` e no app desktop.

## 3. Fontes

Classe A: fonte primária (especificação, código-fonte, documentação oficial). Acesso: 2026-11-19.

| ID | Fonte | Classe | Achado |
| --- | --- | --- | --- |
| M-01 | https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle | A | initialize, negociação de versão, notifications/initialized |
| M-02 | https://modelcontextprotocol.io/specification/2025-11-25/basic/transports | A | stdio: uma mensagem por linha, stderr para logs |
| M-03 | https://modelcontextprotocol.io/specification/2025-11-25/server/tools | A | tools/list, tools/call, isError, validar entradas |
| M-04 | https://modelcontextprotocol.io/specification/2025-11-25/schema.md | A | Anotações de ferramenta são dicas (lido em parte) |
| M-05 | https://modelcontextprotocol.io/specification/2026-07-28/basic.md | A | Versão nova sem handshake |
| M-06 | https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning.md | A | Versão por pedido e erro -32022 |
| O-01 | https://open-jarvis.github.io/OpenJarvis/user-guide/tools/ | A | Ferramentas e adaptador MCP (lido em parte) |
| O-02 | https://open-jarvis.github.io/OpenJarvis/getting-started/configuration | A | `[tools.mcp]` com `enabled` e `servers` (lido em parte) |
| O-03 | https://open-jarvis.github.io/OpenJarvis/user-guide/system-access/ | A | `tools.enabled` é a lista completa; confirmação por modo (lido em parte) |
| O-04 | Pesquisa do tema Windows, `windows/PESQUISA-WINDOWS.md` | Casa | `shell_exec` aprova sozinho fora do `jarvis chat` |
| C-01 | https://github.com/open-jarvis/OpenJarvis/blob/main/src/openjarvis/core/config.py | A | `MCPConfig`, `resolve_mcp_servers` (JSON ou arquivo) |
| C-02 | https://github.com/open-jarvis/OpenJarvis/blob/main/src/openjarvis/mcp/loader.py | A | Campos de cada servidor; filtros de ferramentas |
| C-03 | https://github.com/open-jarvis/OpenJarvis/blob/main/src/openjarvis/system/builder.py | A | `tools.enabled` filtra as ferramentas MCP |
| C-04 | https://github.com/open-jarvis/OpenJarvis/blob/main/src/openjarvis/mcp/client.py | A | protocolVersion 2025-03-26; anotações descartadas; 600 s |
| C-05 | https://github.com/open-jarvis/OpenJarvis/blob/main/src/openjarvis/mcp/transport.py | A | stdio em modo texto; stderr drenado |
| C-06 | https://github.com/open-jarvis/OpenJarvis/blob/main/src/openjarvis/mcp/protocol.py | A | JSON com escape ASCII |
| C-07 | https://github.com/open-jarvis/OpenJarvis/blob/main/src/openjarvis/tools/mcp_adapter.py | A | Junta o texto do resultado; isError vira falha |
| A-01 | https://github.com/akitaonrails/ai-memory/blob/main/companions/ai-memory-ts/schema/tools.json | A | Parâmetros das ferramentas do ai-memory |
| N-01 | https://github.com/microsoft/referencesource/blob/master/mscorlib/system/environment.cs | A | `SetEnvironmentVariable` usa `SetValue(nome, valor)` |
| N-02 | https://github.com/microsoft/referencesource/blob/master/mscorlib/microsoft/win32/registrykey.cs | A | String vira `RegistryValueKind.String` |
| W-01 | https://learn.microsoft.com/en-us/dotnet/api/system.environment.setenvironmentvariable | A | Avisa por WM_SETTINGCHANGE; User fica em HKCU\Environment |
| W-02 | https://learn.microsoft.com/en-us/previous-versions/windows/internet-explorer/ie-developer/windows-scripting/x83z1d9f(v=vs.84) | A | Popup: 6, 7, -1; opções 4, 48, 256, 4096 |
| W-03 | https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_language_modes | A | ConstrainedLanguage: métodos só de tipos permitidos |
| W-04 | https://learn.microsoft.com/en-us/windows/package-manager/winget/install | A | Opções do `winget install` |
| W-05 | https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/start-process | A | `-Verb RunAs`, `-Wait`, `-PassThru` |
| W-06 | https://learn.microsoft.com/en-us/dotnet/api/microsoft.visualbasic.fileio.filesystem.deletefile | A | `SendToRecycleBin`; opções de interface fora de serviços |
| W-07 | https://learn.microsoft.com/en-us/powershell/module/scheduledtasks/new-scheduledtasksettingsset | A | Limite padrão de três dias; `IgnoreNew` |
| W-08 | https://learn.microsoft.com/en-us/dotnet/api/system.management.automation.language.parser.parseinput | A | `ParseInput(input, out tokens, out errors)` |

## 4. Lacunas

- Nada disso rodou num Windows real nesta sessão: os scripts PowerShell foram testados com um executor falso. O `--autoteste` é a conferência no PC.
- Não achei documentação do erro do `Start-Process -Verb RunAs` quando o UAC é cancelado, nem de `CommandAst.GetCommandName` devolvendo nulo para nome dinâmico. O servidor trata os dois casos como recusa.
- Não conferi se `winget uninstall` e `winget upgrade` aceitam todas as opções do `install`. O `--autoteste` não instala nada; teste com um pacote pequeno antes de confiar.
- O caminho de página que o servidor usa no ai-memory (`ia-operador/<pasta>/<slug>.md`) segue o esquema, mas não foi testado contra um ai-memory real. Se ele recusar, a nota cai na memória local e a resposta mostra o erro.
