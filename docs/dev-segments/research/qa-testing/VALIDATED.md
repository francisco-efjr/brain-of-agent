# QA e testes — consolidado VALIDADO (qa-testing)

Data: 2026-10-10 · Validador: claude-sonnet-5-5 (independente: modelo diferente dos pesquisadores, claude-haiku-5-5, mas da mesma família Anthropic; por isso toda afirmação foi reconferida na fonte primária e não por concordância entre lentes) · Contexto: validação de prompt (rubrica D1–D12) e de fontes (rubrica 0–10).

## Cabeçalho e estatísticas

| Lente | Recebidos | Aprovados (linhas) | Rebaixados | Rejeitados | Observação |
| --- | --- | --- | --- | --- | --- |
| authoritative | 28 | 27 | 1 (R-22 Sanity) | 0 | R-28 aprovado só como referência de existência |
| github | 24 | 18 | 3 (R-14, R-17, R-19) | 3 (R-16, R-22, R-24) | R-10 teve afirmação falsa corrigida |
| community | 25 | 16 | 9 | 0 | muitos itens duplicam as outras lentes |
| **Total** | **77** | **61** | **13** | **3** | 61 linhas aprovadas viram **41 itens únicos** (V-01 a V-41) após deduplicação entre lentes; 5 deles são descobertas do validador (V-21, V-24, V-25, V-26, V-27) e 3 foram ampliados por ele (V-10, V-16, V-22) |

- URLs re-verificadas com sucesso: **74** (docs oficiais, páginas de repositório, arquivos raw de SKILL.md, threads do HN). Itens tocados por re-verificação: 76 de 77 (98%; meta mínima 40%). Falhas registradas: `api.github.com/repos/*` retornou 403 e o limite de requisições da API bloqueou `curl`; `raw.githubusercontent.com/obra/superpowers/main/skills/test-driven-development/testing-anti-patterns.md` retornou 404 (o arquivo real é `writing-good-tests.md`); o artigo do Google sobre testes flaky só entrega comentários de leitores, sem corpo.
- Itens classe A re-verificados: todos (V-01 a V-11, V-18, V-19, V-20, V-21, V-23, V-24).
- Pontuação média de prompt/skill/regra (fontes originais, 12 artefatos pontuados, D1–D12): **73,9**. Versões reescritas neste arquivo (seção "Conteúdo reescrito"): meta de 85 ou mais, autoavaliada; reavaliar após os evals do plugin.
- Limitações desta validação: (a) estrelas e forks foram lidos nas páginas HTML dos repositórios; a API do GitHub ficou bloqueada, então datas de último commit/push não puderam ser reconferidas (a atualidade de repositórios ficou em 1 salvo prova); (b) o `WebSearch` do turno estava esgotado, então não houve descoberta nova por busca livre, só por navegação direta em páginas oficiais; (c) o número de estrelas de `anthropics/skills` (180,2 mil) vem da lente github e não foi reconferido por mim; (d) Reddit, X, YouTube, Medium, dev.to e newsletters continuam sem cobertura.

## Erros e alucinações encontrados nas lentes (resumo adversarial)

1. github R-10 (mattpocock/tdd) afirma "checklist de 10 itens lido no SKILL" e "ler GLOSSARIO e ADRs da área". Falso para `tdd/SKILL.md`: ele tem 4 seções (o que é bom teste, seams, anti-padrões, regras do ciclo) e 3 regras do ciclo; a leitura de GLOSSARY.md e ADRs pertence a `diagnosing-bugs`. Corrigido em V-33.
2. authoritative R-24 e community R-03 dizem que os anti-padrões (acoplado à implementação, tautológico, fatiamento horizontal) são "implicação" ou ausentes. Estão literalmente no SKILL.md. Corrigido.
3. community R-02 diz "quatro passos" no gate de verificação do superpowers; são **cinco** (github R-02 estava certo).
4. community R-17 diz que o TIL de Simon Willison sugere pedir ao Claude que faça login com as credenciais do usuário. Falso: o TIL recomenda que o próprio usuário digite as credenciais no navegador visível.
5. community R-15 e a tabela de conflitos dizem que "value card" não existe no gstack. Existe: `qa-only/SKILL.md` define "Value: protects=...; fails_when=...; why_new=...; seam=..." e `test-audit` tem value card e retirement card. O README só usa "evidence card" (authoritative R-25 estava certo quanto ao README).
6. github R-13 diz "5% da suíte" para quarentena. O texto diz mais de 5% **dos testes em quarentena** sinaliza problema sistêmico. Além disso, a `description` do SKILL começa com "Runtime per-test healing with evidence..." e não descreve triagem de flaky (gatilho fraco, D1).
7. github R-11 diz "mock só nas bordas". O arquivo diz para mockar na fronteira e preferir implementação real para funções puras, mas não diz "somente".
8. authoritative R-08 sugere que subagente não delega além do limite de profundidade. Na doc atual, aninhamento é permitido por padrão até 3 camadas (ajustável por variável de ambiente).
9. authoritative R-27 e github R-03 deixam a licença de `webapp-testing` em aberto. `LICENSE.txt` da pasta é Apache-2.0 (verificado). Isso muda a política de reuso de "só destilar" para "literal permitido com atribuição e aviso de modificação"; mesmo assim este arquivo destila.
10. authoritative R-22 chama o "95%" de retórica. O autor (Vincent Quigley, 02/09/2025) apresenta 95% e 50% como taxas de lixo na primeira e na segunda tentativa, auto-relatadas e anedóticas.
11. authoritative R-20 e community R-18 divergem em data de Willison: as páginas lidas não mostram data de publicação do capítulo. Tratado como "sem data".
12. community R-05 confirmado: a Anthropic descreve um único agente de codificação que verifica o próprio trabalho; avaliador cético separado aparece só como direção futura. O lead AO-20 não se sustenta.
13. community R-12 confirmado: o texto do Ralph não traz aviso de sandbox nem proibição de afrouxar testes. Essas regras do atlas são inferência, não conteúdo da fonte.
14. github R-16 diz "dez skills iniciais" no `qaskills`; a página lista 20 com notas auto-atribuídas sem metodologia.
15. github R-22 não registra que `Visma-Severa/QA-Agents` foi arquivado pelo dono em 11/06/2026.

## Itens aprovados

Convenção: Verificado = lido por mim nesta execução; Inferido = síntese minha; Suposição = hipótese sem leitura. Citações literais: nenhuma. Todo "conteúdo reutilizável" é destilação com redação própria.

### V-01 — Verificação com evidência e revisão adversarial no Claude Code (origem R-authoritative-02, R-github-06, R-community-07) — Classe A (8) · Prompt-score da fonte 88 (trecho do prompt de revisão contra PLAN.md)
- **Lente:** authoritative + github + community
- **Tipo:** claude-md-rule + checklist + workflow
- **Fonte:** https://code.claude.com/docs/en/best-practices · **Autor/Org:** Anthropic
- **Sinais:** documentação oficial atual (menciona Claude Code v2.1.283); sem data na página. Verificado.
- **Para que serve:** fechar o ciclo mudança, verificação, evidência em qualquer tarefa de QA.
- **Técnicas-chave (Verificado):**
  - Dar ao agente um check que devolva passa ou falha: suíte de testes, build, linter, script que compara saída com fixture, screenshot comparado a design.
  - Quatro graus de rigor: no prompt; condição de sessão `/goal` (avaliador separado reavalia a cada turno); gate determinístico com hook `Stop`; segunda opinião por subagente de verificação ou workflow dinâmico que tenta refutar.
  - Pedir evidência (saída do teste, comando e retorno, screenshot) em vez de afirmação; revisar evidência é mais rápido que reexecutar.
  - Causa raiz, não supressão do erro.
  - Revisor em subagente com contexto novo vê só o diff e os critérios; deve reportar apenas lacunas de correção ou de requisito, porque revisor sempre acha algo e isso leva a over-engineering.
  - Padrão Writer/Reviewer em sessões separadas; vale também para testes (uma sessão escreve testes, outra escreve código).
  - Falhas comuns nomeadas: trust-then-verify gap ("se não dá para verificar, não entregue"), correção em loop (após duas correções falhas, `/clear`), CLAUDE.md inchado (testar cada linha: "remover isso faria o Claude errar?"; ênfase em uma linha por vez).
- **Conteúdo reutilizável:** ver R1 (regra de CLAUDE.md) e R2 (skill `verification-gate`) em "Conteúdo reescrito".
- **Ressalvas:** guia geral de uso do Claude Code, não específico de QA. `/goal`, hook `Stop` e `/verify` dependem de versão; conferir a versão instalada.
- **Verificação:** página relida por inteiro nas seções citadas; texto do exemplo de prompt de revisão conferido; seção "Avoid common failure patterns" conferida.

### V-02 — Testar o próprio plugin com `claude plugin eval` (origem R-authoritative-01, R-github-04, R-community-08) — Classe A (8)
- **Lente:** authoritative + github + community
- **Tipo:** workflow + reference
- **Fonte:** https://code.claude.com/docs/en/plugin-evals · **Autor/Org:** Anthropic
- **Sinais:** doc oficial; exige Claude Code v2.1.269 ou superior e git 2.31 ou superior. Verificado (a lente community deixou a versão como "não verificada").
- **Para que serve:** medir se uma skill/agente do plugin muda o resultado (comparação com e sem plugin), pegar regressão ao trocar de modelo, travar CI.
- **Técnicas-chave (Verificado):**
  - Caso = prompt realista + graders. Layout `evals/<caso>/prompt.md` com `graders/*.md`, ou `case.yaml`; frontmatter do grader com `type`, `weight` opcional, `arm` opcional.
  - Três execuções por caso por padrão; nota da execução = fração de graders aprovados (com pesos); nota do caso = média; passa com `--threshold` (padrão 1.0).
  - Seis tipos: `regex`, `tool_used`, `tool_order`, `file_exists` (sem custo de juiz), `llm` (juiz vota PASS em 2 de 3), `baseline` (compara com transcrição de referência `.jsonl`).
  - `tool_used: Skill` fica fora do score nas duas arms (indicador "plugin disparou"); se passa mas o Δ é negativo, suspeitar do juiz antes do plugin.
  - Um grader no resultado e outro nos passos; para provar que build/teste rodou, o prompt manda gravar o resultado em arquivo e o grader checa o arquivo mais `tool_used` com `input_match`.
  - Flags confirmadas: `--case`, `--runs`, `--ablation none|with-without`, `--judge-model`, `--threshold`, `--max-cost-usd`, `--trust-plugin`, `--json [path]`, `--allow-tools`. Códigos de saída: 0 ok, 1 reprovação/erro, 2 execução parcial (teto de custo ou credencial recusada).
  - Receita de CI: `--trust-plugin`, `--json results.json`, modelos fixados, teto de custo.
  - Formato diferente do `evals/evals.json` do skill-creator; um não lê o outro.
  - **Windows nativo não tem backend de sandbox: suítes que concedem Bash/PowerShell precisam de WSL2** (Verificado; relevante para quem usa Windows).
- **Conteúdo reutilizável:** ver R9 (layout de suíte e grader).
- **Ressalvas:** cada execução e cada juiz custam chamadas de modelo; nomes de flags podem mudar entre versões.
- **Verificação:** página inteira salva e pesquisada por requisitos, flags, códigos de saída e seção de segurança.

### V-03 — Avaliar agentes: tarefa, trial, grader, pass@k e pass^k (origem R-authoritative-03, R-github-05, R-community-04) — Classe A (9)
- **Lente:** authoritative + github + community
- **Tipo:** pattern + checklist
- **Fonte:** https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents · **Autor/Org:** Anthropic Engineering (Mikaela Grace, Jeremy Hadfield, Rodrigo Olivares, Jiri De Jonghe) · publicado em 09/01/2026
- **Sinais:** data e autores verificados (a lente authoritative e a github não tinham a data).
- **Para que serve:** desenhar evals para agentes e plugins de QA.
- **Técnicas-chave (Verificado):** definições de task, trial e grader; três tipos de grader (código, modelo, humano); pass@k versus pass^k (exemplo do texto: 75% por trial dá cerca de 42% em três trials seguidos); começar com 20 a 50 tarefas tiradas de falhas reais; ler transcrições para separar erro do agente de erro do grader; conjuntos balanceados (casos em que o comportamento deve e não deve ocorrer); eval de regressão perto de 100%.
- **Conteúdo reutilizável:** checklist de tarefa de eval em R9.
- **Ressalvas:** artigo conceitual; números de benchmark não revalidados.
- **Verificação:** data, autores, definições, exemplo numérico, recomendação de 20 a 50 tarefas e balanceamento conferidos na página.

### V-04 — Desenvolver testes e critérios de sucesso para funcionalidades com LLM (origem R-authoritative-04) — Classe A (8)
- **Lente:** authoritative
- **Tipo:** checklist + rubric template
- **Fonte:** https://platform.claude.com/docs/en/test-and-evaluate/develop-tests · **Autor/Org:** Anthropic (Plataforma)
- **Sinais:** doc oficial; sem data; 137 mil caracteres (lidos 100 mil). Verificado.
- **Para que serve:** montar conjunto de testes de classificação/extração/resposta com LLM.
- **Técnicas-chave (Verificado):** critérios específicos, mensuráveis, atingíveis e relevantes; priorizar volume de casos graduados automaticamente sobre poucos revisados à mão; casos de borda (entrada irrelevante, muito longa, ambígua); métodos de grading (exact match, similaridade por embedding, ROUGE-L, Likert/binário/ordinal por LLM); nos exemplos de código, comentário recomendando usar outro modelo como grader.
- **Conteúdo reutilizável:** modelo de rubrica binária em R8.
- **Ressalvas:** exemplos de código usam IDs de modelo e sintaxe de SDK específicos; conferir contra a lista de modelos atual antes de copiar. Último trecho da página não lido.
- **Verificação:** presença de cada técnica conferida; a dica de "rubrica" não foi confirmada no trecho lido.

### V-05 — Gerador, avaliador e critérios de parada (origem R-authoritative-05) — Classe A (9)
- **Lente:** authoritative
- **Tipo:** pattern
- **Fonte:** https://www.anthropic.com/engineering/building-effective-agents · **Autor/Org:** Anthropic Engineering
- **Técnicas-chave (Verificado):** evaluator-optimizer (um LLM gera, outro avalia em loop) quando há critério claro; checar progresso contra a verdade do ambiente (saída de teste/execução) a cada passo; condição de parada como teto de iterações; testar em sandbox com guardrails; exigir caminho absoluto na ferramenta eliminou uma classe de erro no agente de SWE-bench (o texto não usa o termo poka-yoke).
- **Conteúdo reutilizável:** checklist de loop de revisão de testes: critério verificável por ferramenta; N máximo de iterações; escalar a humano ao travar; registrar o que cada iteração mudou (Inferido).
- **Ressalvas:** conceitual, sem métricas de ganho.
- **Verificação:** cinco afirmações conferidas na página.

### V-06 — Lista de features com `passes` e protocolo de sessão (origem R-authoritative-06, R-github-07, R-community-05) — Classe A (8)
- **Lente:** authoritative + github + community
- **Tipo:** template + pattern
- **Fonte:** https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents · **Autor/Org:** Anthropic Engineering · publicado em 26/11/2025 (Verificado)
- **Técnicas-chave (Verificado):** lista de features em JSON com categoria, descrição, passos de teste e `passes` (inicialmente falso; exemplo com mais de 200 itens); o texto diz que remover ou editar testes é inaceitável; JSON escolhido porque o modelo altera menos que Markdown; início de sessão: `pwd`, log do git, arquivo de progresso, lista de features, `init.sh`, teste E2E básico; automação de navegador (Puppeteer MCP) achou bugs que unitário e `curl` não acharam; limitação: alertas nativos do navegador são invisíveis. **Não há avaliador cético separado**: o mesmo agente verifica o próprio trabalho.
- **Conteúdo reutilizável:** protocolo R10.
- **Ressalvas:** pesado para QA pontual; exige sandbox e revisão humana.
- **Verificação:** data, campo `passes`, frase sobre edição de testes, rotina de início de sessão e ausência de avaliador separado conferidos.

### V-07 — Saída de teste desenhada para o modelo (origem R-authoritative-07, R-community-06) — Classe A (8)
- **Lente:** authoritative + community
- **Tipo:** checklist + pattern
- **Fonte:** https://www.anthropic.com/engineering/building-c-compiler · **Autor/Org:** Anthropic Engineering · publicado em 05/02/2026 (Verificado)
- **Técnicas-chave (Verificado):** console com poucas linhas e log completo em arquivo; `ERROR` com o motivo na mesma linha para `grep`; estatísticas pré-calculadas; progresso impresso raramente (o modelo não sente tempo); opção `--fast` com amostra determinística de 1% ou 10% por agente, aleatória entre máquinas; verificador de testes quase perfeito, senão o agente resolve o problema errado; CI para impedir regressão.
- **Conteúdo reutilizável:** convenção de saída em R6.
- **Ressalvas:** projeto extremo (compilador); princípio generaliza, números não.
- **Verificação:** oito afirmações conferidas.

### V-08 — Subagentes: formato, ferramentas e restrições (origem R-authoritative-08) — Classe A (8)
- **Lente:** authoritative
- **Tipo:** reference + subagent
- **Fonte:** https://code.claude.com/docs/en/sub-agents · **Autor/Org:** Anthropic
- **Técnicas-chave (Verificado):** obrigatórios `name` e `description`; `tools` (allowlist) e `disallowedTools` (denylist; aplicada primeiro); subagentes de plugin ignoram `hooks`, `mcpServers` e `permissionMode`; sessão em `bypassPermissions`, `acceptEdits` ou auto prevalece sobre o `permissionMode` do subagente; "use proactively" na `description` incentiva delegação; aviso de startup quando as descrições somam mais de 15 mil tokens; detalhe longo vai no corpo.
- **Correção:** aninhamento de subagentes é permitido por padrão até 3 camadas abaixo da conversa principal (variável `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`); versões anteriores diferiam.
- **Conteúdo reutilizável:** agente `test-reviewer` em R4.
- **Ressalvas:** campos e limites mudam entre versões; conferir a versão instalada. Últimos 8 mil caracteres não lidos.
- **Verificação:** oito afirmações conferidas, uma refutada (acima).

### V-09 — Formato e gatilhos de SKILL.md (origem R-authoritative-09) — Classe A (8)
- **Lente:** authoritative
- **Tipo:** reference + checklist
- **Fonte:** https://code.claude.com/docs/en/skills · **Autor/Org:** Anthropic
- **Técnicas-chave (Verificado):** `description` mais `when_to_use` cortados em 1.536 caracteres na listagem (colocar o uso principal no início); `SKILL.md` abaixo de 500 linhas; `disable-model-invocation: true` para fluxos com efeito colateral; `context: fork`; `allowed-tools` vale só para o turno que invocou; `license`, `compatibility` (até 500 caracteres) e `metadata` não alteram comportamento; skill-creator avalia com `evals/evals.json`, `grading.json`, `benchmark.json`.
- **Ressalvas:** últimos 6 mil caracteres não lidos.
- **Verificação:** sete afirmações conferidas com números exatos.

### V-10 — Plugins oficiais da Anthropic como referência (origem R-authoritative-28) — Classe A (8) como referência de existência
- **Lente:** authoritative
- **Tipo:** reference
- **Fonte:** https://github.com/anthropics/claude-plugins-official (e `/tree/main/plugins`) · **Autor/Org:** Anthropic
- **Sinais:** 37,6 mil estrelas, 4,2 mil forks, 4.379 commits, Apache-2.0 no repositório; o README manda ver a licença de cada plugin e avisa que a Anthropic não verifica o conteúdo dos plugins. Verificado.
- **Conteúdo verificado:** a pasta `plugins/` lista 40 entradas (a página indica que a lista pode estar incompleta), entre elas `pr-review-toolkit`, `code-review`, `ralph-loop`, `skill-creator`, `security-guidance`, `feature-dev`, `hookify`, `plugin-dev`, `claude-md-management`. O lead sobre `pr-review-toolkit` está confirmado quanto à existência.
- **Ressalvas:** nenhum conteúdo de plugin foi lido; só reutilizar após ler cada SKILL/agente e a licença do plugin. Próximo passo para o construtor: ler `pr-review-toolkit`, `code-review` e `skill-creator` pelo raw do GitHub.
- **Verificação:** página do repositório e da pasta `plugins/` buscadas; API bloqueada (403).

### V-11 — Skill `webapp-testing` da Anthropic (origem R-authoritative-27, R-github-03, R-community-24) — Classe A (8) · Prompt-score da fonte 75
- **Lente:** authoritative + github + community
- **Tipo:** skill
- **Fonte:** https://raw.githubusercontent.com/anthropics/skills/main/skills/webapp-testing/SKILL.md · repositório https://github.com/anthropics/skills · **Autor/Org:** Anthropic
- **Sinais:** `LICENSE.txt` da pasta = **Apache-2.0** (Verificado); ~180,2 mil estrelas (reportado pela lente github, não reconferido).
- **Técnicas-chave (Verificado):** árvore de decisão (HTML estático: ler o arquivo e achar seletores; app dinâmico sem servidor: helper `scripts/with_server.py`; servidor já ativo: reconhecimento e depois ação); rodar `--help` do helper e tratá-lo como caixa-preta; esperar `networkidle` antes de inspecionar o DOM; seletores descritivos e esperas explícitas; navegador headless; referências `element_discovery.py`, `static_html_automation.py`, `console_logging.py`.
- **Riscos:** `with_server.py` executa comandos de shell arbitrários passados em `--server`; o exemplo grava screenshot em `/tmp` (neste ambiente usar o diretório de scratchpad); a instrução de não ler o código do helper reduz a capacidade de auditá-lo antes de executar.
- **Conteúdo reutilizável:** roteiro de reconhecimento em cinco passos (navegar; esperar rede ociosa; capturar screenshot e lista de elementos interativos; escolher seletores; agir e conferir resultado) e o princípio "o plugin documenta o comando, não embute o helper".
- **Ressalvas:** escopo de app local; sem regra sobre dados sensíveis.
- **Verificação:** SKILL.md e LICENSE.txt lidos.

### V-12 — Avaliação de LLM por Hamel Husain e Shreya Shankar (origem R-authoritative-10a, R-github-08, R-community-09) — Classe B (7)
- **Lente:** authoritative + github + community
- **Tipo:** checklist + rubric
- **Fonte:** https://hamel.dev/blog/posts/evals-faq/ · **Autor/Org:** Hamel Husain e Shreya Shankar · título atual "AI Evals: Everything You Need to Know" · publicado em 18/09/2026, modificado em 21/09/2026 (Verificado)
- **Técnicas-chave (Verificado, números exatos da página):** binário em vez de Likert; subchecagens binárias para progresso; código antes de juiz LLM; um juiz por modo de falha; validar juiz com rótulos humanos (TPR e TNR; divisão treino 10–20%, dev 40–45%, teste 40–45%; 30 a 50 exemplos de Pass e de Fail em dev e em teste; pelo menos 50 Pass e 50 Fail ao depurar o juiz; 100 a 200 exemplos rotulados por modo de falha); análise de erros primeiro (pelo menos 30 traces anotados, cerca de 100 traces, parar quando nada novo aparece; 60–80% do tempo de desenvolvimento); ciclos de pelo menos 100 traces a cada 2 a 4 semanas; 100% de aprovação sugere eval que não desafia o sistema.
- **Ressalvas:** o texto se declara "opiniões fortes, não verdades universais"; 53 mil caracteres finais não lidos.
- **Verificação:** tabela de números extraída da página; data observada.

### V-13 — Vieses de juízes LLM (Eugene Yan) (origem R-authoritative-10b, R-github-09, R-community-10) — Classe B (5)
- **Lente:** authoritative + github + community
- **Tipo:** checklist
- **Fonte:** https://eugeneyan.com/writing/llm-evaluators/ · **Autor/Org:** Eugene Yan · agosto de 2024
- **Técnicas-chave (Verificado):** vieses de posição, verbosidade e auto-preferência com números de estudos de 2023 (claude-v1 e gpt-3.5); inflação de nota (o texto cita o estudo Shepherd, sem o termo "leniência"); mitigações: pairwise para tarefas subjetivas, saída binária, CoT, painel de juízes pequenos e diversos, paráfrase de instrução, kappa de Cohen.
- **Ressalvas:** modelos antigos; usar como direção, não como medida atual. O texto não traz mitigação testada específica para posição ou verbosidade. Atualidade 0 a 1.
- **Verificação:** biases e modelos estudados conferidos.

### V-14 — Distribuição de testes: pirâmide prática e testes mais integração (origem R-authoritative-11) — Classe B (7)
- **Lente:** authoritative
- **Tipo:** checklist + reference
- **Fontes:** https://martinfowler.com/articles/practical-test-pyramid.html (Ham Vocke, publicado em 26/02/2018 em martinfowler.com) · https://kentcdodds.com/blog/write-tests (Kent C. Dodds, 13/07/2019)
- **Técnicas-chave (Verificado):** empurrar cada teste para o nível mais baixo possível; E2E é lento e notoriamente instável; alerta contra o "ice-cream cone"; testar comportamento observável; não rodar automação contra produção; serviço falso para integração; contract tests consumer-driven com Pact. Dodds: poucos testes, concentrados em integração; retornos decrescentes de cobertura acima de cerca de 70% (o autor admite que o número não vem de dados); evitar testar trivialidade e detalhe de implementação.
- **Correções:** o artigo de Fowler/Vocke chama de "brittle" só os fakes, não UI como categoria; a página `bliki/TestPyramid` não foi relida.
- **Conflito entre fontes:** base unitária ampla versus ênfase em integração. Decisão recomendada: a menor camada que prova a regra, ajustada por risco e custo (Inferido).
- **Ressalvas:** textos de 2018 e 2019 (atemporais no conceito, antigos na ferramenta).
- **Verificação:** ambos relidos; tabela de afirmações conferida.

### V-15 — Property-based testing (fast-check) e mutation testing (Stryker) (origem R-authoritative-12) — Classe B (6) · item fino
- **Lente:** authoritative
- **Tipo:** reference + checklist
- **Fontes:** https://fast-check.dev/docs/introduction/ · https://stryker-mutator.io/docs/
- **Verificado:** fast-check gera centenas de casos e faz shrinking até a menor entrada que ainda falha; arbitraries, seeds e replay **não** aparecem na página. Stryker: mutante morto (teste falhou) versus sobrevivente (testes passaram); StrykerJS (JS/TS), Stryker.NET (C#), Stryker4s (Scala); sem fórmula de score na página.
- **Conteúdo reutilizável (Inferido):** triagem de mutante sobrevivente: é equivalente? falta caso de borda? a asserção é fraca? Complementar com a "mutation check" manual do superpowers (V-31).
- **Ressalvas:** conteúdo raso; manter como referência até haver fonte sobre equivalent mutants e seeds. Mutation testing é caro; aplicar a módulos críticos.
- **Verificação:** ambas as páginas relidas.

### V-16 — Teste de contrato com Pact (origem R-authoritative-13) — Classe B (7)
- **Lente:** authoritative
- **Tipo:** reference + checklist
- **Fontes:** https://docs.pact.io/ · https://docs.pact.io/getting_started/how_pact_works
- **Verificado:** contrato por exemplo; consumer-driven (só o que os consumidores usam é testado); o teste do consumidor gera o arquivo pact; a verificação do provider reenvia as requisições gravadas e compara com a resposta mínima esperada; o broker conecta com o CI. `can-i-deploy` não aparece nessa página. A página raiz também descreve "provider contract testing" contra um documento OpenAPI como abordagem distinta.
- **Conteúdo reutilizável:** checklist: listar interações por consumidor; gerar contrato nos testes do consumidor; verificar no provider no CI; tratar quebra de contrato como breaking change.
- **Ressalvas:** não substitui E2E de jornada de usuário. A página `what_is_contract_testing` do lead retorna 404.
- **Verificação:** duas páginas lidas.

### V-17 — BDD: descoberta, formulação e automação com Cucumber (origem R-authoritative-14) — Classe B (6)
- **Lente:** authoritative
- **Tipo:** reference + template
- **Fonte:** https://cucumber.io/docs/bdd/
- **Verificado:** três práticas (Discovery, Formulation, Automation); exemplos automatizados funcionam como guias; Gherkin como linguagem compartilhada. A página **não** menciona Given/When/Then.
- **Conteúdo reutilizável (Inferido):** cenário declarativo em linguagem de negócio (contexto, ação do usuário, resultado observável), sem seletores nem cliques. Convenção de tags de status `@todo`, `@wip`, `@done` vem de um comentário do HN (V-41), não do Cucumber.
- **Ressalvas:** BDD vira custo quando cenários se tornam scripts de UI. Fonte para sintaxe: "Gherkin reference" (não lida).
- **Verificação:** página relida.

### V-18 — Acessibilidade: WCAG 2.2 e avaliação W3C WAI (origem R-authoritative-15) — Classe A (9)
- **Lente:** authoritative
- **Tipo:** checklist + reference
- **Fontes:** https://www.w3.org/TR/WCAG22/ · https://www.w3.org/WAI/test-evaluate/
- **Verificado:** WCAG 2.2 é Recomendação W3C de 12/12/2024; 4.1.1 Parsing marcado obsoleto e removido; 87 critérios listados (86 ativos); nove critérios novos (2.4.11, 2.4.12, 2.4.13, 2.5.7, 2.5.8, 3.2.6, 3.3.7, 3.3.8, 3.3.9); princípios POUR. WAI: avaliar cedo; Easy Checks; nenhuma ferramenta sozinha determina conformidade; lista com mais de 100 ferramentas; WCAG-EM; avaliação humana qualificada e envolvimento de pessoas com deficiência. Priorização por impacto aparece apenas na transcrição de vídeo.
- **Conteúdo reutilizável:** auditoria em três camadas (ferramenta automatizada, revisão manual, teste com usuários); achados com critério WCAG e impacto (Inferido).
- **Ressalvas:** lidos 100 mil de 270 mil caracteres do WCAG. A skill `accessibility-testing` do qa-skills cita WCAG 2.1 (desatualizado frente a 2.2).
- **Verificação:** status, data, contagem e critérios novos conferidos.

### V-19 — Boas práticas de Playwright para E2E estável (origem R-authoritative-16) — Classe A (8)
- **Lente:** authoritative
- **Tipo:** checklist
- **Fonte:** https://playwright.dev/docs/best-practices · **Autor/Org:** Playwright (Microsoft)
- **Verificado:** testar comportamento visível ao usuário; testes isolados (storage e dados próprios; projeto de setup para reaproveitar login); não testar terceiros (stub com `page.route`); locators voltados ao usuário (`getByRole`); asserções web-first com `await`; evitar `expect(await ...isVisible())`; trace por padrão no primeiro retry em CI; `expect.soft`; `codegen`. A página **não** trata `waitForTimeout` nem política de retries (ver V-21).
- **Conteúdo reutilizável:** checklist de revisão de PR de E2E em R11.
- **Verificação:** doze itens conferidos (dez presentes, dois ausentes).

### V-20 — Agentes de teste do Playwright: planner, generator, healer (origem R-authoritative-17) — Classe A (8)
- **Lente:** authoritative
- **Tipo:** workflow + agent
- **Fonte:** https://playwright.dev/docs/test-agents
- **Verificado:** planner escreve plano Markdown em `specs/`; generator produz testes em `tests/`; healer reexecuta, ajusta e entrega teste passando **ou teste pulado se julgar a funcionalidade quebrada**; `seed.spec.ts`; `npx playwright init-agents --loop=vscode|claude|codex|opencode`; regenerar após atualizar o Playwright; a experiência com agentes pede VS Code 1.105 ou superior.
- **Conteúdo reutilizável (Inferido):** guardrail do healer: corrigir teste só quando a funcionalidade está certa; se parece quebrada, registrar como falha de produto e não ajustar a asserção; aceitar correção só com revisão de diff.
- **Ressalvas:** o healer pode mascarar regressão; ferramenta recente.
- **Verificação:** página relida.

### V-21 — Retries e classificação de flaky no Playwright (origem: descoberta do validador) — Classe A (8)
- **Lente:** validador (preenche lacuna de flaky nas três lentes)
- **Tipo:** reference + checklist
- **Fonte:** https://playwright.dev/docs/test-retries
- **Verificado:** retries por `--retries=3` ou `retries: 3` na configuração, ou por grupo com `test.describe.configure({ retries: 2 })`; por padrão não há retry; resultados classificados como passed, flaky (falhou e passou no retry) e failed; após falha o worker é descartado e um novo é iniciado, então teste falho não contamina os saudáveis; modo serial (`test.describe.serial`) agrupa testes dependentes e a página recomenda isolamento; a página **não** cobre `--repeat-each` nem `--fail-on-flaky-tests` nem trace (ver V-19 para trace).
- **Uso:** base de classe A para a política "retry é sinal, não correção" de V-37.
- **Verificação:** página lida.

### V-22 — Testing Library: testar como o usuário usa (origem R-authoritative-18) — Classe B (7)
- **Lente:** authoritative
- **Tipo:** reference + principle
- **Fontes:** https://testing-library.com/docs/guiding-principles/ · https://testing-library.com/docs/queries/about/#priority
- **Verificado:** três princípios (nós do DOM, não instâncias de componente; testar como o usuário usa; API simples). Prioridade de queries: `getByRole` primeiro, depois `getByLabelText`, `getByPlaceholderText`, `getByText`, `getByDisplayValue`, depois `getByAltText` e `getByTitle`, e `getByTestId` por último. A página de princípios **não** usa a expressão "detalhes de implementação" (a lacuna do pesquisador está resolvida pela página de queries).
- **Ressalvas:** específico de DOM no front-end.
- **Verificação:** duas páginas lidas.

### V-23 — Tipos de teste de performance com k6 (origem R-authoritative-19) — Classe A (8)
- **Lente:** authoritative
- **Tipo:** reference + table
- **Fonte:** https://grafana.com/docs/k6/latest/testing-guides/test-types/ · **Autor/Org:** Grafana Labs
- **Verificado:** smoke, average-load, stress, soak, spike, breakpoint, cada um com seu propósito; ordem sugerida: começar com smoke e subir carga e duração; durações aproximadas (smoke de segundos a minutos, load e stress de 5 a 60 minutos, soak de horas); nenhum limiar numérico de aprovação.
- **Ressalvas:** sem SLO nem script de exemplo na página; lacuna de limiares permanece.
- **Verificação:** página lida.

### V-24 — Boas práticas do Cypress (origem: descoberta do validador) — Classe A (8)
- **Lente:** validador (lacuna "Cypress" em todas as lentes)
- **Tipo:** checklist
- **Fonte:** https://docs.cypress.io/app/core-concepts/best-practices · **Autor/Org:** Cypress · "última atualização 20/09/2026" (Verificado)
- **Verificado:** atributos dedicados (`data-cy`) em vez de tag, classe ou id; evitar `cy.wait(<número>)` e esperar por alias de rede; testar apenas o que você controla; login programático e `cy.session()`; limpar dados em `beforeEach`, não em `after`, porque a limpeza pode nunca rodar; cada teste deve passar sozinho (`it.only`); página objects listados como anti-padrão; múltiplas asserções em E2E são aceitáveis; não atribuir retorno de comandos a variáveis; segredos fora do código (`cy.env()`); definir `baseUrl`; a página não cobre retries.
- **Conflito com Playwright:** Cypress recomenda `data-cy`; Testing Library e Playwright preferem role/label primeiro. Decisão: papel/label primeiro, atributo de teste como último recurso, conforme V-22 e V-19.
- **Verificação:** página lida.

### V-25 — Mocks e timers no Vitest (origem: descoberta do validador) — Classe B (7)
- **Lente:** validador (lacuna Jest/Vitest)
- **Tipo:** reference
- **Fonte:** https://vitest.dev/guide/mocking (doc v5.0.3)
- **Verificado:** `vi.fn`, `vi.spyOn`, `vi.mock` com hoisting; `importOriginal` para mock parcial; mock só afeta acesso externo ao módulo; limpar/restaurar mocks entre testes; `vi.setSystemTime` não reseta sozinho (usar `vi.useRealTimers()`); `vi.stubGlobal` e `import.meta.env` persistem entre testes salvo `unstubGlobals`/`unstubEnvs` ou chamadas `vi.unstubAll*`.
- **Uso:** regra "resetar mocks, relógio e globals entre testes" para o checklist de revisão de teste.
- **Ressalvas:** só Vitest; Jest segue sem fonte oficial lida.
- **Verificação:** página lida.

### V-26 — Teste de API a partir de OpenAPI com Schemathesis (origem: descoberta do validador) — Classe B (5)
- **Lente:** validador (lacuna API)
- **Tipo:** reference
- **Fontes:** https://schemathesis.readthedocs.io/en/stable/ · https://schemathesis.readthedocs.io/en/stable/quick-start/
- **Verificado:** gera casos a partir de OpenAPI (2.0, 3.0, 3.1, 3.2) e GraphQL; comando `uvx schemathesis run <url-do-schema>` (ou `schemathesis`/`st`); checagens de erro 5xx, status não documentado, resposta fora do schema, requisição inválida aceita, autenticação ausente ou inválida e método não suportado; saída traz `curl` de reprodução e um seed; `replay <ID>` reenvia um caso. Licença e versão não aparecem nas páginas.
- **Ressalvas:** rodar só contra ambiente de teste local ou de staging, com credenciais de teste (nunca produção); execução de pacote de terceiros fica a cargo do usuário e não entra como hook ou comando automático.
- **Verificação:** duas páginas lidas.

### V-27 — Como escrever um bom relatório de bug (Mozilla Bug Writing Guidelines) (origem: descoberta do validador) — Classe B (6)
- **Lente:** validador (lacuna "relatório de bug")
- **Tipo:** checklist + template
- **Fonte:** https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html · **Autor/Org:** Mozilla
- **Verificado:** resumo curto e único (cerca de 10 palavras ou 60 caracteres), sem a solução proposta; passos para reproduzir numerados e precisos, com frequência (sempre, às vezes, nunca); resultado esperado separado do obtido, e observação separada de palpite; um bug por relatório; pesquisar duplicata; testar build mais novo e perfil novo; caso mínimo; janela de regressão; detalhes extras por tipo (stack trace em crash, perfil em lentidão). Sem data na página.
- **Uso:** base de classe superior para o template de bug R7, mais forte que `qa-bug-report.mdc` (V-39).
- **Ressalvas:** orientado a Firefox/Bugzilla; adaptar campos.
- **Verificação:** página lida.

### V-28 — Red/green TDD e teste manual por agente, com registro de evidência (Simon Willison) (origem R-authoritative-20, R-community-18) — Classe B (6)
- **Lente:** authoritative + community
- **Tipo:** checklist + pattern
- **Fontes:** https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/ · https://simonwillison.net/guides/agentic-engineering-patterns/agentic-manual-testing/
- **Verificado:** dizer "use red/green TDD" ativa o fluxo; se a falha não for confirmada o teste pode já passar sem exercitar o código novo; sempre executar o código gerado; `python -c`, `curl` contra servidor de dev, automação de navegador (Playwright) e screenshot; bug achado vira teste de regressão; ferramenta Showboat registra `note`, `image` e `exec`, e o `exec` desencoraja o agente de escrever o que esperava em vez do que ocorreu. Páginas sem data. O comando do Showboat e o CLI Rodney não foram executados nem validados.
- **Conteúdo reutilizável:** R6 (relatório de evidência).
- **Ressalvas:** guia pessoal; licença não declarada, por isso só destilação.
- **Verificação:** duas páginas lidas.

### V-29 — Limites da verificação por LLM e do teste gerado (Dan Luu) (origem R-authoritative-21, R-github-20, R-community-13) — Classe B (6)
- **Lente:** authoritative + github + community
- **Tipo:** anti-pattern + checklist
- **Fonte:** https://danluu.com/ai-coding/ (título: "Agentic test processes, LLM benchmarks, and other notes on agentic coding from Galapagos Island")
- **Verificado (todas anedóticas, segundo o próprio autor):** testes escritos por LLM tendem a ser fracos; fuzzers gerados por LLM acham bugs reais com cobertura estreita; fuzzing escrito à mão geralmente vence a caça de bugs por LLM em latência, quantidade e falsos positivos, com alta variância; ao explicar quando um bug entrou, os agentes erraram cerca de metade das vezes e exigir execução de código para testar a hipótese removeu a maioria dos erros; caso de vídeo de reprodução fabricado; artefato mais revisão independente do artefato reduzem falso positivo. Datas internas de atualização: 2026-08 e 2026-09.
- **Conteúdo reutilizável:** regra "prova = comando + saída + artefato" e checklist anti-falso-positivo em R1 e R2.
- **Ressalvas:** evidência anedótica; 10 mil caracteres finais não lidos. Classe baixa por falta de método, não por erro factual.
- **Verificação:** tabela de seis afirmações conferida por seção.

### V-30 — Loop Ralph e back pressure (Geoffrey Huntley) (origem R-authoritative-23, R-community-12) — Classe B (5)
- **Lente:** authoritative + community
- **Tipo:** pattern
- **Fonte:** https://ghuntley.com/ralph/ · 14/07/2025 (Verificado)
- **Verificado:** back pressure = qualquer checagem que rejeite código inválido (tipos, testes, análise estática, scanners); rodar os testes da unidade alterada após cada mudança; tipagem estática ou analisador para linguagens dinâmicas; testes que documentam o próprio propósito; viés do modelo para implementação mínima e placeholder, com instrução explícita contra; "melhor para greenfield", o autor diz que não usaria em base existente. **Não há** aviso de sandbox nem regra de não afrouxar testes no texto; o autor roda o agente de forma autônoma com commit e push e avisa que pode acordar com a base quebrada.
- **Ressalvas:** loop autônomo sem limite de custo e sem isolamento é arriscado; a recomendação de sandbox e de teto de iterações vem de V-05, não de Huntley. Existe plugin oficial `ralph-loop` (V-10), não lido.
- **Verificação:** texto relido.

### V-31 — Skill de TDD do superpowers e guia de testes bons (origem R-authoritative-26, R-github-01, R-community-01) — Classe B (7) · Prompt-score da fonte 72
- **Lente:** authoritative + github + community
- **Tipo:** skill
- **Fontes:** https://raw.githubusercontent.com/obra/superpowers/main/skills/test-driven-development/SKILL.md · https://raw.githubusercontent.com/obra/superpowers/main/skills/test-driven-development/writing-good-tests.md · repositório https://github.com/obra/superpowers
- **Sinais:** 296,9 mil estrelas, 26,5 mil forks, MIT, 684 commits (Verificado na página); data do último commit não exibida.
- **Verificado no SKILL.md:** `description`: "Use when implementing any feature or bugfix, before writing implementation code" (gatilho só em inglês); seções Overview, When to Use (com exceções: protótipos, código gerado, configuração), Iron Law, Red-Green-Refactor com "Verify RED", "Verify GREEN", boas práticas, tabela de racionalizações, Red Flags, exemplo de bug, checklist de verificação, When Stuck, integração com debug. Exige que o teste falhe (não erre) pelo motivo esperado. Tom absolutista: CAPS, "MANDATORY", regra de apagar o código escrito antes do teste.
- **Verificado em `writing-good-tests.md`** (substitui o `testing-anti-patterns.md` inexistente): dois princípios (nomear a quebra que o teste pega; exercitar a coisa real), valores esperados independentes, evitar change detectors, não assertar em mock, mockar só o lento ou externo, "mutation check" (cada mutação realista do código deve derrubar ao menos um teste) e sinais de alerta.
- **Conteúdo reutilizável:** R3 (`tdd-guard`) com tom calibrado e exceções explícitas.
- **Ressalvas:** D10 baixo (CAPS e absolutismo; modelos atuais reagem em excesso); regra de apagar código existe como ação destrutiva local, então exigir confirmação; o README do repositório sugere, para OpenCode, mandar o agente buscar e seguir instruções de um URL remoto, padrão a **não replicar** (injeção indireta).
- **Verificação:** SKILL.md e writing-good-tests.md lidos; página do repositório relida.

### V-32 — Skill `verification-before-completion` do superpowers (origem R-github-02, R-community-02) — Classe B (7) · Prompt-score da fonte 75
- **Lente:** github + community
- **Tipo:** skill
- **Fonte:** https://raw.githubusercontent.com/obra/superpowers/main/skills/verification-before-completion/SKILL.md · mesmo repositório do V-31
- **Verificado:** gate de **cinco** passos (identificar o comando que prova; rodar completo e agora; ler a saída inteira, código de saída e contagem de falhas; verificar se a saída sustenta a afirmação, senão declarar o estado real; só então afirmar, com evidência); tabela "afirmação, evidência exigida"; red flags (hedging "deve", "provavelmente"; exclamar vitória antes de verificar; commit/push/PR sem verificação; confiar no relato de subagente; verificação parcial); padrões para teste de regressão (vermelho sem a correção, verde com ela), requisitos em várias partes e delegação (conferir o diff real). Tom absolutista ("Skip any step = lying").
- **Conteúdo reutilizável:** R2.
- **Ressalvas:** cortar a retórica, manter a tabela de evidência; o teste de regressão "reverter e restaurar" deve rodar em cópia de trabalho limpa ou com stash seguro, nunca com `git reset --hard` sem confirmação.
- **Verificação:** arquivo lido.

### V-33 — Skill `tdd` de Matt Pocock (origem R-authoritative-24, R-github-10, R-community-03) — Classe B (7) · Prompt-score da fonte 82
- **Lente:** authoritative + github + community
- **Tipo:** skill
- **Fonte:** https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/tdd/SKILL.md · repositório https://github.com/mattpocock/skills
- **Sinais:** 283,0 mil estrelas, 23,7 mil forks, MIT, 545 commits (Verificado); data do último commit não exibida.
- **Verificado:** frontmatter com `description` clara e com gatilhos ("test-first", "red-green-refactor", testes de integração); cerca de 40 linhas; seções: o que é um bom teste, seams (onde ficam os testes), anti-padrões e regras do ciclo. Anti-padrões presentes: acoplado à implementação (mocka colaboradores internos, testa métodos privados, verifica por canal lateral), tautológico (a expectativa recalcula como o código) e fatiamento horizontal (todos os testes antes de todo o código). Regras do ciclo: vermelho antes do verde, uma fatia vertical por vez, refatoração fora do ciclo (na revisão). Expectativa deve vir de fonte independente.
- **Correção:** **não existe** checklist de 10 itens no SKILL (R-github-10 errou).
- **Conteúdo reutilizável:** núcleo de R3.
- **Ressalvas:** o skill pressupõe GLOSSARY e ADRs em outras skills do repositório; adaptar ao plugin. MIT permite trecho literal com atribuição, mas o arquivo tem cerca de 40 linhas; preferimos destilar.
- **Verificação:** SKILL.md lido, README relido.

### V-34 — Skill `diagnosing-bugs` de Matt Pocock (origem R-github-23) — Classe B (7) · Prompt-score da fonte 85
- **Lente:** github
- **Tipo:** workflow
- **Fonte:** https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/diagnosing-bugs/SKILL.md
- **Verificado:** `description` com gatilhos ("diagnose", "debug this", algo quebrado, lançando erro, falhando ou lento); lê GLOSSARY.md e ADRs; **redige segredos** (`<REDACTED>`); seis fases: (1) construir um loop de feedback rápido, determinístico e que falhe, sem teorizar antes; (2) reproduzir e minimizar; (3) 3 a 5 hipóteses falsificáveis e ranqueadas, cada uma com previsão; (4) instrumentar uma variável por vez, com logs marcados por prefixo único; (5) correção e teste de regressão só em um seam que exercite o padrão real do bug (se não existir, registrar como achado de arquitetura); (6) limpeza (remover logs marcados, registrar a hipótese correta no commit).
- **Riscos:** pede execuções sem supervisão, testes de estresse, 1.000 entradas de fuzzing, `git bisect run` e mutação de código para forçar falha, sem delimitar o ambiente. Exigir confirmação do ambiente-alvo e nunca instrumentar produção sem autorização.
- **Conteúdo reutilizável:** R5 ganha o passo "loop de feedback primeiro"; fases 1 a 6 como roteiro de bug-para-correção.
- **Verificação:** arquivo lido.

### V-35 — gstack: `qa-only`, `qa` e `test-audit` (origem R-authoritative-25, R-github-12, R-community-15) — Classe B (6) · Prompt-score da fonte 73 (`qa-only`) e 80 (`test-audit`, lido via resumo)
- **Lente:** authoritative + github + community
- **Tipo:** skill
- **Fonte:** https://raw.githubusercontent.com/garrytan/gstack/main/qa-only/SKILL.md · https://raw.githubusercontent.com/garrytan/gstack/main/test-audit/SKILL.md · repositório https://github.com/garrytan/gstack
- **Sinais:** 135,7 mil estrelas, 20,2 mil forks, MIT, 445 commits (Verificado); data do último commit não exibida.
- **Verificado:** `qa-only` ("Report browser/API/CLI/job/worker/webhook bugs") escreve charters antes de sondar, define um "test value bar" com cartão `Value: protects=...; fails_when=...; why_new=...; seam=...` (160 bytes por campo), grava relatórios em `.gstack/qa-reports/run-<timestamp UTC>` com screenshots, e proíbe corrigir bug ou escrever teste de produto; a restrição depende de instrução, pois a ferramenta Write está liberada. `test-audit`: procura testes que custam mais do que protegem (sondas sem asserção, auto-comparações, fixtures copiadas, greps frágeis em código-fonte, duplicatas, exports só para teste), padrão de 10 candidatos, cartão de valor e cartão de aposentadoria (`test`, `detects`, `non_test_callers`, `search_command`, `stronger_proof`, `history`, `unlocks`, `validation`), prova de regressão (falha no HEAD, passa na base, passa após a correção), relatório somente leitura até aprovação por lote, nunca faz commit nem push. `./setup` do repositório compila binário, baixa Chromium e registra hooks em `~/.claude/settings.json`.
- **Conteúdo reutilizável:** R12 (cartão de valor e checklist de auditoria) e o princípio "relatar" separado de "relatar e corrigir".
- **Ressalvas:** preâmbulo longo com telemetria e estado em diretório próprio (D9 e D8 baixos); não instalar, não replicar o preâmbulo; os dois SKILLs não foram lidos até o fim (referências a `sections/` e `templates/` não incluídas).
- **Verificação:** README, `qa-only/SKILL.md` e `test-audit/SKILL.md` lidos; "value card" confirmado.

### V-36 — Instruções de QA do awesome-copilot (origem R-github-11) — Classe B (7) · Prompt-score da fonte 62
- **Lente:** github
- **Tipo:** claude-md-rule + checklist
- **Fonte:** https://raw.githubusercontent.com/github/awesome-copilot/main/instructions/qa-engineering-best-practices.instructions.md · repositório https://github.com/github/awesome-copilot
- **Sinais:** 39,9 mil estrelas, 5,1 mil forks, MIT, 2.437 commits (Verificado).
- **Verificado:** `applyTo: '**'`; pirâmide 60–70% unitários, 20–30% integração, 5–10% E2E; mock na fronteira (cliente HTTP, adaptador de banco, fila) e implementação real para funções puras; prioridade de seletor role, label, test-id, texto; retentativa automática uma vez no CI com sinalização de flaky; factories ou builders, sem produção nem PII.
- **Conteúdo reutilizável:** checklist de revisão de teste em R4/R11, com a pirâmide tratada como heurística, não como cota (conflito com Dodds, V-14).
- **Ressalvas:** os percentuais são convenção, não resultado empírico; a retentativa contradiz V-37 ("retry detecta, não corrige"): usar uma retentativa apenas como sinal, com ticket.
- **Verificação:** arquivo lido; as cinco afirmações conferidas (uma com nuance).

### V-37 — Triagem e quarentena de testes flaky (qa-skills) (origem R-github-13) — Classe C (4), aprovado com cruzamento · Prompt-score da fonte 75
- **Lente:** github
- **Tipo:** skill
- **Fonte:** https://raw.githubusercontent.com/petrkindlmann/qa-skills/main/skills/test-reliability/SKILL.md · repositório https://github.com/petrkindlmann/qa-skills
- **Sinais:** 170 estrelas, 30 forks, MIT, 53 commits, 50 skills (Verificado); push de 2026-06-10 reportado pela lente github, não reconferido. Autoridade 1, evidência 1, atualidade 1, comunidade 0, licença 1 = 4.
- **Verificado:** `version: "2.0"`, `license: MIT`; sete categorias de causa raiz (timing, dependência de dados, ambiente, dependência de ordem, sensibilidade ao tempo, renderização visual, serviço externo); "retries are a detection mechanism, not a fix"; quarentena com idade máxima de 14 dias; mais de 5% **dos testes em quarentena** indica problema sistêmico; correção validada com `--repeat-each=50` e 50 de 50 passes.
- **Cruzamento com fontes A (obrigatório por ser C):** isolamento e dados próprios (V-19, V-24), sem espera fixa (V-24), asserções web-first (V-19), classificação flaky/failed (V-21). Os números 14 dias, 5% e 50 execuções são convenção do autor, não padrão: marcar como "valores iniciais ajustáveis".
- **Ressalvas:** `description` não bate com o conteúdo (começa por "Runtime per-test healing..."), então o gatilho precisa ser reescrito (D1); o pacote de cura automática de seletores não foi avaliado.
- **Conteúdo reutilizável:** R5.
- **Verificação:** SKILL.md lido; cinco números conferidos (um corrigido).

### V-38 — `coder_eval` da UiPath para avaliar skills em CI (origem R-github-15) — Classe B (5)
- **Lente:** github
- **Tipo:** pattern
- **Fonte:** https://github.com/UiPath/coder_eval · **Autor/Org:** UiPath
- **Sinais:** 151 estrelas, 5 forks, Apache-2.0, 189 commits (Verificado); "Playwright for coding agents"; data do último commit não exibida (o push de 2026-10-09 vem da lente github).
- **Verificado:** suítes YAML com `success_criteria` ponderados de 0.0 a 1.0; `skill_triggered` como checagem de ativação; A/B de harness; **o driver `tempdir` não é fronteira de segurança, tarefas não confiáveis exigem container**.
- **Uso:** inspiração de esquema de critérios ponderados com timeout e checagem de ativação; para o plugin, a ferramenta oficial `claude plugin eval` (V-02) tem prioridade.
- **Ressalvas:** não executar sem sandbox; terceiros.
- **Verificação:** página do repositório lida.

### V-39 — Regra de relatório de bug do awesome-cursorrules (origem R-github-18, parcial) — Classe B (5) · Prompt-score da fonte 68
- **Lente:** github
- **Tipo:** template
- **Fonte:** https://raw.githubusercontent.com/PatrickJS/awesome-cursorrules/main/rules/qa-bug-report-cursorrules-prompt-file.mdc · repositório https://github.com/PatrickJS/awesome-cursorrules
- **Sinais:** 40,9 mil estrelas, 3,5 mil forks, CC0-1.0, 170 commits (Verificado). A lista de 20+ arquivos de regra (Playwright x5, Cypress x5, Jest, Vitest, Gherkin, testrail, xray, pr-review) existe, mas só dois foram lidos.
- **Verificado:** persona de QA; escala de severidade com cinco níveis; template de dez seções (descrição, ambiente, severidade, passos, esperado/obtido, evidência visual, logs, notas, correção possível); dez boas práticas; exemplo completo com dados fictícios. Frontmatter com `globs: **/*` sem aspas (YAML possivelmente inválido); nenhum campo marcado como obrigatório; "Possible Fix" convida a diagnóstico especulativo.
- **Conteúdo reutilizável:** R7, com campos obrigatórios explícitos e separação de observação e hipótese (V-27).
- **Ressalvas:** formato Cursor; CC0 permite cópia, mas o material é raso frente a V-27. A regra `playwright-e2e` foi lida e **rejeitada** (ver tabela): exemplo com rota relativa, `route.fulfill` sem `await` e seletores `data-testid` via `page.locator`.
- **Verificação:** dois arquivos lidos.

### V-40 — `TESTING.md` mantido pelo agente (ykdojo) (origem R-github-21, R-community-14) — Classe B (5)
- **Lente:** github + community
- **Tipo:** pattern
- **Fonte:** https://github.com/ykdojo/claude-code-tips (dica 48)
- **Sinais:** 10,2 mil estrelas, 827 forks, 742 commits (Verificado); página não identifica a licença (arquivo LICENSE existe); data não exibida. Autoridade 1, evidência 1, atualidade 1, comunidade 2, licença 0 = 5.
- **Verificado:** pedir ao Claude que teste a fundo e registre em `TESTING.md` como verificou, para que o humano revise o documento e não todo o código; ajustar o documento (encurtar, expandir, simplificar); no repositório vira log corrente de revisões.
- **Correção:** os campos "comando executado", "saída" e "o que NÃO foi testado" **não** estão na dica; são acréscimo nosso (Suposição consolidada com V-01 e V-28, que sustentam a ideia).
- **Conteúdo reutilizável:** R6.
- **Verificação:** página lida.

### V-41 — Práticas relatadas no HN: "Ask HN: What is your (AI) dev tech stack / workflow?" (origem R-community-21) — Classe B (6)
- **Lente:** community
- **Tipo:** pattern (sinal de prática)
- **Fonte:** https://news.ycombinator.com/item?id=48413629
- **Sinais:** 171 pontos e 136 comentários (Verificado); data inferida de um resumo vinculado pelo autor (2026-06-05), a página só mostra "4 meses atrás".
- **Verificado nos comentários (relatos, não fatos):** TDD com `AGENTS.md` (testes primeiro, revisão humana, depois código); o agente às vezes edita os testes em vez do código; tags Gherkin `@todo`, `@wip`, `@done` como estado de história; subagentes de revisão em paralelo antes de commit; revisão por outro modelo; verificação "à esquerda" (tipos, lint, constraints, build, depois testes).
- **Uso:** sustenta a regra "o agente não altera teste para fazer passar sem aprovação humana", cuja base A é V-06 (inaceitável editar testes) e V-01.
- **Ressalvas:** relatos anônimos; cerca de 11 mil caracteres finais não lidos.
- **Verificação:** página lida; quatro afirmações conferidas.

## Pontuação D1–D12 dos prompts/skills/regras coletados (fontes originais)

Escala 0–5 por dimensão; nota = soma/60 × 100. Todas as notas são avaliação minha, sobre o texto lido.

| Artefato | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | D11 | D12 | Nota | Principais achados |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| superpowers TDD (V-31) | 4 | 4 | 5 | 5 | 4 | 3 | 5 | 2 | 3 | 1 | 3 | 4 | 72 | CAPS e absolutismo; regra de apagar código sem pedir confirmação; gatilho só em inglês |
| superpowers verification (V-32) | 4 | 4 | 5 | 5 | 3 | 3 | 5 | 4 | 4 | 1 | 3 | 4 | 75 | Tom ameaçador ("= lying"); excelente tabela de evidência |
| mattpocock tdd (V-33) | 5 | 4 | 4 | 5 | 4 | 2 | 4 | 3 | 5 | 5 | 3 | 5 | 82 | Curto, bem gatilhado; sem formato de saída |
| mattpocock diagnosing-bugs (V-34) | 5 | 4 | 5 | 5 | 3 | 3 | 5 | 4 | 3 | 5 | 4 | 5 | 85 | Redação de segredos; riscos de execução não delimitados |
| anthropics webapp-testing (V-11) | 4 | 3 | 4 | 4 | 5 | 2 | 3 | 3 | 5 | 5 | 3 | 4 | 75 | Executa `--server` arbitrário; proíbe ler o helper; screenshot em `/tmp` |
| gstack qa-only (V-35) | 4 | 3 | 5 | 4 | 3 | 5 | 5 | 3 | 1 | 3 | 4 | 4 | 73 | Preâmbulo, telemetria e estado próprio inflam o contexto |
| gstack test-audit (V-35, lido por resumo) | 5 | 4 | 5 | 5 | 3 | 5 | 5 | 4 | 2 | 4 | 4 | 4 | 80 | Aprovação em lote; mesmo preâmbulo |
| awesome-copilot QA (V-36) | 3 | 2 | 4 | 4 | 3 | 2 | 2 | 3 | 3 | 4 | 2 | 4 | 62 | Percentuais como cota; sem motivação; sem verificação |
| cursorrules qa-bug-report (V-39) | 3 | 2 | 4 | 4 | 5 | 5 | 2 | 3 | 3 | 4 | 2 | 4 | 68 | Template bom; YAML duvidoso; sem campos obrigatórios |
| cursorrules playwright-e2e (rejeitado) | 3 | 2 | 4 | 4 | 2 | 2 | 1 | 2 | 4 | 4 | 1 | 2 | 52 | Exemplo com bugs; sem `getByRole`; sem verificação |
| qa-skills test-reliability (V-37) | 4 | 3 | 5 | 4 | 3 | 3 | 5 | 3 | 3 | 4 | 4 | 4 | 75 | Descrição desalinhada com o conteúdo; números de convenção |
| Prompt de revisão contra PLAN.md (V-01) | 5 | 4 | 5 | 3 | 4 | 4 | 5 | 4 | 5 | 5 | 4 | 5 | 88 | Exemplo oficial; "reporte lacunas, não preferências de estilo" |

Média: 73,9. Nenhum artefato foi reprovado por critério automático, mas V-31 e V-32 beiram D10 (tom) e `playwright-e2e` é rejeitado por D12 e D7.

## Rejeitados e rebaixados

| Item | Decisão | Motivo |
| --- | --- | --- |
| authoritative R-22 (Sanity "First attempt will be 95% garbage") | Rebaixado a C (4) | Relato de 6 semanas de um engenheiro (Vincent Quigley, 02/09/2025); taxas auto-relatadas, sem método. O conteúdo útil (revisão em três camadas, regra das três tentativas) é coberto por V-01 (Writer/Reviewer) e fica como sinal. Presente também em github R-19 e community R-11 |
| github R-14 (buer2233/ai-api-test-skill) | Rebaixado a C (4) | 162 estrelas, README em chinês, SKILL.md não lido; só o gate de pré-verificação (arquivo, local, nome do caso antes de editar) vale como ideia. Inclui serviço de captura com mitmproxy, a avaliar antes de qualquer uso |
| github R-17 (mhattingpete/claude-skills-marketplace) | Rebaixado a C (4) | 680 estrelas, Apache-2.0, 22 commits; os SKILLs `test-fixing` e `review-implementing` não foram abertos. Ideia aproveitável: agrupar falhas por similaridade antes de corrigir |
| github R-19 / community R-11 (duplicatas do Sanity) | Rebaixado | Ver R-22 |
| github R-16 (PramodDutta/qaskills) | Rejeitado | Nenhum conteúdo lido; instalação por `npx @qaskills/cli` e por servidor MCP via `npx -y` executa pacote de terceiros; "notas de qualidade" auto-atribuídas sem metodologia; 235 estrelas |
| github R-22 (Visma-Severa/QA-Agents) | Rejeitado | Arquivado pelo dono em 11/06/2026, 0 estrelas, nenhum arquivo lido, licença não identificada na página |
| github R-24 (lista de candidatos da busca por API) | Rejeitado | Nenhum aberto; 0 a poucas estrelas, vários sem licença; não reconferível com a API bloqueada |
| github R-18, parte `playwright-e2e` do awesome-cursorrules | Rejeitado (a regra) | Exemplo com `page.route('/api/login')` relativo, `route.fulfill` sem `await`, resposta sem content-type e seletores via `data-testid`; V-19 é superior |
| community R-16 (lackeyjb/playwright-skill) | Rebaixado a C (4) | 3,2 mil estrelas, MIT, 26 commits; Show HN verificado (189 pontos, 45 comentários, 20/10/2025, id 45642911); instalação exige `npm run setup` (baixa Playwright e Chromium) e `npx skills add`; navegador visível por padrão. Sinal de interesse na economia de contexto, sem conteúdo reutilizável lido |
| community R-17 (TIL de Willison sobre Playwright MCP) | Rebaixado a C (4) | Ponteiro de configuração de 01/07/2025 com pacote `@latest` de terceiros; a alegação do pesquisador de que ele manda logar com credenciais do usuário é falsa (o usuário digita as próprias) |
| community R-18 (índice de padrões de Willison) | Rebaixado/absorvido | Só títulos; conteúdo está em V-28 |
| community R-19 (Yonatan Kra) | Rebaixado a C (4) | Relato único de 25/11/2025: 5 de 18 specs geradas falharam; testes checavam propriedades privadas e nomes não correspondiam às asserções. Evidência útil para a checklist de revisão de teste gerado (V-29, V-31); sem método |
| community R-20 (Eleanor Berger) | Rebaixado a C (3) | Artigo de 19/10/2025: fase de testes isolada do código ("iniciar a sessão no diretório de testes"); a separação autor de teste versus implementador já tem base A em V-01 (Writer/Reviewer) |
| community R-22 (HN sobre medir desempenho do Claude Code) | Rebaixado a C (3) | 3 pontos e 9 comentários; ferramenta `stet.sh` não verificada; só o conceito de benchmark a partir do próprio repositório |
| community R-23 (mnapoli/exspec) | Rebaixado a C (3) | 16 estrelas, MIT, 34 commits; ideia verificada (agente só com ferramentas Playwright; cenário não verificável pelo navegador falha) |
| community R-25 (HAMY, 9 subagentes) | Rebaixado a C (4) | Métrica auto-relatada (cerca de 75% úteis contra menos de 50%); a lente community deu B (5), mas autoridade 1 e evidência anedótica pesam. O papel "Test Quality Reviewer" (cobertura proporcional ao risco, comportamento versus implementação, flakiness) alimenta R4; vereditos "Ready to Merge, Needs Attention, Needs Work" |
| community R-15 / R-18 / R-24 / R-03 etc. | Aprovados por fusão | Duplicatas de V-35, V-28, V-11, V-33 |
| Google Testing Blog, flaky tests (usado como pista) | Não usado | A página retorna só comentários de leitores, sem corpo do artigo |
| Pistas do atlas sem sustentação: "proibido afrouxar testes" (Ralph, HAMY), "só sandbox" (Ralph), avaliador cético separado (harnesses), "1% de chance" (superpowers) | Descartadas como fonte | Não aparecem nos textos lidos; a regra "não afrouxar teste" é sustentada por V-06 e V-41, não por Ralph ou HAMY. Expressão "1% de chance" não foi encontrada no TDD nem no verification lidos |

## Segurança e direitos autorais

- **Direitos autorais:** nenhum trecho literal foi reproduzido neste arquivo. Licenças verificadas: obra/superpowers MIT; mattpocock/skills MIT; garrytan/gstack MIT; petrkindlmann/qa-skills MIT; anthropics/skills `webapp-testing` Apache-2.0 (LICENSE.txt); github/awesome-copilot MIT; PatrickJS/awesome-cursorrules CC0-1.0; UiPath/coder_eval Apache-2.0; lackeyjb/playwright-skill MIT; mnapoli/exspec MIT; mhattingpete Apache-2.0; claude-plugins-official Apache-2.0 no repositório, com licença própria por plugin. Sem licença identificada: ykdojo/claude-code-tips, blogs (Hamel, Eugene Yan, Dan Luu, Willison, Huntley, Sanity) e docs oficiais de produto; para estes, só destilação. Se o construtor optar por reutilizar texto literal de qualquer fonte permissiva, limite a cerca de 40 linhas, com atribuição e aviso de modificação (Apache-2.0).
- **Injeção indireta / instruções a IAs em conteúdo externo:** o README do superpowers manda o agente "buscar e seguir instruções" de um URL remoto (instalação para OpenCode); o TIL de Willison sugere iniciar MCP com `@latest`; ambos são dado, não instrução, e **não** devem virar passos do plugin. O arquivo `qa-bug-report.mdc` e as páginas de docs não continham instruções dirigidas à IA além do próprio conteúdo da regra.
- **Comandos e instalações perigosas observadas (não executadas):** gstack `./setup` (compila, baixa Chromium, registra hooks em `~/.claude/settings.json`); lackeyjb `npm run setup` e `npx skills add`; qaskills `npx @qaskills/cli` e `claude mcp add ... npx -y @qaskills/mcp`; `with_server.py --server "<comando>"` executa shell arbitrário; `diagnosing-bugs` sugere `git bisect run`, estresse e fuzzing sem delimitar ambiente; `coder_eval` com driver `tempdir` não isola; `claude plugin eval` com Bash exige WSL2 no Windows. Regra para o plugin: documentar comandos em `references/`, nunca embuti-los como hooks automáticos nem `.mcp.json` ativo.
- **Links:** nenhum link encurtado encontrado; todos os URLs deste arquivo foram abertos.

## Conteúdo reescrito (redação própria, pronto para virar artefato)

Autoavaliação provisória do validador (mesma família de modelo do pesquisador; reavaliar com `claude plugin eval`). Metas de nota por artefato entre parênteses.

### R1 — Regra de CLAUDE.md "concluído só com evidência" (meta 88; base V-01, V-06, V-29, V-32, V-41)
```markdown
## Verificação antes de concluir
- Antes de dizer "pronto", "corrigido" ou "passando", rode o comando que prova a afirmação (teste do escopo alterado, build ou lint) e cole a saída relevante com o código de saída.
- Se não rodou ou não conseguiu rodar, diga isso e liste o que ficou sem verificação. Não apresente o resultado esperado como se fosse o obtido.
- Não edite, remova nem afrouxe teste, asserção ou lista de verificação para fazer o resultado passar. Se o teste parece errado, explique o motivo e peça decisão.
- Correção de bug exige um teste de regressão que falhou antes da correção; cole a falha e depois o verde.
```
Motivo para o plugin: cada linha passa no teste "remover isso faria o Claude errar?" (V-01) e fecha o risco de falsa conclusão descrito em V-29 e V-41.

### R2 — Skill `verification-gate` (meta 87)
```markdown
---
name: verification-gate
description: Exige prova antes de declarar uma tarefa concluída, corrigida ou aprovada. Use ao terminar uma mudança, antes de commit/PR, ou quando disser "pronto", "funciona" ou "testes passam" / Use before claiming done, fixed or passing.
---
Objetivo: toda afirmação de sucesso vem com evidência executada nesta sessão.

Passos
1. Nomeie o comando que prova a afirmação (teste do escopo, build, lint, script de checagem).
2. Execute-o por completo agora, não de memória.
3. Leia a saída inteira: código de saída, contagem de falhas, avisos.
4. Compare com a afirmação. Se não bate, relate o estado real com a evidência.
5. Só então afirme, anexando comando e saída relevante.

Tipos de afirmação e prova
- Bug corrigido: reproduza o sintoma original e mostre que sumiu; o teste de regressão falha sem a correção e passa com ela.
- Requisito com várias partes: verifique cada parte e relate uma a uma.
- Trabalho delegado a subagente: leia o diff real, não o relato.
- UI: screenshot ou E2E; sem acesso ao navegador, diga que não verificou.

Saída: bloco "Evidência" (comando, resultado, o que foi verificado) e bloco "Não verificado".
Casos de borda: se o comando não existe ou falha por ambiente, registre o erro e pergunte como verificar; não invente a execução.
```

### R3 — Skill `tdd-guard` (meta 86; base V-31, V-33, V-28)
```markdown
---
name: tdd-guard
description: Guia implementação test-first em fatias verticais. Use ao criar funcionalidade ou corrigir bug, "red-green-refactor", "teste primeiro", "TDD" / Use for test-first feature work and bug fixes.
---
Por quê: um teste que nunca foi visto falhando pode estar passando sem exercitar o código novo.

Ciclo (uma fatia vertical por vez, nunca todos os testes antes de todo o código)
1. Combine com o usuário a fronteira pública (seam) que será testada.
2. Escreva um teste do comportamento observável.
3. Rode e cole a falha. Ela deve ser pelo motivo certo (funcionalidade ausente), não por erro de sintaxe ou configuração. Se passou de primeira, revise o teste.
4. Implemente o mínimo para passar.
5. Rode o teste e depois a suíte do escopo; cole o resultado.
6. Refatore com tudo verde, na etapa de revisão.

Evite
- Testes acoplados à implementação (mock de colaborador interno, método privado, consulta direta ao banco).
- Testes tautológicos: o valor esperado vem de fonte independente (literal, exemplo trabalhado, especificação), não do mesmo cálculo do código.
- Check de mutação final: uma alteração realista no código de produção deve derrubar pelo menos um teste.

Exceções: protótipo descartável e configuração. Se pular o ciclo, diga ao usuário e registre o que não foi coberto. Código já escrito antes do teste: pergunte antes de apagar.
```

### R4 — Subagente `test-reviewer` (meta 87; base V-01, V-08, V-31, V-33, V-35, V-36)
```markdown
---
name: test-reviewer
description: Revisa testes novos ou alterados em um diff, em contexto limpo e somente leitura. Use proativamente depois de escrever ou alterar testes / Use proactively after tests change.
tools: Read, Grep, Glob
---
Você revisa testes, não escreve nem corrige. Reporte só lacunas que afetam correção ou requisitos; ignore estilo.

Para cada teste do diff, verifique
1. Nomeia o comportamento e a quebra que pegaria.
2. Tem asserção sobre comportamento observável (não só "não lança erro").
3. Valor esperado independente da implementação (sem tautologia, sem snapshot cego).
4. Não depende de ordem, relógio, rede nem estado compartilhado; sem espera fixa.
5. Mocks só em fronteiras; estado de mock, relógio e globals restaurados.
6. Nível adequado (menor camada que prova a regra); E2E só para jornada de valor.
7. Dados por factory, sem PII nem segredo.
8. Os testes do diff não foram afrouxados para passar (asserção removida, `skip`, tolerância ampliada) sem justificativa.

Saída: tabela "arquivo:teste | achado | evidência (trecho) | severidade (crítica, alta, média)" e veredito (Pronto, Precisa de ajuste). Se não houver lacunas, diga "sem lacunas relevantes" e liste o que não conseguiu verificar.
```
Nota (V-08): subagentes de plugin ignoram `hooks`, `mcpServers` e `permissionMode`; a restrição de leitura vem de `tools`. Para rodar testes, o usuário adiciona `Bash`.

### R5 — Skill `flaky-triage` (meta 85; base V-37, V-21, V-24, V-19, V-34)
```markdown
---
name: flaky-triage
description: Diagnostica teste instável (passa e falha sem mudança de código). Use quando um teste falha só no CI, às vezes, ou "flaky/intermitente" / Use for intermittent test failures.
---
Regra: retry detecta flake, não corrige. Uma retentativa serve de sinal e abre ticket.

1. Reproduza com execuções repetidas (por exemplo `--repeat-each` no Playwright) e registre a taxa de falha.
2. Classifique em uma causa antes de mexer: espera/timing, dados compartilhados, ordem, ambiente, relógio, renderização, serviço externo.
3. Corrija a causa: esperar condição (não atraso fixo), dados e estado por teste, relógio simulado, stub de terceiros.
4. Valide com muitas execuções seguidas sem falha (valor inicial: 50; ajuste ao custo).
5. Se não der para corrigir agora: quarentena com ticket, data e dono, fora do gate de CI, com prazo (valor inicial: 14 dias) e revisão semanal.
6. Se a quarentena passar de uma pequena fração da suíte (valor inicial: 5%), trate como problema de processo.
Saída: causa, evidência (comandos e taxas antes e depois), mudança feita, o que não foi validado.
```

### R6 — Relatório de evidência (`TESTING.md`) e saída de teste para agente (meta 86; base V-28, V-40, V-07)
```markdown
# Evidência de teste: <mudança>
- Escopo: <o que foi alterado>
- Comando executado: `<comando>`
- Saída relevante: <colar; truncar o resto e apontar para o log>
- Verificado: <comportamentos confirmados, por teste ou por execução manual>
- NÃO testado: <lacunas, motivo>
- Riscos residuais: <...>
```
Convenção para scripts de teste consumidos por agente: console com poucas linhas; `ERROR <arquivo>:<teste> - <motivo curto>` numa linha só; sumário final de três linhas (total, falhas, caminho do log); log completo em arquivo.

### R7 — Template de relatório de bug (meta 87; base V-27, V-39)
Campos obrigatórios: resumo curto (sem a solução); passos numerados para reproduzir, com frequência; resultado esperado; resultado obtido (observação separada de hipótese); ambiente (versão, SO, navegador/build); evidência (log, screenshot, trace); severidade com critério; menor caso reproduzível. Opcionais: janela de regressão, hipótese de causa (rotulada como Suposição). Regra: um bug por relatório; pesquisar duplicata antes.

### R8 — Rubrica binária de juiz LLM e checklist de viés (meta 86; base V-04, V-12, V-13)
```text
Critério: <um modo de falha, descrito em uma frase>.
Responda apenas PASS ou FAIL.
PASS quando <condição concreta e observável>.
FAIL quando <condição concreta e observável>.
Contexto fornecido: <só o trecho necessário>.
```
Checklist: código antes de juiz; um juiz por modo de falha; validar com rótulos humanos (TPR e TNR) em conjunto separado; trocar a ordem em comparação par a par; desconfiar de resposta longa; juiz de família diferente do gerador; testar paráfrases da rubrica; desconfiar de 100% de aprovação.

### R9 — Suíte de evals do plugin (meta 88; base V-02, V-03, V-12)
Estrutura: `evals/<caso>/prompt.md` mais `graders/*.md` com frontmatter `type` (e `weight`). Para cada skill: um caso que deve disparar, um que não deve disparar (pedido não relacionado), um grader no resultado (`regex`/`file_exists`) e um nos passos (`tool_used`/`tool_order`); `llm` só para saída curta, com PASS e FAIL concretos. Iterar com `--ablation none` e `--runs 1`; confirmar com as três execuções padrão; CI com `--trust-plugin`, `--json`, modelos fixados e `--max-cost-usd`. No Windows, suítes com Bash exigem WSL2. Tarefas iniciais de 20 a 50 retiradas de falhas reais; ler transcrições antes de confiar no score.

### R10 — Protocolo de feature list para execução longa (meta 85; base V-06)
Registro JSON: `id`, `category`, `description`, `steps` (lista), `passes` (booleano, inicia falso). Regras: alterar somente `passes`; nunca remover nem editar passos; marcar verdadeiro só após verificação ponta a ponta como usuário (navegador, não só unitário ou `curl`); uma feature por sessão; início de sessão: `pwd`, `git log`, arquivo de progresso, `init.sh`, E2E de sanidade; fim: commit descritivo e log. Registrar alerta nativo de navegador como limitação. Exigir sandbox e revisão humana.

### R11 — Checklist de revisão de E2E (meta 87; base V-19, V-24, V-21, V-22)
(a) locator por role/label/texto, `data-*` como último recurso; (b) asserção web-first com `await`; (c) sem espera de duração fixa; (d) estado e dados isolados por teste, cada teste passa sozinho; (e) terceiros com stub; (f) login programático ou estado reaproveitado; (g) limpeza em `beforeEach`, não só em `after`; (h) trace no retry; (i) sem segredo no código; (j) E2E limitado às jornadas de maior valor.

### R12 — Cartão de valor para teste proposto ou candidato a remoção (meta 85; base V-35)
Teste novo: protege o quê; falha quando; por que a cobertura atual não pega; precisa de seam de produção. Candidato a remoção: o que detecta; quem o chama fora de teste; prova mais forte que o substitui; histórico. Relatório só leitura até aprovação por lote; nunca commit nem push automáticos.

### R13 — Decisão de camada de teste (meta 85; base V-14, V-16, V-36)
Lógica pura: unitário. Combinação de módulos: integração com serviço falso de terceiros. Contrato entre serviços: Pact. Jornada de usuário: E2E curto. Domínio amplo de entradas: property-based. Regra: a menor camada que prova a regra; proporções 60/25/10 são ponto de partida, não cota.

## Mapa de cobertura do escopo (após validação)

| Subtema | Itens aprovados | Estado |
| --- | --- | --- |
| Estratégia e plano de testes | V-14, V-36, V-35 (charters) | Parcial: sem fonte de norma (ISTQB, IEEE 29119) |
| Pirâmide e troféu | V-14, V-36 | Coberto, conflito explicitado |
| Testes unitários | V-14, V-25, V-33 | Coberto para Vitest; Jest sem fonte oficial lida |
| Integração | V-14, V-16 | Parcial |
| Contrato | V-16 | Coberto (can-i-deploy não confirmado) |
| E2E Playwright | V-19, V-20, V-21, V-11 | Coberto |
| E2E Cypress | V-24 | Coberto (doc oficial, 20/09/2026) |
| TDD | V-28, V-31, V-33 | Coberto |
| BDD | V-17, V-41 | Parcial: sintaxe Given/When/Then não lida |
| Property-based | V-15 (fast-check) | Parcial: seeds e arbitraries sem fonte |
| Mutation testing | V-15, V-31 (mutation check) | Parcial: mutante equivalente sem fonte |
| Testes flaky | V-21, V-37, V-19, V-24 | Parcial: fonte B/C para quarentena e valores |
| Dados de teste | V-19, V-36 | Parcial: sem guia específico |
| Exploratórios | V-35, V-28 | Parcial: SBTM só página de apresentação (PDF não lido) |
| Acessibilidade | V-18, V-22 | Coberto em princípio; sem guia de ferramenta (axe) |
| Performance | V-23 | Parcial: sem limiares/SLO |
| Testes de API | V-26, V-16, V-28 | Parcial: sem Postman/REST Assured |
| IA/LLM e evals | V-02, V-03, V-04, V-12, V-13, V-38 | Coberto |
| Relatório de bug e evidência | V-27, V-39, V-40, V-28, V-32, V-34 | Coberto |
| Auditoria de qualidade dos testes | V-31, V-33, V-35 | Coberto |
| Revisão de teste por subagente | V-01, V-08, R4 | Coberto |
| Ecossistema de plugins/skills de QA | V-10, V-11, V-37 | Parcial: plugins oficiais listados, nenhum lido |
| Debug de falhas | V-34, V-01 | Coberto |

## Lacunas (objetivas e pesquisáveis)

1. Ler `anthropics/claude-plugins-official/plugins/pr-review-toolkit`, `code-review`, `skill-creator` e `ralph-loop` (SKILL/agentes e LICENSE de cada plugin) e extrair padrões de revisão de testes; fontes: `https://github.com/anthropics/claude-plugins-official/tree/main/plugins/<nome>` e raw correspondente.
2. Fonte oficial ou de norma para plano e estratégia de teste: ISTQB (glossário/syllabus Foundation 4.0) e ISO/IEC/IEEE 29119-3; verificar disponibilidade pública e licença.
3. Exploratory testing: baixar/ler o PDF de SBTM (satisfice.com, James e Jon Bach) ou "Exploratory Testing Explained"; charter, duração de sessão, debrief e métricas.
4. Jest: documentação oficial (jestjs.io) sobre mocks, timers e isolamento, para igualar a cobertura de Vitest.
5. Property-based: página "What is Property-Based Testing?" e docs de seeds/replay do fast-check; Hypothesis (Python) como segunda fonte.
6. Mutation testing: documentação do Stryker sobre mutantes equivalentes, `no coverage`, score; PIT (Java) ou mutmut (Python).
7. Flaky: fonte A ou B para quarentena e política de retries além do Playwright; Cypress retries (docs.cypress.io, test-retries); texto do Google com corpo legível (por exemplo cópias oficiais do Google Testing Blog) ou artigos de engenharia da Atlassian/Spotify/GitHub.
8. Dados de teste: fonte sobre factories, geração de dados sintéticos e anonimização (por exemplo guia de testes do OWASP ou docs de factory_boy/fishery).
9. Teste de API: Postman/Newman, REST Assured ou OpenAPI Generator como segunda fonte; OWASP API Security Top 10 para casos negativos.
10. Performance: critérios de aprovação e SLO (Google SRE Workbook, capítulo de SLOs) e exemplos de thresholds do k6 (`thresholds` na doc do k6).
11. BDD: referência de Gherkin (cucumber.io/docs/gherkin/reference) e "Writing better Gherkin"; cenário declarativo.
12. Axe/Lighthouse e pa11y para acessibilidade automatizada, com limites declarados.
13. Comunidade: Reddit (r/ClaudeCode, r/ClaudeAI, r/QualityAssurance), X, YouTube, dev.to e newsletters não foram cobertos; recoletar quando houver orçamento de busca. Procurar relatos reais de agentes que enfraqueceram testes e das mitigações usadas.
14. Datas de último commit/push de todos os repositórios (API do GitHub bloqueada nesta execução): reconferir com `gh api` autenticado antes de publicar.

## Recomendações ao construtor

**Skills (SKILL.md, menos de 500 linhas cada, `description` com gatilhos PT-BR e EN):**
- `verification-gate` (R2): núcleo do plugin; base V-01, V-29, V-32, V-41.
- `tdd-guard` (R3): base V-31, V-33, V-28; tom calibrado, sem CAPS, com exceções explícitas.
- `flaky-triage` (R5): base V-37 cruzada com V-21, V-24, V-19.
- `test-strategy` (R13 mais decisão de camada): V-14, V-16, V-36, V-23, V-18; com `references/` para k6, WCAG, Pact.
- `e2e-review` (R11): V-19, V-20, V-21, V-22, V-24; `references/` com Playwright e Cypress; guardrail do healer.
- `bug-report` (R7): V-27, V-39; `disable-model-invocation` não é necessário (sem efeito colateral), mas nunca criar issue externa sem confirmação.
- `bug-diagnosis` (roteiro de V-34, com delimitação de ambiente e confirmação antes de instrumentar).
- `eval-design` (R8, R9): V-02, V-03, V-04, V-12, V-13.

**Agentes (somente leitura por padrão):** `test-reviewer` (R4); `qa-reporter` (modo somente relatório, V-35; ferramentas Read, Grep, Glob, Bash opcional); `test-auditor` (R12; relatório sem edição até aprovação por lote). Não criar `qa-lead` que corrige código sem pedido humano; se for criado, usar `disable-model-invocation` na skill associada.

**Checklists/referências (`references/`):** R6 (evidência e saída de teste), R10 (feature list), R11, R12, WCAG 2.2 em três camadas (V-18), tipos de k6 (V-23), Schemathesis (V-26), anti-padrões de teste de V-31 e V-33.

**Prompts da biblioteca (brain-of-agent):** R2 (verificação), R3 (TDD), R4 (revisor), R8 (juiz binário), prompt de revisão contra plano (V-01), "use red/green TDD" (V-28), prompt de confirmação de hipótese por execução (V-29).

**Regras de CLAUDE.md:** R1; regra de testes mínimos ("cada linha passa no teste de remoção", V-01); convenção de saída de teste (R6). Manter o CLAUDE.md curto.

**Comandos (slash):** `/qa-evidence` (gera R6) e `/eval-plugin` (executa `claude plugin eval` com `--ablation none`), ambos opcionais; sem efeitos externos. Nota sobre colisão de nome `qa` com o namespace do plugin foi apontada pelo atlas e não foi reverificada por mim.

**Segurança de empacotamento:** sem hooks que executem shell, sem `.mcp.json` ativo, sem instalar pacotes de terceiros (gstack, qaskills, playwright-skill); documentar em `references/` o hook `Stop` de verificação (V-01) para o usuário habilitar conscientemente; no Windows, advertir que `claude plugin eval` com Bash precisa de WSL2 (V-02).

**Medição:** suíte de evals do próprio plugin (R9) com graders determinísticos primeiro, um grader `llm` binário por modo de falha, e baseline sem plugin; começar com 20 a 30 casos de falhas reais (V-03).

**Conflitos a documentar no plugin:** (1) pirâmide versus integração: menor camada que prova a regra (V-14); (2) retry no CI versus retry não corrige: uma retentativa só como sinal com ticket (V-36, V-37, V-21); (3) rigidez do TDD (V-31) versus pragmatismo (V-33): ciclo obrigatório com exceções declaradas; (4) healer automático (V-20) versus verificador quase perfeito (V-07): correção só com revisão de diff; (5) revisor que sempre acha algo (V-01): restringir a lacunas de correção e requisito; (6) seletores: role/label primeiro, `data-*` por último (V-22, V-24, V-19).

**Veredito:** 41 itens únicos aprovados (≥ 18), todos os subtemas com ao menos um item; lacunas listadas acima são de profundidade (fontes de norma, Jest, property/mutation, dados, SLO, comunidade social), não de cobertura básica.
