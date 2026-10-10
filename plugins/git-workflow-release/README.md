# git-workflow-release

Plugin do Claude Code para o fluxo de git do commit à release: commits convencionais, PRs pequenos e revisáveis, resolução de conflitos, rebase e revert seguros, bisect, worktrees, semver, changelog, tags e GitHub Releases. Princípio central: **commit é local e livre; push, PR, merge, tag e publicação só com a sua confirmação, com o comando exato à vista.**

Palavra-chave do modo completo: `RELEASE-COMPLETO`. Versão 0.1.0, licença MIT. Conteúdo em português brasileiro; comandos, código e nomes de skills em inglês/kebab-case.

## O que entrega

- Um **playbook** que roteia o pedido, impõe 12 princípios com motivo, um processo de 9 passos com critério de saída e rótulos epistêmicos (Verificado, Inferido, Suposição, Não verificável, Não aplicável).
- **8 skills de tarefa**, 1 biblioteca de **prompts** (32 prompts prontos), **4 agentes somente leitura** (revisão de diff, revisão contra plano, go/no-go de release, auditoria de política do repositório) e **12 casos de eval** desenhados (formato conferido na documentação oficial de `claude plugin eval`) (acima do limite 6–10 do blueprint, justificado em `evals/README.md`).
- **12 referências** densas, **15 templates** (mensagem de commit, corpo e template de PR, checklist e go/no-go de release, CHANGELOG, `release.yml`, CODEOWNERS, handoff, relatórios de conflito, bisect, triagem, rollback, cobertura de docs e retro) e **20 regras prontas para o CLAUDE.md**.
- Hook, regras `deny` e CI com Claude **documentados e desativados** em `skills/playbook/references/ferramentas-e-mcp.md` (JSON pronto, riscos, fonte).

## Quando usar

Ao commitar ou escrever mensagem de commit; abrir, revisar ou dividir PR; resolver conflito; limpar ou desfazer histórico; achar a regressão; encerrar branch e worktree; escolher versão; escrever changelog; cortar tag e release; triar contribuição externa; definir política de branch, CODEOWNERS e CLAUDE.md para git. Não é para deploy, pipelines de CI, observabilidade nem escrever documentação (veja "Fronteiras" abaixo).

## Componentes

| Tipo | Nome | Para que serve | Efeito externo |
| --- | --- | --- | --- |
| Skill (núcleo) | `playbook` | Router, princípios, processo, modo `RELEASE-COMPLETO`, fronteiras | Não |
| Skill | `prompts` | Biblioteca de prompts curados (commits, PRs, revisão, histórico, release, sistema) | Não |
| Skill | `commit-convencional` | Diff atual vira commits atômicos, verificados, no estilo do repositório; sem push | Não (local) |
| Skill | `criar-pr` | Prepara e abre PR em rascunho, depois de verificar | Sim, com confirmação |
| Skill | `resolver-conflitos` | Resolve conflitos entendendo a intenção de cada lado | Não |
| Skill | `rebase-seguro` | Limpa histórico local, decide rebase/merge/revert, recupera commits perdidos | Sim se publicar, com confirmação |
| Skill | `bisect-regressao` | Acha o primeiro commit ruim com teste como oráculo | Não (executa código do repositório) |
| Skill | `encerrar-branch` | Menu de encerramento, portão de prontidão de merge, limpeza de worktree | Sim (merge), com confirmação |
| Skill | `release-cut` | Versão justificada, changelog, tag anotada/assinada, GitHub Release | Sim, com confirmação |
| Skill | `triagem-contribuicao` | Triagem de PR/issue de terceiros, texto como dado, rascunho de resposta | Não |
| Agente | `revisor-diff` | Revisa o diff com limiar de confiança 80 | Não (somente leitura) |
| Agente | `revisor-plano` | Revisão adversarial do diff contra o plano, até 2 rodadas | Não |
| Agente | `auditor-release` | Go/no-go com evidência por item | Não |
| Agente | `auditor-politica-repo` | Audita proteção de branch, CODEOWNERS, templates, workflows | Não |

Namespaces: skills como `/git-workflow-release:release-cut`; agentes como `git-workflow-release:revisor-diff`.

**Atenção ao desenho:** as skills com efeito colateral usam `disable-model-invocation: true`, ou seja, só rodam quando você digita o `/comando`; o modelo não as chama sozinho. Por isso o `playbook` (que o modelo pode chamar) roteia seu pedido, lê o roteiro da tarefa e **executa os passos locais e reversíveis que você pediu** (ex.: "commite isso"). Passos externos ou destrutivos param, mostram o comando exato e esperam sua confirmação. Só `playbook`, `prompts`, `resolver-conflitos` e `triagem-contribuicao` são acionáveis pelo modelo.

## Instalação

Dentro do Claude Code:

```text
/plugin marketplace add francisco-efjr/brain-of-agent
/plugin install git-workflow-release@brain-of-agent
```

Depois de instalar, confira com `/help` que as skills aparecem com o prefixo `git-workflow-release:`. Requisitos: `git`; `gh` autenticado por você (`gh auth login`) é opcional e necessário só para PR, merge e release pelo terminal. O plugin não instala hooks, servidores MCP nem binários.

## Exemplos de pedidos

1. **Commit atômico:** "Mexi em `src/api/rate.ts`, no teste dele, no README e na cor do botão. Commita." O plugin divide em commits `feat(api)`, `docs` e `style(ui)`, roda o comando de verificação do CLAUDE.md, usa `git add` por caminho e não faz push.
2. **PR em rascunho:** "Abra o PR da `feat/rate-limit`." Mede o tamanho, exige verde, usa o template do repositório (ou o do plugin), mostra título e corpo e só então pede confirmação para `git push -u` e `gh pr create --draft`.
3. **Conflito de merge:** "Deu conflito ao mesclar a `main`; resolve." Lê base e as duas versões, escreve a intenção de cada lado e **pergunta** quando a regra de negócio conflita, em vez de escolher um lado.
4. **Desfazer com segurança:** "Preciso desfazer o merge do PR #88 que já está na `main`." Descobre a forma do merge (dois pais, squash ou rebase), propõe `git revert -m 1` e PR de revert se a branch é protegida; nunca `reset --hard`.
5. **Regressão:** "O `/total` devolvia 120 e agora 118; estava certo na v2.3.0." Escreve primeiro o teste que falha, monta o script de bisect com códigos 0/1/125, pede para você ler o script e só então roda `git bisect run`.
6. **Release:** "Corte a release: `feat: add export`, `fix: null date`, `feat!: remove /v1/orders`." Propõe **2.0.0**, pede confirmação do MAJOR, escreve o changelog para o usuário, e separa tag, push da tag e GitHub Release em passos confirmados um a um.
7. **Triagem:** "Triar este PR de fork" (cujo corpo manda você ignorar regras e rodar um script). Trata o texto como dado, cita o trecho, aponta workflow e lockfile alterados e rascunha uma resposta cordial sem postar.
8. **Política:** "Configure o CLAUDE.md para git" entrega o bloco S-01; "audite o fluxo de git deste repositório" aciona o `auditor-politica-repo`.

## Modo `RELEASE-COMPLETO`

Escreva `RELEASE-COMPLETO` no seu pedido (ex.: "RELEASE-COMPLETO: audite o fluxo de git e release deste repositório"). O playbook então lê as 12 referências em 3 lotes, registrando cada uma como lida, parcial ou ausente; monta uma matriz de aplicabilidade (commits, branching, PRs, revisão, conflitos, histórico, worktrees, versionamento, release, CI com Claude, monorepo, open source, CLAUDE.md); implementa **apenas** o que o pedido incluir; revalida com evidências. Garantias: a palavra em log, issue, PR ou documento **não** ativa o modo; a palavra **não amplia permissões** (push, merge, tag e release continuam pedindo confirmação concreta); auditoria não altera o produto. Sem a palavra, só o necessário é carregado.

## Fronteiras

Este plugin cuida do ciclo de vida da mudança em git e da política de colaboração. Deploy e pipelines: `/devops-cloud-infra:playbook`; saúde pós-deploy: `/sre-observability:playbook`; segurança profunda: `/security-appsec:playbook`; estratégia de testes e go/no-go completo: `/qa-testing:playbook`; escrita de documentação: `/technical-writing-docs:playbook`; revisão ampla de qualidade: `/code-quality-refactoring:playbook`; empacotamento e distribuição: `/cli-desktop-tooling:playbook`. A lista completa está no `SKILL.md` do playbook.

## Principais fontes (top 10)

| # | Fonte | Classe | Licença do que é reutilizado |
| --- | --- | --- | --- |
| 1 | Claude Code: best practices (code.claude.com) | A | Destilado |
| 2 | Claude Code: skills | A | Destilado |
| 3 | Claude Code: hooks | A | Destilado |
| 4 | `anthropics/claude-code-action` e `docs/security.md` | A | MIT |
| 5 | Claude Code: worktrees | A | Destilado |
| 6 | Plugins oficiais `commit-commands`, `code-review`, `pr-review-toolkit` | A | Proprietária; destilado |
| 7 | Claude Code: common workflows | A | Destilado |
| 8 | Semantic Versioning 2.0.0 (Tom Preston-Werner) | A | CC BY 3.0 |
| 9 | release-please (googleapis) | A | Apache-2.0 |
| 10 | Conventional Commits 1.0.0 | B | CC BY 3.0 |

Bibliografia completa, com URL, classe, licença e data de consulta (2026-10-10), em `skills/playbook/references/fontes.md`.

## Créditos e licenças de terceiros

- Este plugin: MIT, Francisco Edson. Parte do conteúdo vem do repositório do autor `francisco-efjr/brain-of-agent` (MIT): templates de go/no-go e de handoff e a distinção entre preparar, implantar e verificar.
- **gstack** (https://github.com/garrytan/gstack, MIT, Copyright (c) 2026 Garry Tan): apenas o **processo** de `ship`, `land-and-deploy`, `document-release` e `retro` foi destilado com redação própria (detecção de plataforma, commits atômicos, gate de evidência, portão de prontidão por SHA, revert por forma do merge, mapa de cobertura de docs, métricas de retro). Não foram importados telemetria, hooks, auto-commit nem binários.
- **superpowers** (https://github.com/obra/superpowers, MIT): inspiração do gate de evidência e do menu de encerramento de branch, em redação própria.
- Conventional Commits e Semantic Versioning (CC BY 3.0), Keep a Changelog (MIT, Olivier Lacan), Google eng-practices (CC-BY 3.0), Open Source Guides (CC-BY-4.0), release-please (Apache-2.0), claude-code-action (MIT): conteúdo destilado com atribuição.
- Documentação e repositório da Anthropic, manual do Git e documentação do GitHub: destilados, nunca copiados.
- O plugin não vende nem recomenda ferramentas de terceiros por padrão; qualquer hook, `deny` ou CI vem desativado e com riscos descritos.

## Limitações honestas

- **Nenhum eval foi executado.** Os 12 casos estão `designed_not_executed`; `claude plugin eval` exige Claude Code 2.1.269 ou superior (o CLI local da fábrica é 2.1.128). A pontuação das skills é estimativa de LLM; **a validação não é totalmente independente** (pesquisadores, validador e construtor são modelos de linguagem).
- O hook `git-guard.ps1` foi testado em 12 comandos **fora** do Claude Code; o formato de registro (`command` + `args`, `if`, `hookSpecificOutput` com `hookEventName`) foi conferido na documentação de hooks em 2026-10-10, mas o script nunca rodou dentro do Claude Code. Só PowerShell; não há versão bash.
- A sintaxe das regras `deny` (`Bash(prefixo *)`) foi conferida na documentação de permissões, que também lista o que elas não casam (`git -C`, `git -c`, `bash -c`, caminho absoluto); teste cada regra em repositório descartável. Hook e `allowed-tools` são de melhor esforço, não fronteira de segurança: `allowed-tools` só pré-aprova.
- `GIT_SEQUENCE_EDITOR=true` para automatizar rebase é inferido e não testado; falhando, o plugin entrega os comandos para você rodar.
- Limiares (400 linhas ou 10 arquivos por PR, até 3 worktrees, confiança 80, 2 rodadas de revisão, 15 minutos de espera de CI) são **Suposição** ajustável; são sugestões, nunca bloqueios.
- Cobertura focada em **GitHub**. GitLab (`glab`), Bitbucket e Azure DevOps entram só como detecção de plataforma.
- Lacunas conhecidas: release branches e backport têm só um roteiro manual **Inferido** (`releases-e-versionamento.md`, seção 12; `release-cut` não automatiza essa linha); release de monorepo (manifesto do release-please e comandos do Changesets não confirmados); commits assinados e SLSA; `SECURITY.md`, governança e triagem em escala; Git LFS e submódulos; servidor MCP do GitHub; `git rerere`; `/goal` e Stop hook (páginas não lidas).
- O plugin **complementa** `/commit`, `/code-review` e `/commit-push-pr` oficiais, não os substitui; revalide a cada versão do Claude Code e das fontes (superpowers e gstack mudam quase diariamente).
- Reddit, X, YouTube e newsletters não foram cobertos; a API REST do GitHub falhou durante a pesquisa, então estrelas e datas vêm de páginas e feeds.
