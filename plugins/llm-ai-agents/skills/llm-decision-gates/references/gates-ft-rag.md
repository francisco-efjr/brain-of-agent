# Gates de fine-tuning e de RAG, plano medido e citações

Base: V-34 (OpenAI SFT, PEFT, TRL, cookbook; gate é síntese Inferida), V-25 (Contextual Retrieval, 19/09/2024), V-36 (embeddings Voyage, estudo do Chroma de 03/07/2024, RAGAS), V-35 (Citations e Search results), brain `qa/references/ia-e-llm.md` (diagnóstico de RAG, MIT). Conferido em 2026-10-10. Lacunas: nenhum documento lido sobre pgvector, Pinecone, Qdrant nem sobre reranking independente do catálogo Voyage; definições das métricas do RAGAS não lidas.

## Gate de fine-tuning: 6 perguntas

| # | Pergunta | Se a resposta for "não" |
| --- | --- | --- |
| 1 | Prompt bem escrito, exemplos few-shot e, se couber, RAG já foram medidos numa suíte própria? | Pare (a fonte diz "só invista em fine-tuning depois de montar avaliações") |
| 2 | Existe holdout com a distribuição do uso real para comparar o modelo ajustado com o base? | Pare |
| 3 | Há exemplos revisados por especialista? (Referência de um provedor: mínimo 10; começar perto de 50 bem feitos; ganhos costumam aparecer entre 50 e 100.) Se 50 exemplos não mudam o resultado, revise a tarefa ou o prompt antes de coletar mais | Colete e revise antes |
| 4 | O ganho paga a manutenção (retreinar quando o modelo base mudar; custo de inferência do modelo ajustado)? | Não treine |
| 5 | A plataforma ainda aceita novos jobs e mantém modelos ajustados? | Pare (a OpenAI está encerrando a dela: fechada a novos usuários, segundo a página lida) |
| 6 | O modelo-alvo tem pesos abertos? | PEFT/TRL não se aplicam; para API fechada, a Anthropic não documenta fine-tuning direto na plataforma (não afirmar o contrário sem a página oficial) |

Resposta "não" em 1, 2 ou 5 ⇒ não treinar. Em modelos abertos, começar por SFT; DPO só com dados de preferência confiáveis; evitar trainers marcados como experimentais em produção. Referências: PEFT ajusta poucos parâmetros extras e se aplica a pesos abertos; TRL tem trainers estáveis (online: GRPO, RLOO; recompensa: Reward; offline: SFT, DPO, KTO; destilação) e uma lista experimental à parte. Formato típico de dados (provedor citado): JSONL, uma estrutura por linha.

Rótulo: os limites numéricos são de um provedor e de uma data; o gate é síntese (**Inferido**), cada critério ligado a uma fonte.

## Gate de RAG: cabe no contexto?

Se a base tem menos de ~200 mil tokens (~500 páginas), inclua tudo no prompt e use cache de prompt; não use RAG (V-25). Isso é regra da fonte (Anthropic, 2024, modelo antigo): confirme o limite com a janela de contexto do modelo atual e meça.

Como calcular: contar tokens do corpus com a contagem de tokens da API (V-38). Regra de bolso ilustrativa: ~200 mil tokens para ~500 páginas dá ~400 tokens por página (**Inferido**, depende do idioma e do formato). Um manual de 120 páginas teria algo como 48 mil tokens: confirmar por contagem.

Exemplo de decisão (caso `rag-ou-fine-tuning`): "Manual interno de 120 páginas + FAQ. Chefe quer fine-tuning do Claude; colega quer RAG com banco vetorial."

| Item | Resposta | Rótulo |
| --- | --- | --- |
| Cabe no contexto? | Provavelmente sim (~48 mil tokens + FAQ), abaixo de ~200 mil: prompt completo com cache | Inferido; contar tokens |
| Fine-tuning de Claude? | Não afirmo disponibilidade; gate 1 e 2 sem suíte nem holdout ⇒ não treinar | Verificado (ausência de página); Não verificado (disponibilidade) |
| RAG com banco vetorial? | Só se o corpus crescer além do contexto ou a latência/custo medidos pedirem | Inferido |
| Próximo passo | Montar 30 a 50 perguntas reais com resposta de referência; medir prompt completo + cache; comparar | Plano, não executado |

## Plano de RAG medido (V-36, V-25)

1. **Suíte:** 100 perguntas com trecho de referência extraído do próprio corpus (pedidos de síntese e de "não consta" incluídos).
2. **Chunking:** medir recall e precisão por token ou por chunk antes de fixar tamanho e overlap. Comece por divisão recursiva de 200 a 400 tokens com overlap pequeno e teste variações. O padrão de fornecedor (800/400) não é ponto de partida. O estudo do Chroma (5 corpora, 328.208 tokens, ~472 perguntas) usou métricas no nível de token (recall, precisão, precisão com recall perfeito, IoU): metodologia aproveitável, números não.
3. **Embeddings:** a Anthropic não oferece modelo próprio e aponta a Voyage AI, recomendando avaliar fornecedores. Modelos da geração atual na página lida: `voyage-4-large`, `voyage-4`, `voyage-4-lite`, `voyage-code-4`, `voyage-4-nano` (pesos abertos, Apache-2.0, roda local) e `voyage-context-4` (embeddings por chunk com contexto do documento). Informe `input_type` (`query` ou `document`) e nunca omita em RAG; vetores normalizados (produto interno = cosseno); dimensões 256/512/1024/2048 (Matryoshka: truncar e renormalizar). Fixe modelo e dimensão no registro do experimento. Confirme a lista na página: https://platform.claude.com/docs/en/build-with-claude/embeddings.
4. **Recuperação:** busca vetorial mais lexical (BM25), top-k amplo, reranker (`rerank-3` indicado para a maioria; `rerank-3-lite` mais leve) sobre o top-k. Contextual Retrieval: gerar um contexto curto por trecho; a fonte relata a falha de recuperação nos 20 primeiros trechos caindo de 5,7% para 3,7% (embeddings contextuais), 2,9% (com BM25 contextual) e 1,9% (com reranking), recuperando 150 trechos e reordenando para 20. São números dos conjuntos do post de 2024 com modelo antigo: meça de novo com o seu.
5. **Cache:** use cache de prompt para o documento inteiro ao gerar contextos (a fonte relata redução de custo de até 90% e de latência em mais de 2 vezes; medição do fabricante).
6. **Avaliação:** recall@k contra o trecho de referência; fidelidade e relevância da resposta com métricas de RAG (RAGAS lista oito: Context Precision, Context Recall, Context Entities Recall, Noise Sensitivity, Response Relevancy, Faithfulness, Multimodal Faithfulness, Multimodal Relevance; definições não lidas) calibradas contra rótulo humano (ver `eval-design`).
7. **Repetir** a medição ao trocar corpus, embedding ou modelo gerador.

## Diagnóstico de RAG por etapa (brain `ia-e-llm`, adaptado)

Avalie recuperação e geração separadamente: resposta falsa pode vir de documento faltante, filtro errado, recuperação ruim ou interpretação ruim.

| Etapa | Experimento | Oráculo |
| --- | --- | --- |
| Ingestão | documento atualizado, excluído, OCR incompleto, tabela dividida | versão e conteúdo indexados correspondem à fonte permitida |
| Recuperação | pergunta com trechos relevantes rotulados | recall@k dos trechos necessários; precisão quando ruído importa |
| Filtro | mesmo tema em tenants A e B | nenhum trecho de B em contexto ou citação de A |
| Geração | fornecer manualmente o contexto correto | afirmações corretas e sustentadas pelo contexto |
| Citação | abrir ID/trecho usado na resposta | fonte existe, é acessível ao usuário e sustenta a afirmação |
| Insuficiência | documento não contém a resposta | explica a lacuna sem inventar; pergunta objetiva ou encaminha |
| Conflito | duas políticas com vigências diferentes | aplica vigência e precedência; sinaliza conflito não resolvido |
| Robustez | instrução maliciosa dentro de documento | continua sendo dado; não muda permissões nem destinatário |

Julgue afirmações materiais individualmente. Conte recusas corretas e indevidas separadamente.

## Contrato de citações (V-35)

1. Documentos próprios entram como blocos com `citations: {enabled: true}` (`title` e `context` opcionais); resultados de busca entram como blocos `search_result` com `source` e `title` obrigatórios e `content` (lista de blocos de texto).
2. Tool de busca: entrada = consulta e limite; saída = lista de `search_result` com trechos, não o documento inteiro; falha = lista vazia com o motivo, nunca trecho inventado.
3. Validação da resposta: afirmação factual sem bloco de citação é registrada como "não sustentada pelas fontes" e não é exibida como fato.
4. Cachear o documento ou o resultado (aceita `cache_control`), não a resposta; os blocos de citação gerados não são cacheáveis.
5. Interface: tratar quatro tipos de localização: `char_location` (texto), `page_location` (PDF), `content_block_location` (conteúdo customizado) e `search_result_location`. `cited_text` não conta como token de saída.
6. Os ponteiros são válidos por construção; isso não prova que a citação sustenta a afirmação. Avalie a fidelidade com juiz calibrado.
