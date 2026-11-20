---
data: 2026-11-19
tags: [llm-ai-agents, contexto-agente, seguranca-hardening]
plugins: [llm-ai-agents, security-appsec]
agentes: [llm-ai-agents:agent-architect, llm-ai-agents:rag-pipeline-reviewer, llm-ai-agents:agent-security-reviewer]
contexto: "Memória de longo prazo em arquivos markdown para uma IA local (OpenJarvis + Ollama), com base no desenho do akitaonrails/ai-memory"
tipo_de_sessao: pesquisa
modelo: claude-opus-5-5
---
# Memória de longo prazo para IA local: markdown, níveis, origem e bastão

Origem: pesquisa de 41 fontes que gerou `local-ai-core/memoria/`. Detalhes em `local-ai-core/memoria/PESQUISA-MEMORIA.md`.

## Boas práticas confirmadas
- [Verificado na documentação] Markdown como fonte da verdade e banco como índice derivado e reconstruível. Motivo: o dono lê, corrige e versiona a memória com qualquer editor. Evidência: ai-memory (README, ARCHITECTURE), Letta (arquivos simples com 74,0% no LoCoMo, número da própria Letta), Open Knowledge Format do Google Cloud.
- [Verificado na documentação] Níveis com durações diferentes: perfil, decisões e procedimentos não envelhecem; episódios envelhecem e são compactados em fatos duráveis. Evidência: ai-memory (design de envelhecimento), CoALA, MemoryBank.
- [Verificado na documentação] Nada se apaga por conta própria: versão nova substitui a antiga, que fica no git ou em `arquivo\`. Evidência: ai-memory.
- [Verificado na documentação] Origem pesa: o que o usuário disse vale mais que o que o modelo concluiu, que vale mais que resultado de ferramenta; texto de ferramenta nunca vira regra. Evidência: ai-memory (proveniência), MINJA (98,2% de injeção de memória), estudo de 2026 que recomenda defender o caminho de escrita.
- [Verificado na documentação] Passagem de bastão estruturada ao parar: onde parou, o que falhou, o que está aberto. Evidência: ai-memory; I-PASS reduziu erros médicos em 23%.
- [Verificado na documentação] Regra fixa é escassa: só vai para o prompt o que, esquecido, causaria erro em muitas tarefas. Evidência: ai-memory (promoção de regras).

## Armadilhas
- [Verificado na documentação] Defesas contra injeção de prompt não cobrem envenenamento de memória → defender na escrita (origem, quarentena, nada de origem ferramenta virando regra).
- [Verificado] O ai-memory cita um estudo (arXiv 2611.09721) que a busca não encontrou → citar os estudos encontrados (MINJA, MemoryGraft, arXiv 2606.04329) em vez de repetir a citação.
- [Verificado na documentação] A documentação do OpenJarvis não deixa claro se o agente grava memória sozinho → memória em arquivos e `jarvis memory index`.

## Pesquisa
| Fonte (URL) | Classe | Acesso | Achado |
| --- | --- | --- | --- |
| https://github.com/akitaonrails/ai-memory | A | 2026-11-19 | Princípios de desenho da memória |
| https://arxiv.org/abs/2410.10813 | A | 2026-11-19 | LongMemEval: atualização e abstenção são pontos fracos |
| https://arxiv.org/abs/2503.03704 | A | 2026-11-19 | MINJA: injeção de memória só conversando |
| https://arxiv.org/abs/2606.04329 | A | 2026-11-19 | Defesa no caminho de escrita |
| https://psnet.ahrq.gov/issue/changes-medical-errors-after-implementation-handoff-program | A | 2026-11-19 | Passagem de bastão estruturada |

## Lacunas
- Não há tag para "IA local / OpenJarvis". Sugestão: tag curada `ia-local` apontando para `local-ai-core/`, com líder `llm-ai-agents`.

## Promoção sugerida
- `llm-ai-agents` / `## Gotchas`: envenenamento de memória passa pelas defesas de injeção; origem por nota.
