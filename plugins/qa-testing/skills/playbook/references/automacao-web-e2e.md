# Automação web e E2E

Como escolher, escrever, estabilizar e revisar testes de navegador (Playwright, Cypress, Selenium). Leia ao criar ou revisar suíte E2E, page objects, ao decidir sobre agentes de teste ou ao investigar teste intermitente. Base: V-19, V-20, V-21, V-22, V-24, V-11, V-37 (classe A/B, ver `fontes.md`) e `automacao-web.md` do brain-of-agent (MIT, condensado). **Convenção de rótulos:** o que vem das páginas oficiais lidas é Verificado; o que vem do brain (nomes de opções de versões específicas, números de versão) é **Inferido**: confirme com `npx playwright --version`, `npx cypress --version` e na documentação antes de copiar. Validado em 2026-10-10.

## Sumário

- [Escolha de ferramenta](#escolha-de-ferramenta)
- [Localizadores](#localizadores)
- [Esperas e asserções web-first](#esperas-e-asserções-web-first)
- [Isolamento, login e dados](#isolamento-login-e-dados)
- [Fixtures e Page Objects](#fixtures-e-page-objects)
- [Mock de rede](#mock-de-rede)
- [Asserções significativas](#asserções-significativas)
- [Regressão visual e depuração](#regressão-visual-e-depuração)
- [Retries, paralelismo e timeouts](#retries-paralelismo-e-timeouts)
- [Flaky em E2E: diagnóstico e causas](#flaky-em-e2e-diagnóstico-e-causas)
- [Agentes de teste do Playwright (planner, generator, healer)](#agentes-de-teste-do-playwright)
- [Reconhecimento em 5 passos](#reconhecimento-em-5-passos)
- [Cypress e Selenium em pontos](#cypress-e-selenium-em-pontos)
- [Testing Library, componente e mobile](#testing-library-componente-e-mobile)
- [Checklist de revisão de PR de E2E](#checklist-de-revisão-de-pr-de-e2e)

## Escolha de ferramenta

| Critério | Playwright | Cypress | Selenium 4 |
| --- | --- | --- | --- |
| Linguagens | TS/JS, Python, Java, .NET | só JS/TS | Java, Python, C#, Ruby, JS |
| Navegadores | Chromium, Chrome/Edge, Firefox, WebKit (build próprio) | Chrome, Edge, Firefox | qualquer um com driver, inclusive Safari real |
| Multi-aba e multi-origem | nativo | uma aba; outra origem com `cy.origin` | nativo |
| Espera | auto-wait em ações + asserções que repetem | queries e asserções repetem; ações não | manual (`WebDriverWait`) |
| Paralelismo | workers e sharding nativos | balanceamento no serviço pago; fora dele, divisão manual | Grid ou runner da linguagem |
| Vence quando | projeto novo sem restrição | time JS de front, teste de componente maduro | time Java/C#, Grid existente, Safari real obrigatório |

Linhas de comparação: Inferido (brain, out/2026). O WebKit do Playwright não é o Safari: fluxo crítico para iPhone precisa de Safari real em dispositivo ou nuvem antes do release. Migrar suíte estável só por moda raramente se paga; migre quando a dor (intermitência, tempo de CI, falta de multi-aba) custa mais que reescrever.

Organize por capacidade de negócio (pedidos, pagamento), não por tela. URL, usuário e token vêm de variável de ambiente; nada de configuração com segredo versionado.

## Localizadores

Ordem de preferência (Playwright; Testing Library tem a mesma prioridade: V-22, V-19):

1. `getByRole('button', { name: 'Finalizar compra' })`: quase tudo; se não acha, provavelmente há defeito de acessibilidade.
2. `getByLabel('CPF')`: campos de formulário.
3. `getByPlaceholder(...)`: só sem rótulo (falta de rótulo é bug).
4. `getByText('Pedido cancelado')`: conteúdo não interativo.
5. `getByTestId('status-pedido')`: sem semântica estável (célula, gráfico, texto traduzido).

```ts
// Encadeie e filtre para chegar ao elemento pelo contexto, não pela posição
const linha = page.getByRole('row').filter({ hasText: 'CAFE-250G' });
await linha.getByRole('button', { name: 'Remover' }).click();
page.getByRole('button', { name: 'Salvar', exact: true }); // não casa "Salvar rascunho"
```

- Locator do Playwright é estrito: ação em locator que casa dois elementos falha. É aviso de ambiguidade; calar com `.first()` esconde o problema.
- Evite `nth()`, XPath absoluto, classes geradas (`.css-1x2y3z`, utilitárias do Tailwind) e IDs gerados.
- Suíte em vários idiomas: texto quebra; use `data-testid` ou leia as strings do mesmo arquivo de i18n do app.
- **Conflito:** a documentação do Cypress recomenda `data-cy` (V-24); Testing Library e Playwright preferem papel e rótulo. Decisão (K6): papel/rótulo/texto primeiro, atributo de teste por último. No Cypress: `@testing-library/cypress` (`cy.findByRole`) ou `cy.get('[data-cy=...]')`.
- Selenium não localiza por papel: prefira `By.ID`, `By.NAME`, `[data-testid=...]`; XPath relativo por texto só sem alternativa.

## Esperas e asserções web-first

O Playwright espera o elemento estar anexado, visível, estável, recebendo eventos e habilitado antes de agir. Ele não sabe se *seus dados* chegaram: isso é papel da asserção (V-19).

```ts
// Frágil: lê uma vez; se a API não respondeu, compara "Carregando…"
expect(await page.getByTestId('total').textContent()).toBe('R$ 64,80');
// Robusto: repete até bater ou estourar o timeout do expect
await expect(page.getByTestId('total')).toHaveText('R$ 64,80');

// Registre a espera da resposta ANTES da ação que a dispara
const resposta = page.waitForResponse(
  (r) => r.url().includes('/api/pedidos') && r.request().method() === 'POST',
);
await page.getByRole('button', { name: 'Finalizar compra' }).click();
expect((await resposta).status()).toBe(201);

// Estado fora da tela (fila, back-end assíncrono): expect.poll
await expect.poll(async () => (await (await api.get(`/api/pedidos/${id}`)).json()).status,
  { timeout: 15_000 }).toBe('PAGO');
```

- `isVisible()`, `textContent()`, `count()` e `page.url()` são instantâneos; dentro de `expect(...)` comum viram corrida. Use `toBeVisible`, `toHaveText`, `toHaveCount`, `toHaveURL`, `toHaveValue`, `toBeEnabled`.
- `Intl` formata `R$ 64,80` com espaço não separável (U+00A0): `toHaveText` com string normaliza espaços; `toBe` sobre `textContent()` pode falhar (Inferido).
- `waitForTimeout`/`sleep`/`cy.wait(5000)` é antipadrão duplo: lento quando o sistema está rápido e curto quando está lento, e esconde a condição real. A página de boas práticas do Playwright lida **não** trata `waitForTimeout` (V-19); a proibição vem da doc do Cypress (V-24, `cy.wait(<número>)`) e da prática. Evite também `waitForLoadState('networkidle')` (Inferido: desaconselhado pela documentação do Playwright).

## Isolamento, login e dados

- **Contexto por teste:** cada teste do Playwright recebe contexto novo (cookies, storage, cache limpos). Não reaproveite `page` entre testes com `beforeAll`.
- **Login uma vez:** projeto `setup` faz login pela tela e salva `storageState`; os demais dependem dele (V-19). Um arquivo por perfil. Login pela tela tem um teste próprio, não 300 repetições. No Cypress: login programático e `cy.session()` com `validate` (V-24). Guarde `playwright/.auth` no `.gitignore`.
- **Dados por teste via API ou fábrica**, com valor único, limpeza no teardown da fixture. Massa compartilhada é causa nº 1 de falha que só ocorre em paralelo.
- **Limpeza em `beforeEach`, não só em `after`:** a limpeza em `after` pode nunca rodar se o teste aborta (V-24).
- **Conta por worker** quando criar usuário é caro: use o índice paralelo estável do runner (Playwright: `testInfo.parallelIndex`, Inferido) e não o `workerIndex`, que muda quando o worker reinicia.
- **Recurso global** (configuração da conta, feature flag): serialize só os testes que disputam o recurso; novas versões do Playwright têm mecanismo de lock por teste (Inferido: confirme na sua versão).

## Fixtures e Page Objects

Fixture (`test.extend`) entrega a cada teste o que ele declara, com preparo e limpeza no mesmo lugar. Escopo `worker` para o que é caro e seguro de compartilhar; `{ auto: true }` para o que todo teste deve ter (bloquear terceiros, coletar log).

Page Object bem feito: **métodos de intenção** (`cancelar(motivo)`, não `clicarBotaoCancelar()`); seletores em um lugar, criados no construtor (locators são preguiçosos); **asserções no teste** (o objeto expõe locators somente leitura; `expect` escondido oculta o que o teste prova); componentes para partes repetidas, recebendo um `Locator` raiz. Evite página-base com 50 métodos, herança em cadeia, `if` por ambiente e espera fixa dentro de método. A documentação do Cypress lista page objects como antipadrão (V-24); no Playwright, use com moderação (Inferido).

## Mock de rede

Use para estados difíceis (500, timeout, lista vazia, 10 mil itens, resposta lenta), terceiros fora do seu controle e telas de teste visual determinístico (V-19: não teste terceiros).

```ts
test('bloqueia a compra quando o cálculo de frete falha', async ({ page }) => {
  // Registrada ANTES da ação que dispara a requisição
  await page.route('**/api/frete**', (route) =>
    route.fulfill({ status: 503, contentType: 'application/json', body: JSON.stringify({ erro: 'indisponível' }) }),
  );
  await page.goto('/carrinho');
  await page.getByLabel('CEP').fill('01310-100');
  await expect(page.getByRole('alert')).toHaveText('Não foi possível calcular o frete. Tente novamente.');
  await expect(page.getByRole('button', { name: 'Finalizar compra' })).toBeDisabled();
});
```

Regras: a rota vai antes da ação; o handler **retorna ou dá `await` na promessa** de `fulfill` (em arrow `r => r.fulfill(...)` a promessa já é retornada, então a falta de `await` explícito não é defeito aí) e entrega corpo e `contentType` realistas. Perigos: mock que diverge do contrato real deixa a suíte verde e a produção quebrada (valide contra OpenAPI ou contrato); mockar o próprio back-end transforma o "E2E" em teste de front, então dê esse nome e mantenha alguns fluxos críticos sem mock; HAR envelhece e pode conter token e dado pessoal: sanitize antes de versionar.

## Asserções significativas

- `toBeVisible()` num toast passa até com toast de erro: verifique texto, valor e efeito persistido (consulta por API).
- Esperado calculado de forma independente (2 × R$ 24,90 + frete de R$ 15,00 do mock = R$ 64,80), nunca copiado da tela.
- Asserção negativa passa cedo demais: `not.toBeVisible()` é verdadeira antes da resposta chegar. Espere primeiro o sinal positivo de conclusão, depois verifique a ausência.
- `expect` sem `await` vira promessa solta e o teste passa sem verificar; ative a regra de lint equivalente (`eslint-plugin-playwright` tem regras para await, espera fixa e asserção web-first: Inferido).
- **Soft assertion** (`expect.soft`, V-19) continua o teste e reprova no fim: útil para vários campos independentes da mesma tela; nunca para pré-condição.

## Regressão visual e depuração

**Visual** (`toHaveScreenshot`; Inferido do brain, confirme opções na versão): mascare o que muda a cada execução (datas, IDs, avatares, carrossel); prefira captura de componente a página inteira; tolerância por `maxDiffPixels`/`maxDiffPixelRatio`; renderização muda com SO e fonte, então gere e compare no mesmo container e com a mesma versão do pacote; vale para design system, checkout, páginas impressas e e-mails; não vale para tela que muda toda semana (o time aprende a aprovar diff sem olhar). Atualize snapshot só com o diff revisado.

**Depuração:** o trace viewer (`npx playwright show-trace trace.zip`) mostra cada ação com DOM antes/depois, rede, console e linha do código: primeira ferramenta para falha de CI (V-19: trace é habilitado por padrão no primeiro retry em CI). UI mode (`--ui`), inspector (`--debug`, `page.pause()`) e `codegen` para descobrir locators. O código do codegen não deve ser aceito cru: é roteiro linear, sem fixture nem dado via API, com asserções rasas e às vezes `nth()`.

## Retries, paralelismo e timeouts

Verificado (V-21): sem retry por padrão; configure por `--retries`, `retries` no arquivo ou `test.describe.configure({ retries: 2 })`; resultados são passed, **flaky** (falhou e passou no retry) e failed; após falha o worker é descartado e um novo é iniciado, então teste falho não contamina os saudáveis; `test.describe.serial` agrupa testes dependentes, mas a página recomenda isolamento. Valores de referência (Inferido, brain; ajuste ao seu pipeline): `retries` 0 local e 1 no CI (mais que 2 esconde defeito); `expect.timeout` 5 s (10 s em ambiente lento); `actionTimeout` explícito de 10 a 15 s (sem limite por padrão, ação travada consome o teste); `globalTimeout` no CI; fluxo longo usa `test.slow()` e não aumento global; `workers` fixo no CI (container pode reportar núcleos errados; back-end de teste costuma saturar antes da máquina). `fullyParallel` exige testes de fato independentes; sharding entre máquinas (`--shard=1/4` com relatório em blob e merge). Acompanhe a taxa de flaky e, estabilizada, considere falhar o build quando um teste for flaky (a página de retries lida não cobre `--fail-on-flaky-tests`: Inferido, confira). Mais workers gerando 5xx no ambiente não é teste intermitente, é capacidade.

## Flaky em E2E: diagnóstico e causas

Skill: `flaky-triage`. Roteiro: (1) reproduza isolado e sequencial com repetição (`npx playwright test arquivo.spec.ts --repeat-each=30 --workers=1 --retries=0 --trace=retain-on-failure`; `--repeat-each` é Verificado só em V-37; confirme em `--help`), depois com 4 workers: se só falha em paralelo, é estado compartilhado ou capacidade; (2) registre a **taxa**; com zero falhas em n execuções independentes e população estável, 3/n é uma aproximação do limite superior unilateral de 95% da taxa (Inferido, do brain): 30 execuções limpas ainda são compatíveis com taxa perto de 10%; cerca de 150 estreitam para perto de 2%; (3) abra o trace da falha (`retain-on-failure`, porque `on-first-retry` grava a reexecução, que pode ter passado); (4) compare falhas (mesma linha e mensagem → corrida naquele passo; linhas diferentes → ambiente instável); (5) corrija a causa, repita a medição e só então feche. Retry e sleep não são correção.

| Causa | Sintoma | Correção |
| --- | --- | --- |
| Corrida clique × navegação | lê URL ou texto da página antiga | `await expect(page).toHaveURL(/\/pedidos\/\d+$/)` e ancore em algo exclusivo da nova página |
| Animação | "element intercepts pointer events", clique no lugar errado | esperar o estado final (`toBeHidden`); reduzir movimento se o app respeita `prefers-reduced-motion`; nunca `force: true` |
| Hidratação (SPA/Next.js) | clique sem efeito, formulário faz GET nativo, `fill` apagado | botão desabilitado até hidratar (`useState` + `useEffect`); o auto-wait de "habilitado" resolve |
| Estado compartilhado | carrinho com itens de outro teste | dados por teste via fixture; conta por worker |
| Dependência de ordem | passa na suíte, falha sozinho | cada teste cria seus dados; `serial` só para jornada de fato sequencial |
| Dados de outro teste | `toHaveCount(3)` vira 4 em paralelo | filtrar pelo dado único que o teste criou (`randomUUID().slice(0, 8)` no nome) |
| Relógio e fuso | falha perto da meia-noite ou só no CI (UTC) | fuso e relógio explícitos (`timezoneId`, `page.clock`: só controla o navegador, não o servidor) |
| Rede de terceiros | `goto` lento, widget de chat cobre o botão | fixture automática que bloqueia analytics/chat; nunca o terceiro em teste |

## Agentes de teste do Playwright

Verificado (V-20): **planner** escreve plano Markdown em `specs/`; **generator** produz testes em `tests/`; **healer** reexecuta, ajusta e entrega teste passando **ou teste pulado se julgar a funcionalidade quebrada**; `seed.spec.ts`; `npx playwright init-agents --loop=claude` (também `vscode`, `codex`, `opencode`); regenere após atualizar o Playwright.

**Guardrail (K4, Inferido):** corrija o teste **só** se a funcionalidade está correta. Se ela parece quebrada, registre falha de produto e não toque na asserção. Aceite a correção do healer só com revisão de diff, como PR de pessoa; o "teste pulado" pode mascarar regressão e contradiz a regra de que editar ou remover teste é inaceitável (V-06). Comando e riscos de instalação em `ferramentas-e-mcp.md` (T-02).

## Reconhecimento em 5 passos

Para E2E novo contra app dinâmico (V-11, Apache-2.0, destilado; o plugin documenta o comando e **não embute** o helper `with_server.py`, porque ele executa shell arbitrário via `--server`; leia o código do helper antes de executar): (1) navegar para a página; (2) esperar um elemento esperado da página (não `networkidle`, desencorajado pela documentação do Playwright) antes de inspecionar o DOM; (3) capturar screenshot e a lista de elementos interativos; (4) escolher seletores descritivos; (5) agir e conferir o resultado. Só contra local ou staging; screenshots no diretório de trabalho do projeto (não em `/tmp` do sistema). Em HTML estático, leia o arquivo e ache os seletores sem subir navegador.

## Cypress e Selenium em pontos

**Cypress (V-24, Verificado, página atualizada em 20/09/2026):** `data-cy` em vez de tag, classe ou id; sem `cy.wait(<número>)` (use alias de rede registrado antes da ação); teste só o que você controla; login programático e `cy.session()`; limpar dados em `beforeEach`; cada teste deve passar sozinho; múltiplas asserções em E2E são aceitáveis; não atribua retorno de comando a variável (a fila de comandos é assíncrona: `let id; cy.request().then(r => id = ...); cy.visit(id)` visita `undefined`; use `.then`/`.its`/alias); segredo fora do código; defina `baseUrl`; a página não cobre retries. Sem `async/await` com comandos Cypress (não são promessas) e `.then(($el) => expect(...))` não repete: prefira `.should(...)` (Inferido, brain).

**Selenium 4 (Inferido, brain):** sem auto-wait (`find_element` falha na hora): use espera explícita por condição; **nunca misture espera implícita e explícita** (tempo imprevisível; deixe a implícita em 0); `StaleElementReferenceException` significa re-renderização: localize de novo em vez de guardar o elemento; Selenium Manager resolve drivers; paralelismo via Grid ou runner da linguagem.

## Testing Library, componente e mobile

**Testing Library (V-22):** princípios: nós do DOM (não instâncias de componente), testar como o usuário usa, API simples; prioridade de queries: `getByRole` → `getByLabelText` → `getByPlaceholderText` → `getByText` → `getByDisplayValue` → `getByAltText`/`getByTitle` → `getByTestId` por último. Teste de componente escrito junto com o componente (Testing Library/Vitest no mesmo PR) é do plugin `web-frontend`; revisão de suíte, E2E, flaky e estratégia ficam aqui. Prefira componente a E2E para estados difíceis de alcançar (erro, vazio, carregando, 1.000 itens), variações de design system e interação interna (máscara de CPF); jsdom não tem layout (visibilidade por CSS, scroll e tamanho não são reais). Deixe para E2E a integração, navegação, autenticação e contrato real com o back-end.

**Mobile e matriz de navegadores:** emulação de dispositivo aplica viewport, user agent, densidade e toque, mas não reproduz Safari de iOS real, teclado virtual, área segura, gestos, CPU e memória de Android de entrada, autofill nem diálogos do sistema. Use emulação para layout responsivo no CI e valide fluxos críticos em aparelho real ou nuvem. Matriz pelos dados de acesso dos últimos 90 dias, cobrindo os motores (Chromium, WebKit, Gecko se houver público); separe "suportado" de "melhor esforço" por escrito. Ritmo comum: Chromium no PR; todos os motores + mobile emulado no noturno; dispositivo real antes do release. Testes nativos (Appium, Espresso, XCUITest, Maestro): plugin `mobile-apps`.

## Checklist de revisão de PR de E2E

Ordem de dano: falso verde > intermitência > lacuna de risco > lentidão > manutenção > estilo. Skill: `e2e-review`; agente: `test-reviewer`.

- [ ] Cada teste verifica o efeito de negócio (valor, status, dado persistido), não só que "algo apareceu"; esperado calculado, não copiado.
- [ ] Todo `expect` tem `await`; nenhuma asserção instantânea sobre algo que muda.
- [ ] Asserção negativa só depois de um sinal positivo de conclusão.
- [ ] Nenhum `waitForTimeout`, `sleep`, `cy.wait(número)` nem `force: true`.
- [ ] Localizadores por papel, rótulo ou texto (`data-*` por último); sem `nth`, XPath absoluto, classe gerada, nem `.first()` para calar ambiguidade.
- [ ] Dados criados por teste, únicos e limpos (em `beforeEach`); nada depende de ordem; roda em paralelo.
- [ ] Rodou com repetição (`--repeat-each` ou loop do comando) antes do merge; taxa registrada.
- [ ] Terceiros com stub; mock coerente com o contrato real; fluxo crítico mantém versão sem mock.
- [ ] Rotas registradas antes da ação; `fulfill` com corpo e `contentType` realistas.
- [ ] Login programático ou estado reaproveitado; sem segredo no código; pasta de estado no `.gitignore`.
- [ ] Sem `test.only` (use a proteção de CI), `skip`/`fixme` sem ticket, nem aumento de retries ou timeout sem justificativa.
- [ ] Trace habilitado no retry; page object com métodos de intenção e sem asserção escondida.
- [ ] Snapshot visual atualizado com o diff revisado, não com atualização às cegas.
- [ ] O nome descreve a regra e o nível é o certo: isso não caberia em componente, API ou unitário?
- [ ] E2E restrito às jornadas de maior valor; ambiente de teste, nunca produção.
