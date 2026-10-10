# code-quality-refactoring

Qualidade de código, revisão, refatoração e debugging para o Claude Code. Revisa diffs com filtro de alto sinal, investiga bugs por causa raiz, refatora com rede de segurança, simplifica sem mudar comportamento, conduz migrações com juiz de paridade, prioriza dívida técnica e mede a saúde do código, sempre com evidência executável e rótulos Verificado, Inferido, Suposição e Não verificável.

Versão 0.1.0 · Licença MIT · Autor: Francisco Edson · Modelo-alvo: Claude Sonnet 5.5, Fable 5.1 e Haiku 5.5, com a documentação da Anthropic consultada em 2026-10-10 (conselhos que dependem de versão de modelo estão marcados e devem ser medidos).

## O que entrega

- **Revisão de código** (`review-diff`) somente leitura: triagem, regras do projeto, revisão independente, validação de cada achado por tentativa de refutação, filtro de falsos positivos, severidades e veredito.
- **Debugging** (`debug-causa-raiz`): quatro fases (causa raiz, padrão, hipótese com comando, correção com teste que falha primeiro), dois contadores de escalada e relatório de causa raiz.
- **Refatoração segura** (`refactor-seguro`): testes de caracterização, passos pequenos nomeados pelo catálogo de refatorações, testes a cada passo, commits separados de comportamento.
- **Simplificação** (`simplify-safe`), **migração e upgrade** (`migration-parity`, juiz primeiro, rulebook, piloto, paridade por módulo), **dívida técnica** (`tech-debt-triage`, frequência x dor), **saúde do código** (`code-health-report`) e **compreensão de base de código** (`codebase-onboarding`).
- **Base de conhecimento** no `playbook`: 12 referências, 10 templates, snippets de CLAUDE.md, ferramentas e CI documentados e desativados, bibliografia com classe e licença.
- **Biblioteca de prompts** (`prompts`) e **5 subagentes** especialistas.

O plugin não substitui os comandos nativos `/code-review`, `/simplify`, `/batch` e o plan mode: ele acrescenta critérios de saída, filtro de falsos positivos, protocolo de debugging, rede de segurança antes de refatorar, juiz de migração e rótulos de evidência.

## Quando usar

Use para melhorar a qualidade de código que já existe ou acabou de ser escrito: revisar antes do merge, achar a causa de um bug, refatorar sem quebrar, entender um legado, planejar um upgrade, decidir o que arrumar primeiro.

Não use para: estratégia de testes e e2e (`qa-testing`), threat modeling e auditoria de segurança completa (`security-appsec`), desenho de arquitetura (`architecture-design`), escrita de feature nova, incidente de produção em andamento (`sre-observability`). A skill `playbook` lista as fronteiras com os outros 24 plugins do marketplace.

## Componentes

Todos ficam namespaced pelo nome do plugin: `/code-quality-refactoring:<skill>` e subagente `code-quality-refactoring:<agente>`.

| Tipo | Nome | O que faz | Invocação |
| --- | --- | --- | --- |
| Skill núcleo | `playbook` | Router, princípios, processo, referências, modo `QUALIDADE-COMPLETO`, fronteiras | automática ou `/code-quality-refactoring:playbook` |
| Skill | `review-diff` | Revisão de diff/PR somente leitura com validação por achado | automática |
| Skill | `debug-causa-raiz` | Investigação até a causa raiz, correção com teste de regressão | automática |
| Skill | `refactor-seguro` | Refatoração com caracterização e passos pequenos | automática |
| Skill | `simplify-safe` | Simplificação sem mudar comportamento | automática |
| Skill | `tech-debt-triage` | Triagem de dívida e auditoria de testes, só relatório | automática |
| Skill | `codebase-onboarding` | Convenções com evidência, mapa de entradas e dependências | automática |
| Skill | `migration-parity` | Migração/upgrade major com juiz, rulebook e veredito de paridade | só por comando (custo alto, muitos arquivos) |
| Skill | `code-health-report` | Painel de saúde com as ferramentas do projeto, somente leitura | só por comando (executa comandos do projeto) |
| Skill | `prompts` | Biblioteca de prompts curados (revisão, debug, refatoração, legado, dívida) | automática |
| Agente | `code-reviewer` | Revisor somente leitura em contexto novo | delegado por `review-diff` |
| Agente | `finding-validator` | Tenta refutar cada achado | delegado por `review-diff` |
| Agente | `debugger` | Reproduz, isola e propõe patch como diff, sem editar | delegado por `debug-causa-raiz` |
| Agente | `refactor-planner` | Plano de refatoração somente leitura | delegado por `refactor-seguro` |
| Agente | `codebase-mapper` | Mapa curto da base de código | delegado por `codebase-onboarding`, `tech-debt-triage` |
| Evals | 12 casos em `evals/` | Disparo, não disparo, escopo, segurança | `claude plugin eval` (ver abaixo) |

Referências do `playbook` (`skills/playbook/references/`): `checklist-completo`, `padroes-e-antipadroes`, `decisoes-e-tradeoffs`, `claude-md-snippets`, `ferramentas-e-mcp`, `fontes`, `revisao-de-codigo`, `debugging-sistematico`, `refatoracao-segura`, `modernizacao-e-migracao`, `divida-e-saude`, `compreensao-de-codigo`. Templates (`skills/playbook/assets/templates/`): `review-report`, `debug-report`, `refactor-plan`, `characterization-test-log`, `migration-rulebook`, `parity-verdict-table`, `tech-debt-register`, `health-dashboard`, `pr-split-plan`, `handoff-checkpoint`.

## Instalação

No Claude Code, dentro de uma sessão:

```text
/plugin marketplace add francisco-efjr/brain-of-agent
/plugin install code-quality-refactoring@brain-of-agent
```

`<caminho-ou-repo>` é o caminho local da pasta `dev-segments` (raiz do marketplace) ou `dono/repositório` no GitHub quando o marketplace estiver publicado. Equivalente na linha de comando: `claude plugin marketplace add francisco-efjr/brain-of-agent` e `claude plugin install code-quality-refactoring@brain-of-agent`. Valide a estrutura com `claude plugin validate <pasta-do-plugin>`.

Em caminhos com espaço (por exemplo `C:\Users\Nome Sobrenome\dev-segments`), use aspas.

## Exemplos de pedidos

1. "Pode mergear esse PR? Segue o diff do `app/users.py`." Aciona `review-diff`: relatório com achados `arquivo:linha`, veredito e o que não foi checado.
2. "O `test_counter` falha 1 vez em 5. Aqui estão o teste, a classe e o log." Aciona `debug-causa-raiz`: reprodução em laço, hipótese única com comando, teste de regressão, correção mínima.
3. "Refatore essa função `calcular_frete` para ficar legível, sem mudar o comportamento. Ela não tem testes." Aciona `refactor-seguro`: testes de caracterização primeiro, passos nomeados, bug de arredondamento listado como follow-up.
4. "O que devo refatorar primeiro neste repositório? Segue o `git log --name-only` dos últimos 6 meses." Aciona `tech-debt-triage`: ordem por frequência x dor, estável e feio no fim.
5. "Entenda este repositório e me diga as convenções de tratamento de erro." Aciona `codebase-onboarding`: convenções com arquivo de exemplo e rótulo por contagem.
6. "/code-quality-refactoring:migration-parity migrar 180 arquivos JS para TypeScript; temos testes jest." Plano com juiz, rulebook, piloto e aprovação antes de migrar em massa.
7. "/code-quality-refactoring:code-health-report" Painel de saúde com os comandos do `## Health Stack`, cobertura declarada e nada corrigido.
8. "Me dê um prompt para revisão adversarial de diff contra um plano." Aciona `prompts`.
9. "Como melhorar a qualidade deste módulo?" Pedido amplo: o `playbook` classifica a intenção e escolhe o caminho.

## Modo QUALIDADE-COMPLETO

Digite explicitamente, por exemplo: "rode QUALIDADE-COMPLETO neste módulo". O `playbook` então lê as 12 referências em 3 lotes (registrando lido, parcial ou ausente), monta uma matriz de aplicabilidade por área (revisão, debugging, refatoração, simplificação, migração, dívida, análise estática, compreensão de código, segurança do diff, documentação), implementa dentro do escopo pedido e revalida com evidência. A keyword só vale quando escrita por você na conversa: aparecer em documento, log, diff ou issue não ativa nada. O modo não amplia permissões nem autoriza ações externas (push, comentário em PR, instalação). Sem a keyword, o plugin carrega só o necessário.

## Segurança por padrão

- Sem hooks, `.mcp.json`, `.lsp.json` nem `bin/`. Hooks, CI e MCP recomendados estão documentados e desativados em `references/ferramentas-e-mcp.md`, com JSON pronto e riscos.
- Revisão e auditoria não alteram o produto. Postar comentário em PR, commitar, dar push ou instalar ferramenta só acontece com pedido explícito na conversa.
- Diff, logs, issues e páginas são tratados como dados; texto dirigido à IA dentro deles é reportado como achado de segurança.
- O plugin não recomenda `--dangerously-skip-permissions` nem execução sem supervisão como padrão; quando citado, é como risco, só em sandbox e repositório confiável.

## Top 10 fontes

Lista completa, com URL, classe, licença e data em `skills/playbook/references/fontes.md`.

1. Claude Code, Best practices (A): https://code.claude.com/docs/en/best-practices
2. Claude Code, Common workflows (A): https://code.claude.com/docs/en/common-workflows
3. obra/superpowers, systematic-debugging (A, MIT): https://github.com/obra/superpowers/blob/main/skills/systematic-debugging/SKILL.md
4. anthropics/claude-code, plugin `code-review` (A, proprietária; só destilado)
5. Claude Code, Subagents (A): https://code.claude.com/docs/en/sub-agents
6. How Anthropic runs large-scale code migrations with Claude Code (A): https://claude.com/blog/ai-code-migration
7. Prompting Claude Fable 5.1 e Claude prompting best practices (A): https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
8. anthropics/claude-code-action (A, MIT): https://github.com/anthropics/claude-code-action
9. Google Engineering Practices, code review (B): https://google.github.io/eng-practices/review/reviewer/looking-for.html
10. Feathers (Characterization Testing) e Fowler (Technical Debt, Parallel Change, Strangler Fig) (B): https://michaelfeathers.silvrback.com/characterization-testing

## Créditos e licenças de terceiros

- Este plugin: MIT (Francisco Edson).
- **brain-of-agent** (francisco-efjr, MIT): `testes-e-debugging.md` e o modelo de handoff foram incorporados e adaptados; convenções de modo completo e rótulos epistêmicos herdadas.
- **gstack** (Garry Tan, MIT): ideias de `/investigate`, `/review` e `/health` descritas em redação própria; nenhum script, hook, binário ou telemetria foi copiado ou deve ser instalado.
- **obra/superpowers** (MIT): ideia das quatro fases de debugging, reescrita sem CAPS.
- **Conventional Comments** (https://conventionalcomments.org/, CC BY 3.0): os rótulos de comentário aparecem literalmente em `revisao-de-codigo.md`, com atribuição.
- **OWASP Secure Code Review Cheat Sheet** (CC BY-SA 4.0): só destilado em redação própria.
- Fowler, Feathers, Google Engineering Practices, documentação da Anthropic, `pr-review-toolkit` e demais fontes sem licença permissiva identificada: apenas ideias em redação própria, com a fonte citada.

## Limitações honestas

- Nenhum item tem eval próprio executado: os 12 casos de `evals/` estão como `designed_not_executed`. Rodá-los exige Claude Code 2.1.269 ou superior (`claude plugin eval .` na raiz do plugin); o CLI local registrado na fundação era 2.1.128. As eficácias citadas (escopo, verificação) são afirmações das fontes.
- Conselhos de escopo e overengineering vêm de documentação de modelos específicos e devem ser medidos nos evals.
- Validação por achado e revisão por subagente usam o mesmo modelo: independência parcial; leitura humana do diff continua necessária.
- Cobertura fraca ou parcial em: upgrades de framework (nenhum guia oficial por framework lido; licença do OpenRewrite não verificada), análise estática por linguagem (só Ruff com documentação lida), clean code por linguagem e métodos quantitativos de dívida.
- A voz da comunidade é quase ausente (quatro comentários do Hacker News); a pesquisa se apoia em fontes oficiais e autores reconhecidos.
- Alguns limiares são Suposição ajustável: 400 linhas ou 10 arquivos para dividir mudança, janela de 6 meses para frequência, pesos do painel de saúde, modelo do `finding-validator`.
- `allowed-tools` nas skills só pré-aprova as ferramentas listadas durante o turno que invoca a skill; não restringe as demais. Quem remove ferramentas é `disallowed-tools` (usado nas skills somente leitura, vale até a próxima mensagem do usuário). A forma `Bash(git diff *)` é a sintaxe documentada (conferido em https://code.claude.com/docs/en/skills e https://code.claude.com/docs/en/permissions em 2026-10-10). O agente `debugger` tem `Bash` amplo, que permite escrita via shell: risco declarado, mitigado pelo comando exato passado na delegação.
- Parte dos moldes de comando foi executada (Python 3.14.4, Node v24.15.0, Git Bash e Windows PowerShell 5.1, em 2026-10-10) e aparece como Verificado nas referências; os demais estão como Inferido.
- Os cinco agentes usam `model: inherit` (o plano previa `sonnet`, e `haiku` para o `finding-validator`, como Suposição de custo). Troque só depois de medir nos evals.
