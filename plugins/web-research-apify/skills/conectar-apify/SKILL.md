---
name: conectar-apify
description: "Orienta a conexão do Apify MCP ao Claude Code sem ativar nada por conta própria: escolhe o perfil de tools (docs grátis, descoberta, pesquisa controlada), mostra o comando exato com efeito e riscos, espera o 'sim' do usuário antes de qualquer claude mcp add e deixa o login OAuth com o usuário. Use para 'conectar o Apify', 'instalar o apify mcp', 'configurar mcp.apify.com', 'adicionar o conector do Apify', 'token do Apify'; EN 'connect Apify MCP', 'add Apify to Claude Code', 'set up the Apify connector'. Nunca pede, recebe nem repete token; não instala o plugin oficial; não duplica servidor existente. Para só checar o que já está carregado, use diagnosticar-apify."
argument-hint: "[perfil: docs | descoberta | pesquisa] [escopo: local | user]"
allowed-tools: Read, Glob, Grep
---

# conectar-apify: mostrar o caminho, confirmar, deixar o login com o usuário

Objetivo: levar o usuário a um Apify MCP conectado com o menor conjunto de tools que serve ao uso, sem que o assistente ative, instale ou autentique nada sozinho. Razões: o plugin não traz `.mcp.json` por política da casa; `claude mcp add` grava em `~/.claude.json`, liga telemetria por padrão e deixa disponível uma tool que gasta dinheiro (`call-actor`); e o OAuth e qualquer token pertencem ao usuário (V-15, V-16, V-29).

Validade: sintaxe conferida na doc e no código em 2026-10-13 (servidor v0.18.0); **nenhuma receita foi testada em runtime**. Receitas abaixo: NÃO ATIVAS, copiar só depois de ler o efeito e dar o "sim".

## Entradas ($ARGUMENTS)

Perfil desejado (P2 para pesquisa; P0 só para testar), escopo (`local` é o padrão do Claude Code; `user` vale para todos os projetos), sistema e shell (PowerShell exige aspas na URL), uso interativo ou sem humano (headless). Falta o perfil? Assuma P2 e diga que assumiu.

## Passos

1. **Estado atual.** Rode o roteiro de `diagnosticar-apify` (ou peça ao usuário `claude mcp list`): existe servidor `apify`? Conector claude.ai com Apify? Plugin oficial da Apify instalado? Duplicidade? Saída: situação em uma linha. Já conectado como esperado: pare e diga.
2. **Escolher a receita.** R-A OAuth (padrão) · R-B só docs (teste, sem auth) · R-C token por variável de ambiente (headless ou SSH) · R-D conector no claude.ai (nunca junto com R-A) · R-F stdio (último recurso). Saída: receita e perfil.
3. **Mostrar comando e efeito**, nunca executar ainda: onde grava (`~/.claude.json` no escopo `local`), telemetria (evento por chamada com nome da tool, Actor, `runId`, ID Apify quando conhecido, sem os argumentos; `&telemetry-enabled=false` desliga), e que `call-actor` roda Actors de terceiros que cobram (V-11, V-18).
4. **Esperar o "sim" explícito deste chat.** Só então o assistente roda o comando pelo Bash, com o prompt de permissão normal, ou o usuário o roda com o prefixo `!`. Nada de `--scope` ou perfil diferente do que foi mostrado.
5. **Login é do usuário.** Ele abre `/mcp` > `apify` > Authenticate no navegador. O assistente não pede token, senha nem código.
6. **Travas.** Primeiro, o usuário liga o limite de uso da conta (Console › Billing › Limits, overage desligado): é a única trava que não depende de o modelo obedecer. Depois, proponha as regras `ask` e `deny` abaixo e só edite settings se ele pedir.
7. **Verificar.** `claude mcp list` e `/mcp`: as tools carregadas batem com o perfil (tabela em `conexao-e-perfis.md`); `call-actor` está em `ask`; nenhum segredo apareceu em comando, URL ou arquivo; sem servidor duplicado. Registre `serverInfo.version` se visível.

## Receitas (NÃO ATIVAS: copiar só com confirmação)

R-A, perfil P2 (Verificado a sintaxe; Não testado). O nome `apify` define o prefixo das permissões e do agente `apify-researcher`:

```bash
claude mcp add --transport http apify "https://mcp.apify.com/?tools=actors,docs"
```

R-B, só docs, sem auth e sem gasto (comando da própria Apify):

```bash
claude mcp add apify "https://mcp.apify.com/?tools=docs" -t http
```

R-C, token por variável de ambiente (Verificado o formato; Não testado se `${APIFY_MCP_TOKEN}` expande, H-09). Defina `APIFY_MCP_TOKEN` no ambiente do SO (token **com escopo e expiração**, V-29); o valor nunca vai no comando, no arquivo ou no chat. Com o header definido não há fallback OAuth:

```json
{ "mcpServers": { "apify": { "type": "http", "url": "https://mcp.apify.com/?tools=actors,docs",
  "headers": { "Authorization": "Bearer ${APIFY_MCP_TOKEN}" } } } }
```

R-D (claude.ai, Customize > Connectors > Add custom connector, URL `https://mcp.apify.com`) e R-F (stdio com Node ≥ 22; no Windows exige `cmd /c`, rebaixado) estão em `${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/conexao-e-perfis.md`. O plugin oficial da Apify traz MCP ativo sem `tools=`, agente com `Bash` e CLI sem teto de gasto (V-18): não instale junto para pesquisa.

Permissões recomendadas (Verificado a sintaxe; efeito não testado, H-07; troque o prefixo se o servidor tiver outro nome):

```json
{ "permissions": {
  "ask":  ["mcp__apify__call-actor", "mcp__apify__abort-actor-run"],
  "deny": ["mcp__apify__apify-api-write", "mcp__apify__delete-actor", "mcp__apify__create-schedule",
           "mcp__apify__update-schedule", "mcp__apify__delete-schedule", "mcp__apify__build-actor"] } }
```

Lista completa de `deny` (tasks, publish): `conexao-e-perfis.md`. Para desfazer: `claude mcp logout apify` corta a sessão; `claude mcp remove apify` apaga o registro e os tokens OAuth.

## Verificação

- Perfil carregado = perfil pedido; `call-actor` em `ask`, nunca em `allow`; um único servidor com tools da Apify.
- Nenhum token em chat, URL (`?token=` é anti-padrão), comando ou arquivo. Se o usuário colou um token no chat, trate-o como exposto: não o repita, peça para revogar ou rotacionar no Console (a rotação mantém o antigo por 24 h) e use R-A ou R-C.
- Rótulos: Verificado (sintaxe lida na doc), Não testado (nenhuma conexão real feita), Não verificável (versão do servidor sem `/mcp`).

## Formato de saída

```text
Conexão: perfil <P0-P3> · prefixo observado <mcp__apify__ | não conectado> · tools <n, lista> · versão <vX | não verificável>
Comando proposto (não executado): <comando com aspas> · Efeito: <grava em ..., telemetria ..., gasto ...>
Pendências do usuário: <autenticar em /mcp | definir APIFY_MCP_TOKEN | ligar limite em Billing › Limits>
Aguardando: "sim" para rodar o comando
```

## Gotchas

- `tools=` informado substitui o conjunto padrão inteiro; sem ele, o padrão pode mudar entre releases (V-02). Sempre fixe.
- PowerShell: a URL vai entre aspas; a vírgula de `tools=a,b` vira array e `&` quebra o comando.
- Servidor adicionado no Claude Code tem precedência sobre o conector do mesmo endpoint, mas URL com query diferente conta como **outro** servidor (duplicidade).
- Conectores do claude.ai só aparecem no Claude Code com login de assinatura; custom connectors não são verificados pela Anthropic (V-17). Com conector, o nome das tools é `mcp__claude_ai_<servidor>__…` e o `apify-researcher` não as enxerga.
- Header `Authorization` manual desliga o fallback OAuth. `${APIFY_TOKEN}` pode ser lida como vazia: use variável de nome próprio.
- Preferir variável do SO a `env` em `settings.local.json`, que o modelo consegue ler.
- Tool search do Claude Code adia as definições MCP: as tools aparecem por `ToolSearch`, não na lista inicial.

## Referências

`${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/conexao-e-perfis.md`, `seguranca-e-privacidade.md` (tokens, telemetria), `decisoes-e-tradeoffs.md`. Prompts prontos: P-02, P-20 na skill `prompts`.
