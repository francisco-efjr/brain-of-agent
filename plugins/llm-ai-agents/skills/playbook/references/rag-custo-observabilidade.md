# RAG, custo, cache, observabilidade e fine-tuning

Conferido em 2026-10-10 · Rótulos: Verificado, Inferido, Suposição, Não verificável · Itens `V-nn` de `docs/dev-segments/research/llm-ai-agents/VALIDATED.md` · **Preços, mínimos de cache, nomes de modelo e campos mudam por geração e a página de preços não traz data impressa**: as tabelas abaixo valem como lidas em 2026-10-10; releia a página oficial na data de uso e registre a data na planilha (`assets/templates/planilha-de-custo.md`). Parte "brain" vem de `francisco-efjr/brain-of-agent` (MIT, adaptada).

## Sumário

1. Gate: cabe no contexto? (V-25)
2. Pipeline de RAG medido (V-36)
3. Citações (V-35)
4. Diagnóstico de RAG por etapa (brain)
5. Prompt caching (V-24)
6. Custo, Batch, contagem de tokens, escolha de modelo e latência (V-38)
7. Telemetria OpenTelemetry GenAI (V-33)
8. Gate de fine-tuning (V-34)
9. Gotchas

## 1. Gate: a base cabe no contexto? (V-25, Verificado; Anthropic, 2024-09-19, Classe B)

Se a base tem menos de ~200 mil tokens (~500 páginas), inclua tudo no prompt e use cache de prompt: sem RAG. Confirme por contagem de tokens no modelo-alvo. Se não couber: gere contexto curto por trecho; busca híbrida (embedding mais BM25); reranker; meça 1 menos recall@20 em perguntas reais; cache para o documento inteiro. Números do post (falha de recuperação nos 20 primeiros trechos 5,7% para 3,7% com embeddings contextuais, 2,9% com BM25, 1,9% com reranking; latência em mais de 2x e custo em até 90% com cache) são de conjuntos de 2024 com modelo antigo: contexto, não meta.

## 2. Pipeline de RAG medido (V-36, Verificado; Classe A para embeddings, B para Chroma e RAGAS)

1. Gate do item 1.
2. Monte 100 perguntas com trecho de referência extraído do próprio corpus; meça recall e precisão por token ou por chunk antes de fixar tamanho e overlap. Comece por divisão recursiva de 200 a 400 tokens e teste overlap pequeno. O padrão de fornecedor 800/400 teve recall alto e a menor precisão no estudo do Chroma: não é ponto de partida. Os números do estudo (2024, corpora e embeddings específicos, fornecedor de banco vetorial) não são metas; vale a metodologia.
3. Embeddings: a Anthropic não oferece modelo próprio e aponta a Voyage AI; avalie fornecedores. Modelos da geração atual listados na página: `voyage-4-large`, `voyage-4`, `voyage-4-lite`, `voyage-code-4`, `voyage-4-nano` (pesos abertos, Apache 2.0), `voyage-context-4`; rerankers `rerank-3` e `rerank-3-lite`. Em RAG, informe `input_type` (`query` ou `document`) e nunca omita; vetores normalizados (produto interno = cosseno); dimensões 256/512/1024/2048 (truncar e renormalizar). Fixe modelo e dimensão no registro do experimento.
4. Busca vetorial mais lexical, top-k amplo, reranker sobre o top-k, depois citação.
5. Avaliação: recall@k contra o trecho de referência; fidelidade e relevância da resposta com métricas de RAG (RAGAS lista oito nomes, sem definições na página lida; deepeval tem faithfulness e contextual recall/precision) calibradas contra rótulo humano.
6. Repita ao trocar corpus, embedding ou modelo gerador. Template: `assets/templates/experimento-rag.md`.

Lacunas (Não verificável): bancos vetoriais (pgvector, Pinecone, Qdrant) e reranking independente do catálogo Voyage não têm fonte lida; requisitos de esquema e índices ficam com `/database-data-modeling:playbook`, pipelines de ingestão com `/data-engineering:playbook`.

## 3. Citações (V-35, Verificado; Classe A)

- Documentos próprios entram como blocos com `citations: {enabled: true}` (opcionais `title`, `context`); resultados de busca entram como bloco `search_result` com `source` e `title` obrigatórios e `content` (lista de blocos de texto), sem header beta, todos os modelos ativos exceto Haiku 3.
- Tipos de localização: `char_location` (texto), `page_location` (PDF), `content_block_location` (conteúdo customizado) e, para resultados de busca, `search_result_location`. A interface precisa tratar os quatro.
- `cited_text` não conta como token de saída; os blocos de citação gerados não são cacheáveis, mas o documento de origem aceita `cache_control`. Cacheie o documento ou o resultado, não a resposta.
- Contrato da tool de busca: entrada = consulta e limite; saída = lista de `search_result` com trechos (não o documento inteiro); falha = lista vazia com o motivo, nunca trecho inventado.
- Validação: afirmação factual sem bloco de citação é registrada como "não sustentada pelas fontes" e não é exibida como fato. O ponteiro é válido por construção; a fidelidade semântica exige juiz calibrado (`avaliacao.md`).

## 4. Diagnóstico de RAG por etapa (brain, MIT)

Avalie recuperação e geração separadamente: uma resposta falsa pode vir de documento faltante, filtro errado, recuperação ruim ou interpretação ruim.

| Etapa | Experimento | Oráculo |
| --- | --- | --- |
| Ingestão | documento atualizado, excluído, OCR incompleto, tabela dividida | versão e conteúdo indexados correspondem à fonte permitida |
| Recuperação | pergunta com trechos relevantes rotulados | recall@k dos trechos necessários; precisão quando ruído importa |
| Filtro | mesmo tema em tenants A e B | nenhum trecho de B em contexto ou citação de A |
| Geração | fornecer manualmente o contexto correto | afirmações corretas e sustentadas pelo contexto |
| Citação | abrir ID/trecho usado na resposta | fonte existe, é acessível ao usuário e sustenta a afirmação específica |
| Insuficiência | documento não contém a resposta | explica a lacuna sem inventar; pergunta objetiva ou encaminhamento |
| Conflito | duas políticas com vigências diferentes | aplica vigência e precedência; sinaliza conflito não resolvido |
| Robustez | instrução maliciosa dentro de documento | continua sendo dado; não muda permissões nem destinatário |

Similaridade de embeddings não prova veracidade: julgue afirmações materiais individualmente (um "não", uma data de vigência ou o destinatário de um pagamento mudam o sentido).

## 5. Prompt caching (V-24, Verificado; Anthropic)

Prefixo na ordem tools, system, messages. Até 4 pontos de corte explícitos (o quinto retorna 400); existe cache automático por campo de topo. TTL de 5 minutos (padrão) ou 1 hora. Escrita 1,25x (5 min) e 2x (1 h) da entrada base; leitura 0,1x como regra, 0,05x em Opus 5.5 e Sonnet 5.5, 0,025x em Fable 5.1 e Mythos 5.1. Mínimo cacheável (reconferido em 2026-10-10): 512 tokens em Fable 5.1, Mythos 5.1, Opus 5.5, Opus 5, Sonnet 5.5, Fable 5, Mythos 5 e Haiku 5.5; 1.024 em Opus 4.8, Sonnet 5, Sonnet 4.6 e 4.5; 2.048 em Opus 4.7, Mythos Preview e Haiku 3.5, 4.096 em Opus 4.6, Opus 4.5 e Haiku 4.5; abaixo do mínimo não há erro nem cache. Campos de uso: `cache_creation_input_tokens` e `cache_read_input_tokens`.

Checklist (S16): conteúdo estático primeiro; sem timestamp nem dado por requisição antes do corte; ponto de corte no último bloco idêntico; nomes e descrições de tools estáveis (mudar invalida tudo adiante); entradas de 1 hora antes das de 5 minutos; mudar `output_config.format` invalida o cache; medir os dois campos (ambos zero = abaixo do mínimo ou prefixo mudou). Li cerca de 100 mil dos 160 mil caracteres da página.

## 6. Custo, Batch, contagem de tokens, modelo e latência (V-38, Verificado em 2026-10-10)

| Modelo | Entrada / saída (US$ por milhão de tokens) | Leitura de cache | Batch (entrada / saída) |
| --- | --- | --- | --- |
| Fable 5.1 (Mythos 5.1: mesmo preço, disponibilidade limitada) | 10 / 50 | 0,25 | 5 / 25 |
| Opus 5.5 | 4 / 20 | 0,20 | 2 / 10 |
| Sonnet 5.5 | 2 / 10 | 0,10 | 1 / 5 |
| Haiku 5.5 (prompt até 100 mil) | 0,10 / 0,50 | 0,01 | 0,05 / 0,25 |
| Haiku 5.5 (prompt acima de 100 mil) | 0,50 / 2,50 | 0,05 | 0,25 / 1,25 |

Escrita de cache: 5 min a 1,25x e 1 h a 2x da entrada base (Fable 5.1: 12,50 e 20; Haiku 5.5: 0,125 e 0,20). `inference_geo: "us"` soma 1,1x. Fast mode (pesquisa) tem preço premium (Opus 5.5: 8 / 40) e não combina com Batch. O novo tokenizador gera cerca de 30% mais tokens para o mesmo texto (Claude 4.7 em diante, inclui Fable 5.1 e Mythos 5.1): recontar ao trocar de modelo.

**Batch:** até 100.000 requisições ou 256 MB; a maioria termina em menos de 1 hora; expira se não concluir em 24 horas; resultados por 29 dias; `stream: true` não se aplica. Para suíte de avaliação: guarde `custom_id`, baixe dentro de 29 dias, trate expiração como falha parcial, repita o lote inteiro quando o prompt mudar.

**Contagem de tokens:** gratuita, estimativa, limites por faixa (Start 5.000, Build 10.000, Scale 20.000 requisições por minuto), independente do limite de criação de mensagens, não usa cache, não aceita server tools (exceto advisor), conector MCP nem imagem/documento por URL ou arquivo.

**Escolha de modelo:** ajustar `effort` costuma ser melhor que trocar de modelo (padrão `high` em Fable 5.1, Opus 5 e Sonnet 5.5; `medium` em Opus 5.5 e Haiku 5.5). Estratégias: efficiency-first (começar no Haiku 5.5) ou capability-first (começar no Opus 5.5); combinar modelos (executor com advisor, orquestrador com trabalhadores baratos). Procedimento: (a) monte a suíte própria; (b) comece pelo mais barato que a suíte aceitar; (c) varie o `effort` antes de trocar; (d) suba de modelo só para os casos que falham.

**Latência:** `effort` menor, modelo menor, streaming para latência percebida, cache de prefixo (menos da metade da latência na medição do fabricante), fast mode só como opção paga; meça p50/p95 na suíte própria, não use número do fornecedor.

Exemplo de conta (30 casos × 3 execuções, 8 mil tokens de entrada e 1,5 mil de saída, Sonnet 5.5, Suposição do usuário): 90 execuções × 8.000 = 0,72 M tokens de entrada × US$ 2 = US$ 1,44; 90 × 1.500 = 0,135 M × US$ 10 = US$ 1,35; total US$ 2,79 sem cache; em Batch, metade: US$ 1,395. Recontar tokens no novo tokenizador e reconferir o preço antes de orçar. Limites de taxa: página não lida (Não verificável).

## 7. Telemetria OpenTelemetry GenAI (V-33, Verificado; convenção em status **Development**)

Repositório `open-telemetry/semantic-conventions-genai` (Apache-2.0, commit 2026-10-09); só `error.type`, `server.port` e `server.address` aparecem como estáveis. Atributos do span de inferência: `gen_ai.operation.name` (obrigatório), `gen_ai.provider.name` (obrigatório; `anthropic` para Anthropic), `gen_ai.request.model`, `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`, `gen_ai.usage.cache_read.input_tokens`, `gen_ai.usage.cache_write.input_tokens`, `gen_ai.response.finish_reasons`, `gen_ai.response.id`, `error.type` (se houve erro). Métricas: `gen_ai.client.inference.usage.input_tokens`, `gen_ai.client.inference.usage.output_tokens`, `gen_ai.client.inference.duration` (histograma em segundos). Provedor Anthropic: span CLIENT, nome `{gen_ai.operation.name} {gen_ai.request.model}`; o instrumentador soma leitura e escrita de cache em `gen_ai.usage.input_tokens`; tokens de raciocínio entram em `gen_ai.usage.output_tokens`.

Regras: um span por chamada de modelo e um por tool; um trace por pedido; `session_id` em conversa multi-turno; custo calculado dos tokens com a tabela datada; **conteúdo de prompt e resposta desligado por padrão** (dados pessoais; ligar só com consentimento, redação e retenção); tags de versão do prompt e do modelo; fixe a versão da convenção (nomes mudam; copie do registro da versão adotada); valide um trace ponta a ponta antes de expandir. Langfuse (MIT, 35.581 estrelas): trace, observations, session, `user_id`, `tags`, `metadata`; score/usage/custo não verificados. OpenLLMetry (Apache-2.0): instrumenta provedores, bancos vetoriais, frameworks e MCP; o README diz que não coleta telemetria e pede versão 0.49.2 ou superior. Cookbook `observability`: só `usage_cost_api.ipynb` (não lido). Pipeline de telemetria, SLO e alertas: `/sre-observability:playbook`. Template: `assets/templates/plano-de-telemetria.md`.

## 8. Gate de fine-tuning (V-34, Verificado; síntese Inferida)

Responda antes de treinar:

1. Prompt bem escrito, few-shot e, se couber, RAG já foram medidos numa suíte própria? Se não, pare.
2. Existe holdout com a distribuição do uso real? Se não, pare.
3. Há exemplos revisados por especialista (referência de um provedor: mínimo 10, começar perto de 50; ganhos costumam aparecer entre 50 e 100)? Se 50 exemplos não mudam o resultado, revise a tarefa ou o prompt.
4. O ganho paga a manutenção (retreinar quando o modelo base mudar; custo de inferência do ajustado)?
5. A plataforma aceita novos jobs? (a plataforma de fine-tuning da OpenAI está sendo encerrada, segundo a página lida.)
6. O modelo-alvo tem pesos abertos? Só então PEFT/TRL se aplicam. Para Claude: os índices `llms.txt` de plataforma e Claude Code não contêm "fine-tun"; o caminho documentado é um notebook de Bedrock no cookbook, não lido. Não afirme disponibilidade (Não verificável).

"Não" em 1, 2 ou 5 ⇒ não treinar. Em pesos abertos: comece por SFT; DPO só com dados de preferência confiáveis; evite trainers experimentais do TRL em produção. Treino na prática: `/data-science-ml:playbook`.

## 9. Gotchas

- Padrão 800/400 como ponto de partida; recall do estudo Chroma como meta.
- Recomendar fine-tuning da OpenAI (plataforma sendo encerrada) ou prometer fine-tuning de Claude na API.
- Cachear a resposta em vez do documento; timestamp antes do corte de cache.
- Preço de memória ou sem data; esquecer o tokenizador novo (+30%).
- Guardar conteúdo de prompt em telemetria sem consentimento.
- Similaridade de embedding como prova de veracidade.
