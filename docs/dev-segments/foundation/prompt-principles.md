# Princípios de prompt — dev-segments

Data: 2026-10-09 · Autor: indexador do atlas global (Claude Sonnet 5.5) · Base: os seis atlas `_global/*.validated.md` (anthropic-official, claude-code-ecosystem, cross-tool-rules, prompt-engineering-canon, community-pulse, brain-of-agent).
Leitores: todos os construtores e validadores. Este arquivo consolida e deduplica; não substitui `prompt-quality-rubric.md`.

Como ler as fontes: `AO-nn` = R-anthropic-nn · `PC-nn` = R-canon-nn · `CT-nn` = R-cross-nn · `CP-nn` = R-community-nn · `BR-nn` = R-global-nn do brain-of-agent · `EC-nn` = item nn do claude-code-ecosystem. Todos em `docs/research/_global/<tema>.validated.md`.
Rótulos: Verificado (reconferido por um validador) · Inferido (leitura do pesquisador, não reconferida) · Não verificável. Onde só há uma fonte de comunidade, o item vem marcado "sinal de prática".
Modelo-alvo: recomendações medidas em modelos Claude da geração 4.x/5.x (docs de 2026); conselhos mudam por modelo. Todo plugin deve registrar a versão e a data em que conferiu (AO-03, PC-26).

## 1. Princípios oficiais para Claude

### 1.1 Escrever o pedido
- P-01 Explique o porquê da regra e dê o contexto; proibição seca é frágil. Fonte: AO-01, PC-26 (Verificado).
- P-02 Prefira instrução positiva ("faça X") a "não faça Y"; toda proibição traz a alternativa. Fonte: AO-01, PC-11 (exemplo Verificado), CT-02 (Augment: muitos "don'ts" sem "dos" levam a sobre-exploração).
- P-03 Linguagem calma: sem CAPS, sem "CRITICAL/MUST" generalizados; ênfase em uma linha só e apenas após falha observada. Modelos atuais reagem em excesso a tom agressivo e a "se em dúvida, use a ferramenta". Fonte: AO-01, AO-06, PC-26, PC-03 (Verificado).
- P-04 Seja imperativo quando quer ação ("implemente", não "você poderia sugerir"); a ação é pedida explicitamente. Fonte: AO-01.
- P-05 Use 3 a 5 exemplos diversos, de estrutura idêntica, dentro de tags `<example>`; para ferramentas, prefira interface tipada a exemplos de uso. Fonte: AO-01, PC-06, PC-27.
- P-06 Use XML (ou um único estilo de delimitador) para separar instruções, dados e exemplos. Fonte: AO-01, PC-26, PC-06.
- P-07 Documentos longos no topo, pergunta/tarefa no fim (ganho de até 30% em testes internos da Anthropic); peça para citar trechos antes de responder. Fonte: AO-01, PC-26 (Verificado), PC-08, PC-25 (Lost in the Middle).
- P-08 Peça solução geral, não gabarito para os testes; peça para investigar antes de afirmar ("leia o arquivo antes de opinar"). Fonte: AO-01.
- P-09 Diga o escopo mínimo: o pedido define o escopo; bugs vizinhos viram follow-up; sem overengineering. Fonte: AO-01, AO-03.
- P-10 Não peça cadeia de raciocínio manual a modelos com thinking; peça "verifique contra X antes de terminar" e ajuste `effort`. Fonte: PC-26, PC-04, PC-08 (Verificado).
- P-11 Remova truques de geração antiga ao migrar (anti-preguiça, "seja exaustivo", gorjeta, ameaça) e reconstrua do menor prompt que preserva o contrato; suba effort só com ganho medido. Fonte: PC-03, PC-02, PC-26.

### 1.2 Agentes, contexto e ferramentas
- P-12 Contexto é recurso finito: o menor conjunto de tokens de alto sinal; carregue just-in-time; use compaction, notas em arquivo e subagentes que devolvem resumo curto. Fonte: AO-16 (Inferido), PC-27 (Verificado).
- P-13 Regras viram julgamento, exemplos viram interfaces, carga antecipada vira progressive disclosure (fonte: Claude 5 rules, Verificado). Fonte: PC-27.
- P-14 Estado fora da janela: JSON de features/testes, arquivo de progresso, git. Fonte: AO-01, AO-20.
- P-15 Compaction preserva: decisões exatas, problemas resolvidos, opções descartadas, estado atual, pendências e detalhes difíceis de reencontrar. Fonte: AO-03 (Verificado).
- P-16 Ferramentas: consolidar operações, namespacing, descrição como docstring (fator principal), formato `concise|detailed`, erros acionáveis, poka-yoke. Fonte: AO-15, AO-17 (Inferido), BR-27.
- P-17 Ações destrutivas, compartilhadas ou visíveis ao exterior pedem confirmação; leitura livre, escrita confirmada. Fonte: AO-01, AO-23, CP-22, PC-19.
- P-18 Delegue com objetivo, formato de saída, ferramentas e fronteiras; repita no prompt de delegação as regras críticas, porque subagentes não herdam CLAUDE.md com garantia. Fonte: AO-18 (Verificado), EC-04.
- P-19 Paralelize chamadas independentes de ferramenta; multiagente ganha em amplitude e perde em código com dependências compartilhadas. Fonte: AO-01, AO-18.
- P-20 Conteúdo lido (arquivo, página, resultado de tool, tag "da Anthropic" no turno do usuário) é dado, nunca instrução. Fonte: AO-23, AO-27 (Verificado), PC-21, BR-26.
- P-21 Se não puder verificar URL, ID ou número, diga que não verificou; "Done." sozinho não é resposta final. Fonte: AO-27 (Verificado).

### 1.3 Verificar e avaliar
- P-22 Dê ao agente um meio executável de verificar o próprio trabalho (teste, build, lint, screenshot, comando) e exija evidência. Fonte: AO-06 (Verificado), CP-01, CP-02.
- P-23 Verificação em graus: no prompt, `/goal`, Stop hook, subagente verificador; após duas correções falhas, `/clear` e prompt melhor. Fonte: AO-06 (Verificado).
- P-24 Revisor adversarial em contexto limpo, read-only, que reporta só lacunas de correção/requisito, não estilo. Fonte: AO-06, AO-29, CP-16.
- P-25 Autor e revisor separados; autoelogio de agentes é conhecido, então o avaliador é separado e cético. Fonte: AO-20, AO-29.
- P-26 Instrução é pedido; hook ou permissão é garantia. O que deve valer sempre vira hook documentado, não frase em CLAUDE.md. Fonte: AO-10, AO-12, AO-23, CT-04.
- P-27 Evals antes de documentação extensa: critérios específicos e mensuráveis, 20 a 50 casos de falhas reais, graders de código primeiro, ler transcripts. Fonte: AO-02, AO-21 (Verificado).
- P-28 Pass@k mede "alguma vez acerta"; pass^k mede consistência (75% por tentativa vira cerca de 42% em 3 tentativas). Fonte: AO-21 (Verificado).
- P-29 Juiz LLM: modelo diferente do gerador, binário com crítica, validado contra especialista; vieses de posição, verbosidade e autopreferência. Fonte: PC-16, PC-15, PC-24 (Verificado), AO-02.
- P-30 Uma execução não prova nada; use várias execuções e mediana. Fonte: CT-02 (AAIF, Verificado), PC-12.
- P-31 Raciocínio exibido não é prova (CoT mencionou a dica em 25% e 39% dos casos nos testes da Anthropic). Fonte: PC-24 (Verificado).

### 1.4 Escrever skills, subagentes e arquivos de contexto
- P-32 Skill: `name` até 64 caracteres `[a-z0-9-]`, sem "anthropic"/"claude"; `description` até 1024 caracteres, 3ª pessoa, o que faz e quando usar; corpo abaixo de 500 linhas; referências a 1 nível; sumário em arquivos acima de 100 linhas; no mínimo 3 avaliações; testar em Haiku, Sonnet e Opus. Fonte: AO-04, BR-29 (Verificado).
- P-33 A `description` é o gatilho de disparo; a seção `## Gotchas`, alimentada por falhas reais, é o conteúdo de maior sinal; medir undertriggering. Fonte: AO-31, CP-07.
- P-34 Graus de liberdade: alto para julgamento, médio para padrões, baixo (script/comando exato) para operações frágeis; feedback loops e plan-validate-execute. Fonte: AO-04 (Verificado).
- P-35 Skill com efeito colateral: `disable-model-invocation: true` e `allowed-tools` mínimos. Fonte: AO-08, BR-19.
- P-36 Subagente: `description` comportamental, `tools` allowlist (read-only para revisores), formato de saída no corpo; plugins ignoram hooks, mcpServers e permissionMode em agentes. Fonte: AO-09, EC-04, CP-16.
- P-37 CLAUDE.md/AGENTS.md: abaixo de 200 linhas; só o que o agente não descobre lendo o repo (comandos exatos, limites, convenções divergentes, verificação de pronto); teste de remoção; sem segredos; regra nova só na 2ª ocorrência de um erro. Fonte: AO-07, CT-02 (arXiv 2602.11988, Verificado), CP-04, CP-05.
- P-38 Árvore de decisão de onde colocar cada coisa: hook (sempre) → CLAUDE.md (fato universal, curto) → regra com `paths` → skill → subagente → MCP. Fonte: AO-12, CP-08.
- P-39 Formato de plugin: `name` único obrigatório; `agents`/`commands` declarados substituem o scan padrão, `skills` adiciona; sem `bin/`; CLAUDE.md na raiz do plugin não carrega; caminhos começam com `./` dentro da raiz; `${CLAUDE_PLUGIN_ROOT}` no corpo. Fonte: BR-27 (Verificado).
- P-40 Eval de plugin: `claude plugin eval` (Claude Code 2.1.269 ou superior), 3 execuções por caso, caso que dispara e caso que deve ignorar pedido alheio (`arm: both`), baseline sem plugin; marcar `designed_not_executed` até rodar. Fonte: AO-11, BR-05, BR-28 (Verificado).

## 2. Checklist universal de prompt para desenvolvimento

Aplique a todo prompt, skill, agente ou comando que um plugin gere ou contenha. Cada item é verificável por leitura.

- C-01 Papel e objetivo em uma frase; resultado esperado descrito (não só atividade). [P-04, P-09]
- C-02 Escopo: o que está dentro, o que fica fora, o que não pode mudar. [P-09, CP-13]
- C-03 Contexto mínimo suficiente: stack, versão, caminhos, convenções divergentes; sem o que o agente descobre lendo o repo. [P-12, P-37]
- C-04 Entradas: o que o usuário deve fornecer; pergunta ao usuário só para dúvida material, uma por vez. [CP-09, CT-21]
- C-05 Passos ou decisões em ordem; julgamento descrito como critério, não como roteiro rígido, exceto operações frágeis. [P-13, P-34]
- C-06 Cada regra com motivo curto; cada proibição com alternativa. [P-01, P-02]
- C-07 Tom calmo: zero CAPS e zero "MUST/NEVER" fora de invariantes de segurança. [P-03]
- C-08 Dados e instruções separados por delimitadores; conteúdo externo declarado como dado. [P-06, P-20]
- C-09 Formato de saída definido (tabela, JSON com campos, `arquivo:linha`), com exemplo quando o formato é estrito. [P-05, AO-24]
- C-10 Critério de pronto com comando de verificação literal e exigência de evidência colada (saída, diff, screenshot). [P-22, P-31]
- C-11 Rótulos epistêmicos (Verificado, Inferido, Suposição, Não verificável) e proibição de afirmar execução que não houve. [BR-04]
- C-12 Política de incerteza: quando não souber ou não puder verificar, diga e pare na decisão dependente. [P-21, PC-09 "dar uma saída ao modelo"]
- C-13 Ações com efeito externo (push, deploy, issue, escrita em produção, pagamento): confirmação explícita; `disable-model-invocation: true` quando for skill. [P-17, P-35]
- C-14 Ferramentas mínimas por agente; revisores somente leitura. [P-36, CT-15]
- C-15 Achados de revisão com severidade, confiança, `arquivo:linha`, cenário concreto e ação; limiar de confiança explícito e "em dúvida, não reporte". [AO-24, AO-29, BR-16]
- C-16 Escalada: após 3 tentativas ou hipóteses falhas, parar e reportar (ou re-planejar), sem empilhar correção. [EC-01, BR-15, CP-13]
- C-17 Seção `## Gotchas` com falhas reais (data/origem), vazia só se declarado. [P-33]
- C-18 Modelo-alvo e data de validação registrados; APIs e comandos confirmados na versão instalada. [P-11, BR-29]
- C-19 Tamanho: skill menor que 500 linhas, CLAUDE.md menor que 200, referências a 1 nível, sumário acima de 100 linhas. [P-32, P-37]
- C-20 Pelo menos 3 casos de eval (disparo, não disparo, falha comum) e rubrica binária com crítica, fora do contexto do executor. [P-27, P-40]
- C-21 Nenhuma URL, número, licença ou citação sem fonte observada; reuso literal só de licença permissiva, com atribuição. [00-LEIA-PRIMEIRO regras 2 e 3]
- C-22 Sem segredos, sem instruções de instalar ou executar código de terceiros; hooks e MCP só documentados em `references/`. [CT (supply chain nos transversais), EC (plugin seguro por padrão)]

## 3. Padrões de prompt reutilizáveis

Cada padrão é destilação com redação própria; adapte ao modelo-alvo e meça.

- PAD-01 Esqueleto de prompt: Papel · Contexto · Tarefa · Restrições com motivo · Formato de saída · Critério de pronto · Quando incerto. Fonte: PC-05, PC-10, AO-01.
- PAD-02 Pesquisar, planejar, implementar, verificar: explorar sem editar, plano curto, implementação por incrementos, verificação executável; pular o plano se o diff cabe em uma frase. Fonte: AO-06, CP-02, CP-03.
- PAD-03 Entrevista para spec: o agente pergunta (uma por vez) até ter requisitos testáveis, escreve `SPEC.md`, e a implementação começa em sessão nova só com a spec. Fonte: AO-06, CP-09, CP-25, CT-21.
- PAD-04 Spec testável: histórias priorizadas P1/P2/P3, Given/When/Then, requisitos `FR-NNN`, critérios `SC-NNN` independentes de tecnologia, seção Assumptions, marcador `[NEEDS CLARIFICATION]`. Fonte: EC-02, CT-22.
- PAD-05 Gate de aprovação humana: parar após perguntas, após escolha de arquitetura e antes de construir. Fonte: AO-29 (feature-dev), AO-30 (code-modernization).
- PAD-06 Reproduzir antes de corrigir: reproduzir, isolar, hipótese, correção mínima, teste de regressão que falhava antes, relatório de causa raiz; 3 correções falhas implicam rever a arquitetura. Fonte: EC-01 (Verificado), CT-21, CP-11, BR-17.
- PAD-07 TDD com vermelho confirmado: sem código de produção sem teste que falhou pelo motivo certo; verde com a suíte inteira; bug vira teste antes do fix. Fonte: EC-01, CP-09, CP-11.
- PAD-08 Revisor adversarial: papel, escopo (diff), checks, pontuação 0 a 100 ou confiança 1 a 10, saída `path:linha`, lista "não reportar"; cada achado validado por subagente fresco. Fonte: AO-29, BR-16, CP-16.
- PAD-09 Revisão de CI: contexto, passos, `--allowedTools` restrito, destino do resultado (comentário, issue-resumo). Fonte: AO-26.
- PAD-10 Delegação a subagente: objetivo, formato de saída, ferramentas, fronteiras, regras críticas repetidas, "um escritor por arquivo". Fonte: AO-18, CP-16.
- PAD-11 Handoff/checkpoint: Entregue · Verificado/Inferido · Pendências · Riscos · Próximo passo · Retomar; gerar antes de a janela encher (limiar de cerca de 40% é guia disputado: medir). Fonte: BR-06/07, CP-06, CP-18.
- PAD-12 Juiz binário com crítica: critério único, resposta PASS/FAIL, justificativa antes do veredito, calibrado com humano; asserção em código antes de juiz LLM. Fonte: PC-16, PC-17, AO-11.
- PAD-13 Anti-alucinação de API: tabela "importação banida → substituto → desde qual versão"; "não tem certeza de que o pacote existe: não importe, verifique (`npm ls`, `pip show`)"; menos código correto vence mais código chutado. Fonte: CT-08.
- PAD-14 Declarar a stack antes de gerar: stack, hospedagem, ORM, auth e bibliotecas aceitas; proibir auth, cripto, flags e cache próprios quando há biblioteca padrão. Fonte: CP-24.
- PAD-15 Molde de checklist de revisão: `ID · severidade · detecção (comando/regex) · referência normativa · correção`. Fonte: CT-16, CT-19, CT-20.
- PAD-16 Fatia vertical com ADR só quando há decisão material: ler, invariantes, opções, fatia vertical com testes, revisão adversarial, entrega com limitações. Fonte: BR-02, BR-21.
- PAD-17 Modo completo por keyword (`<SEGMENTO>-COMPLETO`): só por pedido explícito, leitura em lotes, matriz de aplicabilidade, registro lido/parcial/ausente. Fonte: BR-03.
- PAD-18 Tabela de racionalização: desculpa comum do agente, contra-argumento e sinal de alerta que força recomeçar. Fonte: EC-01.
- PAD-19 Autorização por risco: confirmar antes de pagamento ou escrita; checagem de leitura é livre. Fonte: PC-02, CP-22.
- PAD-20 Prompt de verificação de pipeline de dados: contagem origem vs destino, campos vs colunas, idempotência, testes unique/not null/relationships/freshness. Fonte: CP-26.
- PAD-21 Ficha de documentação de prompt: nome, objetivo, modelo-alvo, parâmetros, versão, resultado dos casos, data. Fonte: PC-07, PC-05.
- PAD-22 Relatório de bug/evidência: ID, ação, comando, saída real, status epistêmico, data. Fonte: BR-06, CP-11.

## 4. Anti-padrões e conselhos obsoletos

Evite; cada item indica o substituto.

- AP-01 CAPS, "CRITICAL", "MUST" em tudo (over-trigger em modelos atuais; arquivos comunitários chegam a abrir com "OVERRIDE all other behavior"). Substituto: motivo + uma linha de ênfase. [PC-26, CT-08 (ressalva do tom)]
- AP-02 Prefill de resposta (erro 400 em Claude 4.6 ou superior). Substituto: instrução de formato, saída estruturada. [PC-26]
- AP-03 `budget_tokens` em extended thinking (erro 400 em 4.7 ou superior). Substituto: adaptive thinking com `effort`. [PC-26]
- AP-04 "Pense passo a passo" como muleta em modelos com raciocínio; CoT manual e temperatura 0 para CoT (conselho de 2023 a 2024). Substituto: pedir verificação e ajustar effort. [PC-04, PC-07, PC-29]
- AP-05 Truques de 2023 (gorjeta, ameaça, repetição, "26 princípios"). Estudo fraco, rebaixado a C. [Rejeitados em PC]
- AP-06 Mexer em temperature, top_p, top_k nos modelos atuais sem motivo medido. [PC-06, PC-08]
- AP-07 Persona genérica "você é um especialista em…" sem diretivas verificáveis. Substituto: critérios e comandos. [CT-05]
- AP-08 Anti-preguiça e "seja exaustivo", "se em dúvida use a ferramenta". Causam excesso de tool calls. Substituto: critério de parada e orçamento. [PC-02, PC-26]
- AP-09 CLAUDE.md gerado em massa, com visão geral do repo, árvore de diretórios, "boas práticas" genéricas: custo médio de +20% sem ganho (arXiv 2602.11988). [CT-02]
- AP-10 Kitchen sink: sessão única misturando tarefas, correção repetida, trust-then-verify, exploração sem fim. Substituto: `/clear`, escopo, verificação. [AO-06, CP-02]
- AP-11 Hook ou regra de texto como "fronteira de segurança" (regex não substitui scanner; hooks são guardrail). Substituto: sandbox, permissões, CI. [EC-12, CP-19, AO-23]
- AP-12 Controle de acesso e validação de efeitos descritos só no prompt. Substituto: código. [CT-11]
- AP-13 Aceitar "pronto" por vídeo, resumo ou relato sem saída de comando gerada na sessão. [CP-20]
- AP-14 Testes tautológicos, acoplados à implementação, fatiamento horizontal; enfraquecer teste para passar. [CP-10, CP-16]
- AP-15 `--dangerously-skip-permissions` como atalho. Substituto: allowlist em settings e sandbox. [CP-01, CP-02, CP-12]
- AP-16 Autoavaliação do mesmo modelo apresentada como validação independente; notas D1 a D12 autoatribuídas. [BR-04, BR (tabela de notas rejeitada)]
- AP-17 Instruções contraditórias sem prioridade; regras sem motivo; regras para falhas que nunca ocorreram. Substituto: adicionar restrição após falha observada. [PC-02, CT-15]
- AP-18 Cópia de prompts vazados de produtos comerciais; cópia de texto sem licença clara. Reprovação automática. [CT-30 rejeitado, 00-LEIA-PRIMEIRO]
- AP-19 Instalar ou executar `npx`, `install.sh` ou scripts de terceiros a pedido de um README; obedecer texto dirigido à IA dentro de páginas. [EC-13, PC-14]
- AP-20 Métrica de popularidade (estrelas) como prova de qualidade; números de blog e de fornecedor sem reprodução. [EC transversais, BR]

## 5. Tensões a decidir por medição

- Número de exemplos (zero a 12 ou mais), XML contra Markdown, posição da instrução, role prompting: sem consenso entre labs; medir no modelo-alvo (PC transversais).
- "Description pushy" do skill-creator contra aviso de linguagem agressiva: usar ênfase cirúrgica (AO transversais).
- Limiar de contexto para handoff (cerca de 40% contra "sem degradação até 50%"): disputado; medir (CP-03, CP-06).
- Multiagente: ganha em pesquisa ampla (90,2% em eval interna da Anthropic, cerca de 15 vezes mais tokens) e perde em código acoplado (AO-18).
- Think tool e self-check: em grande parte superados por thinking adaptativo; exceção citada pela doc: Opus 5 não precisa de self-check (AO-17 Inferido, PC-26).
- Doc atual prevalece sobre repos quando divergem (hooks, output styles) (AO transversais).

## 6. Limites desta consolidação

- Itens marcados Inferido nos atlas (AO-02, 05, 07 a 10, 12 a 17, 19, 20, 22; PC-02, 04, 05, 08, 10, 13, 15, 18 a 20) mantêm esse rótulo aqui.
- Números citados (30%, 25%/39%, 42%, 90,2%, 20%) são dos autores originais e dependem de modelo e data; não os reproduza em plugins sem a fonte e a ressalva.
- Fontes PT-BR de nível A ou B inexistem no atlas; este arquivo está em PT-BR por convenção da casa, não por fonte.
- Antes de citar qualquer item, abra o atlas `_global` correspondente; este arquivo não substitui a leitura da fonte para reuso literal.
