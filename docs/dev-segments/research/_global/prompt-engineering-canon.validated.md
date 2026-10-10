# Cânone de engenharia de prompt e de contexto — versão validada (condensada)

Data: 2026-10-09 · Validador: Claude Sonnet 5.5 (`claude-sonnet-5-5`), independente do pesquisador (Claude Fable 5.1). Declaração: ambos são modelos Claude; a independência é de execução e de reverificação por ferramenta, não de família de modelo. Origem: `prompt-engineering-canon.md` (R-canon-01..30 + comparação, checklist A–K, templates T1–T18, sugestões à rubrica).

## 1. Método e resultado da validação

- Reverificados com WebFetch/API pública nesta data: 34 URLs (19 de 30 itens tocados, ~63%; classe A e afirmações numéricas priorizadas).
- Confirmados (Verificado): estrelas/licença de `openai/openai-cookbook` (76,5k★, MIT), `dair-ai/Prompt-Engineering-Guide` (79,0k★ hoje; o atlas diz 78,9k; MIT), `stanfordnlp/dspy` (38,6k★, MIT), `brexhq/prompt-engineering` (9,6k★, MIT; 3 citações literais conferidas), `anthropics/prompt-eng-interactive-tutorial` (38,4k★; licença não visível), `trigaten/Learn_Prompting` (4,7k★; licença NÃO identificada na página); datas e números de arXiv 2406.06608, 2205.11916, 2506.08837, 2303.11366, 2210.03629, 2305.10601, 2306.05685, 2411.10541; páginas da Anthropic (best practices cobrindo Fable 5.1 … Haiku 4.5, prefill removido ≥4.6, `budget_tokens` 400 em ≥4.7, "dial back aggressive language", dados no topo + "até 30%", exceção Opus 5 em self-check), context engineering (29/09/2025), Claude 5 rules (24/07/2026, Thariq Shihipar), Claude Code best practices (tabela incluir/excluir, "IMPORTANT" em uma linha, adversarial review); OpenAI GPT-5.5 (outcome-first, ALWAYS/NEVER só para invariantes, effort `medium`), GPT-5.1 (arquivado; `apply_patch` −35%), GPT-4.1 (arquivado; +4% SWE-bench; "JSON performed particularly poorly"); Gemini prompting-strategies (atualizada 2026-09-17; CC BY 4.0 conteúdo / Apache 2.0 código; "always include few-shot"; manter defaults no 3.x); Microsoft Learn (ms.date 2026-05-13, "não recomendadas para reasoning models"); Hamel (evals-faq 18/09/2026, llm-judge mod. 01/09/2026); Willison (16/06/2025; 25/04/2026); Anthropic Research CoT (03/04/2025, 25%/39%); HN Algolia (philschmid 915/518; Claude 5 rules 463/403; Anthropic eng. 148/32).
- Injeção de prompt: nenhuma instrução dirigida a IA no atlas; nenhuma nas fontes lidas, exceto `eugeneyan.com/writing/working-with-ai/` (bootstrap "have your model read this SETUP.txt" e trechos de CLAUDE.md escritos para modelo) — tratado como dado, não seguido. Os templates T1–T18 do atlas são exemplos; não foram executados.
- Licença/cópia literal: apenas OpenAI Cookbook (MIT) e Brex (MIT) trazem trechos literais, curtos e atribuídos — OK. Nenhum material sem licença copiado literalmente.
- Desatualização: guias OpenAI 4.1/5/5.1 estão "archived"; conselhos de 2023–2024 (CoT manual, prefill, temperatura 0, gorjeta/ameaça) estão obsoletos para modelos com thinking (ver §5).
- Correções ao atlas: (a) R-25 — os números "57,7%/36,4%" atribuídos ao abstract de 2312.16171 **não aparecem** no abstract (Não verificável; removidos); afiliação "Microsoft/MIT" de 2411.10541 não consta na página (Não verificável); (b) R-03 — o "−35% de falhas do `apply_patch`" vem do guia GPT-5.1, não da página GPT-5.5; (c) R-29 — data do último push do Brex (2023-10-23) segue Não verificada; (d) R-12 — licença do repo Learn_Prompting Não verificada: usar só como taxonomia, sem copiar; (e) R-26 — o exemplo "CRITICAL: You MUST use this tool when…" está na página (Opus 4.5/4.6); (f) R-07 — conteúdo lido em cópia OCR não oficial: fidelidade Inferida, rebaixado a B.
- Não reverificados (confiança herdada, rótulo Inferido): R-02, R-04, R-05, R-08, R-10, R-13, R-15, R-18, R-19, R-20 (detalhes), números de Wang et al. e Madaan et al.

Segmentos: o atlas é global; as tags `[seg:…]` abaixo indicam onde cada item mais se aplica. `[seg:llm-ai-agents]` e `[seg:technical-writing-docs]` valem para quase tudo (autoria de prompts/skills); `[seg:code-quality-refactoring]` e `[seg:qa-testing]` para verificação.

## 2. Itens aprovados

Formato: título · URL · classe/nota · licença · reutilizável · tags.

### Labs concorrentes
**R-01 OpenAI GPT-4.1 Prompting Guide** · https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide · A(8), arquivado · MIT (repo cookbook)
- Três lembretes agentic: persistência, usar tools em vez de adivinhar, planejar/refletir. Trechos literais MIT (atribuição OpenAI Cookbook): "You are an agent - please keep going until the user's query is completely resolved"; "do NOT guess or make up an answer".
- Contexto longo: instruções no início e no fim; JSON ruim para muitos documentos; tools pelo campo `tools`.
- Adaptar: remover "MUST"/CAPS e o convite "pense passo a passo" para modelos atuais.
- [seg:llm-ai-agents] [seg:code-quality-refactoring] [seg:cli-desktop-tooling]

**R-02 OpenAI GPT-5 Prompting Guide** · https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide · A(8), arquivado · MIT repo · (não reverificado)
- Controle de "eagerness": bloco de coleta de contexto com critério de parada precoce e orçamento de tool calls; escape hatch sob incerteza.
- Instruções contraditórias custam raciocínio; remover "maximize_/EXTREMAMENTE minucioso" (causavam excesso de tool calls no Cursor).
- Limiares de confirmação por risco (checkout/pagamento antes de busca).
- [seg:llm-ai-agents] [seg:fintech-payments] [seg:devops-cloud-infra]

**R-03 OpenAI GPT-5.1 + "Using GPT-5.5"** · https://developers.openai.com/api/docs/guides/latest-model/gpt-5.5 · https://developers.openai.com/cookbook/examples/gpt-5/gpt-5-1_prompting_guide · https://simonwillison.net/2026/Apr/25/gpt-5-5-prompting-guide/ · A(8) · docs API sem licença (destilar); cookbook MIT
- Novo modelo = nova família: reconstruir do menor prompt que preserva o contrato; prompts orientados a resultado; ALWAYS/NEVER só para invariantes, regras de decisão para julgamentos; subir effort só com ganho medido em evals.
- Pedir verificação (tests/typecheck/build) e dizer por que não pôde validar; tool nomeada (`apply_patch`) reduziu falhas em 35% (GPT-5.1, relato do lab).
- [seg:llm-ai-agents] [seg:code-quality-refactoring] [seg:technical-writing-docs]

**R-04 OpenAI Reasoning best practices** · https://developers.openai.com/api/docs/guides/reasoning-best-practices · A(7) · destilar · (não reverificado; escrito para o1/o3-mini)
- Evitar "think step by step" em modelos com raciocínio; zero-shot primeiro; delimitadores; explicitar critério de sucesso.
- [seg:llm-ai-agents] [seg:data-science-ml]

**R-05 OpenAI Prompt engineering guide (API)** · https://developers.openai.com/api/docs/guides/prompt-engineering · A(8) · destilar · (não reverificado)
- Prompt de produção é código: versionado, revisado, testado; pin de snapshot + evals; seções Identity → Instructions → Examples → Context.
- [seg:llm-ai-agents] [seg:git-workflow-release] [seg:devops-cloud-infra] [seg:web-frontend]

**R-06 Google Gemini API: Prompt design strategies** · https://ai.google.dev/gemini-api/docs/prompting-strategies · A(8) · CC BY 4.0 (texto), Apache 2.0 (código) — Verificado
- Few-shot com estrutura idêntica entre exemplos, poucos e variados; um só estilo de delimitador; evitar linguagem persuasiva; não alterar temperature/top_p/top_k no 3.x.
- Template agentic: planejar, avaliar risco (ler ≠ escrever), persistir.
- [seg:llm-ai-agents] [seg:technical-writing-docs] [seg:data-science-ml]

**R-07 Google whitepaper "Prompt Engineering" (Boonstra)** · https://www.kaggle.com/whitepaper-prompt-engineering (cópia lida: archive.org, não oficial) · B(6, rebaixado) · copyright Google (destilar)
- Ficha de documentação de prompt (nome, objetivo, modelo, parâmetros, prompt, saída, versão, OK/NOT OK); instruções em vez de restrições; variáveis; documentar tentativas.
- Ressalva: "temperatura 0 para CoT" é conselho de 2024.
- [seg:technical-writing-docs] [seg:llm-ai-agents] [seg:data-science-ml]

**R-08 Gemini 3.x: best practices e migração** · https://ai.google.dev/gemini-api/docs/interactions/gemini-3 · A(8) · CC BY 4.0 (inferido do site)
- Técnicas elaboradas de modelos antigos fazem o modelo over-analisar; `thinking_level` substitui `thinking_budget`; dados primeiro, pergunta no fim.
- [seg:llm-ai-agents]

**R-09 Microsoft Learn: Prompt engineering techniques** · https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/prompt-engineering · A(7) · licença não verificada (destilar)
- Vale para modelos não-reasoning. "Give the model an out" ("responda 'not found'"); citação inline próxima ao trecho reduz fabricação; especificar estrutura de saída; grounding.
- [seg:llm-ai-agents] [seg:technical-writing-docs] [seg:data-science-ml]

**R-10 Microsoft Learn: System message design** · https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/advanced-prompt-engineering · A(7) · destilar · (não reverificado)
- Checklist: trabalho, limites, formato, política "quando incerto", testar com prompts adversariais; system message não garante conformidade (camadas de defesa).
- [seg:llm-ai-agents] [seg:security-appsec]

### Educadores e praticantes
**R-11 Prompt Engineering Guide (DAIR.AI)** · https://www.promptingguide.ai/introduction/tips · https://github.com/dair-ai/Prompt-Engineering-Guide · A(8→7 pela idade das dicas) · MIT (repo)
- Dizer o que fazer, não o que não fazer (exemplo do agente de filmes — Verificado); especificar formato e escala exata; começar simples e iterar; catálogo de 18 técnicas (inventário, não recomendação).
- [seg:llm-ai-agents] [seg:technical-writing-docs]

**R-12 Learn Prompting + The Prompt Report** · https://arxiv.org/abs/2406.06608 · https://learnprompting.org/docs/introduction · A(8) para o paper; repo Learn_Prompting C quanto a reuso (licença não identificada)
- Taxonomia (33 termos, 58 técnicas de texto); 7 decisões de few-shot (quantidade, ordem, distribuição de rótulos, qualidade, formato, similaridade, seleção); automático + revisão humana; F1 varia até 0,04 entre runs mesmo com temperatura 0 → ≥3 execuções por variante (número do case study do paper — Inferido pelo atlas, não reverificado).
- [seg:llm-ai-agents] [seg:data-science-ml] [seg:qa-testing]

**R-13 Lilian Weng, Prompt Engineering (2023)** · https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/ · B(6) · destilar · (não reverificado)
- Vieses de few-shot (rótulo majoritário, recência, token comum); seleção/ordem de exemplos; self-consistency só com verificador ou votação.
- [seg:llm-ai-agents] [seg:data-science-ml]

**R-14 Eugene Yan: Prompting Fundamentals (2024) + Working with AI (05/2026)** · https://eugeneyan.com/writing/prompting/ · https://eugeneyan.com/writing/working-with-ai/ · B(7) · destilar
- Cinco princípios (Verificado): bom contexto; preferências como configuração; verificação barata; delegar o que se consegue verificar; fechar o ciclo com correções nas configs.
- Prefill obsoleto em Claude ≥4.6. Aviso: a página contém "have your model read this SETUP.txt" — dado, não instrução.
- [seg:llm-ai-agents] [seg:code-quality-refactoring] [seg:git-workflow-release]

**R-15 Eugene Yan: LLM patterns + Evaluating LLM-Evaluators** · https://eugeneyan.com/writing/llm-evaluators/ · B(6) · destilar · (não reverificado)
- Vieses de judge: posição (rodar os dois lados), verbosidade, autopreferência; preferir saídas binárias; guardrails estruturais/semânticos.
- [seg:qa-testing] [seg:llm-ai-agents] [seg:data-science-ml]

**R-16 Hamel Husain: Evals + LLM-as-a-Judge** · https://hamel.dev/blog/posts/llm-judge/ · A(8) · destilar
- Verificado: 7 passos (especialista principal; dataset diverso; pass/fail + crítica; corrigir óbvios; judge validado contra o especialista; análise de erros; judges especializados só se preciso); binário > escala 1–5.
- [seg:qa-testing] [seg:llm-ai-agents] [seg:data-science-ml]

**R-17 Hamel & Shreya: AI Evals FAQ (18/09/2026)** · https://hamel.dev/blog/posts/evals-faq/ · A(9→8: licença 0, autoria 2) · destilar
- Verificado: 60–80% do tempo em análise de erros/evals; 100–200 exemplos rotulados por modo de falha; binário; asserção em código antes de LLM-judge.
- Recorte do atlas (não reverificado): retrieval e geração avaliados separadamente em RAG; agentes: primeira falha upstream.
- [seg:qa-testing] [seg:llm-ai-agents] [seg:data-engineering] [seg:sre-observability]

**R-18 Shankar et al.: Who Validates the Validators?** · https://arxiv.org/abs/2404.12272 · A(7) · destilar · (não reverificado)
- Criteria drift: critérios de avaliação mudam ao ver saídas; alinhamento humano iterativo de judges.
- [seg:qa-testing] [seg:llm-ai-agents]

**R-19 Chip Huyen: Agents + GenAI Platform** · https://huyenchip.com/2025/01/07/agents.html · B(7) · destilar · (não reverificado)
- Validar o plano antes de executar; ações de escrita exigem confiança; prompt injection é a maior ameaça em write actions → limitar permissões.
- [seg:llm-ai-agents] [seg:security-appsec] [seg:sre-observability]

**R-20 Jason Liu: RAG** · https://jxnl.co/writing/2024/05/22/systematically-improving-your-rag/ · B(6) · destilar · (não reverificado)
- Query understanding estruturada, avaliação de retrieval em separado.
- [seg:data-engineering] [seg:llm-ai-agents] [seg:database-data-modeling]

**R-21 Willison: Lethal trifecta + Design Patterns (arXiv 2506.08837)** · https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ · https://arxiv.org/abs/2506.08837 · A(8) · destilar
- Verificado: dados privados + conteúdo não confiável + comunicação externa; conteúdo não confiável não deve poder disparar ações consequentes. Seis padrões (Action-Selector, Plan-Then-Execute, Map-Reduce, Dual LLM, Code-Then-Execute, Context-Minimization).
- [seg:security-appsec] [seg:llm-ai-agents] [seg:automation-integrations] [seg:devops-cloud-infra] [seg:saas-multitenant]

### Papers
**R-22 CoT, Zero-shot CoT, Self-Consistency, ToT** · https://arxiv.org/abs/2205.11916 (e 2201.11903, 2203.11171, 2305.10601) · A(8) · destilar
- Verificado: zero-shot CoT MultiArith 17,7→78,7%, GSM8K 10,4→40,7% (text-davinci-002); ToT Game of 24: 4%→74% (GPT-4). Self-consistency só com agregador/verificador. Todos pré-thinking.
- [seg:llm-ai-agents] [seg:data-science-ml]

**R-23 ReAct, Reflexion, Self-Refine** · https://arxiv.org/abs/2210.03629 · https://arxiv.org/abs/2303.11366 · https://arxiv.org/abs/2303.17651 · A(8) · destilar
- Verificado: ReAct +34 pts ALFWorld, +10 WebShop; Reflexion 91% pass@1 HumanEval vs 80% GPT-4. Self-Refine usa o mesmo modelo como crítico: autoavaliação não é validação externa.
- [seg:llm-ai-agents] [seg:code-quality-refactoring]

**R-24 LLM-as-a-Judge (Zheng) + fidelidade do CoT (Anthropic)** · https://arxiv.org/abs/2306.05685 · https://www.anthropic.com/research/reasoning-models-dont-say-think · A(8) · destilar
- Verificado: >80% de concordância com humanos; vieses de posição/verbosidade/autoengrandecimento; CoT mencionou a dica em 25% (Claude 3.7) e 39% (R1) → raciocínio exibido não é evidência.
- [seg:qa-testing] [seg:llm-ai-agents] [seg:security-appsec]

**R-25 (parcial) Lost in the Middle + Prompt Formatting** · https://arxiv.org/abs/2307.03172 · https://arxiv.org/abs/2411.10541 · B(6) · destilar
- Informação relevante rende mais no início/fim; formato muda desempenho em até 40% em GPT-3.5-turbo (GPT-4 mais robusto) — Verificado. Aprovado só nesta parte.
- [seg:llm-ai-agents] [seg:technical-writing-docs]

### Anthropic (baseline)
**R-26 Prompting best practices (plataforma)** · https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices · A(9) · destilar
- Contexto/motivação em vez de proibição seca; exemplos 3–5 diversos em tags; XML para separar instruções/dados; dados longos no topo, pergunta no fim (até 30% em testes internos); citar trechos antes de responder.
- Dial back de linguagem agressiva e de "if in doubt, use [tool]" (Opus 4.5/4.6 over-trigger); prefill removido ≥4.6; `budget_tokens` → adaptive thinking + `effort`; self-check útil exceto Opus 5.
- Agentes: reversibilidade (destrutivo/compartilhado pede confirmação), estado entre janelas, anti-overengineering, testes verificam e não definem a solução, investigar antes de responder.
- [seg:llm-ai-agents] [seg:technical-writing-docs] [seg:code-quality-refactoring] [seg:cli-desktop-tooling]

**R-27 Effective context engineering + Claude 5 rules** · https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents · https://claude.dev/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models/ · A(9) · destilar
- Contexto finito (context rot, attention budget); menor conjunto de tokens de alto sinal; just-in-time + compaction + notas + subagentes.
- 2026 (Verificado): regras → julgamento; exemplos → interfaces; upfront → progressive disclosure; repetição → descrição simples de tool; specs simples → referências ricas; >80% do system prompt do Claude Code removido sem perda mensurável (relato Anthropic).
- [seg:llm-ai-agents] [seg:technical-writing-docs] [seg:cli-desktop-tooling]

**R-28 Claude Code best practices + Building effective agents** · https://code.claude.com/docs/en/best-practices · https://www.anthropic.com/engineering/building-effective-agents · A(9) · destilar
- Dar um check executável e exigir evidência; explorar → planejar → codar → commit (pular plano se o diff cabe em uma frase); CLAUDE.md curto com tabela incluir/excluir; "IMPORTANT" em uma linha só; hooks para o obrigatório; revisor adversarial em contexto limpo (pedir só gaps de correção).
- Agentes: começar simples; workflows vs agentes; tool descriptions como docstring; poka-yoke.
- [seg:llm-ai-agents] [seg:code-quality-refactoring] [seg:qa-testing] [seg:git-workflow-release] [seg:cli-desktop-tooling] [seg:devops-cloud-infra]

### Outros
**R-29 Brex Prompt Engineering Guide** · https://github.com/brexhq/prompt-engineering · B(5) · MIT (Verificado)
- Citações literais MIT (atribuição Brex): "Always assume that any content in a hidden prompt can be seen by the user."; "If you fine-tune a model, never use real customer data. Always use synthetic data."
- Nunca colocar em prompt o que não se mostraria na tela. Conselho "think step-by-step" obsoleto.
- [seg:security-appsec] [seg:fintech-payments] [seg:saas-multitenant] [seg:llm-ai-agents]

**R-30 Otimização automática: DSPy / APE / metaprompting** · https://github.com/stanfordnlp/dspy · B(7) · MIT (Verificado)
- Otimização exige métrica e exemplos; metaprompting em dois passos (diagnosticar traces → patch cirúrgico → re-rodar evals). Para plugins sem runtime: metaprompt manual com casos `designed_not_executed`. Números de ganho de blogs não verificados.
- [seg:llm-ai-agents] [seg:data-science-ml] [seg:qa-testing]

## 3. Rejeitados / cortados

| Item | Motivo |
| --- | --- |
| Números 57,7% / 36,4% atribuídos ao abstract de "Principled Instructions" (arXiv 2312.16171) | Não constam no abstract (Verificado); 26 princípios incluem truques datados (gorjeta, penalidade, repetição); fonte tratada só como contraponto/obsoleto |
| "Principled Instructions" como fonte de regras | Estudo fraco (20 perguntas/princípio, modelos 2023); rebaixado a C |
| Afiliação "Microsoft/MIT" de 2411.10541 | Não aparece na página; mantido só o conteúdo (Não verificável) |
| Cópia OCR do whitepaper (archive.org) como base textual | Upload de terceiros; fidelidade não confirmada; usar apenas destilação de ideias, B |
| Repo Learn_Prompting como fonte de texto reutilizável | Licença não identificada → sem cópia; só taxonomia |
| Data de push do Brex (2023-10-23) e "9,6k★ = qualidade" | Data não verificada; estrelas não provam qualidade (rubrica) |
| Atribuir "−35% apply_patch" ao GPT-5.5 | Pertence ao guia GPT-5.1 (arquivado) |
| Conselhos obsoletos mantidos no atlas como regra (CoT manual, prefill, `budget_tokens`, temperatura 0 para CoT, CAPS) | Ver §5; só como "evitar" |
| Lacunas não preenchidas: lista dos 16 padrões de White et al.; curso DeepLearning.AI; GPT-5.2 guide; paper MIPRO; fontes PT-BR nível A/B | Não verificáveis nesta execução; não usar como fonte |

## 4. Templates reutilizáveis (T1–T18, só índice; texto no atlas original)

T1 esqueleto de system prompt · T2 lembretes agentic calmos · T3 coleta de contexto com parada/orçamento · T4 política de risco/reversibilidade (teste da tríade letal) · T5 investigar antes de responder · T6 escopo mínimo · T7 testes verificam, não definem · T8 tarefa longa multi-janela · T9 revisor adversarial em contexto limpo · T10 judge binário com crítica · T11 entrevista → spec · T12 metaprompt de melhoria · T13 CLAUDE.md mínimo · T14 ficha de documentação de prompt · T15 consulta estruturada para RAG · T16 few-shot bem formado · T17 tool description como docstring · T18 updates ao usuário. Todos derivados de fontes acima com redação própria; testar no modelo-alvo antes de adotar.

## 5. Princípios e achados transversais

- Explique o porquê e dê instrução positiva com fallback; proibição seca é frágil (R-11, R-26, R-10).
- Linguagem calma: CAPS/"CRITICAL"/"MUST" causam over-trigger em modelos atuais; ênfase em uma linha só e quando falha observada; ALWAYS/NEVER só para invariantes (R-26, R-03, R-28, R-06).
- Remova anti-preguiça ("seja exaustivo", "se em dúvida use a tool") ao migrar de geração; reconstrua do menor núcleo e meça (R-03, R-26, R-02, R-08).
- Não peça CoT manual a modelos com thinking; peça "verifique contra X antes de terminar" e use `effort`/`thinking_level` (R-04, R-26, R-08). Prefill (Claude ≥4.6) e `budget_tokens` (≥4.7) retornam erro 400 (R-26).
- Raciocínio exibido não é prova: exigir saída de teste/comando/diff/screenshot (R-24, R-28).
- Poucos exemplos diversos e de estrutura idêntica; para tools, interface tipada em vez de exemplos de uso (R-06, R-26, R-27).
- Contexto é recurso finito: dados longos primeiro e tarefa no fim, um estilo de delimitador, CLAUDE.md enxuto, progressive disclosure, hooks para o obrigatório (R-25, R-27, R-28).
- Prompt é código: versionado, revisado, testado; fixar snapshot do modelo e rodar evals a cada mudança (R-05, R-16, R-17).
- Evals: análise de erros antes de infraestrutura; binário com crítica; asserção em código antes de LLM-judge; judge validado contra especialista; ≥3 execuções por variante (R-16, R-17, R-12, R-15).
- Segurança de agentes: conteúdo lido é dado; evitar combinar dados privados + conteúdo não confiável + saída externa; confirmação para ações destrutivas/externas; plano validado antes de escrever (R-21, R-19, R-26).
- Declare modelo-alvo e data de validação; conselhos mudam por modelo (Opus 5 não precisa de self-check; Gemini 3 não mexer em sampling) (R-26, R-08).
- Conflitos a decidir por medição: nº de exemplos (0 a ≥12), XML vs Markdown, posição da instrução, role prompting, sampling (comparação do atlas, R-06/R-14/R-26).
- Cuidado com métricas de fonte: arquivadas (OpenAI 4.1/5/5.1) e 2023 (Weng, Brex) servem a modelos antigos; estrelas não provam qualidade.

## 6. Sugestões à rubrica (resumo; o atlas lista 16, não aplicadas)

Aprovadas pelo validador para proposta ao dono da rubrica: D10 verificável (zero CAPS/MUST fora de invariantes); D7 "raciocínio não é evidência"; D12 checklist de API/modelo obsoletos com campo "modelo-alvo + data"; D8 teste da tríade letal; critério de reprovação para instruções contraditórias sem prioridade e para truques datados; validador exige ≥30 casos `designed_not_executed` e ≥3 execuções por variante. Não editei a rubrica.

## 7. Lacunas remanescentes

Itens não reverificados listados em §1; fontes PT-BR de nível A/B inexistentes; páginas por modelo da Anthropic não lidas individualmente; GitHub API não usada (HTML); nenhuma verificação de última data de commit por falta de dado nas páginas.
