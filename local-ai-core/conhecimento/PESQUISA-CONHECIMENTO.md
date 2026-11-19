# Pesquisa: core de pesquisa e conhecimento

Data: 2026-11-19 · Pesquisador: Claude Opus 5.5 (Claude Code) · Consultas de busca: 52 · Páginas abertas: 13 (4 lidas na íntegra, 9 por resumo) · Fontes catalogadas: 57 (45 de classe A, 12 de classe B).

Explica de onde veio cada regra do [CORE-CONHECIMENTO.md](CORE-CONHECIMENTO.md), da [REFERENCIA-CONHECIMENTO.md](REFERENCIA-CONHECIMENTO.md) e da generalização feita no [CORE-BASE.md](../CORE-BASE.md). Segue a rubrica e o método de pesquisa da casa (S-01, S-21). Status de leitura e rótulos como em `../windows/PESQUISA-WINDOWS.md`: **Íntegra**, **Resumo** ou **Busca**.

## Sumário

1. Método
2. Achados principais
3. Validação da esteira para pesquisa
4. O que muda na base comum
5. Achados sobre o OpenJarvis
6. Decisões de desenho
7. Tensões a decidir por medição
8. Limites
9. Fontes

## 1. Método

Quatro lentes, como pede o método da casa (uma oficial, uma de bases e exemplos, uma de prática): método de checagem e avaliação de fontes (bibliotecas, checadores, medicina baseada em evidência); pesquisa sobre LLMs, RAG e alucinação (artigos revisados, documentação da Anthropic e da OpenAI); ferramentas locais (OpenJarvis, Ollama, SQLite, embeddings); e gestão de conhecimento e livros. Nada foi executado no PC do usuário: tudo que é comando ou configuração fica **Não verificado na máquina-alvo** até rodar os casos de [evals/CASOS-CONHECIMENTO.md](evals/CASOS-CONHECIMENTO.md).

## 2. Achados principais

1. **Esforço proporcional à pergunta.** A Anthropic embutiu no prompt do seu sistema de pesquisa: fato simples com 3 a 10 chamadas, comparação com 2 a 4 subagentes de 10 a 15 chamadas cada, pesquisa complexa com mais de 10 subagentes; sem isso, agentes gastavam demais em perguntas simples (R-06).
2. **Comece amplo, depois estreite.** Consultas longas e específicas demais voltavam vazias; a correção foi buscar curto, ver o que existe e afunilar (R-06).
3. **Agentes preferem fazendas de SEO** a fontes boas, até receberem heurísticas de qualidade de fonte no prompt (R-06). Daí a hierarquia de fontes explícita no core.
4. **Leitura lateral funciona.** Checadores profissionais, saindo da página para ver o que outros dizem dela, chegaram a conclusões melhores e mais rápidas que historiadores e estudantes (S-03). O SIFT empacota isso em quatro passos (S-02).
5. **"Não sei" reduz invenção.** Permitir admitir incerteza, extrair citações literais antes de responder e exigir uma citação por afirmação, retirando a que não tiver, são as técnicas básicas da Anthropic (R-04). Perguntas de verificação respondidas em separado reduzem alucinação (R-05); divergência entre amostras sinaliza alucinação (R-08).
6. **Referências inventadas são comuns.** 55% das citações do GPT-3.5 e 18% das do GPT-4 eram fabricadas num estudo de 2023 (R-14). Daí a invariante "nunca invente fonte" e a checagem de DOI no Crossref (S-16).
7. **Conteúdo recuperado pode atacar.** Injeção indireta controla modelos por instruções escondidas em páginas e documentos (R-15); poucos textos maliciosos envenenam uma base de RAG com alta taxa de sucesso (R-16, R-17).
8. **A consulta é um dado.** Logs de busca "anonimizados" identificaram uma pessoa pelas próprias buscas (S-19). A busca web do OpenJarvis usa provedores externos por padrão (L-01). Daí a invariante de privacidade nas consultas.
9. **Recuperar bem pesa mais que gerar bem.** Busca híbrida (BM25 mais vetores) com fusão por posição (R-11, B-01) e contexto acrescentado a cada trecho antes de indexar reduziram falhas de recuperação nas avaliações da Anthropic (R-10). O OpenJarvis já traz o backend híbrido com RRF (L-02).
10. **Evidência tem níveis.** GRADE e a tabela do Oxford CEBM graduam a certeza; preprints não são revisados (S-06, S-07, S-09). Daí a regra de declarar o nível de evidência em saúde.
11. **Links morrem.** 38% das páginas de 2013 já não existiam em 2023 (S-17): data de acesso e arquivo para fonte importante.
12. **Avaliar com poucas perguntas reais já mostra muito.** A Anthropic começou com cerca de 20 perguntas e um juiz com critérios de precisão factual, precisão de citação, completude, qualidade de fonte e eficiência (R-06); o RAGAS mede fidelidade ao contexto e relevância (R-03).

## 3. Validação da esteira para pesquisa

A esteira da base serve à pesquisa sem mudança de passos. O estudo confirma que verificar (está certo?) e validar (é a pergunta certa?) são o centro de uma boa pesquisa, e ajusta o sentido de alguns passos:

| Passo | Em pesquisa | Evidência |
| --- | --- | --- |
| 0 Classificar | Classe pelo impacto do erro e pela exposição de dados; define o orçamento de chamadas | R-06; S-06, S-07 |
| 1 Estruturar | Reescrever a pergunta e consultar a base local primeiro, buscando fora só se a base não bastar | R-02, R-12 (decidir quando recuperar e quando ir à web) |
| 2 Visão | Hipótese de resposta e o que precisaria ser verdade | R-05 (rascunho que depois é verificado) |
| 3 Testar a visão | Busca exploratória curta e ampla | R-06 |
| 4 Validar a visão | Gate humano só quando há efeito (dado pessoal sai, custo); sem efeito, autoconferência | Ajuste do estudo: aprovação liga-se a efeito, não a leitura |
| 5 Conceber | Plano de busca: termos, idiomas, fontes previstas, orçamento; salvo em arquivo na pesquisa ampla | S-08 (protocolo antes de buscar), R-06 (plano salvo) |
| 6 Produzir | Coletar e ler com SIFT e leitura lateral; citações literais primeiro | S-02, S-03, R-04, R-18 |
| 7 Testar de novo | Checagem por afirmação, perguntas de verificação, consistência, DOI conferido | R-04, R-05, R-08, R-14, S-16 |
| 8 Validar o escopo | Responde à pergunta feita? Completa? Lacunas declaradas? | R-06 (critério de completude) |
| 9 Implementar | Entregar no formato RESPOSTA, EVIDÊNCIA, CONFIANÇA, LACUNAS, FONTES | R-04, R-19 |
| 10 Verificar e registrar | Passe de citação final e nota na base local com data de revisão | R-06 (agente de citação), S-18, B-06 |

## 4. O que muda na base comum

Com o segundo tema, a esteira, as classes de risco, as invariantes gerais, os formatos e as regras de parada saíram do core do Windows para o `CORE-BASE.md`, como o README previa. Três generalizações vieram do estudo:
- **Risco medido por efeito e por impacto do erro.** R2 passa a incluir "envia dado do usuário para fora" e "embasa decisão importante"; R3, "embasa decisão de saúde, jurídica, financeira ou de segurança".
- **Aprovação para efeito, rigor para leitura.** Pesquisa pura não pede "sim"; o que sobe é a verificação e a declaração de confiança.
- **Duas invariantes novas na base:** nada pessoal sai da máquina sem aprovação, inclusive em termos de busca; nunca inventar número, nome, URL, citação ou resultado.

## 5. Achados sobre o OpenJarvis

Lido por resumo em 2026-11-19 (L-01, L-02, L-03). Confira na versão instalada.
- `web_search` escolhe o provedor sozinho: Tavily, You.com, Serply ou Firecrawl se houver chave; sem chave, plano gratuito do You.com e, como reserva, DuckDuckGo. SearXNG não aparece. A consulta sempre sai da máquina, exceto com Firecrawl hospedado localmente.
- Memória: SQLite FTS5 com BM25 por padrão em `~/.openjarvis/memory.db`; backends `bm25`, `faiss`, `colbert` e `hybrid` (RRF, k=60); trechos de 512 com sobreposição de 64; o contexto recuperado entra com a origem `[Source: ...]` e um pedido para citar.
- Não está documentado se o agente grava memória sozinho; o caminho documentado é `jarvis memory index`. Por isso a base local do core é feita de arquivos `.md` reindexados.
- `jarvis scan --data-boundaries` audita a configuração e lista o que pode sair da máquina; não bloqueia consultas em tempo real. Útil para o dono conferir a privacidade.
- Inferido, não testado: um SearXNG próprio em `127.0.0.1` com saída JSON ligada (L-07), consultado pelo `http_request`, manteria as consultas sob controle do dono.

## 6. Decisões de desenho

- **Temas compostos.** `montar_core.py` junta base e temas num `CORE.md` único, porque o OpenJarvis aceita um só arquivo de prompt. Dá para montar só os temas desejados.
- **Core curto, referência longa.** Regras e formato no prompt; operadores, fontes brasileiras, níveis de evidência, ABNT, Crossref e RAG na referência sob demanda.
- **Formato de resposta fixo** com confiança e lacunas, porque calibrar e admitir o que falta reduz invenção (R-04, R-09).
- **Base local com proveniência e validade** (`revisar_em`), porque informação envelhece e notas antigas sem data viram fonte de erro.
- **Fontes brasileiras primeiro para assuntos do Brasil** (planalto.gov.br, LexML, IBGE, SciELO, checadores signatários da IFCN), em português, e documentação técnica em inglês.

## 7. Tensões a decidir por medição

- **Tamanho do prompt montado** (base mais dois temas) contra obediência e velocidade. O script mostra a estimativa de tokens; se o modelo local piorar, monte só os temas do uso do dia ou corte exemplos.
- **Buscar amplo contra privacidade.** Consultas amplas são boas para descobrir, mas saem da máquina; o core generaliza os termos e pede aprovação para dado pessoal.
- **Duas fontes independentes contra velocidade.** Para fato trivial, uma fonte primária basta; a regra das duas vale para o que importa.
- **Embeddings em português.** Rankings multilíngues não preveem bem o desempenho em português (L-05): medir com perguntas reais antes de trocar o backend padrão.

## 8. Limites

- A maioria das fontes foi conferida por trechos de busca; quatro foram lidas na íntegra e a documentação do OpenJarvis, por resumo.
- Livros não foram lidos de capa a capa; entram como referência de aprofundamento.
- A NBR 6023 é norma paga: foi lida por guias de universidades, que citam uma possível edição mais nova.
- Endereços oficiais de órgãos de saúde e economia não foram abertos; a referência marca isso como Inferido.
- Os percentuais citados (fabricação de referências, recuperação, links mortos) são dos autores originais, dependem de modelo e data, e não foram reproduzidos.

## 9. Fontes

### 9.1 LLMs, RAG e alucinação (R)

| ID | Fonte | Classe | Status | Usado em |
| --- | --- | --- | --- | --- |
| R-01 | [Lewis et al. Retrieval-Augmented Generation (NeurIPS 2020)](https://arxiv.org/abs/2005.11401) | A | Busca | O que é RAG |
| R-02 | [Asai et al. Self-RAG (ICLR 2024)](https://arxiv.org/abs/2310.11511) | A | Busca | Decidir quando recuperar e criticar a recuperação |
| R-03 | [Es et al. Ragas](https://arxiv.org/abs/2309.15217) | B | Busca | Avaliar fidelidade e relevância |
| R-04 | [Anthropic: Reduce hallucinations](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations) | A | Íntegra | "Não sei", citações literais, uma citação por afirmação, consistência |
| R-05 | [Dhuliawala et al. Chain-of-Verification (Findings ACL 2024)](https://arxiv.org/abs/2309.11495) | A | Busca | Perguntas de verificação separadas |
| R-06 | [Anthropic: How we built our multi-agent research system (2025-06-13)](https://www.anthropic.com/engineering/multi-agent-research-system) | A | Íntegra | Orçamento de esforço, amplo antes de específico, qualidade de fonte, passe de citação, avaliação |
| R-07 | [Min et al. FActScore (EMNLP 2023)](https://arxiv.org/abs/2305.14251) | A | Busca | Fatos atômicos sustentados |
| R-08 | [Manakul et al. SelfCheckGPT (EMNLP 2023)](https://arxiv.org/abs/2303.08896) | A | Busca | Divergência entre amostras como sinal |
| R-09 | [Kadavath et al. Language Models (Mostly) Know What They Know (2022)](https://arxiv.org/abs/2207.05221) | A | Busca | Calibração e seus limites |
| R-10 | [Anthropic: Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) | A | Busca | Contexto no trecho, BM25 mais vetores |
| R-11 | [Reciprocal Rank Fusion (Cormack et al., 2009), explicação](https://redis.io/blog/reciprocal-rank-fusion/) | B | Busca | Fusão por posição, k=60 (artigo original não lido) |
| R-12 | [Yan et al. Corrective RAG](https://arxiv.org/abs/2401.15884) | B | Busca | Avaliar a recuperação e ir à web quando ela falha |
| R-13 | [Edge et al. GraphRAG (Microsoft Research)](https://arxiv.org/abs/2404.16130) | A | Busca | Perguntas sobre a base inteira |
| R-14 | [Walters e Wilder. Fabrication and errors in bibliographic citations generated by ChatGPT (Scientific Reports, 2023)](https://www.nature.com/articles/s41598-023-41032-5) | A | Busca | Referências inventadas |
| R-15 | [Greshake et al. Indirect Prompt Injection (AISec 2023)](https://arxiv.org/abs/2302.12173) | A | Busca | Injeção por conteúdo recuperado |
| R-16 | [Zou et al. PoisonedRAG (USENIX Security 2025)](https://www.usenix.org/conference/usenixsecurity25/presentation/zou) | A | Busca | Envenenamento da base |
| R-17 | [OWASP LLM08:2025 Vector and Embedding Weaknesses](https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/) | A | Busca | Riscos de vetores e embeddings |
| R-18 | [Anthropic: Long context prompting tips](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/long-context-tips) | A | Busca | Documento antes da pergunta, citações primeiro |
| R-19 | [Anthropic: Search results content blocks](https://platform.claude.com/docs/en/build-with-claude/search-results) | A | Busca | Resposta com citação por resultado |
| R-20 | [OpenAI: Introducing deep research (2025)](https://openai.com/index/introducing-deep-research/) | A | Busca | Limites declarados: alucinação, dificuldade com fontes |

### 9.2 Método, fontes e checagem (S)

| ID | Fonte | Classe | Status | Usado em |
| --- | --- | --- | --- | --- |
| S-01 | Rubrica de fonte da casa (`docs/dev-segments/foundation/source-quality-rubric.md`) | A | Íntegra | Classes A, B, C |
| S-02 | [Caulfield. SIFT (The Four Moves)](https://hapgood.us/2019/06/19/sift-the-four-moves/) | A | Busca | Pare, investigue, encontre, rastreie |
| S-03 | [Stanford: fact checkers outperform historians (Wineburg e McGrew)](https://news.stanford.edu/stories/2017/10/fact-checkers-outperform-historians-evaluating-online-information) | A | Busca | Leitura lateral |
| S-04 | [Wikipedia: Reliable sources](https://en.wikipedia.org/wiki/Wikipedia:Reliable_sources) | B | Busca | Primária, secundária, terciária |
| S-05 | [ACRL Framework: Authority Is Constructed and Contextual (guia)](https://guides.library.appstate.edu/acrl_framework/authority) | B | Busca | Autoridade depende do contexto |
| S-06 | [Oxford CEBM Levels of Evidence](https://www.cebm.ox.ac.uk/resources/levels-of-evidence/ocebm-levels-of-evidence) | A | Busca | Níveis por tipo de pergunta |
| S-07 | [BMJ Best Practice: What is GRADE?](https://bestpractice.bmj.com/info/evidence/learn-ebm/what-is-grade/) | A | Busca | Certeza alta a muito baixa |
| S-08 | [PRISMA 2020 statement](https://pubmed.ncbi.nlm.nih.gov/33789819/) | A | Busca | Protocolo e fluxo de revisão |
| S-09 | [Guidelines for preprints as a source (PMC, 2020)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7738646/) e [JAMA sobre avisos de preprint](https://jamanetwork.com/journals/jama/fullarticle/2772743) | A | Busca | Preprint não revisado |
| S-10 | [ABNT NBR 6023:2018, manual da UFSCar](https://www.bco.ufscar.br/arquivos/manual-bco-nbr-6023-2018.pdf) | B | Busca | "Disponível em" e "Acesso em" |
| S-11 | [IFCN: avaliação da Lupa](https://mail.ifcncodeofprinciples.poynter.org/application/public/lupa/282CC55D-2D3A-8E87-A7B2-5E98981262F0) e páginas do Estadão Verifica e Aos Fatos | A | Busca | Checadores signatários |
| S-12 | [Planalto: legislação](https://planalto.gov.br/ccivil_03/) e [LexML Brasil](https://www.wikiwand.com/en/articles/LexML_Brasil) | A | Busca | Lei pela fonte primária |
| S-13 | [IBGE: API de agregados](https://servicodados.ibge.gov.br/api/docs/agregados?versao=3) | B | Busca | Estatística oficial (conteúdo da página via pacotes R) |
| S-14 | [Critérios SciELO Brasil (2024)](https://www.scielo.br/media/files/20240900-Criterios-SciELO-Brasil.pdf) | A | Busca | Periódicos brasileiros |
| S-15 | [Google: Refine Google searches](https://support.google.com/websearch/answer/2466433) | A | Busca | Operadores de busca |
| S-16 | [Crossref REST API](https://crossref.org/documentation/retrieve-metadata/rest-api) | A | Busca | Conferir DOI |
| S-17 | [Pew Research: When Online Content Disappears (2024)](https://www.pewresearch.org/data-labs/2024/05/17/when-online-content-disappears/) | A | Busca | Links que somem |
| S-18 | [W3C PROV Primer](https://www.w3.org/TR/prov-primer/) | A | Busca | Proveniência das notas |
| S-19 | [AOL search log release](https://en.wikipedia.org/wiki/AOL_search_log_release) | B | Busca | Consulta identifica pessoa |
| S-20 | [RFC 9309: Robots Exclusion Protocol](https://www.rfc-editor.org/info/rfc9309) | A | Busca | robots.txt |
| S-21 | Método de pesquisa da casa (`docs/dev-segments/METODO-PESQUISA.md`) | A | Íntegra | Lentes, injeção, validação |
| S-22 | [Internet Archive: Save pages in the Wayback Machine](https://help.archive.org/help/save-pages-in-the-wayback-machine/) | A | Busca | Arquivar fonte importante |

### 9.3 Ferramentas locais (L)

| ID | Fonte | Classe | Status | Usado em |
| --- | --- | --- | --- | --- |
| L-01 | [OpenJarvis: tools](https://open-jarvis.github.io/OpenJarvis/user-guide/tools/) e [web_search](https://open-jarvis.github.io/OpenJarvis/api-reference/openjarvis/tools/web_search/) | A | Resumo | Provedores de busca, http_request |
| L-02 | [OpenJarvis: memory](https://open-jarvis.github.io/OpenJarvis/user-guide/memory/) e [arquitetura de memória](https://open-jarvis.github.io/OpenJarvis/architecture/memory/) | A | Resumo | Backends, trechos, `[Source]` |
| L-03 | [OpenJarvis: data boundary scan](https://open-jarvis.github.io/OpenJarvis/user-guide/data-boundary-scan/) | A | Resumo | Auditoria de privacidade |
| L-04 | [Ollama: embeddings](https://docs.ollama.com/capabilities/embeddings) | A | Busca | `/api/embed` |
| L-05 | [MTEB-BR: benchmark de embeddings em português](https://arxiv.org/abs/2607.04581) | B | Busca | Ranking multilíngue não prevê português |
| L-06 | [Ollama: web search](https://docs.ollama.com/capabilities/web-search) | A | Busca | Busca hospedada com chave |
| L-07 | [SearXNG via LangChain](https://docs.langchain.com/oss/python/integrations/providers/searx) | B | Busca | Metabusca própria com JSON |
| L-08 | [SQLite FTS5](https://sqlite.org/fts5.html) | A | Busca | BM25 no backend padrão |

### 9.4 Livros e artigos de referência (B)

| ID | Obra | Classe | Status | Usado em |
| --- | --- | --- | --- | --- |
| B-01 | Manning, Raghavan, Schütze. *Introduction to Information Retrieval*. Cambridge UP, 2008. [edição online](https://nlp.stanford.edu/IR-book/) | A | Busca | BM25, avaliação de recuperação |
| B-02 | Huyen. *AI Engineering*, cap. 6 (RAG e agentes). O'Reilly, 2025. [notas do capítulo](https://alexstrick.com/posts/2025-01-24-notes-on-ai-engineering-chip-huyen-chapter-6.html) | A | Busca | Busca por termo, por vetor e híbrida |
| B-03 | Bergstrom, West. *Calling Bullshit*. Random House, 2020. [editora](https://www.penguinrandomhouse.com/books/563882/calling-bullshit-by-carl-t-bergstrom-and-jevin-d-west/) | A | Busca | Números e gráficos enganosos |
| B-04 | Tetlock, Gardner. *Superforecasting*, e dados do Good Judgment Project. [Good Judgment](https://goodjudgment.com/wp-content/uploads/2021/10/Superforecasters-A-Decade-of-Stochastic-Dominance.pdf) | A | Busca | Calibração |
| B-05 | Forte. *The PARA Method*. [introdução](https://every.to/praxis/para-an-introduction-827085) | B | Busca | Organização da base |
| B-06 | Ahrens. *How to Take Smart Notes*, 2017. [resumo](https://zettelkasten.de/posts/concepts-sohnke-ahrens-explained/) | B | Busca | Nota atômica |
| B-07 | Keshav. *How to Read a Paper* (artigo, 2007). [PDF](https://www.cs.princeton.edu/courses/archive/fall10/cos597B/papers/howtoread-keshav.pdf) | A | Busca | Leitura em três passadas |

Contagem: 20 (R) + 22 (S) + 8 (L) + 7 (B) = 57 fontes.
