---
name: harness-setup
description: "Prepara o Playwright para a rodada: registra versões, usa ou instala @playwright/test com versão exata (commit separado), cria o harness e2e-playwright/ em projeto não-JS, escolhe Chrome/Edge instalado ou Chromium, sobe o sistema em 127.0.0.1 com dados sintéticos e grava config e .gitignore (CI só se pedido). Use por /comando para 'preparar o Playwright', 'instalar Playwright no projeto', 'criar o harness de e2e', 'set up Playwright', 'configurar CI do Playwright'."
argument-hint: "[projeto] [--ci]"
disable-model-invocation: true
allowed-tools: Read, Grep, Glob
---

# harness-setup: preparar o Playwright sem surpresas

Esta skill instala dependência e grava arquivos no projeto. Por isso ela não dispara sozinha (`disable-model-invocation: true`) e tem uma condição de uso escrita aqui.

## Quando executar (condição de uso)

O **agente principal** (o orquestrador, ou o Claude da sessão) lê este arquivo e o executa em dois casos:

1. A rodada está sob o protocolo do orquestrador (§3.2), que pré-autoriza só isto: `@playwright/test` com versão exata como devDependency na branch local, o harness `e2e-playwright/` e o Chromium no cache do usuário.
2. O usuário pediu a preparação na conversa (por `/qa-playwright:harness-setup` ou em texto).

Em qualquer outro caso, mostre os comandos e peça confirmação antes de rodar. **Subagente nunca executa esta skill**: ele recebe o ambiente pronto.

Continuam exigindo confirmação explícita: `--with-deps` e `install-deps` (admin ou sudo), instalar plugin ou MCP no Claude Code, `init-agents`, `init-skills`, qualquer outra dependência (`@axe-core/playwright`, Appium, Maestro) e enviar trace, vídeo ou relatório para fora.

## Entradas

Argumentos recebidos: $ARGUMENTS (projeto e, se vier, `--ci`).

- Caminho do projeto, comando que sobe o sistema e a porta.
- Há login? Origem da conta de teste (passo 9).
- O projeto já usa Playwright? Se sim, a versão dele prevalece.

## Pré-checagens

1. Modo melhoria: árvore git limpa e branch local criada. Auditoria pura: pasta temporária fora do projeto (nada é commitado).
2. Projeto de link de terceiros: leia `package.json` (scripts, `postinstall`), config do Playwright e CI antes de rodar o `webServer.command`. `npx playwright test` executa código do projeto, então só se roda em projeto confiável.
3. Nenhum `.env*` é aberto. Credencial nunca vai ao chat, a arquivo ou a comando visível.

## Passos

1. **Caminho de trabalho.** Registre o diretório (projeto ou pasta temporária). Saída: um caminho absoluto.
2. **Versões.** Rode `node --version` (mínimo 20; use 22 ou superior), `npm --version` e `npx --no-install playwright --version`. Registre o resultado.
3. **Onde instalar.** Projeto JS: devDependency do projeto. Sem `package.json` ou não-JS: pasta `e2e-playwright/` com `package.json` e lockfile próprios. Projeto que já tem Playwright 1.64 ou mais: mantenha a versão dele. Menor que 1.64: harness `e2e-playwright/` com versão exata, sem subir a do projeto (a CLI embutida vem da 1.62 e o `--shuffle` da 1.64).
4. **Instalar com versão exata.** `npm view @playwright/test version` (leitura) para a estável do dia; depois `npm i -D -E @playwright/test@<versão>`. Confira que o `package.json` ficou **sem** `^` nem `~`: o comando abaixo não deve devolver nada. Se devolver, corrija à mão e rode `npm install` de novo.

   ```bash
   grep '"@playwright/test": "[~^]' package.json
   ```

   ```powershell
   Select-String -Path package.json -Pattern '"@playwright/test": "[~^]'
   ```

   A instalação não baixa browser. Verificado (X-22): com `-E`, o `package.json` ficou `"@playwright/test": "1.64.0"`, e `npm ci` reproduziu a instalação depois de apagar `node_modules`.
5. **Browser.** Com Chrome ou Edge instalado: `PW_CHANNEL=chrome` (ou `msedge`) na config e `--browser=chrome` na CLI, sem download. Sem eles: avise que `npx playwright install chromium` baixa algumas centenas de MB para o cache do usuário (no Windows, `%USERPROFILE%\AppData\Local\ms-playwright`), rode-o e use `PW_CHANNEL=chromium`. Nunca use `--with-deps` aqui.
6. **Arquivos.** Copie dos templates e ajuste `testDir`, porta, comando do servidor e caminho de saúde:
   - [playwright.config.ts](${CLAUDE_PLUGIN_ROOT}/skills/playbook/assets/templates/playwright.config.ts) e [fixtures.ts](${CLAUDE_PLUGIN_ROOT}/skills/playbook/assets/templates/fixtures.ts);
   - [auth.setup.ts](${CLAUDE_PLUGIN_ROOT}/skills/playbook/assets/templates/auth.setup.ts), só se houver login;
   - [gitignore-trecho.txt](${CLAUDE_PLUGIN_ROOT}/skills/playbook/assets/templates/gitignore-trecho.txt) no `.gitignore` (inclui `**/playwright/.auth/`, que também pega `e2e-playwright/playwright/.auth/`; confira com `git check-ignore -v <caminho do estado>`, `test-results/`, `playwright-report/`, `.playwright-cli/`);
   - [harness-package.json](${CLAUDE_PLUGIN_ROOT}/skills/playbook/assets/templates/harness-package.json) só mostra o resultado esperado: o arquivo real vem do `npm i -D -E`.
   Mantenha a config e o `package.json` na mesma pasta: com a config numa subpasta sem `package.json`, o `playwright-report/` foi gravado na pasta do `package.json` (X-17).
7. **Verificar.** `npx playwright --version` igual ao `package.json`; `npx playwright cli --help` lista `open`, `snapshot` e `find`; `npx playwright test --list` executa. Saída: três comandos com resultado.
8. **Instância de exploração.** Suba o sistema em `127.0.0.1` numa porta própria (por exemplo 4173), com dados sintéticos e sem `.env` real. Confira HTTP 200 no caminho de saúde e registre o PID e como parar. A instância de teste não se sobe à mão: o `webServer` da config sobe e derruba uma a cada execução (porta 4174, X-17). Se o app aceitar, a instância de teste usa **banco próprio** (variável de banco ou arquivo por porta). Senão, as duas compartilham dados, e os specs afirmam delta e criam dados únicos. Servidor ligado só a `127.0.0.1`, nunca `0.0.0.0` nem túnel.
9. **Login (se houver).** Obtenha a conta de teste nesta ordem:
   1. conta sintética do seed, fixture ou exemplo de config do próprio projeto, só para o sistema local;
   2. variável que o usuário já exportou no ambiente (staging);
   3. cadastro pelo próprio sistema local, com dados sintéticos.

   Nunca peça senha no chat. Sem nenhuma das três, as funcionalidades com login ficam `Bloqueado`, com decisão pendente. Com a conta, exporte `E2E_USER` e `E2E_PASSWORD` só no ambiente do comando, sem repetir os valores na saída, e gere o estado contra a instância de exploração:

   ```bash
   E2E_AUTH=1 E2E_PORT=4173 E2E_REUSE=1 npx playwright test --project=setup
   ```

   ```powershell
   $env:E2E_AUTH='1'; $env:E2E_PORT='4173'; $env:E2E_REUSE='1'
   npx playwright test --project=setup
   Remove-Item Env:E2E_AUTH, Env:E2E_PORT, Env:E2E_REUSE
   ```

   `E2E_PORT` e `E2E_REUSE` esquecidos na sessão fariam o gate reutilizar a instância de exploração. Remova também `E2E_USER` e `E2E_PASSWORD` se foi você quem os definiu nesta sessão; variável que o usuário exportou fica como está.

   Confira que `playwright/.auth/user-4173.json` existe **listando a pasta**, sem abrir o arquivo. O estado vale como credencial: não o leia, não o imprima, não o anexe. O projeto `setup` roda com `trace: 'off'` porque o trace gravaria a senha digitada. Esse caminho foi verificado no sistema-demo (X-23): o comando acima gerou `user-4173.json` (1 passed), nenhum `trace.zip` saiu do setup e o `state-load` da CLI abriu a área logada. O estado é por porta; que a sessão do servidor de teste não valha no de exploração é Inferido.
10. **Commit separado** (modo melhoria): `chore(e2e): playwright <versão> harness`, depois de `git diff --cached` sem segredo nem pasta de saída. Sem push.
11. **CI só a pedido:** [github-actions-e2e.yml](${CLAUDE_PLUGIN_ROOT}/skills/playbook/assets/templates/github-actions-e2e.yml), com as versões das actions conferidas e fixadas por SHA. Detalhes em [config-execucao-e-ci.md](${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/config-execucao-e-ci.md).

**Critério de saída:** o bloco "Ambiente" (versões, canal, portas, PIDs, commit, papéis com estado de login gerado) está colado no `FUNCIONALIDADES.md`.

## Verificação

- [ ] `package.json` sem `^` nem `~` no `@playwright/test`; lockfile no commit.
- [ ] `npx playwright --version` igual à versão do `package.json`.
- [ ] `.gitignore` cobre `test-results/`, `playwright-report/`, `.playwright-cli/`, `playwright/.auth/`.
- [ ] Servidor de exploração responde 200 em `127.0.0.1`; PID e forma de parar registrados.
- [ ] Nenhuma credencial em arquivo, comando visível ou mensagem.
- [ ] Nenhum `install-deps`, `--with-deps`, `init-agents`, `init-skills` ou `@latest` foi usado.

## Formato de saída

Bloco "Ambiente", colado no topo do `FUNCIONALIDADES.md`:

```markdown
## Ambiente
Node <v> · npm <v> · Playwright <versão exata> · Browser <canal e versão> · SO <...>
Projeto: <caminho> · Branch: <nome> · Commit do harness: <sha>
Exploração: http://127.0.0.1:<porta> (PID <n>; parar com <comando>) · Teste: porta <porta>, subida pelo webServer
Banco: <próprio por instância | compartilhado, com delta e dado único>
Papéis com estado de login gerado: <papel: sim/não> (arquivos em playwright/.auth/, não lidos)
```

## Armadilhas

- `npm i -D` grava `^` por padrão (o harness de teste do orquestrador ficou com `^1.64.0`): use `-E` e confira.
- `@latest`, `init-agents`, `init-skills` e `--with-deps` fora da pré-autorização.
- `E2E_REUSE=1` no gate ou na evidência: herda o estado da exploração. Só o passo de gerar o estado de login o usa.
- Estado de login gerado na instância errada (porta diferente da de exploração).
- Config numa subpasta sem `package.json`: o relatório sai na pasta do `package.json`.
- Chrome ausente sem fallback para `chromium`; Node 18.
- No PowerShell, a variável de ambiente fica na sessão: limpe com `Remove-Item Env:<nome>` ao fim.

## Referências

- [versoes-e-instalacao.md](${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/versoes-e-instalacao.md), [config-execucao-e-ci.md](${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/config-execucao-e-ci.md), [seguranca-e-evidencia.md](${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/seguranca-e-evidencia.md).
- Origem: V-02, V-03, V-04, V-39, X-01, X-04, X-15, X-17, X-22, X-23, X-25; decisões D-3, D-4.

Validado em: 2026-10-13 · modelo-alvo: claude-sonnet-5-5. Instalação exata e login por estado por porta verificados no sistema-demo (X-22, X-23); o harness em projeto não-JS de ponta a ponta (S-19) não foi exercitado.
