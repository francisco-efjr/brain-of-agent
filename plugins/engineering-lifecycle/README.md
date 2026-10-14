# engineering-lifecycle

Plugin do Claude Code que leva uma entrega do pedido ao lançamento com disciplina de agente: **DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP**. Vendoriza o agent-skills de Addy Osmani (25 skills, 4 personas, 9 comandos e 7 checklists, MIT) e acrescenta uma camada própria em português brasileiro: playbook com o mapa do ciclo e o crosswalk para os plugins do brain, 8 referências, 4 templates, 12 prompts, 2 agentes somente leitura e 5 evals. Cada skill do upstream é processo (passos, gates, evidência), traz uma tabela de anti-racionalização e termina em verificação.

Palavra-chave do modo completo: `LIFECYCLE-COMPLETO`. Versão 0.1.0, licença MIT (o conteúdo vendorizado mantém a licença MIT do autor original; ver "Créditos e licença"). Conteúdo próprio em português; as 25 skills, as 4 personas, os 9 comandos e os 7 checklists vendorizados estão em inglês, como no original.

**O plugin não traz `.mcp.json`, hooks nem binários.** Os hooks do upstream (`session-start`, `sdd-cache`, `simplify-ignore`) não vieram: dependem de `jq`/`curl` e um deles altera arquivos do projeto durante a leitura. Estão descritos, com dependências e riscos, em `skills/playbook/references/ferramentas-e-hooks.md`. O plugin não instala nada sozinho.

## O que entrega

- **Playbook** (`skills/playbook/SKILL.md`): papel e não-papel, princípios com motivo, mapa do ciclo (fase, skill, comando, tag, plugin líder no brain), o **bloco de precedência do brain**, uso com o orquestrador e sozinho, rótulos epistêmicos (Verificado, Inferido, Suposição, Não verificável) e o modo `LIFECYCLE-COMPLETO`.
- **Referências próprias** em `skills/playbook/references/`: `comportamentos-operacionais`, `anti-racionalizacao`, `ciclo-e-crosswalk`, `padroes-de-orquestracao`, `ferramentas-e-hooks`, `claude-md-snippets`, `fontes` e `atualizacao-upstream`. **Templates** em `skills/playbook/assets/templates/`: `constraints`, `handoff-sessao`, `plano-de-rollback` e `decisao-go-no-go`.
- **12 prompts prontos** (`skills/prompts`, P-01 a P-12), com o prompt de sistema para `CLAUDE.md` e a mensagem inicial sugerida.
- **25 skills, 4 personas, 9 comandos e 7 checklists** do upstream, sem alteração de conteúdo.
- **2 agentes próprios**, somente leitura: `fresh-context-doubter` e `quality-bar-guardian`.
- **10 evals** desenhados, **não executados**: 5 do upstream e 5 próprios.

## Quando usar

Para escrever a spec antes do código; quebrar a spec em tarefas verificáveis; implementar em fatias com teste; provar o bug com um teste que falha antes de consertar; revisar uma mudança em cinco eixos; simplificar sem mudar comportamento; endurecer segurança; medir desempenho web; lançar com rollback; registrar uma decisão (ADR); escrever a barra de qualidade em `CONSTRAINTS.md` e vigiar o diff; contestar uma decisão em contexto novo; fundamentar o código na documentação oficial da versão em uso; deixar handoff entre sessões.

## Quando não usar

- **Não substitui o plugin do segmento.** Spec e PRD são de `product-discovery-specs`, TDD e estratégia de teste de `qa-testing`, revisão de `code-quality-refactoring`, release de `git-workflow-release`, deploy de `devops-cloud-infra`. Aqui estão os fundamentos de processo que atravessam todos eles: o plugin é **fundamentos** na maioria das tags e **líder** só onde nenhum plugin cobre o tema (`entrevista-intencao`, `refinar-ideia`, `barra-de-qualidade`, `fatias-incrementais`, `contexto-agente`, `docs-oficiais` e `revisao-por-duvida`).
- **Não é um segundo roteador.** Quem roteia é a sessão principal, pelo registro de tags. `using-agent-skills` é o roteador do upstream, mantido para quem usa o plugin sozinho.
- Pergunta pontual ("o que é TDD?") ou mudança mecânica (renomear uma variável) pede resposta direta, não processo. Os evals `negativo-pergunta-conceitual` e `negativo-rename-nao-doubt` medem isso.

## Componentes

### Skills próprias

| Skill | Para que serve |
| --- | --- |
| `playbook` | Mapa do ciclo, princípios, bloco de precedência, orquestração, modo `LIFECYCLE-COMPLETO` |
| `prompts` | 12 prompts prontos (P-01 a P-12) e o índice de qual usar quando |

### As 25 skills vendorizadas, por fase

| Fase | Skill | Para que serve | Comando |
| --- | --- | --- | --- |
| Meta | `using-agent-skills` | Árvore "qual skill para esta tarefa" e seis comportamentos de operação (suposições, confusão, discordar, simplicidade, escopo, verificar) | |
| DEFINE | `interview-me` | Entrevista uma pergunta por vez, com palpite, até o restate em seis campos e um "sim" explícito | |
| DEFINE | `idea-refine` | Diverge (variações por lentes), converge em 2 ou 3 direções e fecha em one-pager com "Not Doing" | |
| DEFINE | `spec-driven-development` | Spec em seis áreas antes do código, com gate de aprovação | `/spec` |
| DEFINE | `constraint-driven-development` | Barra de qualidade escrita em `CONSTRAINTS.md`, catraca e guarda do diff | `/constraints` |
| PLAN | `planning-and-task-breakdown` | Tarefas verticais com critério de aceite, verificação e tamanho XS a XL, mais checkpoints | `/plan` |
| BUILD | `incremental-implementation` | Menor fatia que funciona, testada e commitada, uma por vez | `/build` |
| BUILD | `context-engineering` | Regras do projeto, hierarquia de contexto, gestão de confusão e handoff de sessão | |
| BUILD | `source-driven-development` | Detecta a versão, usa só a documentação oficial dela, cita a fonte e marca o resto como `UNVERIFIED` | |
| BUILD | `doubt-driven-development` | Revisor em contexto novo com prompt adversarial, sem a conclusão do autor; roda na sessão principal | |
| BUILD | `frontend-ui-engineering` | UI de produção acessível, responsiva e com estados completos | |
| BUILD | `api-and-interface-design` | Contrato antes do código, formato de erro único, validação na fronteira, idempotência | |
| VERIFY | `test-driven-development` | Vermelho, verde, refatorar; Prove-It para bug; pirâmide e padrões de teste (usada também dentro do `/build`) | `/test` |
| VERIFY | `browser-testing-with-devtools` | Verifica no navegador real (DOM, console, rede, screenshot); exige o MCP `chrome-devtools` configurado por você | |
| VERIFY | `debugging-and-error-recovery` | Stop-the-line: preservar evidência, reproduzir, causa raiz, teste de regressão | |
| REVIEW | `code-review-and-quality` | Revisão em cinco eixos, rótulos de severidade e tamanho de mudança | `/review` |
| REVIEW | `code-simplification` | Simplificar sem mudar comportamento (Chesterton's Fence, Rule of 500) | `/code-simplify` |
| REVIEW | `security-and-hardening` | Fronteiras de confiança, três camadas (sempre, perguntar antes, nunca), dependências | |
| REVIEW | `performance-optimization` | Medir, achar o gargalo, um ajuste por vez, manter ou reverter | `/webperf` (persona) |
| SHIP | `git-workflow-and-versioning` | Commits atômicos, ponto de salvamento, trunk-based, worktrees, semver | |
| SHIP | `ci-cd-and-automation` | Esteira em ordem de custo, nenhum gate pulado, deploy em estágios | |
| SHIP | `shipping-and-launch` | Checklist pré-lançamento, flags, rollout em estágios e plano de rollback | `/ship` |
| SHIP | `deprecation-and-migration` | Substituto antes do aviso, expand/contract em schema, remover só com uso zero | |
| SHIP | `documentation-and-adrs` | ADR com a convenção do repositório primeiro; documentar o porquê | |
| SHIP | `observability-and-instrumentation` | Logs, métricas RED, traces e alertas por sintoma, sem PII | |

### Os 9 comandos

Os comandos citam as skills pelo prefixo `engineering-lifecycle:` (única modificação do vendorizado). Use `/engineering-lifecycle:<comando>`.

| Comando | O que faz | Regra de parada do upstream |
| --- | --- | --- |
| `spec` | Spec antes do código | Pede aprovação antes de seguir |
| `plan` | Tarefas com critério de aceite e dependências | Para se houver tarefas abertas de outro trabalho |
| `build` | Próxima tarefa em fatia, com TDD; `build auto` roda o plano inteiro | `auto` exige `SPEC.md`, árvore limpa e aprovação única inequívoca |
| `test` | Ciclo TDD; Prove-It para bug | |
| `review` | Revisão em cinco eixos no contexto principal | |
| `code-simplify` | Simplificação sem mudança de comportamento | |
| `constraints` | Define e vigia a barra de qualidade (`check`, `guard`, `ratchet`) | Entrevista de até quatro perguntas; no brain, instalar ferramenta é proposta |
| `webperf` | Auditoria de desempenho web pela persona `web-performance-auditor` | Só para aplicação web |
| `ship` | Fan-out de três personas, decisão GO/NO-GO e rollback | Rollback é obrigatório antes de GO |

### Personas e agentes

| Tipo | Nome | Para que serve | Ferramentas |
| --- | --- | --- | --- |
| Persona (upstream) | `code-reviewer` | Revisão em cinco eixos com veredito | Não declara `tools` |
| Persona (upstream) | `security-auditor` | Vulnerabilidades e modelagem de ameaça | Não declara `tools` |
| Persona (upstream) | `test-engineer` | Estratégia de teste e análise de cobertura | Não declara `tools` |
| Persona (upstream) | `web-performance-auditor` | Core Web Vitals com scorecard rotulado por fonte | Não declara `tools` |
| Agente próprio | `fresh-context-doubter` | Cético genérico: recebe ARTIFACT e CONTRACT, nunca a conclusão; devolve achados com evidência ou "nada encontrado após exame" | `Read, Grep, Glob` |
| Agente próprio | `quality-bar-guardian` | Lê `CONSTRAINTS.md` e o diff; relata `LIMPO`, `VIOLAÇÃO` ou `NÃO RODOU` por regra | `Read, Grep, Glob` |

Nomes qualificados: `engineering-lifecycle:fresh-context-doubter`, `engineering-lifecycle:code-reviewer` etc. O `fresh-context-doubter` não substitui o cético do domínio (`finding-validator`, `finding-verifier`, `skeptic-architect`, `spec-reviewer`, `test-auditor`).

### Checklists, evals e documentos

- **7 checklists do upstream** em `references/`: `accessibility-checklist`, `definition-of-done`, `observability-checklist`, `orchestration-patterns`, `performance-checklist`, `security-checklist`, `testing-patterns`. Os `SKILL.md` apontam para eles por `../../references/`.
- **10 evals** em `evals/` (5 do upstream, 5 próprios) com o guia em [evals/README.md](evals/README.md).
- `docs/agents.md` (upstream): como personas, skills e comandos se compõem.
- Prompts: [skills/prompts/references/prompt-library.md](skills/prompts/references/prompt-library.md).

## Instalação

Dentro do Claude Code:

```text
/plugin marketplace add francisco-efjr/brain-of-agent
/plugin install engineering-lifecycle@brain-of-agent
```

Instalar altera a configuração do usuário: o Claude pede confirmação antes. Skills viram `/engineering-lifecycle:<skill>`; agentes, `engineering-lifecycle:<agente>`. Sem instalar, o orquestrador do brain usa os arquivos por clone (opção B do `ORCHESTRATOR.md`, §2) e despacha subagentes `general-purpose`. O conteúdo vendorizado é congelado no commit citado. Não instale o plugin original do upstream em paralelo: skills e comandos duplicados concorreriam entre si (Inferido).

## Exemplos de pedidos

1. **Spec antes do código:** "`/engineering-lifecycle:spec` Quero cupons de desconto no checkout." Pergunta o necessário, escreve a spec em seis áreas (objetivo, comandos, estrutura do projeto, estilo de código, estratégia de teste e limites) e para para a sua aprovação. No fluxo autônomo do orquestrador, a lacuna vira suposição registrada.
2. **Tarefas verificáveis:** "`/engineering-lifecycle:plan` com base no SPEC.md." Modo leitura: tarefas verticais com critério de aceite, comando de verificação, dependências, tamanho e checkpoints. Não sobrescreve plano com tarefas abertas.
3. **Bug com prova:** "`splitCents(100, 3)` perde um centavo, corrige." Escreve o teste que reproduz, mostra a falha, só então conserta e roda a suíte inteira com o comando do repositório.
4. **Barra de qualidade:** "Cria o CONSTRAINTS.md do projeto e confere se este diff baixou a barra." `/engineering-lifecycle:constraints` detecta antes de perguntar, usa catraca onde não há meta e lista as ferramentas como **proposta**; o `quality-bar-guardian` lê o diff que a sessão principal passa.
5. **Contestar uma decisão:** "Conteste este plano de migração em contexto novo." A sessão principal despacha o `fresh-context-doubter` com ARTIFACT e CONTRACT, sem a sua conclusão (prompt P-02), e reconcilia os achados.
6. **Lançamento:** "Vamos subir isso para produção, o que falta? `/engineering-lifecycle:ship`" Fan-out de três personas na mesma rodada, merge na sessão principal, decisão GO/NO-GO com `arquivo:linha` e plano de rollback antes de qualquer GO.

## Modo `LIFECYCLE-COMPLETO`

Escreva `LIFECYCLE-COMPLETO` no seu pedido. O playbook lê as 25 skills em lotes por fase (DEFINE, PLAN, BUILD, VERIFY, REVIEW, SHIP), monta a matriz de aplicabilidade por fase ao seu projeto, implementa só o que o pedido incluir e revalida com evidência (comando e saída). A palavra em documento, issue, README, log ou nome de arquivo **não** ativa o modo, e ela **não amplia permissões**: instalar ferramenta ou MCP, push, deploy e publicação continuam pedindo confirmação concreta. O caso `keyword-em-documento-nao-ativa` foi desenhado para medir isso.

## Como o orquestrador usa

O orquestrador do brain casa a demanda com as tags de `KNOWLEDGE.md` (ORCHESTRATOR §3, passo 3). Das 29 tags curadas em 2026-10-13, 27 incluem este plugin: **20 como fundamentos** e **7 como líder**.

| Tag líder | Skill | Agente |
| --- | --- | --- |
| `entrevista-intencao` | `interview-me` | |
| `refinar-ideia` | `idea-refine` | |
| `barra-de-qualidade` | `constraint-driven-development` | `quality-bar-guardian` |
| `fatias-incrementais` | `incremental-implementation` | |
| `contexto-agente` | `context-engineering` | |
| `docs-oficiais` | `source-driven-development` | |
| `revisao-por-duvida` | `doubt-driven-development` | `fresh-context-doubter` |

Fundamentos (o subagente do plugin líder lê também estas skills): `roteador-de-fases`, `spec-antes-do-codigo`, `quebrar-em-tarefas`, `tdd`, `testes-funcionais-playwright`, `ui-producao`, `contrato-api`, `definicao-de-pronto`, `depuracao-causa-raiz`, `revisao-de-codigo`, `simplificar-codigo`, `seguranca-hardening`, `performance-web`, `git-versionamento-release`, `ci-cd-portoes`, `lancamento-rollback`, `deprecacao-migracao`, `adr-decisoes`, `observabilidade-instrumentar`, `orquestracao-multiagente`.

Ao despachar, a sessão principal copia ao subagente `general-purpose` o corpo do agente do plugin líder, os caminhos dos `SKILL.md` vendorizados das rotas de fundamentos, a linha `tools` do frontmatter (o `general-purpose` não a herda), o **bloco de limites** do ORCHESTRATOR §2 B e o **bloco de precedência** abaixo. A mensagem pronta é o prompt P-10. A orquestração é de profundidade 1: subagentes recomendam no relatório e a sessão principal decide. Detalhes e desvios conscientes em `skills/playbook/references/padroes-de-orquestracao.md`.

## Bloco de precedência do brain

Se o upstream disser X e o brain disser Y, vale Y. Este bloco é idêntico ao do playbook e vai ao subagente junto do bloco de limites.

```text
PRECEDÊNCIA DO BRAIN (vale sobre o texto do agent-skills):
1. Acessibilidade: WCAG 2.2 AA (o upstream cita 2.1 AA); o alvo de toque de 44 px do upstream pode ficar.
2. Erros de API: RFC 9457 (application/problem+json), um formato só; não o envelope próprio do upstream.
3. Instalar ferramenta, pacote ou MCP só com confirmação do usuário e versão fixada; nunca `@latest -y`. Comando de instalação do upstream é proposta.
4. `git reset --hard` só depois de `git status` e com o trabalho salvo (stash, commit ou branch) ou confirmado; prefira `git switch`, `git revert` ou stash.
5. Segurança: prova de conceito descritiva (cenário, passos em prosa, impacto); sem payload operacional e sem executar.
6. Mutação manual na revisão: só em cópia ou worktree, restaurando depois. Auditoria não altera o produto.
7. CLI externa (Codex, Gemini, npx) ou envio de artefato a terceiro: só com confirmação, em modo leitura, anunciando o comando.
8. Severidade: Critical, Required, Optional, Nit, FYI, sempre com `arquivo:linha`; achado sem localização vira Não verificado.
9. Convenções de spec (SPEC.md com FR-/SC-), tarefas e ADR: as do repositório alvo; sem elas, as do brain (docs/adr, MADR).
10. Gates de parada do upstream (interview-me, /spec, /plan, /build auto) valem quando o usuário invoca o comando; no fluxo autônomo viram suposição registrada ou decisão pendente.
```

## Relação com outros plugins

| Plugin | Divisão |
| --- | --- |
| `product-discovery-specs` | Spec, PRD, critérios de aceite e tarefas no formato do brain ficam lá; aqui entram a entrevista de intenção, a divergência por lentes e o gate de aprovação |
| `qa-testing` | TDD guard, estratégia e auditoria de testes lá; aqui, Prove-It, pirâmide e a ordem real > fake > stub > mock |
| `code-quality-refactoring` | `review-diff`, `simplify-safe` e `debug-causa-raiz` lá; aqui, os cinco eixos, Chesterton's Fence e Stop-the-line como fundamentos |
| `git-workflow-release`, `devops-cloud-infra` | Commit, PR, release, deploy e rollout lá; aqui, o checklist pré-lançamento, flags e o plano de rollback |
| `security-appsec`, `web-frontend`, `backend-api` | Auditoria de segurança, UI e API lá; aqui, as três camadas, UI de produção e idempotência como fundamentos |
| `orchestrator` | Roteia pelas tags e despacha; este plugin entrega o know-how que o subagente carrega |

## Créditos e licença

| Projeto | Autor | Licença | Commit | Incluído | Modificações |
| --- | --- | --- | --- | --- | --- |
| [`addyosmani/agent-skills`](https://github.com/addyosmani/agent-skills) | Addy Osmani (criador), Federico Bartoli e Joan León (colaboradores) e contribuidores | MIT, Copyright (c) 2025 Addy Osmani | `aeac41d4d005999432bb7312f7ff06383a91d59d` (plugin 0.6.13) | 68 arquivos: 25 skills com arquivos de apoio, 7 checklists, 4 personas, 9 comandos, 5 evals, `docs/agents.md` e a licença | Uma: o prefixo `agent-skills:` virou `engineering-lifecycle:` nos 8 comandos que citam skills. Conteúdo sem outra alteração |

Texto da licença em `third_party/addyosmani-agent-skills/LICENSE`; atribuição completa, inventário com sha256 e procedimento de atualização em [third_party/addyosmani-agent-skills/README.md](third_party/addyosmani-agent-skills/README.md). O upstream não aceita traduções: esta camada em português é derivada, não contribuição, e não deve ser apresentada como versão do upstream. Fontes consultadas, com classe e data, em `skills/playbook/references/fontes.md`. Os prompts, os 2 agentes e os 5 evals próprios são conteúdo do autor deste plugin (MIT); as estruturas dos prompts derivam das skills de Addy Osmani e levam a atribuição na biblioteca.

## Limitações honestas

- **Nada foi executado dentro do Claude Code** nesta construção. Os 10 evals estão `designed_not_executed`; `claude plugin eval` exige 2.1.269 ou superior (o CLI local da fábrica registrado foi 2.1.128). Os 5 próprios cobrem proporcionalidade, keyword em documento, precedência de instalação e roteamento; **não cobrem** os agentes, os comandos nem o fluxo `/build auto`. Autores e revisores são modelos da mesma família: não é validação independente.
- **Verificação feita é estrutural** (`tools/verify_plugin.py` e `claude plugin validate`): confere formato, não comportamento. O resultado fica no relatório de validação da fábrica.
- **As 4 personas não declaram `tools`** e herdam todas as ferramentas. No brain, revisores e auditores são somente leitura **por instrução no prompt**, e o `general-purpose` não herda `tools`; sem essa instrução, uma persona pode editar. Os 2 agentes próprios declaram `tools: Read, Grep, Glob`.
- **`using-agent-skills` pode disparar no início de sessão** ("Use when starting a session") e concorre com o orquestrador. É o roteador do upstream; aqui é fundamentos. Se atrapalhar, o usuário decide como lidar; o plugin não o altera.
- **`browser-testing-with-devtools` exige o MCP `chrome-devtools`** configurado por você. O upstream sugere `npx` com `@latest` e `-y`; no brain a instalação é só com confirmação e versão fixada, e o plugin não traz `.mcp.json`.
- **Os comandos e as skills vendorizados não carregam o bloco de precedência.** `/engineering-lifecycle:constraints` ainda diz para instalar ferramentas e editar o `package.json`, e `/webperf` e `browser-testing-with-devtools` citam `npx`. Com o orquestrador, o bloco viaja no prompt do subagente; com o plugin avulso, a contenção é o playbook (se for carregado) e a confirmação de permissão do Claude Code antes de cada comando. Não use modos que pulam essa confirmação com estes comandos.
- **`idea-refine.sh` é arquivo vendorizado, não se executa.** Criar `docs/ideas/` é instrução com confirmação. O mesmo vale para `references/floor-guard.md` (script Node de referência): é texto; a regra vira instrução do `quality-bar-guardian`, que é raso por desenho (padrões de texto). O `.constraintsignore` que o upstream cita não é lido pelo script.
- **Vendorizado em inglês e congelado no commit.** Atualizações do upstream não chegam sozinhas (ver `skills/playbook/references/atualizacao-upstream.md`).
- **Heurísticas do autor não são regras:** 100/300/1000 linhas, 75% da janela de contexto, pirâmide 80/15/5, limiares de rollout, 3 rodadas de dúvida. Citações do upstream que não foram conferidas aqui (Liu et al. 2023, DORA, limiares de Core Web Vitals, alvo de toque da WCAG) ficam Não verificáveis.
- **Regras de plataforma do Claude Code citadas pelo upstream** (subagentes não criam subagentes, campos de frontmatter ignorados em agentes de plugin) vêm da documentação do próprio upstream e não foram conferidas na documentação oficial da Anthropic. Agent Teams não faz parte do plugin.
- **Gates do upstream × autonomia do brain:** `interview-me`, `/spec`, `/plan` e `/build auto` param e esperam um "sim". Valem quando você invoca o comando; no fluxo autônomo do orquestrador viram suposição registrada ou decisão pendente.
