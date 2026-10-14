# qa-playwright: validação da integração no protocolo do orquestrador

Data: 2026-10-13 (22:36, hora local da máquina) · Validador: Claude Sonnet 5.5 (`claude-sonnet-5-5`) · **Revisão da mesma família de modelos dos autores (Claude); reduz erro de leitura e de contagem, não é validação externa.**

Escopo: somente leitura. Nenhum npm, npx ou script foi executado. Comandos usados: `cmp`, `diff`, `grep`, `ls`, `sed`, e `git` de leitura (`log`, `show`, `diff`, `status`, `ls-remote --heads`). O plugin `plugins/qa-playwright/` só foi lido, para conferir nomes e comandos; a validação dele é de outro validador.

Arquivos examinados: `publish/ORCHESTRATOR.md` e `plugins/orchestrator/skills/playbook/references/protocolo.md` (idênticos, `cmp` sem diferença; a numeração de linhas vale para os dois), `plugins/orchestrator/**`, ponteiros em `qa-testing`, `web-frontend`, `backend-api`, `mobile-apps` e `design-engineering-kit`, `docs/foundation/knowledge/testes-funcionais-playwright.json`, `docs/research/qa-playwright/PUBLISH.json`, `SYNTHESIS.md` §5 e §6, `VERIFICACAO-ORQUESTRADOR.md` (X-01..X-26) e `tools/publish_brain.py`.

## Veredito: APROVADO COM RESSALVAS

O texto do §3.2 é coerente com §0, §3.1, §5 e §6, tem 33 linhas (limite ~45), mantém o bloco de limites fechado para subagentes (item 1 inalterado, `protocolo.md:86`), e todos os nomes de agentes, skills e tags existem. Nenhum achado crítico.

Há **1 achado alto** (ordem de publicação: o §3.2 obrigatório já está no ar sem o plugin) e **9 médios** (versão do Playwright do projeto, exceção de instalação invertida no playbook, auditoria pura, obrigatoriedade sem saída, N/A sem executor registrado, gate sem `--retries=0`, "senha em comando", fundamentos com MCP `@latest`, versão do orquestrador). Os 10 têm correção em texto exato abaixo. O achado ALTA-1 deve ser fechado antes de qualquer push; os médios 2 a 5 e 7 a 8 antes de o protocolo ser usado numa rodada real.

## Achados de severidade média para cima

### ALTA-1. O §3.2 obrigatório já está publicado, mas o plugin `qa-playwright` não existe no brain

Evidência (Verificado):
- `cmp publish/ORCHESTRATOR.md brain-of-agent/ORCHESTRATOR.md` não acusa diferença: a "versão publicada anterior" já traz o §3.2. O commit `32c29b0` (22:30, "orquestrador 0.4.0") levou o arquivo sincronizado às 22:28 (`git show 32c29b0 -- ORCHESTRATOR.md` tem 31 menções a Playwright). `git ls-remote --heads origin` devolve `32c29b0` em `refs/heads/main`: está no remoto.
- `brain-of-agent/plugins/qa-playwright` não existe. `KNOWLEDGE.md:39` e `:489` marcam a tag como "em construção".
- `tools/publish_brain.py:276-281` pula o plugin enquanto `docs/research/qa-playwright/BUILD-REPORT-quality.md` não existir (hoje não existe).
- O working tree do brain já tem, sem commit, os ponteiros `qa-playwright:*` em `qa-testing`, `web-frontend`, `backend-api`, `mobile-apps` e `design-engineering-kit`, e o playbook e os prompts do orquestrador. O SYNTHESIS §6 (linha 940) diz: "Nada disso entra antes de o plugin existir".

Consequência: quem manda hoje só o link recebe um passo "obrigatório" que nomeia `qa-playwright:feature-explorer` e outros, que não existem no clone, e a tag em construção manda "usar a rota mais próxima" (`protocolo.md:108`). As duas instruções se contradizem. Os ponteiros, se publicados antes do plugin, quebram do mesmo jeito. Efeito colateral: a comparação de regressão contra a versão anterior não é possível por diff; foi feita por presença de trechos (ver "Regressões").

Correção:
1. Não commitar nem dar push dos ponteiros, do playbook e dos prompts até o plugin ser publicável.
2. Concluir a validação do plugin (gera `docs/research/qa-playwright/BUILD-REPORT-quality.md`), rodar `python tools/publish_brain.py <brain>` e conferir que a saída não tem "PULANDO qa-playwright" e que `KNOWLEDGE.md` mostra `testes-funcionais-playwright | ... | publicado`.
3. Um único commit e push com plugin, ponteiros e orquestrador.
4. Se o push demorar, desfazer o §3.2 no remoto (aplicar ao contrário o SYNTHESIS §5) em vez de deixar o passo obrigatório sem plugin.

### MÉDIA-2. "Use o `@playwright/test` do projeto" quebra a CLI e o gate em versões antigas, e a config do projeto não lê `E2E_RUN`

`protocolo.md:179` (passo 3). `versoes-e-instalacao.md:110` registra que `npx playwright cli` só vem embutido desde a 1.62, e `:108` que `--shuffle` só entrou na 1.64. O `harness-setup/SKILL.md:42` manda manter a versão do projeto que já tem Playwright. Com um projeto em 1.4x (caso comum), o passo 4 (CLI) e o gate do passo 5 (`--shuffle`) não existem. Além disso, `test-results/<id>/` e `playwright-report/<id>/` (passo 6) só existem se a config ler `E2E_RUN` (template T-03); a config própria do projeto não lê. Rótulo: Inferido (limiares lidos no plugin; X-01..X-26 só exercitaram a 1.64.0).

Correção. Em `protocolo.md:179`, trocar

````text
Use o `@playwright/test` do projeto; sem ele, `npm i -D -E @playwright/test@<versão>` (projeto não-JS: harness `e2e-playwright/`), em commit próprio, e confira que o `package.json` ficou sem `^`.
````

por

````text
Use o `@playwright/test` do projeto só se for 1.64 ou mais (`npx playwright --version`; a CLI embutida vem da 1.62 e o `--shuffle` da 1.64) e se a config dele ler `E2E_RUN` (modelo T-03). Senão, ou se não houver Playwright, instale com `npm i -D -E @playwright/test@<versão>` (projeto não-JS ou com versão menor que 1.64: harness `e2e-playwright/`, sem tocar a versão nem a config do projeto), em commit próprio, e confira que o `package.json` ficou sem `^`.
````

Ajuste espelho em `harness-setup/SKILL.md:42`: trocar "Projeto que já tem Playwright: mantenha a versão dele e suba só a pedido." por "Projeto que já tem Playwright 1.64 ou mais: mantenha a versão dele. Menor que 1.64: harness `e2e-playwright/` com versão exata, sem subir a do projeto."

### MÉDIA-3. A exceção de instalação aparece no lugar errado no playbook e o §3.2 diz que "prevalece sobre o bloco de limites"

- `plugins/orchestrator/skills/playbook/SKILL.md:21` (lista de paradas) e `:66` (Modo melhoria, passo 4) ainda dizem "instalar plugins ou SDKs" sem a exceção; quem usa o plugin instalado (opção A) lê o playbook, e não o protocolo, e vê a preparação do Playwright como parada.
- `SKILL.md:23` colocou a exceção dentro do resumo do **bloco de limites dos subagentes**: "sem push nem instalações (exceto a preparação do Playwright, §3.2)". O bloco tem de continuar fechado para subagente; a pré-autorização é só do orquestrador.
- `protocolo.md:188` diz que a pré-autorização "prevalece sobre o §0, o §3.1 e o bloco de limites". O bloco é só dos subagentes, que não executam a preparação (`:179`, "só o orquestrador").

Correção, texto exato:
- `SKILL.md:21`: trocar "stack, instalar plugins ou SDKs)." por "stack, instalar plugins ou SDKs; a preparação do Playwright do §3.2 é pré-autorizada)."
- `SKILL.md:23`: trocar "(sem push nem instalações (exceto a preparação do Playwright, §3.2), escrita só no projeto," por "(sem push nem instalações, escrita só no projeto," e acrescentar no fim da frase: " A preparação do Playwright do §3.2 é só do orquestrador, nunca do subagente."
- `SKILL.md:66`: trocar "e instalar plugins ou SDKs." por "e instalar plugins ou SDKs (exceto a preparação do Playwright, §3.2)."
- `protocolo.md:188`: trocar "(prevalece sobre o §0, o §3.1 e o bloco de limites; só o orquestrador executa)" por "(prevalece sobre o §0 e o §3.1; só o orquestrador executa, e o bloco de limites do §2 B continua fechado para subagentes)".

### MÉDIA-4. Auditoria pura: três pontos do protocolo se contradizem

- `protocolo.md:179` manda `npm i -D -E` no projeto (altera `package.json` e o lockfile), mas `:194` diz que em auditoria pura "o harness fica numa pasta temporária fora do projeto e nada é commitado", e o §5 diz "Auditoria não altera o produto".
- `:194` grava `docs/testes/AAAA-MM-DD/funcional/` dentro do projeto, mas o §6 item 2 diz que em auditoria pura os relatórios só vão ao projeto "com autorização de escrita; sem ela, ficam no chat".
- O bloco de limites item 2 (`:87`) permite escrever "só na pasta do projeto", e na auditoria o explorador e o redator gravam na pasta temporária do harness (inclusive `.playwright-cli/`).

Correção, texto exato:
- `:179`, acrescentar no fim do passo 3:

````text
 Em auditoria pura, use sempre o harness temporário e não toque o `package.json` do projeto.
````

- `:194`, trocar a última frase ("Em auditoria pura, o harness fica numa pasta temporária fora do projeto e nada é commitado.") por:

````text
Em auditoria pura, o harness, o `FUNCIONALIDADES.md`, o `RELATORIO-FUNCIONAL.md` e `exploracao/` ficam numa pasta temporária fora do projeto (informe o caminho absoluto) e nada é commitado; com autorização de escrita, os artefatos vão para `docs/testes/AAAA-MM-DD/funcional/`.
````

- `:87` (item 2 do bloco), trocar o texto do item por:

````text
escrever só na pasta do projeto e, no modo melhoria, só na branch local (em auditoria pura com validação funcional, só na pasta temporária do harness do §3.2);
````

### MÉDIA-5. A obrigatoriedade tem gatilho ambíguo, não tem saída quando o sistema não sobe e a linha da matriz é condicional

`protocolo.md:174`: "§3 passo 7" dispara o ciclo para toda implementação com superfície web ou HTTP, mas a frase seguinte diz que "demanda sem teste" não dispara. Uma feature nova sem a palavra "teste" cai nas duas regras. Sem alvo rodável (serviço externo, segredo ausente, Node abaixo de 20, sem alvo informado), o §3.2 não diz o que fazer, e a mensagem final (`:281`) só pede a linha da matriz "com validação funcional", então pular o ciclo não deixa rastro obrigatório. Isso enfraquece o "obrigatório de fato" pedido pelo dono.

Correção, texto exato:
- `:174`: trocar "Pergunta pontual, correção localizada e demanda sem teste não disparam o ciclo (§5)." por:

````text
Pergunta pontual, correção localizada e tarefa que não muda comportamento (documentação, refactor sem efeito) não disparam o ciclo (§5); feature nova ou mudança de comportamento com superfície web ou HTTP dispara, nas funcionalidades tocadas. Se o sistema não sobe (serviço externo, segredo ausente, Node abaixo de 20, sem alvo), as linhas ficam `Bloqueado` com o motivo e o comando para o usuário; o inventário e a matriz saem do mesmo jeito.
````

- `:281` (item 3 da mensagem final), acrescentar no fim:

````text
 Se o ciclo se aplicava e não rodou, escreva `Validação funcional: não executada, <motivo>` no lugar da linha.
````

### MÉDIA-6. "Qualquer tipo de sistema": o N/A com equivalente não tem passo que execute nem registre o equivalente, e faltam tipos na tabela

`protocolo.md:178` diz "toda linha tem executor", mas os passos 6 e 7 só executam e registram Playwright, e `Passou` só admite prova `spec-estável` ou `exploração` (`:183`, template `FUNCIONALIDADES.md`, legenda). Para UI nativa Android ou iOS, ninguém é mandado rodar o equivalente nem diz onde o resultado entra. O ponteiro `mobile-test-engineer.md:18` ("devolva o status com evidência no mesmo formato") sugere um status que a matriz não tem. A tabela (`:198-204`) também não cobre desktop não Electron, jogo, embarcado e pipeline de dados, que o `escopo-e-stacks.md` cobre.

Correção (mantém o template e o `evidence-report` como estão). Em `:196`, trocar a frase de abertura por:

````text
**Onde o Playwright não se aplica**, a matriz é a mesma e muda o executor. O executor equivalente roda a funcionalidade (no §3.1, junto da suíte do passo 1 e do passo 6) e entrega comando, resultado e evidência; a linha continua `N/A`, com esses dados na coluna Evidência, e não entra em `Passou` (que é só de spec ou exploração Playwright). Sem como rodá-lo (sem emulador, sem Xcode), o comando exato vai para o usuário:
````

e acrescentar, depois da linha "Backend/API desses sistemas":

````text
| Outro sistema sem superfície web ou HTTP (desktop não Electron, jogo, embarcado, pipeline de dados) | Runner do próprio segmento; detalhe em `qa-playwright:non-web-systems` |
````

Em `mobile-apps/agents/mobile-test-engineer.md:18`, trocar "devolva o status com evidência no mesmo formato" por "devolva resultado e evidência por F-NN para a coluna Evidência da linha N/A; só `evidence-report` grava a matriz".

### MÉDIA-7. O gate do §3.2 omite `--retries=0`

`protocolo.md:181` escreve "gate `--repeat-each=5` e `--shuffle --workers=2` sem falha". X-24 e o `playbook/SKILL.md:135-136` usam `--retries=0`. Sem ele, numa config com `retries` maior que zero, um teste intermitente passa "verde" na repetição, e o spec vira `spec-estável` sem ser estável (risco R-02 do SYNTHESIS).

Correção, texto exato em `:181`: trocar "gate `--repeat-each=5` e `--shuffle --workers=2` sem falha" por "gate `--repeat-each=5 --retries=0` e `--shuffle --workers=2 --retries=0`, sem falha nem `flaky`".

### MÉDIA-8. "Senha nunca em comando" contradiz o login do projeto `setup`

`protocolo.md:190`: "(seed local ou variável já exportada) ... Senha nunca no chat, em comando nem em relatório." Para a conta sintética do seed, o único jeito de rodar o `setup` é passar `E2E_USER` e `E2E_PASSWORD` na variável de ambiente do comando (X-23(b); `harness-setup/SKILL.md` passo 9; guardrail G-03 permite isso, "nunca em nota, spec ou relatório"). Lido literalmente, o texto manda deixar toda funcionalidade com login como `Bloqueado`, o que derruba a cobertura de "qualquer sistema".

Correção, texto exato em `:190`: trocar "Senha nunca no chat, em comando nem em relatório." por:

````text
Senha de conta real nunca no chat nem em relatório. A conta sintética do seed local entra só como variável de ambiente (`E2E_USER`, `E2E_PASSWORD`) do comando do projeto `setup`, nunca na CLI de exploração, em nota, spec ou relatório.
````

### MÉDIA-9. A tag manda o explorador seguir uma skill que instala MCP com `@latest -y`

`docs/foundation/knowledge/testes-funcionais-playwright.json:15` lista `engineering-lifecycle:browser-testing-with-devtools` como **fundamentos**. O §2 B (`protocolo.md:83`) manda o subagente seguir as skills dos fundamentos. Essa skill vendorizada (`plugins/engineering-lifecycle/skills/browser-testing-with-devtools/SKILL.md:26-41`) manda gravar em `.mcp.json` o servidor `npx -y chrome-devtools-mcp@latest`, contra o §3.2 (MCP exige confirmação, nunca `@latest`) e contra a pré-autorização estreita. O item 2 do bloco ("escrever só na pasta do projeto") não impede gravar `.mcp.json`. A rota já existia antes desta integração, mas a tag é o que o orquestrador usa para montar o prompt.

Correção, texto exato. Em `:15` do JSON, trocar por

`{ "plugin": "engineering-lifecycle", "skills": ["test-driven-development"], "agents": ["test-engineer"], "role": "fundamentos" },`

e acrescentar ao fim de `notes`: ` browser-testing-with-devtools (engineering-lifecycle) fica de fora dos fundamentos: manda configurar chrome-devtools-mcp@latest com -y em .mcp.json, contra o §3.2.`

### MÉDIA-10. A versão do `orchestrator` não subiu

`plugins/orchestrator/.claude-plugin/plugin.json:3` continua `0.4.0`, igual à do brain, mas README, playbook, prompts (O-08, O-09) e `protocolo.md` mudaram. Os plugins `qa-testing`, `web-frontend`, `backend-api`, `mobile-apps` e `design-engineering-kit` subiram corretamente de 0.1.0 para 0.1.1. Sem o bump, quem instalou o 0.4.0 não recebe as mudanças no `plugin update`.

Correção: em `plugin.json:3`, `"version": "0.4.1"`.

## Achados baixos (sem bloquear)

- **B-1** `protocolo.md:274` (§6 item 5): "`E2E_RUN=<id>` antes" não roda no PowerShell. Texto, trocando o trecho "para guardar a evidência, `E2E_RUN=<id>` antes, e no PowerShell `Remove-Item Env:E2E_RUN` depois":

  ````text
  para guardar a evidência, bash: `E2E_RUN=<id> npx playwright test --grep "F-07"`; PowerShell: `$env:E2E_RUN='<id>'; npx playwright test --grep "F-07"; Remove-Item Env:E2E_RUN`
  ````
- **B-2** `testes-funcionais-playwright.json` tem 22 gatilhos; o esquema pede 6 a 15 (`knowledge-registry-spec.md` §2). Sem aviso do gerador. Sugestão: remover `playwright mcp`, `playwright cli`, `e2e tests`, `browser tests`, `end-to-end`, `testar no navegador` e `automação de testes web` (sobram 15).
- **B-3** `protocolo.md:299` cita só O-08; trocar por "(O-08 e O-09)".
- **B-4** `protocolo.md:174` mapeia `${CLAUDE_PLUGIN_ROOT}` só para `qa-playwright`; as skills de `qa-testing` (fundamentos) usam a mesma variável. Generalizar no §2 B: "`${CLAUDE_PLUGIN_ROOT}` nas skills e agentes = `<clone>/plugins/<plugin>`".
- **B-5** `design-engineering-kit/skills/playbook/references/playwright-verificacao-ui.md:30` diz "Recomendado" e "Prefira" na mesma linha. Texto: "Recomendado só se o projeto não tiver `@playwright/test` 1.62 ou mais; se tiver, prefira `npx playwright mcp` do pacote fixado (o `@playwright/mcp@0.0.83` depende de Playwright alpha)."
- **B-6** `protocolo.md:154`: harness (config, fixtures, lockfile) pode estourar as ~600 linhas de diff. Texto: "Harness, specs e matriz do §3.2 não contam como melhoria nem nas ~600 linhas; a correção de um bug achado por ela conta."
- **B-7** `protocolo.md:186` (Teto): não diz como cobrir o resto. Acrescentar: " A mensagem final diz como cobrir o resto: nova rodada ou `PLAYWRIGHT-COMPLETO`."
- **B-8** §6 mensagem final (`:278-283`): com 6 melhorias, o bloco "onde testar", a linha da matriz e os caminhos do Playwright, o total passa de 25 linhas. Sugestão: "Os caminhos absolutos dos relatórios (testes, Playwright, matriz) vão agrupados em até 3 linhas."
- **B-9** `protocolo.md:182`: no §2 C (chat sem subagentes) o orquestrador é o autor dos specs. Acrescentar: "No §2 C, declare que autor e executor são o mesmo (independência parcial)."
- **B-10** `protocolo.md:179`: `<versão>` sem origem. Sugestão: "a estável de `npm view @playwright/test version`, publicada há mais de 7 dias".

## Conferências sem achado

| Item do pedido | Resultado |
| --- | --- |
| 1. Coerência interna | `§3.2` tem 33 linhas (`:172-204`). Sem contradição com §0 (`:33`), §3.1 (`:121`, `:132`, `:155`, `:161-168`), §5 (`:231-238`) e §6, exceto MÉDIA-3, 4 e 5. A exceção de instalação aparece em `:33`, `:121`, `:132`, `:155` e `:188`; faltava só no playbook do orquestrador (MÉDIA-3). |
| 2. Pedido do dono | Obrigatório no título e no "Quando" (`:172-174`), com ponteiros e §4/§5; "abrir e validar funcionalidade por funcionalidade" está claro nos passos 1 a 7 (uma por vez, verifica o efeito, `npx playwright cli`). Lacunas: MÉDIA-5 e MÉDIA-6. |
| 3. Executabilidade | Todos os agentes e skills citados existem em `plugins/qa-playwright/` (`feature-explorer`, `spec-writer`, `spec-reviewer`, `failure-triager`, `matrix-auditor`, `evidence-report`, `feature-inventory`, `explore-feature`, `write-specs`, `non-web-systems`, `api-and-network`, `playbook`). `--grep "F-07"` sem barra invertida e nenhum `--%` com `npx` (X-16). Lacunas: MÉDIA-2, 7 e B-1. |
| 4. Segurança | Item 1 do bloco inalterado (`:86`); itens 3 e 6 conforme SYNTHESIS §5.2 (`:88`, `:91`); pré-autorização estreita (`:188`); produção, credenciais, `init-agents`, `--with-deps` e `install-deps` sob confirmação (`:188`, `:190`); o item 6 do bloco proíbe `install*`, `init-agents`, `init-skills`. Ajustes: MÉDIA-3, 8 e 9. |
| 5. Ponteiros | Cada ponteiro aponta para skill ou agente existente (`qa-playwright:playbook`, `explore-feature`, `api-and-network`, `non-web-systems`). Nenhum `networkidle` como recomendação (só como "não use"), nenhum `@latest` ou `--%` novo (varredura em todos os plugins, fora `qa-playwright`). Patch subiu em cinco plugins; faltou o `orchestrator` (MÉDIA-10). |
| 6. Tag e sidecar | `tag` igual ao nome do arquivo; uma rota `lider` (`qa-playwright`); skills e agentes de todas as rotas existem; `validators` em `plugin:agente` e existentes (`qa-playwright:matrix-auditor`, `qa-testing:test-auditor`); `sources` existem; sidecar `{mode_keyword, validation_report}` no formato de `knowledge-registry-spec.md` §5 e igual aos irmãos. Ajustes: MÉDIA-9, B-2. O `validation_report` aponta para um arquivo que ainda não existe, o que mantém o plugin "pendente" no gerador (ALTA-1). |
| 7. Regressões | Presentes e intactos em `publish/ORCHESTRATOR.md`: registro de conhecimento por tag (`:47`, `:83`, `:103-108`, `:225`), Profundidade 1 (`:95`), Apify (`:111`, `:224`, `:235`), engineering-lifecycle (`:223`), designer com direções de estilo e cult-ui (`:160`), Java 21 no Windows (`:135-138`). A conferência foi por presença de trechos, porque a versão publicada já é idêntica à nova (ALTA-1). Corrida possível: outra sessão pode editar `publish/ORCHESTRATOR.md` antes do push; refazer `cmp` com `protocolo.md` na hora de publicar. |

Declaração de independência: este parecer é da mesma família de modelos (Claude) que escreveu a pesquisa, o desenho e a integração. Não substitui revisão humana nem de outro fornecedor, e nada foi executado: comandos citados foram conferidos contra X-01..X-26 e contra o texto do plugin, não rodados.
