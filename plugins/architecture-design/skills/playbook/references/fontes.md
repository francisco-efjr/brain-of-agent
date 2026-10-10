# Fontes: bibliografia validada do segmento Arquitetura e design de sistemas

Consulta e validação: 2026-10-10 · Modelo-alvo: Claude 4.x/5.x · Rótulos: Verificado, Inferido, Suposição, Não verificável.
Classe A: oficial da Anthropic ou documentação/norma da tecnologia. Classe B: repositório com licença clara e uso, ou especialista reconhecido. Classe C: comunidade ou fornecedor, usado como sinal. "Destilar" = sem permissão de cópia literal; só redação própria.
Origem dos itens: `V-nn` vêm do VALIDATED da pesquisa (conferidos por um validador do mesmo vendor, independência parcial); `N-nn` foram abertos por um único verificador; N-01 (243x e jitter consistente por host para trabalho agendado), N-03 (status expirado e códigos 400/422/409) e N-05 (MADR 4.0.0 de 2024-09-17, licença MIT OR CC0-1.0) foram reconferidos pelo validador de qualidade em 2026-10-10, também do mesmo vendor.

## Sumário

1. Top 20 por valor para o plugin
2. Fontes de apoio e fontes novas
3. Conteúdo próprio do usuário e material de terceiros embutido
4. Metadados de repositórios (verificados em 2026-10-10)
5. Rejeitadas e rebaixadas
6. Lacunas (fonte primária não lida)
7. Política de uso e licenças
8. Gotchas

## 1. Top 20

| # | Fonte | URL | Classe | Licença de reuso | Consulta | Usada em |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Azure Well-Architected, Architecture decision record (V-12) | https://learn.microsoft.com/azure/well-architected/architect-role/architecture-decision-record | A | Microsoft (destilar) | 2026-10-10 | adr-e-governanca |
| 2 | Documenting Architecture Decisions, Nygard (V-13) | https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions | B | destilar | 2026-10-10 | adr-e-governanca |
| 2b | ArchitectureDecisionRecord, Fowler (V-13) | https://www.martinfowler.com/bliki/ArchitectureDecisionRecord.html | B | destilar | 2026-10-10 | adr-e-governanca |
| 3 | Claude Code best practices (V-03) | https://code.claude.com/docs/en/best-practices | A | Anthropic docs (destilar) | 2026-10-10 | claude-md-snippets, fluxo |
| 4 | Building effective agents (V-01) | https://www.anthropic.com/engineering/building-effective-agents | A | destilar | 2026-10-10 | fluxo-com-agentes |
| 5 | Effective context engineering for AI agents (V-02) | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | A | destilar | 2026-10-10 | fluxo-com-agentes |
| 6 | Create custom subagents (V-04) | https://code.claude.com/docs/en/sub-agents | A | destilar | 2026-10-10 | fluxo, ferramentas |
| 7 | Skills (V-05) | https://code.claude.com/docs/en/skills | A | destilar | 2026-10-10 | playbook |
| 8 | skill-creator (V-07) | https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md | A | Apache-2.0 (literal permitido com atribuição; não foi necessário) | 2026-10-10 | trigger-queries |
| 9 | How we built our multi-agent research system (V-08) | https://www.anthropic.com/engineering/multi-agent-research-system | A | destilar | 2026-10-10 | fluxo-com-agentes |
| 10a | Idempotent Consumer pattern (V-33) | https://learn.microsoft.com/azure/architecture/patterns/idempotent-consumer | A | destilar | 2026-10-10 | resiliencia |
| 10b | Transactional Outbox, Cosmos DB (V-34) | https://learn.microsoft.com/azure/architecture/databases/guide/transactional-out-box-cosmos | A | destilar | 2026-10-10 | resiliencia |
| 10c | Saga pattern (V-35) | https://learn.microsoft.com/azure/architecture/patterns/saga | A | destilar | 2026-10-10 | resiliencia |
| 11a | CQRS pattern (V-36) | https://learn.microsoft.com/azure/architecture/patterns/cqrs | A | destilar | 2026-10-10 | resiliencia |
| 11b | Event Sourcing pattern (V-37) | https://learn.microsoft.com/azure/architecture/patterns/event-sourcing | A | destilar | 2026-10-10 | resiliencia |
| 12a | Circuit Breaker pattern (V-30) | https://learn.microsoft.com/azure/architecture/patterns/circuit-breaker | A | destilar | 2026-10-10 | resiliencia |
| 12b | Retry pattern (V-31) | https://learn.microsoft.com/azure/architecture/patterns/retry | B | destilar | 2026-10-10 | resiliencia |
| 12c | Bulkhead pattern (V-32) | https://learn.microsoft.com/azure/architecture/patterns/bulkhead | A | destilar | 2026-10-10 | resiliencia |
| 13 | Timeouts, retries, and backoff with jitter, AWS Builders' Library (N-01) | https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter (redireciona de aws.amazon.com/builders-library/) | A (reconferida em 2026-10-10 pelo validador de qualidade) | destilar | 2026-10-10 | resiliencia |
| 14 | Cache-Aside pattern (V-38) | https://learn.microsoft.com/azure/architecture/patterns/cache-aside | A | destilar | 2026-10-10 | api-cache-escala |
| 15a | Web API design, Azure Architecture Center (V-39) | https://learn.microsoft.com/azure/architecture/best-practices/api-design | B | destilar (leitura parcial) | 2026-10-10 | api-cache-escala |
| 15b | RFC 9457 Problem Details for HTTP APIs (N-02) | https://www.rfc-editor.org/rfc/rfc9457.html | A | IETF (destilar) | 2026-10-10 | api-cache-escala |
| 16a | BoundedContext, Fowler (V-26) | https://martinfowler.com/bliki/BoundedContext.html | B | destilar | 2026-10-10 | fronteiras |
| 16b | DDD_Aggregate, Fowler (V-26) | https://martinfowler.com/bliki/DDD_Aggregate.html | B | destilar | 2026-10-10 | fronteiras |
| 16c | Hexagonal architecture, Cockburn (V-25) | https://alistair.cockburn.us/hexagonal-architecture/ | B | destilar | 2026-10-10 | fronteiras |
| 17a | MonolithFirst, Fowler (V-27) | https://martinfowler.com/bliki/MonolithFirst.html | B | destilar | 2026-10-10 | fronteiras |
| 17b | Strangler Fig Application, Fowler (V-29) | https://www.martinfowler.com/bliki/StranglerFigApplication.html | B | destilar | 2026-10-10 | fronteiras |
| 17c | architecture-paradigm-modular-monolith, athola/claude-night-market (V-28) | https://raw.githubusercontent.com/athola/claude-night-market/master/plugins/archetypes/skills/architecture-paradigm-modular-monolith/SKILL.md | B (5/10) | MIT | 2026-10-10 | fronteiras |
| 18a | C4 model, Simon Brown (V-21) | https://c4model.com/ | B | destilar | 2026-10-10 | c4-e-diagramas |
| 18b | diagram skill, garrytan/gstack (V-23) | https://raw.githubusercontent.com/garrytan/gstack/main/diagram/SKILL.md | B | MIT (só regras destiladas) | 2026-10-10 | c4-e-diagramas |
| 19a | feature-dev command (V-09) | https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/feature-dev/commands/feature-dev.md | A | Todos os direitos reservados: só destilar | 2026-10-10 | fluxo-com-agentes |
| 19b | code-architect agent (V-10) | https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/feature-dev/agents/code-architect.md | B | Todos os direitos reservados: só destilar | 2026-10-10 | checklist, agentes |
| 19c | code-modernization (V-11) | https://github.com/anthropics/claude-plugins-official/tree/main/plugins/code-modernization | A | Apache-2.0 (só método destilado) | 2026-10-10 | fluxo-com-agentes |
| 20 | system-design-skills, proyecto26 (V-41) | https://github.com/proyecto26/system-design-skills | B (5/10) | MIT | 2026-10-10 | api-cache-escala |

## 2. Fontes de apoio e novas

| ID | Fonte | URL | Classe | Licença | Consulta | Uso |
| --- | --- | --- | --- | --- | --- | --- |
| V-06 | Output styles | https://code.claude.com/docs/en/output-styles | B | destilar | 2026-10-10 | estilo `arquiteto` |
| V-14 | ADR Generator, github/awesome-copilot | https://raw.githubusercontent.com/github/awesome-copilot/main/agents/adr-generator.agent.md | B | MIT | 2026-10-10 | entradas do ADR |
| V-15 | adlc `adr`, wuersch/adlc | https://raw.githubusercontent.com/wuersch/adlc/main/plugins/adlc/skills/adr/SKILL.md | B (5/10) | MIT | 2026-10-10 | gatekeeper |
| V-16 | architecture-decision-records, affaan-m/everything-claude-code | https://raw.githubusercontent.com/affaan-m/everything-claude-code/main/skills/architecture-decision-records/SKILL.md | B | MIT | 2026-10-10 | consentimento (não rodar o instalador) |
| V-17 | implementation-plan, github/awesome-copilot | https://raw.githubusercontent.com/github/awesome-copilot/main/agents/implementation-plan.agent.md | B | MIT | 2026-10-10 | template de plano |
| V-18 | spec-driven-workflow, github/awesome-copilot | https://raw.githubusercontent.com/github/awesome-copilot/main/instructions/spec-driven-workflow-v1.instructions.md | B | MIT | 2026-10-10 | EARS, gate |
| V-19 | plan-eng-review, garrytan/gstack | https://raw.githubusercontent.com/garrytan/gstack/main/plan-eng-review/SKILL.md | B | MIT | 2026-10-10 | processo de design-review (não importar o arquivo) |
| V-20 | How I use Claude Code, Boris Tane | https://boristane.com/blog/how-i-use-claude-code/ | B | sem licença visível (destilar) | 2026-10-10 | pesquisar, planejar, anotar |
| V-22 | c4-context, wshobson/agents | https://raw.githubusercontent.com/wshobson/agents/main/plugins/c4-architecture/agents/c4-context.md | B | MIT | 2026-10-10 | níveis C4 |
| V-24 | FastAPI production architecture rule, PatrickJS/awesome-cursorrules | https://raw.githubusercontent.com/PatrickJS/awesome-cursorrules/main/rules/fastapi-production-architecture-cursorrules-prompt-file.mdc | B | CC0-1.0 | 2026-10-10 | tabela de imports |
| V-40 | api-designer, Jeffallan/claude-skills | https://raw.githubusercontent.com/Jeffallan/claude-skills/main/skills/api-designer/SKILL.md | B | MIT | 2026-10-10 | checklist de API |
| V-42 | backend-architect, wshobson/agents | https://raw.githubusercontent.com/wshobson/agents/main/plugins/backend-development/agents/backend-architect.md | B | MIT | 2026-10-10 | 10 passos |
| V-43 | Claude Is Not Your Architect, Charlie Holland | https://www.hollandtech.net/claude-is-not-your-architect/ | B (5/10) | destilar | 2026-10-10 | arquiteto cético |
| V-44 | Cinco padrões de CLAUDE.md (espelho de r/ClaudeAI) | https://reddit.sentinel-team.org/posts/1v13yrk/snapshots/2026-07-20T20%3A24%3A21.6759Z | B (5/10) | destilar | 2026-10-10 | snippets |
| V-45 | Architecture lesson, developertoolkit.ai | https://developertoolkit.ai/en/claude-code/lessons/architecture/ | C | destilar | 2026-10-10 | checklist de revisão |
| N-01 | AWS Builders' Library, jitter | ver Top 20 item 13 | A | destilar | 2026-10-10 | publicada 2026-06-12, modificada 2026-06-15; 5 camadas x 3 tentativas = 243x |
| N-02 | RFC 9457 | https://www.rfc-editor.org/rfc/rfc9457.html | A | IETF (destilar) | 2026-10-10 | julho de 2023; obsoleta a RFC 7807 |
| N-03 | draft-ietf-httpapi-idempotency-key-header-07 | https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/ | B | IETF (destilar) | 2026-10-10 | rascunho expirado (2025-10-15); sem RFC. Reconferido pelo validador de qualidade em 2026-10-10, inclusive o texto da revisão 07: 400 (chave ausente), 422 (reuso com corpo diferente), 409 (em processamento) |
| N-04 | Parallel Change, Danilo Sato | https://martinfowler.com/bliki/ParallelChange.html | B | destilar | 2026-10-10 | expand/contract (13/05/2014) |
| N-05 | MADR 4.0.0 | https://adr.github.io/madr/ | B | MIT e CC0-1.0 (escolha) | 2026-10-10 | variante de ADR (2024-09-17) |
| N-06 | OWASP Threat Modeling Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html | A | CC BY-SA 4.0 (destilar; ShareAlike impede mistura literal) | 2026-10-10 | quatro perguntas, STRIDE |
| N-07 | Azure Well-Architected, pilares | https://learn.microsoft.com/azure/well-architected/pillars | A | destilar | 2026-10-10 | cinco pilares (ms.date 2025-01-22) |
| N-08 | SEI/CMU, ATAM collection | https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/ | A | destilar | 2026-10-10 | vocabulário leve (página de 2018-02-14) |

## 3. Conteúdo próprio e material de terceiros embutido

| Material | Origem | Licença | Onde entra |
| --- | --- | --- | --- |
| `arquitetura-e-dominio.md` (checklist, exemplo antes/depois, ADR mínima) | brain-of-agent, Francisco Edson, commit 0d025fb | MIT (do próprio usuário) | `checklist-completo.md`, `padroes-e-antipadroes.md`, `resiliencia-e-consistencia.md`, templates |
| `assets/templates/adr.md` | brain-of-agent | MIT | `assets/templates/adr.md` (base literal curta, atribuída, fundida com campos de V-13) |
| `handoff-checkpoint.md` | brain-of-agent | MIT | `assets/templates/handoff.md` (adaptado) |
| Processo de `plan-eng-review` e regras de `diagram` | gstack, Garry Tan, versão 1.91.27 (THIRD_PARTY_NOTICES do brain-of-agent) | MIT | Só processo reescrito, com atribuição; nenhum arquivo importado |
| Método de extração de regras | code-modernization, Anthropic | Apache-2.0 | Destilado em `rule-card.md`; sem código |

Microsoft, AWS, Fowler, Cockburn, C4, IETF e OWASP: nenhum texto literal foi copiado.

## 4. Metadados de repositórios (verificados em 2026-10-10, páginas HTML e feeds Atom; a API do GitHub estava com limite de taxa)

| Repositório | Estrelas | Licença | Último commit | Observação |
| --- | --- | --- | --- | --- |
| anthropics/skills | 180,2 mil | Apache-2.0 em `skills/skill-creator/LICENSE.txt` | 2026-10-09 | nem toda skill do repositório é permissiva |
| anthropics/claude-code | 149,9 mil | LICENSE.md: todos os direitos reservados | 2026-10-09 | feature-dev e code-architect: só destilar |
| anthropics/claude-plugins-official | 37,6 mil | Apache-2.0 | 2026-10-09 | |
| github/awesome-copilot | 39,9 mil | MIT | 2026-10-09 | |
| garrytan/gstack | 135,7 mil | MIT | 2026-10-09 | |
| PatrickJS/awesome-cursorrules | 40,9 mil | CC0-1.0 | 2026-05-30 | mais de 4 meses sem commit |
| wshobson/agents | 40,3 mil | MIT | 2026-10-04 | |
| Jeffallan/claude-skills | 11,8 mil | MIT | 2026-10-03 | |
| athola/claude-night-market | 341 | MIT | 2026-10-02 | |
| proyecto26/system-design-skills | 85 | MIT | 2026-06-02 | |
| wuersch/adlc | 1 | MIT | 2026-08-01 | alpha declarado |
| affaan-m/everything-claude-code | 276 mil | MIT | 2026-10-10 | popularidade não prova qualidade |

Números de estrelas mudam; use como contexto, não como critério (AP-20).

## 5. Rejeitadas e rebaixadas (não usar como fonte)

| Item | Decisão | Motivo |
| --- | --- | --- |
| VoltAgent architect-reviewer | Classe C | Checklist vazio, dá `Write, Edit, Bash` a revisor; só a ideia dos oito eixos foi reaproveitada |
| mblode agents-md | Classe C | Só README lido; fora do núcleo |
| josiahsiegel c4-model | Rejeitado | Caminho 404; não verificável |
| Composer MCP, Structurizr AI/MCP | Classe C | Fornecedor; a documentação não sustenta as alegações; não ativar MCP de terceiros |
| understandingdata plan-mode | Rejeitado | Métricas sem método |
| besthub, CLAUDE.md em camadas | Rejeitado | Atribuição não verificável; princípios já estão na doc oficial |
| tw93 (seis camadas) | Classe C | Relato pessoal; a doc oficial cobre |
| Encore (monólito vs microsserviços) | Classe C | Fornecedor; sem limiares numéricos |
| Issue "Architect Mode" (claude-code #60995) | Classe C | Fechada como "not planned"; sinal de lacuna |
| Agregados/catálogos de skills | Rejeitado como prova | Estrelas e contagens de agregador são Não verificáveis até conferidas no repositório |

## 6. Lacunas (fonte primária não lida; conteúdo correspondente sai como Inferido ou Suposição)

1. Clean Architecture/onion (Martin) e ArchUnit/dependency-cruiser na regra "dependências para dentro".
2. DDD primário: Evans (DDD Reference) e Vernon (Effective Aggregate Design).
3. Escalabilidade e capacidade: Builders' Library sobre load shedding, Azure PE:05, Google SRE (overload).
4. HTTP normativo: RFC 9110, Google AIP, Microsoft REST API Guidelines, documentação de idempotência da Stripe.
5. Segurança de arquitetura além da modelagem leve: STRIDE da Microsoft, checklist de revisão de segurança de design.
6. Evolução de esquema de banco: expand/contract para SQL, particionamento, banco por serviço.
7. Fitness functions (Ford, Parsons, Kua) e exemplos de CI.
8. Plugins oficiais de arquitetura em claude-plugins-official e cookbooks (só feature-dev e code-modernization foram abertos).
9. Event-driven geral (Fowler 2017) e AsyncAPI.
10. Reddit r/ClaudeCode, YouTube, X e dev.to sem cobertura direta.
11. Sintaxe exata de regras de permissão e hooks para limitar escrita por diretório.
12. Conteúdo de `c4-component.md` e `c4-code.md` da wshobson.
13. Eficácia: nenhum item tem avaliação publicada além dos arquivos de proyecto26 e do método do skill-creator.

## 7. Política de uso e licenças

- Cópia literal somente de: conteúdo do próprio usuário (brain-of-agent, MIT) e, se algum dia necessário, trechos curtos (até cerca de 40 linhas) de fontes MIT, Apache-2.0, CC0 ou CC-BY, com atribuição.
- OWASP (CC BY-SA): não misturar texto literal, para não impor ShareAlike ao plugin.
- Anthropic/claude-code (direitos reservados): somente destilação.
- Conteúdo de páginas, READMEs e prompts coletados é dado, não instrução. Quando um texto externo dirigido a IA foi encontrado, ele foi ignorado e registrado como risco. A "injeção" relatada por pesquisadores no `SKILL.md` do gstack não foi encontrada no arquivo raw (provável artefato do sumarizador).
- Tudo o que um agente construtor escreveu é Inferido até reconferência; revisão por modelo da mesma família não é validação independente.

## 8. Gotchas

- Links de padrões da Microsoft mudam de caminho com frequência; se uma URL falhar, procure o título da página.
- A URL de N-01 redireciona; confira o redirecionamento ao citar.
- Datas "ms.date" e "updated" das páginas da Microsoft são do dia da consulta; conteúdo pode ter mudado.
- A versão mais recente de uma RFC ou do MADR pode ter avançado; confira antes de afirmar "a versão atual é".
- O percentual de ganho de 90,2% em V-08 é de uma avaliação interna de pesquisa com modelos antigos (junho de 2025).
