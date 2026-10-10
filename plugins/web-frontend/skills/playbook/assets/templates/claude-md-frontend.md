# Modelo de CLAUDE.md de raiz para projeto de frontend

Copie para o `CLAUDE.md` do projeto e substitua os colchetes pelos valores reais, lidos do `package.json` e dos scripts. Meta: menos de 60 linhas na raiz (e sempre abaixo de 200). Estrutura what/why/how (V-30, V-33). Remova linhas que o agente descobre lendo o repositório; teste por linha: "remover isto causaria um erro?". Regra nova só na segunda ocorrência de um erro. Regras por tipo de arquivo vão em `.claude/rules/*.md` com `paths`; procedimentos longos viram skills. Regras prontas com fonte: `references/claude-md-snippets.md`. Sem segredos.

````markdown
# [Nome do projeto]: frontend web

## O que é
[Produto, público, framework e versão, em 1 a 2 linhas.]

## Stack aceita (não introduzir biblioteca fora da lista sem perguntar)
UI: [lib] · estilo: [Tailwind v4 / CSS Modules / outro] · estado de servidor: [TanStack Query / loader]
formulários: [lib ou nativo] · testes: [runner] + e2e: [Playwright]

## Como verificar (comandos exatos; "pronto" exige a saída destes nesta sessão)
typecheck: [pnpm typecheck] · lint: [pnpm lint] · teste: [pnpm test] · e2e: [pnpm e2e] · build: [pnpm build]

## Regras de UI
- Toda mudança visual: capturar screenshot em 320 px e em desktop e anexar o caminho.
- Seletores de teste: role, label, texto; test-id por último.
- Nunca atualizar baseline de screenshot só para a falha sumir; classifique o diff antes.
- Sem dangerouslySetInnerHTML, v-html, {@html} ou bypassSecurityTrust* com dado externo sem sanitização.
- Acessibilidade: HTML nativo antes de ARIA; todo controle com nome acessível; foco visível; operável só com teclado.
- Leitura de código não é teste executado; sem saída de comando ou captura desta sessão, o item é "Não verificado".

## Versões (ler antes de aplicar regra de framework)
Antes de aplicar regra de Next.js, Tailwind ou Nuxt, leia package.json e a config ([cacheComponents / v3 ou v4]) e siga um único modelo.

## Documentação sob demanda (uma linha cada; leia só quando a tarefa pedir)
- docs/design-tokens.md: tokens e escala tipográfica
- docs/arquitetura-frontend.md: fronteira client/server e estratégia de cache
- .claude/rules/react.md e .claude/rules/testes.md: regras por caminho
````

## Importando AGENTS.md

Se o projeto usa `AGENTS.md` para outros agentes, mantenha o `CLAUDE.md` com a linha `@AGENTS.md` (a leitura nativa de `AGENTS.md` só ocorre quando não há `CLAUDE.md`; confira a versão do Claude Code).

## Teste de remoção

Para cada linha: "se eu apagar isto, o agente erra algo que não descobriria sozinho?" Se a resposta é não, apague. Revise o arquivo quando um erro se repetir, não por antecipação.
