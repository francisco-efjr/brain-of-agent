# Contexto completo: como o Brain of Agent foi feito e como manter

Período do trabalho: 2026-10-09 a 2026-10-11. Estado descrito: 2026-10-10. Idioma: português brasileiro; termos técnicos, comandos e código em inglês.

Versão de uma página para colar em chats: [CONTEXTO-CURTO.md](CONTEXTO-CURTO.md). Método de pesquisa reutilizável em outros domínios: [METODO-PESQUISA.md](METODO-PESQUISA.md). Catálogo: [CATALOGO.md](CATALOGO.md).

Fonte dos números: o plano de execução da fábrica local (histórico de lotes e medições de uso), os `BUILD-REPORT*.md` e `VALIDATED.md` de cada segmento, o relatório de validação do kit de design e os scripts. Onde um número não tem fonte, ele não aparece.

## 1. Objetivo e resultado

**Objetivo.** Pesquisar de forma ampla e verificada os melhores prompts, skills, subagentes, regras de CLAUDE.md, checklists e workflows para cada segmento de desenvolvimento de software e transformar o material filtrado em **um plugin do Claude Code por segmento**, instalável e reutilizável. Também criar um **orquestrador**: dado o link do repositório e uma demanda, uma IA escolhe os especialistas, despacha, exige validação independente e entrega.

**Resultado em 2026-10-11** (marketplace `brain-of-agent`, 27 entradas: 25 segmentos, o kit e o orquestrador):

| Entrega | Situação |
| --- | --- |
| 25 plugins de segmento | Publicados, cada um com verificador estrutural sem erros e relatório de validação de qualidade |
| `orchestrator` 0.2.0 | Publicado: protocolo, modo melhoria e biblioteca de prompts O-01 a O-08 |
| `design-engineering-kit` | Publicado (opcional): 17 skills de terceiros (MIT), playbook, 16 prompts, 2 agentes, 8 evals |
| `saas-multitenant`, `fintech-payments`, `ecommerce-marketplace` | Último lote (2026-10-11), depois de uma rodada extra de complemento de pesquisa, com validador de qualidade Opus por envolverem dinheiro e dados. Qualidade média de 87,6 a 92,8. |
| Design system da casa (Mo baile) | Incorporado em `design-systems/mo-baile/` e referenciado por `ux-ui-design` e pelo orquestrador |
| Brains próprios `qa` e `fullstack`, `vendor/gstack` | Já existiam; o orquestrador os usa (`QA-COMPLETO`, `FULLSTACK-COMPLETO`) |

Os 25 segmentos planejados estão em [foundation/segments.json](foundation/segments.json). Os que ainda não passaram pelo gate aparecem como pendentes em [catalog.json](catalog.json) e em [CATALOGO.md](CATALOGO.md).

## 2. Arquitetura

### 2.1 Repositório publicado (`brain-of-agent`, privado)

| Caminho | Conteúdo |
| --- | --- |
| [ORCHESTRATOR.md](../../ORCHESTRATOR.md) | Protocolo do orquestrador (acesso, fluxo, modo melhoria §3.1, regras, formato de entrega) |
| `.claude-plugin/marketplace.json` | Marketplace `brain-of-agent` (gerado por `publish_brain.py`) |
| [plugins/](../../plugins/) | Um plugin por segmento, mais `orchestrator` e `design-engineering-kit` |
| [design-systems/mo-baile/](../../design-systems/mo-baile/) | Design system da casa, criado pelo usuário |
| [docs/dev-segments/](README.md) | Esta documentação: [foundation/](foundation/), `research/<segmento>/`, [CATALOGO.md](CATALOGO.md), [catalog.json](catalog.json) |
| [tools/dev-segments/](../../tools/dev-segments/) | `verify_plugin.py` e os workflows `research-v2.js` e `build-v2.js` |
| `brains/qa`, `brains/fullstack`, `vendor/gstack` | Base anterior do repositório |

Em `research/<segmento>/` só entram arquivos validados: `_leads.md`, `VALIDATED.md`, `SYNTHESIS.md` e relatórios de build. A pesquisa bruta dos pesquisadores baratos **não** é publicada.

### 2.2 Fábrica local (não publicada)

Pasta de trabalho separada, com a mesma estrutura mais o que não vai a público:

```text
<fábrica>/
├── docs/foundation/          base compartilhada (vai para docs/dev-segments/foundation;
│                             a subpasta brain-of-agent-snapshot/ só existe aqui, não é publicada)
├── docs/research/_global/    atlas global; docs/research/<slug>/ pesquisa por segmento
├── docs/PLANO-EXECUCAO.md    histórico, estado e roteiro de retomada (só local)
├── plugins/<slug>/           plugins em construção ou prontos
├── design-systems/           design systems da casa
├── tools/verify_plugin.py    verificador estrutural determinístico
├── tools/publish_brain.py    publicação controlada no brain-of-agent
├── tools/workflows/          research-v2.js, build-v2.js (e legacy/)
└── publish/                  ORCHESTRATOR.md e dev-segments-README.md (fonte dos dois arquivos publicados)
```

### 2.3 Fluxo ponta a ponta

```text
base compartilhada -> atlas global (6 tópicos, validados) -> pistas por segmento (_leads.md)
-> 3 lentes de pesquisa por segmento -> validador independente (+ rodada de lacunas)
-> síntese (desenho do plugin) -> crítico independente
-> 3 construtores em paralelo -> validador estrutural -> validador de qualidade -> gate
-> publish_brain.py (só publica o validado) -> commit e push (com autorização)
```

## 3. Pipeline de pesquisa (`research-v2.js`)

Fontes: [research-v2.js](../../tools/dev-segments/workflows/research-v2.js), [foundation/](foundation/).

**Base compartilhada.** Antes de qualquer pesquisa, foram escritos e conferidos contra a documentação oficial: [plugin-format-spec.md](foundation/plugin-format-spec.md), [plugin-blueprint.md](foundation/plugin-blueprint.md), [prompt-quality-rubric.md](foundation/prompt-quality-rubric.md) (D1 a D12), [source-quality-rubric.md](foundation/source-quality-rubric.md) (A/B/C), [research-file-format.md](foundation/research-file-format.md), [house-style.md](foundation/house-style.md) e [segments.json](foundation/segments.json). Todos os agentes recebem os mesmos arquivos, então "bom" significa a mesma coisa para pesquisador, validador, construtor e crítico.

**Atlas global (`mode: "atlas"`).** Seis tópicos transversais: corpus oficial da Anthropic, ecossistema comunitário do Claude Code, regras de outras ferramentas de IA para código, cânone de engenharia de prompt, pulso da comunidade e análise do próprio brain-of-agent. Cada tópico é pesquisado, depois validado por outro agente que reverifica uma amostra (cerca de 30%, priorizando classe A e números) e grava uma versão condensada. Um indexador gera `_leads.md` por segmento e [prompt-principles.md](foundation/prompt-principles.md), lido por todos os construtores e validadores. Custo medido do atlas: cerca de 6% da janela de uso de 5 horas.

**Pesquisa por segmento (`mode: "segments"`).** Para cada segmento:

1. **Três lentes em paralelo.** `authoritative` (Anthropic, documentação e normas, autores de referência), `github` (prompts, skills, agentes e regras em repositórios, conferindo estrelas, licença e último push pela API pública) e `community` (Reddit, Hacker News, vídeos, newsletters, blogs de praticantes). Meta por lente: 15 a 30 itens, ao menos 10 reaproveitáveis, com 15 a 25 consultas e 15 ou mais páginas lidas.
2. **Validador independente** (um por segmento, sobre as três lentes). Reverifica todos os itens classe A e todo item que vira prompt, no mínimo 40% do total; pontua prompts pela rubrica D1 a D12; checa licença e injeção; deduplica entre lentes; grava `VALIDATED.md`. Veredito `pass` com 18 ou mais itens aprovados e cobertura razoável; senão `needs_more` com lacunas objetivas.
3. **Rodada de lacunas.** Se `needs_more`, um pesquisador faz 10 ou mais consultas só nas lacunas (`gapfill.md`) e o validador roda de novo, agora acrescentando a `VALIDATED.md`.
4. **Síntese.** Um agente desenha o plugin (`SYNTHESIS.md`): nomes de skills e agentes, prompts planejados, snippets de CLAUDE.md, evals, fronteiras com outros segmentos. É a fonte única dos construtores.
5. **Crítico independente.** Pontua o desenho, corrige direto o que for claro e acrescenta "Revisão do crítico". `rework` só para falha estrutural; nesse caso há uma segunda síntese.

**Modelos por camada e por quê.** Preços de referência anotados no script (por milhão de tokens, entrada/saída, 2026-10): Fable 10/50, Opus 5.5 4/20, Sonnet 5.5 2/10, Haiku 5.5 0,10/0,50.

| Camada | Modelo | Motivo |
| --- | --- | --- |
| Pesquisa (3 lentes, lacunas) | Haiku 5.5 | Volume alto de leitura e coleta; erros são esperados e capturados na camada seguinte |
| Validação, síntese, índice do atlas | Sonnet 5.5 | Exige verificar de verdade e raciocinar sobre o desenho, a custo médio |
| Crítico | Opus 5.5 | Poucas chamadas, decisão de maior alavancagem |

Princípio: o modelo mais barato coleta, outro mais forte verifica. Na pesquisa e no desenho, autor e validador são modelos diferentes. Exceção declarada: nos plugins de nicho dos lotes 1 e 2 da construção (sem dinheiro, dados sensíveis ou segurança), o plano registra validador de qualidade Sonnet 5.5, o mesmo modelo dos construtores, em outro agente e com outra instrução. Nos demais, o validador de qualidade é Opus 5.5.

**Disjuntor.** A função `run()` envolve cada agente. Após 3 falhas seguidas (sinal de limite de uso), ela para de lançar novos agentes e o script devolve o que já concluiu. Retoma-se depois com `resumeFromRunId`, sem refazer o que já está em disco.

**Lições da 1ª tentativa.** Em 2026-10-09, por volta das 21:00 (horário local do plano, UTC−4), todos os agentes rodaram no modelo mais caro e a janela de 5 horas acabou em cerca de 25 minutos. Sobraram em disco 5 arquivos do atlas. A retomada reaproveitou esses arquivos e adotou: modelos por camada, execução em lotes, disjuntor e **medição de uso entre lotes** (se a janela passa de cerca de 70%, não se lança novo lote; acima de cerca de 85%, para-se e registra-se o ponto exato). Os scripts antigos ficaram em `tools/workflows/legacy/` na fábrica.

**Resultados medidos** (do plano de execução):
- Lote A: 12 segmentos, 80 de 80 agentes concluídos, 12 sínteses aprovadas pelo crítico com notas de 82 a 87.
- Mini-lote: `mobile-apps` (crítico 84) e `ux-ui-design` (crítico 86).
- Lote B: 11 segmentos, 76 de 76 agentes. Resultado: os 25 segmentos têm `VALIDATED.md` e `SYNTHESIS.md` aprovados.
- `fintech-payments` (13 itens), `ecommerce-marketplace` (10) e `saas-multitenant` (21) saíram finos; ganharam uma rodada de complemento (`gapfill2.md`, "rodada 3"): +20, +15 e +21 itens validados, respectivamente.

## 4. Pipeline de construção (`build-v2.js`, `mode: "plugins"`)

Fonte: [build-v2.js](../../tools/dev-segments/workflows/build-v2.js). O `verify_plugin.py` exige as skills `playbook` e `prompts` em todo plugin. Para cada plugin:

1. **Três construtores em paralelo** (Sonnet 5.5), cada um dono de uma parte e proibido de escrever fora dela:
   - `core`: `plugin.json`, `README.md` e a skill `playbook` (router, princípios com porquê, processo, modo `<SEGMENTO>-COMPLETO`, fronteiras) com 6 a 10 referências e templates;
   - `tasks`: 5 a 8 skills de tarefa;
   - `agents-prompts-evals`: 3 a 5 agentes, a skill `prompts` (20 ou mais prompts) e 8 ou mais evals no formato oficial.
2. **Validador estrutural** (Haiku 5.5): roda [verify_plugin.py](../../tools/dev-segments/verify_plugin.py) e `claude plugin validate`, corrige erros, compara com o `SYNTHESIS.md` e grava `BUILD-REPORT-structural.md`.
3. **Validador de qualidade** (Opus 5.5; Sonnet 5.5 nos nichos via `args.sonnetQuality`): outro modelo, adversarial; pontua cada `SKILL.md`, agente, amostra de 10 ou mais prompts e os evals pela rubrica D1 a D12 **antes e depois**, corrige até 80 ou mais em tudo, confere fatos técnicos e licenças, grava `BUILD-REPORT-quality.md`.
4. **Gate** (Haiku 5.5): roda os dois verificadores, conta componentes e consolida `BUILD-REPORT.md`. `pass` exige verificador sem erros e `claude plugin validate` aprovado.

**Regras de construção** (valem para todos): sem hooks, `.mcp.json`, `.lsp.json` ou `bin/` ativos (o verificador reprova); recomendações de MCP e hooks ficam documentadas e desativadas em `references/ferramentas-e-mcp.md`; nunca recomendar `--dangerously-skip-permissions` como padrão; revisores e auditores sem `Write`/`Edit`; ao menos 1 eval negativo (a skill não deve disparar) e 1 de escopo/segurança; evals começam como `designed_not_executed`.

**Lições incorporadas depois de um teste real** em um app Android real do usuário (a skill de arquitetura foi aplicada e os achados voltaram ao construtor; `architecture-design` foi para 0.2.0):
- Contrato de entrega coerente com as ferramentas: agente sem `Write` devolve o documento completo com o caminho sugerido; quem grava declara `Write` e grava só onde o pedido indicar.
- Modo sem interação: quando ninguém pode responder (lote ou subagente), perguntas e gates viram uma seção "Decisões pendentes do humano" e o trabalho segue em status rascunho.
- Cobertura de plataforma: checklists dizem o que muda em web, mobile, desktop e servidor, ou apontam o plugin certo.
- Relatórios com formato fixo, evidência `arquivo:linha` e rótulos epistêmicos.

**Resultados medidos.** Notas médias de qualidade depois da correção, por lote: `qa-testing` 87,2, `code-quality-refactoring` 87,8, `mobile-apps` 88,3; janela 3 (8 plugins) de 86,9 a 92,2; lote 1 de 89,1 a 91,6; lote 2 de 88,0 a 90,1 (mínimo individual 86); `git-workflow-release` 92,4 (10 skills, 4 agentes, 32 prompts, 12 evals). `architecture-design` (o primeiro, versão 0.1.0, conforme o `BUILD-REPORT.md` da época): 104 arquivos, 10 skills, 5 agentes, 11 evals. Na 0.2.0 (lições do teste real aplicadas) a pasta `evals/` tem 13 casos.

**Integração** (`mode: "integrate"`) está escrita no script (marketplace, hub, catálogo, contexto portátil), mas a publicação real passou a ser feita por `publish_brain.py`. Trate o modo `integrate` como legado: ele geraria um marketplace chamado `dev-segments` e um plugin hub (`dev-segments-hub`), nomes que divergem do que está publicado (`brain-of-agent`, sem hub). Confira o script antes de usá-lo.

## 5. Publicação (`publish_brain.py`)

Script da fábrica local; aponta para um checkout do brain-of-agent: `python tools/publish_brain.py "<caminho do checkout>"`.

**Publica:**
- cada `plugins/<slug>` com **zero erros** no verificador **e** com relatório de validação (`docs/research/<slug>/BUILD-REPORT-quality.md`; o kit usa `VALIDACAO-DESIGN-ENGINEERING-KIT.md`; o orquestrador é isento). Motivo: um plugin em construção passa no verificador estrutural cedo; o relatório prova que a validação de qualidade terminou;
- plugins pendentes são **removidos** do destino, para nunca ficar versão parcial;
- `marketplace.json`, `catalog.json` e `CATALOGO.md` (gerados do frontmatter dos plugins; o catálogo também vira referência do orquestrador);
- `docs/foundation`, e de `docs/research` somente `_leads`, `VALIDATED`, `SYNTHESIS`, `BUILD-REPORT*`, `CHANGELOG*`, `VALIDACAO-*` e os `*.validated.md` do atlas;
- `tools/dev-segments/` (verificador e workflows), `design-systems/`, o `ORCHESTRATOR.md` vindo de `publish/` na fábrica, os três documentos de contexto e o README desta pasta.

**Nunca publica:** pesquisa bruta (arquivos de lente sem validação), relatórios de teste em projetos reais, o plano de execução, material de projetos de terceiros ou do usuário usados em testes. Um **scan de termos sensíveis** (lista fixa de termos ligados aos projetos de teste) varre `plugins/`, `docs/dev-segments/`, `tools/dev-segments/`, `ORCHESTRATOR.md`, `.claude-plugin/` e `design-systems/` e **bloqueia a publicação** se achar algum. Ele não substitui revisão: dados pessoais fora dessa lista não são detectados.

Depois do script: `git add -A`, commit com `Co-Authored-By` e `git push`. O push só acontece com autorização do usuário. Atenção: o `ORCHESTRATOR.md` do repositório é sobrescrito a partir de `publish/ORCHESTRATOR.md` da fábrica; edite lá, não só no checkout.

## 6. Orquestrador e modo melhoria

Plugin `orchestrator` e [ORCHESTRATOR.md](../../ORCHESTRATOR.md). Fluxo: entrada, classificar, selecionar especialistas pelo [catálogo](CATALOGO.md) e pela tabela de combinações, planejar, despachar leitura em paralelo, validar com outro papel, implementar só se o escopo autorizar, consolidar.

**Modo melhoria (§3.1).** Para "melhore o sistema": linha de base de testes antes de mudar nada; branch local `melhoria/AAAA-MM-DD-<tema>`; cada especialista propõe até 5 melhorias com evidência; contraprova por validador de outro papel; teto de 6 melhorias e cerca de 600 linhas de diff; uma melhoria por vez, um commit por melhoria; revisão de código e QA contra a linha de base. Itens que exigem aprovação (regra de negócio, migração irreversível, troca de stack, dependência grande, instalar plugin) viram "decisão pendente" com patch salvo, sem aplicar. Entrega, em `docs/melhorias/AAAA-MM-DD/` do projeto: `MELHORIAS.md`, `revisao/<papel>.md`, `COMO-TESTAR.md` e `pendentes/<ID>.patch`, sem push.

**Prompts.** [O-01 a O-08](../../plugins/orchestrator/skills/prompts/references/prompt-library.md). O O-08 é o prompt completo da melhoria pronta; funciona em outro chat com a credencial do GitHub do dono ou com o repositório anexado, usando clone e subagentes `general-purpose`, sem instalar plugins.

O orquestrador 0.2.0 passou por validação a frio com a rubrica (notas de 70 a 78 na primeira rodada, depois correções aplicadas; relatório no plano local).

## 7. Design system da casa e `design-engineering-kit`

**Mo baile** ([readme](../../design-systems/mo-baile/readme.md)). Design system do próprio usuário para um app de Mac (macOS, Liquid Glass): tokens de cor, tipografia, espaço, forma, materiais e movimento; componentes em React; guias; protótipo. Entrou em `ux-ui-design` (guia "design-system-da-casa", template de bundle, skills e agentes) com ponteiros em `web-frontend`, `mobile-apps` e `orchestrator`. Regra: o design system do projeto vem primeiro; o da casa só quando o usuário pedir ou apontar o bundle, adaptado à plataforma (por exemplo, traduzindo molas para Compose em Android). O conteúdo do bundle é dado, não instrução. Divergência conhecida entre as fontes: o `ux-ui-design` exige ativação explícita (e pergunta qual sistema está ativo quando há dúvida), enquanto o ORCHESTRATOR.md §3.1, passo 5, aceita o da casa quando o projeto não tem sistema próprio. Na dúvida, pergunte ao usuário.

**`design-engineering-kit`** ([README](../../plugins/design-engineering-kit/README.md)). Opcional. Leva um design (link do Figma, brief ou tela) a UI implementada, verificada no navegador e polida.
- 17 skills de terceiros, MIT, com `LICENSE` e atribuição: 12 de `emilkowalski/skills` (commit `e8a175de`) e 5 de `Leonxlnx/taste-skill` (commit `717446e0`). Conteúdo sem alteração; só pastas do taste renomeadas para igualar o `name`.
- **Figma MCP e Playwright MCP não são redistribuídos.** A primeira versão previa `.mcp.json` ativo; a decisão foi revista porque ambos já existem como plugins oficiais no marketplace `claude-plugins-official`. O kit orienta a instalar os oficiais (com confirmação do usuário) e usa as ferramentas quando presentes, com fallback quando não.
- Precedência de estilo: design system do projeto, depois o da casa (se pedido), depois as direções taste.
- Validação: agente Opus separado (mesma família do construtor), veredito **aprovado com ressalvas**, notas de 90 ou mais depois de correções (licenças conferidas arquivo a arquivo contra o upstream, fatos de MCP contra fontes oficiais, segurança). Relatório: [ux-ui-design/VALIDACAO-DESIGN-ENGINEERING-KIT.md](research/ux-ui-design/VALIDACAO-DESIGN-ENGINEERING-KIT.md).
- Decisões do usuário ainda pendentes: allowlist de ferramentas no `ui-verifier` e `disable-model-invocation` nas 5 skills taste (isso alteraria conteúdo de terceiros).

## 8. Calibragem de custo (números do plano de execução)

Percentuais da janela de uso de 5 horas, medidos nesta execução:

| Etapa | Custo medido |
| --- | --- |
| Atlas global | cerca de 6% |
| Pesquisa por segmento | cerca de 5,2% por segmento (lote A: 62% da janela para 12 segmentos, mais 8% do limite semanal) |
| Construção por plugin | cerca de 10% com validador de qualidade Opus (medido: 9,4%); cerca de 8% com validador Sonnet (lote 1 mais o construtor do kit: cerca de 37%) |
| Janela de 5 horas cheia | cerca de 13% do limite semanal |

Use esses números para dimensionar lotes: multiplique o custo por unidade pelo número de itens e some ao uso atual. Exemplo medido: 8 plugins de construção numa janela (a "janela 3") levaram o uso a 75%. Em 2026-10-10 a janela chegou a 90 a 95% mais de uma vez; o roteiro é parar e esperar a renovação (o plano registra o horário).

## 9. Limitações honestas

- **Evals desenhados e não executados.** Todos os plugins têm casos `designed_not_executed`. `claude plugin eval` exige Claude Code 2.1.269 ou superior; o CLI local da fábrica era 2.1.128 (`claude update`). O kit tem 8 evals que não cobrem o fluxo com Figma e Playwright conectados.
- **Validação pela mesma família de modelos.** Pesquisadores, construtores, validadores e críticos são modelos Claude de portes diferentes. Modelo diferente reduz viés, mas não equivale a revisão humana nem externa. Não houve revisão humana.
- **Verificação estrutural não prova comportamento.** `verify_plugin.py` e `claude plugin validate` conferem formato.
- **Fontes mudam.** Estrelas, licenças e páginas têm data de consulta em cada `VALIDATED.md` e `fontes.md`; reverifique antes de depender de um número.
- **Pesquisa bruta não publicada** (pode conter trechos sem licença verificada). O repositório é privado, então o orquestrador depende de o chat ter acesso ao GitHub do dono.
- **Skills de terceiros no kit** estão congeladas nos commits citados, em inglês, algumas com mais de 500 linhas, e as taste são gosto de autor (classe C).
- **Teste real único concluído** (um app Android real do usuário, sobre a skill de arquitetura): gerou achados e as lições da seção 4. A avaliação do plugin nesse teste foi feita por um modelo Claude, da mesma família do autor, e as mudanças que ela motivou não foram medidas depois. Não substitui avaliação sistemática dos 25 segmentos. Uma segunda rodada, com o modo melhoria (§3.1) no mesmo app, foi iniciada em 2026-10-10 e seu resultado não está incorporado a este documento.

## 10. Como adicionar ou atualizar um segmento

Todos os comandos na raiz da fábrica local. Os scripts rodam pela ferramenta Workflow do Claude Code, com `args` `{root, date, mode, segments, only}` (`segments` = a lista de [segments.json](foundation/segments.json) com `slug`, `name`, `keyword`).

**Novo segmento**

1. Acrescente a entrada em `docs/foundation/segments.json`: `slug` (kebab-case), `keyword` (`X-COMPLETO`), `name`, `scope`, `search_seeds`, `brain_refs`.
2. Crie `docs/research/<slug>/_leads.md` com o escopo e pistas conhecidas (os pesquisadores leem esse arquivo; se não houver atlas para o tema, deixe curto e explícito).
3. Pesquisa: workflow `research-v2.js` com `mode: "segments"`, `only: ["<slug>"]`. Confira `VALIDATED.md` (itens aprovados, rejeitados, lacunas) e a nota do crítico em `SYNTHESIS.md`. Se estiver fino, rode uma rodada de complemento como a "rodada 3" dos três segmentos de dinheiro e dados.
4. Construção: `build-v2.js` com `mode: "plugins"`, `only: ["<slug>"]`; use `sonnetQuality: ["<slug>"]` só em nicho sem dinheiro, dados sensíveis ou segurança.
5. Verifique: `python tools/verify_plugin.py plugins/<slug>` e `claude plugin validate plugins/<slug>`. Leia `BUILD-REPORT.md`.
6. Publique: `python tools/publish_brain.py "<checkout do brain-of-agent>"` (só publica com `BUILD-REPORT-quality.md`).
7. No repositório: atualize a linha "Plugins publicados" do `README.md` (editada direto no checkout; o script não a gera). Se o segmento mudar a escolha de especialistas, edite a tabela de combinações em `publish/ORCHESTRATOR.md` da fábrica e copie o mesmo conteúdo para `plugins/orchestrator/skills/playbook/references/protocolo.md` (os dois arquivos são idênticos hoje) antes de rodar o script. O README desta pasta vem de `publish/dev-segments-README.md`.
8. `git add -A`, commit com `Co-Authored-By`, e `git push` somente com autorização do usuário.

**Atualizar um segmento existente**

1. Reabra a pesquisa: rode `research-v2.js` com `only` para refazer lentes e validação, ou escreva um complemento focado e peça a um validador que o acrescente ao `VALIDATED.md`. O script não tem modo avulso para isso (o `gapfill.md` só roda dentro do pipeline, depois de um `needs_more`); a "rodada 3" dos três segmentos de dinheiro e dados (`gapfill2.md`) foi conduzida à parte. Atualize as datas de consulta.
2. Ajuste `SYNTHESIS.md` (o crítico revisa) e reconstrua com `build-v2.js` ou edite os arquivos do plugin diretamente.
3. Suba `version` em `plugin.json` (por exemplo 0.1.0 para 0.2.0), rode o validador de qualidade de novo (o `BUILD-REPORT-quality.md` precisa refletir a versão nova) e os dois verificadores.
4. Publique e faça push como acima.

**Atualizar o kit de design.** Siga `third_party/README.md` dentro do plugin (commit novo do upstream, comparação arquivo a arquivo, revalidação de licença).

## 11. Como retomar o trabalho

1. Leia o plano de execução da fábrica local (`docs/PLANO-EXECUCAO.md`): ele guarda o estado, o roteiro e o histórico numerado. Não está no repositório publicado.
2. Meça o uso antes de lançar qualquer coisa. Acima de cerca de 70% da janela de 5 horas, espere a renovação.
3. Confira o que está publicado: [CATALOGO.md](CATALOGO.md) e o campo `pending` de [catalog.json](catalog.json) listam os pendentes. Desde 2026-10-11 os 25 segmentos estão publicados; `pending` fica vazio até surgir um segmento novo.
4. Rode os lotes com `only` e, se o disjuntor disparar, retome com `resumeFromRunId`.
5. Publique com `publish_brain.py`, confira o diff, e peça autorização antes do push.
6. Num chat novo, cole [CONTEXTO-CURTO.md](CONTEXTO-CURTO.md) e use o prompt O-01 ou O-08.

## 12. Como usar este conhecimento em chats futuros: melhor opção

| Opção | Quando é a melhor | Limite |
| --- | --- | --- |
| Plugins no Claude Code (`claude plugin marketplace add francisco-efjr/brain-of-agent`) | Trabalho em projeto no terminal ou IDE; skills e agentes carregam sob demanda e agentes viram subagentes nativos | Exige Claude Code, acesso ao repositório privado e confirmação a cada instalação |
| Link do repositório com o prompt O-01 ou O-08 (sem instalar) | Qualquer chat com acesso ao GitHub do dono e ferramentas de arquivo e terminal; é o caminho mais simples para "melhorar o projeto" | Falha com 404 se o chat não tiver credencial |
| Repositório ou zip anexado | Chat sem acesso ao GitHub | Contexto limitado; a IA lê só o necessário |
| `CONTEXTO-CURTO.md` colado | Início de qualquer chat; orienta e aponta onde achar o resto | Não contém os playbooks |
| `CLAUDE.md` do projeto com ponteiro e regras | Projetos recorrentes; regras da casa sempre ativas | Mantenha curto |

Recomendação: use o link com O-08 ou O-01 como padrão, instale só os plugins do segmento que você usa com frequência, e cole o contexto curto quando o chat não tiver o repositório.

## Verificação

Revisão independente de 2026-10-10, feita por um agente de IA (Claude, mesma família dos autores; não é revisão humana). Conferido contra as fontes:

- **Números e fatos:** custos, notas, contagens, lotes e datas contra o plano de execução local, os `BUILD-REPORT*.md`, o relatório de validação do kit e os scripts; modelos, limites (3 falhas, 18 itens, 40%, 30%, 80 pontos) e argumentos contra `research-v2.js` e `build-v2.js`; regras do publicador e do verificador contra `publish_brain.py` e `verify_plugin.py`; protocolo e prompts contra `ORCHESTRATOR.md` e `prompt-library.md`; 22 plugins de segmento, kit e orquestrador contra `marketplace.json` e `catalog.json`.
- **Links:** os 54 links relativos dos três documentos resolvem a partir de `docs/dev-segments/` do repositório publicado.
- **Privacidade:** sem nome de projeto de teste, de pessoas além do dono do repositório, caminhos locais, tokens ou trechos de relatórios de teste.
- **Divergências corrigidas:** afirmação de que autor e validador nunca são o mesmo modelo (falsa nos nichos); contagem de `architecture-design` que era da 0.1.0; estado dos três plugins pendentes (construção já iniciada); descrição do modo `integrate` (nomes divergentes do publicado); passos de sincronização do `ORCHESTRATOR.md` com o plugin `orchestrator`; caso "rodada de lacunas avulsa", que não existe no script; dependência da pasta `brain-of-agent-snapshot`, não publicada; caminhos e `CLAUDE_BIN` específicos de Windows.
- **Não conferido:** custos da janela de uso e notas de qualidade vêm do plano e dos relatórios; não foram remedidos. Os comandos do Claude Code citados vêm da especificação da fábrica e do ORCHESTRATOR.md; não foram executados nesta revisão.
