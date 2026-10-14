# Versões e instalação

Como fixar a versão do Playwright, o que cada passo de instalação altera, qual navegador usar e o que muda entre versões. Fontes: V-02, V-03, V-04, V-48, V-49, X-01, X-02, X-04, X-22. Quem instala é o agente principal (orquestrador) sob o §3.2 ou a pedido do usuário; **subagente nunca instala** (G-11). A skill `harness-setup` (`${CLAUDE_PLUGIN_ROOT}/skills/harness-setup/SKILL.md`) executa estes passos.

## Sumário

- [Política de versão](#política-de-versão)
- [Passo a passo da instalação](#passo-a-passo-da-instalação)
- [Navegador](#navegador)
- [Node](#node)
- [O que é pré-autorizado e o que pede confirmação](#o-que-é-pré-autorizado-e-o-que-pede-confirmação)
- [Registrar versões na rodada](#registrar-versões-na-rodada)
- [Atualizar a versão](#atualizar-a-versão)
- [Notas de release 1.55 a 1.64 que mudam a suíte](#notas-de-release-155-a-164-que-mudam-a-suíte)
- [Docker e CI](#docker-e-ci)
- [Rede corporativa](#rede-corporativa)

## Política de versão

1. **Fixe `@playwright/test` com versão exata** (sem `^` nem `~`) e use o `npx playwright cli` e o `npx playwright mcp` **desse pacote** (V-02, G-10). A versão verificada em 13/10/2026 foi a 1.64.0 (X-01).
2. **Nunca `@latest`.** `@latest` muda a cada execução. O plugin oficial `playwright` do Claude Code usa `npx @playwright/mcp@latest` (V-02). O npm `@playwright/mcp` 0.0.83 e `@playwright/cli` 0.1.22 dependem de `playwright` e `playwright-core` em `1.64.0-alpha-1790635538000`, não do 1.64.0 (V-02).
3. Registre a versão no relatório da rodada (`npx playwright --version`, Node, navegador). Relatório sem versões é incompleto (SK-08).
4. Projeto que já tem Playwright: **mantenha a versão dele**; suba só a pedido (V-49, SK-02 passo 3).
5. Atualize por PR com lockfile e `npm ci` (V-02), regenerando os arquivos do `init-agents` se o usuário os usa.

## Passo a passo da instalação

O `npm i -D` grava `^` por padrão: o `package.json` do harness do orquestrador ficou com `"@playwright/test": "^1.64.0"` (R-05, verificado). Por isso o `-E` e a conferência.

Bash:

```bash
node --version && npm --version && npx --no-install playwright --version   # registrar; o último falha se ainda não instalado
npm view @playwright/test version                                          # leitura: versão estável do dia
npm i -D -E @playwright/test@<versão>                                      # -E é --save-exact do npm
grep '"@playwright/test": "[~^]' package.json                              # sem resultado = sem ^ nem ~
```

PowerShell:

```powershell
node --version; npm --version; npx --no-install playwright --version
npm view @playwright/test version
npm i -D -E @playwright/test@<versão>
Select-String -Path package.json -Pattern '"@playwright/test": "[~^]'      # sem resultado = sem ^ nem ~
```

Se o `package.json` ficou com `^` ou `~`, corrija à mão e rode `npm install` de novo. `-E` equivale a `--save-exact` do npm. Verificado (X-22): `npm i -D -E @playwright/test@1.64.0` gravou `"@playwright/test": "1.64.0"`, sem `^`, e, apagando `node_modules`, `npm ci` reproduziu a instalação (3 pacotes). Confira o arquivo de qualquer forma: uma configuração de npm do usuário pode mudar o padrão.

O que muda e o que não muda: `npm i -D @playwright/test@1.64.0` adicionou 3 pacotes em 4 s e **não baixou navegador** (verificação do orquestrador). Altera `package.json` e o lockfile; faça commit **separado**: `chore(e2e): playwright <versão> harness`, depois de `git diff --cached` sem segredo nem pasta de saída. Sem push.

Onde instalar:

| Situação | Onde |
| --- | --- |
| Projeto JavaScript ou TypeScript | devDependency do projeto |
| Sem `package.json` ou sistema não JS (Java, Python, .NET, Go) | pasta `e2e-playwright/` com `package.json` e lockfile próprios (modelo em `assets/templates/harness-package.json`) |
| Auditoria pura, sem tocar o projeto | pasta temporária fora do projeto; nada é commitado |
| Projeto com Playwright já instalado | mantenha a versão; use a dele |

Verificar depois de instalar: `npx playwright --version` igual ao `package.json`; `npx playwright cli --help` lista `open`, `snapshot`, `find` (X-03); `npx playwright test --list` executa.

## Navegador

Fonte: V-03, X-04.

1. **Chrome ou Edge instalado:** `channel: 'chrome'` ou `'msedge'` na config (`PW_CHANNEL`) e `--browser=chrome` ou `--browser=msedge` na CLI. **Sem download** (X-04). É o padrão do plugin. Chrome e Edge foram usados nas verificações.
2. **Sem eles:** `npx playwright install chromium` baixa algumas centenas de MB para `%USERPROFILE%\AppData\Local\ms-playwright` no Windows. Avise o tamanho antes. O "281 MB" que circula é a **amostra** de um `du -hs` em macOS (`browsers.md:965`), e o texto diz "a few hundred megabytes": cite assim (V-03). Use `PW_CHANNEL=chromium`.
3. **`install-deps` e `--with-deps`** pedem sudo ou administrador ("will ask for sudo permissions", X-02): só com confirmação do usuário. No Windows, o comportamento sem elevação não está documentado: **não eleve** (V-03, lacuna 4, G-12).
4. `PLAYWRIGHT_BROWSERS_PATH` não afeta Chrome e Edge (`browsers.md:1120`). Registre a versão do navegador na evidência.
5. WebKit **não é Safari**; Firefox acompanha o Firefox estável sem build de marca (V-50, `browsers.md:584, 590`). Para iOS Safari real, não há suporte (escopo-e-stacks).
6. Extensão Chrome precisa do Chromium empacotado (`channel: 'chromium'`), porque Chrome e Edge estáveis removeram as flags de side-load (V-62).

## Node

Fonte: V-04, conflito 7.

- **Mínimo técnico: 20** (`engines.node >= 20` em `playwright`, `playwright-core` e `@playwright/test` 1.64.0).
- **Suportado e recomendado pela doc: 22, 24 ou 26.** Use 22 ou superior. Node 20 aparece como fim de vida em nodejs.org.
- Os READMEs do MCP e da CLI dizem "18 ou superior": estão desatualizados.
- Registre `node --version` na rodada. A máquina de verificação usou Node 24.15.0.

## O que é pré-autorizado e o que pede confirmação

Pré-autorizado pelo dono, e só o orquestrador executa (§3.2 do protocolo): `@playwright/test` com versão exata como devDependency na branch local, o harness `e2e-playwright/` e o Chromium no cache do usuário (avise o tamanho). **Continua exigindo confirmação:** `--with-deps`, `install-deps`, admin ou sudo; plugin ou MCP no Claude Code; `init-agents` e `init-skills`; qualquer outra dependência (`@axe-core/playwright`, Appium, Maestro); enviar trace, vídeo ou relatório para fora (G-11, G-12, G-13, G-14).

## Registrar versões na rodada

Bloco "Ambiente" no `FUNCIONALIDADES.md` e no relatório: Node, npm, Playwright exato, canal e versão do navegador, SO, portas de exploração e de teste, PIDs e como parar, commit, papéis com estado de login gerado (sem valores). Templates em `assets/templates/`.

## Atualizar a versão

Fonte: V-49, V-02. Atualização é decisão do usuário (por PR), não efeito colateral de rodada.

1. Leia as notas de release entre a versão antiga e a nova.
2. Atualize com `npm i -D -E @playwright/test@<nova>`; confira que não voltou o `^`.
3. `npm ci` em ambiente limpo; rode o gate (`--repeat-each=5` e `--shuffle --workers=2`, V-47) nos specs.
4. Refaça os baselines visuais se o descritor de dispositivo mudou (`screen` passa a vir do descritor na 1.64); revise o diff, não atualize às cegas (V-55).
5. Regenere os arquivos do `init-agents`, se usados (`test-agents-js.md:30-32`).
6. Imagem Docker na mesma versão (veja abaixo).

## Notas de release 1.55 a 1.64 que mudam a suíte

Conferidas em `docs/src/release-notes-js.md` (V-49) e, onde indicado, em outras fontes.

| Versão | O que muda para a suíte |
| --- | --- |
| 1.64 | `TestProject.default: false` mantém projeto na config sem rodar por padrão (`--project="*"` roda todos); `--shuffle [seed]`; `lock` em `describe.configure`; `Locator.within`; `Page.getByRef`; `screen` vem do descritor do dispositivo; `--update-snapshots=missing` passa a rodada; iframes ocultos; JSX segue o `tsconfig`; `fontSize` do vídeo deprecado (release v1.64.0, 07/10/2026) |
| 1.63 | Locks por nome entre arquivos, workers e projetos; `Locator.visible()` no lugar de `:visible`; Ubuntu 20.04 fora; pacotes `@playwright/experimental-ct-*` deixam de ser atualizados |
| 1.62 | Component testing por stories e galeria com a fixture `mount` (estável); **MCP e CLI embutidos** no pacote (`npx playwright mcp` e `npx playwright cli`) |
| 1.59 | `--debug=cli`; `npx playwright trace`; modo de trace `retain-on-failure-and-retries`; JUnit separa `<error>` de `<failure>`; `page.ariaSnapshot`; `experimental-ct-svelte` removido; macOS 14 sem WebKit |
| 1.57 | `page.accessibility` removido; Chromium passa a ser Chrome for Testing; `wait` com grupo nomeado no `webServer` |
| 1.56 | Test Agents (`init-agents`; V-13) |
| 1.49 | `toMatchAriaSnapshot` |
| 1.48 | `routeWebSocket` |
| 1.45 | `page.clock` |
| 1.43 | Modo de trace `retain-on-first-failure` |

Versões de `toMatchAriaSnapshot` e `page.ariaSnapshot` estão em V-56; `Page.getByRef` com modo `ai` na 1.64 não foi verificado em profundidade.

## Docker e CI

Fonte: V-48. Imagem `mcr.microsoft.com/playwright:v1.64.0-noble`; "always pin your Docker image to a specific version"; versão diferente da do projeto faz o Playwright não achar os executáveis; use `--init` e `--ipc=host`. Cache de navegadores na CI não é recomendado (`ci.md:1008`). Headed em Linux exige `xvfb-run`. Os exemplos oficiais trazem `%%VERSION%%` e versões de actions diferentes entre páginas: confira. Template em `assets/templates/github-actions-e2e.yml`, só a pedido.

## Rede corporativa

`PLAYWRIGHT_DOWNLOAD_HOST` aponta o download de navegadores para um espelho. A verificação de integridade dos binários baixados não aparece nas fontes lidas (Não verificável) (V-03).
