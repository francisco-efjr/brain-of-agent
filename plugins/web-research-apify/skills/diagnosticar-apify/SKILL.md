---
name: diagnosticar-apify
description: "Diagnostica em leitura a configuração do Apify MCP na sessão: quais tools da Apify estão carregadas e sob qual prefixo, qual perfil (P0 a P3) isso representa, se há duplicidade (servidor manual, conector claude.ai, plugin oficial), se call-actor está em ask, se há tools de escrita carregadas e qual a versão do servidor. Use para 'o Apify está conectado?', 'quais tools do Apify eu tenho', 'checar o apify', 'o apify mcp não aparece', 'por que não acho call-actor'; EN 'is Apify connected', 'which Apify tools are loaded'. Somente leitura: não conecta nem executa Actor; para configurar ou corrigir a conexão, use conectar-apify."
allowed-tools: Read, Glob, Grep, ToolSearch
---

# diagnosticar-apify: o que está carregado, sob qual prefixo, com quais riscos

Objetivo: dizer, só lendo, se o Apify MCP está disponível nesta sessão, qual perfil de tools ele representa e o que merece correção, sem conectar nem executar nada. Razão: o prefixo das tools depende de como o servidor foi registrado e o conjunto muda com `tools=` e entre releases (V-02, V-03, V-13), então presumir nomes leva a chamadas que falham ou a tools de escrita ativas sem ninguém notar.

Validade: tabela de perfis conferida no código em 2026-10-13 (v0.18.0); nunca verificada contra uma sessão real (Suposição até o smoke test, H-01 e H-02). Se a doc ou o `tools/list` real divergirem, vale o que a sessão mostrar.

## Entradas

Nenhuma obrigatória. Se o usuário reclamar de algo ("não acho call-actor"), registre o sintoma e confira-o no passo 3.

## Passos

1. **Procurar as tools por nome.** `ToolSearch` por palavra-chave, uma consulta por nome (a consulta por nome acha a tool independentemente do prefixo): `search-actors`, `fetch-actor-details`, `call-actor`, `get-actor-run`, `get-dataset-items`, `search-apify-docs`, `apify-api-write`, `report-problem`, `delete-actor`. Use `max_results` ≥ 10. Saída: lista de nomes completos encontrados.
2. **Prefixo e origem.** `mcp__apify__` = servidor manual chamado `apify` · `mcp__claude_ai_<nome>__` = conector do claude.ai · `mcp__plugin_<plugin>_<servidor>__` = servidor de plugin (o nome exato do plugin oficial da Apify é Inferido). Mais de um prefixo com tools da Apify: **duplicidade**.
3. **Perfil pela tabela (V-04):**

   | Achado | Perfil |
   | --- | --- |
   | só `search-apify-docs` e `fetch-apify-docs` | P0 docs |
   | + `search-actors` e `fetch-actor-details`, sem `call-actor` | P1 descoberta |
   | + `call-actor`, `get-actor-run`, `get-dataset-items`, `get-key-value-store-record`, `abort-actor-run` | **P2 pesquisa controlada** |
   | tools `apify--<nome>` (ou `<dono>--<nome>`) | P3 Actors diretos: sem teto em dólares (alerta) |

   **Alerta** para qualquer uma destas carregada: `apify-api-write`, `delete-actor`, `create-schedule`, `update-schedule`, `delete-schedule`, `publish-actor-task`, `unpublish-actor-task`, `create-actor-task`, `update-actor-task`, `build-actor`. Alerta de baixa gravidade para `report-problem` no Claude Code (o README diz que fica escondida: o esperado é **ausente**).
4. **Permissões.** `Grep` por `mcp__apify` em `.claude/settings.json`, `.claude/settings.local.json` e no `.mcp.json` do projeto. `call-actor` deve estar em `ask`, não em `allow`; as tools de escrita em `deny`. Não abra `~/.claude.json` e não exiba blocos `env` ou `headers`: podem conter token. Ler com `Grep` mostra só a linha da regra.
5. **Telemetria e versão.** Não verificáveis daqui. Diga o que o usuário deve conferir: `claude mcp list` e `/mcp` (URL do servidor com ou sem `telemetry-enabled=false`; `serverInfo.version`).
6. **Recomendar**, em ordem de risco: tool de escrita carregada, `call-actor` sem `ask`, duplicidade, P3 para pesquisa com orçamento, perfil abaixo do necessário (oferecer `conectar-apify`).

## Verificação

- Cada linha do relatório aponta a evidência (resultado do `ToolSearch`, linha de settings com `arquivo:linha`).
- Nada foi conectado, executado ou editado. Nenhum valor de token foi lido ou repetido.
- Rótulos: Verificado (tool encontrada ou ausente nesta sessão, regra lida no arquivo), Inferido (perfil deduzido da tabela), Não verificável (versão, telemetria, `ask` efetivo).

## Formato de saída

```text
| Item | Estado | Evidência | Recomendação |
| Tools da Apify | <n carregadas> | ToolSearch: <nomes> | ... |
| Prefixo | mcp__apify__ | <nome completo de uma tool> | ... |
| Perfil | P2 | tabela V-04 | ... |
| Duplicidade | não | só um prefixo | ... |
| call-actor em ask | sim/não/Não verificável | .claude/settings.json:<linha> | ... |
| Tools de escrita | nenhuma | ToolSearch por apify-api-write: ausente | ... |
| Versão do servidor | Não verificável | exige /mcp | conferir serverInfo.version |
Não verificável: <lista>
```

Exemplo ilustrativo: `ToolSearch` por `call-actor` devolve `mcp__apify__call-actor`, e por `get-dataset-items` devolve `mcp__apify__get-dataset-items`; `apify-api-write`, `delete-actor` e `report-problem` não aparecem. Leitura: prefixo `mcp__apify__` (servidor manual), perfil P2, sem alertas; falta confirmar `ask` em settings e a versão do servidor (Não verificável).

## Gotchas

- `report-problem` ausente é o esperado no Claude Code (V-11); não é defeito.
- Tools adiadas pelo tool search só aparecem por `ToolSearch`: não conclua "não está conectado" só porque não estão na lista inicial.
- Nos perfis de pesquisa, `get-dataset-items` só aparece por auto-injeção (com `call-actor`, tool de Actor ou `get-actor-run`); em P0 e P1 ela não existe (V-03).
- `get-actor-log` virou `get-actor-run-log`; `add-actor` e `run-actor` não existem (V-03, V-13, V-18): nome antigo em material de terceiros não indica defeito da sessão.
- Perfil P2 sem Actors diretos: `apify--rag-web-browser` e `apify--web-fetch` não estão carregados; o caminho é `call-actor`.
- Conector claude.ai só carrega com login de assinatura (V-17); sem ele a ausência é esperada.
- Sem as tools: o trabalho segue com WebSearch e WebFetch e a lacuna é declarada; não instale nada.

## Referências

`${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/catalogo-de-tools.md` (catálogo e auto-injeção), `conexao-e-perfis.md`, `padroes-e-antipadroes.md`. Prompt pronto: P-02 na skill `prompts`. Para corrigir a conexão: `conectar-apify`.
