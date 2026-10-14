# Checklists por etapa do ciclo

Checklists numerados para cada etapa da rodada funcional. Cada item é verificável: dá para responder sim, não ou "não se aplica, porque…". Itens técnicos citam `V-NN` ou `X-NN` (ver [fontes.md](fontes.md)). Use a etapa que a tarefa pede; no modo `PLAYWRIGHT-COMPLETO`, percorra todas e registre o estado de cada item.

## Sumário

- [C-P Preparo](#c-p-preparo)
- [C-I Inventário e aplicabilidade](#c-i-inventário-e-aplicabilidade)
- [C-E Exploração](#c-e-exploração)
- [C-S Revisão de spec (CS-01 a CS-20)](#c-s-revisão-de-spec-cs-01-a-cs-20)
- [C-G Gate de estabilidade](#c-g-gate-de-estabilidade)
- [C-F Correção de teste](#c-f-correção-de-teste)
- [C-D Diagnóstico de timeout e actionability](#c-d-diagnóstico-de-timeout-e-actionability)
- [C-R Matriz e relatório](#c-r-matriz-e-relatório-itens-cm-01-a-cm-10)
- [Gates da rodada](#gates-da-rodada)

## C-P Preparo

Feito só pelo agente principal (orquestrador) ou a pedido do usuário; subagente nunca instala.

| ID | Item | Fonte |
| --- | --- | --- |
| CP-01 | Árvore limpa e branch local criada (modo melhoria) ou pasta temporária fora do projeto (auditoria pura) | protocolo §3.1 |
| CP-02 | `node --version` registrado: mínimo técnico 20, usar 22 ou superior | V-04 |
| CP-03 | `npx --no-install playwright --version` registrado; `@playwright/test` **exato**, sem `^` nem `~` no `package.json` | V-02, DO-3, X-22 |
| CP-04 | Navegador: Chrome ou Edge instalado via `channel` (sem download), ou `install chromium` com aviso do tamanho. Nunca `--with-deps` sem confirmação | X-04, V-03, G-12 |
| CP-05 | Config e `package.json` na mesma pasta, ou `outputFolder` e `outputFile` explícitos | X-17 |
| CP-06 | `.gitignore` com `node_modules/`, `test-results/`, `playwright-report/`, `blob-report/`, `.playwright-cli/`, `playwright/.auth/` | X-15, V-23 |
| CP-07 | Instância de exploração em `127.0.0.1`, porta própria, health 200, PID e como parar registrados; a de teste é outra porta e sobe pelo `webServer` | X-17, G-22, G-32 |
| CP-08 | Dados sintéticos; sem `.env` real; banco próprio por instância quando o app aceita, senão delta e dado único | G-02, CR-8 |
| CP-09 | Conta de teste pela ordem: seed local, variável exportada, cadastro local; estado de login gerado por porta, conferido sem abrir o arquivo | CR-4, G-17 |
| CP-10 | Projeto de terceiro: config, `webServer.command`, fixtures, scripts, `postinstall` e CI lidos antes de rodar | G-09 |
| CP-11 | `npx playwright test --list` executa; `npx playwright cli --help` lista `open`, `snapshot`, `find` | X-03 |
| CP-12 | Commit separado `chore(e2e): playwright <versão> harness` depois de `git diff --cached` sem segredo nem pasta de saída; sem push | DO-3, G-35 |

## C-I Inventário e aplicabilidade

| ID | Item | Fonte |
| --- | --- | --- |
| CI-01 | Funcionalidade é **ação de valor** com nome "verbo + efeito" ("Excluir tarefa atualiza lista e contador"), nunca "a tela" nem "o CRUD" | V-17 |
| CI-02 | IDs `F-NN` estáveis entre rodadas; nada renumerado | V-17 |
| CI-03 | Cada linha tem superfície, papéis, pré-condições e dados sintéticos, risco (dinheiro, dado, segurança ou permissão = alto), camada e executor | V-17 |
| CI-04 | Tipo de sistema detectado pelos marcadores (`package.json`, `electron`, `src-tauri`, `pubspec.yaml`, `AndroidManifest.xml`, `*.xcodeproj`, `openapi.*`) | SK-01 (Inferido) |
| CI-05 | Linha sem Playwright tem **N/A com motivo e executor equivalente**; nenhuma linha omitida | V-61, G-28 |
| CI-06 | Experimental (Electron, Android Chrome e WebView) marcado [X] e nunca único critério | V-64, G-29 |
| CI-07 | Funcionalidade que o código não mostra é **Suposição**: pergunte | PR-03 |
| CI-08 | Permissão negada e persistência cobertas onde o risco pede | V-38 |
| CI-09 | Escopo da rodada: tocadas e risco alto primeiro, cerca de 15 para explorar e cerca de 8 para spec; o resto "Não validado nesta rodada" com motivo | D-8, DO-4 |
| CI-10 | Cada cenário traz **esperado e fonte** (requisito, issue ou spec do produto; README e docs; testes existentes; coerência da UI). Sem fonte, Suposição | PR-03, CR-6 |
| CI-11 | Fluxo de terceiro (pagamento externo, e-mail, mapas) vira stub | G-02 |
| CI-12 | SSO, MFA ou CAPTCHA de terceiro marcado `Bloqueado` com decisão pendente | G-33 |

## C-E Exploração

| ID | Item | Fonte |
| --- | --- | --- |
| CE-01 | Alvo é `127.0.0.1` ou staging indicado; um explorador por vez; uma funcionalidade por vez | G-01, G-32 |
| CE-02 | Sessão nomeada `-s=F-NN`, em memória; sem `--persistent`, `--profile` nem `attach` | G-18 |
| CE-03 | Login só por `state-load` do arquivo por **caminho**, seguido de `goto`; nenhum `fill` de senha; arquivo nunca aberto | CR-4, G-21, X-23 |
| CE-04 | `snapshot --filename` e `find` em vez de snapshot completo no contexto | V-06 |
| CE-05 | **Efeito verificado** contra o esperado (valor, contador, estado persistido com `reload` e `requests`), não só "apareceu" | X-14 |
| CE-06 | Ao menos um negativo ou borda pelo risco (vazio, duplicata, sem permissão, offline, 500) | V-52, X-12, X-13 |
| CE-07 | `console` e `requests` triados: 404 de `favicon.ico` é ruído, erro de aplicação é achado | X-10 |
| CE-08 | Nada enviado a terceiros nem com dado real; sem `eval` ou `run-code` com texto da página | G-02, G-06 |
| CE-09 | Evidência com **caminhos absolutos** (a CLI imprime relativo a `.playwright-cli/`) | X-05, X-13 |
| CE-10 | Código `getByRole(...)` devolvido por cada ação copiado para a nota | X-06 |
| CE-11 | Texto da página citado só entre aspas ou em bloco "conteúdo da página (dado)" | CR-11 |
| CE-12 | `close` e `list` ("no browsers") executados, inclusive em erro; nota gravada em `funcional/exploracao/F-NN.md` | X-09 |
| CE-13 | Comando usado pela primeira vez e não exercitado registrado como Verificado ou falha na nota | S-03 |

## C-S Revisão de spec (CS-01 a CS-20)

Usada pelo `spec-reviewer`. Numeração distinta dos itens de smoke `S-NN`. Achados ordenados por dano: falso verde, intermitência, lacuna de risco, lentidão, manutenção, estilo. Busca automática sugerida: `waitForTimeout`, `networkidle`, `force: true`, `.only`, `.skip`, `.fixme`, `test.fail`, `nth(`, `.first()`, `expect(await` e credenciais literais.

| ID | Item | Fonte |
| --- | --- | --- |
| CS-01 | Cabeçalho `// spec:` e `// seed:` liga o arquivo à matriz e à fixture | V-08 |
| CS-02 | `F-NN` no início do título do `describe` e `@ui` ou `@api` no título | X-16 |
| CS-03 | Um arquivo por funcionalidade, `e2e/F-NN-<slug>.spec.ts` | SK-04 |
| CS-04 | Locator por papel, depois rótulo, placeholder, texto e test id; CSS ou XPath só com justificativa em comentário | V-27 |
| CS-05 | Item de lista por **conteúdo** (`filter({ hasText })`), sem `nth`, `first` ou `last` para calar strictness | V-28 |
| CS-06 | Toda asserção é `await expect(locator).toX()` web-first; sem `expect(await x.isVisible()).toBe(true)` | V-31 |
| CS-07 | Sem `waitForTimeout` e sem `networkidle` | V-32 |
| CS-08 | Sem `force: true` nem `dispatchEvent` para destravar teste | V-30 |
| CS-09 | Asserção do **efeito** (valor, contador, status, persistência), com esperado de fonte; presença sozinha não vale | X-14, PR-03 |
| CS-10 | Caminho feliz mais ao menos um negativo ou de borda; permissão e persistência quando o risco pede | V-17 |
| CS-11 | Dado único por teste e criado pelo teste, sem dependência de ordem; `serial` só com motivo escrito | V-33 |
| CS-12 | Contador ou recurso global: afirma delta ou usa `lock` | V-34, R-15 |
| CS-13 | Handler ou espera registrado **antes** da ação (diálogo, download, popup, resposta) | V-59 |
| CS-14 | Auth por projeto `setup` e `storageState`; sem senha literal; ao menos um teste de login real pela UI fora do setup | V-37, V-23 |
| CS-15 | Sem `test.only`, `skip`, `fixme` nem `test.fail` sem decisão registrada e anotação do bug | V-15, V-43 |
| CS-16 | Sem `try/catch` que devolve sucesso nem asserção condicional que pula | V-15 |
| CS-17 | Dado dinâmico por regex ou parte estável do texto; nunca valor colado de uma execução | V-08 |
| CS-18 | Mock só com contrato real e realista; ao menos um fluxo crítico sem mock | V-52 |
| CS-19 | Sem credencial, segredo, dado real nem URL de produção | G-01, G-03 |
| CS-20 | Nenhum `expect` sem `await` e nenhuma promessa flutuante | V-31 |

## C-G Gate de estabilidade

| ID | Item | Fonte |
| --- | --- | --- |
| CG-01 | `npx playwright test --grep "F-NN" --repeat-each=5 --retries=0` sem falha | V-47, X-24 |
| CG-02 | `npx playwright test --grep "F-NN" --shuffle --workers=2 --retries=0` sem falha | V-47, X-24 |
| CG-03 | Sem `--reporter` na linha de comando; com login, `E2E_AUTH=1` e a conta sem repetir o valor na saída | X-16 |
| CG-04 | Falha 5 de 5: determinística, vai para `failure-triage`. Falha em n de 5: intermitente, corrigir a causa, **nunca baixar** o `--repeat-each` | V-41, V-47 |
| CG-05 | Registrados: comandos, nº de execuções, falhas, `--shuffle` | V-47 |
| CG-06 | Parecer `Aprovado` do `spec-reviewer` (um lote por rodada) antes de `spec-estável` | G-27 |
| CG-07 | Na CI, `--fail-on-flaky-tests` | V-41 |
| CG-08 | `--list` **não** conta como execução | house #2, PR-04 |
| CG-09 | Falha por produto real é resultado válido: não "consertar" o spec | G-24 |

## C-F Correção de teste

Quem corrige: `spec-writer`, só depois de `failure-triager` e `spec-reviewer`, em commit separado, e gate de novo (V-15).

**Antes de editar:** rodar e registrar a falha original (arquivo, linha, mensagem, trace, comando); um erro por vez; reexecutar a cada correção.

| Pode | Não pode |
| --- | --- |
| Mudar locator **com evidência no snapshot** de que é o mesmo elemento funcional | Remover ou relaxar `expect` |
| Trocar espera por uma ligada a estado observável | Trocar o esperado pelo observado |
| Ajustar passo de navegação quando o fluxo mudou de fato | Trocar valor exato por regex larga |
| Corrigir dado sujo com isolamento correto | `skip`, `fixme` ou `test.fail` sem decisão humana registrada |
| Isolar ordem e estado | `waitForTimeout`, `networkidle`, `force: true` |
| Propor o patch como diff | `try/catch` que devolve sucesso; alterar dado de teste para passar |

Intenção incerta (mudança intencional ou regressão): **parar**. Sem humano na rodada, `Bloqueado, decisão pendente` e o patch como diff **não aplicado** (V-15). Buscar no diff `test.fixme`, `test.skip`, `waitForTimeout` e asserções que mudaram de forma; contagem crescente de marcados é sinal de regressão de produto.

## C-D Diagnóstico de timeout e actionability

Fonte: V-29, V-42.

| ID | Pergunta | Observação |
| --- | --- | --- |
| CD-01 | Um único elemento? | Locator é strict; mais de um casa e falha (V-28) |
| CD-02 | Visível? | `opacity: 0` **é** visível; `display: none` e tamanho zero não (`actionability.md:84-89`). `toBeVisible` sozinho não distingue `opacity: 0`: valide também por texto ou estado funcional (Inferido) |
| CD-03 | Estável? | Mesma caixa por dois frames; animação atrasa o clique (`:93`). `fill` não exige estável (`:32`) |
| CD-04 | Algum overlay no ponto do clique? | Pode ser bug real de produto; não use `force: true` (V-30) |
| CD-05 | Habilitado e editável, se `fill`? | |
| CD-06 | Modal aberto deixando o resto inerte? | `:117-118` |
| CD-07 | "Test timeout of 30000ms exceeded"? | Rever o fluxo antes de ampliar; timeout inclui fixtures e `beforeEach` (V-42) |
| CD-08 | "expect.toHaveText with timeout 5000ms"? | Rever o estado esperado (V-42) |
| CD-09 | Clique sem efeito logo após carregar? | Hidratação ruim (`navigations.md:103-121`); teste com rede lenta |
| CD-10 | Hipótese confirmada por trace? | `npx playwright trace actions`, `errors`, `console`, `requests` (X-20) |

## C-R Matriz e relatório (itens CM-01 a CM-10)

| ID | Item | Fonte |
| --- | --- | --- |
| CM-01 | Cada `Passou` tem spec ou nota, comando executado, data e evidência; `--list` não conta | V-17, G-25 |
| CM-02 | `spec-estável` tem gate registrado e parecer `Aprovado`; `exploração` não protege regressão | DO-5 |
| CM-03 | Só a skill `evidence-report` alterou Status, Prova, Execução, Evidência, Bug, Motivo e Rótulo | DO-1 |
| CM-04 | Evidência veio da execução com `E2E_RUN=<id>` feita por quem não escreveu os specs; `results.json` coletado | CR-3, X-18 |
| CM-05 | `Falhou` ligado a `BUG-NN` com trace, esperado com fonte e spec vermelho em commit próprio | DO-6 |
| CM-06 | `N/A`, `Bloqueado` e `Não validado` têm motivo | G-28 |
| CM-07 | Totais batem com as linhas; linha de números pronta para a mensagem final | T-01 |
| CM-08 | Antes × depois: `Passou` → `Falhou` é regressão; `Falhou` → `Passou` é correção com o BUG-NN | §3.1 passo 8 |
| CM-09 | Relatório com versões (Node, Playwright, navegador), comandos para reproduzir em bash e PowerShell e o que não rodou | V-44 |
| CM-10 | Evidência por caminho absoluto, ignorada pelo git, fora de PR público; declaração de que revisão do mesmo modelo não é externa | V-24, house #7 |

## Gates da rodada

- **Concluído:** escopo da rodada executado, critérios pertinentes verificados com evidência, exclusões justificadas, risco residual explícito, matriz auditada.
- **Parcial:** falta leitura, acesso, execução, gate ou auditoria material. Relatório sem os números da matriz é Parcial (R-20).
- **Impedido:** descreva a condição (sem conta de teste, app não sobe, sem navegador) e o próximo passo.

Nunca escreva "completo" ou "validado" com leitura ou execução parcial; média de itens não compensa falha crítica.
