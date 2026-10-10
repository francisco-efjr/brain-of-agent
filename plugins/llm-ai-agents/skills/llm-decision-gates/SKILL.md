---
name: llm-decision-gates
description: "Decide entre prompt, RAG e fine-tuning; planeja RAG (chunking, embeddings, reranking, citações) com medição; escolhe modelo e effort; estima custo e latência com preços datados, cache e Batch. Use para 'fine-tuning ou RAG?', chunking, embeddings, qual modelo, custo de tokens, latência, reduzir custo, RAG vs contexto longo. Não use para revisar código do cliente (llm-api-client-review) nem para treinar modelos na prática (data-science-ml)."
argument-hint: "[caso de uso e números conhecidos]"
allowed-tools: Read, Grep, Glob
---

# llm-decision-gates: medir antes de indexar, treinar ou trocar de modelo

Objetivo: responder, item a item e com evidência, se o caso pede prompt, RAG ou fine-tuning; qual modelo e `effort` testar primeiro; e quanto a rodada custa, com preços datados. Razão: cada atalho (RAG por padrão, fine-tuning por impulso, modelo maior por medo) cria custo de manutenção que a medição teria evitado (V-25, V-34, V-38).

Esta skill decide e planeja. Não treina modelo, não indexa corpus, não faz chamadas pagas. Preços, mínimos de cache e matriz de modelos mudam por geração: tudo que for número volátil leva a data da leitura e remete à página oficial.

## Entradas

Argumentos recebidos: $ARGUMENTS (vazio: pergunte o caso de uso, o tamanho do corpus e o volume).

- Tamanho e volatilidade do corpus (páginas, tokens, frequência de mudança) e tipo de pergunta (fatos pontuais, síntese, raciocínio sobre tudo).
- Volume (requisições por dia), latência e custo aceitáveis, requisitos de citação.
- Suíte de avaliação existente (ou não) e exemplos reais. Qualquer número do usuário vira **Suposição** até conferido.
- Modelo-alvo atual e superfície (API direta, Bedrock etc.).

## Pré-checagens

1. Há suíte própria? Sem ela, nenhuma decisão aqui é "recomendada": é hipótese a medir. Encaminhe para `eval-design`.
2. Conte tokens do corpus com a contagem de tokens da API (gratuita, é uma estimativa; recontar ao trocar de modelo) em vez de converter páginas de cabeça (V-38).
3. Preços: abra https://platform.claude.com/docs/en/about-claude/pricing e registre a data. A tabela deste plugin é de 2026-10-10 e pode estar velha.
4. Fine-tuning direto de Claude: não afirme disponibilidade. Os índices de documentação consultados não têm página sobre isso (ausência de página, não prova de inexistência); o cookbook tem um notebook de Bedrock cujo conteúdo não foi lido (V-34, conflito C12).

## Passos

1. **Gate de fine-tuning** (V-34) em [gates-ft-rag.md](references/gates-ft-rag.md): (1) prompt bem escrito, few-shot e, se couber, RAG já foram medidos na suíte própria? (2) existe holdout com a distribuição do uso real? (3) há exemplos revisados por especialista (referência de um provedor: mínimo 10, começar perto de 50)? (4) o ganho paga a manutenção? (5) a plataforma ainda aceita novos jobs? (6) o modelo tem pesos abertos? "Não" em 1, 2 ou 5 ⇒ não treinar. PEFT/TRL só para pesos abertos. Saída: respostas item a item e a decisão.
2. **Gate de RAG** (V-25): a base cabe no contexto (abaixo de ~200 mil tokens, ~500 páginas)? Então prompt completo com cache de prompt e sem RAG. Saída: contagem de tokens e a decisão.
3. **Se for RAG, plano medido** (V-36, V-35): 100 perguntas com trecho de referência extraído do corpus; medir recall e precisão por chunk ou token antes de fixar tamanho e overlap; começar por divisão recursiva de 200 a 400 tokens e overlap pequeno; embeddings com `input_type` correto e fixar modelo e dimensão; busca vetorial + lexical (BM25), top-k amplo, reranker, depois citações com `search_result`; avaliar recuperação e geração separadamente. Saída: plano de experimento (template `experimento-rag.md`).
4. **Modelo e `effort`** (V-38): monte a suíte; comece pelo modelo mais barato que a suíte aceitar; varie o `effort` antes de trocar de modelo; suba de modelo só para os casos que falham. Saída: ordem de experimentos.
5. **Latência** (**Inferido** a partir de V-24, V-25, V-38; sem página de latência lida): `effort` menor, modelo menor, streaming para latência percebida, cache de prefixo (a fonte de RAG relata menos da metade da latência em medição do fabricante), fast mode só como opção paga em pesquisa e sem combinar com Batch. Meça p50/p95 na suíte própria. Saída: alavancas ordenadas por custo/benefício esperado.
6. **Planilha de custo** ([custo-modelo-latencia.md](references/custo-modelo-latencia.md)): por tarefa, tokens de entrada (com e sem cache), saída, execuções e fator de Batch; data dos preços; recontagem de tokens ao trocar de modelo (o tokenizador novo gera cerca de 30% mais tokens a partir do Claude 4.7). Mostre a conta. Saída: tabela com a conta visível.
7. **Cache** (V-24): conteúdo estático primeiro; sem timestamp antes do corte; até 4 pontos de corte; mínimos por modelo; medir `cache_creation_input_tokens` e `cache_read_input_tokens`. Para revisar o código que faz isso, use `llm-api-client-review`.

## Verificação

- Cada preço e mínimo citado tem data de leitura e remete à página; valores sem fonte lida agora ficam **Não verificado**.
- Cada número do usuário aparece rotulado **Suposição**.
- O gate está respondido item a item, não com um parágrafo.
- Nada é "recomendado" sem a suíte própria; o plano diz **projetado, não executado**.
- A conta de custo está visível e reproduzível (entradas, multiplicadores, resultado).
- Números de estudos (5,7% para 1,9% de falha de recuperação; 91,9 de recall) não viram meta: valem para os corpora e modelos daquele estudo.

## Formato de saída

1. Decisão (prompt, RAG, fine-tuning ou híbrido) e o gate respondido item a item.
2. Plano de experimento: dados, métricas, parâmetros fixados, critério de parada.
3. Escolha de modelo e `effort` com ordem de teste.
4. Planilha de custo com data dos preços e premissas.
5. Latência: alavancas e como medir.
6. Riscos (qualidade do corpus, vazamento entre tenants, citação sem fidelidade, preços voláteis).
7. Verificado / Inferido / Suposição / Não verificado; próximo passo.

## Exemplo rápido

Pedido: 30 casos × 3 execuções no Sonnet 5.5, ~8 mil tokens de entrada e ~1,5 mil de saída por execução (números do usuário: Suposição). Conta com a tabela de 2026-10-10: 90 execuções; entrada 720.000 tokens × US$ 2/M = US$ 1,44; saída 135.000 × US$ 10/M = US$ 1,35; total US$ 2,79; em Batch (metade do preço) US$ 1,395; reconferir os preços na página oficial antes de usar. Variantes com cache e tokenizador em [custo-modelo-latencia.md](references/custo-modelo-latencia.md).

## Gotchas

- Padrão de fornecedor 800/400 (tamanho/overlap) como ponto de partida: o estudo do Chroma de 2024 achou divisão recursiva de 200 tokens sem overlap consistentemente forte e a configuração 800/400 com recall alto e a menor precisão; use a metodologia, não os números (V-36).
- Recall do estudo como meta: é de corpora e embeddings específicos.
- Recomendar fine-tuning da OpenAI: a plataforma está sendo encerrada, segundo a página lida (V-34).
- Similaridade de embedding como prova de veracidade: texto parecido pode trocar um "não" ou uma data de vigência (brain `ia-e-llm`).
- Omitir `input_type` (`query`/`document`) nos embeddings de RAG (V-36).
- Cachear a resposta em vez do documento ou do prefixo (V-35, V-24).
- Orçar com a tabela de preços velha: reconfira; o preço de Haiku 5.5 muda acima de 100 mil tokens de prompt (V-38).
- Esquecer que mudar `output_config.format` invalida o cache de prompt (V-37).
- Usar Batch para tudo: expira em 24 h e `stream: true` não se aplica; não serve para fluxo interativo.
- Bancos vetoriais (pgvector, Pinecone, Qdrant): sem fonte lida; não recomende um específico (lacuna de fonte declarada em `fontes.md`). O plugin de banco de dados é dono do tema.

## Quando delegar

Para revisar código ou configuração de um pipeline de RAG existente (ingestão, `input_type`, filtro por tenant, rerank, citações), delegue ao agente `rag-pipeline-reviewer` (somente leitura) com o briefing: caminhos, modelo de embedding, parâmetros, formato de saída. Para a suíte e o juiz, `eval-designer`/`eval-design`. Para o cliente da API, `llm-api-client-review`. Treino na prática: segmento `data-science-ml`.

## Referências

- [gates-ft-rag.md](references/gates-ft-rag.md): gate de fine-tuning, gate de RAG, plano medido, citações, diagnóstico por etapa.
- [custo-modelo-latencia.md](references/custo-modelo-latencia.md): tabela de preços datada, contas de exemplo, cache, Batch, escolha de modelo, latência.
- Compartilhadas: `${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/rag-custo-observabilidade.md`, `${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/decisoes-e-tradeoffs.md`; templates `planilha-de-custo.md`, `experimento-rag.md` em `${CLAUDE_PLUGIN_ROOT}/skills/playbook/assets/templates/`.
- Fontes: V-24, V-25, V-34, V-35, V-36, V-38, V-11; brain `ia-e-llm` (diagnóstico de RAG).
