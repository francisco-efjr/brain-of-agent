# Desenvolvimento de jogos (game-development) — VALIDADO (consolidado das 3 lentes)

Data: 2026-10-10 · Validador: claude-sonnet-5-5 (independente: os pesquisadores foram claude-haiku-5-5; a revisão é de outro modelo, mas ainda da família Claude, então não substitui revisão humana) · Itens recebidos: 66 · URLs/endpoints re-verificados: 74 (ver "Método e limites")

## Estatísticas por lente

| Lente | Recebidos | Aprovados (mesma classe ou maior) | Rebaixados (classe menor, só referência, ou fundido como nota) | Rejeitados | Itens V gerados a partir dela |
| --- | --- | --- | --- | --- | --- |
| authoritative | 23 | 17 | 4 (R-12, R-19, R-21, R-23) | 2 (R-17, R-18) | V-01 a V-21, V-34, V-35 (parcial), V-36 (parcial) |
| github | 18 | 9 | 5 (R-06, R-08, R-09, R-17, R-18) | 4 (R-07, R-14, R-15, R-16) | V-22 a V-29, V-03, V-04, V-11, V-35 |
| community | 25 | 14 | 5 (R-06, R-15, R-20, R-22, R-23) | 6 (R-11, R-12, R-13, R-14, R-24, R-25) | V-02, V-22 a V-33, V-36 |
| **Total** | **66** | **40** | **14** | **12** | **36 itens V (após deduplicação entre lentes)** |

Estatísticas dos itens V: 36 aprovados. Classe A: 19 (V-01 a V-13, V-15 a V-17, V-19 a V-21; V-12 é A para a CLI do Godot e B para GUT). Classe B: 16 (V-14, V-18, V-22 a V-35). Classe C: 1 (V-36, anti-padrões, uso como caso negativo). Prompt-score médio dos 31 artefatos reutilizáveis tipo prompt/skill/agente/regra/checklist, após a reescrita: **83,8/100** (média antes da reescrita estimada em 72). Nenhum artefato reprovado automaticamente.

Itens por tipo de uso: skills 7 (V-25, V-26, V-27, V-28, V-29 como padrão, V-34 como formato, V-08 como método), subagentes 3 (V-03, V-23, V-24), regras de CLAUDE.md 7 (V-01, V-11, V-16, V-19, V-22, V-31, V-32), checklists 14, referências 7, anti-padrões 1.

## Método e limites desta validação

- Re-verificação com ferramenta de 62 dos 66 itens recebidos (94%), acima do mínimo de 40%. Todos os itens classe A foram reabertos. Os 4 itens não reabertos com sucesso: R-authoritative-17 (agenda GDC, HTTP 403), R-authoritative-18 (GDQuest, não reaberto por ser C e não aproveitado), R-community-24 (Medium, HTTP 403), e a parte "Isla/Orkin" de R-authoritative-17.
- GitHub: a API pública anônima do meu IP esgotou a cota (60/h); usei WebFetch em `api.github.com` (funcionou para 9 repositórios, HTTP 403 para 6) e, nos 403, a página HTML do repositório (estrelas, forks e licença visíveis; data do último commit não aparece no HTML).
- WebFetch devolve resumo de um modelo pequeno, não o texto integral. Para afirmações numéricas e de campo (limites de frontmatter, números, datas) pedi confirmação item a item e trato o resultado como Verificado. Para "ausência de instrução dirigida a IA" a verificação tem essa limitação.
- WebSearch: a cota do turno (200, compartilhada) já estava esgotada quando precisei; nenhuma busca nova foi possível. Os itens adicionados por mim (marcados "origem: validador") vieram de URLs oficiais já previstas nas lacunas dos pesquisadores ou nas pistas do atlas, abertas diretamente.
- Nada foi baixado nem executado. Nenhuma página lida continha instrução dirigida à IA; todo conteúdo foi tratado como dado.

## Itens aprovados

Legenda do campo "Lente": authoritative = A, github = G, community = C. "Pontuação D1–D12" completa na seção seguinte à lista de itens.

### V-01 — Claude Code: verificação executável, fluxo explorar-planejar-implementar e CLAUDE.md enxuto (origem R-authoritative-05) — Classe A · Prompt-score 87 (original 73)
- **Lente:** A. **Tipo:** checklist + claude-md-rule. **Fonte:** https://code.claude.com/docs/en/best-practices · **Autor/Org:** Anthropic.
- **Sinais:** documentação oficial; página aberta e conferida em 2026-10-10. Licença do texto: não verificada (só destilação).
- **Para que serve:** base de qualquer CLAUDE.md de jogo e da disciplina "dar ao agente algo que ele rode (build headless, teste, captura) antes de dizer pronto".
- **Técnicas-chave (todas conferidas na página):** dar um critério executável (testes, build, captura de tela); fluxo explorar, planejar, implementar, commitar; pular o plano quando o diff cabe numa frase; teste de cada linha do CLAUDE.md ("remover isso faria o Claude errar?"); excluir o que o código já mostra; ênfase ("IMPORTANT") só em uma linha que o agente insiste em ignorar; hooks para o que precisa ocorrer sempre; `/clear` após duas correções falhas; revisor adversarial em subagente com contexto novo, pedindo só lacunas de correção.
- **Conteúdo reutilizável (reescrito):** esqueleto de CLAUDE.md para jogo.
  ```markdown
  # <projeto> — <Godot 4.x | Unity <versão exata> | Unreal <versão exata>>
  ## Comandos que o agente não adivinha
  - Abrir/rodar: <comando>   · Check headless: <comando> (sai com 0 e sem erro no log)
  - Testes: <comando>; durante o trabalho rode só os afetados
  ## Pronto significa
  - O comando de check passou e o agente colou a saída real; comportamento pedido foi exercitado
    (captura, log de sonda ou clipe); nada que funcionava antes quebrou.
  - Sensação de jogo, áudio e legibilidade visual ficam como pendência para um humano jogar.
  ## Regras do projeto (só o que difere do padrão)
  - Não editar: <pastas geradas pela engine>. Cena/mapa principal: <caminho>.
  - Valores de gameplay vivem em <dados/config>, não no código.
  ## Se faltar algo
  - Versão da engine desconhecida ou comando de check ausente: pergunte uma vez, antes de codar.
  ```
- **Ressalvas:** página muda com frequência (cita versões recentes do Claude Code); conferir antes de publicar regra derivada. Rótulo: Verificado para as técnicas; o esqueleto é Inferido (adaptação a jogos).
- **Verificação:** WebFetch da página completa; checadas as 8 técnicas acima, incluindo a tabela de inclusão/exclusão do CLAUDE.md.

### V-02 — Memória do Claude Code: tamanho, regras por caminho, importações e hooks (origem R-community-09) — Classe A
- **Lente:** C. **Tipo:** reference + claude-md-rule. **Fonte:** https://code.claude.com/docs/en/memory · **Autor/Org:** Anthropic.
- **Sinais:** oficial; aberta e conferida (arquivo salvo e busca por trechos).
- **Para que serve:** decidir onde cada regra de jogo mora (CLAUDE.md raiz, `.claude/rules/` por tipo de arquivo, `CLAUDE.local.md`).
- **Técnicas-chave (Verificado):** alvo abaixo de 200 linhas por CLAUDE.md; `@import` organiza mas não reduz custo de contexto; regras com `paths` carregam sob demanda (ex.: `**/*.gd`); `CLAUDE.local.md` para preferências pessoais, fora do git; `AGENTS.md` é lido só quando não há CLAUDE.md acima; instruções são contexto, e bloqueio garantido exige hook (PreToolUse). A memória automática carrega as primeiras 200 linhas ou 25 KB.
- **Conteúdo reutilizável (reescrito):** regra de organização para o plugin: CLAUDE.md curto com comandos e "pronto significa"; convenções de linguagem em `.claude/rules/gdscript.md` com `paths: ["**/*.gd"]` (equivalente para `**/*.cs`, `**/*.cpp`); nada de segredos em nenhum desses arquivos.
- **Ressalvas:** detalhes de carregamento mudam por versão (a página cita v2.1.277 para AGENTS.md).
- **Verificação:** WebFetch + grep nas linhas do arquivo salvo (linhas 31, 88, 102, 123, 349-370).

### V-03 — Subagentes: campos, precedência, mínimo privilégio e template de revisor de gameplay (origens R-authoritative-01, R-github-12) — Classe A · Prompt-score 85 (original 70)
- **Lentes:** A, G. **Tipo:** reference + subagent. **Fonte:** https://code.claude.com/docs/en/sub-agents · **Autor/Org:** Anthropic.
- **Sinais:** oficial; página lida em 100.000 dos 108.415 caracteres (o restante não foi lido).
- **Técnicas-chave (Verificado):** só `name` e `description` são obrigatórios; campos conhecidos: `tools`, `disallowedTools`, `model`, `maxTurns`, `skills`, `omitClaudeMd`, `effort`, `isolation`, `permissionMode`, `hooks`, `mcpServers`, `memory`, `background`, `color`, `initialPrompt`; campos desconhecidos são ignorados em silêncio; precedência: managed > `--agents` > `.claude/agents/` > `~/.claude/agents/` > `agents/` de plugin; subagentes de plugin ignoram `hooks`, `mcpServers` e `permissionMode`; o subagente não vê o histórico da conversa; aviso quando a soma das descrições passa de 15.000 tokens.
- **Correção ao pesquisador:** `name` não aceita `:`; o limite de caracteres citado na página é 256 (não 64, que é o limite de skills).
- **Conteúdo reutilizável (reescrito):**
  ```markdown
  ---
  name: gameplay-reviewer
  description: Revisa alterações em scripts de gameplay (GDScript, C#, C++) e aponta alocação por frame, ciclo de vida incorreto, referências nulas e valores de gameplay fixos no código. Use depois de editar arquivos de scripts de jogo ou quando o usuário pedir revisão de mecânica.
  tools: Read, Grep, Glob
  model: haiku
  ---
  Você revisa código de gameplay sem editar nada. Recebe do orquestrador: arquivos, versão da engine e o critério de pronto.
  Para cada achado: arquivo:linha, o que está errado, por que importa (frame, crash, tuning) e correção sugerida.
  Separe "correção de comportamento" de "estilo" e relate só a primeira por padrão.
  Se a versão da engine ou os arquivos de referência faltarem, diga o que faltou e não afirme APIs de memória.
  Termine com: veredito (sem achados | achados menores | achados que bloqueiam) e o que você não conseguiu avaliar.
  ```
- **Ressalvas:** `model: haiku` é uma escolha de custo (Inferido); validar com avaliações (V-06). Campos mudam entre versões do Claude Code.
- **Verificação:** WebFetch focado em campos, precedência, plugins e histórico; checado o limite de 15.000 tokens.

### V-04 — Harness para projetos longos: `features.json` com `passes`, init e rotina de sessão (origens R-authoritative-02, R-github-11, R-community-07) — Classe A · Prompt-score 87 (original 77)
- **Lentes:** A, G, C (três lentes citam o mesmo artigo; deduplicado). **Tipo:** pattern + checklist. **Fonte:** https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents · **Autor/Org:** Anthropic Engineering.
- **Sinais:** publicado em 26/11/2025 (Verificado na página; a lente community dizia "data não verificada").
- **Técnicas-chave (Verificado):** agente inicializador (ambiente, `init.sh`, progresso, commit inicial) e agente de codificação; lista de funcionalidades em JSON com `passes: false`; JSON preferido porque o modelo o sobrescreve menos que Markdown; uma funcionalidade por sessão; rotina de início (diretório, log do git, progresso, lista, init, teste ponta a ponta); limite do Puppeteer com alertas nativos.
- **Conteúdo reutilizável (reescrito):**
  ```json
  {"id": "dash-01", "categoria": "gameplay",
   "descricao": "Dash consome stamina e respeita colisão com paredes",
   "passos": ["abrir a cena de teste", "acionar dash via sonda de input", "ler stamina e posição no log"],
   "passes": false}
  ```
  Regras: só o campo `passes` muda, e só depois de rodar os `passos`; nunca apagar nem editar passos; um item por sessão.
  Rotina de início (jogo): confirmar diretório → ler `git log` e o arquivo de progresso → ler a lista e escolher o primeiro `passes: false` → rodar o init (abre o jogo/editor e executa o check headless) → rodar o teste mínimo antes de codar. Fim: commit descritivo, atualizar progresso com o que ficou quebrado.
- **Ressalvas:** o exemplo do artigo é aplicação web; a transposição a jogos é Inferido (testes de sensação continuam humanos, ver V-28 e V-30).
- **Verificação:** WebFetch da página, cada afirmação confirmada; data de publicação lida.

### V-05 — Gerador e avaliador separados: contrato, avaliador cético, limiar por critério (origens R-authoritative-03, R-community-08) — Classe A · Prompt-score 83 (original 63)
- **Lentes:** A, C. **Tipo:** pattern + prompt (avaliador). **Fonte:** https://www.anthropic.com/engineering/harness-design-long-running-apps · **Autor/Org:** Anthropic Engineering. Publicado em 24/03/2026 (Verificado).
- **Técnicas-chave (Verificado):** planner, generator e evaluator; contrato de sprint combinado por arquivo; agentes elogiam o próprio trabalho, e é mais viável calibrar um avaliador cético do que fazer o gerador se criticar (o avaliador padrão aprovava o trabalho depois de notar falhas e precisou de várias rodadas de ajuste); limiar rígido por critério; few-shot com nota detalhada reduz deriva; com o Opus 4.6 o autor removeu o sprint e passou a rodar o avaliador uma vez no fim; avaliador só compensa onde o modelo não resolve sozinho.
- **Custos relatados pelo autor (Verificado como relato):** execução solo 20 min e US$ 9; harness completo 6 h e US$ 200; versão atualizada US$ 124,70 (tabela 3 h 50 min, texto "cerca de 4 h").
- **Conteúdo reutilizável (reescrito):** prompt-base do avaliador de feature de jogo.
  ```markdown
  Você avalia uma funcionalidade de jogo que outro agente construiu. Seu trabalho é achar falhas, não elogiar.
  Entrada: contrato de pronto, build/commit, comando para rodar.
  Rode o jogo (ou a cena de teste) e exercite cada comportamento do contrato; leia o log real.
  Critérios (cada um tem limiar mínimo definido no contrato; abaixo do limiar reprova):
  1. Funciona: sem erro no log, comportamento do contrato observado. 2. Regressão: um comportamento antigo segue igual.
  3. Orçamento de frame no perfil de referência. 4. Legibilidade: feedback visual/sonoro presente.
  Marque "NÃO AVALIADO" para sensação de jogo e áudio; isso é de um humano.
  Para cada falha: passos, esperado, observado, evidência (log/captura). Se tudo passou, diga o que exercitou.
  ```
  Calibração: anexar 2 a 3 exemplos de notas comentadas do projeto antes do uso.
- **Ressalvas:** a fonte não publica o prompt do avaliador; este é Inferido a partir dos princípios. Custo alto; usar em partes difíceis. A rubrica de jogo é Suposição até testar em projeto real.
- **Verificação:** WebFetch, cada item conferido, valores de custo e data lidos.

### V-06 — Avaliações de agentes: 20 a 50 tarefas, referência, graders e casos negativos (origem R-authoritative-04) — Classe A · Prompt-score 83 (original 67)
- **Lente:** A. **Tipo:** checklist. **Fonte:** https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents · **Autor/Org:** Anthropic Engineering. Publicado em 09/01/2026 (Verificado).
- **Técnicas-chave (Verificado):** começar com 20 a 50 tarefas tiradas de falhas reais; solução de referência prova que a tarefa é resolvível; taxa de 0% em muitas tentativas costuma indicar tarefa quebrada; graders de código, de modelo e humano; avaliar o resultado e não o caminho; testar casos em que o comportamento deve e não deve ocorrer.
- **Conteúdo reutilizável (reescrito):**
  ```yaml
  id: godot-spawner-001
  tarefa: "Criar spawner que instancia 10 inimigos, com limite de instâncias"
  referencia: "cena de teste com 10 spawns e saída limpa no headless"
  grader: codigo        # contar nós + procurar ERROR no log + exit code 0
  deve_disparar_skill: true
  casos_negativos: ["spawner sem limite deve reprovar", "pedido de 'melhor engine 2D' não aciona a skill"]
  ```
- **Ressalvas:** exemplos de jogo são Inferido (a fonte não tem jogos).
- **Verificação:** WebFetch; citações curtas da fonte conferidas ("20-50", "0%", "graders", "outcome").

### V-07 — Checklist de revisão de skill (limites de frontmatter, tamanho e teste) (origem R-authoritative-06) — Classe A · Prompt-score 83 (original 80)
- **Lente:** A. **Tipo:** checklist. **Fonte:** https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices · **Autor/Org:** Anthropic.
- **Técnicas-chave (Verificado):** `name` até 64 caracteres, minúsculas, números e hífen, sem as palavras reservadas "anthropic" e "claude"; `description` até 1.024 caracteres, não vazia, sem tags XML, em terceira pessoa, dizendo o que faz e quando usar; corpo do SKILL.md com menos de 500 linhas; referências a um nível de profundidade; sumário em referência acima de 100 linhas; barras normais nos caminhos; testar com Haiku, Sonnet e Opus; criar avaliações antes de documentação extensa; no mínimo três avaliações; evitar informação com prazo.
- **Conteúdo reutilizável (reescrito):**
  - [ ] `name` == nome da pasta; só minúsculas, números, hífen; sem "claude"/"anthropic"
  - [ ] `description` (<= 1.024) com o que faz + gatilhos concretos em PT-BR e EN + engine e versão alvo
  - [ ] SKILL.md < 500 linhas; detalhe em `references/` linkado direto do SKILL.md
  - [ ] passos numerados com ponto de verificação; comando de check explícito
  - [ ] pelo menos 3 avaliações, rodadas com e sem a skill, em dois tamanhos de modelo
  - [ ] nenhuma data ou versão "que vai mudar" no corpo (vai para tabela "padrões antigos")
- **Ressalvas:** o nome do plugin/skill neste projeto não deve conter "claude". Requisitos de rede/pacotes dependem da plataforma.
- **Verificação:** WebFetch da página completa, limites conferidos linha a linha.

### V-08 — skill-creator: ciclo de avaliação com e sem skill e matriz de gatilho (origem R-authoritative-07) — Classe A · Prompt-score 82 (original 67)
- **Lente:** A. **Tipo:** workflow. **Fonte:** https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md · licença da pasta: Apache License 2.0 (LICENSE.txt aberto e confirmado) · **Autor/Org:** Anthropic.
- **Sinais (Verificado via API em 2026-10-10):** repositório `anthropics/skills` com 180.246 estrelas, 21.331 forks, push em 2026-10-09; o campo `license` do repositório é `null`.
- **Técnicas-chave (Verificado):** capturar intenção; 2 a 3 prompts realistas de teste; rodada com skill e linha de base no mesmo turno; asserções só quando objetivo; descrição "pushy" com o que faz e quando; otimização da descrição com cerca de 20 consultas (8 a 10 que devem disparar e 8 a 10 quase-iguais que não); critério de parada.
- **Conteúdo reutilizável (reescrito):** matriz de gatilho da skill de Godot. Deve disparar: "meu CharacterBody2D não anda", "crie uma máquina de estados no Godot 4", "o jogo trava ao carregar a cena". Não deve disparar: "instale o Godot no Linux", "qual engine é melhor para 2D", "explique o que é um sprite".
- **Ressalvas (segurança):** o SKILL.md manda executar scripts Python (`aggregate_benchmark`, `run_loop`, `package_skill`) e subir um servidor local de visualização. Não foram abertos nem executados; o construtor deve ler os scripts antes de rodar.
- **Verificação:** WebFetch do SKILL.md (frontmatter e fluxo), do LICENSE.txt e da API do repositório.

### V-09 — Prompting best practices: XML, documentos longos no topo, citações primeiro, estado em JSON/git, tom calmo (origem R-authoritative-08) — Classe A · Prompt-score 80 (original 60)
- **Lente:** A. **Tipo:** prompt pattern. **Fonte:** https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices · **Autor/Org:** Anthropic.
- **Rebaixamento anulado:** o pesquisador só viu snippet e classificou com ressalva. Abri a página inteira (arquivo salvo) e conferi: seção "Structure prompts with XML tags" (tags consistentes, aninhamento), "longform data at the top", "ground responses in quotes", "use structured formats for state data", "use git for state tracking", e o aviso de que, nos modelos recentes, linguagem agressiva ("CRITICAL: You MUST") deve ser suavizada para evitar sobregatilho. Também há a observação de que instruções de verificação herdadas de modelos antigos podem causar excesso de verificação no Opus 5.
- **Conteúdo reutilizável (reescrito):**
  ```xml
  <documentos><documento index="1"><fonte>GDD v3 cap. combate</fonte><conteudo>...</conteudo></documento></documentos>
  <instrucoes>Primeiro cite em <citacoes> os trechos do GDD relevantes ao sistema pedido. Depois gere tarefas por sistema.</instrucoes>
  <formato_saida>Lista com id, sistema, critério de aceite verificável, dependências. Se um dado faltar, escreva "questão aberta" em vez de inventar.</formato_saida>
  ```
- **Ressalvas:** a página lista muitos modelos e muda com frequência; conferir a seção do modelo-alvo antes de fixar tom ou esforço.
- **Verificação:** WebFetch + grep no arquivo salvo (linhas 95-102, 246-302, 491, 782, 847-849).

### V-10 — Desenhar testes para agentes: saída curta, amostragem rápida e oráculo de referência (origem: validador, pista do atlas AO-31) — Classe A · Prompt-score 82
- **Lente:** (nenhuma; adicionado pelo validador a partir de `_leads.md`). **Tipo:** pattern + checklist. **Fonte:** https://www.anthropic.com/engineering/building-c-compiler · **Autor/Org:** Anthropic Engineering (Nicholas Carlini), publicado em 05/02/2026 (Verificado).
- **Técnicas-chave (Verificado):** saída do console com poucas linhas e detalhes em arquivo de log; erros com etiqueta fixa para busca; subamostra rápida e determinística de testes por agente; oráculo (compilador de referência) para isolar a origem de uma falha.
- **Conteúdo reutilizável (reescrito, transposição a jogos = Inferido):** o comando `check` do projeto imprime no máximo 20 linhas (resumo + caminho do log), etiqueta erros como `ERROR[sistema]`, aceita `--quick` (amostra de cenas/níveis) e `--full`; quando existir referência (captura de uma versão aprovada, saída de um build anterior), comparar contra ela para localizar a regressão.
- **Ressalvas:** o contexto é compilador; a ideia de sonda de jogo é analogia.
- **Verificação:** WebFetch da página, três lições confirmadas, data e autor lidos.

### V-11 — GDScript: guia de estilo oficial e tipagem estática (origens R-authoritative-09, R-github-13, R-community-10 e artefato A12) — Classe A · Prompt-score 85 (original 77)
- **Lentes:** A, G, C (deduplicado). **Tipo:** checklist + claude-md-rule. **Fonte:** https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_styleguide.html · **Autor/Org:** Godot Engine.
- **Técnicas-chave (Verificado):** arquivos em snake_case; classes em PascalCase; sinais em snake_case no passado (`door_opened`); constantes em CONSTANT_CASE; enums PascalCase no singular com membros CONSTANT_CASE; prefixo `_` para privados e virtuais sobrescritos; ordem de membros (anotações de ferramenta, `class_name`, `extends`, doc, sinais, enums, constantes, estáticos, `@export`, demais variáveis, `@onready`, callbacks, métodos, classes internas); `:=` quando o tipo está claro na linha, tipo explícito com `get_node()`; `as` falha em silêncio com `null` em tipo incompatível.
- **Conteúdo reutilizável (reescrito, vira `.claude/rules/gdscript.md` com `paths: ["**/*.gd"]`):**
  - Tipar variáveis, parâmetros e retornos; `:=` só quando o tipo é óbvio na mesma linha; ao usar `as`, tratar `null` (a conversão falha sem erro).
  - Nomes: arquivo e função snake_case, classe PascalCase, constante CONSTANT_CASE, sinal no passado, privado com `_`.
  - Ordem dos membros conforme o guia; filhos em `@onready` tipado, nunca em `_init()`.
  - Física e movimento em `_physics_process` (ver V-14); visual e UI em `_process`.
- **Ressalvas:** a página `stable` muda com a versão; confirmar a versão do projeto. Rótulo: Verificado.
- **Verificação:** WebFetch pontual no guia (lista completa de ordem de membros e regras de tipagem).

### V-12 — Godot: verificação headless e testes (`--headless --import`, `--check-only -s`, GUT) (origem: validador, lacuna das três lentes) — Classe A (CLI) / B (GUT) · Prompt-score 83
- **Lente:** (adicionado pelo validador). **Tipo:** checklist + workflow. **Fontes:** https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html ; https://gut.readthedocs.io/en/latest/ ; https://gut.readthedocs.io/en/latest/Command-Line.html · **Autor/Org:** Godot Engine; mantenedores do GUT (MIT).
- **Técnicas-chave (Verificado):** `--headless` equivale a driver de vídeo headless com áudio Dummy; `--import` abre o editor, espera a importação e sai; `--check-only` analisa o script e sai, usado com `-s`; `--path` aponta o projeto (precisa de `project.godot`); GUT 9 exige Godot 4 (docs atuais miram Godot 4.6); execução em linha de comando: `godot --headless -s addons/gut/gut_cmdln.gd -gdir=res://test/unit -gexit`, código de saída 0 se tudo passa e 1 se falhar. Observação do fornecedor Summer Engine (C): "headless não prova qualidade visual, animação, áudio ou sensação" (confirmada literalmente na página dele).
- **Conteúdo reutilizável (reescrito):**
  ```text
  Checagens Godot 4 (rodar da raiz do projeto, ler a saída real):
  1. em checkout limpo: godot --headless --path . --import
  2. sintaxe de um script: godot --headless --path . --check-only -s res://scripts/x.gd
  3. testes (se o projeto adotou GUT): godot --headless --path . -s addons/gut/gut_cmdln.gd -gdir=res://test/unit -gexit
  Exit code != 0 ou "ERROR" no log = não está pronto. Escolher UM framework de teste por projeto.
  O que isto NÃO prova: aparência, animação, áudio, sensação. Registrar como pendência humana.
  ```
- **Ressalvas:** `--check-only` está em builds de editor/templates estendidos; o `--headless` com `--check-only` foi montado por mim a partir de opções documentadas, mas não executei (regra de não executar). Confirmar a versão do Godot antes de usar. O texto de GUT sobre linha de comando não menciona `--headless`; a combinação é Inferido.
- **Verificação:** WebFetch das três páginas; opções conferidas na referência de CLI.

### V-13 — Godot: fluxo de performance (medir, isolar por bisseção, repetir) (origem R-authoritative-10) — Classe A · Prompt-score 83 (original 75)
- **Lente:** A. **Tipo:** workflow + checklist. **Fonte:** https://docs.godotengine.org/en/stable/tutorials/performance/general_optimization.html · **Autor/Org:** Godot Engine.
- **Técnicas-chave (Verificado):** perfilar antes; busca binária desligando metade das rotinas do frame; testar em mais de um dispositivo (sobretudo mobile); medir com V-Sync desligado; o quadro é limitado pelo mais lento entre CPU e GPU; combinar profiler de CPU e de GPU (Nsight, RGP, PIX, Xcode). Mudar uma variável por vez é implícito (exemplo de sprites), não frase literal.
- **Correção ao pesquisador:** a afirmação "evitar chamadas que bloqueiam o servidor a cada frame" não está nesta página (só um link para "Using Servers"). Removida.
- **Conteúdo reutilizável (reescrito):** checklist: [ ] há medição antes e depois, mesmo cenário, V-Sync off; [ ] uma mudança por medição; [ ] gargalo achado no profiler (ou por bisseção), não por suposição; [ ] CPU e GPU olhados separadamente; [ ] testado em hardware de referência; [ ] orçamento em ms definido (ver V-17).
- **Ressalvas:** resultados de busca com a documentação 3.5 não se aplicam ao Godot 4.
- **Verificação:** WebFetch com checklist ponto a ponto (7 de 8 presentes).

### V-14 — Loop de jogo e timestep: passo fixo, acumulador, teto de iterações, interpolação; física no Godot (origens R-authoritative-15, R-authoritative-16 + Godot physics, validador) — Classe B (Nystrom, Fiedler) com apoio A (Godot)
- **Lente:** A (e adição do validador). **Tipo:** pattern. **Fontes:** https://gameprogrammingpatterns.com/game-loop.html (Robert Nystrom, © 2009-2021); https://gafferongames.com/post/fix_your_timestep/ (Glenn Fiedler, publicado em 10/06/2004, © 2004-2026); https://docs.godotengine.org/en/stable/tutorials/physics/physics_introduction.html.
- **Técnicas-chave (Verificado):** passo fixo para atualização com renderização variável e fator de interpolação (`render(lag / passo)`); o texto de Nystrom sugere limitar iterações do laço interno (a expressão "espiral da morte" não aparece nessa página, o conceito sim); Fiedler limita o tempo de quadro a 0,25 s, usa `alpha = acumulador / dt` e slerp para quaternions; no Godot, código que lê ou altera propriedades de corpo físico vai em `_physics_process`, o tick de física padrão é 60 por segundo, `move_and_slide()` já considera o passo (não multiplicar a velocidade por `delta`; gravidade, que é aceleração, ainda usa `delta`), camadas e máscaras de colisão (32 camadas).
- **Conteúdo reutilizável (reescrito, pseudocódigo próprio):**
  ```
  acumulador += min(tempo_do_quadro, TETO)      # TETO ~ 0,25 s evita a espiral
  processar_input()
  enquanto acumulador >= PASSO:  simular(PASSO); acumulador -= PASSO   # com máximo de iterações
  renderizar(acumulador / PASSO)                # interpolar entre estado anterior e atual
  ```
  Teste: mesma sequência de tempos e inputs produz o mesmo estado final (determinismo), pré-requisito para replay e lockstep.
- **Ressalvas:** licenças dos textos não declaradas: só destilação. O corte para Unity (FixedUpdate) não foi lido; Inferido.
- **Verificação:** WebFetch das 3 páginas; os cinco pontos do Godot e os pontos de Fiedler e Nystrom conferidos.

### V-15 — Netcode: autoridade e validação no servidor (Unity Netcode for GameObjects e Godot) (origens R-authoritative-13 corrigido + adição do validador) — Classe A · Prompt-score 83 (original 70)
- **Lente:** A (+ validador). **Tipo:** checklist + pattern. **Fontes:** https://docs.unity3d.com/Packages/com.unity.netcode.gameobjects@2.7/manual/terms-concepts/authority.html ; https://docs.unity3d.com/Packages/com.unity.netcode.gameobjects@2.5/manual/basics/ownership.html ; https://docs.godotengine.org/en/stable/tutorials/networking/high_level_multiplayer.html · **Autor/Org:** Unity; Godot Engine.
- **Técnicas-chave (Verificado):** Unity: cada NetworkObject tem uma e somente uma autoridade; em cliente-servidor o servidor tem a autoridade final sobre spawn e despawn; usar `HasAuthority` para checar autoridade por objeto, pois funciona nas duas topologias (`IsServer` é a checagem tradicional só de cliente-servidor). Godot: o servidor (peer 1) é a autoridade padrão; tratar input do cliente como não confiável, validar argumentos de RPC, limitar a taxa de ações frequentes, não confiar em posições, relógios ou recursos informados pelo cliente; `@rpc` com modo, sync, transfer_mode e canal (padrão equivalente a authority, call_remote, reliable, 0); `multiplayer.get_remote_sender_id()` identifica quem chamou.
- **Correções ao pesquisador:** (1) a página de autoridade do Unity **não** recomenda validar RPCs de cliente nem fala de `IsHost` (isso era recomendação de fórum); (2) "servidor decide spawn/despawn" vem da página de ownership, não da de autoridade. A validação de RPC é oficial no Godot, não no Unity.
- **Conteúdo reutilizável (reescrito):**
  - [ ] cada objeto de rede tem uma autoridade declarada (servidor por padrão)
  - [ ] estado autoritativo só muda em código de servidor; cliente envia intenção (input), não resultado
  - [ ] todo RPC/ServerRpc valida faixa, dono e frequência antes de aplicar (regra de projeto, Godot oficial; Unity: boa prática, Inferido)
  - [ ] visual derivado localmente do estado sincronizado; previsão do cliente só com reconciliação
  - [ ] teste de dois pares (servidor + cliente) antes de marcar "pronto"
- **Ressalvas:** nada foi lido sobre Unreal replication além de V-20; netcode determinístico (rollback) sem fonte.
- **Verificação:** WebFetch das 3 páginas; itens da pesquisa original refutados ou confirmados um a um.

### V-16 — Unity: regras de código de runtime (alocação, ciclo de vida, async) (origem R-authoritative-11) — Classe A · Prompt-score 85 (original 73)
- **Lente:** A. **Tipo:** checklist + claude-md-rule. **Fonte:** https://docs.unity3d.com/6000.0/Documentation/Manual/programming-best-practices.html · **Autor/Org:** Unity.
- **Técnicas-chave (Verificado):** evitar alocações por frame (a página diz "avoid", não "zero bytes", que era do manual 2022.3 só em trecho); cachear `GetComponent` em `Awake`; evitar LINQ e concatenação de string em runtime; `Awaitable` no lugar de `Task`; nunca bloquear a thread principal com `Task.Result`/`Wait` (risco de deadlock); não acessar GameObject, Transform, componentes ou APIs de asset em threads de fundo; sem finalizadores C# (rodam em outras threads e pesam no GC); `Object.Destroy` em runtime e `DestroyImmediate` só no editor; Assembly Definitions; Profiler, Project Auditor e analisadores Roslyn.
- **Conteúdo reutilizável (reescrito, vira `.claude/rules/unity-csharp.md` com `paths: ["**/*.cs"]`):** sem LINQ nem string concatenada em `Update`/`FixedUpdate`; `GetComponent` só em `Awake`/`OnEnable`, ou referência serializada; async com `Awaitable`, sem `.Result`/`.Wait()`; nada de API Unity fora da thread principal; `Destroy` em runtime; antes de marcar performance como ok, abrir o Profiler numa cena representativa (V-17).
- **Conflito registrado:** comunidade recomenda UniTask; o manual oficial recomenda `Awaitable`. Adotar o oficial.
- **Ressalvas:** página da versão 6000.0; em 2022 LTS confirmar APIs.
- **Verificação:** WebFetch, 10 itens conferidos (9 presentes, 1 com redação mais fraca).

### V-17 — Orçamento de frame e profiling (Unity oficial; vale como método geral) (origens R-community-19, A4, A15) — Classe A (promovida de B) · Prompt-score 83
- **Lente:** C. **Tipo:** reference + checklist. **Fonte:** https://unity.com/how-to/best-practices-for-profiling-game-performance · **Autor/Org:** Unity.
- **Técnicas-chave (Verificado):** medir tempo de quadro em ms, não só FPS (média esconde engasgos); 33,33 ms para 30 fps e 16,66 ms para 60 fps; estourar o orçamento em menu/carregamento é aceitável, em gameplay não; perfilar builds no dispositivo-alvo; gargalo é a unidade/thread mais lenta (CPU ou GPU); Deep Profiling distorce os tempos; em mobile deixar cerca de 35% do quadro livre (22 ms a 30 fps); Project Auditor aponta alocações gerenciadas; Frame Debugger ajuda em batching.
- **Data:** a página não declara data de publicação (rodapé 2026).
- **Conteúdo reutilizável (reescrito):** checklist de auditoria: (1) ler orçamentos (fps alvo, memória, draw calls, tempo de carga, build) do config do projeto; (2) métrica sem orçamento = NÃO AVALIADO, nunca "passa"; (3) medir em ms em build no hardware-alvo; (4) classificar CPU-bound ou GPU-bound; (5) análise estática gera candidatos, o profiler confirma; (6) cada recomendação com ganho, esforço e risco; (7) repetir o mesmo perfil depois da mudança; (8) veredito COMPLETO ou NÃO AVALIADO com a lista do que faltou.
- **Ressalvas:** Unity-específico em ferramentas; princípios vão para Godot (V-13) e Unreal (usar `stat unit`, não verificado).
- **Verificação:** WebFetch pontual, 8 afirmações conferidas.

### V-18 — Unity: ScriptableObjects como arquitetura (origem R-authoritative-12) — Classe B (rebaixada de A) · Prompt-score 80 (original 67)
- **Lente:** A. **Tipo:** pattern + claude-md-rule. **Fonte:** https://unity.com/how-to/architect-game-code-scriptable-objects · **Autor/Org:** Unity.
- **Motivo do rebaixamento:** a página diz "Last updated January 2020" (Verificado), logo anterior ao Unity 6; conteúdo de padrão ainda útil, mas atualidade fraca.
- **Técnicas-chave (Verificado):** ScriptableObject como contêiner compartilhado; referência pública no lugar de singleton; variáveis em asset; separar valor inicial de valor de runtime para não alterar o asset salvo; canal de evento com ouvinte registrado em `OnEnable` e removido em `OnDisable`; cenas como folha em branco.
- **Conteúdo reutilizável (reescrito):** estado compartilhado entre sistemas vai em ScriptableObject de variável ou canal de evento, sem singleton novo; cada ouvinte se desregistra em `OnDisable`; edição em runtime persiste no asset no editor, então usar campo de valor de runtime; pequenos projetos podem dispensar o padrão (comentário de terceiros, Inferido).
- **Ressalvas:** conferir contra a documentação atual de ScriptableObject antes de virar regra firme.
- **Verificação:** WebFetch, 6 de 6 itens e data lidos.

### V-19 — Unreal: padrão de código C++ (prefixos, ponteiros, lambdas diferidas, enums, namespaces) (origem R-authoritative-14) — Classe A · Prompt-score 83 (original 73)
- **Lente:** A. **Tipo:** checklist + claude-md-rule. **Fonte:** https://dev.epicgames.com/documentation/en-us/unreal-engine/epic-cplusplus-coding-standard-for-unreal-engine · **Autor/Org:** Epic Games. A página é da versão **UE 5.8** (Verificado).
- **Técnicas-chave (Verificado):** prefixos U, A, S, I, C, T, E, b, F; UObject passado por ponteiro; lambdas diferidas sem captura por referência de locais ou membros, usando `CreateWeakLambda`/`CreateSPLambda` ou `TWeakObjectPtr`/`TWeakPtr`, com comentário quando se desviar; enums expostos a Blueprint baseados em `uint8`; sem namespace em UCLASS/USTRUCT.
- **Conteúdo reutilizável (reescrito):** bloco de regras para CLAUDE.md Unreal: prefixos conforme o tipo base; sem namespace em tipos reflexivos; lambda diferida só com ponteiro fraco; enum de Blueprint em `uint8`; fixar a versão da engine (5.8 neste documento) e conferir headers antes de afirmar API.
- **Ressalvas:** não cobre Blueprints. Lacuna aberta.
- **Verificação:** WebFetch, 5 itens conferidos e versão lida.

### V-20 — Unreal: Gameplay Framework (GameMode, GameState, PlayerState, PlayerController, Pawn, Character, HUD) (origem: validador, lacuna da lente authoritative) — Classe A · Prompt-score 80
- **Lente:** (adicionado pelo validador). **Tipo:** reference + checklist. **Fonte:** https://dev.epicgames.com/documentation/en-us/unreal-engine/gameplay-framework-in-unreal-engine · **Autor/Org:** Epic Games.
- **Técnicas-chave (Verificado, paráfrase):** GameMode existe só no servidor, define regras da partida e não persiste entre níveis; GameState e PlayerState replicam do servidor para os clientes (estado compartilhado e por jogador); PlayerController trata input humano e possui um Pawn; Pawn é a representação física; Character é Pawn com capsule e movimento; HUD é por jogador; GameInstance existe em cada máquina e não replica.
- **Conteúdo reutilizável (reescrito):** tabela "onde cada dado mora" para CLAUDE.md Unreal: regra de partida em GameMode; placar e fase em GameState; vida/munição por jogador em PlayerState; input em PlayerController; corpo em Pawn/Character; UI em HUD.
- **Ressalvas:** a página não detalha a replicação das demais classes; não assumi. Versão não lida.
- **Verificação:** WebFetch.

### V-21 — Unity Test Framework: Edit Mode e Play Mode (referência) (origem: validador) — Classe A (conteúdo curto)
- **Lente:** (adicionado). **Tipo:** reference. **Fonte:** https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/index.html · **Autor/Org:** Unity.
- **Sinais (Verificado):** versão 1.4.6; baseado em NUnit 3.5; exige Unity 2019.2 ou superior; limitações: `UnityTest` não suporta WSA nem a maioria dos testes parametrizados, não suporta `Repeat`, fixtures aninhadas não rodam na interface, `Retry` em Play Mode lança `InvalidCastException` (a seção cita 1.3.x, possível trecho desatualizado).
- **Conteúdo reutilizável:** apenas nota para a skill de Unity: testes de EditMode para lógica pura e de PlayMode para ciclo de vida; rodar pelo Test Runner ou linha de comando.
- **Ressalvas:** a página de execução por linha de comando (`run-tests-from-command-line.html`) retornou 404; os parâmetros `-runTests`/`-testPlatform` ficam **Não verificados**.
- **Verificação:** WebFetch.

### V-22 — CLAUDE.md de estúdio e protocolo de colaboração "perguntar antes de escrever" (origens R-github-01, R-community-01, R-community-02, A3) — Classe B · Prompt-score 87 (original 77)
- **Lentes:** G, C (deduplicado). **Tipo:** claude-md-rule + workflow. **Fonte:** https://github.com/Donchitos/Claude-Code-Game-Studios (CLAUDE.md em raw) · **Autor/Org:** Donchitos (indivíduo).
- **Sinais (Verificado em 2026-10-10 via API):** 26.049 estrelas, 3.696 forks, MIT, push em 2026-10-08, não arquivado, 63 issues abertas; README: 49 agentes, 74 skills (a descrição "About" diz 72), 12 hooks; 42 commits em `main`. Conclusão: popularidade alta e atualização recente, mas **sem evidência independente de eficácia** (estrelas não provam qualidade).
- **Técnicas-chave (Verificado):** campos de stack (engine, linguagem, build, assets) ainda "a escolher" e preenchidos por setup; documentos importados com `@`; protocolo de cinco etapas (pergunta, opções, decisão, rascunho, aprovação); perguntar antes de gravar, aprovar conjunto em mudanças multiarquivo, commit só por instrução, pergunta ignorada não conta como consentimento; checkpoint em `production/session-state/active.md`.
- **Conteúdo reutilizável (reescrito, redação própria; a licença é MIT, mas destilei):**
  ```markdown
  ## Protocolo (fase de design em evolução)
  1. Pergunte o que falta; 2. proponha 2 a 3 opções com trade-offs; 3. espere a decisão;
  4. mostre um rascunho; 5. só então grave. Gravação em vários arquivos: aprovar o conjunto.
  - Pergunta sem resposta não é permissão; não prossiga. Commit apenas se o usuário pedir.
  - Exceções pré-aprovadas: anotar o checkpoint de sessão em production/session-state/active.md.
  - Em tarefas mecânicas e bem delimitadas (renomear, formatar), execute sem o protocolo.
  ```
- **Ressalvas:** o texto original usa MAIÚSCULAS ("MUST", "Never") e depende de estrutura de pastas e de hooks bash/Python; copiar só o padrão. Protocolo reduz autonomia (bom para design, ruim para tarefas mecânicas). Segurança: os 12 hooks rodam automaticamente; revisar antes de instalar o repositório inteiro.
- **Verificação:** API do repositório, página do repositório e CLAUDE.md em raw (resumo por modelo).

### V-23 — Subagente gameplay-programmer (origem R-github-02) — Classe B · Prompt-score 87 (original 73)
- **Lente:** G. **Tipo:** subagent. **Fonte:** https://raw.githubusercontent.com/Donchitos/Claude-Code-Game-Studios/main/.claude/agents/gameplay-programmer.md · **Autor/Org:** Donchitos (MIT).
- **Sinais (Verificado):** frontmatter com `tools: Read, Glob, Grep, Write, Edit, Bash`, `model: inherit`, `maxTurns: 20`; escalonamento nomeado (lead-programmer, game-designer, technical-director, engine-programmer); regra de dados em config; transições de estado explícitas; input com buffer e rebind; exceção: em execução orquestrada pode criar arquivos novos em `production/`, `docs/`, `tests/` sem pedir.
- **Conteúdo reutilizável (reescrito):**
  ```markdown
  ---
  name: gameplay-programmer
  description: Implementa mecânicas de jogo (estados, input, eventos) a partir de um GDD ou critério de aceite. Use quando houver design aprovado e a tarefa for código de gameplay.
  tools: Read, Glob, Grep, Write, Edit
  ---
  Você traduz design em código; não altera o design. Entradas: GDD/critério, versão da engine, ADRs.
  1. Leia o design e liste lacunas. 2. Proponha estrutura e trade-offs; espere aprovação antes de gravar.
  3. Valores de gameplay em arquivo de dados, nunca fixos no código. Estados com tabela de transições; estados inválidos inalcançáveis.
  4. Input com buffer e rebind. Use delta time. Lógica separada de UI por eventos.
  5. Cite o GDD nos casos de borda; registre desvios do design.
  Escalone: arquitetura -> lead; lacuna de design -> designer; performance -> technical lead.
  Entrega: arquivos alterados, desvios do design, como testar (comando), o que não pôde ser verificado.
  ```
  (Bash removido de propósito; adicionar só se o projeto precisar rodar o check.)
- **Ressalvas:** refere-se a docs que podem não existir no projeto (ADRs, referência de engine); sem verificação executável no original, adicionei "como testar".
- **Verificação:** WebFetch do arquivo em raw.

### V-24 — Subagente de especialista de engine (modelo godot-specialist) com checagem de versão (origens R-community-05, A6) — Classe B · Prompt-score 85 (original 70)
- **Lente:** C. **Tipo:** subagent. **Fonte:** https://raw.githubusercontent.com/Donchitos/Claude-Code-Game-Studios/main/.claude/agents/godot-specialist.md · **Autor/Org:** Donchitos (MIT).
- **Sinais (Verificado):** frontmatter `model: inherit`, ferramentas incluindo `Agent` restrito a 4 subespecialistas, `maxTurns: 20`.
- **Técnicas-chave (Verificado):** ler a referência de versão do projeto antes de sugerir API e marcar como "não verificado" o que não estiver nela; checar se o pedido é de outra engine; guiar a escolha GDScript vs C# vs GDExtension por trade-off; propor antes de gravar; limites claros (não decide design, não aprova plugin).
- **Conteúdo reutilizável (reescrito, com campo `<engine>`):**
  ```markdown
  ---
  name: engine-specialist
  description: Especialista na engine do projeto (Godot, Unity ou Unreal) para arquitetura de cenas/objetos, sinais/eventos e revisão de código. Use para dúvidas de API e design técnico; não decide design de jogo.
  tools: Read, Glob, Grep
  ---
  Antes de sugerir qualquer API: leia a versão fixada do projeto e a referência dessa versão; se o dado não estiver lá, rotule "não verificado" e diga como conferir.
  Se o pedido usa conceitos de outra engine, avise que o especialista correto é outro.
  Escolha de linguagem (ex.: GDScript vs C# vs GDExtension): compare por custo de build, desempenho e integração com o editor.
  Não decida design de jogo, não aprove plugins/addons sem decisão do responsável. Proponha antes de pedir gravação.
  Dica de busca (ripgrep): para .gd use glob "*.gd" em vez de type "gdscript".
  ```
- **Ressalvas:** o aviso do ripgrep vem do próprio arquivo, não conferi na ferramenta de busca.
- **Verificação:** WebFetch do arquivo em raw.

### V-25 — Auditoria de performance com orçamentos e veredito "NÃO AVALIADO" (origens R-github-03, R-community-03) — Classe B · Prompt-score 88 (original 82)
- **Lentes:** G, C. **Tipo:** skill + checklist. **Fonte:** https://raw.githubusercontent.com/Donchitos/Claude-Code-Game-Studios/main/.claude/skills/perf-profile/SKILL.md · **Autor/Org:** Donchitos (MIT).
- **Sinais (Verificado):** `model: sonnet`; ferramentas Read, Glob, Grep, Write, Bash; argumento de sistema ou `full`; modos de enforcement `warn` (padrão), `block`, `off`; lista cada insumo como FOUND ou ABSENT; sem dados, o único veredito é NOT ASSESSED; orçamento não definido é NOT ASSESSED, nunca "passa", e o placeholder de 16,67 ms do template não vale; gravar relatório exige confirmação; roda scripts shell do repositório (leitura de config).
- **Conteúdo reutilizável (reescrito):** use o checklist do V-17; estrutura da skill: 0) ler config e declarar o modo de enforcement; 1) tabela de insumos presentes/ausentes; 2) escopo (sistema ou completo); 3) orçamentos do projeto (se faltar, NÃO AVALIADO); 4) análise estática por subsistema (CPU, memória, render, I/O) com rótulo "candidato"; 5) tabela de hotspots por impacto x esforço; 6) decisão do usuário para itens M/L (implementar, reduzir escopo, adiar); 7) gravar relatório só com confirmação.
- **Ressalvas:** acoplada a `project.yaml` e a pastas do repositório; comandos de profiling por engine não foram lidos.
- **Verificação:** WebFetch do arquivo em raw.

### V-26 — Plano de QA por tipo de teste (origens R-github-04) — Classe B · Prompt-score 85
- **Lente:** G. **Tipo:** skill + checklist. **Fonte:** https://raw.githubusercontent.com/Donchitos/Claude-Code-Game-Studios/main/.claude/skills/qa-plan/SKILL.md · **Autor/Org:** Donchitos (MIT).
- **Sinais (Verificado):** `model: sonnet`; tipos Logic, Integration, Visual/Feel, UI, Config/Data; `Type:` declarado é autoritativo, tipo inferido vira lacuna; empate Logic/Integration vira Integration; escopo vazio devolve NOT ASSESSED; níveis minimal/standard/full; o back-fill sobrescreve uma seção em arquivos de história (risco), mas só com aprovação.
- **Conteúdo reutilizável (reescrito):** tabela: Logic (fórmulas, limiares, transições, economia) = teste automático obrigatório; Integration (save/load, rede, persistência) = automático ou smoke; Visual/Feel = captura + humano; UI = captura + checklist; Config/Data = validação de dados. Plano com resumo por tipo, testes automáticos exigidos, checklist manual, escopo de smoke, requisitos de playtest e definição de pronto. Sem histórias no escopo: NÃO AVALIADO (não gerar plano vazio).
- **Ressalvas:** depende de histórias com campo `Type:`.
- **Verificação:** WebFetch.

### V-27 — Revisão de GDD em 4 dimensões com veredito (origem R-github-05) — Classe B · Prompt-score 85
- **Lente:** G. **Tipo:** skill + checklist. **Fonte:** https://raw.githubusercontent.com/Donchitos/Claude-Code-Game-Studios/main/.claude/skills/design-review/SKILL.md · **Autor/Org:** Donchitos (MIT).
- **Sinais (Verificado):** dimensões completude, consistência, implementabilidade, encaixe entre sistemas (+ grafo de dependências); vereditos APPROVED, NEEDS REVISION, MAJOR REVISION NEEDED, NOT ASSESSED (NOT ASSESSED prevalece sobre APPROVED na agregação); modos full, lean, solo; reaproveita veredito só se documento e registro são idênticos byte a byte; escritas exigem confirmação; roda scripts shell do repositório.
- **Conteúdo reutilizável (reescrito):** rubrica de revisão: Completude (seções obrigatórias presentes, "vazio é lacuna, não aprovado"), Consistência (fórmulas vs comportamento, casos de borda vs regras, dependências nos dois sentidos), Implementabilidade (regras precisas, critérios de aceite testáveis), Encaixe (conflito com mecânicas e pilares). Saída: tabela por dimensão + veredito + lista de perguntas abertas. Revisão é só leitura; registro em arquivo só com confirmação.
- **Ressalvas:** cobre estrutura do GDD, não balanceamento numérico nem economia (lacuna).
- **Verificação:** WebFetch.

### V-28 — Playtest: plano, observação e relatório que separa defeito de sensação (origens R-community-04, R-authoritative-22 corrigido, A5) — Classe B · Prompt-score 83
- **Lentes:** C, A. **Tipo:** checklist + skill. **Fontes:** https://raw.githubusercontent.com/Donchitos/Claude-Code-Game-Studios/main/.claude/skills/playtest-report/SKILL.md ; https://book.leveldesignbook.com/process/blockout/playtesting ; https://developers.meta.com/horizon/resources/playtest-planning-survey-script/ ; https://ixdf.org/literature/topics/playtesting.
- **Sinais (Verificado):** playtest-report (modo `new` ou `analyze`, bugs separados de "pain points", roteamento em design/balanceamento/bug/polish, revisão de diretor só no modo full, insumo ausente vira "não avaliado"); Level Design Book (observar mais que perguntar, escopo e perguntas-foco definidos antes, dados: tempo, mortes, taxa de vitória, telemetria, briefing com avisos de conteúdo); Meta (plano com metas, método, logística, cronograma, papéis de moderador e anotador, roteiro, consentimento, telemetria de poucos eventos); IXDF (FAQ: "5 a 8 jogadores por sessão", várias sessões ao longo do desenvolvimento).
- **Correção ao pesquisador:** o número 5 a 8 vem do FAQ do IXDF; as páginas do Meta e do Level Design Book não trazem cifra de amostra. Tratar o número como referência comercial, não regra.
- **Conteúdo reutilizável (reescrito):**
  Plano: objetivo e hipótese; público; build/commit; método (presencial ou remoto, moderado ou não); papéis; roteiro e briefing; dados a coletar (poucos eventos); consentimento. Relatório: sessão (build, foco, hipótese); primeiras impressões; tabela de bugs (crash, queda de frame, softlock, passos para reproduzir); pain points (só sensação, sem misturar com defeito); dados quantitativos; roteamento (design, balanceamento, bug, polish) com próximo passo; comparação com os pilares; "não avaliado" quando faltar dado. Comparar o que o jogador disse com o que fez.
- **Ressalvas:** playtest automatizado sem fonte validada (lacuna). Licenças dos textos não declaradas: só destilação.
- **Verificação:** WebFetch de 4 páginas; o ixdf e as demais lidas hoje.

### V-29 — Critério de aceite por execução do jogo (godogen como padrão, sem executar) (origens R-github-10, R-community-21) — Classe B · Prompt-score 83
- **Lentes:** G, C. **Tipo:** workflow + pattern. **Fonte:** https://github.com/htdt/godogen · **Autor/Org:** htdt.
- **Sinais (Verificado):** 7.079 estrelas, 658 forks, MIT, push em 2026-10-01 (API); HN "Show HN" com 337 pontos e 205 comentários em 2026-03-16 (Algolia); requisitos: Godot 4 .NET, Rust/Cargo (Bevy), Node 20+ (22.12+ para Babylon.js), Python 3, Chrome com WebGL2, chaves de API pagas (Google ou xAI para imagem, Tripo para 3D), pacotes de sistema; o agente julga pelo jogo rodando (URL ao vivo ou clipe gravado); modo supervisionado e modo sem supervisão com vídeo de prova de 15 a 20 s; pasta `engines/` com um guia por engine.
- **Conteúdo reutilizável (reescrito):** "A cada iteração: rodar o jogo, capturar evidência (captura ou clipe curto), listar defeitos visíveis e só então marcar a tarefa como feita. Compilar sem erro não é prova." Estrutura de guia por engine: `engines/<nome>.md` com comandos de build, check e captura.
- **Ressalvas (segurança):** o sistema gera assets com chaves pagas e executa código; **não instalar, não executar, não virar hook**. Aproveitar só o padrão. A referência a Opus 4.6 só aparecia em resultado de busca (não confirmada).
- **Verificação:** API do repositório, página do repositório, Algolia.

### V-30 — Oráculos e sondas de teste no próprio jogo (caso Amiga para Godot) (origem R-community-20, A9, A13) — Classe B (rebaixada de A) · Prompt-score 83 (original 73)
- **Lente:** C. **Tipo:** workflow + checklist. **Fonte:** https://babyloniantwins.com/blog/porting-a-1993-amiga-game-to-godot/ · **Autor/Org:** blog pessoal (BitHunch LLC).
- **Motivo do rebaixamento:** autoria individual, texto sem licença aberta (© declarado), números do próprio autor; mas HN 381 pontos e 133 comentários (Algolia, 2026-09-03) e técnicas transferíveis. Por 2 + 2 + 2 + 1 + 0 na régua, nota 6 a 7: classe B.
- **Sinais e correções (Verificado):** data do post 01/09/2026; flags `--level`, `--pose`, `--drive`, `--probe`, `--screenshot` para o modelo testar sem humano; o rebuild do binário original ficou idêntico, mas partes de área variável diferiam em cerca de 108 bytes (o autor atribui a um snapshot de memória, sem checar); a comparação pixel a pixel (zero pixels diferentes) foi dos níveis de 1993 renderizados contra capturas de 2020, **não do port moderno, que o autor revisou a olho**; cerca de 21 min do projeto vazio a um personagem jogável em C++ (o autor diz que ajustar a sensação levou cerca de três dias); o autor afirma que nada verificou se o jogo "parecia certo".
- **Conteúdo reutilizável (reescrito):** (1) expor flags de teste no jogo (`--level`, `--drive` com entrada por script, `--probe` com estado interno, `--screenshot`) antes de pedir mecânicas novas; (2) dois checks headless: compilar todos os scripts e carregar todos os níveis relatando falhas; (3) quando existe referência (binário, captura, saída esperada), comparar em vez de olhar; (4) registrar sensação, áudio e "parece certo" como pendência humana; (5) manter constantes ajustadas à mão no tick original.
- **Ressalvas:** é um caso de port de jogo existente; para jogo novo não há oráculo, só sondas.
- **Verificação:** WebFetch da página (7 de 8 pontos confirmados) e Algolia.

### V-31 — CLAUDE.md para Unity com editor via MCP (origens R-community-17, R-community-18, A2) — Classe B · Prompt-score 83 (original 70)
- **Lente:** C. **Tipo:** claude-md-rule + checklist. **Fontes:** https://github.com/IvanMurzak/Unity-MCP/blob/main/Unity-MCP-Plugin/CLAUDE.md ; https://devinreimer.substack.com/p/building-a-solid-claudemd-for-unity.
- **Sinais (Verificado):** Unity-MCP: 4,4 mil estrelas, 392 forks, Apache-2.0 (página), mínimo Unity 2022.3; regras: chamadas da API Unity passam por `MainThread.Instance.Run()`; testes EditMode e PlayMode em pastas de testes do pacote; caminho do projeto sem espaços; durante a recompilação o MCP não responde, então ler `Editor.log` do disco. Devin Reimer (publicado em 26/02/2026, o autor diz que as regras são subjetivas): scripts temporários de editor em pasta própria e apagados no fim da tarefa; GameObjects e prefabs por MCP, não por YAML; evitar `GetComponent`/`GetChild` em runtime; eventos com delegate vazio; `Debug.LogError` onde a falha seria grave; não suprimir warning com `#pragma`; executar passos de editor via MCP em vez de devolver ao usuário; terminar com mensagem de conclusão.
- **Conteúdo reutilizável (reescrito):** use o bloco "Regras" do V-16 e acrescente, para projetos com MCP de editor: conferir status da conexão; se o editor estiver compilando, aguardar e ler `Editor.log`; scripts temporários em `Editor/TemporaryGeneratedScripts` removidos ao final; nunca editar YAML de cena ou prefab à mão; pedir aprovação antes de apagar assets. Campo "Pipeline de render: <URP|HDRP|Built-in>" e "Input: <Input System|legacy>" a preencher.
- **Ressalvas:** "passos de editor executados pelo agente" exige que a pessoa aprove essa autonomia; sem MCP, a regra não vale. O arquivo de Unity-MCP aponta para `docs/claude/*.md` não lidos. Segurança: o repositório menciona `start_mcp_inspector.bat`; não executar sem aprovação.
- **Verificação:** WebFetch das duas páginas e da página do repositório.

### V-32 — CLAUDE.md de Godot 4 (GDScript) consolidado e revalidado (origens A1 da lente community, R-community-11/12/13, R-github-07) — Classe B (base derivada de fontes A) · Prompt-score 85 (original 72)
- **Lentes:** C, G. **Tipo:** claude-md-rule. **Fontes de apoio verificadas:** guia de estilo (V-11), CLI (V-12), referência de TileMap (https://docs.godotengine.org/en/stable/classes/class_tilemap.html), física (V-14). Fontes de terceiros usadas só como sinal: thepromptshelf.dev (25/08/2026), vegcale.com (12/07/2026), claudecodeguides.com (20/04/2026), BlueBirdBack/godot-cursorrules (Godot 4.4, último push 2025-03-25).
- **Conteúdo reutilizável (reescrito; cada linha tem fonte oficial ou está rotulada):**
  ```markdown
  # <projeto> — Godot 4.x (GDScript)   [fixar a versão exata: godot --version]
  ## Comandos (da raiz)
  - Importar em checkout limpo: godot --headless --path . --import
  - Sintaxe de um script: godot --headless --path . --check-only -s res://scripts/x.gd
  - Testes: <GUT ou GdUnit4: escolha um>; lint: <gdlint/gdformat, se o projeto usa gdtoolkit>
  ## Regras (estilo oficial)
  - Tipar variáveis, parâmetros e retornos; := só com tipo óbvio; tratar null após `as`.
  - snake_case (arquivo, função, variável, sinal), PascalCase (classe), CONSTANT_CASE; sinal no passado.
  - Filhos com @onready tipado; não procurar nós em _process.
  - Movimento e física em _physics_process; move_and_slide() não recebe velocidade * delta.
  - Dados compartilhados em Resource (.tres); autoload só para estado global único.
  - TileMap está deprecated: use TileMapLayer.   [a página da classe confirma; a versão que o depreciou não foi confirmada]
  - Não editar .godot/ nem addons/.
  ## Pronto
  - Os comandos acima saíram com 0 e sem ERROR no log; cena principal abre; pendências de sensação/áudio listadas.
  ```
- **Ressalvas:** os pontos "uma classe State por estado", "sinais em vez de globals" e "EventBus" vêm de terceiros e **não** foram incluídos como regra firme (são padrões de design, não de estilo). thepromptshelf tem sinais de conteúdo gerado em massa (artigos relacionados com datas posteriores à do artigo, variável `$CLAUDE_FILE_PATH` não confirmada): rejeitado como fonte. Alegações de economia de tokens (claudecodeguides) rejeitadas.
- **Verificação:** cada linha acima conferida na documentação oficial correspondente.

### V-33 — Plugin oficial da Unity para Claude Code (referência, sem regras) (origem R-community-16) — Classe B (promocional)
- **Lente:** C. **Tipo:** reference. **Fonte:** https://unity.com/blog/unity-plugin-for-claude-code · **Autor/Org:** Unity (Rachel Zhao, 09/09/2026).
- **Sinais (Verificado):** 29 skills em 9 domínios (primeiros passos e CLI, UI e texto, 2D, gráficos e render, áudio, cena e gameplay, monetização, multiplayer, plataforma e localização), `/unity-cli`; a página **não** cita MCP e não traz medição para "menos erros, menos tokens, menos turnos".
- **Uso:** lista de domínios como checklist de cobertura da skill Unity do plugin; **não** derivar regras sem testar o plugin. Nada instalado.
- **Verificação:** WebFetch.

### V-34 — Convenções de skill de engine com versão declarada (quodsoler/unreal-engine-skills) (origem R-authoritative-20) — Classe B · Prompt-score 83
- **Lente:** A. **Tipo:** skill (formato) + checklist. **Fonte:** https://github.com/quodsoler/unreal-engine-skills · **Autor/Org:** quodsoler.
- **Sinais (Verificado):** 363 estrelas, 60 forks, MIT, push em 2026-09-28; 27 skills (a contagem "31" do corpo está desatualizada); mira UE 5.8 e diz ter conferido nos headers (não verificado de forma independente); regras de contribuição: `name` igual à pasta, `description` entre aspas e começando com "Use when" com gatilhos e skill irmã, `metadata` com `version` e `engine`, SKILL.md até 500 linhas, `references/` linkado, tabela "Deprecated — do not use" por skill; comandos de instalação (`npx`, `git submodule`, `cp`) são para o usuário rodar.
- **Conteúdo reutilizável (reescrito):** checklist de frontmatter de skill de engine: [ ] `name` == pasta; [ ] `description` com "Use when" + gatilhos PT-BR e EN + engine e versão; [ ] `metadata.engine` e `metadata.version`; [ ] tabela de APIs depreciadas com a versão que as trocou; [ ] referências linkadas direto; [ ] avaliação com e sem a skill (V-08).
- **Ressalvas:** 363 estrelas dá 0 pontos de sinal comunitário; não li skill por skill.
- **Verificação:** API + página.

### V-35 — Catálogos de skills de terceiros (somente referência, sem hooks nem instalação) (origens R-authoritative-19, R-github-06/08/09/17/18, R-community-06/15) — Classe B/C (rebaixados de B)
- **Lentes:** A, G, C. **Tipo:** reference. **Observações verificadas (2026-10-10):**
  - **wshobson/agents** (`plugins/game-development`): 40.318 estrelas, 4.294 forks, MIT, push em 2026-10-05; pasta do plugin tem `.claude-plugin/`, `.codex-plugin/`, `agents/`, `skills/`. As estrelas são do marketplace inteiro. Skill `godot-gdscript-patterns` lida: frontmatter `name` + `description` ("Master Godot 4 ... Use when ..."), mostra `class_name`/`extends`, sinais tipados, `@export_range`/`@export_group`, `@onready`, `move_and_slide()` em `_physics_process`, clamp de vida; sem verificação nem avaliação; versão "Godot 4.x". Skill `unity-ecs-patterns` lida: `ISystem` em vez de `SystemBase`, Burst, command buffer, evitar tipos gerenciados, descartar coleções nativas, **"Aspects"** (provável API removida/depreciada em versões novas do Entities; **Não verificado**, a página oficial da Entities 1.3.15 não trata disso); versão do pacote Entities não declarada. Classe B (descartar Aspects até conferir).
  - **jame581/GodotPrompter**: 806 estrelas, 47 forks, MIT, 56 skills (core/processo 8, arquitetura 6, física/2D/3D/XR 4, sistemas de gameplay 13, UI 3, multiplayer 3, render 2, build e deploy 5, scripting 4, nativo e performance 2, matemática 1, addons de terceiros 5), 519 commits; **SessionStart hook** que injeta cartão de roteamento ao detectar `project.godot` (o README diz não ter rede nem escrita; não inspecionei o código). Ajuda a formar o índice de domínios.
  - **thedivergentai/GD-Agentic-Skills**: 823 estrelas, 53 forks, **LGPL-3.0**, push em 2026-09-09; alvo Godot 4.7+; 99 skills, 27 blueprints de gênero, personas (Master, Analyst, Auditor, Builder, Artificer, Agent Vision); alerta contra instalar tudo (`--all`) por sobrecarga de contexto; usa `npx skills add`. Copyleft: só princípios.
  - **Zate/cc-godot**: 18 estrelas, 6 forks, MIT (README), 6 commits; `/gd:setup`, `/gd:init-game`, `/gd:run`, `/gd:stop`; agente `game-planner`; **hook SessionStart** e geração de `.mcp.json`; setup manual pede clonar um servidor MCP cuja URL é placeholder. Classe C: não copiar hook nem `.mcp.json`.
  - **PatrickJS/awesome-cursorrules**: 40.891 estrelas, CC0-1.0 (API; o pesquisador achou que não havia licença, o README de fato não a cita), push em 2026-05-30; entradas de jogo: ASCII Simulation Game, DragonRuby, GameMaker GML, Unity (C#); nada de Godot ou Unreal. Classe C para este segmento; arquivo `.mdc` de Unity não aberto.
- **Uso:** índice de domínios (GodotPrompter), nomes de personas (GD-Agentic), formato (wshobson, V-34). Nada disso entra no plugin como código.

### V-36 — Anti-padrões de agentes de jogo (origens R-authoritative-21 corrigido, R-community-22, R-community-23, A11) — Classe C · uso: casos negativos para o avaliador de prompts
- **Lentes:** A, C. **Tipo:** anti-pattern.
- **Fontes verificadas:** davila7/claude-code-templates (agente `unity-game-developer`, repositório com 32,5 mil estrelas e MIT na página); dev.to/datadeer (Lucca Sanwald, publicado em 22/06/2025, editado depois); mirror de Reddit (r/ClaudeAI, 2 pontos, 6 comentários).
- **Correção ao pesquisador:** o agente do davila7 **cita** versão (Unity 2022.3 LTS+) e pipelines (URP e HDRP); os defeitos reais são: persona genérica com "8+ anos", seis áreas de expertise amplas, ausência de comandos de verificação e de critérios de aceite, `description` que diz "triggers proactively" sem gatilho concreto.
- **Lista de anti-padrões (paráfrase própria):** (1) papel amplo sem versão do projeto, comando de check nem critério de pronto; (2) pedir o jogo inteiro numa tarefa só (contexto estoura, sobra trabalho pela metade); (3) declarar pronto sem a lista de funcionalidades; (4) prompt curto e vago que gera código plausível e errado; (5) design fora do repositório: o agente imita o código vizinho; (6) perder o entendimento do próprio código (um autor abandonou o projeto por isso); (7) tratar teste de lógica como prova de jogabilidade; (8) CLAUDE.md gigante, regra com MAIÚSCULAS em tudo.
- **Verificação:** raw do agente, páginas e mirror lidos.

## Pontuação D1–D12 dos artefatos reutilizáveis (versão reescrita)

Escala 0 a 5 por dimensão; total = soma × 100 / 60. Todos sem critério de reprovação automática (nenhum manda inventar resultado, autorizar deploy/push sem confirmação, obedecer conteúdo externo, copiar sem licença, ou vazar segredo). Pontuação feita por mim com leitura do texto reescrito; justificativas resumidas pelas fraquezas dominantes.

| Item | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | D11 | D12 | Total | Fraqueza dominante |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V-01 | 4 | 4 | 5 | 4 | 3 | 4 | 5 | 4 | 5 | 5 | 4 | 5 | 87 | poucos exemplos |
| V-03 | 4 | 4 | 4 | 4 | 3 | 4 | 4 | 5 | 5 | 5 | 4 | 5 | 85 | sem exemplo de delegação |
| V-04 | 5 | 4 | 5 | 4 | 4 | 4 | 5 | 4 | 4 | 5 | 4 | 4 | 87 | transposição a jogos Inferido |
| V-05 | 4 | 4 | 5 | 4 | 3 | 5 | 5 | 4 | 4 | 5 | 3 | 4 | 83 | prompt do avaliador é Inferido |
| V-06 | 4 | 4 | 4 | 4 | 4 | 4 | 5 | 4 | 4 | 5 | 4 | 4 | 83 | exemplos de jogo Inferido |
| V-07 | 4 | 4 | 4 | 4 | 3 | 4 | 5 | 3 | 5 | 5 | 4 | 5 | 83 | pouca segurança de skill |
| V-08 | 4 | 4 | 4 | 4 | 4 | 3 | 5 | 4 | 4 | 5 | 4 | 4 | 82 | scripts a revisar |
| V-09 | 4 | 4 | 4 | 5 | 4 | 3 | 4 | 4 | 4 | 5 | 3 | 4 | 80 | formato de saída genérico |
| V-10 | 4 | 4 | 5 | 4 | 3 | 4 | 5 | 4 | 4 | 5 | 4 | 3 | 82 | analogia compilador a jogo |
| V-11 | 4 | 4 | 5 | 4 | 4 | 3 | 4 | 4 | 5 | 5 | 4 | 5 | 85 | sem formato de saída |
| V-12 | 4 | 4 | 5 | 4 | 3 | 4 | 5 | 4 | 4 | 5 | 4 | 4 | 83 | comandos não executados |
| V-13 | 4 | 4 | 5 | 4 | 3 | 4 | 5 | 4 | 4 | 5 | 4 | 4 | 83 | sem exemplos |
| V-14 | 4 | 4 | 4 | 4 | 3 | 3 | 5 | 3 | 4 | 5 | 4 | 5 | 80 | sem formato de saída |
| V-15 | 4 | 4 | 5 | 4 | 3 | 4 | 5 | 5 | 4 | 5 | 3 | 4 | 83 | Unity sem fonte para validar RPC |
| V-16 | 4 | 4 | 5 | 4 | 3 | 3 | 5 | 4 | 5 | 5 | 4 | 5 | 85 | sem formato de saída |
| V-17 | 4 | 4 | 5 | 4 | 3 | 4 | 5 | 4 | 4 | 5 | 4 | 4 | 83 | sem exemplos |
| V-18 | 4 | 4 | 4 | 4 | 3 | 3 | 4 | 4 | 4 | 5 | 4 | 5 | 80 | fonte de 2020 |
| V-19 | 4 | 4 | 5 | 4 | 4 | 3 | 4 | 4 | 5 | 5 | 3 | 5 | 83 | sem Blueprints |
| V-20 | 4 | 4 | 4 | 4 | 3 | 3 | 4 | 4 | 4 | 5 | 4 | 5 | 80 | sem detalhe de replicação |
| V-22 | 4 | 5 | 5 | 4 | 3 | 4 | 5 | 5 | 4 | 5 | 4 | 4 | 87 | original usa MAIÚSCULAS |
| V-23 | 4 | 5 | 5 | 5 | 3 | 5 | 5 | 5 | 4 | 5 | 3 | 3 | 87 | depende de docs do projeto |
| V-24 | 4 | 4 | 5 | 4 | 3 | 4 | 5 | 5 | 4 | 5 | 4 | 4 | 85 | sem exemplo |
| V-25 | 5 | 5 | 5 | 4 | 3 | 5 | 5 | 4 | 4 | 5 | 5 | 3 | 88 | acoplada a pastas do original |
| V-26 | 4 | 4 | 5 | 4 | 3 | 5 | 4 | 4 | 4 | 5 | 5 | 4 | 85 | exige campo Type |
| V-27 | 4 | 4 | 5 | 4 | 3 | 5 | 4 | 4 | 4 | 5 | 5 | 4 | 85 | sem balanceamento |
| V-28 | 4 | 4 | 4 | 4 | 4 | 5 | 4 | 4 | 4 | 5 | 4 | 4 | 83 | cifra de amostra comercial |
| V-29 | 4 | 4 | 4 | 4 | 3 | 4 | 5 | 4 | 4 | 5 | 4 | 5 | 83 | só o padrão é usável |
| V-30 | 4 | 4 | 5 | 4 | 3 | 4 | 5 | 4 | 4 | 5 | 4 | 4 | 83 | números do autor |
| V-31 | 4 | 4 | 5 | 4 | 3 | 3 | 4 | 4 | 5 | 5 | 4 | 5 | 83 | exige MCP |
| V-32 | 4 | 4 | 5 | 4 | 3 | 4 | 5 | 4 | 4 | 5 | 4 | 5 | 85 | só uma engine |
| V-34 | 4 | 4 | 5 | 4 | 3 | 3 | 4 | 4 | 5 | 5 | 4 | 5 | 83 | sem exemplo de frontmatter |

Média dos 31 artefatos: 83,8. Média estimada dos originais (como coletados): cerca de 72, com os piores em V-05 (63), V-09 (60), V-06 e V-18 (67), porque eram snippets ou resumos sem formato de saída, verificação nem tratamento de ausência.

## Rejeitados e rebaixados

| Item | Decisão | Motivo |
| --- | --- | --- |
| R-authoritative-12 (Unity ScriptableObjects) | Rebaixado A para B (V-18) | Página marca "Last updated January 2020". |
| R-authoritative-13 (Netcode) | Aprovado com correção (V-15) | A página de autoridade não fala em validar ServerRpc nem `IsHost`; spawn/despawn está na página de ownership; validação de RPC é do Godot. |
| R-authoritative-10 (Godot perf) | Aprovado com correção (V-13) | "Evitar chamadas que bloqueiam o servidor a cada frame" não está na página. |
| R-authoritative-11 (Unity runtime) | Aprovado com correção (V-16) | "Zero bytes por frame" não consta no manual 6000.0 (diz "evitar"); limite de `name` de subagente era outro campo. |
| R-authoritative-17 (FSM x BT, GDC Isla) | Rejeitado como base | Classe C; a agenda do GDC retornou 403 e os slides nunca foram abertos. Substituído por pista concreta em "Lacunas" (Game AI Pro). |
| R-authoritative-18 (GDQuest) | Rejeitado | Classe C, texto antigo, não reaberto; o guia oficial (V-11) cobre as mesmas regras. |
| R-authoritative-19 (wshobson Godot skill) | Rebaixado a referência (V-35) | Estrelas são do marketplace; sem avaliação; descrição do catálogo confusa. |
| R-authoritative-21 (davila7) | Rebaixado a anti-padrão C (V-36) e corrigido | O agente cita versão e pipeline; faltam verificação e critério de aceite. |
| R-authoritative-22 (playtest em snippets) | Aprovado depois de aberto (V-28) | Páginas abertas hoje; cifra 5 a 8 é só do IXDF. |
| R-authoritative-23 (índice Anthropic sem skill de jogos) | Rebaixado a nota | Verificado (180.246 estrelas, licença `null`); sem skill de jogos no acervo: usado em "Cobertura". |
| R-github-06 (wshobson game-development, não lido) | Rebaixado (V-35) | Só pastas listadas; conteúdo de `agents/` desconhecido. |
| R-github-07 (BlueBirdBack godot-cursorrules) | Rejeitado | Classe C: 119 estrelas, último push em 2025-03-25 (mais de 18 meses), mira Godot 4.4, formato legado; as regras úteis têm fonte oficial (V-11, V-32). |
| R-github-08 (GodotPrompter) | Rebaixado a referência (V-35) | Conteúdo das skills não lido; tem hook SessionStart. |
| R-github-09 (GD-Agentic) | Rebaixado a referência (V-35) | LGPL-3.0, conteúdo não lido, alegação 4.7+ não cruzada. |
| R-github-14 (cryptorabea Unity) | Rejeitado | 3 estrelas, 1 commit; só README; V-16 e V-31 cobrem melhor. |
| R-github-15 (pluginagentmarketplace) | Rejeitado | 36 estrelas, licença personalizada ("Custom License"), conteúdo genérico de papéis. |
| R-github-16 (overlook-game-framework) | Rejeitado | 9 estrelas, sem regras para agentes de IA (o próprio pesquisador anotou), específico de um framework. |
| R-github-17 / R-community-15 (cc-godot) | Rebaixado a referência C (V-35) | 18 estrelas; hook SessionStart e `.mcp.json`; URL de dependência é placeholder. |
| R-github-18 (awesome-cursorrules) | Rebaixado a referência C (V-35) | Sem Godot ou Unreal; licença no pesquisador estava errada (CC0-1.0 pela API). |
| R-community-06 (wshobson skills) | Rebaixado/mesclado (V-35) | Alegação "Aspects" em ECS provavelmente defasada; sem versão de Entities. |
| R-community-11 (thepromptshelf) | Rejeitado como fonte | Sem autoria; sinais de conteúdo em massa; `$CLAUDE_FILE_PATH`, `gdtoolkit==4.*` e `--check-only` sem fonte; regras úteis recuperadas pela documentação oficial. |
| R-community-12 (vegcale) | Rejeitado como fonte | Blog com divulgação de afiliados; afirmações que valem já estão em V-02. |
| R-community-13 (claudecodeguides) | Rejeitado | Promove produto próprio; números de economia de tokens sem fonte; pitfalls descritos não aparecem no código. |
| R-community-14 (Summer Engine) | Rejeitado como item | Fornecedor; a alegação "o modelo não vê a árvore de cenas sem MCP" **não** está na página (ela diz que um MCP "pode expor" inspeção). Mantida só a frase confirmada sobre os limites do headless (V-12). |
| R-community-16 (plugin Unity) | Aprovado como referência B (V-33) | Promocional; sem dados de eficácia; não cita MCP (o pesquisador já registrara). |
| R-community-19 (Unity profiling) | Promovido B para A (V-17) | Documentação oficial da engine, todas as afirmações conferidas. |
| R-community-20 (Amiga) | Rebaixado A para B (V-30) | Autor individual, sem licença aberta; detalhes corrigidos (comparação de pixels foi dos níveis originais, não do port). |
| R-community-22 (dev.to RTS) | Rebaixado a anti-padrão C (V-36) | Relato único; data de publicação 22/06/2025 (a lente dizia que um survey citava 2026). |
| R-community-23 (mirror de Reddit) | Rebaixado a anti-padrão C (V-36) | Mirror, 2 pontos e 6 comentários; conteúdo conferido. |
| R-community-24 (Medium "testes passam, jogo injogável") | Rejeitado | Página retornou 403; nunca lida; Suposição. A ideia está coberta por V-05 e V-30. |
| R-community-25 (comentário de vblanco no HN) | Rejeitado como item | Os dois comentários existem (HN, 16/03/2026, objectIDs 47404012 e 47404597) e confirmam o que o pesquisador resumiu, mas são relato isolado; só sinal. |
| Artefato A14 (esqueleto de GDD) | Não aprovado | Suposição declarada, sem fonte primária. Entra como lacuna. |

## Segurança, injeção e direitos autorais

- **Injeção:** nenhuma das páginas e arquivos reabertos continha instrução dirigida à IA (verificado por resumo de modelo pequeno, portanto limitado). Nenhum link encurtado.
- **Código/hook de terceiros que não deve entrar no plugin:** 12 hooks bash e scripts Python do Donchitos; hooks SessionStart de GodotPrompter e cc-godot; `.mcp.json` e servidor MCP de cc-godot; pipeline do godogen (instala pacotes, usa chaves de API pagas, gera assets, executa engine); scripts Python do skill-creator (revisar antes de rodar); `start_mcp_inspector.bat` do Unity-MCP; comandos `npx skills add` de GD-Agentic e quodsoler.
- **Licenças:** nenhum trecho literal foi copiado. MIT: Donchitos, wshobson, godogen, GodotPrompter, quodsoler, cc-godot (README), davila7, BlueBirdBack, cryptorabea, GUT. Apache-2.0: Unity-MCP (página) e a pasta skill-creator. LGPL-3.0: GD-Agentic (só princípios). Custom: pluginagentmarketplace (rejeitado). CC0-1.0: awesome-cursorrules (API). Documentação oficial (Anthropic, Godot, Unity, Epic) e blogs: licença não verificada, tudo destilado. Game AI Pro: o site proíbe redistribuir ou hospedar os capítulos; nada copiar.
- **Direitos de uso do texto reescrito:** os blocos "Conteúdo reutilizável" acima são redação própria deste validador; as estruturas (JSON de funcionalidade, tabela de tipos de teste, vereditos) são ideias, não texto.

## Mapa de cobertura do escopo

| Subtema | Itens V | Situação |
| --- | --- | --- |
| Godot / GDScript | V-11, V-12, V-13, V-14, V-15, V-24, V-32 | Bem coberto (estilo, CLI, testes, performance, física, multiplayer). Falta: GUT sem execução, UI e shaders. |
| Unity / C# | V-15, V-16, V-17, V-18, V-21, V-31, V-33 | Coberto em runtime, profiling, netcode, arquitetura. Faltam: `-runTests` por CLI, Addressables, UI Toolkit. |
| Unreal / C++ e Blueprints | V-19, V-20, V-34 | Parcial: C++ e Gameplay Framework; Blueprints, GAS e replicação detalhada sem fonte. |
| Game loop e timestep | V-14 | Coberto. |
| Física | V-14 (Godot) | Parcial: Unity e Unreal sem leitura. |
| ECS / DOTS | V-35 (wshobson) | Fraco: skill de terceiro com possível API defasada; sem doc oficial de Entities lida. |
| IA de jogo (FSM, behavior tree) | nenhum | Lacuna. Pista: Game AI Pro, Vol. 1, cap. 6 (verificado que existe, gratuito, sem redistribuição; conteúdo não lido). |
| Game design (GDD, balanceamento, economia) | V-27 (revisão de GDD) | Parcial: só revisão de GDD; criação de GDD e balanceamento sem fonte validada. |
| Performance e profiling | V-13, V-17, V-25 | Bem coberto. |
| Netcode | V-15 | Parcial (Unity NGO + Godot); Unreal e rollback sem fonte. |
| Pipeline de assets | nenhum | Lacuna. |
| Shaders | nenhum | Lacuna. |
| UI de jogo | V-33 (só lista de domínios Unity) | Lacuna. |
| Testes e QA | V-06, V-10, V-12, V-21, V-26 | Coberto para Godot e geral; Unity por CLI não verificado. |
| Playtesting e telemetria | V-28 | Coberto no processo; automação de playtest sem fonte. |
| Publicação / export | nenhum | Lacuna. |
| Harness para projetos longos | V-04, V-05, V-29, V-30 | Bem coberto. |
| Skills, subagentes, CLAUDE.md | V-01, V-02, V-03, V-07, V-08, V-09, V-22 a V-24, V-34 | Bem coberto. |

Seis dos 17 subtemas não têm item aprovado (IA de jogo, pipeline de assets, shaders, UI de jogo, publicação, criação de GDD/balanceamento) e ECS tem cobertura fraca. O núcleo do plugin (agentes de engine, verificação, performance, netcode, harness) está bem apoiado.

## Lacunas objetivas e pesquisáveis (para nova rodada)

1. **Unreal Blueprints/GAS:** abrir a documentação oficial de Blueprints na Epic (dev.epicgames.com/documentation, seções "Blueprints Visual Scripting" e "Gameplay Ability System"), com versão 5.8; nenhuma fonte oficial lida.
2. **Replicação no Unreal:** documentação oficial de networking e replicação (Actor Replication, RPCs) e checklist de autoridade equivalente ao V-15.
3. **IA de jogo:** ler Game AI Pro Vol. 1, cap. 6 ("The Behavior Tree Starter Kit", Champandard e Dunstan) e cap. 10 (utilidade em BT), e decidir FSM x BT a partir do texto; abrir a palestra de Damian Isla (GDC) em vez de agenda.
4. **Shaders:** documentação oficial de linguagem de shader do Godot, Shader Graph da Unity e Materiais do Unreal (uma regra de revisão por engine); sem item hoje.
5. **UI de jogo:** documentação oficial de Control/containers do Godot e UI Toolkit/uGUI da Unity; regras de ancoragem, escala e foco para gamepad.
6. **Pipeline de assets:** guias oficiais de importação (Godot "Import process", Unity importers/Addressables, Unreal Content Browser/naming) e convenções de nomenclatura; ler `asset-audit` do Donchitos no raw (só havia snippet).
7. **Publicação:** exportação do Godot, builds do Unity, e requisitos de loja (documentação Steamworks e de lojas móveis); checklist de build de release.
8. **GDD e balanceamento:** fonte primária para criação de GDD e economia (faucets e sinks, curvas): procurar material de design de jogos com autoria reconhecida; hoje A14 é Suposição.
9. **Unity por CLI:** abrir a página do Test Framework que lista `-runTests`, `-batchmode`, `-testPlatform` (a URL tentada deu 404); e a Entities (Upgrade Guide) para confirmar o destino de "Aspects".
10. **Física em Unity e Unreal:** FixedUpdate/Rigidbody e Chaos Physics, para completar V-14.
11. **Playtest automatizado e rede determinística:** sem fonte validada.
12. **Reddit oficial, X, YouTube, palestras do GDC:** não lidos por nenhuma lente (cotas de busca); novo ciclo de pesquisa com cota nova.

## Recomendações ao construtor

**Skills (SKILL.md com description em PT-BR e EN, versão da engine no frontmatter):**
- `game-perf-audit` (base V-25 + V-17 + V-13): orçamento do projeto, veredito NÃO AVALIADO, profiling por engine.
- `game-qa-plan` (V-26 + V-28): tipos de teste, smoke e playtest.
- `gdd-review` (V-27): rubrica de 4 dimensões; criação de GDD só depois de fonte validada.
- `godot-gdscript` (V-11, V-12, V-14, V-32), `unity-csharp` (V-16, V-17, V-18, V-21, V-31), `unreal-cpp` (V-19, V-20), cada uma com tabela de APIs depreciadas (V-34) e avaliação com e sem skill (V-08).
- `game-netcode-review` (V-15).
- `game-verify-by-running` (V-29 + V-30 + V-10): critério de aceite por execução, sondas, oráculos.

**Agentes:** `gameplay-programmer` (V-23), `engine-specialist` com checagem de versão (V-24), `gameplay-reviewer` somente leitura (V-03), `game-evaluator` cético para o fim do trabalho (V-05). Subagentes de plugin ignoram `hooks`, `mcpServers` e `permissionMode`.

**Comandos:** `/game:verify` (V-12, V-29), `/game:init-session` (rotina de V-04), `/game:playtest-report` (V-28). Sem hooks ativos no plugin; documentar hooks opcionais em `references/` (por ex. check headless após editar) com instrução de habilitação consciente.

**Checklists em `references/`:** estilo GDScript (V-11), performance (V-13, V-17), netcode (V-15), Unreal (V-19), revisão de skill (V-07), anti-padrões (V-36), catálogo de terceiros (V-35) com avisos de segurança.

**Regras de CLAUDE.md (templates do plugin):** esqueleto de jogo (V-01), Godot (V-32), Unity (V-31), Unreal (V-19, V-20), protocolo de colaboração (V-22), com regra de organização do V-02 (por caminho, abaixo de 200 linhas).

**Biblioteca de prompts:** matriz de gatilho (V-08), modelo de tarefa de avaliação (V-06), prompt de avaliador (V-05), `features.json` (V-04), XML para GDD (V-09).

**Cuidados:** não promover como fato as alegações de eficácia de repositórios (Donchitos, godogen, GodotPrompter, plugin da Unity); rotular Inferido a transposição de artigos web para jogos; sensação de jogo, áudio e legibilidade visual sempre como pendência humana.

## Veredito

36 itens aprovados de boa qualidade (prompt-score médio 83,8; 19 classe A), núcleo do plugin bem coberto, mas seis subtemas sem item aprovado (IA de jogo, pipeline de assets, shaders, UI de jogo, publicação, criação de GDD/balanceamento) e Unreal/ECS fracos. Leitura estrita da regra ("cobertura razoável de todos os subtemas") daria `needs_more`; como o núcleo está sólido e as lacunas são objetivas e pesquisáveis (lista acima), o veredito registrado é **pass_with_gaps**.
