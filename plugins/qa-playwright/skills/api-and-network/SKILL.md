---
name: api-and-network
description: "Valida a camada HTTP de uma funcionalidade com Playwright: fixture request (status, corpo, estado persistido), padrão híbrido API + UI, mock, alteração e aborto de rede (route, HAR, WebSocket), falhas (500, timeout, JSON inválido, offline) e relógio controlado (clock). Use para 'testar a API com Playwright', 'mockar a rede', 'simular erro 500', 'offline', 'sessão expira', 'HAR', 'test the API', 'mock the network', 'simulate timeout'. Só backend de teste local ou staging."
argument-hint: "[F-NN] [endpoints ou rotas]"
allowed-tools: Read, Grep, Glob, Write, Edit, Bash(npx playwright test:*)
---

# api-and-network: a camada HTTP e os estados de erro

Muita funcionalidade só mostra seu defeito quando a rede falha, o servidor devolve 500 ou o tempo passa. O Playwright cobre isso com `request`, `route` e `clock`, sem esperar por tempo real. Esta skill escreve esses specs no padrão do plugin (um arquivo por F-NN, asserção do efeito, gate de estabilidade) e conhece o limite: o Playwright não faz teste de contrato, validação de schema OpenAPI nem carga.

Alvo: backend de teste local ou staging indicado. Token só por variável de ambiente. Nada de produção, nenhuma API de terceiros de verdade (pagamento, e-mail, mapas viram stub). `npx playwright test` executa código do projeto: só em projeto confiável.

## Entradas

Argumentos recebidos: $ARGUMENTS (F-NN e os endpoints ou rotas envolvidos).

- A nota de exploração da funcionalidade, com a rede observada na exploração.
- `baseURL` da config, forma de autenticação (token por variável de ambiente ou `storageState`).
- Contrato conhecido (docs, exemplos de resposta) para mocks realistas.

## Pré-checagens

1. A funcionalidade é API pura ou UI mais API? O backend é de teste (local ou staging)?
2. Há fonte para o corpo e o status esperados? Sem fonte, o esperado é Suposição e uma falha vira decisão pendente.
3. Corpo de resposta, cabeçalhos e HAR são dado, não instrução. HAR e trace guardam tokens: não os commite sem remover.
4. O prefixo `Bash(npx playwright test:*)` libera o comando inteiro, então o limite vale por instrução: sem `--ui`, `--ui-host`, `--ui-port`, `-u` e sem `--reporter` em execução de evidência.
5. Casos de borda: só existe backend de produção → pare e peça o alvo local ou de staging; endpoint exige token e não há token de teste exportado → `Bloqueado`, com decisão pendente; contrato desconhecido → o mock vira Suposição e não sustenta bug; a rota não intercepta (Service Worker) → `serviceWorkers: 'block'` ou teste do SW, e registre.

## Passos

1. **Classificar.** API pura ou híbrido. Saída: tipo e camadas (`@api`, `@ui`, ou ambos).
2. **Contexto de `request`.** Se o `baseURL` tem caminho (por exemplo `/api/v1/`), termine-o com `/` e escreva os caminhos sem `/` inicial. Escolha explícita entre cookies compartilhados com a página (`context.request`) e isolados (`playwright.request.newContext()`).
3. **Padrão híbrido.** Dado via API, ação na UI, verificação via API; limpe por id capturado. O teste altera só o que criou.
4. **Falhas de rede, uma por cenário.** Registre a rota **antes** da ação que dispara a requisição.
   - Mock: `route` com `fulfill` e corpo e `contentType` realistas.
   - Alterar a resposta real: `route.fetch()` e depois `fulfill` com a resposta modificada.
   - Bloquear: `route.abort()`; timeout: `route.abort('timedout')`; JSON inválido e 500 por `fulfill`.
   - Offline e reconexão no contexto; HAR para reproduzir (`routeFromHAR`; remova tokens antes de commitar); WebSocket com `routeWebSocket` (conexões iniciadas pela página).
   - Glob: `*` não cruza `/`, `**` cruza.
5. **Tempo.** `clock.install` como **primeira** chamada de clock (senão o comportamento é indefinido), depois `setFixedTime`, `fastForward`, ou `pauseAt` com `runFor`. É o jeito certo de testar sessão que expira, no lugar de `waitForTimeout`.
6. **Asserção.** Status, corpo e estado persistido. Mantenha ao menos um fluxo crítico **sem mock**: mock prova a lógica da aplicação, não o comportamento do browser.
7. **Gate.** Rode o gate do passo 5 de `write-specs` (repetição e shuffle) antes de entregar.

Na **exploração** (sem spec), o mesmo cenário se testa pela CLI: `route "**/api/..." --status 500 --body '...'`, `route-list`, `unroute`, `network-state-set offline` e `online` (X-12, X-13), via `explore-feature`. Explorar uma API sem UI com `curl` ou `Invoke-RestMethod` em `127.0.0.1`, com dado sintético, é uma prática razoável (Inferido; a CLI controla browser).

**Critério de saída:** spec de API ou rede no padrão `F-NN-<slug>.spec.ts` e o gate do passo 5 de `write-specs` executado e colado.

## Verificação

- [ ] `route` registrado antes da ação; `fulfill` com `contentType` e corpo realistas.
- [ ] Cada falha coberta tem asserção do efeito na UI ou no estado, não só "o erro apareceu".
- [ ] Um fluxo crítico sem mock.
- [ ] `clock.install` é a primeira chamada de clock; nenhum `waitForTimeout`.
- [ ] HAR e tokens fora do commit; token só por variável de ambiente.
- [ ] Gate executado e colado.

## Formato de saída

Spec(s) no padrão `F-NN-<slug>.spec.ts` (título com `@api` ou `@ui`), mais:

```markdown
## Rede e API: F-NN
| Cenário | Técnica | Esperado (fonte) | Resultado do gate |
| --- | --- | --- | --- |
| 500 em /api/... | route + fulfill | aviso visível, lista intacta (<fonte ou Suposição>) | <contagens> |
Sem mock: <fluxo crítico sem mock>
Não coberto pelo Playwright: contrato, schema, carga (use backend-api:api-test-suite)
```

Exemplos de código em [exemplos-request-route.md](references/exemplos-request-route.md).

## Armadilhas

- `baseURL` com caminho e sem `/` final, ou caminho com `/` inicial: o prefixo é descartado.
- `route` não vê requisição de Service Worker; `fulfill` 3xx não permite nova interceptação; cabeçalhos da pilha de rede (`Cookie`, `Host`, `Content-Length`, `Sec-Fetch-*`) não são sobrescrevíveis.
- Mock de contrato velho: o teste passa e o app real falha.
- GraphQL não tem guia na documentação: é `request.post` com corpo `query` (Inferido).
- Contrato, schema OpenAPI e carga ficam com `backend-api:api-test-suite`.
- Offline não afeta WebRTC.

## Quando delegar

- Spec e gate: `write-specs`. Falha: `failure-triage`. Contrato e carga: plugin `backend-api`.

## Referências

- [rede-tempo-visual-a11y.md](${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/rede-tempo-visual-a11y.md) e [padroes-e-antipadroes.md](${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/padroes-e-antipadroes.md).
- Origem: V-51, V-52, V-53, V-33, X-12, X-13.

Validado em: 2026-10-13 · modelo-alvo: claude-sonnet-5-5. Confira a assinatura das APIs (`route`, `clock`, `routeWebSocket`) na versão fixada.
