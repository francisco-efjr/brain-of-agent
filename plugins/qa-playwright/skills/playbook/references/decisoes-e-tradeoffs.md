# Decisões e trade-offs

As decisões de projeto do plugin, o porquê de cada uma, os conflitos entre fontes e como foram resolvidos, e as objeções que o orquestrador decidiu. Use quando alguém perguntar "por que assim?" ou quando uma fonte externa contradisse uma regra. Fontes: V-02, V-18, V-61, conflitos 1 a 7 de `docs/research/qa-playwright/VALIDATED.md`, SYNTHESIS.

## Sumário

- [Siglas](#siglas)
- [Decisões D-1 a D-9](#decisões-d-1-a-d-9)
- [Papéis da rodada](#papéis-da-rodada)
- [Os sete conflitos resolvidos](#os-sete-conflitos-resolvidos)
- [CLI contra MCP contra teste gerado](#cli-contra-mcp-contra-teste-gerado)
- [`FUNCIONALIDADES.md` e `feature-list.json`](#funcionalidadesmd-e-feature-listjson)
- [Spec vermelho por bug de produto](#spec-vermelho-por-bug-de-produto)
- [Correção de teste contra regra de negócio](#correção-de-teste-contra-regra-de-negócio)
- [Playwright contra equivalentes nativos](#playwright-contra-equivalentes-nativos)
- [Objeções O-1 a O-10 e decisões DO-1 a DO-12](#objeções-o-1-a-o-10-e-decisões-do-1-a-do-12)
- [Mudanças do crítico](#mudanças-do-crítico)

## Siglas

`D-1..D-9` decisões do orquestrador · `PR-` princípio · `G-` guardrail (ver [seguranca-e-evidencia.md](seguranca-e-evidencia.md)) · `O-` objeção · `DO-1..DO-12` decisões do orquestrador sobre as objeções · `CR-` mudança do crítico · `BUG-NN` bug de produto achado na rodada · `S-` item de smoke do desenho (S-02, S-22 e parte de S-03 e S-04 já viraram X-22..X-26; os demais seguem pendentes) · `X-` fato verificado por execução.

## Decisões D-1 a D-9

| ID | Decisão | Porquê |
| --- | --- | --- |
| D-1 | Um plugin `qa-playwright`, licença MIT, sem `.mcp.json`, hooks nem `bin/` | Regra da casa: plugin seguro por padrão; MCP e hooks viram documentação em `ferramentas-e-mcp.md` para o usuário habilitar conscientemente |
| D-2 | Validação funcional com Playwright, funcionalidade por funcionalidade, é o jeito padrão de testar sistema com superfície web ou HTTP. Ciclo: inventário, aplicabilidade, preparar, explorar, codificar, executar com gate, registrar na matriz, comparar antes e depois | Pedido do dono: abrir e validar uma a uma. Testar "a tela" mistura estado e contexto, e o inventário é o contrato da rodada (V-17) |
| D-3 | Exploração com `npx playwright cli` do `@playwright/test` **fixado**; MCP só como alternativa | Versão igual à da suíte, evidência em arquivo e código `getByRole` pronto em cada ação (X-05, X-06). **Não** é por economia de tokens, que não tem medição rastreável (V-06, conflito 6) |
| D-4 | Instalação pré-autorizada: só `@playwright/test` exato, harness `e2e-playwright/` e Chromium no cache. O resto pede confirmação | Dá autonomia ao orquestrador sem abrir a superfície: `--with-deps`, `init-agents`, plugin ou MCP e novas dependências continuam dependendo do usuário (G-11..G-14) |
| D-5 | Alvo só local ou staging indicado | Teste funcional escreve dado; produção e terceiros ficam fora (G-01). Com confirmação explícita e a URL nomeada, só leitura (DO-8) |
| D-6 | O healer **propõe**, não aplica | O healer da Microsoft afrouxa asserção e marca `fixme` para passar (V-14); o agente tende a editar o teste em vez do produto (V-15) |
| D-7 | N/A com motivo e executor equivalente; a matriz é a mesma | Omitir a linha esconde a lacuna; trocar o executor não troca a pergunta (V-61) |
| D-8 | Proporcionalidade e teto: cerca de 15 funcionalidades exploradas e cerca de 8 com spec por rodada; `PLAYWRIGHT-COMPLETO` tira o teto | Rodada sem teto estoura custo e contexto: o agente custou US$ 15-30 por execução no experimento da Slack (V-18) |
| D-9 | Artefatos em `funcional/` da rodada; `.playwright-cli/`, `test-results/`, `playwright-report/` e `playwright/.auth/` no `.gitignore` | Evidência é dado sensível e acumula (X-15, V-24) |

## Papéis da rodada

Fonte: CR-3. A tabela "Quem faz o quê numa rodada" do `SKILL.md` do playbook é a regra vigente. O porquê: quem escreve o spec não executa a evidência nem revisa, e quem altera o status (`evidence-report`, aplicada pelo agente principal) não é quem audita (`matrix-auditor`, que confere contra um `results.json` que não gerou). Subagente não instala nada e não altera a matriz. Revisão pelo mesmo modelo reduz erro de leitura, mas não é validação externa (house #7).

## Os sete conflitos resolvidos

Fonte: `VALIDATED.md`, "Conflitos resolvidos".

| # | Conflito | Evidência | Decisão |
| --- | --- | --- | --- |
| 1 | Healer: trocar asserção e marcar `fixme` sem perguntar **ou** parar e perguntar | O healer manda "Do not ask user questions"; a CLI do mesmo produto manda "stop and ask the user" e "Never silently skip". Arquivos idênticos no pacote 1.64.0 | O plugin adota a regra da CLI, endurecida: o healer propõe e não aplica mudança que altere o significado de uma asserção. Só deriva técnica de locator ou espera, com evidência de snapshot e revisão por outro agente. Sem humano, `Bloqueado, decisão pendente` (V-14, V-15) |
| 2 | Pista AO-20: "avaliador separado e cético" no artigo da Anthropic | O artigo (26/11/2025) tem só inicializador e codificador com o mesmo prompt de sistema; o navegador é o Puppeteer MCP; `passes` é booleano que começa falso | Não vale como fato da fonte. Vale `passes` mais a regra de não editar testes. O plugin acrescenta (Inferido) evidência obrigatória, status só por execução e revisão por outro agente (V-17) |
| 3 | `networkidle`: `webapp-testing` da Anthropic **ou** Microsoft | A API marca `networkidle` como `DISCOURAGED`; o healer e `test-generation.md:405` proíbem; `running-code.md:99` da CLI o usa; `webapp-testing` manda esperar `networkidle` e `wait_for_timeout` | Vale a Microsoft. Em spec do `@playwright/test`, `networkidle` e `waitForTimeout` são proibidos. Na exploração, espere um elemento esperado (V-32) |
| 4 | Component testing: experimental **ou** estável? | Página pública: "It is stable"; pacotes `experimental-ct-*` removidos; modelo de stories com `mount` na 1.62; npm `latest` dos pacotes antigos = 1.62.1 | **Estável desde a 1.62**. A afirmação "experimental" está desatualizada (V-58) |
| 5 | Timeout de fixture e modos de trace | `test-timeouts-js.md:162` diz "no timeout", `:193` diz que a fixture divide o timeout do teste; o código do 1.64.0 decide. Trace: a lista curta do viewer tem 5 modos, `test-use-options-js.md` tem 7 | Fixture de teste divide os 30 s do teste; fixture de worker tem 30 s próprios; ambas aceitam `{ timeout: N }`. Sete modos de trace válidos (V-35, V-42, V-45) |
| 6 | MCP contra CLI contra teste gerado: quem é mais barato? | Slack mediu; o README diz "mais eficiente em tokens" sem número; o "114K × 27K" é de snippet | CLI embutida e fixada como padrão **por razões de engenharia e de política da casa**, não por token (próxima seção) |
| 7 | Node mínimo: 18, 20 ou 22? | `engines.node >= 20` nos pacotes; a doc cita 22, 24 ou 26; os READMEs do MCP e da CLI citam 18 | Mínimo técnico **20**; adotado: **22 ou superior** (V-04) |

## CLI contra MCP contra teste gerado

Fonte: V-18, V-06, conflito 6. O experimento da Slack Engineering (11/06/2026; fonte B) sustenta pouco, e o plugin diz o que sustenta:

| Configuração | Falha por fluxo (Thread Reply e Search Discovery) | Duração média | Tokens no Search Discovery |
| --- | --- | --- | --- |
| MCP | 0% e ~12% | ~5-8 min | ~3,5-3,8 M |
| CLI | ~12% e ~20% | ~9-11 min | ~6 M |
| Testes gerados | ~8% e ~48% | ~3 min incluindo a geração (execução bruta ~32 s e ~45 s) | ~7 M na geração de código |

Cada configuração foi rodada 20 vezes; custo de US$ 15-30 por execução com agente; Claude Sonnet 4.5 nos agentes e Opus 4.6 nos testes gerados. Os autores concluem que agentes complementam testes determinísticos e servem melhor à depuração e à exploração do que à CI de alta frequência.

**O que se sustenta (Inferido):** (1) o teste gerado em uma tacada foi o modo mais frágil no fluxo médio (~48%); (2) nesse experimento a CLI **não** foi mais barata em tokens que o MCP; (3) com 20 execuções, a diferença MCP contra CLI (~10 pontos) fica dentro do ruído; (4) uma empresa, um tipo de aplicação, sem multi-janela. O número "114K × 27K" não tem medição primária e um re-benchmark achou paridade (rejeitado em [fontes.md](fontes.md)).

**Consequências:** explorar antes de escrever o spec (PR-02), **gate de estabilidade** antes de "passou" (PR-05), nenhuma promessa de percentual de economia, e **medir** na rodada piloto com `/context` (S-14). Regra de método: antes de fixar um modo, rode o mesmo fluxo N vezes e meça a taxa de falha por cenário.

## `FUNCIONALIDADES.md` e `feature-list.json`

A fonte (Anthropic Engineering, 26/11/2025) prefere JSON com `passes` porque o modelo o sobrescreve menos que Markdown (V-17). O plugin escolheu **Markdown com tabela rígida** (DO-1) e compensa com processo: só a skill `evidence-report` altera status, e o `matrix-auditor` confere a matriz contra o `results.json` de uma execução que ele não fez (R-14).

Mapeamento com o `feature-list.json` do plugin `qa-testing` (Proposta), para rodadas longas em várias sessões:

| `feature-list.json` | `FUNCIONALIDADES.md` |
| --- | --- |
| `id` | `F-NN` (mesmo ID estável) |
| `description` | "Funcionalidade (ação de valor)" |
| `steps` | Passos dos cenários (seção 2) |
| `passes: true` | Status `Passou` **e** prova `spec-estável` |
| `passes: false` | Qualquer outro status, inclusive `Passou` por `exploração` |

As regras da fonte valem nas duas formas: altere só o status; nunca remova nem edite o teste; marque verde só com verificação ponta a ponta e evidência. O protocolo de execução longa multi-sessão está em `protocolo-feature-list.md` do `qa-testing`.

## Spec vermelho por bug de produto

Fonte: O-7, DO-6. Quando o spec falha porque o produto está errado:

1. O spec **continua vermelho**, sem afrouxar nada, em commit próprio (`test(e2e): F-NN reproduz BUG-NN`).
2. No modo melhoria, se a correção cabe no escopo e **não é regra de negócio**, o spec vermelho é o teste que falha antes da correção (§3.1 passo 5).
3. Sem correção na rodada, ele não conta como regressão e vira **decisão pendente**: corrigir, ou `test.fail()` com a anotação `{ type: 'issue', description: 'BUG-NN' }`.
4. A linha da matriz é `Falhou`, ligada ao `BUG-NN` com trace.

`test.fail` **roda** o teste e exige que falhe; `test.fixme` não roda; `test.skip` é para configuração em que o teste não se aplica (`test-annotations-js.md:11-13`).

## Correção de teste contra regra de negócio

Restaurar um esperado **com fonte** (requisito, documentação, teste existente ou a própria UI, por exemplo rótulo contra lista) não muda regra de negócio: a regra de negócio aplicável do §3.1 passo 4 não é invocada (DO-6). Sem fonte, trate como regra de negócio: o esperado é Suposição e a falha vira decisão pendente, não bug afirmado (PR-03, CR-6). Ordem das fontes do esperado: requisito, issue ou spec do produto; README e docs; testes existentes; coerência da própria UI.

## Playwright contra equivalentes nativos

O Playwright cobre web, Electron e Chrome ou WebView em Android (estes dois experimentais); **não** cobre UI nativa Android e iOS (V-61). Nesses casos o executor é outro e a matriz é a mesma:

- Android nativo: Compose UI test, Espresso ou UI Automator (plugin `mobile-apps`); exploração por `adb` no emulador existente, **verificada** (X-21); Appium e Maestro só com instalação confirmada.
- iOS nativo: XCUITest no simulador, só com macOS e Xcode; não verificado como fonte oficial.
- CLI e biblioteca sem HTTP: runner da linguagem. Backend e API desses sistemas continuam no Playwright `request`.

Tabela completa e texto-padrão de N/A em [escopo-e-stacks.md](escopo-e-stacks.md).

## Objeções O-1 a O-10 e decisões DO-1 a DO-12

Registro; a regra vigente está nas referências citadas.

| ID | Objeção (resumo e evidência) | Decisão do orquestrador | Onde está |
| --- | --- | --- | --- |
| O-1, DO-1 | Inventário em Markdown contra JSON (V-17) | Markdown com tabela rígida. Só a skill de evidência altera status; o auditor confere contra o `results.json` | template `FUNCIONALIDADES.md`, G-25, R-14 |
| O-2, DO-2 | O bloco de limites proíbe ler pastas ignoradas, onde fica a evidência (X-15) | Liberar a leitura de `.playwright-cli/`, `test-results/` e `playwright-report/`; `playwright/.auth/` continua proibida | G-21, S-11 |
| O-3, DO-3 | `npm i -D` gravou `^1.64.0` | `npm i -D -E @playwright/test@<versão>` e conferir o `package.json` sem `^` | [versoes-e-instalacao.md](versoes-e-instalacao.md), G-10 |
| O-4, DO-4 | "Todas recebem exploração" contra teto de ~15 | O inventário lista todas; a rodada escolhe o subconjunto (~15 e ~8) por risco e mudança; o resto "Não validado nesta rodada", com motivo | D-8, CI-09 |
| O-5, DO-5 | "Passou" sem nível de prova infla o número | Coluna Prova: `spec-estável` ou `exploração`, com totais separados | template `FUNCIONALIDADES.md` |
| O-6, DO-7 | Equivalentes nativos sem validação | Compose UI test, Espresso ou UI Automator; `adb` verificado (X-21); Appium e Maestro só com instalação confirmada | [escopo-e-stacks.md](escopo-e-stacks.md) |
| O-7, DO-6 | Onde fica o spec que falha por bug | Ver "Spec vermelho por bug de produto" | acima |
| O-8, DO-8 | Duas regras para produção | Recusar por padrão. Com confirmação explícita e a URL nomeada: só leitura, sem login real nem escrita | G-01 |
| O-9, DO-9 | Pasta fora do modo melhoria | `docs/testes/AAAA-MM-DD/funcional/` | D-9 |
| O-10, DO-10 | Nomes em PT-BR contra a casa em inglês | Skills e agentes em inglês (kebab-case); descriptions, corpo e templates em PT-BR | árvore do plugin |
| DO-11 | `show-report` pré-aprovado em V-25 | Fica fora da pré-aprovação: abre servidor e prende o agente | G-08 |
| DO-12 | A evidência de uma execução era apagada pela seguinte | `outputDir: test-results/${E2E_RUN ?? 'local'}` e HTML em `playwright-report/${E2E_RUN ?? 'local'}`; **verificado** em X-18 | [config-execucao-e-ci.md](config-execucao-e-ci.md) |

## Mudanças do crítico

Parecer: `approved_with_changes`, nota 78/100 do desenho recebido. O crítico é do mesmo fornecedor e família de modelos, então a crítica não é revisão externa. As marcas `CR-n` nas referências apontam para:

| CR | Mudança |
| --- | --- |
| CR-1 | Decisões DO-1 a DO-12 incorporadas; nomes das skills e agentes em inglês; bugs como `BUG-NN` |
| CR-2 | Evidência por execução: `test-results/${E2E_RUN ?? 'local'}` e `playwright-report/${E2E_RUN ?? 'local'}` |
| CR-3 | Papéis da rodada: orquestrador executa a evidência e aplica `evidence-report`; auditor reexecuta |
| CR-4 | Login sem senha no contexto: projeto `setup` com `trace: 'off'`, estado por porta, `state-load` por caminho, nunca `fill` de senha |
| CR-5 | `harness-setup` com `disable-model-invocation` e a condição escrita; subagente nunca a executa |
| CR-6 | Oráculo: todo cenário traz o esperado e a fonte; sem fonte, Suposição |
| CR-7 | Inventário caixa-preta: sessão de mapa do `feature-explorer`, funcionalidades como Inferido |
| CR-8 | Um explorador por vez, lotes de até 5, banco próprio por instância quando possível, estimativa de custo |
| CR-9 | §3.1 coerente: inventário e exploração das de risco alto no passo 1; specs das tocadas depois do passo 4 |
| CR-10 | §3.2 do protocolo enxuto (até ~45 linhas) |
| CR-11 | Flags perigosas proibidas por instrução dentro dos prefixos pré-aprovados; MCP configurado fora da evidência; texto da página marcado como dado na nota |
| CR-12 | Evals e itens de smoke alinhados (S-22 login, S-23 nativos, S-24 rodada simulada) |

Riscos remanescentes do desenho, atualizados com o smoke de X-22..X-26: o caminho de login inteiro (eco do `fill`, setup contra a instância de exploração, `state-load` + `goto`, `trace: 'off'`) foi **verificado** no sistema-demo (X-23), e falta confirmá-lo em sistema com SSO ou com outro mecanismo de sessão; o limite de comando dentro de um prefixo pré-aprovado vale só por instrução; a matriz em Markdown continua editável pelo modelo; o teto de 15 e 8 e o custo por rodada não foram medidos (S-14); app sem banco por instância depende de delta e dado único; as duas cópias do protocolo do orquestrador divergem (R-18).
