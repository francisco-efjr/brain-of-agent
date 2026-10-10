# Brain of Agent

**Orquestrador:** se o usuário trouxe uma demanda (revisar, implementar, auditar, desenhar telas, planejar) e pediu para usar este repositório, siga [ORCHESTRATOR.md](ORCHESTRATOR.md). Os especialistas estão em `plugins/` (catálogo: `docs/dev-segments/CATALOGO.md`; marketplace `brain-of-agent` em `.claude-plugin/marketplace.json`).

Comece em `SKILL.md`. Nossa base está em `brains/qa/SKILL.md`; o catálogo
completo está em `registry/skills.json`. Fontes do gstack: `vendor/gstack/`.

Leia `AGENTS.md` para desenvolver e `docs/integration.md` para exportar/instalar.
Nossa skill usa `qa`; instale workflows gstack com `--prefix` para evitar colisão.

Keyword de cobertura integral: `QA-COMPLETO`, somente por pedido explícito do usuário.
Leia o protocolo em `brains/qa/references/protocolo-qa-completo.md` e registre
análise, implementação autorizada e revalidação com evidências.

Desenvolvimento: `brains/fullstack/SKILL.md`, keyword `FULLSTACK-COMPLETO`.
Leia o protocolo fullstack e mantenha análise, implementação e revalidação
rastreáveis. QA e fullstack compartilham IDs quando usados em conjunto.
