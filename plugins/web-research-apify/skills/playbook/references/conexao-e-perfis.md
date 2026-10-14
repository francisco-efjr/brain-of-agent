# Conexão e perfis de tools

Validade: lido em 2026-10-13 (README e código do `apify-mcp-server` v0.18.0, docs da Apify, docs do Claude Code). **Selo: volátil.** Nada aqui foi executado: a sintaxe é Verificada na fonte; o comportamento em sessão real é Suposição até o smoke test (`lacunas-e-smoke-test.md`).

**O plugin não registra nenhum servidor.** Tudo o que está nesta página é receita para você ler, entender o efeito e só então rodar (ou pedir ao assistente, depois de um "sim" explícito no chat). O assistente nunca pede, recebe nem repete token.

Sumário: 1. Primeiro passo: trava da conta · 2. Perfis P0 a P3 · 3. Parâmetros de URL · 4. Receitas R-A a R-F · 5. Windows e PowerShell · 6. Escopos, precedência e duplicidade · 7. Permissões · 8. Token e variável de ambiente · 9. Telemetria · 10. Gerenciar e desligar · 11. Diagnóstico · 12. Hook opcional

## 1. Primeiro passo: a trava da conta

Antes de conectar qualquer perfil com `call-actor`, ligue o limite de uso no Console da Apify: **Console › Billing › Limits**, com *overage* desligado. Ao atingir o limite do plano, a plataforma suspende os serviços (lido pelo crítico em docs.apify.com/platform/console/billing, 2026-10-14; se o limite pode ficar abaixo do valor do plano: Inferido). Motivo: é a única trava que não depende de o modelo obedecer a uma instrução (o `ask` não é respondível em execução não interativa, H-08). Detalhes em `custo-e-orcamento.md`.

## 2. Perfis de `tools=` para pesquisa (V-04; fatos Verificados, recomendação Inferida)

`tools=` informado substitui o conjunto padrão inteiro. Nenhum perfil foi conectado de verdade.

| Perfil | URL | O que carrega | Custo | Auth |
| --- | --- | --- | --- | --- |
| **P0 docs** | `?tools=docs` | `search-apify-docs`, `fetch-apify-docs` (2 tools) | zero | não |
| **P1 descoberta** | `?tools=search-actors,fetch-actor-details,docs` | 4 tools de leitura; sem tools de run; sem auto-injeção | zero | não |
| **P2 pesquisa controlada (recomendado)** | `?tools=actors,docs` | P1 mais `call-actor` e as 4 auto-injetadas (9 tools no total) | só em `call-actor`, com teto em `callOptions` | sim |
| **P3 Actors diretos** | `?tools=apify/rag-web-browser,apify/web-fetch,docs,...` | tools diretas mais as 4 auto-injetadas | **sem teto em dólares por MCP** | sim |

Como escolher:

- **Só ler documentação ou testar a conexão:** P0 (receita R-B). Não precisa de login e não gasta.
- **Escolher Actor e ver preço:** P1. Sem login e sem gasto; não lê dataset (não há `get-dataset-items`).
- **Coletar dados com orçamento:** P2. É o único perfil em que o teto de dólares existe: `call-actor` aceita `callOptions.maxTotalChargeUsd` (só para Actors cobrados por evento).
- **Evite P3 para pesquisa com orçamento.** A tool direta chama o Actor só com `{ memory }` (`tool_dispatch.ts:257`): não aceita `callOptions`, logo não tem teto em dólares nem `timeout`. O perfil que alguns materiais chamam de "sem call-actor" é P3: continua executando Actors pagos e injeta `abort-actor-run`.
- **Fora de qualquer perfil de pesquisa:** `apify-api-write`, `delete-actor`, `delete-schedule`, `update-schedule`, `create-schedule`, `publish-actor-task`, `build-actor`, `create-actor-task`. O motivo está em `catalogo-de-tools.md`, seção 8.
- Em P2, `abort-actor-run` fica em `ask`: só encerra gasto, mas deixa dados parciais.
- Tool search do Claude Code adia as definições (V-34), então tools extras custam pouco contexto; ainda assim a escolha errada de tool é risco, e a superfície de ataque cresce com cada tool.

## 3. Parâmetros de URL (V-02)

| Parâmetro | Efeito | Rótulo |
| --- | --- | --- |
| `tools=` | Categorias (`actors, docs, runs, storage, tasks, schedules, builds, source, api, dev`), nomes de tool e Actors `usuario/nome`. Se informado, **nada** do padrão entra | Verificado (código e README) |
| `actors=` | Legado; mesclado em `tools` | Verificado |
| `telemetry-enabled=false` | Desliga a telemetria no servidor hospedado | Verificado (README; docs) |
| `ui=` (`true`, `apps`, `default`, `false`, `auto`) | Widgets; não usar em pesquisa | Inferido (espelhamento do `dev_server.ts`) |
| `payment=` (`x402`, `skyfire`) | Pagamento agêntico; não usar | Inferido |
| `client=` | Etiqueta de telemetria | Inferido |
| `?token=` | Existe só no servidor de desenvolvimento local; o hospedado não o documenta. **Não use nem recomende**: token em URL vai para histórico e logs | Verificado |

A página de docs da Apify documenta só `tools` e `telemetry-enabled`; os demais vêm do README e do código (fonte primária, porém menos documentados). Combine parâmetros com `&` (o README mostra `?tools=actors,docs&ui=true`). O padrão sem `tools=` (categorias `actors` e `docs`, `apify/rag-web-browser`, `apify/web-fetch`, `report-problem` condicionado e as auto-injetadas) pode mudar entre releases: **fixe `tools=`**.

## 4. Receitas de conexão

> Não ativas. O plugin não registra servidor nenhum. Copie só depois de ler o efeito e de confirmar com o assistente. Rótulos: sintaxe Verificada na fonte; nenhuma foi testada em runtime.

### R-A. Claude Code com OAuth (recomendada)

Fonte: code.claude.com/docs/en/mcp, docs.apify.com/platform/integrations/mcp, build-with-ai. Rótulo: Verificado (sintaxe), Não testado.

```bash
claude mcp add --transport http apify "https://mcp.apify.com/?tools=actors,docs"
```

- **Efeito:** grava o servidor em `~/.claude.json` no escopo `local` (padrão: só você, só este projeto). Telemetria ligada por padrão. `call-actor` roda Actors de terceiros, que cobram.
- **Depois, na sessão:** `/mcp` > `apify` > Authenticate (abre o navegador). O login é seu; o assistente não pede token, senha nem código.
- **Variações:** `&telemetry-enabled=false` (Verificado no README); `--scope user` para valer em todos os projetos.
- **O nome `apify`** define o prefixo das permissões (`mcp__apify__...`; seção 7).

### R-B. Só documentação, teste mínimo (sem auth e sem gasto)

Comando literal da Apify (build-with-ai):

```bash
claude mcp add apify "https://mcp.apify.com/?tools=docs" -t http
```

- **Efeito:** carrega só `search-apify-docs` e `fetch-apify-docs`. Bom primeiro passo e roteiro S1 do smoke test.

### R-C. Token por variável de ambiente (headless ou SSH, se o OAuth não servir)

Fonte: doc do Claude Code (expansão de variáveis) e `DEVELOPMENT.md` do repo. Rótulo: Verificado (formato), **Não testado** (expansão de `APIFY_TOKEN`; H-09). Conteúdo que você poderia pôr no `.mcp.json` do **seu** projeto (escopo `project`; o Claude Code pede aprovação para servidores desse arquivo):

```json
{
  "mcpServers": {
    "apify": {
      "type": "http",
      "url": "https://mcp.apify.com/?tools=actors,docs",
      "headers": { "Authorization": "Bearer ${APIFY_MCP_TOKEN}" }
    }
  }
}
```

- **Por que o nome `APIFY_MCP_TOKEN`:** em `url` e `headers` de servidor remoto, o Claude Code lê como vazias as variáveis de credencial conhecidas (por exemplo `ANTHROPIC_API_KEY`); `APIFY_TOKEN` não está na lista nominal, mas a categoria "outras credenciais" é ambígua. A doc manda copiar o valor para uma variável de nome próprio.
- **Onde definir:** variável de usuário do sistema operacional (Windows: Variáveis de Ambiente do usuário). Evite `env` em `.claude/settings.local.json`: o modelo consegue ler esse arquivo.
- **Token com escopo e expiração curta** (V-29). O valor nunca vai no `.mcp.json`, no comando, na URL nem no chat. Evite `--header "Authorization: Bearer <token real>"` na linha de comando: ela fica no histórico do shell e em `~/.claude.json`.
- **Efeito:** com o header definido **não há fallback OAuth**. Se o token falhar, o servidor não conecta.
- Conferir: `claude mcp list` (variável ausente carrega o texto literal com aviso) e `claude --debug-file <arquivo>` procurando `never expanded toward a remote server`.

### R-D. Conector custom no claude.ai

Fonte: support.claude.com (Verificado). Customize > Connectors > "+ Add" > "Add custom connector" > nome e URL `https://mcp.apify.com` > Continue > autenticação "Sign in now" com "Use Claude's published identity (Recommended)" > Add.

- **Efeito:** vale no claude.ai e **aparece no Claude Code** só com login de assinatura claude.ai (não carrega com `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, `apiKeyHelper`, Bedrock, Vertex nem `CLAUDE_CODE_OAUTH_TOKEN`). Prefixo `mcp__claude_ai_<servidor>__`. Desligar: `ENABLE_CLAUDEAI_MCP_SERVERS=false claude` ou `"disableClaudeAiConnectors": true`.
- **Não use junto com R-A** (duplicidade; seção 6). A página de suporte avisa que conectores custom não são verificados pela Anthropic e podem trazer instruções ocultas: "Allow always" só para servidor confiável.
- O conector Apify do diretório da Anthropic: URL e lista de tools não lidas (lacuna 4).

### R-E. Plugin oficial da Apify (opção separada; só para desenvolver Actors)

```text
/plugin marketplace add apify/apify-claude-code-plugin
/plugin install apify@apify
```

Verificado nos docs da Apify e do Claude Code. **Traz MCP ativo** sem `tools=` e um agente com `Bash`; a skill de scraping usa a CLI, que não tem flag de teto de gasto e pede `apify login --token`. Por isso este plugin não o empacota e **não deve coexistir com R-A** para pesquisa (a URL com query diferente cria um segundo servidor). Detalhes em `seguranca-e-privacidade.md`, seção 11.

### R-F. stdio local (último recurso)

```bash
claude mcp add --transport stdio apify -- npx -y @apify/actors-mcp-server
```

- Exige Node **≥ 22** (a página de docs da Apify ainda diz ≥ 18: desatualizada) e `APIFY_TOKEN` no ambiente. Sem `APIFY_TOKEN`, o stdio lê `~/.apify/auth.json` (login do Apify CLI) sem avisar.
- No Windows nativo o Claude Code emite o aviso "Windows requires 'cmd /c' wrapper to execute npx" (issues #9594 e #20061, fechadas como `not_planned`; a #20061 relata que `claude mcp add` troca `/c` por `C:/`). A doc atual não menciona `cmd /c`.
- **Rebaixada:** prefira o remoto (R-A). Se usar, fixe a versão do pacote em vez de `@latest` (cadeia de suprimentos; `/security-appsec:secrets-supply-chain-review`). Rótulo: Verificado a sintaxe, Não testado.

## 5. Windows e PowerShell (V-02, V-17)

- **Aspas na URL, sempre.** No PowerShell a vírgula de `tools=a,b` vira array e `&` quebra o comando; as aspas evitam os dois. Exemplo: `claude mcp add --transport http apify "https://mcp.apify.com/?tools=actors,docs"`.
- Sem aspas, a falha costuma ser silenciosa (URL truncada, perfil errado). Depois de adicionar, rode `claude mcp list` e confira a URL e as tools do perfil.
- Para `&telemetry-enabled=false`, as aspas são ainda mais necessárias.
- R-C no Windows: use a variável de usuário do sistema; reinicie o terminal para o Claude Code enxergá-la.

## 6. Escopos, precedência e duplicidade (V-15, V-17, V-18)

- **Escopos:** `local` (padrão; `~/.claude.json`, só você neste projeto), `project` (`.mcp.json`, compartilhado), `user` (todos os projetos).
- **Precedência:** local, depois project, user, plugin e por fim conector. Servidores do `.mcp.json` de projeto pedem aprovação.
- **Duplicidade:** servidor adicionado no Claude Code tem precedência sobre o conector do mesmo endpoint, mas **URL com query diferente conta como outro servidor** (`?tools=actors,docs` e `?client=claude+code+plugin` viram dois). Sintoma: tools da Apify sob mais de um prefixo. Correção: mantenha um só (`claude mcp remove` do que sobrar ou desabilite o conector/plugin).
- Plugins não carregam em sessões remotas ou web.

## 7. Permissões do Claude Code (V-19; sintaxe Verificada, efeito não testado: H-07)

Avaliação: `deny`, depois `ask`, depois `allow`. As regras são impostas pelo Claude Code, não pelo modelo: por isso valem mais que qualquer instrução no prompt. Sintaxe `mcp__<servidor>`, `mcp__<servidor>__*`, `mcp__<servidor>__<tool>`; `deny` e `ask` aceitam glob de nome; `allow` só com glob depois do prefixo literal `mcp__<servidor>__`. Regras `mcp__` com parênteses são ignoradas (para filtrar por parâmetro existe `--disallowedTools`). **Não ponha `call-actor` em `allow`.**

Exemplo para o servidor chamado `apify` (troque o prefixo se o nome for outro; edite o `settings.json` do usuário ou do projeto, a pedido seu):

```json
{
  "permissions": {
    "ask":  ["mcp__apify__call-actor", "mcp__apify__abort-actor-run"],
    "deny": ["mcp__apify__apify-api-write", "mcp__apify__delete-actor", "mcp__apify__delete-schedule",
             "mcp__apify__update-schedule", "mcp__apify__create-schedule", "mcp__apify__publish-actor-task",
             "mcp__apify__unpublish-actor-task", "mcp__apify__create-actor-task", "mcp__apify__update-actor-task",
             "mcp__apify__build-actor"]
  }
}
```

- `ask` em `call-actor` dá a cada run um ponto de parada humano em uso interativo. Em execução não interativa (workflow, `claude -p`) o `ask` não é respondível (H-08): a trava passa a ser o limite da conta.
- `deny` em tool que o perfil não carrega deve ser inofensivo (H-07, a confirmar).
- Com conector claude.ai o prefixo é `mcp__claude_ai_<servidor>__`; com plugin, `mcp__plugin_<plugin>_<servidor>__`.

## 8. Token e variável de ambiente (V-15, V-16, V-29)

- **Uso interativo:** OAuth (R-A). **Headless ou CI:** token com escopo e expiração curta (Inferido) em variável de ambiente de nome próprio (R-C).
- Tipos de token: pessoal, de organização (acesso total) e com escopo ("scoped": só recursos liberados; não cria nem altera Actors). Rotação mantém o token antigo por 24 h. Um token por serviço; nunca em código cliente. O header `Authorization` é a forma recomendada (a API também aceita `?token=`, mas a doc diz que o header é mais seguro).
- Não verificado: se token com escopo funciona no `mcp.apify.com`; escopos do OAuth do MCP; revogação direta (lacuna 3).
- Se um token apareceu no chat, em URL, comando ou arquivo, trate como exposto: rotacione ou remova no Console (console.apify.com/settings/integrations) e lembre que a rotação mantém o antigo por 24 h. Não repita o valor nem para "confirmar".

## 9. Telemetria (V-11)

Ligada por padrão. Cada chamada gera um evento com nome, versão e capacidades do cliente, ID de sessão, `?client=`, nome da tool, status, duração, tamanhos de resposta, `actor_name` e `actor_id`, `run_id`, `dataset_id`, `key_value_store_id`, detalhes de validação e `failure_detail` (pode conter até 200 caracteres de mensagem de erro). **Não inclui os argumentos da tool.** Com usuário conhecido usa o ID Apify; só sem usuário vira `anonymousId` (então "anônima" não vale para sessão autenticada). Desligar: `?telemetry-enabled=false` no hospedado; `--telemetry-enabled=false` ou `TELEMETRY_ENABLED=false` no stdio (a flag vence a variável; o Sentry, só no stdio, desliga junto). Política completa: docs.apify.com/legal.

## 10. Gerenciar e desligar (V-15)

| Ação | Comando | Efeito |
| --- | --- | --- |
| Listar | `claude mcp list` ou `/mcp` | Mostra servidores e estado; variável ausente aparece com aviso |
| Autenticar | `/mcp` > `apify` > Authenticate | OAuth no navegador, por você |
| Sair | `claude mcp logout apify` | **Interruptor de emergência:** encerra a autenticação e corta as tools da sessão (Inferido: o servidor continua registrado) |
| Remover | `claude mcp remove apify` | Apaga o registro e os tokens OAuth |
| Desligar conectores claude.ai | `ENABLE_CLAUDEAI_MCP_SERVERS=false claude` | Só para essa execução |

Encerramento completo: `logout` ou `remove`, apagar datasets de teste, revogar token de teste (ver `checklist-completo.md`, seção EN).

## 11. Diagnóstico (usado por `diagnosticar-apify`)

1. `ToolSearch` pelos nomes da seção 7 de `catalogo-de-tools.md`; derive prefixo e perfil. Só docs: P0. Quatro de leitura: P1. `call-actor` mais 4 injetadas: P2. Presença de `apify--...`: P3. Qualquer tool "fora" do catálogo carregada: alerta.
2. Mais de um prefixo com tools da Apify: duplicidade.
3. Permissões: `Grep` por `mcp__apify` em `.claude/settings*.json` e `.mcp.json` do projeto. **Não abra `~/.claude.json` nem exiba `env`** (pode conter token). `call-actor` deve estar em `ask`, não em `allow`.
4. Telemetria e versão do servidor: não verificáveis sem `/mcp` ou a URL; diga o que o usuário deve conferir.
5. `report-problem` ausente é o esperado no Claude Code.

## 12. Hook opcional (Suposição; não incluído)

Um hook `PreToolUse` em `mcp__apify__call-actor` que negue chamada sem `callOptions.maxTotalChargeUsd` ou acima do orçamento seria uma trava mecânica. É **Suposição** (não foi testado) e é código executável: o plugin não o traz. Se quiser, desenhe com `/automation-integrations:writing-hook-guardrails`, em ambiente descartável. Lembre que um hook é guardrail, não fronteira de segurança.
