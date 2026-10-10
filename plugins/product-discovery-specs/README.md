# Produto, descoberta e especificação (`product-discovery-specs`)

Plugin do Claude Code que transforma uma ideia ou um pedido vago em artefatos de produto **verificáveis antes do código**: entrevista guiada, PRD enxuto, spec testável (`FR-` e `SC-`), critérios de aceite (Given/When/Then, EARS), histórias INVEST, priorização (RICE, ICE, MoSCoW, Kano), roadmap, OKRs, experimentos A/B e plano de tarefas, com gates de aprovação humana e revisão adversarial em contexto novo.

Versão 0.1.0 · Licença MIT · Autor: Francisco Edson · Pesquisa e validação datadas de 2026-10-10.

## O que entrega

- **Processo proporcional:** uma escada N0 a N4 decide quanto de spec o pedido merece. Mudança cujo diff cabe numa frase não ganha spec nenhuma.
- **Entrevista sem inventar:** rodadas de até 3 perguntas, play back do que foi entendido e lacuna registrada como `[NEEDS CLARIFICATION]` em vez de chute.
- **Artefatos prontos:** 26 templates (spec, PRD, histórias, critérios, RICE, OKR, roadmap, pitch, experimento A/B, tarefas, plano, handoff e mais).
- **Verificabilidade:** todo requisito com check e oráculo; checklists `spec-readiness`, `prd-readiness`, `story-ready`, `sprint-ready` e `experiment-design`.
- **Revisão independente:** o agente `spec-reviewer` em contexto novo, somente leitura, apontando só lacunas de correção e de requisito.
- **Segurança por padrão:** nenhum hook, MCP, LSP ou `bin/` ativo; recomendações de ferramentas ficam documentadas e desativadas.

## Quando usar

Use quando faltam requisitos, quando precisa de PRD, spec, critérios de aceite, priorização, roadmap, OKR, roteiro de entrevista ou experimento, ou quando vai delegar a implementação a outra sessão. Não use para implementar código, desenhar arquitetura ou automatizar testes (veja as fronteiras no playbook) nem para mudança pequena já bem definida.

## Componentes

Skills se invocam como `/product-discovery-specs:<nome>`; agentes como `product-discovery-specs:<nome>`.

| Componente | Tipo | Para que serve |
| --- | --- | --- |
| `playbook` | skill | Router e processo essencial; escada N0 a N4; gates; referências; modo `PRODUTO-COMPLETO`; fronteiras com os outros plugins |
| `prompts` | skill | Biblioteca de 40 prompts prontos, prompt de sistema e mensagem inicial sugerida |
| `spec-interview` | skill | De um pedido vago a um `SPEC.md` aprovado, por entrevista |
| `write-prd` | skill | PRD enxuto com métricas, não-objetivos e quatro riscos |
| `write-spec` | skill | Spec de feature, spec de bugfix e atualização da spec após implementar |
| `acceptance-criteria` | skill | Critérios de aceite e revisão de histórias (palavras vagas, regras implícitas, NFR) |
| `refine-backlog` | skill | INVEST, divisão de histórias, Example Mapping, three amigos, planejamento de sprint |
| `prioritize-roadmap` | skill | RICE, ICE, MoSCoW, Kano, Now-Next-Later, OKR, pitch |
| `run-discovery` | skill | Roteiro de entrevista JTBD, árvore de oportunidades, quatro riscos, síntese, premissas, experimento A/B |
| `spec-to-tasks` | skill (só por comando explícito) | Spec aprovada para `tasks.md`, plano com IDs, lista de features e briefing |
| `spec-reviewer` | agente (somente leitura) | Revisão adversarial de spec, PRD, histórias e diff contra a spec |
| `plan-writer` | agente | Plano de implementação com IDs e critério de conclusão por fase (grava só no caminho que o pedido indicar, sugestão `plans/`; sem caminho, devolve o texto) |
| `feasibility-scout` | agente (somente leitura) | Mapeia o código que a spec toca e os riscos de viabilidade |
| `discovery-synthesizer` | agente (somente leitura) | Sintetiza notas de entrevistas sem fabricar falas |
| `decision-recorder` | agente | Registra decisões de produto (sugestão `docs/decisions/`; grava só no caminho indicado e nunca escolhe a opção pelo humano) |

Dentro de `skills/playbook/`: 12 referências (`references/`) e 26 templates (`assets/templates/`). Veja o mapa no `SKILL.md`.

## Instalação

Dentro de uma sessão do Claude Code:

```text
/plugin marketplace add francisco-efjr/brain-of-agent
/plugin install product-discovery-specs@brain-of-agent
```

Pela linha de comando:

```text
claude plugin marketplace add francisco-efjr/brain-of-agent
claude plugin install product-discovery-specs@brain-of-agent
```

O marketplace `dev-segments` é a raiz deste repositório (`.claude-plugin/marketplace.json`). Valide uma cópia local com `claude plugin validate <pasta-do-plugin>`.

## Exemplos de pedidos

1. "Quero adicionar login com Google no meu app de agenda (Next.js + Postgres, hoje só e-mail e senha). Já pode começar?" → `spec-interview`: não escreve código, faz até 3 perguntas, levanta regras implícitas (conta existente com o mesmo e-mail) e propõe um `SPEC.md` com lacunas marcadas.
2. "Escreva o PRD de um app de delivery de marmitas fit." → `write-prd`: sem problema, usuário e métrica, faz até 3 perguntas e para; não inventa tamanho de mercado.
3. "Critérios de aceite desta história: 'Como gerente quero exportar relatórios'. O export deve ser rápido e seguro, vários formatos etc." → `acceptance-criteria`: transforma "rápido", "vários" e "etc." em perguntas e escreve cenários declarativos com caminho negativo.
4. "Priorize com RICE: A (alcance 2000, impacto 2, confiança 80%, esforço 2), B (500, 3, 100%, 1), C (8000, 1, 50%, 4), D (300, 0,5, 100%, 0,5)." → `prioritize-roadmap`: 1600, 1500, 1000 e 300, mostra que A e B estão próximos e deixa a decisão com você.
5. "Monte o roteiro de entrevista para 5 gestores de clínicas sobre faltas de pacientes." → `run-discovery`: roteiro de 30 minutos em 4 blocos, perguntas sobre a última vez e sem pitch de solução.
6. "Vou rodar um A/B com 10 mil por braço, olhar toda manhã e parar quando p < 0,05. Taxa base 4%, quero detectar +0,5 ponto." → `run-discovery`: aponta o risco de parar ao ver significância e calcula cerca de 24,6 mil por braço pela regra de bolso.
7. "Quebre a spec em `specs/agenda/spec.md` em tarefas" → `/product-discovery-specs:spec-to-tasks specs/agenda/spec.md`: `tasks.md` com `T001 [P] [US1]`, checkpoints por história e gate G2.
8. "Revise esta spec antes de eu mandar codar." → agente `spec-reviewer`: tabela de achados com severidade, confiança e local.

## Modo `PRODUTO-COMPLETO`

Escreva `PRODUTO-COMPLETO` no chat, como pedido explícito, para cobertura integral: leitura das 12 referências em 4 lotes com registro `lido`, `parcial` ou `ausente`; matriz de aplicabilidade por área; produção dos artefatos aplicáveis dentro do escopo; revalidação com checklists e `spec-reviewer`; handoff.

O que o modo **não** faz: não é senha nem autorização; não amplia permissões (criar issue, publicar e escrever fora do combinado continuam pedindo confirmação); não ativa com a palavra em documento, ticket, transcrição ou log; não inventa requisitos nem pesquisa de usuários. Sem a keyword, o plugin aplica proporcionalidade e carrega só o necessário.

## Top 10 fontes

Bibliografia completa (45 itens, classe, URL, licença e data) em `skills/playbook/references/fontes.md`.

| # | Fonte | Classe |
| --- | --- | --- |
| 1 | Best practices for Claude Code (entrevista, explorar-planejar-implementar, verificação, revisor adversarial), https://code.claude.com/docs/en/best-practices | A |
| 2 | spec-kit, template de spec e de tarefas (GitHub, MIT), https://github.com/github/spec-kit | A |
| 3 | superpowers, skill `brainstorming` (Jesse Vincent, MIT), https://github.com/obra/superpowers | A |
| 4 | Plugin `feature-dev` da Anthropic (paradas obrigatórias, agente arquiteto de leitura) | A |
| 5 | Plugin `code-modernization` da Anthropic (`RULE-NNN`, Apache-2.0) | A |
| 6 | Effective harnesses for long-running agents (Anthropic Engineering), https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | A |
| 7 | How we built our multi-agent research system (Anthropic Engineering), https://www.anthropic.com/engineering/multi-agent-research-system | A |
| 8 | Skill authoring best practices e `skill-creator` (Anthropic) | A |
| 9 | Böckeler, "Understanding Spec-Driven-Development: Kiro, spec-kit and Tessl", https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html | A |
| 10 | Cucumber: Gherkin reference e "Writing better Gherkin", https://cucumber.io/docs/gherkin/reference/ | A |

## Créditos e licenças

- **brain-of-agent** (MIT, Francisco Edson): base de critérios de aceite, Example Mapping, three amigos, Gherkin, templates de revisão de história, handoff, decisão e plano.
- **GitHub spec-kit** (MIT, Copyright GitHub, Inc.), **obra/superpowers** (MIT, Jesse Vincent), **github/awesome-copilot** (MIT), **phuryn/pm-skills** (MIT), **snarktank/ralph** (MIT): ideias destiladas e reescritas.
- **anthropics/skills** (`skill-creator`) e **anthropics/claude-plugins-official** (`code-modernization`) (Apache-2.0, Anthropic) e **product-on-purpose/pm-skills** (Apache-2.0): destilados.
- **gstack** (MIT, Copyright (c) 2026 Garry Tan): inspiração de processo (premissas, alternativas, rodadas de especificação), sem cópia de texto.
- Documentação da Anthropic, Cucumber, Intercom, Shape Up (© 37signals), SVPG, Evan Miller, Mountain Goat, Scrum Guide e outros: apenas destilados com redação própria, com URL e classe em `fontes.md`.
- O repositório `deanpeters/Product-Manager-Skills` (CC BY-NC-SA 4.0) **não** foi usado.

Este plugin é distribuído sob MIT. Itens de terceiros mantêm as licenças de origem listadas acima.

## Limitações honestas

- **Organiza o processo; não promete ganho.** As fontes descrevem práticas e raramente medem resultado. Sinais de comunidade (Hacker News) são fracos e mistos.
- **Não substitui pesquisa com usuários nem decisão de negócio.** O modelo prepara e sintetiza; a descoberta e as escolhas continuam humanas.
- **Revisão pelo mesmo modelo não é validação externa.** O `spec-reviewer` ajuda, mas não substitui revisão humana.
- **Evals ainda não foram executados** (status `designed_not_executed`). `claude plugin eval` exige Claude Code 2.1.269 ou superior; a CLI local usada na construção é 2.1.128.
- **Calibrações são Suposição ou Inferido:** limiares N0 a N4, limite de 3 perguntas por rodada, definição de `story-ready`, perguntas-teste do INVEST e definição operacional de métrica. Meça e ajuste.
- **Lacunas de evidência:** JTBD sem fonte primária; experimentação avançada (OEC, SRM) fora do atlas; métricas de produto (North Star, HEART, AARRR) sem fonte validada; roadmap com uma única fonte autoatribuída; nenhuma fonte em português do Brasil (o texto em português é tradução e destilação).
- **Versões do Claude Code variam:** `AskUserQuestion`, `/goal`, `/verify`, sintaxe de hooks e de permissões devem ser conferidos na versão instalada; há fallback textual.
- **Licenças:** várias fontes oficiais não declaram licença de reuso; por isso o plugin só as destila.
