# Experimento de RAG

Fontes: V-36, V-25, V-35 e brain `ia-e-llm.md` (MIT, diagnóstico por etapa). Os números dos estudos citados não são metas; vale a metodologia. Status até rodar: **projetado, não executado**.

## 0. Gate

- Tokens do corpus (contagem no modelo-alvo, data): [N]. Cabe em ~200 mil tokens (~500 páginas)? [sim ⇒ prompt completo com cache, sem RAG / não ⇒ continue]

## 1. Parâmetros fixados (registre antes de rodar)

| Parâmetro | Valor |
| --- | --- |
| Corpus (versão/commit/data) | |
| Divisão (recursiva, tamanho em tokens, overlap) | |
| Modelo de embedding, dimensão, `input_type` documento/consulta | |
| Busca (vetorial / lexical / híbrida), top-k | |
| Reranker | |
| Modelo gerador e `effort` | |
| Citações (`citations` ou `search_result`) | |

## 2. Perguntas de referência (≥ 100)

| ID | Pergunta | Trecho de referência (do próprio corpus) | Resposta esperada | Tipo (respondível / insuficiente / conflito / tenant / injeção) |
| --- | --- | --- | --- | --- |

## 3. Métricas por etapa

| Etapa | Experimento | Oráculo | Resultado |
| --- | --- | --- | --- |
| Ingestão | atualizado, excluído, OCR incompleto, tabela dividida | versão e conteúdo indexados = fonte permitida | |
| Recuperação | trechos rotulados | recall@k por chunk ou token; precisão | |
| Filtro | mesmo tema em tenants A e B | nenhum trecho de B em contexto ou citação de A | |
| Geração | contexto correto fornecido à mão | afirmações corretas e sustentadas | |
| Citação | abrir ID/trecho | existe, acessível, sustenta a afirmação específica | |
| Insuficiência | documento sem a resposta | explica a lacuna sem inventar | |
| Conflito | vigências diferentes | aplica precedência ou sinaliza | |
| Robustez | instrução maliciosa em documento | continua sendo dado | |

Fidelidade e relevância da resposta: métricas de RAG (nomes do RAGAS ou do deepeval) calibradas contra rótulo humano; similaridade de embedding não prova veracidade.

## 4. Variações a testar (uma por vez)

Tamanho de chunk (200, 300, 400 tokens), overlap (0, pequeno), híbrida e rerank, `input_type`, modelo de embedding. Repetir ao trocar corpus, embedding ou gerador.

## 5. Conclusão

Configuração escolhida, números com denominador, limites de validade, Suposições e próximo passo.
