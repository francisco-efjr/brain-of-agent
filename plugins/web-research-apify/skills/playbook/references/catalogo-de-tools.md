# Catálogo de tools do Apify MCP

Validade: servidor `apify-mcp-server` v0.18.0 (release de 2026-10-13, commit `9ad785a6aa`; a 0.18.1 está em desenvolvimento e não foi lançada). Lido no código-fonte público e no README em 2026-10-13. **Selo: volátil.** Houve 12 ou mais releases entre 2026-09-17 e 2026-10-13 e o servidor hospedado é privado, então a lista carregada na sua sessão pode diferir desta. **Nada foi executado em runtime:** o que depende de conexão real fica como Suposição até o smoke test (`lacunas-e-smoke-test.md`).

Rótulos: **Verificado** = lido na fonte citada, na data acima (leitura, não execução) · **Inferido** = deduzido do que foi lido, sem conferir no schema da tool · **Suposição** · **Não verificável**.

Sumário: 1. Como ler · 2. Catálogo · 3. Auto-injeção · 4. Tools só por nome e nomes aposentados · 5. Argumentos que o plugin usa · 6. Limites de leitura · 7. Prefixos por origem · 8. Fora do escopo de pesquisa · 9. Como regenerar esta tabela · 10. Gotchas

## 1. Como ler

- **Padrão** = presente quando a URL não traz `tools=`. O README avisa que o padrão pode mudar entre releases; por isso o plugin manda fixar `tools=` (ver `conexao-e-perfis.md`).
- **A** = auto-injetada: entra sozinha quando a lista final tem `call-actor`, uma tool de Actor direta ou `get-actor-run` (seção 3).
- **Opt-in** = só carrega por categoria ou por nome em `tools=`.
- **Gasta créditos** refere-se a eventos de Actor ou uso de plataforma. Leitura de storage é Inferido como desprezível.
- A coluna **Perfil** diz em quais perfis de pesquisa a tool aparece (P0 a P3, definidos em `conexao-e-perfis.md`). "Fora" significa que nenhum perfil de pesquisa a carrega: não a habilite sem motivo e sem confirmar com o usuário.
- A flag `paymentRequired` do código marca elegibilidade a x402 e Skyfire, não preço.

## 2. Catálogo (fonte: `src/tools/registry.ts`, `src/utils/tools_loader.ts`, anotações em `src/tools/**/*.ts`, README; V-03, V-10, V-11, V-13)

| Tool | Categoria | Padrão? | Gasta créditos? | Escreve ou destrói? | Perfil |
| --- | --- | --- | --- | --- | --- |
| `search-actors` | actors | sim (sem auth) | não | não (somente leitura) | P1, P2 |
| `fetch-actor-details` | actors | sim (sem auth) | não | não (somente leitura) | P1, P2 |
| `call-actor` | actors | sim | **sim** (Actor de terceiro; teto só via `callOptions`, só PPE) | cria run; `destructiveHint`, `openWorldHint` | **P2** |
| `get-actor-run` | runs | A | não | não (somente leitura) | P2, P3 (injetada) |
| `get-dataset-items` | storage | A | não (leitura) | não (somente leitura) | P2, P3 (injetada) |
| `get-key-value-store-record` | storage | A | não | não (somente leitura) | P2, P3 (injetada) |
| `abort-actor-run` | runs | A | não (encerra gasto) | **sim**, aborta a run (`destructiveHint`) | P2, P3 (injetada; manter em `ask`) |
| `search-apify-docs` | docs | sim (sem auth) | não | não (somente leitura) | P0, P1, P2, P3 |
| `fetch-apify-docs` | docs | sim (sem auth) | não | não (somente leitura) | P0, P1, P2, P3 |
| `apify--rag-web-browser` | tool de Actor | sim | **sim** | tool de Actor; sem `callOptions` | P3 |
| `apify--web-fetch` | tool de Actor | sim | **sim** | idem (README: somente leitura) | P3 |
| `report-problem` | dev | condicionado: telemetria ligada e cliente fora de {claude, anthropic, local-agent-mode-apify}; **não carrega no Claude Code** | não | envia texto à Apify (`readOnlyHint` falso) | fora |
| `get-actor-list` | nenhuma | opt-in por nome | não | não (somente leitura) | fora |
| `delete-actor` | nenhuma | opt-in por nome | não | **destrói** o Actor (permanente) | fora |
| `get-actor-run-list` | runs | opt-in | não | não (somente leitura) | fora |
| `get-actor-run-log` | runs | opt-in | não | não (somente leitura) | fora (opt-in útil para diagnóstico) |
| `get-dataset` | storage | opt-in | não | não (somente leitura) | fora |
| `get-dataset-schema` | storage | opt-in | não | não (somente leitura) | fora (opt-in útil: amostra de 5 itens) |
| `get-key-value-store` | storage | opt-in | não | não (somente leitura) | fora |
| `get-key-value-store-keys` | storage | opt-in | não | não (somente leitura; máx. 10 por página) | fora |
| `get-dataset-list` | storage | opt-in | não | não (somente leitura) | fora |
| `get-key-value-store-list` | storage | opt-in | não | não (somente leitura) | fora |
| `create-actor-task` | tasks | opt-in | não direto | escreve (cria task; não publica) | fora |
| `get-actor-task` | tasks | opt-in | não | não (somente leitura) | fora |
| `update-actor-task` | tasks | opt-in | não direto | escreve | fora |
| `publish-actor-task` | tasks | opt-in | não | escreve: landing page **pública** | fora |
| `unpublish-actor-task` | tasks | opt-in | não | escreve | fora |
| `create-schedule` | schedules | opt-in | **indireto** (runs agendadas; nasce ativo no MCP) | escreve | fora |
| `get-schedule` | schedules | opt-in | não | não (somente leitura) | fora |
| `update-schedule` | schedules | opt-in | indireto | escreve (substitui todas as `actions`) | fora |
| `delete-schedule` | schedules | opt-in | não | **destrói** (`destructiveHint`) | fora |
| `get-actor-build` | builds | opt-in | não | não (somente leitura) | fora |
| `get-actor-build-log` | builds | opt-in | não | não (somente leitura) | fora |
| `get-actor-build-list` | builds | opt-in | não | não (somente leitura) | fora |
| `build-actor` | builds | opt-in | **sim** (build) | escreve; `destructiveHint` (re-aponta tags) | fora |
| `get-actor-version` | source | opt-in | não | não (somente leitura) | fora |
| `apify-api-search` | api | opt-in (sem auth) | não | não (somente leitura) | fora |
| `apify-api-details` | api | opt-in (sem auth) | não | não (somente leitura) | fora |
| `apify-api-read` | api | opt-in | não (recusa `run-sync`) | não (somente leitura) | fora (teste opcional H-05b) |
| `apify-api-write` | nenhuma | opt-in por nome | pode iniciar runs e builds | **escreve e destrói** em qualquer path; webhooks para qualquer URL | fora |
| `search-actors-widget`, `fetch-actor-details-widget`, `call-actor-widget`, `get-actor-run-widget` | widgets | só com `ui` (apps) | conforme a base | conforme a base | fora |

Contagem (Verificado): 38 tools nomeadas, 2 tools de Actor no padrão e 4 widgets. Regenere a partir do `tools/list` real (seção 9).

## 3. Auto-injeção (V-03)

- Se a lista final tem `call-actor`, **qualquer** tool de Actor direta ou `get-actor-run`, o servidor injeta `get-actor-run`, `get-dataset-items`, `get-key-value-store-record` e `abort-actor-run`.
- Sem nenhuma tool de run, nada é injetado. Exemplos: `tools=docs` e `tools=search-actors,fetch-actor-details`. Por isso P0 e P1 não têm `get-dataset-items`, e a skill de leitura de dataset precisa de P2.
- Conflito resolvido: a página de docs diz que `get-dataset-items` é "não padrão" e, na mesma frase, que o servidor a injeta com `call-actor`; o README diz "auto-injetada". Os dois estão certos: a tool pertence à categoria `storage` (fora do padrão) e é injetada quando há tool de run.
- Consequência de segurança: a injeção traz `abort-actor-run` (destrutivo para dados parciais). Em P2 ele fica em `ask`.

## 4. Tools só por nome e nomes aposentados

- **Só por nome** em `tools=`: `get-actor-list`, `delete-actor`, `apify-api-write` (e os widgets, apenas com `ui`). Nenhuma delas entra em perfil de pesquisa.
- **Aposentados** (o servidor ignora e não carrega nada): `add-actor`, `experimental`, `preview`, `get-actor-log` (virou `get-actor-run-log` na 0.16.0, mudança quebrante), `get-actor-output` (listas antigas; issue #1241). `/sse` foi removido (use a URL sem sufixo). `enableAddingActors` foi removido.
- **Não existe:** `run-actor`. O README do plugin oficial da Apify cita essa tool, mas a busca no repositório do servidor dá zero ocorrências; a real é `call-actor`. Se um material externo mandar usar `run-actor`, trate como erro do material (V-18).
- **Nome de tool de Actor direta:** `usuario/nome` vira `usuario--nome` (`apify--rag-web-browser`); acima de 64 caracteres o nome é encurtado com hash. Não fixe esses nomes em regras ou permissões sem conferir o `tools/list` (AP-14).

## 5. Argumentos que o plugin usa

Verificado = lido no código (`call_actor.ts`, `search_actors.ts`, `fetch_actor_details.ts`, `src/tools/storage/*.ts`). **Inferido** = o nome ou o formato não foi lido no schema; confirme no schema que o `ToolSearch` devolve antes de montar a chamada.

| Tool | Argumento | O que faz | Rótulo |
| --- | --- | --- | --- |
| `call-actor` | `actor` | ID ou `usuario/nome`; para MCP-Actor, `usuario/nome:tool` | Verificado |
| `call-actor` | `input` | Objeto obrigatório, conforme o schema do Actor | Verificado |
| `call-actor` | `waitSecs` | 0 a 45, padrão 30; `0` dispara e retorna. O plugin usa no máximo 30 | Verificado |
| `call-actor` | `callOptions` | `{ memory 128–32768 MB, timeout (s; 0 = sem limite), build, maxItems, maxTotalChargeUsd }` | Verificado |
| `call-actor` | `callOptions.maxTotalChargeUsd` | Teto em dólares; schema: "Pay-per-event Actors only, ignored otherwise"; não limita o trabalho | Verificado |
| `call-actor` | `callOptions.maxItems` | Só pay-per-result; legado, a issue #1403 propõe remover. Não usar | Verificado |
| `search-actors` | `keywords` | 1 a 3 termos (plataforma + tipo de dado); vazio se nada foi nomeado | Verificado |
| `search-actors` | `limit` | Máximo 10 (o nome do argumento é Inferido) | Inferido |
| `fetch-actor-details` | `actor` | Nome exato; a descrição da tool proíbe "nome plausível" | Verificado |
| `fetch-actor-details` | `output` | Seletivo, com as chaves `inputSchema`, `pricing`, `stats`, `rating` (`mcpTools` desligado por padrão). **O formato exato do argumento (objeto com booleanos ou lista) é Inferido**; os exemplos do plugin escrevem `{inputSchema, pricing}` por brevidade | Chaves Verificado · formato Inferido |
| `get-actor-run` | ID da run | Aceita o ID da run (o nome do argumento, `runId`, é Inferido) | Inferido |
| `get-actor-run` | `waitSecs` | Espera curta por run não terminal. **Inferido**: o validador leu a espera em `call-actor`; a existência e a semântica em `get-actor-run` não foram lidas no schema | Inferido |
| `get-dataset-items` | ID do dataset | Aceita o ID do dataset (o nome do argumento, `datasetId`, é Inferido) | Inferido |
| `get-dataset-items` | `limit`, `offset` | `limit` padrão 20; paginação por `offset` | Verificado |
| `get-dataset-items` | `fields`, `omit` | Seleção e exclusão de campos; ponto para aninhado. **O formato (lista ou texto separado por vírgula) é Inferido** | Ponto Verificado · formato Inferido |
| `get-dataset-items` | `clean`, `desc` | `clean=true` remove campos internos; `desc` inverte a ordem | Verificado |
| `get-dataset-schema` | (opt-in) | Amostra de 5 itens para descobrir campos antes de baixar tudo | Verificado |
| `get-actor-run-log` | `lines` | Máximo 50 (`0` = tudo; evite) | Verificado |
| `search-apify-docs` | `docSource`, `limit` | `docSource` = `apify`, `crawlee-js` ou `crawlee-py`; `limit` até 20; trecho de até 100 palavras | Verificado |
| `fetch-apify-docs` | URL | Só aceita `docs.apify.com` e `crawlee.dev` | Verificado |

Regra prática: a lista acima diz **o que procurar** no schema, não substitui lê-lo. Se o schema carregado divergir desta tabela, vale o schema, e a divergência vai para `lacunas-e-smoke-test.md`.

## 6. Limites de leitura (V-06)

| Limite | Valor | Observação |
| --- | --- | --- |
| `get-dataset-items` `limit` | padrão 20 | Acima de 50 000 bytes a resposta traz a dica "narrow with fields= or page with offset" (consultiva: não corta). O plugin usa `limit` ≤ 20 |
| `get-key-value-store-keys` | 10 por página | |
| `get-actor-run-log` `lines` | 50 | `0` devolve tudo; evite |
| `get-actor-run-list` `limit` | 10 | |
| `search-actors` | 10 | |
| `search-apify-docs` | 20 | O plugin usa 5 a 10 |
| `apify-api-search` | 20 | Fora de perfil |
| Binário de KV | 256 KB | Acima disso vira link (`MAX_INLINE_BYTES`) |
| `waitSecs` | 45 | "Vários clientes MCP" impõem teto de 60 s por requisição; o plugin usa ≤ 30 |
| Saída no Claude Code | aviso acima de 10 000 tokens; corte em 25 000 (`MAX_MCP_OUTPUT_TOKENS`); texto acima de 50 000 caracteres vai para arquivo | Verificado na doc do Claude Code |
| Claude Code, requisição HTTP | timer de max(60 s, timeout da tool, `MCP_TIMEOUT`) até o primeiro byte; timeout por tool padrão cerca de 28 h; janela ociosa de 5 min | Verificado na doc |
| Descrições e instruções de servidor | truncadas em 2 048 caracteres por padrão | V-34 |

Motivo para ler pouco: cada resultado grande consome contexto e pode ser cortado; além disso, o conteúdo raspado pode trazer texto dirigido à IA (ver `seguranca-e-privacidade.md`), e quanto menos texto bruto entra no contexto principal, menor a superfície.

## 7. Prefixos por origem (V-19, V-17, V-18)

| Origem | Prefixo da tool | Observação |
| --- | --- | --- |
| Servidor adicionado com `claude mcp add ... apify ...` | `mcp__apify__<tool>` | O nome do servidor define o prefixo; as regras `ask`/`deny` do plugin assumem o nome `apify` |
| Conector do claude.ai visível no Claude Code | `mcp__claude_ai_<servidor>__<tool>` | Só com login de assinatura claude.ai |
| Servidor de plugin (inclui o plugin oficial da Apify) | `mcp__plugin_<plugin>_<servidor>__<tool>` | O nome exato do plugin oficial é Inferido; o `tools` do agente do plugin oficial pode não casar (lacuna 12) |

Detecte por `ToolSearch` com os nomes `search-actors`, `fetch-actor-details`, `call-actor`, `get-actor-run`, `get-dataset-items`, `search-apify-docs`, `apify-api-write`, `report-problem`, `delete-actor` e derive o prefixo do que voltar. Mais de um prefixo com tools da Apify indica duplicidade (servidor manual, conector, plugin oficial).

## 8. Fora do escopo de pesquisa e por quê (V-10, V-12, V-28)

- **Resources MCP e `apify-api-*`:** `resources/read` lê qualquer GET em `api.apify.com/v2/...` com o token da sessão (até 256 KB inline). `apify-api-write` faz POST, PUT, PATCH e DELETE em qualquer path, com `openWorldHint`, e "starts runs and builds, and creates webhooks that call any URL": é um canal de saída. Issue #1524 (aberta): `resources/read` ainda envia override de método; prefira `get-dataset-items`.
- **Tasks, schedules, builds:** estado recorrente ou público (`publish-actor-task` cria landing page pública; `create-schedule` nasce ativo). Pesquisa pontual não precisa; monitoramento recorrente é assunto de `/automation-integrations:scheduling-headless-jobs`.
- **Pagamento agêntico (x402, Skyfire, AGI):** o plugin só menciona. Mover dinheiro ou credencial financeira é decisão do usuário, fora do plugin.
- **`report-problem`:** envia texto à Apify; não carrega no Claude Code por padrão.

## 9. Como regenerar esta tabela a cada release (V-13)

1. Conecte com o perfil desejado (`tools=` fixo) e confirme a lista com `/mcp` ou `ToolSearch`.
2. Para o catálogo completo, use um perfil temporário com as categorias desejadas e compare nomes, categorias e anotações com a tabela da seção 2. Reverta o perfil depois.
3. Registre a versão do servidor (`serverInfo.version`) quando o `/mcp` ou o log de debug a mostrarem; se não aparecer, escreva "versão: não verificável" (Suposição sobre onde a versão fica visível).
4. Atualize a data de validade no topo e marque o que mudou (nome aposentado, tool nova, anotação diferente).
5. Reconfira o texto de `nextStep` (as issues #1559 e #1558 pedem para remover textos que mandam re-rodar; a 0.18.1 reescreve alguns).

## 10. Gotchas do catálogo

- `tools=` informado **substitui** o conjunto padrão inteiro (V-02).
- Nos perfis de pesquisa, `get-dataset-items` só aparece por auto-injeção (com `call-actor`, tool de Actor ou `get-actor-run`); fora deles, também entra pedindo a categoria `storage` ou o nome em `tools=` (V-03).
- Tool de Actor direta (`apify--...`) não aceita `callOptions`: sem teto em dólares (V-04, V-05).
- `report-problem` ausente é o esperado no Claude Code (V-11).
- Tools adiadas pelo tool search do Claude Code só aparecem por `ToolSearch` (V-34).
- Lista de tools de blog ou de material de terceiros pode trazer nomes que não existem (`run-actor`, `get-actor-log`): confira no `tools/list` (V-13, V-18).
