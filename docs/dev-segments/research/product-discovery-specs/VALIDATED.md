# Produto, descoberta e especificação — VALIDADO (consolidado das 3 lentes)

Data: 2026-10-10 · Validador: claude-sonnet-5-5 (independente; os pesquisadores eram claude-haiku-5-5, outro modelo) · Segmento: `product-discovery-specs`

Rótulos: Verificado (lido por ferramenta nesta validação) · Inferido · Suposição · Não verificável. Resumos de WebFetch passam por um modelo intermediário: afirmações numéricas e de existência foram cruzadas, mas o texto de terceiros não foi copiado. Nenhum conteúdo lido continha instrução dirigida a agente. Todo "conteúdo reutilizável" abaixo é destilação com redação própria (sem trecho literal); só há licença permissiva comprovada nos itens indicados, e mesmo nesses o plugin deve reescrever.

## Estatísticas

| Lente | Recebidos | Aprovados (V-) | Rebaixados a C / não aprovados | Rejeitados | Registro de lacuna |
| --- | --- | --- | --- | --- | --- |
| authoritative | 29 | 28 | 1 (R-authoritative-28, substituído por V-43) | 0 | 0 |
| github | 22 | 17 | 5 (15, 16, 18, 19, 20) | 0 | 0 |
| community | 26 | 17 | 6 (03, 04, 05 mantidos como sinal C; 07, 13, 24 rebaixados) | 2 (17, 23) | 1 (26, Reddit) |
| **Total** | **77** | **62** | **12** | **2** | **1** |

- Itens aprovados únicos após deduplicação entre lentes: **45** (V-01 a V-45). Os 62 aprovados das lentes colapsam nesses 45; 3 itens (V-43, V-44, V-45) foram acrescentados pelo validador para cobrir OKR, sprint planning e roadmap.
- URLs/arquivos re-verificados: **79 URLs + 1 arquivo local** (≈ 95% dos itens; mínimo exigido 40%). Todos os itens classe A e todos os candidatos a virar prompt/skill/regra foram reabertos.
- Estrelas, licença e último push vêm da API de busca do GitHub (`api.github.com/search/repositories`), pois `/repos/<owner>/<repo>` retorna 403 (WebFetch) ou rate limit (curl sem token).
- Prompt-score médio dos 22 itens tipo prompt/skill/agente/comando/regra: **80,0 após reescrita** (média das fontes originais ≈ 72,7). Nenhum atingiu critério de reprovação automática; 3 fontes tinham nota abaixo de 70 antes da reescrita (V-12, V-13, V-37) por tom rígido, tools excessivas ou `curl | bash`.
- Itens que dependem de versão do Claude Code (`/goal`, hook Stop, `/verify`, `claude -p`, plan mode): conferir na instalação do usuário.

Armadilhas descobertas nas lentes (já corrigidas abaixo): nome do arquivo de features do harness; "pelo menos 3 perguntas" no prd do awesome-copilot (é 2); `Background` "só Given" no Cucumber (a página não restringe); implementation-plan.agent com tools de execução e sem campo formal de critério por fase; estudo de expertise da Anthropic sem prescrição de pedido; OKR oficial do Google existe em outra URL; Dwyer recomenda `--dangerously-skip-permissions`.

---

## Itens aprovados

### V-01 — Entrevista guiada pelo Claude antes da spec (SPEC.md, sessão nova) — Classe A (9) · Prompt-score 82 (fonte 70)
- **Lente:** authoritative + github + community (origens R-authoritative-01, R-github-12, R-community-06)
- **Tipo:** prompt | workflow
- **Fonte:** https://code.claude.com/docs/en/best-practices (seção "Let Claude interview you") · **Autor/Org:** Anthropic
- **Sinais:** documentação oficial; sem data de atualização visível na página. Licença do texto: não verificada, destilar.
- **Para que serve:** levantar requisitos, UX, bordas e trade-offs de feature grande antes de qualquer código; gerar spec autocontida; executar em sessão limpa.
- **Técnicas-chave:** prompt mínimo + ferramenta `AskUserQuestion`; não perguntar o óbvio; continuar até cobrir; escrever SPEC.md; abrir sessão nova para executar; spec boa nomeia arquivos/interfaces, declara fora de escopo e termina com verificação ponta a ponta.
- **Conteúdo reutilizável (reescrito, D1–D12 = 4/4/4/4/3/4/4/4/5/5/4/4):**
  > Quero construir [descrição]. Antes de escrever qualquer coisa, me entreviste com a ferramenta de perguntas, em rodadas curtas. Cubra problema e usuário, comportamento esperado, UX, bordas e falhas, restrições, trade-offs e o que fica fora do escopo. Não pergunte o que dá para descobrir lendo o código; aprofunde o que eu provavelmente não considerei e repita em poucas linhas o que entendeu antes de seguir. Quando eu disser que acabou, escreva SPEC.md com objetivo, fora de escopo, arquivos e interfaces envolvidos, critérios de aceite verificáveis (cada um com o comando, teste ou evidência que o prova) e perguntas em aberto marcadas `[NEEDS CLARIFICATION]`. Não implemente. Se eu não souber responder ou faltar acesso, registre a lacuna em vez de supor.
- **Ressalvas:** a doc descreve prática, não mede ganho. Para tarefas cujo diff cabe em uma frase, a entrevista é sobrecarga (ver V-02).
- **Verificação:** página aberta; confirmados o prompt de entrevista, o uso de `AskUserQuestion`, "sessão nova" e a frase sobre specs autocontidas. Relatos secundários (Analytics Vidhya, Substack) não usados.

### V-02 — Explorar, planejar, implementar, commitar + gatilho de plano + verificação executável — Classe A (9) · Prompt-score 80 (fonte 74)
- **Lente:** authoritative (R-authoritative-02, R-authoritative-03; reforçado por R-github-12 e R-community-06)
- **Tipo:** workflow | checklist
- **Fonte:** https://code.claude.com/docs/en/best-practices (seções "Explore first, then plan, then code" e "Give Claude a way to verify its work") · **Autor/Org:** Anthropic
- **Sinais:** doc oficial. Opções `/goal`, hook `Stop`, `/verify` e plan mode (Shift+Tab, `--permission-mode plan`) existem na página lida hoje; dependem da versão instalada.
- **Para que serve:** evitar resolver o problema errado e declarar "pronto" sem prova.
- **Técnicas-chave:** quatro fases (explorar em modo somente leitura, planejar editável via Ctrl+G, implementar contra o plano, commitar); planejar quando a abordagem é incerta, mexe em vários arquivos ou o código é desconhecido; pular o plano se o diff cabe em uma frase; todo requisito tem um check que devolve passa/falha; exigir evidência (saída do comando, screenshot), não afirmação; graus de rigor: no prompt, `/goal`, hook `Stop`, subagente de verificação.
- **Conteúdo reutilizável (reescrito, 4/4/4/4/3/4/4/4/4/5/4/4):** checklist "Antes de codar": (1) o diff cabe numa frase? então faça direto; (2) senão, explore sem editar, produza plano com arquivos, fluxo e riscos e espere aprovação; (3) cada requisito lista o check que o prova (comando, teste, comparação de screenshot); (4) ao terminar, mostre a saída real dos checks e diga o que não foi verificado; (5) se o check falhar duas vezes, pare, resuma o que tentou e peça direção.
- **Ressalvas:** plano acrescenta sobrecarga; o gatilho deve ser configurável. A doc não traz métrica de ganho.
- **Verificação:** página aberta e seções conferidas; o exemplo "validateEmail" com casos concretos confirma "incluir casos de teste no pedido".

### V-03 — Revisão adversarial em subagente de contexto novo — Classe A (9) · Prompt-score 83 (fonte 76)
- **Lente:** github (R-github-12) + verificação adicional na própria doc (seção "Add an adversarial review step")
- **Tipo:** prompt | pattern
- **Fonte:** https://code.claude.com/docs/en/best-practices · **Autor/Org:** Anthropic
- **Sinais:** doc oficial; Verificado que o texto inclui a ressalva de que revisor "caça-defeito" acha achados mesmo com trabalho correto.
- **Para que serve:** revisar um diff contra a spec/plano sem viés de quem escreveu.
- **Conteúdo reutilizável (reescrito, 4/4/5/4/3/5/4/4/4/5/4/4):**
  > Use um subagente em contexto novo para revisar o diff contra SPEC.md. Verifique: (a) cada requisito está implementado, com o check correspondente executado; (b) cada borda listada tem teste; (c) nada fora do escopo mudou. Reporte só lacunas que afetam correção ou os requisitos declarados, cada uma com arquivo:linha e o requisito violado. Não reporte preferências de estilo. Se não houver lacunas, diga isso e liste os checks que rodou.
- **Ressalvas:** sem o limite de "só correção e requisitos" o revisor gera sobre-engenharia (a própria doc avisa).
- **Verificação:** trecho e callout lidos na página oficial.

### V-04 — Boas práticas de autoria de skills — Classe A (9)
- **Lente:** authoritative (R-authoritative-04)
- **Tipo:** checklist | reference
- **Fonte:** https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices · **Autor/Org:** Anthropic
- **Sinais:** doc oficial. Verificado: `name` ≤ 64 caracteres, minúsculas/números/hífens, sem tags XML e **sem as palavras reservadas "anthropic" e "claude"** (acréscimo; a lente não citou); `description` não vazia, ≤ 1024 caracteres, sem XML, terceira pessoa, com o quê e quando; corpo do SKILL.md < 500 linhas; referências em um nível; TOC em arquivos > 100 linhas; "pelo menos três avaliações"; testar com Haiku, Sonnet e Opus; barras normais; evitar dar muitas opções sem padrão; evitar informação com data.
- **Para que serve:** checklist de publicação das skills do plugin.
- **Conteúdo reutilizável:** converter a "Checklist for effective Skills" da página em checklist do plugin (qualidade central, código/scripts, teste), mais as regras de nome.
- **Ressalvas:** campos de frontmatter de comando e agente de plugin diferem; conferir a doc de plugins. A página sugere gerúndio para nomes (`writing-specs`), alternativas aceitas.
- **Verificação:** página inteira lida.

### V-05 — Ciclo de criação e avaliação de skill (skill-creator) — Classe A (9) · Prompt-score 85
- **Lente:** authoritative + github (R-authoritative-05, R-github-08)
- **Tipo:** skill | workflow
- **Fonte:** https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md · licença do arquivo: https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/LICENSE.txt · **Autor/Org:** Anthropic
- **Sinais:** repositório `anthropics/skills` ≈ 180,2 mil ★, push 2026-10-09 (search API); licença no nível do repositório "null", mas `LICENSE.txt` da pasta skill-creator é **Apache-2.0, "Copyright 2026 Anthropic, PBC"** (Verificado). A lente github não encontrou a licença: corrigido.
- **Para que serve:** criar e testar skills do plugin; otimizar a `description`.
- **Técnicas-chave:** capturar intenção e entrevistar sobre bordas; rascunho; `evals/evals.json`; rodar cada teste com e sem skill; avaliar; iterar; otimização da description com ≈ 20 consultas (8–10 devem disparar, 8–10 não), priorizando negativos quase-casos, divisão ≈ 60% treino/40% teste; corpo < 500 linhas; explicar o porquê em vez de ALWAYS/NEVER.
- **Conteúdo reutilizável (destilado, 5/4/5/4/4/4/5/3/4/4/4/5):** roteiro de seis etapas (intenção, entrevista, rascunho, teste comparativo, avaliação, iteração) + modelo de lista de gatilhos positivos/negativos.
- **Ressalvas:** executa scripts Python locais e `claude -p` via subprocesso; o plugin não deve embutir isso sem revisão. Skills subjetivas precisam de revisão humana.
- **Verificação:** SKILL.md e LICENSE.txt abertos; ausência de comando que baixe código externo confirmada.

### V-06 — Harness de longa duração: lista de features com `passes` — Classe A (8) · Prompt-score 78 (fonte 70)
- **Lente:** authoritative + github (R-authoritative-06, R-github-13)
- **Tipo:** pattern | template
- **Fonte:** https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents · **Autor/Org:** Anthropic Engineering · publicado em 2025-11-26 (Verificado)
- **Sinais:** o post usa os dois nomes de arquivo (`tests.json` no transcript e `feature_list.json` no texto); **o nome `features.json` da lente github não aparece**. Arquivo de progresso `claude-progress.txt`, script `init.sh`, teste ponta a ponta via Puppeteer MCP.
- **Para que serve:** manter os critérios de uma spec grande entre sessões, uma feature por vez.
- **Conteúdo reutilizável (reescrito, 4/4/4/4/3/5/4/4/4/4/4/3):** item `{category, description, steps[], passes:false}`; regra: o agente só altera `passes`, e só depois de rodar os steps; remover ou editar itens é proibido (a razão: perder funcionalidade). Início de sessão: confirmar diretório, ler log de progresso e `git log`, escolher o item pendente de maior prioridade, subir o ambiente, rodar um teste ponta a ponta básico antes de construir. Nome do arquivo livre; documentar a escolha.
- **Ressalvas:** exemplo é um clone de chat; sem métrica. A rotina executa comandos: usar em sandbox.
- **Verificação:** post aberto, campos, regra do `passes`, rotina e datas conferidos.

### V-07 — Contrato de delegação para subagentes — Classe A (8) · Prompt-score 80 (fonte 72)
- **Lente:** authoritative + github (R-authoritative-07, R-github-14)
- **Tipo:** pattern | prompt-template
- **Fonte:** https://www.anthropic.com/engineering/multi-agent-research-system · **Autor/Org:** Anthropic Engineering · publicado em 2025-06-13 (Verificado)
- **Sinais:** confirmados: subagente recebe objetivo, formato de saída, orientação de ferramentas/fontes e fronteiras; escala de esforço (1 agente com 3–10 chamadas; 2–4 subagentes com 10–15 chamadas cada; "mais de 10" para pesquisa complexa); ≈ 4× tokens de chat para agentes e ≈ 15× para multiagente; rubrica de LLM-judge (acurácia factual, de citação, completude, qualidade de fonte, eficiência de ferramenta) numa chamada, nota 0–1; começar com ≈ 20 consultas.
- **Conteúdo reutilizável (reescrito, 4/4/4/4/4/5/3/4/4/4/4/4):** briefing com cinco campos: Objetivo, Formato de saída, Ferramentas e fontes, Fronteiras (o que não fazer e o que outro agente cobre), Critério de pronto e como relatar o que não encontrou.
- **Ressalvas:** custo de tokens alto; só para tarefas de alto valor; exemplo é de pesquisa web.
- **Verificação:** post aberto e números conferidos.

### V-08 — Estudo de expertise em Claude Code (referência de princípio) — Classe B (6)
- **Lente:** authoritative (R-authoritative-08); community R-community-07 rebaixado (ver tabela)
- **Tipo:** reference
- **Fonte:** https://www.anthropic.com/research/claude-code-expertise · **Autor/Org:** Anthropic · publicado em 2026-06-16 (Verificado)
- **Sinais:** ≈ 400 mil sessões de ≈ 235 mil pessoas, out/2025–abr/2026; pessoas decidem ≈ 70% do planejamento e o Claude ≈ 80% da execução; fração de sessões gastas consertando código quebrado caiu de 33% para 19%; 19% das sessões de novatos terminam abandonadas contra 5–7% dos demais.
- **Para que serve:** justificar que o plugin force a definição do problema, do "pronto" e da verificação antes da execução.
- **Conteúdo reutilizável (destilado):** princípio "a parte humana é o que construir, o que é pronto e como validar; o plugin coleta essas três respostas antes de executar".
- **Ressalvas:** descritivo e correlacional. **O artigo não prescreve escopo/verificação/definição de pronto em todo pedido, não afirma que especialistas pedem mais verificação e não trata de "o que não deve mudar"**; não usar como fonte de boas práticas de escrita de pedido nem atribuí-lo.
- **Verificação:** artigo aberto; números e ausência de recomendação prescritiva conferidos.

### V-09 — Template de especificação do spec-kit — Classe A (8) · Prompt-score 83
- **Lente:** authoritative + github + community (R-authoritative-09, R-github-01, R-community-01)
- **Tipo:** template
- **Fonte:** https://raw.githubusercontent.com/github/spec-kit/main/templates/spec-template.md · repo https://github.com/github/spec-kit · **Autor/Org:** GitHub, Inc.
- **Sinais:** ≈ 140,6 mil ★, push 2026-10-10, licença **MIT, "Copyright GitHub, Inc."** (search API + LICENSE lido). Citação "97 mil" do agregador e "72 mil" de blog são desatualizadas.
- **Estrutura (Verificado):** cabeçalho (título, branch, data, status Draft, entrada); Cenários de usuário e testes (obrigatório): histórias P1, P2, P3 com "por que esta prioridade", "teste independente" e aceite Given/When/Then; Casos de borda (em forma de pergunta); Requisitos (obrigatório): `FR-001…` ("o sistema DEVE…"), marcador `[NEEDS CLARIFICATION: …]`, entidades-chave; Critérios de sucesso (`SC-001…`, mensuráveis e sem tecnologia); Premissas. Comentários HTML são orientação ao redator, não comandos.
- **Conteúdo reutilizável (esqueleto próprio, 4/4/5/5/3/5/4/4/4/4/4/4):** seções acima; regras: cada história é um MVP útil sozinha; nenhum nome de tecnologia em FR/SC; toda lacuna vira `[NEEDS CLARIFICATION]` e é listada ao fim.
- **Ressalvas:** só o template de placeholders foi lido; varia entre versões. Fluxo completo do spec-kit é pesado para mudanças pequenas (V-39).
- **Verificação:** template e LICENSE lidos; página do repositório confirma MIT e ≈ 140,6 mil ★; instalação documentada via `uv tool install specify-cli` (sem `curl | bash`).

### V-10 — Template de tarefas do spec-kit — Classe A (8) · Prompt-score 80
- **Lente:** github + community (R-github-02, R-community-01)
- **Tipo:** template | checklist
- **Fonte:** https://raw.githubusercontent.com/github/spec-kit/main/templates/tasks-template.md · **Autor/Org:** GitHub · MIT (ver V-09)
- **Sinais/estrutura (Verificado):** formato `[ID] [P?] [Story] Descrição` com `T001…`; `[P]` = paralelizável (arquivo diferente, sem dependência); `[US1]…` liga a história; fases: Setup, Fundação (bloqueia as histórias), uma fase por história em ordem de prioridade, Polish; testes são opcionais (só se a spec pedir) e, se existirem, vêm primeiro e devem falhar antes; checkpoint independente por história; o HTML manda substituir as tarefas de exemplo.
- **Conteúdo reutilizável (destilado, 4/3/5/5/3/5/4/3/4/4/4/4):** regras de quebra: caminho de arquivo exato em cada tarefa, ordem setup, fundação, histórias, polish; um checkpoint testável por história; nunca deixar tarefa de exemplo.
- **Ressalvas:** o placeholder `__SPECKIT_COMMAND_TASKS__` é do gerador do spec-kit; não copiar.
- **Verificação:** arquivo lido.

### V-11 — Spec-driven development: fases e gates (post oficial do GitHub) — Classe B (7)
- **Lente:** authoritative (R-authoritative-10)
- **Tipo:** workflow
- **Fonte:** https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/ · **Autor/Org:** Den Delimarsky, GitHub · 2025-09-02 (Verificado)
- **Sinais:** quatro fases (Specify, Plan, Tasks, Implement); não avançar sem validar a tarefa atual; "constitution" **não** aparece no post (confirmado).
- **Conteúdo reutilizável (destilado):** gate por fase com três perguntas: há lacunas? faltam bordas? algo desalinha da spec?
- **Ressalvas:** texto de divulgação de produto; classe B pela natureza promocional (autoridade 2).
- **Verificação:** post aberto; autor, data e fases conferidos.

### V-12 — Workflow de spec com gate de confiança (awesome-copilot) — Classe B (6) · Prompt-score 78 (fonte 62)
- **Lente:** authoritative + github (R-authoritative-11, R-github-04)
- **Tipo:** workflow | instruction
- **Fonte:** https://raw.githubusercontent.com/github/awesome-copilot/main/instructions/spec-driven-workflow-v1.instructions.md · **Autor/Org:** GitHub
- **Sinais:** repo `github/awesome-copilot` ≈ 39,9 mil ★, MIT, push 2026-10-09 (search API); o arquivo não traz licença própria (frontmatter só `description` e `applyTo`). Confirmados seis fases (ANALYZE, DESIGN, IMPLEMENT, VALIDATE, REFLECT, HANDOFF), seis padrões EARS (a fase ANALYZE usa só o orientado a evento) e as faixas > 85%, 66–85%, < 66%.
- **Conteúdo reutilizável (reescrito, 4/4/4/4/3/5/4/3/3/4/4/5):** tabela do gate de confiança (> 85% plano completo; 66–85% prova de conceito/MVP com critério de sucesso antes de expandir; < 66% pesquisa e nova análise, escalar ao humano se persistir) rotulada **Suposição de calibração**, sem evidência citada, e configurável; Decision Record (decisão, contexto, opções, justificativa, impacto, data de revisão).
- **Ressalvas:** "Never skip any step" e "never proceed with unresolved errors" são rígidos; o protocolo de escalonamento citado não é definido; passos automáticos (criar issues, arquivar, análise dinâmica em staging) exigem confirmação do usuário no plugin; não exige aprovação humana antes de construir.
- **Verificação:** arquivo lido; limiares e ausência de licença conferidos.

### V-13 — Agente de plano de implementação com IDs rastreáveis — Classe B (5) · Prompt-score 78 (fonte 58)
- **Lente:** authoritative + github (R-authoritative-12, R-github-05)
- **Tipo:** subagent | template
- **Fonte:** https://raw.githubusercontent.com/github/awesome-copilot/main/agents/implementation-plan.agent.md · **Autor/Org:** GitHub (awesome-copilot, MIT no repo)
- **Sinais/correções (Verificado):** oito seções (Requisitos e restrições, Passos, Alternativas, Dependências, Arquivos, Testes, Riscos e premissas, Especificações relacionadas); prefixos `REQ-`, `SEC-`, `CON-`, `GUD-`, `PAT-`, `TASK-`, `GOAL-`, `ALT-`, `DEP-`, `FILE-`, `TEST-`, `RISK-`, `ASSUMPTION-`. **A fonte diz "não edite código" mas concede `editFiles`, `runInTerminal`, `runCommand` e `runTask`; não há campo formal de critério de conclusão por fase** (a lente afirmava o contrário; parte da leitura é de modelo intermediário, tratar como Inferido).
- **Conteúdo reutilizável (reescrito, 4/3/4/5/3/5/4/4/4/4/4/3):** esqueleto de plano com as oito seções, IDs (`REQ`, `TASK`, `RISK`, `ASSUMPTION`, `ALT`, `TEST`) e **campo "Critério de conclusão" por fase, mensurável e verificável por comando**; tools do nosso subagente: leitura (Read, Grep, Glob) e escrita só em `plans/`; "nenhuma tarefa exige decisão humana nem deixa placeholder".
- **Ressalvas:** classe rebaixada de 6 para 5 pela inconsistência de tools; preferir V-30 como modelo de subagente somente leitura.
- **Verificação:** arquivo lido.

### V-14 — Gerador de ADR com parada por falta de dados — Classe B (6) · Prompt-score 78 (fonte 74)
- **Lente:** github (R-github-06)
- **Tipo:** subagent
- **Fonte:** https://raw.githubusercontent.com/github/awesome-copilot/main/agents/adr-generator.agent.md · **Autor/Org:** GitHub (MIT no repo)
- **Sinais (Verificado):** exige título, contexto, decisão, alternativas e stakeholders antes de gerar (se faltar, pede); status Proposed/Accepted/Rejected/Superseded/Deprecated (padrão Proposed); IDs `POS-`, `NEG-`, `ALT-`, `IMP-`, `REF-`; 3–5 consequências positivas e negativas (o checklist final só exige uma de cada); arquivo `adr-NNNN-slug.md` em `/docs/adr/`.
- **Conteúdo reutilizável (reescrito, 4/3/4/4/3/4/4/5/4/4/5/3):** regra de parada por dado ausente + checklist final (numeração sequencial, slug de 3–5 palavras, campos obrigatórios, data ISO). Para decisão de produto, trocar "consequências" por impacto no usuário e nas métricas.
- **Ressalvas:** orientado a arquitetura; ajustar para decisões de produto.
- **Verificação:** arquivo lido.

### V-15 — Brainstorming antes de construir: uma pergunta por vez, play back e gate — Classe A (8) · Prompt-score 85 (fonte 72)
- **Lente:** authoritative + github + community (R-authoritative-13, R-github-03, R-community-25)
- **Tipo:** skill | prompt
- **Fonte:** https://raw.githubusercontent.com/obra/superpowers/main/skills/brainstorming/SKILL.md · **Autor/Org:** Jesse Vincent (obra)
- **Sinais:** `obra/superpowers` ≈ 296,9 mil ★, MIT "Copyright (c) 2025 Jesse Vincent", push 2026-10-10 (search API + LICENSE lidos). O arquivo usa tom forte (`MUST` na description, tag `<HARD-GATE>`).
- **Técnicas-chave (Verificado):** checar o que já se sabe; uma pergunta por mensagem, abertas primeiro; play back de ≈ 200–300 palavras com palpites marcados; dimensionar o trabalho; design escrito com metas, não-metas, anti-metas e restrições; revisão por subagente que separa dúvidas respondidas, menores (decididas pelo agente e marcadas) e "dele" (só o humano responde); gate: nada é construído antes de aprovação, com exceção de opt-out e spike descartável. **A contagem de passos ("12" ou "16") não se sustenta; a skill tem seções, não checklist numerado.**
- **Conteúdo reutilizável (reescrito, 5/5/4/4/3/4/4/5/4/4/5/4):**
  1. Se o pedido já está completo, execute e relate; se falta algo importante, converse.
  2. Faça uma pergunta por mensagem, aberta primeiro; use opções só quando a pessoa travar.
  3. A cada bloco entendido, devolva 200–300 palavras do que entendeu e marque palpites como palpites.
  4. Classifique o tamanho (tarefa rápida, mudança pequena, projeto com documento de design).
  5. Escreva o design com objetivo, metas, não-metas, restrições, decisões e itens abertos.
  6. Revise o design com um subagente de contexto novo e separe dúvidas em respondidas, menores (você decide e marca) e do humano.
  7. Não construa (código, estrutura, dependências) antes de aprovação explícita do texto completo; ler e explorar é permitido. Gate configurável, padrão ativo. Concordância vaga não é aprovação.
- **Ressalvas:** nomes de skills citadas (`writing-plans`) precisam de mapeamento; gate conflita com modo autônomo, por isso configurável.
- **Verificação:** SKILL.md e LICENSE lidos; ausência de links e comandos suspeitos.

### V-16 — Referência de Gherkin (Cucumber) — Classe A (8)
- **Lente:** authoritative + community (R-authoritative-14, R-community-15)
- **Tipo:** reference
- **Fonte:** https://cucumber.io/docs/gherkin/reference/ · **Autor/Org:** Cucumber Open Source Project; sem licença de reuso declarada, destilar
- **Verificado:** um `Feature` por arquivo; `Rule` desde Gherkin 6; um `Background` por Feature ou Rule; `Scenario` = `Example`; `Scenario Outline` exige `Examples`; Given = estado conhecido, When = ação ou evento, Then = resultado em saída observável (não verificar o banco direto); `And`/`But` e `*` substituem palavras-chave. **Correção:** a página dá "mais de 4 linhas" como sugestão para o Background e **não restringe Background a Given** (a lente afirmava).
- **Conteúdo reutilizável (destilado):** tabela de papel das palavras-chave e regra de uso (regra de negócio, `Rule`; dados variados, `Scenario Outline`; contexto comum curto, `Background`).
- **Ressalvas:** a página não cobre anti-padrões nem nomeação; independência entre cenários não é afirmada.
- **Verificação:** página aberta e cada afirmação cruzada.

### V-17 — Gherkin declarativo: checklist de revisão de cenário — Classe A (8) · Prompt-score n/a (checklist)
- **Lente:** authoritative (R-authoritative-15)
- **Tipo:** checklist
- **Fonte:** https://cucumber.io/docs/bdd/better-gherkin/ · **Autor/Org:** Cucumber
- **Verificado:** descrever comportamento, não implementação; teste "se a implementação mudar, o texto precisa mudar?"; evitar verbos de UI como clicar; o exemplo declarativo é mais curto. **Correção:** a página não diz que dados concretos ficam fora do cenário de forma consistente (o próprio exemplo cita usuários nomeados); não afirma regra de tamanho de passo.
- **Conteúdo reutilizável (destilado):** cinco perguntas de revisão: descreve o quê e não o como? sobrevive a uma mudança de implementação? sem verbos de interação? um comportamento por cenário? o Then é observável?
- **Verificação:** página aberta.

### V-18 — INVEST como checklist e skill de histórias — Classe A (8)
- **Lente:** authoritative + community (R-authoritative-16, R-community-10)
- **Tipo:** checklist | skill
- **Fonte:** https://agilealliance.org/glossary/invest · alternativa de implementação MIT: https://raw.githubusercontent.com/phuryn/pm-skills/main/pm-execution/skills/user-stories/SKILL.md · **Autor/Org:** Agile Alliance (origem Bill Wake 2003 e Mike Cohn 2004); phuryn/pm-skills (≈ 26,9 mil ★, MIT, push 2026-10-09)
- **Verificado:** seis critérios; **as perguntas de teste não estão na página** (foram escritas pelos pesquisadores/validador, rótulo Inferido); a página não tem data de atualização. A skill `user-stories` do phuryn aplica três Cs, INVEST, 4–6 critérios numerados por história (não Given/When/Then).
- **Conteúdo reutilizável (destilado):** checklist INVEST com pergunta-teste (Inferido): independente (pode ser entregue sem esperar outra?), negociável (descreve objetivo, não contrato?), valiosa (quem percebe valor se só ela for entregue?), estimável, pequena (cabe numa iteração?), testável (dá para dizer como confirmar?). Se falhar um, reescrever ou dividir.
- **Verificação:** glossário e SKILL.md lidos.

### V-19 — Histórias: cartão, conversa, confirmação — Classe B (7)
- **Lente:** authoritative (R-authoritative-17)
- **Tipo:** pattern | template
- **Fonte:** https://www.mountaingoatsoftware.com/agile/user-stories · **Autor/Org:** Mountain Goat Software (a página **não nomeia autor**)
- **Verificado:** atualizada em 2026-07-12; três Cs atribuídos a Ron Jeffries; template "Como [tipo de usuário], preciso/quero/sou obrigado a [fazer algo], para que [benefício]" (a página não fixa "quero"); critérios de aceite como exemplos, regras, testes ou notas; entendimento compartilhado vale mais que a forma.
- **Conteúdo reutilizável (destilado):** template de história + checklist "pronta para sprint": a equipe entende o que precisa ser verdade para contar como pronta.
- **Verificação:** página aberta.

### V-20 — EARS: sintaxe de requisitos — Classe B (6)
- **Lente:** authoritative + community (R-authoritative-18, R-community-21)
- **Tipo:** pattern
- **Fonte:** https://en.wikipedia.org/wiki/Easy_Approach_to_Requirements_Syntax (síntese; artigo original de Mavin et al., RE'09, não lido) · **Autor/Org:** Alistair Mavin e colegas (Rolls-Royce), 2009
- **Verificado:** padrões ubíquo, orientado a evento (WHEN), a estado (WHILE), funcionalidade opcional (WHERE), comportamento indesejado (IF/THEN) e complexo; forma `WHILE <pré-condições>, WHEN <gatilho>, the <sistema> SHALL <resposta>`; zero ou mais pré-condições, zero ou um gatilho, um nome de sistema, uma ou mais respostas.
- **Conteúdo reutilizável (destilado):** cinco modelos de frase em PT ("QUANDO <gatilho>, o <sistema> DEVE <resposta>", "ENQUANTO <estado>…", "ONDE <opção>…", "SE <falha>, ENTÃO…") e regra de ordem. Alternativa ao Given/When/Then; adotar um padrão principal por spec.
- **Ressalvas:** fonte secundária; mais de três pré-condições fica pesado; requisitos não condicionais encaixam mal.
- **Verificação:** página aberta.

### V-21 — RICE (Intercom) — Classe B (7)
- **Lente:** authoritative + community (R-authoritative-19, R-community-16)
- **Tipo:** template
- **Fonte:** https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/ · **Autor/Org:** Sean McBride, Intercom · 2018-01-05 (Verificado)
- **Verificado:** impacto 3/2/1/0,5/0,25; confiança 100/80/50% (abaixo disso "moonshot"); esforço em pessoa-mês (0,5 para menos de um mês); "RICE não é regra absoluta". A fórmula aparece só como imagem; **(Alcance × Impacto × Confiança) ÷ Esforço é corroborada** pela skill `prioritization-frameworks` do phuryn (MIT), que traz a mesma fórmula.
- **Conteúdo reutilizável (destilado):** planilha-modelo com as quatro colunas, escalas acima, regra "revisar scores que pareçam errados". "Sem dado de alcance, confiança 50%" é Inferido. "Não comparar RICE entre objetivos" não confirmado.
- **Ressalvas:** escala de confiança varia entre fontes secundárias (algumas citam 20%); registrar a versão usada.
- **Verificação:** artigo aberto.

### V-22 — Modelo Kano — Classe B (6)
- **Lente:** authoritative (R-authoritative-20)
- **Tipo:** checklist | template (questionário)
- **Fonte:** https://en.wikipedia.org/wiki/Kano_model · **Autor/Org:** Noriaki Kano (1984 nas referências; a página diz "anos 1980")
- **Verificado:** categorias must-be, one-dimensional, attractive, indifferent, reverse (a página não usa "basic" e "performance" como nomes; são sinônimos em outra seção); par funcional/disfuncional com cinco respostas (gosto, espero, neutro, tolero, desgosto) e tabela de avaliação. Seções de atributos que mudam e de medição empírica trazem avisos "sem fontes" e um exemplo marcado como ficcional.
- **Conteúdo reutilizável (destilado):** matriz de pares e formato de pergunta; usar para classificar, não para priorizar.
- **Ressalvas:** exige pesquisa com usuários reais; conferir o original antes de usar a tabela como regra.
- **Verificação:** página aberta.

### V-23 — MoSCoW — Classe B (6)
- **Lente:** authoritative (R-authoritative-21)
- **Tipo:** checklist
- **Fonte:** https://en.wikipedia.org/wiki/MoSCoW_method · **Autor/Org:** Dai Clegg (1994, RAD); uso com DSDM desde 2002
- **Verificado:** quatro categorias (Won't = "nesta entrega"); críticas: ambiguidade do Won't e falta de ordem dentro da categoria.
- **Conteúdo reutilizável (destilado):** tabela das quatro categorias com regra de corte, campo "reavaliar em" e rótulo "não nesta entrega" no lugar de "Won't".
- **Verificação:** página aberta.

### V-24 — Como escolher o framework de priorização (inclui ICE) — Classe B (6)
- **Lente:** community (R-community-11)
- **Tipo:** reference | skill
- **Fonte:** https://raw.githubusercontent.com/phuryn/pm-skills/main/pm-execution/skills/prioritization-frameworks/SKILL.md · **Autor/Org:** phuryn/pm-skills (MIT)
- **Verificado:** nove frameworks (Eisenhower, Impacto × Esforço, Risco × Recompensa, Opportunity Score, Kano, matriz ponderada, ICE, RICE, MoSCoW); fórmulas: Opportunity Score = Importância × (1 − Satisfação); ICE = Impacto × Confiança × Facilidade; RICE como acima; princípio "priorizar problemas, não funcionalidades".
- **Conteúdo reutilizável (destilado):** árvore de decisão (objeto, framework, incerteza, formato de saída): problemas de cliente → Opportunity Score; ideias/iniciativas → ICE ou RICE; requisitos → MoSCoW; expectativas → Kano (classifica, não prioriza). Preenche a lacuna ICE.
- **Ressalvas:** sem formato de saída único; links de ensino do autor não devem ser copiados.
- **Verificação:** arquivo lido.

### V-25 — Os quatro grandes riscos de produto — Classe B (7)
- **Lente:** authoritative (R-authoritative-22)
- **Tipo:** checklist
- **Fonte:** https://www.svpg.com/four-big-risks/ · **Autor/Org:** Marty Cagan, SVPG · 2017-12-04 (Verificado)
- **Verificado:** valor, usabilidade, viabilidade (engenharia), viabilidade de negócio; donos: product manager (valor e negócio), designer (usabilidade), líder de engenharia (viabilidade).
- **Conteúdo reutilizável (destilado):** matriz de quatro riscos com dono, pergunta de teste e campo "resolvido por qual evidência".
- **Ressalvas:** texto curto e opinativo; o livro INSPIRED não foi lido.
- **Verificação:** página aberta.

### V-26 — Shape Up: apetite, pitch e aposta — Classe B (7)
- **Lente:** authoritative (R-authoritative-23)
- **Tipo:** workflow | template (pitch)
- **Fonte:** https://basecamp.com/shapeup · **Autor/Org:** Ryan Singer, Basecamp/37signals
- **Verificado:** "Copyright ©1999-2026 37signals LLC. All rights reserved." **Só destilar; nunca reproduzir trecho.** Sumário e glossário confirmam apetite, rabbit holes, no-gos, pitch, betting table, circuit breaker, hill chart e ciclo de seis semanas.
- **Conteúdo reutilizável (destilado):** template de pitch: problema, apetite, solução de baixa fidelidade, limites, rabbit holes, no-gos, riscos de premissa.
- **Ressalvas:** ciclo de seis semanas é contexto do autor; adaptar.
- **Verificação:** página aberta.

### V-27 — Experimentos A/B: erros de desenho e de parada — Classe B (6)
- **Lente:** authoritative (R-authoritative-24)
- **Tipo:** checklist
- **Fonte:** https://www.evanmiller.org/how-not-to-run-an-ab-test.html · **Autor/Org:** Evan Miller · 2010-04-18 (Verificado)
- **Verificado:** fixar a amostra antes; dez espiadas com nível nominal de 1% resultam em ≈ 5% real (tabela do artigo); regra de bolso n ≈ 16·σ²/δ² (δ = menor efeito de interesse; σ² = p(1 − p) para conversão); alternativas: sequencial com checkpoints definidos e bayesiano.
- **Conteúdo reutilizável (destilado):** checklist de desenho (hipótese, efeito mínimo, amostra, critério de parada, alternativas sequenciais) com a fórmula rotulada "regra de bolso do autor".
- **Ressalvas:** artigo de 2010 (estatística atemporal); a cobertura de experimentação continua parcial (ver Lacunas).
- **Verificação:** artigo aberto.

### V-28 — Specs como artefatos vivos (Breunig) — Classe B (6)
- **Lente:** authoritative + community (R-authoritative-25, R-community-19)
- **Tipo:** principles
- **Fonte:** https://www.dbreunig.com/2026/05/04/10-lessons-for-agentic-coding.html · **Autor/Org:** Drew Breunig · 2026-05-04 (Verificado)
- **Verificado:** specs atualizadas junto com código e testes (spec congelada antes do trabalho perde o que se aprende); testes ponta a ponta de comportamento; intenção (o porquê) guardada junto ao código. **O ensaio não descreve diff entre spec e código construído** (lacuna confirmada).
- **Conteúdo reutilizável (destilado):** três artefatos vivos (spec de intenção, testes de comportamento, notas de decisão) com regra de atualização.
- **Ressalvas:** ensaio de opinião, sem dados.
- **Verificação:** ensaio aberto.

### V-29 — Comando `/feature-dev`: sete fases com paradas — Classe A (8) · Prompt-score 82
- **Lente:** authoritative + github (R-authoritative-26, R-github-10)
- **Tipo:** command | workflow
- **Fonte:** https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/feature-dev/commands/feature-dev.md · README https://github.com/anthropics/claude-code/tree/main/plugins/feature-dev · **Autor/Org:** Anthropic (README lista Sid Bidasaria)
- **Sinais:** `anthropics/claude-code` ≈ 149,9 mil ★, push 2026-10-09; **licença do repositório "null": destilar, não copiar**. Frontmatter só com `description` e `argument-hint`.
- **Verificado:** sete fases (descoberta, exploração com 2–3 agentes em paralelo, perguntas de esclarecimento, arquitetura, implementação, revisão de qualidade com 3 revisores, resumo); parada explícita na fase 3 ("crítico"), escolha na fase 4, aprovação obrigatória na fase 5 ("não inicie sem aprovação") e decisão na fase 6; a fase 1 pede confirmação, mas sem parada explícita; "o que achar melhor" exige recomendação e confirmação; usa TodoWrite.
- **Conteúdo reutilizável (reescrito, 4/4/5/4/2/4/4/5/4/4/5/4):** tabela de paradas obrigatórias (entendimento, respostas, escolha de abordagem, aprovação de implementação, destino dos achados) com política "resposta vaga nunca é aprovação" e gate configurável (padrão ativo).
- **Ressalvas:** exploração com vários subagentes consome contexto; ajustar ao orçamento.
- **Verificação:** comando e README lidos; licença: nenhuma visível.

### V-30 — Subagente arquiteto de leitura (code-architect) — Classe A (8) · Prompt-score 80
- **Lente:** github (R-github-11)
- **Tipo:** subagent
- **Fonte:** https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/feature-dev/agents/code-architect.md · **Autor/Org:** Anthropic (licença do repositório "null": destilar)
- **Verificado:** frontmatter `tools: Glob, Grep, LS, Read, NotebookRead, WebFetch, TodoWrite, WebSearch, KillShell, BashOutput`, `model: sonnet`, `color: green`. **Sem ferramenta de escrita, mas com web e controle de shell**; remover `WebFetch`, `WebSearch`, `KillShell` e `BashOutput` no nosso agente. Processo em três etapas (padrões do código incluindo CLAUDE.md, decisão única justificada, blueprint com arquivos, responsabilidades, fluxo de dados e fases) e saída com referências `arquivo:linha`.
- **Conteúdo reutilizável (reescrito, 4/4/4/5/2/5/3/5/4/4/4/4):** subagente somente leitura (`tools: Read, Grep, Glob`) e formato de saída (padrões com `arquivo:linha`, decisão, mapa de arquivos, sequência de build, riscos e testes).
- **Ressalvas:** em projeto novo o blueprint vira suposição, e deve ser rotulado como tal.
- **Verificação:** arquivo lido.

### V-31 — Regras de negócio `RULE-NNN` em Given/When/Then com `arquivo:linha` — Classe A (9) · Prompt-score 85
- **Lente:** authoritative + github (R-authoritative-27, R-github-09)
- **Tipo:** workflow | template
- **Fonte:** https://github.com/anthropics/claude-plugins-official/tree/main/plugins/code-modernization · **Autor/Org:** Anthropic
- **Sinais:** repo ≈ 37,6 mil ★, **Apache-2.0** (repo e README, Verificado), push 2026-10-09; CHANGELOG e LICENSE na pasta.
- **Verificado:** cartão `### RULE-NNN: <nome>` com Given/When/Then e citação `arquivo:linha`; uma regra por decisão de negócio, não por ramo; P0/P1/P2; segundo agente revalida; seis paradas humanas; veredictos PROVEN/PARTLY PROVEN/NOT PROVEN calculados por `scripts/proof_pack.py` a partir de evidência (não opinião); a extração por modelo não é determinística.
- **Conteúdo reutilizável (destilado):** template de `BUSINESS_RULES.md` e checklist de revisão de regra (fonte, prioridade, condição, resultado, revalidação).
- **Ressalvas:** foco em modernização; só reaproveitável para feature nova se houver código de referência. Não executar `scripts/`.
- **Verificação:** README aberto; licença e arquivos conferidos.

### V-32 — Árvore de oportunidades (Torres) e regras de construção — Classe B (7)
- **Lente:** authoritative + community (R-authoritative-29, R-community-12, R-community-24)
- **Tipo:** pattern | template
- **Fonte:** https://www.producttalk.org/opportunity-solution-tree/ (byline 2023-12-06; a página mostra itens de 2026) · implementação MIT: https://raw.githubusercontent.com/phuryn/pm-skills/main/pm-product-discovery/skills/opportunity-solution-tree/SKILL.md · **Autor/Org:** Teresa Torres (Product Talk); phuryn/pm-skills
- **Verificado:** estrutura resultado, oportunidades, soluções, testes de premissa; pré-requisitos (teoria do cliente-alvo, resultado claro, 3–4 entrevistas com histórias); uma oportunidade-alvo por vez e ≈ 3 soluções; uma árvore por resultado; entrevistas semanais e revisão a cada 3–4 entrevistas. A skill phuryn: 3–7 oportunidades (foco nas 2–3 melhores), ≥ 3 soluções por oportunidade, 1–2 experimentos com hipótese, método, métrica e limiar; Opportunity Score = Importância × (1 − Satisfação), normalizados de 0 a 1.
- **Conteúdo reutilizável (destilado):** template de árvore em Markdown (resultado, oportunidades, soluções, testes) com as regras acima; template de "snapshot" de entrevista é Inferido (fontes secundárias; página Vistaly existe e cita snapshots, mas sem o formato).
- **Ressalvas:** texto prescritivo, não empírico; o claim "70% mais rápido" de resumos de terceiros foi descartado.
- **Verificação:** páginas lidas; 3 URLs de terceiros (Vistaly, Maze, Miro) tratadas como pista.

### V-33 — Roteiro de entrevista de discovery com JTBD e regras anti-viés — Classe B (7) · Prompt-score 80 (fonte 76)
- **Lente:** community (R-community-08)
- **Tipo:** skill
- **Fonte:** https://raw.githubusercontent.com/phuryn/pm-skills/main/pm-product-discovery/skills/interview-script/SKILL.md (a lente github falhou com 404 num caminho adivinhado; este caminho correto está na lente community) · **Autor/Org:** Paul Huryn
- **Sinais:** `phuryn/pm-skills` ≈ 26,9 mil ★, MIT, push 2026-10-09 (search API).
- **Verificado:** seções com tempo (abertura 2–3 min, aquecimento 5 min, exploração JTBD 15–20 min, encerramento 3–5 min); regras: perguntar sobre a vida do participante e não sobre a ideia, comportamento passado, ouvir mais do que falar (≈ 80/20), não apresentar solução, tratar elogio genérico como ruído; perguntas-modelo ("me conte a última vez que…", "o que abriria mão para resolver isso?"). **Links de "Further Reading" apontam para curso pago (productcompass.pm): não copiar.**
- **Conteúdo reutilizável (reescrito, 4/4/4/4/4/5/3/4/4/4/4/4):** roteiro de 30 minutos com as quatro seções, oito perguntas-modelo sobre o passado e as cinco regras anti-viés; entrada: objetivo, premissas a validar, perfil do participante; saída: roteiro + modelo de anotações + premissas a confrontar.
- **Ressalvas:** segue princípios do Mom Test, cuja fonte primária (livro) não foi lida; o site oficial do Mom Test não lista as regras.
- **Verificação:** SKILL.md lido.

### V-34 — Skill `prd` com entrevista obrigatória e limites mensuráveis — Classe B (6) · Prompt-score 80 (fonte 66)
- **Lente:** github (R-github-07)
- **Tipo:** skill
- **Fonte:** https://raw.githubusercontent.com/github/awesome-copilot/main/skills/prd/SKILL.md · **Autor/Org:** GitHub (awesome-copilot)
- **Sinais:** frontmatter `license: MIT` (Verificado); repo ≈ 39,9 mil ★.
- **Verificado/corrigido:** discovery obrigatório com **no mínimo 2** perguntas (a lente dizia "bloquear antes de três respostas"); termos subjetivos como "rápido", "fácil" são **desencorajados** (não proibidos); desconhecidos viram `TBD`; non-goals obrigatórios; KPIs 3–5; cinco seções (Resumo executivo, UX e funcionalidade, requisitos de IA se aplicável, especificação técnica, riscos e roadmap MVP, v1.1, v2.0). O próprio arquivo é inconsistente (o exemplo omite critérios de aceite e non-goals e usa 2 KPIs) e cita ferramentas não definidas.
- **Conteúdo reutilizável (reescrito, 4/4/4/4/3/4/4/4/4/4/5/4):** regras de qualidade: (1) pergunte problema, métrica de sucesso e restrições antes de redigir; (2) troque adjetivos vagos por limites mensuráveis ("p95 < 800 ms medido em…"); (3) o que faltar vira `TBD` e entra em perguntas abertas; (4) non-goals obrigatórios; (5) roadmap em fatias; (6) seção de IA só se o produto usa IA.
- **Ressalvas:** a estrutura de IA não vale para software comum; sem checagem automática de prontidão.
- **Verificação:** SKILL.md lido.

### V-35 — PRD enxuto: máximo de três perguntas e premissas explícitas — Classe B (7) · Prompt-score 82 (fonte 78)
- **Lente:** community (R-community-09, R-community-14)
- **Tipo:** skill | prompt
- **Fonte:** https://raw.githubusercontent.com/phuryn/pm-skills/main/pm-execution/skills/create-prd/SKILL.md · duplicata de formato: https://raw.githubusercontent.com/github/awesome-copilot/main/skills/breakdown-feature-prd/SKILL.md · **Autor/Org:** phuryn/pm-skills (MIT); awesome-copilot (MIT no repo, arquivo sem licença própria)
- **Verificado:** máximo de três perguntas numa só mensagem, sem PRD nessa resposta, só sobre o que apenas o usuário sabe; oito seções (resumo, contatos, contexto, objetivo, segmentos, proposta de valor, solução, lançamento); alvo 600–1.000 palavras; desconhecidos vão para premissas e perguntas abertas, "nada inventado no corpo"; não-objetivos na seção de lançamento. O `breakdown-feature-prd` tem oito seções por feature (nome, épico, objetivo, personas, histórias, requisitos, critérios de aceite, fora de escopo), problema em 3–5 frases e **caminho de salvamento fixo do autor (não copiar)**.
- **Conteúdo reutilizável (reescrito, 4/4/4/4/3/5/4/4/5/4/4/4):** "se faltar dado de problema, usuário ou métrica, faça até três perguntas e pare; senão redija em 600–1.000 palavras, com tudo que for desconhecido sob Premissas e Perguntas abertas, e termine com o que fica de fora".
- **Ressalvas:** convenção própria de nome de arquivo; as skills linkam para material pago.
- **Verificação:** dois SKILL.md lidos.

### V-36 — Checklist de qualidade de critério de aceite Given/When/Then — Classe B (7) · Prompt-score 80
- **Lente:** github (R-github-17)
- **Tipo:** skill | checklist
- **Fonte:** https://raw.githubusercontent.com/product-on-purpose/pm-skills/main/skills/deliver-acceptance-criteria/SKILL.md · **Autor/Org:** product-on-purpose
- **Sinais:** repo ≈ 716 ★, **Apache-2.0** (frontmatter e search API), push 2026-10-08; versão 1.1.0.
- **Verificado:** só Given/When/Then; caminho feliz primeiro, depois falhas e bordas com comportamento visível; requisitos não funcionais (desempenho, acessibilidade, segurança, confiabilidade, auditabilidade); critério subjetivo vira resultado mensurável; checklist de sete itens (testável, sem detalhe de implementação…).
- **Conteúdo reutilizável (reescrito, 4/3/5/4/4/5/3/3/5/4/4/4):** ordem de cobertura feliz, falhas, não funcionais, e checklist de seis itens: escopo específico, caminho feliz primeiro, bordas explícitas, erros com recuperação visível, testável, sem detalhe de implementação.
- **Ressalvas:** não escreve histórias nem sistematiza bordas; combinar com V-42 (palavras vagas e regras implícitas).
- **Verificação:** arquivo e licença conferidos.

### V-37 — Skill `prd` para loop autônomo: histórias de uma sessão — Classe B (6) · Prompt-score 78 (fonte 72)
- **Lente:** github (R-github-22)
- **Tipo:** skill
- **Fonte:** https://raw.githubusercontent.com/snarktank/ralph/main/skills/prd/SKILL.md · **Autor/Org:** snarktank
- **Sinais:** `snarktank/ralph` ≈ 21,9 mil ★ e **MIT** (search API; a lente marcou como não verificado), último push 2026-02-02 (≈ 8 meses). Frontmatter `user-invocable: true`.
- **Verificado:** 3–5 perguntas com opções lettered (A, B, C…); cada história cabe em uma sessão focada; "Typecheck passes" em toda história; história de UI inclui verificação no navegador (via skill `dev-browser`, dependência externa); requisitos `FR-1`; non-goals obrigatórios; "não comece a implementar".
- **Conteúdo reutilizável (reescrito, 4/4/4/4/4/4/4/3/4/4/3/5):** formato de pergunta com opções lettered ("1A, 2C"), regra de tamanho de história (uma sessão), critério observável ou reescrever, critério comum a todas as histórias (build/typecheck/lint passam).
- **Ressalvas:** sem ordem formal de dependência; o loop `ralph.sh` não foi lido nem deve ser executado sem revisão.
- **Verificação:** SKILL.md lido; licença via search API.

### V-38 — Sequência de comandos spec-driven com gate e revisão em contexto novo (ai-prd-workflow) — Classe B (5) · Prompt-score 73
- **Lente:** github (R-github-21)
- **Tipo:** workflow
- **Fonte:** https://raw.githubusercontent.com/nurettincoban/ai-prd-workflow/main/README.md · **Autor/Org:** nurettincoban
- **Sinais:** ≈ 298 ★, MIT, push 2026-10-08 (search API). Oito comandos (`/create-prd`, `/verify-prd`, `/extract-features` com MoSCoW, `/generate-rules`, `/generate-rfcs`, `/test-strategy`, `/implement-rfc`, `/review-rfc`) conferidos; `/implement-rfc` para após o plano; `/review-rfc` recusa código escrito na mesma conversa; precedência PRD, FEATURES, RULES, RFCs.
- **Segurança:** o README oferece `curl -fsSL … | bash`. **Não recomendar; se o plugin referenciar, usar clone + revisão + `--ref` de tag. `scripts/trace-check.py` não lido.**
- **Conteúdo reutilizável (destilado):** sequência de etapas, regra de precedência entre documentos e a regra de revisão em contexto novo.
- **Ressalvas:** projeto pequeno e de autor único; só MoSCoW como priorização.
- **Verificação:** README lido.

### V-39 — Crítica a ferramentas SDD e quanto de spec manter (Böckeler/Fowler + sinais HN) — Classe A (8)
- **Lente:** community (R-community-02; sinais de R-community-03, 04, 05)
- **Tipo:** anti-pattern | pattern
- **Fonte:** https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html · **Autor/Org:** Birgitta Böckeler (Thoughtworks) · 2025-10-15 (Verificado)
- **Verificado:** níveis spec-first, spec-anchored, spec-as-source; críticas: fluxo único para todos os tamanhos, revisar muito markdown cansa, Kiro gerou quatro histórias e 16 critérios para um bug pequeno; a citação "Are we making something worse in the attempt of making it better?" aparece na conclusão. HN: 128 pontos e 32 comentários (Verificado).
- **Sinais C (HN, Verificado):** Ask HN "still using SDD?" (6 pts, 7 comentários, 2026-02-03): ferramenta é opcional; um comentarista descreve o prompt explorar, listar dúvidas, escrever plano em markdown e diz que ≈ 20% das perguntas revelam pontos novos (opinião individual). Ask HN "still pay off with frontier models?" (6 pts, 4 comentários, 2026-09-24): planos curtos, explicar o porquê, revisar plano é mais rápido que revisar diff.
- **Conteúdo reutilizável (destilado):** checklist "quanto de spec": diff de uma frase = sem spec; mudança de uma tela = spec curta; regras de negócio = spec com critérios testáveis e dono de manutenção; spec de intenção (por quê, fora de escopo, decisões já tomadas, lacunas a perguntar).
- **Ressalvas:** análise qualitativa; HN com baixo engajamento.
- **Verificação:** artigo e duas árvores de comentários lidos; listagem HN (Marmelab 225/191, VSDD 211/118, spec-kit 84/42) conferida.

### V-40 — Pesquisa, plano, anotação e checklist de fases (Boris Tane) — Classe B (6) · Prompt-score 70
- **Lente:** community (R-community-18)
- **Tipo:** workflow
- **Fonte:** https://boristane.com/blog/how-i-use-claude-code/ · **Autor/Org:** Boris Tane · 2026-02-10 (Verificado)
- **Verificado:** `research.md` persistente, `plan.md`, anotação humana 1–6 rodadas com a regra "não implemente ainda", checklist de fases marcado conforme o avanço. Não menciona pular permissões.
- **Conteúdo reutilizável (destilado, 3/4/4/3/2/3/3/4/4/5/3/4):** ciclo pesquisa, plano, anotação, checklist, com instrução explícita de não implementar durante a revisão e de registrar a pesquisa em arquivo.
- **Ressalvas:** prática individual; sem métricas.
- **Verificação:** post lido.

### V-41 — Specs do Kiro: requisitos, design, tarefas e bugfix com "comportamento inalterado" — Classe B (7)
- **Lente:** community (R-community-20)
- **Tipo:** workflow | template
- **Fonte:** https://kiro.dev/docs/specs/ · **Autor/Org:** Kiro (AWS), página atualizada em 2026-10-02 (Verificado)
- **Verificado:** feature spec "requisitos primeiro" ou "design primeiro"; `requirements.md` (ou `bugfix.md`), `design.md`, `tasks.md`; bugfix com comportamento atual, esperado e **inalterado**; análise de requisitos (inconsistências, ambiguidades, lacunas) antes do design; tarefas em ondas pelo grafo de dependências; "quick spec" sem etapas de aprovação.
- **Conteúdo reutilizável (destilado):** template de bugfix com três blocos (atual, esperado, inalterado) e checagem de lacunas antes do design.
- **Ressalvas:** texto de vendor; formato dos requisitos não definido na página.
- **Verificação:** página lida.

### V-42 — Checklist da casa: palavras vagas, regras implícitas e NFR (QA) — Classe A (9, base própria)
- **Lente:** community (R-community-22)
- **Tipo:** checklist | reference
- **Fonte:** `C:\Users\Francisco Edson\dev-segments\docs\foundation\brain-of-agent-snapshot\brains\qa\references\requisitos-e-bdd.md` · **Autor/Org:** base própria
- **Verificado:** tabela de palavras vagas com a pergunta que as substitui; INVEST com sinal de problema para QA; nove categorias de regras implícitas; tabela de NFR com critério mensurável; escolha entre regra + exemplo, Gherkin e checklist; tabela ruim x bom; Example Mapping (cores amarelo, azul, verde, vermelho).
- **Uso:** **referenciar, não duplicar** (pertence ao segmento QA). O `CLAUDE.md` da pasta snapshot traz palavras-chave de outros protocolos; foram ignoradas por não fazerem parte do pedido. Licença MIT da base: não reverificada.
- **Verificação:** arquivo lido localmente.

### V-43 — OKRs: guia oficial Google re:Work (substitui R-authoritative-28) — Classe B (7) · adicionado pelo validador
- **Lente:** authoritative (lacuna; origem R-authoritative-28, que usava uma URL inexistente)
- **Tipo:** reference
- **Fonte:** https://rework.withgoogle.com/intl/en/guides/set-goals-with-okrs · **Autor/Org:** Google re:Work
- **Verificado (a URL de caminho `…/guides/set-goals-with-okrs/steps/introduction/` da lente dava 404; esta abre):** "cerca de três" key results por objetivo; 3–5 objetivos por equipe; nota de 0,0 a 1,0; sucesso é ≈ 70% e o "ponto ideal" é 0,6–0,7; nota baixa é dado para calibrar o próximo ciclo; OKR não é avaliação de desempenho; notas não são ciência. **A página não usa os rótulos "comprometido" e "aspiracional"** (a lente atribuía alvo 1,0 e 0,7): não usar essa distinção como regra do Google.
- **Conteúdo reutilizável (destilado):** modelo de OKR: um objetivo qualitativo, ≈ 3 key results mensuráveis, nota 0–1 como dado de calibração; regra "não usar OKR para avaliar pessoas".
- **Ressalvas:** guia curto de empresa; sem evidência de eficácia. Nota de classe: 7 por autoridade, sem licença de reuso.
- **Verificação:** página aberta nesta validação.

### V-44 — Sprint Planning no Scrum Guide 2020 — Classe B (7) · adicionado pelo validador
- **Lente:** authoritative (lacuna: sprint planning e refinamento)
- **Tipo:** reference
- **Fonte:** https://scrumguides.org/scrum-guide.html · **Autor/Org:** Ken Schwaber e Jeff Sutherland, edição de novembro de 2020
- **Verificado:** Sprint Planning responde três perguntas (por que a Sprint é valiosa, o que pode ser feito, como o trabalho escolhido será feito); a Sprint Goal é definida ali; timebox de até oito horas para Sprint de um mês; tarefas do plano com ≤ 1 dia; refinamento do Product Backlog é atividade contínua (descrição, ordem, tamanho); Definition of Done. Licença do texto: **Não verificável** (rodapé indica © 2020 Schwaber/Sutherland e © 2025 ScrumGuides.org): destilar.
- **Conteúdo reutilizável (destilado):** checklist de planejamento de sprint em três blocos (valor/meta, seleção, decomposição) e critério de "pronto para entrar em sprint" ligando a V-18.
- **Ressalvas:** descreve Scrum, não é universal; o guia diz que o plano é feito pelo time inteiro, e o plugin só apoia.
- **Verificação:** página aberta.

### V-45 — Roadmap Now-Next-Later (ProdPad) — Classe B (5) · adicionado pelo validador
- **Lente:** authoritative (lacuna: roadmap)
- **Tipo:** pattern
- **Fonte:** https://www.prodpad.com/blog/invented-now-next-later-roadmap/ · **Autor/Org:** ProdPad (Janna Bastow reivindica a invenção; a página não traz data exata)
- **Verificado:** Now = em andamento e bem definido; Next = fila depois do Now, menos detalhe; Later = problemas maiores e vagos, não decompostos; justificativa: roadmaps por data forçam prazos e reduzem flexibilidade; ligar iniciativas a objetivos de negócio. Origem: autoatribuída.
- **Conteúdo reutilizável (destilado):** template de roadmap em três colunas com campos "problema, resultado esperado, grau de certeza" e sem datas obrigatórias.
- **Ressalvas:** fonte comercial e autoatribuída; sem evidência de eficácia; classe B só pelo uso difundido.
- **Verificação:** página aberta.

---

## Rejeitados, rebaixados e mantidos como sinal C

| Item | Decisão | Motivo |
| --- | --- | --- |
| R-authoritative-28 (OKR, URL 404) | Rebaixado e substituído por V-43 | A URL tentada deu 404, mas a página oficial existe em `/intl/en/guides/set-goals-with-okrs`; "comprometido/aspiracional" não aparece nela. |
| R-github-15 `user-story` (deanpeters) | Rebaixado a C | `deanpeters/Product-Manager-Skills` (≈ 7,2 mil ★) tem **LICENSE CC BY-NC-SA 4.0 (Verificado)**, incompatível com plugin possivelmente comercial; o arquivo cita outro repositório sem licença declarada. Usar apenas a ideia "um When e um Then", coberta por V-36. |
| R-github-16 `jobs-to-be-done` (deanpeters) | Rebaixado a C | Mesma licença NC-SA; conteúdo existe (três tipos de job, pains, gains, "por quê" repetido), mas só como inspiração. |
| R-community-13 (índice do mesmo repositório) | Rebaixado a C | Licença NC-SA; escopo lido só no índice. |
| R-github-18 CLAUDE.md de PM (aakashg) | Rebaixado a C | Modelo com campos vazios, banner promocional ("Full PM OS"); 160 ★; push 2026-03-04. Ideias úteis absorvidas nas recomendações: sequência de verificação (perguntar, rascunhar, autorrevisar, sinalizar lacunas), marcador `[NEED: …]`, regra "propor regra e esperar aprovação". |
| R-github-19 PRD-driven context engineering | Rebaixado a C | 180 ★, autor único; a instalação manda rodar `bash install.sh` e um bootstrap não lidos; 41 skills e o script de prontidão não foram lidos. Só ideias: IDs estáveis por tipo e Definition of Done por estágio (limiares 70/50 são do autor, Suposição). |
| R-github-20 Claude Code Spec Workflow (Pimzino) | Rebaixado a C | ≈ 3,9 mil ★, MIT, último push 2025-09-07 (> 13 meses); a página diz que o foco migrou para uma versão MCP; contagem de comandos inconsistente (10, 14 ou 11); instalação global via npm. Só a convenção de nomes `spec-create/execute/status` e `steering` x `specs`. |
| R-community-03 Ask HN "still using SDD?" | Mantido como sinal C | Seis pontos e sete comentários; opiniões individuais. Incorporado em V-39. |
| R-community-04 Ask HN "still pay off?" | Mantido como sinal C | Seis pontos e quatro comentários. Incorporado em V-39. |
| R-community-05 listagem HN | Mantido como sinal C | Só metadados; números conferidos (Marmelab 225/191, VSDD 211/118, spec-kit 84/42, Show HN 40/17 e 20/12); útil para descobrir, não como fonte. |
| R-community-07 estudo de expertise como "checklist de pedido" | Rebaixado | O artigo não afirma que especialistas pedem verificação mais vezes, que pedidos claros associam-se a mais sucesso nem trata de "o que não muda". O estudo vira V-08 como princípio; o checklist de pedido continua válido, mas fundamentado em V-02 e V-01. |
| R-community-24 Torres via fontes secundárias | Rebaixado a C | Fonte primária de snapshot não aberta; página Vistaly é vendor. Método coberto por V-32. |
| R-community-17 Dwyer, SPEC.md curto | Rejeitado | Recomenda sempre `--dangerously-skip-permissions`, inclusive em produção, e a pista do atlas sobre as seções da spec não confere (o SPEC mostrado tem lista de features, detalhes de implementação e detalhes técnicos). |
| R-community-23 blogs de SDD (Medium, DataCamp, DEV, Pimzino) | Rejeitado como fonte | Pistas não lidas; o DataCamp abriu (autor Bexruz Tuychiev, 2026-05-19), mas é promocional, com estrelas e artefatos "reais" não verificáveis. |
| R-community-26 Reddit | Lacuna (não é item) | Reddit bloqueado para a ferramenta; nenhum post lido. |

Afirmações desmentidas ou não sustentadas nos itens aprovados (já corrigidas acima): `features.json` (V-06); "pelo menos três respostas" no prd (V-34); "12 passos"/"16 passos" no brainstorming (V-15); Background só com Given (V-16); critério de conclusão por fase no implementation-plan (V-13); estudo de expertise como guia de pedido (V-08); seções do Dwyer; estrelas "97 mil", "72 mil", "39 mil" do spec-kit/awesome-copilot citadas fora de contexto; "licença não encontrada" de anthropics/skills (a do skill-creator é Apache-2.0).

## Mapa de cobertura do escopo

| Subtema | Itens aprovados | Qualidade | Lacuna? |
| --- | --- | --- | --- |
| Entrevista guiada por IA antes da spec | V-01, V-15, V-40 | Alta (A) | Não |
| Descoberta contínua e árvore de oportunidades | V-32, V-33, V-25 | B | Parcial (Torres só no site; sem snapshot primário) |
| JTBD e entrevistas de troca | V-33 (MIT), C: deanpeters | B | Sim: sem fonte primária de Moesta/Christensen/Ulwick; HBR 2016 abre só o resumo; Mom Test sem as regras |
| PRD e spec de produto | V-09, V-34, V-35, V-11 | A/B | Não |
| Histórias de usuário | V-18, V-19, V-37 | A/B | Não |
| Critérios de aceite (Gherkin, EARS) | V-16, V-17, V-20, V-36, V-42 | A/B | Não |
| Priorização (RICE, ICE, MoSCoW, Kano) | V-21, V-22, V-23, V-24 | B | Parcial (WSJF; Kano só secundária) |
| Roadmap | V-45 | B (5) | Sim, parcial (uma fonte autoatribuída) |
| OKRs e métricas | V-43 | B | Sim para métricas (north star, HEART, árvore de métricas) |
| Experimentos A/B | V-27 (Kohavi apenas como referência C, não aprovado) | B | Parcial: site e HBR de Kohavi existem (autores Kohavi, Tang, Xu; Cambridge 2020) mas só bibliografia; sem OEC, guardrail, SRM |
| Sprint planning e refinamento | V-44, V-42 (Example Mapping) | B | Parcial (sem three amigos oficial nem prática de refinamento por fonte A) |
| SDD com IA | V-09, V-10, V-11, V-12, V-38, V-39, V-41 | A/B | Não |
| Ferramentas Claude Code e skills | V-01..V-07, V-29, V-30 | A | Não |
| Planejamento com IDs rastreáveis | V-13, V-09, V-31 | A/B | Não |
| Português do Brasil | nenhum | n/a | Sim (traduzir os prompts destilados) |
| Redes sociais (Reddit, X, YouTube, newsletters) | só HN | C | Sim |

## Lacunas objetivas e pesquisáveis

1. JTBD primário: ler o capítulo ou resumo oficial de *Competing Against Luck* (Christensen), o framework Outcome-Driven Innovation (Ulwick) e a entrevista de troca de Moesta/Re-Wired Group (forças de progresso: empurrão, atração, ansiedade, hábito) em site do autor; registrar cada URL com autoria.
2. Mom Test: página ou resumo do autor (Rob Fitzpatrick) com as três regras citadas pelo livro (perguntar sobre a vida e não a ideia, sobre o passado específico, falar menos); validar contra V-33.
3. Experimentação: capítulos acessíveis de Kohavi, Tang e Xu (OEC, métricas de guarda, SRM, sample ratio, p-valor e peeking) em `experimentguide.com` ou paper público; Evan Miller "Sequential A/B testing".
4. Métricas de produto: North Star (Amplitude), HEART (Google, Rodden et al. 2010), AARRR; árvore de métricas.
5. Roadmap: segunda fonte para Now-Next-Later e para roadmap por resultado (Roman Pichler, Melissa Perri "Build Trap", SVPG "Product Roadmaps").
6. Refinamento de backlog / three amigos / Example Mapping: fonte A (Cucumber blog de Matt Wynne ou docs oficiais) para Example Mapping; definição de "ready" sem inventar.
7. Priorização: WSJF (SAFe) e Kano em fonte primária (Kano 1984, ou artigo revisado); ICE em Sean Ellis.
8. Reddit, X, YouTube e newsletters: reabrir a lente community com rota de acesso permitida (busca web de domínio específico ou URL colada pelo usuário); a cota de WebSearch da sessão estava esgotada durante esta validação, então nenhuma busca nova pôde ser feita.
9. Português do Brasil: repositórios e prompts de PRD/spec em pt-BR (nenhum encontrado).
10. Licenças: confirmar `LICENSE` de `anthropics/claude-code` (feature-dev) e de `anthropics/skills` (nível de repositório), hoje "null" na API; docs da Anthropic e do Cucumber seguem sem licença de reuso declarada, só destilar.

## Recomendações ao construtor

**Skills**
- `interviewing-for-specs` (de V-01, V-15, V-40): entrevista em rodadas curtas, play back, gate de aprovação configurável; saída SPEC.md.
- `writing-specs` (de V-09, V-10, V-20, V-35, V-39): template de spec e de tarefas, `[NEEDS CLARIFICATION]`, IDs `FR-`/`SC-`/`T`; regra "quanto de spec" por tamanho de tarefa.
- `writing-acceptance-criteria` (de V-16, V-17, V-36, V-42): Given/When/Then declarativo; ordem feliz, falhas, não funcionais; palavras vagas e regras implícitas (referenciar o segmento QA, não duplicar).
- `splitting-user-stories` (de V-18, V-19, V-37): INVEST, três Cs, tamanho de uma sessão.
- `prioritizing-features` (de V-21, V-22, V-23, V-24): árvore de decisão com RICE, ICE, MoSCoW, Kano.
- `running-discovery` (de V-32, V-33, V-25): árvore de oportunidades, roteiro de entrevista, matriz dos quatro riscos.
- `writing-prds` (de V-34, V-35): PRD enxuto com no máximo três perguntas, non-goals, premissas.

**Agentes**
- `spec-reviewer` (somente leitura, contexto novo): de V-03, V-17, V-18, V-12 (gate de confiança como Suposição configurável).
- `plan-writer` (leitura + escrita só em `plans/`): de V-13 corrigido, com critério de conclusão por fase.
- `architect-readonly` (`Read, Grep, Glob`): de V-30.
- `adr-writer` (de V-14) e `rules-extractor` (de V-31, `RULE-NNN`).

**Comando**
- `/spec-feature` (de V-29, V-01, V-38): paradas obrigatórias (entendimento, perguntas, abordagem, aprovação), depois SPEC.md e sessão nova; modo autônomo opcional documentado.
- `/tasks-from-spec` (de V-10, V-37).

**Checklists**
- `spec-readiness` (V-11, V-02), `skill-publishing` (V-04, V-05), `experiment-design` (V-27), `sprint-planning` (V-44).

**Referências (`references/`)**
- `prioritization.md` (V-21..V-24), `discovery.md` (V-25, V-32, V-33), `roadmap-okr.md` (V-43, V-45, V-26), `acceptance-criteria.md` (V-16, V-17, V-20, V-36), `delegation.md` (V-07), `harness.md` (V-06).

**Prompts da biblioteca**
- Entrevista (V-01), revisão adversarial (V-03), brainstorming (V-15), PRD enxuto (V-35), roteiro de entrevista (V-33), briefing de subagente (V-07).

**Regras de CLAUDE.md** (curtas; cada linha deve passar no teste "remover isto faria o Claude errar?")
- "Antes de implementar, confirme a spec aprovada e o check que prova cada requisito." (V-01, V-02)
- "Nunca declare pronto sem a saída real do check; diga o que não foi verificado." (V-02)
- "Dúvida sem resposta vira `[NEEDS CLARIFICATION]`/`TBD`, nunca suposição no texto." (V-09, V-34)
- "Não rode scripts nem instaladores de repositórios de terceiros sem ler; não use `--dangerously-skip-permissions`." (segurança; V-38, rejeitado R-community-17)

**Cuidados de licença e segurança**
- Literal só de itens com licença permissiva comprovada e atribuição: spec-kit (MIT), superpowers (MIT), awesome-copilot (MIT), skill-creator e code-modernization (Apache-2.0), pm-skills do phuryn (MIT), product-on-purpose (Apache-2.0), ralph (MIT). Mesmo assim, o plugin deve reescrever. Docs da Anthropic, Cucumber, Intercom, Shape Up, SVPG, Evan Miller, Mountain Goat e Breunig: só destilar; deanpeters: não usar texto (NC-SA).
- Não reproduzir links de curso pago nem banners promocionais; não referenciar `curl | bash`.
- Gates humanos (V-15, V-29, V-31) configuráveis, com padrão ativo; ações externas e irreversíveis exigem confirmação.
- Esta validação foi feita por um modelo diferente do pesquisador (independência parcial); revisão humana do plugin final continua recomendada.
