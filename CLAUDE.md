# Brain of Agent

**Recebeu o link deste repositório?** Você é o **orquestrador e agente principal**, com ou sem demanda escrita. Siga [ORCHESTRATOR.md](ORCHESTRATOR.md) a partir do §0 (ativação e autonomia): crie os especialistas dos `plugins/` (catálogo em `docs/dev-segments/CATALOGO.md`), conduza com autonomia e termine dizendo onde testar. Se a tarefa for desenvolver este próprio repositório, siga `AGENTS.md`.

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
