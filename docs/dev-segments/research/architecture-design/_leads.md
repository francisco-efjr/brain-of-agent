# architecture-design — pistas do atlas global

Data: 2026-10-09 · Indexador do atlas (Claude Sonnet 5.5) · Origem: `docs/research/_global/*.validated.md` (IDs: AO, EC = ecosystem item nn, CT, PC, CP, BR).
Pista é ponto de partida: reabrir a URL antes de citar. "Dest." = destilar. Princípios comuns de prompt: `docs/foundation/prompt-principles.md`.

## 1. Pistas aprovadas aplicáveis

| Pista | URL | Classe | O que aproveitar |
| --- | --- | --- | --- |
| Building effective agents (AO-15) | https://www.anthropic.com/engineering/building-effective-agents | A | Workflows × agentes, 5 padrões, ACI, poka-yoke; começar simples. Parte datada (2024-12-19). |
| Effective context engineering (AO-16) | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | A | Menor conjunto de tokens de alto sinal; vale para desenhar arquitetura de agentes. |
| ADR generator (CT-21) | https://github.com/github/awesome-copilot | B | Pede dados e para se faltar; `adr-NNNN-slug.md`; Status/Context/Decision/Consequences/Alternatives incluindo "do nothing". MIT. |
| gstack `plan-eng-review` (EC-11, BR-21) | https://github.com/garrytan/gstack | B | Scope Challenge, seções (arquitetura, fluxo de dados, bordas, testes, performance), decisões com recomendação e trade-offs, gate; só revisa. |
| code-modernization (AO-30) | https://github.com/anthropics/claude-plugins-official | A | Regras de negócio Given/When/Then com `file:line`, aprovação antes de construir. Apache-2.0. |
| feature-dev (AO-29) | https://github.com/anthropics/claude-code/tree/main/plugins | A | Parada obrigatória na escolha de arquitetura. Destilar. |
| FastAPI production architecture (CT-07) | https://github.com/PatrickJS/awesome-cursorrules | B | Camadas Router → Service → Repository → ORM com allow-list de imports; handler fino; anti-corruption layer; bulkhead por provedor; "single writer". CC0, limites de LOC são opinião. |
| spec-kit, OpenSpec (EC-02, EC-18) | https://github.com/github/spec-kit | A/B | Spec sem detalhes de implementação; deltas de spec por mudança. |
| Boris Tane e Dex Horthy (CP-03, CP-06) | https://boristane.com/blog/how-i-use-claude-code/ | B | `research.md` → `plan.md` com trade-offs; `handoff.md` com decisões e porquê. |
| VoltAgent subagents (EC-09) | https://github.com/VoltAgent/awesome-claude-code-subagents | B | Esqueleto de agentes por categoria; prompts longos e sem evals. |
| wshobson/agents (EC-10) | https://github.com/wshobson/agents | B | Plugin `c4-architecture` (nome citado pelo atlas; conteúdo não lido). |
| BMAD, ECC (EC-15, EC-13) | https://github.com/bmad-code-org/BMAD-METHOD | B | Papel de arquiteto como skill; ECC "otimizar a janela, persistir o resto". BMAD NOASSERTION; ECC executa instalador: não rodar. |
| awesome-copilot instructions e agents (CT-14) | https://github.com/github/awesome-copilot | A | Agents ADR/debug/plan; instructions spec-driven. Viés Microsoft. |
| Output styles (AO-13) | https://code.claude.com/docs/en/output-styles | A | Estilo "arquiteto" com `keep-coding-instructions: true`; estilo é instrução, não garantia. |
| Ask HN e Breunig (CP-21, CP-23) | https://news.ycombinator.com/item?id=46691243 | B | Fronteiras fortes de módulo ajudam o agente; diffar spec vs construído. |

## 2. Repositórios e arquivos a abrir
- `github/awesome-copilot`: `agents/adr-generator.agent.md`, `agents/implementation-plan.agent.md`, `instructions/spec-driven-workflow-v1.instructions.md`.
- `PatrickJS/awesome-cursorrules`: `rules/fastapi-production-architecture-cursorrules-prompt-file.mdc` (trechos Verificados no raw).
- `garrytan/gstack`: `plan-eng-review/SKILL.md` e `diagram/SKILL.md` (também no snapshot do brain).
- `wshobson/agents`: pasta `plugins/c4-architecture` (abrir e verificar).
- `anthropics/claude-code` `plugins/feature-dev`; `anthropics/claude-plugins-official` `plugins/code-modernization`.
- Docs de plataformas/normas do segmento (C4, DDD, 12-factor, AWS Well-Architected) não estão no atlas: lente authoritative do segmento deve buscar.

## 3. Materiais oficiais Anthropic pertinentes
AO-15, AO-16, AO-18 (https://www.anthropic.com/engineering/multi-agent-research-system), AO-29, AO-30, AO-13. Para decisão de onde colocar cada coisa: AO-12 (https://code.claude.com/docs/en/features-overview).

## 4. Padrões da comunidade
- Plano em markdown com arquivos, snippets e trade-offs, com ciclo de anotação humana (CP-03).
- Direção errada = `git revert` e re-escopo, sem empilhar correção (CP-03, CP-13).
- Gate de aprovação após escolher arquitetura (EC-01, AO-29).
- Declarar stack, ORM e auth antes de gerar; modelo escolhe "Custom/DIY" em 12/20 categorias (CP-24, Verificado).
- Layers com allow-list de imports e verificação por grep (CT-07).

## 5. O que o brain-of-agent já oferece
- `brains/fullstack/references/arquitetura-e-dominio.md` e `brains/fullstack/assets/templates/adr.md` (próprios, MIT).
- `vendor/gstack/plan-eng-review/SKILL.md` e `vendor/gstack/diagram/SKILL.md` (gstack, MIT; destilar com atribuição).
- BR-21: checklist de revisão de arquitetura (limites, estados, falhas parciais e idempotência, concorrência, migração e rollback, authz, observabilidade, testes por camada, alternativa mais simples, ADR); entregar só mermaid.
- BR-02: processo essencial (ler, invariantes, opções só se há decisão material com ADR, fatia vertical, revisão adversarial, revalidar, entregar com limitações).
- BR-13: router intenção → fonte; BR-03: modo `ARQUITETURA-COMPLETO`.

## 6. Lacunas e cuidados
- Sem fonte A sobre DDD, CQRS/event sourcing, resiliência (circuit breaker), consistência e escalabilidade: pesquisa própria.
- `plan-eng-review` do gstack tem preâmbulo longo e acoplado a Bun/telemetria: adotar o processo, não o bloco.
- Exemplos FastAPI/Python são de um stack; generalizar com cuidado.
- Contagens de agentes de wshobson e VoltAgent não verificadas.
