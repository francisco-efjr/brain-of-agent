---
data: 2026-11-19
tags: [llm-ai-agents, docs-oficiais, seguranca-hardening]
plugins: [llm-ai-agents, security-appsec, web-research-apify]
agentes: [llm-ai-agents:rag-pipeline-reviewer, llm-ai-agents:prompt-reviewer, llm-ai-agents:agent-security-reviewer]
contexto: "Prompt de sistema para IA local (OpenJarvis + Ollama) que pesquisa na web e em documentos e mantém uma base de conhecimento local"
tipo_de_sessao: pesquisa
modelo: claude-opus-5-5
---
# IA local pesquisando: método, citação, base local e privacidade das consultas

Origem: pesquisa de 57 fontes que gerou `local-ai-core/conhecimento/`. Detalhes e fontes em `local-ai-core/conhecimento/PESQUISA-CONHECIMENTO.md`.

## Boas práticas confirmadas
- [Verificado na documentação] Dar ao agente um orçamento de esforço por tipo de pergunta (fato simples com 3 a 10 chamadas de ferramenta, comparação com mais, pesquisa ampla com plano salvo). Motivo: sem isso, agentes gastam demais em perguntas simples e não sabem parar. Evidência: Anthropic, sistema de pesquisa multiagente (2025).
- [Verificado na documentação] Buscar curto e amplo antes de estreitar, e dar heurísticas explícitas de qualidade de fonte. Motivo: consultas longas voltam vazias e agentes preferem fazendas de SEO. Evidência: mesma fonte.
- [Verificado na documentação] Permitir "não sei", extrair citações literais antes de responder e exigir um trecho por afirmação, retirando a que não tiver. Evidência: guia "Reduce hallucinations" da Anthropic; Chain-of-Verification (Findings ACL 2024).
- [Verificado na documentação] Ligar aprovação humana a ações com efeito (mudar algo, enviar dado, gastar) e, em pesquisa pura, subir o rigor da verificação em vez de pedir aprovação. Motivo: pedir "sim" para leitura atrasa sem proteger nada; o risco da pesquisa está no erro e no dado que sai.
- [Verificado na documentação] Base de conhecimento local em arquivos `.md` com fonte, confiança e data de revisão, reindexados pela ferramenta de memória. Motivo: informação envelhece e nota sem data vira fonte de erro.

## Armadilhas
- [Verificado na documentação] A busca web do OpenJarvis manda a consulta para provedores externos (You.com sem chave, DuckDuckGo como reserva, Tavily, Serply ou Firecrawl com chave) → o termo de busca é dado que sai da máquina → proibir dado pessoal nas consultas sem aprovação. Não verificado numa instalação real.
- [Verificado na documentação] Modelos inventam referências com DOI plausível (55% no GPT-3.5 e 18% no GPT-4 num estudo de 2023) → citar só o que foi lido e conferir DOI em `api.crossref.org/works/<DOI>`.
- [Verificado na documentação] Poucos textos maliciosos envenenam uma base de RAG (PoisonedRAG, USENIX Security 2025) → indexar só fontes escolhidas, guardar a origem de cada nota e tratar nota que dá ordens como suspeita.
- [Verificado] Com o segundo tema, o prompt montado (base mais dois temas) chegou a cerca de 5.500 tokens pela estimativa do script, contra cerca de 3.200 do core original só de Windows → permitir montar só os temas do uso do dia.

## Pesquisa
| Fonte (URL) | Classe | Acesso | Achado |
| --- | --- | --- | --- |
| https://www.anthropic.com/engineering/multi-agent-research-system | A | 2026-11-19 | Orçamento de esforço, amplo antes de específico, viés por SEO, passe de citação, avaliação com 20 perguntas |
| https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations | A | 2026-11-19 | Sete técnicas contra alucinação |
| https://hapgood.us/2019/06/19/sift-the-four-moves/ | A | 2026-11-19 | SIFT: pare, investigue, encontre cobertura melhor, rastreie |
| https://www.nature.com/articles/s41598-023-41032-5 | A | 2026-11-19 | Taxa de referências fabricadas por modelos |
| https://www.usenix.org/conference/usenixsecurity25/presentation/zou | A | 2026-11-19 | Envenenamento de base de RAG |
| https://www.anthropic.com/news/contextual-retrieval | A | 2026-11-19 | Contexto no trecho e BM25 mais vetores reduzem falhas de recuperação |
| https://open-jarvis.github.io/OpenJarvis/api-reference/openjarvis/tools/web_search/ | A | 2026-11-19 | Provedores da busca web (lido por resumo) |

## Lacunas
- Não há tag para "pesquisa local com citação e base de conhecimento pessoal". `web-research-apify` cobre coleta em escala com Apify; `llm-ai-agents` cobre RAG de produto. Sugestão: tag curada `pesquisa-com-fontes` com líder `llm-ai-agents` (rag-pipeline-reviewer) e fundamentos `web-research-apify` e `technical-writing-docs`.

## Promoção sugerida
- `llm-ai-agents` / seção `## Gotchas`: consulta de busca como dado que sai da máquina; referências inventadas e checagem de DOI.
- `web-research-apify` / playbook: orçamento de esforço por tipo de pergunta e "amplo antes de específico".
