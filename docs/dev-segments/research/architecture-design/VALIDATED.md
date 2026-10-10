# Arquitetura e design de sistemas (architecture-design) — VALIDADO (consolidado das 3 lentes)

Data: 2026-10-10 · Validador: claude-sonnet-5-5 (modelo diferente dos pesquisadores, claude-haiku-5-5, mas da mesma família Claude; a independência é parcial e está declarada) · Rubricas: prompt-quality-rubric (D1–D12) e source-quality-rubric (0–10)

## Cabeçalho e estatísticas

| Lente | Itens recebidos | Aprovados (diretos ou fundidos em um V-) | Rebaixados (só sinal/ideia, classe C) | Rejeitados | Itens com correção de fato |
| --- | --- | --- | --- | --- | --- |
| authoritative | 29 | 29 | 0 | 0 | 10 (R-04 restrições de plugin, R-07 contagem 8–10, R-08 e R-09 licença, R-09 contagem de seções, R-10 telemetria, R-11 número 90,2%, R-12 data, R-18 checklist, R-25 "não fazer nada") |
| github | 20 | 16 | 2 (R-13, R-16) | 2 (R-19, R-20 como item) | 6 |
| community | 25 | 12 | 6 (R-03, R-04, R-05, R-10, R-19, R-24) | 7 (R-02, R-07, R-09, R-11, R-21, R-22, R-23) | 4 (R-01 autoria e data, R-07 exemplo tRPC, R-12 licença, R-25 mantido via espelho) |
| **Total** | **74** | **57** | **8** | **9** | — |

- Itens aprovados consolidados e deduplicados entre as lentes: **45 entradas V-01 a V-45** (40 vêm de itens recebidos; 5 foram descobertos pelo validador para fechar lacunas: V-25 hexagonal, V-32 bulkhead, V-37 event sourcing, V-38 cache-aside, V-39 API design da Microsoft; V-26 foi ampliado com agregados).
- Fontes re-verificadas com ferramentas: cerca de 100 URLs/recursos abertos de novo (páginas, arquivos raw, feeds de commits, Algolia/HN, páginas de repositório). Cobertura de re-verificação por lente: authoritative 29/29 (100%), github 18/20 (90%), community 22/25 (88%). Todos os itens de classe A foram relidos. Não foi possível reler: github R-19 (caminho 404, já relatado), community R-21/R-22/R-23 (só havia snippets de catálogos; não há URL estável para abrir).
- Pontuação de prompts (D1–D12, 0–100) dos 17 artefatos de prompt/skill/agente/regra coletados: média **65,5** (aprovados: 67,5). Os prompts de origem são medianos: poucos passam de 80 (proyecto26 caching 87, skill-creator 82, adlc adr 78). Por isso o que se aprova é o conteúdo (padrão, checklist, critério) e o texto reescrito nesta lista; nenhum prompt de terceiro deve ser copiado como está.
- GitHub API: `api.github.com` voltou a dar HTTP 403 (rate limit) neste ambiente. Metadados foram obtidos por páginas HTML do repositório (estrelas via `stargazerCount`), feeds Atom de commits (`/commits/<branch>.atom`, data do último commit) e arquivo LICENSE raw. Isso resolveu a lacuna "datas e licenças não verificadas" das duas lentes.
- Independência: o validador reabriu tudo por conta própria e discordou dos pesquisadores em vários pontos (tabela de correções abaixo).

### Metadados de repositórios verificados nesta validação (2026-10-10)

| Repositório | Estrelas | Licença (arquivo) | Último commit | Observação |
| --- | --- | --- | --- | --- |
| anthropics/skills | 180,2 mil | Apache-2.0 em `skills/skill-creator/LICENSE.txt` (README: nem toda skill é permissiva) | 2026-10-09 | skill-creator com licença permissiva verificada |
| anthropics/claude-code | 149,9 mil | `LICENSE.md`: "© Anthropic PBC. All rights reserved." + Commercial Terms | 2026-10-09 | **não permissivo**: feature-dev só pode ser destilado |
| anthropics/claude-plugins-official | 37,6 mil | Apache-2.0 (repo e plugin code-modernization) | 2026-10-09 | permissivo |
| github/awesome-copilot | 39,9 mil | MIT | 2026-10-09 | |
| garrytan/gstack | 135,7 mil | MIT | 2026-10-09 | |
| PatrickJS/awesome-cursorrules | 40,9 mil | CC0-1.0 | 2026-05-30 | 4+ meses sem commit |
| wshobson/agents | 40,3 mil | MIT | 2026-10-04 | |
| VoltAgent/awesome-claude-code-subagents | 25,6 mil | MIT | 2026-10-05 | README diz "161+" subagentes |
| Jeffallan/claude-skills | 11,8 mil | MIT | 2026-10-03 | |
| athola/claude-night-market | 341 | MIT | 2026-10-02 | agregador dizia ~325 |
| proyecto26/system-design-skills | 85 | MIT | 2026-06-02 | |
| wuersch/adlc | 1 | MIT | 2026-08-01 | "early alpha" |
| mblode/agent-skills | 144 | MIT (LICENSE.md) | 2026-10-08 | |
| affaan-m/everything-claude-code | 276 mil | MIT | 2026-10-10 | popularidade enorme não prova qualidade |

### Correções de fato aos pesquisadores (resumo)

| Onde | Afirmado | Verificado |
| --- | --- | --- |
| authoritative R-08/R-09, github R-05/R-06, community R-14 | licença de feature-dev/code-architect "não verificada" | `anthropics/claude-code/LICENSE.md` = todos os direitos reservados. Somente destilação com redação própria. |
| authoritative R-09 | "saída fixa com seis seções" | A lista tem **sete** blocos (padrões, decisão, componentes, mapa de implementação, fluxo de dados, sequência de build, detalhes críticos). |
| authoritative R-11 | número 90,2% "só em resumo de terceiros" | Está na página oficial (avaliação interna, líder Opus 4 + subagentes Sonnet 4, junho de 2025). Os modelos citados são antigos; tratar como evidência histórica. |
| authoritative R-12 | texto de Fowler "antigo" (atualidade 1) | A página está datada de 24 de março de 2026. Atualidade 2. |
| authoritative R-18 | item 7 do checklist: evento "fora do fluxo transacional principal" | A fonte manda gravar estado e evento na mesma transação, mesmo contêiner e mesma partição lógica. Item 7 corrigido em V-34. |
| authoritative R-25, github R-01 | o agente não exige "não fazer nada" como alternativa | O arquivo diz "Include the 'do nothing' option if applicable". Ressalva retirada. |
| authoritative R-07 | "10 consultas positivas e 10 negativas" | O arquivo pede 20 consultas, **8–10** que devem disparar e **8–10** que não devem (com casos limítrofes); a otimização usa divisão 60/40 treino/teste. |
| community R-01 | ensaio "Claude Is Not Your Architect", abril/2026, pontuação 7,8, não lido; técnica de premortem | Ensaio de Charlie Holland (hollandtech.net), 6 de abril de 2026. A thread de maio de 2026 no HN tem 275 pontos e 190 comentários (id 48259784). O ensaio **não** menciona premortem nem "o que não construir"; pede desafiar com "há opção mais simples?" e manter um dono humano por decisão. O premortem do pesquisador é construção própria (Inferido). |
| community R-07 | migração REST para "outra API tipada" | É REST para tRPC. As métricas do post (5–7 para 2–3 iterações etc.) não têm método: descartadas. |
| github R-14 | erro "RFC 7807" como boa prática | RFC 9457 (julho de 2023) **obsoleta** a RFC 7807. Corrigido em V-40. |
| github R-02/authoritative R-28 | injeção dirigida à IA no SKILL.md do gstack | Não foi encontrada no arquivo raw (busca por "citation/disclaimer": 0 ocorrências); provável artefato do sumarizador do WebFetch. O arquivo tem outro problema real: 705 linhas, acoplado a binários `gstack-*`, telemetria e escrita em `~/.gstack`. Não importar o arquivo. |
| github R-14 | estrelas "não verificadas" | 11,8 mil (MIT). Sobe de C para B. |
| authoritative R-10 | licença/plugin | Confirmado Apache-2.0 no README do plugin. Novo: a telemetria é ligada por padrão (contagens arredondadas; desligar com `CODE_MODERNIZATION_TELEMETRY=0` ou `DISABLE_TELEMETRY=1`). |
| authoritative R-04 | frontmatter de subagente | Falta o fato mais importante para um plugin: **subagentes de plugin ignoram `hooks`, `mcpServers` e `permissionMode`** (copiar o arquivo para `.claude/agents/` para usá-los). Incluído em V-04. |

## Itens aprovados

Legenda: Verificado = conferido por mim nesta validação; Inferido = síntese minha; Suposição = não validada. Conteúdo reutilizável sempre com redação própria. Atribuição: onde a licença permite citação literal (MIT, Apache-2.0, CC0), nenhum trecho literal foi necessário.

### V-01 — Building effective agents: workflow antes de agente (origem authoritative R-01, community R-18) — Classe A (8/10) · Lente: authoritative+community
- **Tipo:** reference · pattern
- **Fonte:** https://www.anthropic.com/engineering/building-effective-agents · Anthropic · publicado em 19/12/2024; a página avisa que o ecossistema de ferramentas mudou desde então
- **Sinais:** Anthropic Engineering; sem licença de reuso (destilar)
- **Para que serve:** decidir workflow fixo versus agente; escolher a menor complexidade que resolve; desenhar a interface das ferramentas (ACI).
- **Técnicas-chave:** cinco padrões (prompt chaining, routing, parallelization com seccionamento ou votação, orchestrator-workers, evaluator-optimizer); começar simples; tornar o planejamento explícito; poka-yoke nas ferramentas (a fonte conta que exigir caminhos absolutos eliminou erros).
- **Conteúdo reutilizável (reescrito):** Checklist de decisão para o plugin: (1) uma chamada simples com bom contexto resolve? Pare aí. (2) O caminho é conhecido? Use workflow com checagens entre passos. (3) As subtarefas são independentes? Paralelize. (4) A decomposição só se sabe na execução? Orchestrator-workers com limite de subagentes. (5) Existe critério verificável de qualidade? Evaluator-optimizer com número máximo de rodadas. Regra de CLAUDE.md: "Comece pelo workflow mais simples; só acrescente autonomia com evidência de ganho."
- **Ressalvas:** texto de 2024; os padrões são atemporais, os exemplos de ferramenta não.
- **Verificação:** página aberta; data, os cinco padrões, poka-yoke/caminhos absolutos e "comece simples" conferidos.

### V-02 — Context engineering para agentes (origem authoritative R-02, community R-18) — Classe A (8/10) · Lente: authoritative+community
- **Tipo:** reference · checklist
- **Fonte:** https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents · Anthropic · 29/09/2025
- **Para que serve:** decidir o que entra no contexto de agentes de arquitetura (prompt, ferramentas, notas de decisão, subagentes).
- **Técnicas-chave:** menor conjunto de tokens de alto sinal; "altitude certa" do prompt (nem lógica frágil nem vaguidão); conjunto mínimo de ferramentas sem sobreposição; compaction, notas estruturadas fora da janela e subagentes com contexto limpo que devolvem resumo.
- **Conteúdo reutilizável (reescrito):** (a) Prompt de agente de arquitetura começa mínimo e só ganha regra depois de uma falha observada em teste. (b) Regra de compaction: preservar decisões tomadas, alternativas descartadas com motivo, restrições e perguntas em aberto; descartar saída bruta de ferramentas. (c) Se duas ferramentas parecem servir ao mesmo caso, o agente também vai hesitar: remover uma.
- **Ressalvas:** o número "30% de queda de acurácia" de blogs de terceiros não está na fonte: Não verificável, não usar.
- **Verificação:** página aberta; data, compaction, notas, subagentes, "altitude" e conjunto mínimo de ferramentas conferidos.

### V-03 — Claude Code best practices: verificar, explorar-planejar-codar, CLAUDE.md enxuto, revisão adversarial (origem authoritative R-03) — Classe A (8/10) · Lente: authoritative
- **Tipo:** checklist · claude-md-rule · workflow
- **Fonte:** https://code.claude.com/docs/en/best-practices · Anthropic (docs, atual: cita Claude Code v2.1.283)
- **Para que serve:** fluxo de mudança arquitetural em etapas, CLAUDE.md curto, revisor em contexto novo.
- **Técnicas-chave (todas conferidas no texto):** dar um critério executável de verificação e pedir evidência (saída de teste, comando e retorno); explorar, planejar, implementar, commitar; pular o plano se a diff cabe em uma frase; por linha do CLAUDE.md perguntar "remover isto faria o Claude errar?"; incluir "decisões de arquitetura específicas do projeto" e excluir descrição arquivo por arquivo; hooks para o que não pode falhar; subagente para investigação; revisor em contexto novo que reporta "lacunas, não preferências de estilo", e o aviso de que revisor pedido para achar lacunas sempre acha alguma (restringir a correção e requisitos).
- **Conteúdo reutilizável (reescrito):**
  - Bloco de CLAUDE.md de arquitetura: fronteiras de módulo e regra de dependência; ADRs vigentes com caminho; comando que valida fronteiras (teste de arquitetura, lint ou grep); definição de pronto. Nada de tutorial ou lista de arquivos.
  - Prompt de revisão adversarial: "Use um subagente para revisar a diff contra PLAN.md. Confirme que cada requisito foi implementado, que os casos de borda listados têm teste e que nada fora do escopo mudou. Reporte só lacunas que afetam correção ou os requisitos declarados; trate o resto como opcional e diga explicitamente quando não achar lacunas."
- **Ressalvas:** vale para Claude Code atual; recomendações mudam entre versões.
- **Verificação:** página aberta e lida inteira; os trechos acima conferidos.

### V-04 — Formato oficial de subagente e restrições de plugin (origem authoritative R-04) — Classe A (8/10) · Lente: authoritative
- **Tipo:** subagent · reference
- **Fonte:** https://code.claude.com/docs/en/sub-agents · Anthropic
- **Para que serve:** construir os subagentes do plugin (arquiteto, revisor de fronteiras, escritor de ADR).
- **Técnicas-chave (conferidas):** obrigatórios `name` (até 256 caracteres, único, sem `:`) e `description`; opcionais `tools`, `disallowedTools`, `model` (sonnet, opus, haiku, fable, ID completo ou inherit), `permissionMode`, `maxTurns`, `skills`, `memory`, `mcpServers`, `hooks`, `background`, `effort`, `isolation`, `color`. Nomes camelCase; campos desconhecidos são ignorados em silêncio. Prioridade de localização: política gerenciada, `--agents`, `.claude/agents/`, `~/.claude/agents/`, diretório `agents/` de plugin (menor). **Subagentes de plugin ignoram `hooks`, `mcpServers` e `permissionMode`**; hooks e MCP de plugin vão em `hooks/hooks.json` e `.mcp.json`. Definir `memory` liga Read/Write/Edit automaticamente.
- **Conteúdo reutilizável (reescrito):** Modelo de subagente de revisão: `tools: Read, Grep, Glob`; `maxTurns` definido (evita execução sem limite, ver V-45 e tw93 em rebaixados); `description` com gatilho ("use após mudança que cruze limites de módulo ou antes de aceitar um ADR"); corpo com papel de uma linha, passos numerados, formato de saída (severidade, arquivo:linha, problema, correção) e instrução "diga se não achou problemas". Não depender de `permissionMode` em agentes do plugin.
- **Ressalvas:** a página não traz exemplo de arquiteto; os exemplos desta lista são construção própria (Inferido). Restringir escrita a um diretório (por exemplo `docs/adr/`) não é possível só com `tools`: exige regras de permissão ou hook `PreToolUse` do projeto (Inferido, não testado).
- **Verificação:** página aberta (primeiros 100 mil caracteres de 108 mil); campos e restrições de plugin lidos na tabela.

### V-05 — Skills: estrutura, descrição e divulgação progressiva (origem authoritative R-06) — Classe A (8/10) · Lente: authoritative
- **Tipo:** skill · reference
- **Fonte:** https://code.claude.com/docs/en/skills · Anthropic
- **Técnicas-chave (conferidas):** frontmatter `name`, `description` (recomendada), `when_to_use`, `disable-model-invocation`, `user-invocable`, `allowed-tools`, `context: fork` com `agent`, `argument-hint`, `paths`, `license`, `metadata` etc.; `description`+`when_to_use` truncados em 1.536 caracteres na listagem (caso de uso principal primeiro); SKILL.md abaixo de 500 linhas (dica, não limite); fora do Claude Code só valem os campos da especificação Agent Skills, outros dão erro no empacotamento; nomes `anthropic-skills*` reservados.
- **Conteúdo reutilizável (reescrito):** Estrutura de skill de arquitetura: SKILL.md curto com gatilhos em PT-BR e EN na description; `references/adr.md`, `references/checklists.md`, `references/c4.md` carregados sob demanda; scripts só para validação determinística; fluxos que gravam arquivos usam `disable-model-invocation: true`. Se o plugin também for publicado fora do Claude Code, manter só campos da especificação.
- **Ressalvas:** o limite de 1.536 caracteres pode mudar; conferir na versão instalada.
- **Verificação:** página aberta; campos, 500 linhas e 1.536 caracteres confirmados.

### V-06 — Output styles: estilo "arquiteto" (origem authoritative R-05, github R-18, community R-16) — Classe B (7/10) · Lente: as três
- **Tipo:** system-prompt (estilo) · reference
- **Fonte:** https://code.claude.com/docs/en/output-styles · Anthropic
- **Técnicas-chave (conferidas):** frontmatter `name`, `description`, `keep-coding-instructions`, `force-for-plugin` (só em estilos de plugin; sobrescreve a escolha do usuário); estilos em `~/.claude/output-styles`, `.claude/output-styles` ou `output-styles/` dentro de plugin; estilo é instrução, não garantia (garantia = hook); `keep-coding-instructions` só tem efeito no prompt de sistema completo (variável `CLAUDE_CODE_SIMPLE_SYSTEM_PROMPT=0 seleciona o completo`); estilos não mudam subagentes, só a conversa principal e forks. A própria doc traz um exemplo "Diagrams first" com Mermaid e "menos de 15 nós".
- **Conteúdo reutilizável (reescrito):** Estilo "arquiteto" (opcional, nunca forçado): `keep-coding-instructions: true`; ao tratar de arquitetura, abrir com diagrama Mermaid (`flowchart TD` para estrutura, `sequenceDiagram` para fluxo) com até 15 nós, depois prosa com trade-offs; fechar com opções e pergunta quando a decisão é humana; listar o que não foi verificado.
- **Ressalvas:** não usar `force-for-plugin` sem decisão do usuário. Eficácia não medida.
- **Verificação:** página aberta e lida inteira.

### V-07 — skill-creator: avaliar e otimizar skills (origem authoritative R-07) — Classe A (9/10) · Prompt-score 82 · Lente: authoritative
- **Tipo:** skill · workflow · checklist
- **Fonte:** https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md (repositório https://github.com/anthropics/skills) · Anthropic
- **Sinais:** 180,2 mil estrelas; último commit 2026-10-09; **Apache-2.0** em `skills/skill-creator/LICENSE.txt` (citação literal permitida com atribuição; não foi necessária)
- **Prompt-score:** D1 4, D2 5, D3 5, D4 4, D5 4, D6 4, D7 5, D8 4, D9 2 (485 linhas), D10 3, D11 5 (modo sem subagentes), D12 4 = 49/60 → 82.
- **Técnicas-chave (conferidas):** capturar intenção; 2–3 prompts de teste realistas; rodar com a skill e baseline no mesmo turno; asserções verificáveis; generalizar a partir do feedback; 20 consultas de gatilho (8–10 que devem disparar, 8–10 limítrofes que não devem); otimização automática com divisão 60/40 e 3 execuções por consulta.
- **Conteúdo reutilizável (reescrito):** Checklist de avaliação de cada skill de arquitetura: (1) três cenários com decisão real (banco, fronteira, síncrono ou assíncrono); (2) rodar com e sem a skill; (3) asserções sobre a saída (contexto, decisão, alternativas, consequências negativas); (4) 20 consultas de gatilho, metade limítrofe; (5) revisar a description antes do corpo.
- **Ressalvas:** eficácia em skills de arquitetura não medida.
- **Verificação:** arquivo raw lido; LICENSE.txt do diretório lido (Apache-2.0); contagens 8–10/8–10 e 60/40 conferidas.

### V-08 — Sistema multiagente de pesquisa: delegação e escala (origem authoritative R-11, community R-17) — Classe A (8/10) · Lente: authoritative+community
- **Tipo:** pattern · checklist
- **Fonte:** https://www.anthropic.com/engineering/multi-agent-research-system · Anthropic · 13/06/2025
- **Técnicas-chave (conferidas):** agentes usam cerca de 4 vezes os tokens de um chat e multiagente cerca de 15 vezes; consulta simples = 1 agente com 3–10 chamadas, comparação = 2–4 subagentes com 10–15 chamadas, pesquisa complexa = mais de 10 com responsabilidades divididas; cada subagente precisa de objetivo, formato de saída, orientação de ferramentas e fontes e fronteiras de tarefa (sem isso houve duplicação e lacunas); multiagente serve mal quando há contexto compartilhado ou muita dependência, caso da maior parte da programação; ganho de 90,2% numa avaliação interna de pesquisa (Opus 4 líder + Sonnet 4 subagentes).
- **Conteúdo reutilizável (reescrito):** Modelo de briefing a subagente: Objetivo · Entrada (arquivos e decisões relevantes) · Formato de saída (achados com severidade e evidência) · Ferramentas e fontes permitidas · Fronteira (o que não fazer) · Critério de parada. Regra de escala para análise de arquitetura: mudança local = 1 revisor; mudança entre módulos = 2 a 4, um por fronteira; revisão do sistema inteiro = mais, só se o valor justificar o custo. Rubrica de juiz de ADR: completude, alternativas reais, consequências negativas declaradas, rastreio às fontes.
- **Ressalvas:** os números são do contexto de pesquisa, não de programação; os modelos citados são antigos.
- **Verificação:** página aberta; data, multiplicadores, regras de escala, 90,2% e requisitos de delegação conferidos.

### V-09 — feature-dev: fluxo de sete fases com gates humanos (origem authoritative R-08, github R-06, community R-14) — Classe A (8/10) · Prompt-score 67 · Lente: as três
- **Tipo:** command · workflow
- **Fonte:** https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/feature-dev/commands/feature-dev.md · Anthropic
- **Sinais:** repositório com 149,9 mil estrelas e último commit em 2026-10-09; **licença: todos os direitos reservados** (LICENSE.md). **Só destilar.**
- **Prompt-score:** D1 4, D2 3, D3 4, D4 5, D5 3, D6 3, D7 2, D8 4, D9 3, D10 2 (CRITICAL/DO NOT SKIP em caixa alta), D11 3, D12 4 = 40/60 → 67.
- **Técnicas-chave (conferidas):** fases Discovery, Exploration (2–3 agentes), Clarifying Questions (esperar respostas), Architecture Design (2–3 arquitetos com focos mudança mínima, arquitetura limpa, equilíbrio pragmático; apresentar recomendação e perguntar), Implementation ("DO NOT START WITHOUT USER APPROVAL"), Quality Review (3 revisores; perguntar o que corrigir), Summary. "Se o usuário disser 'o que achar melhor', dar recomendação e pedir confirmação explícita."
- **Conteúdo reutilizável (reescrito):** Máquina de estados para `/arquitetura:feature`: descobrir → explorar → perguntar [GATE-1: respostas] → desenhar opções [GATE-2: o humano escolhe] → plano detalhado [GATE-3: aprovação escrita] → implementar → revisar [GATE-4: decidir correções] → resumo. Em cada gate, a pergunta exata e a recomendação do agente; sem resposta, o agente não avança. Em tarefa pequena, usar só desenho + gate. Corrigir o ponto fraco do original: a fase de desenho não diz "aguardar" de forma explícita; o texto derivado deve dizer.
- **Ressalvas:** gasta muitos subagentes; usar a escala de V-08.
- **Verificação:** arquivo raw lido por inteiro; fases, gates e frase de aprovação conferidos; LICENSE.md lido.

### V-10 — code-architect: blueprint decisivo (origem authoritative R-09, github R-05) — Classe B (7/10) · Prompt-score 57 · Lente: authoritative+github
- **Tipo:** subagent
- **Fonte:** https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/feature-dev/agents/code-architect.md · Anthropic · licença: reservada (só destilar)
- **Prompt-score:** D1 3, D2 2, D3 3, D4 4, D5 1, D6 4, D7 1, D8 2, D9 5, D10 4, D11 1, D12 4 = 34/60 → 57 (curto e útil, sem verificação, sem exemplo, ferramentas de web liberadas).
- **Técnicas-chave:** analisar padrões do código antes de desenhar; **uma** abordagem decidida; saída fixa em **sete** blocos.
- **Conteúdo reutilizável (reescrito, para subir de 57 para ~80):**
  - Papel: arquiteto sênior, somente leitura (`Read, Grep, Glob`), `model: sonnet` ou `inherit`.
  - Passos: (1) levantar padrões, fronteiras e regras do CLAUDE.md com arquivo:linha; (2) listar restrições e requisitos não funcionais; (3) decidir uma abordagem e registrar de 1 a 3 alternativas descartadas com motivo (inclui "não mudar nada"); (4) detalhar componentes, mapa de arquivos, fluxo de dados, fases de build como checklist.
  - Saída: Padrões encontrados · Decisão e trade-offs · Alternativas descartadas · Componentes · Mapa de implementação · Fluxo de dados · Sequência de build · Riscos (erro, estado, teste, desempenho, segurança) · Suposições e o que falta verificar.
  - Regras: toda afirmação sobre o código cita arquivo:linha; sem evidência = marcar Suposição; se a decisão depender de preferência humana, devolver as opções e perguntar em vez de decidir; não editar arquivos.
- **Ressalvas:** a "abordagem única" do original pode esconder alternativas; por isso o campo de alternativas descartadas.
- **Verificação:** arquivo lido (34 linhas); sete blocos contados.

### V-11 — code-modernization: regras com prova e aprovação humana (origem authoritative R-10, community R-15) — Classe A (8/10) · Lente: authoritative+community
- **Tipo:** workflow · template
- **Fonte:** https://github.com/anthropics/claude-plugins-official/tree/main/plugins/code-modernization · Anthropic
- **Sinais:** repositório com 37,6 mil estrelas, Apache-2.0 (plugin também), último commit 2026-10-09
- **Técnicas-chave (conferidas):** comandos modernize, preflight, assess, map, extract-rules, review, brief, uplift/transform/reimagine, verify, harden, status; cartões `RULE-NNN` com Given/When/Then e citação arquivo:linha, reconferidos por um segundo agente, prioridade P0–P2; veredito por módulo PROVEN / PARTLY PROVEN / NOT PROVEN calculado por script; seis decisões humanas obrigatórias (respostas de preflight, regras suspeitas, aprovação do brief antes de construir, diferenças aceitas, assinatura da prova, aplicação do patch); código analisado tratado como entrada não confiável.
- **Conteúdo reutilizável (reescrito):** Cartão de regra: id, título, Dado, Quando, Então, fonte arquivo:linha, prioridade, status (confirmada, corrigida, suspeita). Veredito de equivalência por módulo com os três níveis; "NOT PROVEN bloqueia a migração". Nada é construído antes de o plano ser aprovado.
- **Ressalvas:** extração por modelo não é determinística (o plugin avisa; contagens variam entre execuções). **Telemetria ligada por padrão**: não adotar o plugin como dependência sem decisão do usuário; aqui só se destila o método.
- **Verificação:** página aberta; comandos, agentes, cartões, vereditos, seis gates, licença e telemetria conferidos.

### V-12 — Governança de ADR no Azure Well-Architected (origem authoritative R-14) — Classe A (8/10) · Lente: authoritative
- **Tipo:** checklist · governance
- **Fonte:** https://learn.microsoft.com/azure/well-architected/architect-role/architecture-decision-record · Microsoft · ms.date 2026-04-10, updated 2026-04-13
- **Técnicas-chave (conferidas):** só entram escolhas que afetam estrutura, atributos de qualidade ou são difíceis de reverter; log append-only que começa no início e pode ser gerado retroativamente em projeto existente; não editar registro aceito, criar um novo que o substitui com link; registrar problema com contexto, opções, decisão com trade-offs, **nível de confiança** e status; dividir decisão em fases curto/médio/longo; registros curtos, afirmativos e factuais, material de apoio por link; repositório aberto junto da documentação.
- **Conteúdo reutilizável (reescrito):** Critério de inclusão em uma pergunta: "afeta estrutura, atributo de qualidade ou custa caro reverter?". Checklist de governança: ADR no repositório do código; numeração sequencial; status visível; decisão de baixa confiança marcada com data de revisão; índice atualizado a cada supersessão; ADR retroativo permitido em legado.
- **Verificação:** página aberta e lida inteira.

### V-13 — Forma do ADR: Nygard e Fowler (origem authoritative R-12, R-13) — Classe B (7/10) · Lente: authoritative
- **Tipo:** template · reference
- **Fonte:** https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions (Michael Nygard, 15/11/2011) · https://www.martinfowler.com/bliki/ArchitectureDecisionRecord.html (Fowler, página datada de **24/03/2026**)
- **Técnicas-chave (conferidas):** Nygard: título nominal numerado, Status, Contexto neutro com forças em tensão, Decisão em voz ativa ("Vamos..."), Consequências positivas, negativas e neutras; registros de uma ou duas páginas, numeração sem reuso, substituídos e não apagados. Fowler: uma decisão por ADR, cerca de uma página, aceito não se edita (novo ADR substitui e o antigo vira superseded com link), alternativas sérias com prós e contras, consequências explícitas, grau de confiança e mudanças de contexto que obrigam a reavaliar.
- **Conteúdo reutilizável (reescrito):** Template consolidado `adr-NNNN-slug.md`: Título · Status (proposto, aceito, substituído por NNNN, descontinuado) · Data · Contexto · Decisão ("Vamos...") · Alternativas (prós e contras; inclui "não mudar nada") · Consequências (positivas, negativas, neutras) · Confiança (alta, média, baixa) · Gatilhos de reavaliação · Links. Ver V-12 para o critério de inclusão.
- **Ressalvas:** princípios, não formato obrigatório.
- **Verificação:** ambas as páginas abertas; datas, campos e regras de imutabilidade conferidos.

### V-14 — Agente ADR Generator (origem authoritative R-25, github R-01, community R-12) — Classe B (7/10) · Prompt-score 68 · Lente: as três
- **Tipo:** subagent · template
- **Fonte:** https://raw.githubusercontent.com/github/awesome-copilot/main/agents/adr-generator.agent.md · GitHub (awesome-copilot) · MIT, 39,9 mil estrelas, último commit 2026-10-09
- **Prompt-score:** D1 3, D2 2, D3 4, D4 5, D5 2, D6 5, D7 4, D8 3, D9 3, D10 3, D11 3, D12 4 = 41/60 → 68.
- **Técnicas-chave (conferidas):** pede título, contexto, decisão, alternativas e stakeholders e **pergunta se faltar**; próximo número de 4 dígitos em `/docs/adr/`; front matter (title, status, date, authors, tags, supersedes, superseded_by); consequências positivas e negativas com códigos (POS-001, NEG-001), pede 3 a 5 de cada; **inclui a opção "não fazer nada" quando aplicável**; checklist final; nome `adr-NNNN-slug.md`.
- **Conteúdo reutilizável (reescrito):** Subagente `adr-writer`: (1) exigir entradas mínimas e perguntar só o que falta; (2) ler a pasta e numerar; (3) preencher o template de V-13; (4) começar em `proposto`; (5) rodar checklist (número, nome do arquivo, data ISO, ≥1 consequência positiva e ≥1 negativa, ≥2 alternativas com motivo de rejeição); (6) pedir aprovação antes de gravar (ver V-16) e entregar caminho e resumo de um parágrafo. Aplicar o gatekeeper de V-15 antes de tudo.
- **Ressalvas:** os códigos POS/NEG/ALT são cosmética para parsing por máquina e podem ser omitidos; o original grava sem pedir confirmação.
- **Verificação:** arquivo lido por inteiro; "do nothing", 3 a 5 itens, numeração e checklist conferidos; MIT e estrelas conferidos.

### V-15 — Gatekeeper de dois estágios e revisão de ADR por diff (origem github R-08) — Classe B (5/10) · Prompt-score 78 · Lente: github
- **Tipo:** skill
- **Fonte:** https://raw.githubusercontent.com/wuersch/adlc/main/plugins/adlc/skills/adr/SKILL.md · wuersch (indivíduo) · MIT, 1 estrela, último commit 2026-08-01, "early alpha" declarado
- **Prompt-score:** D1 5, D2 5, D3 4, D4 4, D5 1, D6 3, D7 3, D8 4, D9 4, D10 5, D11 5, D12 4 = 47/60 → 78 (melhor prompt de ADR da lista, mas sem exemplos).
- **Técnicas-chave (conferidas):** estágio 1 (a decisão trata de como o sistema é construído?) e estágio 2 (estruturalmente significativa, cara de reverter ou transversal?); rejeição **roteada** (requisitos para a especificação, convenções para o CLAUDE.md, pequenas e reversíveis para lugar nenhum); reunir contexto antes de perguntar; entrevistar um tópico por vez; pendências viram `[NEEDS CLARIFICATION]`; começa em `draft`; supersessão atualiza o ADR antigo; ADR existente nunca é reescrito, só proposta de diff.
- **Conteúdo reutilizável (reescrito):** (a) Gatekeeper com tabela "rejeitado porque... → encaminhar para...". (b) Política: o ADR registra o que os humanos decidiram; o agente estrutura e não inventa; ponto não resolvido vira marcador. (c) Revisão por diff com impacto a jusante. O critério do estágio 2 coincide com o de V-12 (Microsoft), o que o torna sustentável apesar da baixa popularidade.
- **Ressalvas:** projeto muito jovem; não tratar como padrão de mercado; o script `check-docs.py` não foi lido nem executado.
- **Verificação:** arquivo lido por inteiro; MIT e commit conferidos; critério cruzado com V-12.

### V-16 — Skill de ADR que detecta momentos de decisão e pede consentimento (origem community R-13) — Classe B (6/10) · Prompt-score 73 · Lente: community
- **Tipo:** skill
- **Fonte:** https://raw.githubusercontent.com/affaan-m/everything-claude-code/main/skills/architecture-decision-records/SKILL.md · MIT, 276 mil estrelas (popularidade do repositório não prova esta skill), último commit 2026-10-10
- **Prompt-score:** D1 4, D2 3, D3 4, D4 4, D5 3, D6 4, D7 2, D8 5, D9 3, D10 4, D11 4, D12 4 = 44/60 → 73.
- **Técnicas-chave (conferidas):** gatilhos explícitos ("registre esta decisão") e implícitos (escolha de framework, banco ou API com razões); formato Nygard adaptado; **pergunta antes de criar o diretório e só grava depois de aprovação explícita; se recusar, descarta**; atualiza índice README; modo de leitura "por que escolhemos X?".
- **Segurança:** o arquivo foi varrido: sem execução de scripts, instalação ou busca remota. O instalador do pacote ECC não foi lido nem deve ser executado.
- **Conteúdo reutilizável (reescrito):** lista de gatilhos explícitos e implícitos; regra "mostrar rascunho, gravar só após aprovação"; fluxo de leitura quando não há ADRs ("nenhum ADR encontrado; quer começar?").
- **Verificação:** arquivo lido; varredura de segurança feita.

### V-17 — Agente de plano de implementação (origem authoritative R-26, github R-10) — Classe B (6/10) · Prompt-score 60 · Lente: authoritative+github
- **Tipo:** subagent · template
- **Fonte:** https://raw.githubusercontent.com/github/awesome-copilot/main/agents/implementation-plan.agent.md · GitHub · MIT
- **Prompt-score:** D1 3, D2 1, D3 4, D4 4, D5 3, D6 5, D7 4, D8 2, D9 3, D10 2, D11 2, D12 3 = 36/60 → 60. Problemas reais: o front matter lista ferramentas de edição e terminal de VS Code apesar de dizer "DO NOT make any code edits"; exige "zero ambiguidade" e "nenhuma decisão humana", o que contradiz o gate de aprovação.
- **Técnicas-chave:** modo de planejamento; plano autossuficiente; seções (requisitos e restrições, fases com tarefas, alternativas, dependências, arquivos, testes, riscos e suposições, referências); prefixos REQ-/TASK-/RISK-; critério de conclusão mensurável por fase; sem placeholders.
- **Conteúdo reutilizável (reescrito):** Template de plano de arquitetura em português: front matter (objetivo, versão, data, dono, status) · contexto e link para ADRs · requisitos com id (REQ, SEC, CON) · alternativas com a escolhida marcada · fases com critério de conclusão verificável · arquivos por fase · testes por requisito · riscos com mitigação · decisões que dependem do humano. Regra: o planejador só lê, o plano é aprovado antes da execução e **decisões humanas ficam explícitas, não "zero interpretação"**.
- **Verificação:** arquivo lido (161 linhas); contradição ferramentas × "não editar" confirmada.

### V-18 — Fluxo spec-driven com gate de confiança (origem authoritative R-27, github R-09) — Classe B (6/10) · Prompt-score 65 · Lente: authoritative+github
- **Tipo:** workflow · claude-md-rule
- **Fonte:** https://raw.githubusercontent.com/github/awesome-copilot/main/instructions/spec-driven-workflow-v1.instructions.md · MIT
- **Prompt-score:** D1 3, D2 2, D3 4, D4 5, D5 3, D6 4, D7 4, D8 3, D9 2 (323 linhas), D10 2, D11 4, D12 3 = 39/60 → 65.
- **Técnicas-chave (conferidas):** `requirements.md` em EARS ("WHEN ... THE SYSTEM SHALL ..."), `design.md`, `tasks.md`; seis fases; confiança >85% implementa, 66–85% PoC ou MVP, <66% pesquisa; protocolo de retrabalho (reanalisar, redesenhar, replanejar, tentar de novo, escalar).
- **Conteúdo reutilizável (reescrito):** Regra de CLAUDE.md: "mudança arquitetural começa por requisitos testáveis (EARS), design (interfaces, dados, erros) e tarefas; sem os três, não implementar." Gate de confiança com os limiares marcados como **Suposição configurável** (não há fonte primária para 85% e 66%); registrar a confiança no ADR (V-12 pede o mesmo campo). Sequência de escalada de bloqueio.
- **Ressalvas:** não define o que a especificação não deve conter (detalhe de implementação): o plugin deve definir.
- **Verificação:** arquivo lido; limiares e fases conferidos por busca.

### V-19 — Revisão de plano só leitura (plan-eng-review) (origem authoritative R-28, github R-02) — Classe B (6/10) · Prompt-score 70 · Lente: authoritative+github
- **Tipo:** workflow · checklist
- **Fonte:** https://raw.githubusercontent.com/garrytan/gstack/main/plan-eng-review/SKILL.md · Garry Tan · MIT, 135,7 mil estrelas, último commit 2026-10-09
- **Prompt-score:** D1 4, D2 3, D3 5, D4 4, D5 4, D6 5, D7 3, D8 4, D9 1, D10 2, D11 4, D12 3 = 42/60 → 70. O arquivo tem 705 linhas, chama binários `gstack-*`, grava em `~/.gstack` e registra telemetria.
- **Técnicas-chave (conferidas):** gate de alvo (diff, documento, caminho) antes de revisar; "Scope Challenge"; "Review the selected target. Do not build features..." (revisar, não construir sem autorização); cada decisão com opções limitadas a 4, ≥2 prós e ≥1 contra por opção, recomendação marcada.
- **Conteúdo reutilizável (reescrito):** Skill `design-review`: (1) confirmar o alvo; (2) desafiar o escopo: existe solução menor? (3) revisar arquitetura, fluxo de dados, bordas, testes e desempenho; (4) cada decisão: título D-n, problema em linguagem simples, o que acontece se errar, recomendação, 2 a 4 opções com prós e contras; (5) terminar com tabela de decisões pendentes. Não construir. As preferências de engenharia do gstack (abstração mínima, diff pequeno) entram como Suposição.
- **Ressalvas:** **não importar o arquivo**; só o processo. A "injeção" relatada pelos pesquisadores não foi achada no arquivo raw (provável artefato do sumarizador).
- **Verificação:** arquivo raw lido; limite de 4 opções e ≥2 prós/≥1 contra conferidos; varredura por "citation/disclaimer" sem resultado.

### V-20 — Pesquisar → planejar → anotar → implementar (origem github R-17, community R-06) — Classe B (5/10) · Lente: github+community
- **Tipo:** workflow · prompt
- **Fonte:** https://boristane.com/blog/how-i-use-claude-code/ (Boris Tane, 10/02/2026, sem licença visível) cruzado com https://code.claude.com/docs/en/best-practices (V-03)
- **Técnicas-chave (conferidas):** `research.md` em arquivo, `plan.md`, anotação humana de 1 a 6 rodadas com "don't implement yet", tarefas só depois de aprovado, direção errada = descartar mudanças (git) e reescopar. A documentação oficial recomenda explorar, planejar, implementar e permite entrevistar o usuário para escrever um SPEC.md.
- **Conteúdo reutilizável (reescrito, três comandos):**
  - `/arquitetura:pesquisar`: "Leia em profundidade o código relevante e grave `research.md` com o estado atual (cada afirmação com arquivo:linha), as dúvidas e os riscos. Não proponha mudanças."
  - `/arquitetura:planejar`: "Grave `plan.md` com abordagem, arquivos, trade-offs, alternativas descartadas e tarefas com checkbox. Não implemente."
  - `/arquitetura:anotar`: "Atualize o plano conforme as notas do usuário. Não implemente nada."
  - Regra: nenhum código antes da aprovação do plano; se a direção estiver errada, reverter e reescopar.
- **Ressalvas:** fonte única de praticante para os detalhes (1–6 rodadas); a estrutura é corroborada pela doc oficial.
- **Verificação:** blog aberto (data, fluxo e ausência de licença conferidos); doc oficial lida.

### V-21 — Modelo C4 (origem authoritative R-23, community R-04 em parte) — Classe B (6/10) · Lente: authoritative+community
- **Tipo:** reference · checklist
- **Fonte:** https://c4model.com/ · Simon Brown
- **Técnicas-chave (conferidas):** quatro níveis (contexto do sistema, contêiner, componente, código) e diagramas de suporte (panorama do sistema, dinâmico, implantação). A página inicial só lista; não descreve cada nível (confirmado). As descrições abaixo são síntese minha, corroboradas pelos agentes C4 de V-22 que citam as páginas de cada diagrama do site.
- **Conteúdo reutilizável (reescrito):** Contexto: o sistema como caixa, usuários e sistemas externos, sem tecnologia. Contêiner: aplicações e armazenamentos implantáveis, com tecnologia e protocolos. Componente: só para um contêiner por vez e só os que mudam. Código: sob demanda. Dinâmico: um caso de uso com ordem de chamadas. Implantação: infraestrutura. Cada diagrama com título, legenda e data; nunca componente em diagrama de contexto.
- **Verificação:** página aberta (níveis e suporte conferidos).

### V-22 — Agentes C4 da wshobson/agents (origem github R-12) — Classe B (6/10) · Prompt-score 60 · Lente: github
- **Tipo:** subagent (família c4-context, c4-container, c4-component, c4-code)
- **Fonte:** https://raw.githubusercontent.com/wshobson/agents/main/plugins/c4-architecture/agents/c4-context.md (e `c4-container.md`) · MIT, 40,3 mil estrelas, último commit 2026-10-04
- **Prompt-score (c4-context):** D1 4, D2 3, D3 3, D4 4, D5 3, D6 4, D7 1, D8 3, D9 2, D10 3, D11 2, D12 4 = 36/60 → 60 (listas de "capacidades" infladas, sem verificação).
- **Técnicas-chave (conferidas):** contexto sem tecnologia nem protocolo ("Avoid showing technologies, protocols"); contêiner "mostra escolhas de tecnologia de alto nível" e documenta interfaces como API; modelo `sonnet`; diagrama Mermaid `C4Context`. Os arquivos `c4-container.md` e `c4-component.md` existem (HTTP 200); `c4-component` e `c4-code` não foram lidos.
- **Conteúdo reutilizável (reescrito):** template do nível de contexto (visão curta e longa, personas humanas e programáticas, features, jornadas, sistemas externos, diagrama, links) e do nível de contêiner (contêineres, tecnologia, interfaces como API). Regras: tecnologia só no nível de contêiner; texto compreensível por não técnicos no contexto.
- **Ressalvas:** não afirmar que componente e código seguem o mesmo template (não lidos). Corrige a lacuna anterior ("404 do README"): os arquivos de agente existem, só o README do plugin não abre.
- **Verificação:** dois arquivos lidos; listagem de nomes e códigos HTTP conferidos.

### V-23 — Regras de Mermaid para diagramas de arquitetura (origem github R-03, community R-03) — Classe B (6/10) · Prompt-score 70 · Lente: github+community
- **Tipo:** rule · reference
- **Fonte:** https://raw.githubusercontent.com/garrytan/gstack/main/diagram/SKILL.md (MIT) · cruzado com o exemplo "Diagrams first" de https://code.claude.com/docs/en/output-styles ("menos de 15 nós") e com a lição do Show HN Composer (https://news.ycombinator.com/item?id=47622289, 8 pontos; críticas a diagramas ilegíveis e sem níveis)
- **Prompt-score (gstack diagram):** D1 4, D2 3, D3 4, D4 4, D5 3, D6 4, D7 4, D8 3, D9 2, D10 3, D11 4, D12 4 = 42/60 → 70. O arquivo é acoplado a bundle local de renderização, `bun` e scripts.
- **Técnicas-chave (conferidas):** `.mmd` como fonte única; 5–15 nós; rótulos curtos e detalhe nas arestas; `graph LR` para fluxos e `TD` para hierarquias; erro de parse bloqueia a entrega.
- **Conteúdo reutilizável (reescrito):** "Mermaid é a fonte. Um nível de abstração por diagrama. De 5 a 15 nós; passou disso, dividir e dizer por quê. LR para pipelines, TD para hierarquias, sequenceDiagram para chamadas. Rótulo curto no nó, detalhe na aresta. Se o Mermaid não parseia, a entrega fica bloqueada até corrigir." Não executar scripts de renderização de terceiros.
- **Verificação:** arquivo lido; limites e direções conferidos; as duas fontes cruzadas abertas.

### V-24 — Camadas com lista de imports permitidos, verificadas por grep (origem authoritative R-29, github R-04, community R-20/R-11) — Classe B (6/10) · Prompt-score 63 · Lente: as três
- **Tipo:** claude-md-rule · checklist
- **Fonte:** https://raw.githubusercontent.com/PatrickJS/awesome-cursorrules/main/rules/fastapi-production-architecture-cursorrules-prompt-file.mdc · CC0-1.0, 40,9 mil estrelas, **último commit 2026-05-30** (mais de 4 meses sem atividade)
- **Prompt-score:** D1 3, D2 2, D3 5, D4 4, D5 5 (pares GOOD/BAD), D6 2, D7 4, D8 2, D9 3, D10 2 (FORBIDDEN/NOT), D11 2, D12 4 = 38/60 → 63.
- **Técnicas-chave (conferidas):** quatro camadas Router → Service → Repository → ORM/HTTP, imports só para baixo; handler com ≤10 linhas executáveis; serviço recebe dependências por Protocol; adaptador devolve resultado tipado com `retryable` e `code`; um cliente HTTP por provedor (bulkhead); chave de idempotência em efeito colateral; escritor único com verificação por grep; faixas de tamanho de arquivo (verde até 399 linhas, amarelo 400–599, vermelho 600+) são opinião.
- **Conteúdo reutilizável (reescrito):** Tabela "camada → pode importar → não pode importar" por projeto; verificação por grep ou por teste de arquitetura no CI; regra de CLAUDE.md em forma positiva com gatilho de parada: "Domínio não importa adaptadores externos; se parecer necessário, pare e registre a dúvida." Limites de linhas e de handler: Suposição configurável. A corroboração de praticante (r/ClaudeAI via espelho, V-44) diz que listas longas de "não use" falham e que ponteiros para arquivos de exemplo funcionam melhor.
- **Ressalvas:** exemplo de Python/FastAPI; o nome do padrão (hexagonal, clean) não aparece; ver V-25.
- **Verificação:** arquivo lido; trechos, limites e CC0 conferidos.

### V-25 — Arquitetura hexagonal (portas e adaptadores) — descoberto pelo validador — Classe B (6/10) · Lente: validador (lacuna das três lentes)
- **Tipo:** reference · pattern
- **Fonte:** https://alistair.cockburn.us/hexagonal-architecture/ · Alistair Cockburn · texto de 04/09/2005 (relatório técnico), rodapé de 2022
- **Técnicas-chave (conferidas):** a aplicação é dirigida por usuários, programas, testes ou lotes e desenvolvida sem banco e sem UI; adaptadores traduzem eventos externos e chamadas de saída; dependências apontam para dentro (código do interior não vaza para o exterior); mock é um adaptador em memória; portas primárias (dirigem a aplicação) e secundárias (dirigidas por ela); crítica ao diagrama em camadas porque a lógica atravessa as linhas.
- **Conteúdo reutilizável (reescrito):** Perguntas de revisão: (1) o núcleo roda em teste sem banco nem rede? (2) cada tecnologia externa fica atrás de uma porta com um adaptador? (3) algum import do núcleo aponta para fora? (4) as portas são simétricas para entrada e saída? Complementa V-24 com o princípio por trás da regra de camadas.
- **Ressalvas:** fonte de 2005, atemporal; sem fonte sobre Clean Architecture (lacuna aberta).
- **Verificação:** página aberta; data e conceitos conferidos.

### V-26 — DDD: bounded context e agregado (origem authoritative R-24; agregado descoberto pelo validador) — Classe B (5/10) · Lente: authoritative+validador
- **Tipo:** reference · pattern
- **Fonte:** https://martinfowler.com/bliki/BoundedContext.html (15/01/2014) e https://martinfowler.com/bliki/DDD_Aggregate.html (23/04/2013)
- **Técnicas-chave (conferidas):** modelo único para o negócio todo não funciona; cada contexto tem modelo e linguagem próprios e mudança de linguagem costuma marcar a fronteira; relações entre contextos devem ser nomeadas e documentadas num context map. Agregado: grupo de objetos tratado como unidade, referência de fora só ao agregado raiz, transação não atravessa agregados, carregar e gravar o agregado inteiro.
- **Conteúdo reutilizável (reescrito):** Perguntas para mapear contextos: termos com sentido diferente entre áreas; dono de cada definição; relação entre contextos; o que cruza a fronteira e exige tradução. Regras de agregado como checklist de revisão: um raiz, referência por identidade, uma transação por agregado, consistência entre agregados é eventual (ver V-34 e V-35).
- **Ressalvas:** a relação com microsserviços é Inferida (a página não trata disso); Evans e Vernon continuam sem fonte primária (lacuna). Bulkhead (V-32) cita que partições devem alinhar com bounded contexts no DDD tático.
- **Verificação:** ambas as páginas abertas.

### V-27 — Monólito primeiro e quando extrair serviço (origem authoritative R-21, community R-19) — Classe B (6/10) · Lente: authoritative+community
- **Tipo:** reference · checklist
- **Fonte:** https://martinfowler.com/bliki/MonolithFirst.html (03/06/2015) · apoio: https://www.encore.dev/articles/monolith-vs-microservices (Ivan Cernja, 20/07/2026, **fornecedor de framework**, sem limiares numéricos)
- **Técnicas-chave (conferidas):** microsserviços têm custo operacional que desacelera equipe pequena; a maioria dos casos de sucesso começou como monólito; fronteiras certas são difíceis no início e mover funcionalidade entre serviços custa mais que dentro do monólito; extrair só com motivo nomeado (escala diferente, isolamento, times bloqueados no deploy).
- **Conteúdo reutilizável (reescrito):** Prompt de decisão: "Antes de propor dividir, responda: qual módulo seria o primeiro a extrair e por quê; que métrica ou restrição justifica; qual o custo de rede, observabilidade e dados; há times com ciclos de entrega diferentes? Se não houver resposta para a primeira pergunta, recomende monólito modular com fronteiras internas verificadas (V-28)." O teste "nomeie o primeiro serviço" é do artigo do fornecedor; o resto é de Fowler.
- **Ressalvas:** posição argumentada, não teste; a tese do Encore de que agentes raciocinam melhor sobre código inteiro é não medida.
- **Verificação:** Fowler e Encore abertos; data e ausência de limiares numéricos conferidas.

### V-28 — Skill de monólito modular com fronteiras aplicadas por CI (origem github R-15) — Classe B (5/10) · Prompt-score 62 · Lente: github
- **Tipo:** skill · checklist
- **Fonte:** https://raw.githubusercontent.com/athola/claude-night-market/master/plugins/archetypes/skills/architecture-paradigm-modular-monolith/SKILL.md · MIT, 341 estrelas, último commit 2026-10-02
- **Prompt-score:** D1 3, D2 3, D3 4, D4 4, D5 0, D6 3, D7 4, D8 3, D9 3 (seções genéricas de troubleshooting), D10 4, D11 2, D12 4 = 37/60 → 62.
- **Técnicas-chave (conferidas):** módulos por capacidade de negócio ou bounded context; encapsular internos; expor fachadas, APIs ou eventos; proibir acesso direto a tabelas de outro módulo; testes de aptidão que quebram o build; acompanhar acoplamento de mudança; critérios de saída (ADR de fronteiras, CI falha em import proibido, ≥1 caso de violação documentado). Limiar de 50% de acoplamento de mudança é escolha do autor: **Suposição**.
- **Conteúdo reutilizável (reescrito):** Checklist de fronteira de módulo: ADR com mapa de módulos, regras de código compartilhado e condições de extração; contrato formal por interação; acesso a tabela alheia proibido (propriedade de esquema); teste de dependência no CI; um caso de violação documentado; métrica de acoplamento de mudança com limiar configurável.
- **Verificação:** arquivo lido (88 linhas); critérios e limiar conferidos. A seção "Concrete Components" cita ferramentas só como vocabulário (não são dependências).

### V-29 — Strangler Fig (origem authoritative R-22) — Classe B (6/10) · Lente: authoritative
- **Tipo:** workflow · checklist
- **Fonte:** https://www.martinfowler.com/bliki/StranglerFigApplication.html · Fowler · 22/08/2024
- **Técnicas-chave (conferidas):** resultados acordados e revisados; achar ou criar seams; começar por componentes pequenos e de baixo risco; arquitetura transitória vale o custo. A página **não** trata de interceptação de chamadas nem de migração de dados (confirmado).
- **Conteúdo reutilizável (reescrito):** Plano strangler: (1) resultado mensurável por etapa; (2) seams candidatos com risco; (3) primeira fatia pequena; (4) roteamento de tráfego com volta possível (Inferido: fachada ou proxy); (5) código de convivência marcado com data de remoção; (6) critério de desligamento do legado; (7) plano de dados da fatia (lacuna da fonte).
- **Verificação:** página aberta.

### V-30 — Circuit Breaker (origem authoritative R-15) — Classe A (8/10) · Lente: authoritative
- **Tipo:** pattern · checklist
- **Fonte:** https://learn.microsoft.com/azure/architecture/patterns/circuit-breaker · Microsoft · ms.date 2025-02-05, updated 2026-09-26
- **Técnicas-chave (conferidas):** estados fechado, aberto e meio-aberto; contador de falhas baseado em janela de tempo; chamadas de teste limitadas no meio-aberto; um erro no meio-aberto reabre; combina com Retry, que deve parar quando o breaker indica falha não transitória; timeout crescente; reset manual e forçar abertura; um breaker por provedor ou shard; 429 e 503 podem abrir de imediato; evento a cada transição; fallback com valor padrão ou cache. **Não indicado** para estado local em memória, para substituir tratamento de exceção de negócio, em arquiteturas orientadas a mensagens com dead-letter queue (isolamento e retry já embutidos) e quando a recuperação é feita pela plataforma (service mesh, health checks). Ajuste adaptativo com IA aparece como opção.
- **Conteúdo reutilizável (reescrito):** Checklist: (1) limiar de falhas e janela; (2) tempo aberto e crescimento; (3) chamadas de teste; (4) fallback definido; (5) evento e alerta por transição; (6) reset manual; (7) um breaker por dependência ou shard; (8) o timeout do chamador é curto? (um timeout longo anula a proteção); (9) é cabível aqui, ou o broker/mesh já cobre?
- **Verificação:** página aberta e lida inteira; datas conferidas.

### V-31 — Retry (origem authoritative R-16) — Classe B (7/10) · Lente: authoritative
- **Tipo:** pattern · checklist
- **Fonte:** https://learn.microsoft.com/azure/architecture/patterns/retry · Microsoft · ms.date 2024-07-18, updated 2025-12-09
- **Técnicas-chave (conferidas):** estratégias cancelar, repetir já, repetir com atraso; atraso incremental ou exponencial e espalhado entre instâncias; logar tentativas iniciais como informação e só a última como erro; verificar retry embutido no SDK; idempotência antes de repetir; uma só camada faz retry (a mais baixa falha rápido); retry não substitui escala. **Jitter não é citado na página**: a recomendação de variação aleatória vem de V-41 (resilience-failure) e de prática comum (Inferido; fonte primária sugerida em Lacunas).
- **Conteúdo reutilizável (reescrito):** Checklist: falha transitória? operação idempotente? SDK já repete? limite de tentativas e atraso exponencial com variação aleatória; só uma camada repete; logs corretos; erro recorrente abre discussão de capacidade.
- **Verificação:** página aberta; ausência de "jitter" confirmada.

### V-32 — Bulkhead — descoberto pelo validador — Classe A (8/10) · Lente: validador (lacuna authoritative)
- **Tipo:** pattern · checklist
- **Fonte:** https://learn.microsoft.com/azure/architecture/patterns/bulkhead · Microsoft · ms.date 2026-03-19, updated 2026-09-19
- **Técnicas-chave (conferidas):** partições de instâncias por carga de consumidor e requisitos de disponibilidade; pools de conexão ou threads por serviço chamado; isolamento por processos, contêineres ou filas; combinar com retry, circuit breaker e throttling; alinhar partições a bounded contexts; usar controles da plataforma (limites de API Management, RU do Cosmos DB, limites de AKS) em vez de recriar no código; monitorar SLA por partição; quando não usar: uso menos eficiente de recursos é inaceitável ou a complexidade não se justifica; cargas de IA/inferência pedem bulkheads rígidos por cotas.
- **Conteúdo reutilizável (reescrito):** Checklist: (1) quais dependências podem esgotar um recurso compartilhado? (2) pool ou fila separada por dependência crítica; (3) tamanho de cada pool com número medido; (4) a plataforma já oferece o limite?; (5) alerta por pool; (6) custo de menor utilização aceito.
- **Verificação:** página aberta e lida inteira.

### V-33 — Idempotent Consumer (origem authoritative R-17) — Classe A (8/10) · Lente: authoritative
- **Tipo:** pattern · checklist
- **Fonte:** https://learn.microsoft.com/azure/architecture/patterns/idempotent-consumer · Microsoft · ms.date 2026-08-13, updated 2026-09-05 (a página traz `ai-usage: ai-assisted`, informação de transparência)
- **Técnicas-chave (conferidas):** exactly-once ponta a ponta é impraticável; at-least-once mais consumidor que ignora duplicata = efetivamente uma vez; chave estável (MessageId ou chave de negócio, nunca CorrelationId nem ID de entrega); chave composta com identidade do consumidor quando vários consumidores compartilham a tabela; marcador e efeito na mesma transação (Inbox); restrição de unicidade como árbitro de concorrência; estados em andamento e concluído para efeitos externos; retenção maior que a janela de redelivery, inclusive reenvios de dead-letter; preferir operações naturalmente idempotentes; detecção do broker não substitui o consumidor; propagar a chave aos serviços chamados; métrica de duplicatas.
- **Conteúdo reutilizável (reescrito):** Checklist de 8 itens: chave estável · operação naturalmente idempotente? · marcador e efeito na mesma transação · unicidade no banco · em andamento/concluído para efeito externo · TTL maior que redelivery e DLQ · métrica e chave nos logs · ordem tratada por sessão ou versão quando importa.
- **Verificação:** página aberta e lida inteira.

### V-34 — Transactional Outbox (origem authoritative R-18) — Classe A (8/10) · Lente: authoritative
- **Tipo:** pattern · checklist
- **Fonte:** https://learn.microsoft.com/azure/architecture/databases/guide/transactional-out-box-cosmos · Microsoft · ms.date 2026-02-23, updated 2026-09-25
- **Técnicas-chave (conferidas):** resolver o dual write gravando estado e evento na mesma transação; processo separado publica e marca processado; em SQL relacional é direto, mas a ordem dos eventos precisa ser preservada; em Cosmos DB o lote transacional vale numa única partição lógica (evento e entidade no mesmo contêiner e partição), change feed no lugar da coluna "processado", ordem por partição e `SessionId` no Service Bus, deduplicação no broker por MessageId, TTL de vários dias (10 no exemplo); o exemplo **não é código de produção** (limitações de multithreading); bibliotecas como NServiceBus e MassTransit trazem outbox pronto.
- **Conteúdo reutilizável (reescrito, item 7 corrigido):** Checklist: estado e evento na mesma transação · evento com ID estável · publicador assíncrono com retomada · ordem por agregado · TTL com margem de dias · consumidor idempotente (V-33) · **evento persistido no mesmo contêiner/partição ou tabela da transação do estado** (a versão dos pesquisadores dizia o oposto).
- **Verificação:** página aberta e lida inteira.

### V-35 — Saga (origem authoritative R-19) — Classe A (8/10) · Lente: authoritative
- **Tipo:** pattern · checklist
- **Fonte:** https://learn.microsoft.com/azure/architecture/patterns/saga · Microsoft · ms.date 2025-02-25, updated 2026-06-03
- **Técnicas-chave (conferidas):** transações locais com compensações; compensáveis, pivô e retentáveis (idempotentes) depois do pivô; coreografia (simples, difícil de rastrear e testar, risco de dependência cíclica) versus orquestração (fluxos complexos, ponto único de falha); anomalias (atualização perdida, leitura suja, leitura não repetível) e contramedidas (bloqueio semântico, atualizações comutativas, visão pessimista, reler valores, versionar, concorrência por risco); compensação pode falhar e deixar inconsistência. Não usar com transações fortemente acopladas, compensação em participantes anteriores ou dependências cíclicas.
- **Conteúdo reutilizável (reescrito):** Checklist: passos com compensação · pivô marcado · passos após o pivô idempotentes · coreografia só com poucos serviços, senão orquestração · bloqueio semântico em registros em edição · monitorar o estado da saga · plano para compensação que falha.
- **Verificação:** página aberta e lida inteira.

### V-36 — CQRS (origem authoritative R-20) — Classe A (8/10) · Lente: authoritative
- **Tipo:** pattern · checklist
- **Fonte:** https://learn.microsoft.com/azure/architecture/patterns/cqrs · Microsoft · ms.date 2025-02-20, updated 2026-09-25
- **Técnicas-chave (conferidas):** comandos são tarefas de negócio, não atualizações de campo; consultas retornam DTOs sem lógica de domínio; separar primeiro no mesmo banco, depois em bancos diferentes sincronizados por eventos com **outbox e consumidor idempotente**; consistência eventual e dado obsoleto na tela; complexidade significativa, principalmente com event sourcing; usar com colaboração intensa, UI orientada a tarefas, ajuste fino de leitura e escrita, times separados; não usar com domínio simples ou CRUD suficiente.
- **Conteúdo reutilizável (reescrito):** Checklist de decisão: (1) leitura e escrita têm escala diferente? (2) regras justificam um modelo de escrita próprio? (3) a interface é orientada a tarefas? (4) o time aceita consistência eventual e dado obsoleto? (5) há mecanismo de sincronização (V-34, V-33)? Se (1) e (2) forem "não", não aplicar.
- **Verificação:** página aberta e lida inteira.

### V-37 — Event Sourcing — descoberto pelo validador — Classe A (8/10) · Lente: validador (lacuna authoritative)
- **Tipo:** pattern · checklist
- **Fonte:** https://learn.microsoft.com/azure/architecture/patterns/event-sourcing · Microsoft · ms.date 2026-03-27, updated 2026-09-25
- **Técnicas-chave (conferidas):** a página abre com aviso de que o padrão é complexo, caro de adotar ou abandonar e raramente necessário; eventos que capturam intenção, não só estado resultante; fluxo por entidade e rehidratação com snapshots (otimização, não substituto); versionamento (deserialização tolerante, versão no evento, upcasting; migração in-place só como último recurso); ordem e concorrência otimista por fluxo; evento store não é broker (Kafka não substitui); handlers idempotentes; atenção a laços circulares; testes given-when-then; conflito com direito ao esquecimento (dados pessoais fora do evento ou crypto-shredding); adotar seletivamente (ledger de pagamentos sim, perfil de usuário não).
- **Conteúdo reutilizável (reescrito):** Checklist: o benefício (auditoria, reconstrução histórica) justifica o custo? · eventos de intenção · estratégia de evolução de esquema antes do primeiro evento · concorrência otimista · snapshots quando o fluxo cresce · dados pessoais fora do log · handlers idempotentes (V-33) · aplicar só na parte do sistema que precisa. Complementa V-36.
- **Verificação:** página aberta e lida inteira.

### V-38 — Cache-Aside e o fecho de lacuna de cache — descoberto pelo validador — Classe A (8/10) · Lente: validador (lacuna total das lentes)
- **Tipo:** pattern · checklist
- **Fonte:** https://learn.microsoft.com/azure/architecture/patterns/cache-aside · Microsoft · ms.date 2025-09-11, updated 2025-12-09 · reforço de prática: V-41 (skill caching)
- **Técnicas-chave (conferidas):** carregar sob demanda; na escrita, gravar no banco e **depois** invalidar o item no cache (a ordem importa); não garante consistência; expiração coerente com o padrão de acesso; priming; cache local por instância diverge; evitar dado sensível em cache compartilhado; não usar quando o conjunto é estático ou a taxa de acerto é baixa; semantic caching só quando seguro.
- **Conteúdo reutilizável (reescrito):** Checklist: um número mostra que a leitura é o gargalo? · orçamento de obsolescência declarado · estratégia de leitura e escrita (cache-aside é o padrão; write-through quando leitura após escrita precisa estar fresca) · TTL com variação · proteção contra stampede e chave inexistente · aquecimento após deploy · métricas de hit rate, evictions e QPS da origem. A parte de stampede, penetração e hot key vem de V-41 e deve ser conferida contra uma fonte primária (lacuna).
- **Verificação:** página aberta e lida inteira.

### V-39 — Web API design (Azure Architecture Center) — descoberto pelo validador — Classe B (7/10) · Lente: validador (lacuna API)
- **Tipo:** reference · checklist
- **Fonte:** https://learn.microsoft.com/azure/architecture/best-practices/api-design · Microsoft · ms.date 2025-03-27, updated 2026-06-03
- **Técnicas-chave (títulos e seções conferidos; leitura parcial por busca de tópicos):** URIs de recursos e convenções de nome; semântica de métodos HTTP e idempotência de PUT; tipos MIME; operações assíncronas com 202 Accepted; paginação e filtragem (a página usa `limit` e `offset`); respostas parciais; HATEOAS (sem padrão geral); versionamento por URI, query string, cabeçalho ou tipo de mídia com as implicações de cache; APIs multi-tenant; trace context; modelo de maturidade; OpenAPI.
- **Conteúdo reutilizável (reescrito):** Checklist de revisão de API: recursos e nomes · métodos e status · assíncrono com 202 · paginação (cursor para dados que mudam muito, ver V-41) · filtros · versão e depreciação · erro padronizado (RFC 9457) · idempotência · concorrência (ETag) · autorização por objeto · tracing.
- **Ressalvas:** não li a página inteira; não afirmo o que ela diz sobre RFC 9457 (a busca por "9457"/"7807" não retornou ocorrência).
- **Verificação:** página aberta; estrutura por títulos e seções conferida por busca.

### V-40 — api-designer (origem github R-14) — Classe B (6/10) · Prompt-score 65 · Lente: github
- **Tipo:** skill
- **Fonte:** https://raw.githubusercontent.com/Jeffallan/claude-skills/main/skills/api-designer/SKILL.md · MIT, **11,8 mil estrelas**, último commit 2026-10-03
- **Prompt-score:** D1 5, D2 2, D3 4, D4 4, D5 4, D6 5, D7 4, D8 2, D9 3, D10 2 (MUST DO/MUST NOT DO), D11 2, D12 2 (RFC 7807 obsoleta) = 39/60 → 65.
- **Técnicas-chave (conferidas):** seis passos (analisar domínio, modelar recursos, endpoints, contrato OpenAPI 3.1, simular, evolução); listas MUST/MUST NOT; modelos de endpoint e de erro; valida com `npx @redocly/cli lint` e mock com `npx @stoplight/prism-cli`.
- **Conteúdo reutilizável (reescrito):** checklist "deve/não deve" em linguagem positiva; modelo de erro **RFC 9457** (Problem Details, obsoleta a RFC 7807, julho de 2023) com `type`, `title`, `status`, `detail`, `instance` e lista de erros por campo; "o contrato passa por lint antes da entrega" como critério de saída.
- **Ressalvas:** os comandos `npx` baixam e executam pacotes de terceiros: no plugin, apenas documentar para o usuário habilitar; não executar.
- **Verificação:** arquivo lido; MIT, estrelas e commit conferidos; RFC 9457 confirmado no rfc-editor.org.

### V-41 — system-design-skills (proyecto26): blocos de decisão para cache, consistência, resiliência, API e escala (origem github R-07) — Classe B (5/10, sobe de C) · Prompt-score 87 (caching) · Lente: github
- **Tipo:** skill-pack · workflow
- **Fonte:** https://github.com/proyecto26/system-design-skills (README e `skills/<bloco>/SKILL.md` lidos) · MIT, 85 estrelas, último commit 2026-06-02; declara trigger evals (~20 consultas) e uma primeira rodada com e sem skill em `meta/evals/`
- **Prompt-score (skill caching):** D1 5, D2 5, D3 5, D4 5, D5 3, D6 4, D7 4, D8 4, D9 3, D10 5, D11 4, D12 5 = 52/60 → 87. Estrutura repetida nas skills: Quando usar · Quando NÃO usar · Esclarecer primeiro · Opções · Trade-offs (tabela) · Comportamento sob estresse · Como aplicar · Faça e não faça · Números que importam · Esboço de interface.
- **Técnicas-chave (conferidas nos arquivos):** 22 skills em camadas L0–L7 (enquadramento, borda, serviços, estado, assíncrono, correção, operação, crescimento); laço de seis passos clarificar, estimar, desenhar, trade-offs, modos de falha, iterar; cache: cache-aside como padrão, write-through/back/around, LRU/LFU/TTL, stampede, penetração, hot key, cold cache e "não adicione cache antes de um número mostrar que a leitura é o gargalo"; resiliência: retry com backoff e jitter e orçamento, circuit breaker, bulkhead, timeouts; consistência: CAP/PACELC, quórum, consenso, "não alcance consistência forte antes de uma invariante exigir"; API: cursor por padrão, `Idempotency-Key`, versionamento aditivo, envelope de erro estável; decomposição: quando NÃO dividir.
- **Conteúdo reutilizável (reescrito):** (a) estrutura de skill de decisão acima como molde para as skills do plugin; (b) checklist de seis fases com taxonomia L0–L7 para revisão de design; (c) conta de ordem de grandeza (QPS, armazenamento, banda, servidores) feita **no texto da resposta**, sem executar o script `botec.py`.
- **Ressalvas:** repositório pequeno e jovem; os números (100 mil a 1 milhão de QPS por nó de cache etc.) são regras de bolso: Suposição. Cruzar com V-30, V-31, V-32, V-33, V-38 (todas Microsoft) antes de virar regra. Não executar scripts nem instalar.
- **Verificação:** README e cinco skills lidas; MIT, estrelas e commit conferidos; segurança: sem comandos perigosos (só um script stdlib citado).

### V-42 — backend-architect (origem github R-11) — Classe B (7/10 pela fonte; conteúdo só como referência) · Prompt-score 53 · Lente: github
- **Tipo:** subagent (referência)
- **Fonte:** https://raw.githubusercontent.com/wshobson/agents/main/plugins/backend-development/agents/backend-architect.md · MIT, 40,3 mil estrelas
- **Prompt-score:** D1 3, D2 2, D3 3, D4 4, D5 3, D6 4, D7 1, D8 2, D9 1 (309 linhas, listas de capacidades), D10 3, D11 2, D12 4 = 32/60 → 53.
- **Técnicas-chave (conferidas):** "Response Approach" de **dez** passos (requisitos; fronteiras por DDD; contratos; comunicação síncrona ou assíncrona; resiliência; observabilidade; segurança; desempenho; testes; documentação com ADR); lista de entregáveis; seção "Key Distinctions" que delega banco, nuvem, auditoria de segurança e desempenho a outros agentes.
- **Conteúdo reutilizável (reescrito):** só os dez passos e os entregáveis, em um checklist de "design de serviço" de uma página, com a regra de delegação como cabeçalho; descartar as listas de produtos e tecnologias. Acrescentar o que falta: autoverificação e marcação de suposições.
- **Verificação:** arquivo lido; os dez passos contados.

### V-43 — Crítica a "Claude como arquiteto que concorda" (origem community R-01) — Classe B (5/10, sobe de C) · Lente: community
- **Tipo:** pattern · anti-pattern
- **Fonte:** https://www.hollandtech.net/claude-is-not-your-architect/ (Charlie Holland, 06/04/2026) · thread do HN https://news.ycombinator.com/item?id=48259784 (275 pontos, 190 comentários, 24/05/2026; os comentários divergem: alguns dizem que o Claude sabe dizer "não" se o prompt pede)
- **Técnicas-chave (verificadas no ensaio):** o modelo tende a concordar e a produzir desenhos genéricos que ignoram habilidades, restrições e realidade de produção do time; regra "engenheiros projetam, agentes implementam"; desafiar com "existe opção mais simples?"; tratar sugestão como a de um júnior confiante; manter dono humano nomeado em cada decisão; aprovação superficial é um risco.
- **Conteúdo reutilizável (reescrito, marcado Inferido onde é construção minha):** Prompt do "arquiteto cético": antes de propor, faça até cinco perguntas sobre escala, consistência, time e modos de falha; mostre a opção mais simples que atende; diga o que você **não** recomenda construir e por quê (**Inferido**, não vem do ensaio); termine com a decisão pendente e o dono humano. Pré-mortem opcional: "suponha que falhou em 12 meses; três causas e o sinal precoce de cada" (**Inferido**).
- **Ressalvas:** ensaio de opinião, sem medição.
- **Verificação:** ensaio aberto; Algolia consultado (existem três submissões do mesmo título: 275, 19 e 3 pontos); a afirmação de premortem no ensaio foi procurada e **não existe**.

### V-44 — Cinco padrões de CLAUDE.md em produção (origem community R-25) — Classe B (5/10) · Lente: community
- **Tipo:** claude-md-rule · pattern
- **Fonte:** https://reddit.sentinel-team.org/posts/1v13yrk/snapshots/2026-07-20T20%3A24%3A21.6759Z (espelho de terceiros de um post em r/ClaudeAI, u/OkAerie7822, 57 pontos, 26 comentários, 14 capturados; o original não foi acessado)
- **Técnicas-chave (conferidas no espelho):** proibições com gatilho de parada, pesquisar antes de criar (reutilizar função ou tipo existente), ponteiros para arquivos canônicos, checklist curto de início, declarar incerteza antes de editar; listas longas de "não use X" funcionam pior que instruções positivas com exemplo. Corrobora o guia oficial (V-03) sobre CLAUDE.md curto e enxuto.
- **Conteúdo reutilizável (reescrito):** bloco de CLAUDE.md: "Antes de criar tipo ou função, procure o nome no repositório e reutilize; a fronteira X nunca importa Y, pare e pergunte se parecer necessário; padrão canônico de [tema] é [arquivo]; antes de editar, liste os arquivos afetados e o que não tem certeza; rode [comando], sem mock de banco."
- **Ressalvas:** relato de um autor; espelho de terceiros; não é fonte única de nenhuma regra do plugin.
- **Verificação:** página do espelho aberta (título, autor, pontos e padrões conferidos).

### V-45 — Revisão de arquitetura por hipótese e auditoria em sessão nova (origem community R-08) — Classe C (4/10), aprovado como sinal cruzado · Lente: community
- **Tipo:** checklist · workflow
- **Fonte:** https://developertoolkit.ai/en/claude-code/lessons/architecture/ (Michał Jaskólski; publicado em 24/07/2025, modificado em 03/10/2026; site de treinamento pago)
- **Técnicas-chave (conferidas):** plano/modo somente leitura; mapa do estado atual com arquivo:linha por afirmação e marcação de ligações inferidas ou só de runtime; reconciliar com ferramenta estática de dependências (dependency-cruiser, madge); comparar opções pelo grafo de chamadas e restrições do time; ADR **só depois** da decisão humana, com regra de dependência imposta por CI e ponteiro no CLAUDE.md; auditoria das citações em sessão nova com aprovação do tech lead; migração em fases reversíveis, cada uma com verificação própria.
- **Conteúdo reutilizável (reescrito):** checklist de dez passos: leitura apenas · escopo por fluxo · mapa com citação · checagem por ferramenta estática · comparação por impacto no código · identificar e verificar o fato que mudaria a recomendação · ADR após a decisão com regra verificável · auditoria em sessão nova · fases reversíveis com plano de rollback · atualizar a documentação quando o grafo mudar. Convergente com V-03 (revisor em contexto novo), V-11 (prova independente) e V-15 (ADR registra decisão humana).
- **Ressalvas:** fonte comercial de autoria única; as ferramentas citadas não foram executadas nem avaliadas aqui.
- **Verificação:** página aberta; passos, datas e autor conferidos.

## Rejeitados e rebaixados

| Item | Decisão | Motivo |
| --- | --- | --- |
| github R-13 (VoltAgent architect-reviewer) | Rebaixado a C | Prompt-score 33: checklist de oito itens quase vazio ("verified", "confirmed"), manda "consultar o context manager" (inexistente), dá `Write, Edit, Bash` a um revisor, sem formato de relatório. Contagem divergente de subagentes (README "161+") não verificada. Reaproveitar só a ideia dos oito eixos de revisão (padrões, escalabilidade, tecnologia, integração, segurança, desempenho, dívida, evolução), reescrita em V-03/V-19. |
| github R-16 (mblode agents-md) | Rebaixado a C | Só README lido (144 estrelas, MIT); os critérios de auditoria citados nos buscadores não aparecem no README. Fora do núcleo do segmento. |
| github R-19 (josiahsiegel c4-model) | Rejeitado | Caminho 404; só agregadores. Não verificável. |
| github R-20 (agregadores como "prova") | Rejeitado como item; adotado como regra de método | Não é conteúdo reutilizável. Regra aplicada nesta validação: estrelas e instalações de agregador são Não verificáveis até conferidas no repositório. Isso mudou números (athola 341, Jeffallan 11,8 mil). |
| community R-02 (memória em markdown, Show HN cog) | Rejeitado para este segmento | 157 pontos e 49 comentários verificados, mas é sistema de memória de agente, comentários divididos e post criticado como escrito por LLM; fora do escopo de arquitetura. |
| community R-03 (Composer MCP) | Rebaixado a C | 8 pontos, produto do próprio autor. A lição (um nível por diagrama, poucos nós) foi absorvida em V-23. Não instalar MCP de terceiros. |
| community R-04/R-05 (Structurizr AI e MCP) | Rebaixados a C | Documentação de fornecedor sem data (só "v2026.09.19" na navegação). A página **não** afirma que LLMs erram níveis do C4 nem dá o transporte do MCP (o "conflito STDIO versus HTTP" não se sustenta). Mantida a ideia de validação determinística de modelo como código; não ativar `.mcp.json`, não executar Docker. |
| community R-07 (understandingdata plan-mode) | Rejeitado | Métricas sem método (30% para 5% de violações etc.); prompts genéricos já cobertos pela doc oficial (V-03). |
| community R-09 e R-11 (besthub, CLAUDE.md em camadas) | Rejeitados como fonte | Autor "AI Architecture Hub", data 10/07/2026, texto com traços de tradução/LLM, atribuição "200 linhas = guia da Anthropic" não verificável. Os princípios (raiz curta, skill para procedimento, hook para o crítico) estão na doc oficial (V-03, V-06). |
| community R-10 (tw93, seis camadas) | Rebaixado a C | Relato pessoal verificado (12/03/2026); útil como sinal: CLAUDE.md declara, skill descreve, hook impõe; `maxTurns` em subagentes. A doc oficial cobre isso. |
| community R-19 (Encore) | Rebaixado a C | Fornecedor com produto a vender, sem limiares numéricos; a tese sobre agentes não é medida. Usado só como apoio em V-27. |
| community R-21 (checklist de efeitos colaterais, snippets) | Rejeitado | Fontes (gravitee, skillselion) só em snippet, nunca lidas; conteúdo já coberto por V-30 a V-35. |
| community R-22 (revisão de API de catálogos) | Rejeitado | Só snippets de catálogos. Substituído por V-39, V-40, V-41. |
| community R-23 (subagente de bounded contexts, snippets) | Rejeitado | Blog e catálogos não lidos; catálogo alerta que a skill não é assinada. Substituído por V-26 + V-04. |
| community R-24 (issue Architect Mode) | Rebaixado a C | Existe: issue #60995 do claude-code, aberta em 20/05/2026 e fechada como "not planned" em 20/06/2026, 2 comentários. Serve só de sinal de lacuna. A "emulação" proposta pelos pesquisadores (subagente sem Write que grava só em `docs/adr/`) **não é possível apenas com `tools`**; exige regra de permissão ou hook (Inferido, V-04). |
| community R-18, authoritative R-01/R-02 duplicados | Fundidos | Mesma fonte; aparecem uma vez em V-01 e V-02. |

## Mapa de cobertura do escopo (após validação)

| Subtema | Itens aprovados | Qualidade da cobertura |
| --- | --- | --- |
| Decisões de arquitetura e ADR | V-12, V-13, V-14, V-15, V-16 | Forte (fonte A + 4 prompts) |
| Trade-offs e análise de alternativas | V-10, V-19, V-13, V-43 | Boa; falta método formal (ATAM, atributos de qualidade) |
| Diagramas C4 e Mermaid | V-21, V-22, V-23 | Boa |
| DDD: bounded context e agregados | V-26 | Parcial (Fowler; Evans e Vernon sem fonte primária) |
| Hexagonal e camadas | V-24, V-25 | Parcial (sem Clean Architecture) |
| Monólito modular versus microsserviços; migração | V-27, V-28, V-29 | Boa |
| Event-driven, CQRS, event sourcing | V-36, V-37 | Boa |
| Consistência (saga, outbox, idempotência) | V-33, V-34, V-35 | Forte |
| Resiliência (retry, circuit breaker, bulkhead) | V-30, V-31, V-32, V-41 | Forte; jitter sem fonte primária |
| Escalabilidade | V-41 (skill scaling-evolution), V-32 | Fraca (sem fonte A específica) |
| Cache | V-38, V-41 | Razoável (um padrão Microsoft + skill de comunidade) |
| Design de APIs | V-39, V-40, V-41 | Razoável (sem versionamento/paginação/idempotência HTTP de fonte normativa) |
| Revisão de arquitetura | V-19, V-42, V-45, V-03 | Boa |
| Agentes, subagentes e skills | V-04, V-05, V-07, V-08, V-09, V-10 | Forte |
| Context engineering e CLAUDE.md | V-02, V-03, V-44, V-06 | Boa |
| Workflow pesquisa-plano-implementação | V-09, V-17, V-18, V-20 | Forte |
| Segurança de arquitetura (modelagem de ameaças) | nenhum | Lacuna |

## Lacunas objetivas e pesquisáveis (próxima rodada)

1. **Clean Architecture / onion / ports and adapters moderno:** abrir o artigo de Robert C. Martin (blog.cleancoder.com, 2012) e a documentação de uma ferramenta de teste de dependências (ArchUnit, dependency-cruiser) para a regra "dependências apontam para dentro" verificável em CI.
2. **DDD primário:** DDD Reference de Eric Evans (domainlanguage.com) e "Effective Aggregate Design" de Vaughn Vernon (3 partes); hoje só há Fowler.
3. **Escalabilidade e capacidade:** AWS Builders' Library ("Timeouts, retries and backoff with jitter" e artigos de carga/shedding), Azure Well-Architected Performance Efficiency (PE:05 particionamento e escala) e o capítulo de overload do livro Google SRE. Resolve também a fonte primária do **jitter** (V-31).
4. **Idempotência e paginação em HTTP de fonte normativa:** RFC 9110 (semântica de métodos), o rascunho IETF do cabeçalho `Idempotency-Key`, documentação de idempotência da Stripe, Google AIP (aip.dev) e Microsoft REST API Guidelines (github.com/microsoft/api-guidelines); conferir também se o Azure API design cita RFC 9457.
5. **Método de trade-off e atributos de qualidade:** ATAM (SEI/CMU), cenários de atributos de qualidade, ISO/IEC 25010, MADR (adr.github.io/madr) e arc42, para um template de análise de alternativas com fonte reconhecida.
6. **Segurança de arquitetura:** modelagem de ameaças (OWASP Threat Modeling, STRIDE da Microsoft) e checklist de revisão de segurança de design; hoje não existe nenhum item.
7. **Evolução de esquema e dados:** padrão expand/contract (Fowler "ParallelChange"), particionamento de dados (Microsoft Data partitioning), banco por serviço.
8. **Funções de aptidão (fitness functions):** "Building Evolutionary Architectures" (Ford, Parsons, Kua) e exemplos de CI para regras de fronteira; V-28 e V-24 tratam disso só por prompts de comunidade.
9. **Plugins oficiais de arquitetura:** listar `anthropics/claude-plugins-official/plugins` e `anthropics/claude-cookbooks` em busca de agentes/skills de arquitetura ou ADR (a pesquisa só abriu feature-dev e code-modernization); a página do repositório não expande subpastas no WebFetch, usar a listagem raw ou a API autenticada.
10. **Event-driven em geral:** Fowler "What do you mean by Event-Driven?" (2017, citado pela página da Microsoft) e AsyncAPI.
11. **Reddit, YouTube, X e dev.to:** r/ClaudeCode, YouTube e newsletters seguem sem cobertura direta; ver a thread HN "Show HN: Whiteboard (YC W26)" (id 49833867, 424 pontos, 60 comentários de primeiro nível; repositório devdotfast/whiteboard) como candidata ao segmento de design de software; não foi aberta.
12. **Evidência de eficácia:** nenhum item tem avaliação publicada (evals) além dos arquivos de proyecto26 e da metodologia do skill-creator; criar cenários próprios de avaliação ao construir as skills.

## Recomendações ao construtor

**Princípio geral:** nenhum prompt de terceiro deve ser copiado. Use os textos reescritos acima; peça a revisão da rubrica D1–D12 em cada skill nova (meta ≥ 80). Aproveite a licença só para citar: skill-creator (Apache-2.0), awesome-copilot (MIT), awesome-cursorrules (CC0), proyecto26, wshobson e athola (MIT). Conteúdo de `anthropics/claude-code` (feature-dev, code-architect) tem direitos reservados: somente destilado.

**Skills (cada uma com `references/` e gatilhos em PT-BR e EN):**
1. `adr` (V-12, V-13, V-14, V-15, V-16): gatekeeper de dois estágios, entrevista, template consolidado, aprovação antes de gravar, supersessão por diff, índice. `disable-model-invocation: true` na parte que grava arquivos; leitura ("por que escolhemos X?") liberada.
2. `design-review` (V-19, V-42, V-45, V-03): só leitura; desafio de escopo; decisões numeradas com recomendação; tabela de pendências.
3. `system-design` (V-41, V-42): seis fases, camadas L0–L7 como checklist, conta de ordem de grandeza no texto.
4. `architecture-plan` (V-17, V-18, V-20): pesquisar, planejar, anotar; template de plano; EARS; gate de confiança configurável.
5. `resilience-and-consistency` (V-30 a V-37): referências separadas para retry, circuit breaker, bulkhead, consumidor idempotente, outbox, saga, CQRS, event sourcing; cada uma com "quando NÃO usar".
6. `cache-and-scale` (V-38, V-41): só depois de fechar as lacunas 3 e 4.
7. `api-design` (V-39, V-40, V-41): checklist com RFC 9457, `Idempotency-Key`, paginação por cursor, versionamento aditivo.
8. `decomposition` (V-26, V-27, V-28, V-29): monólito modular, bounded context, agregados, strangler.
9. `c4-and-diagrams` (V-21, V-22, V-23): níveis, regras de Mermaid, validação de parse.
10. `skill-eval-architecture` (V-07): checklist de avaliação das próprias skills.

**Subagentes (somente leitura, `maxTurns` definido, sem depender de `permissionMode`/`hooks`/`mcpServers` no arquivo do plugin, ver V-04):**
- `architecture-blueprint` (V-10 reescrito), `architecture-reviewer` (V-03 prompt adversarial + V-19), `boundary-mapper` (V-26, V-24, V-28), `adr-writer` (V-14/V-15/V-16; este grava, então o plugin deve instruir o usuário a limitar a escrita a `docs/adr/` por regra de permissão ou hook do projeto), `skeptic-architect` (V-43).
- Briefing padrão e regra de escala de V-08 em todos.

**Comandos (ação humana, `disable-model-invocation`):** `/arquitetura:feature` (V-09 com gates), `/arquitetura:pesquisar`, `/arquitetura:planejar`, `/arquitetura:anotar` (V-20), `/arquitetura:adr` (V-14/V-16).

**Checklists de referência (`references/`):** resiliência (V-30–V-32), consistência (V-33–V-36), decomposição (V-27–V-29), camadas e fronteiras (V-24, V-25, V-28), C4 (V-21), revisão de API (V-39, V-40), cache (V-38).

**Regras de CLAUDE.md (curtas, testáveis e com verificador):** fronteiras e imports proibidos com comando de grep ou teste de arquitetura (V-24, V-28, V-44); "ADRs aceitos são restrições; mudar exige novo ADR" (V-12); gate de spec antes de código para mudança arquitetural (V-18); "nenhum código antes da aprovação do plano" (V-20); pesquisar antes de criar (V-44).

**Output style opcional:** `arquiteto` com `keep-coding-instructions: true`, diagrama primeiro, até 15 nós (V-06); nunca `force-for-plugin` por padrão.

**Não incluir:** o arquivo plan-eng-review do gstack nem seus binários e telemetria (V-19); scripts `npx` e `botec.py` (V-40, V-41); o plugin code-modernization como dependência (telemetria ligada por padrão, V-11); instaladores do ECC (V-16); qualquer MCP de terceiros (Composer, Structurizr) ativado por padrão; o prompt architect-reviewer do VoltAgent.
