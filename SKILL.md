---
name: brain-of-agent
description: Escolher conhecimento por segmento e workflows do Brain of Agent para pedidos de QA, planejamento, revisão, investigação e entrega de software. Use quando o usuário pedir para usar este projeto ou combinar sua base QA com gstack.
license: MIT
---

# Brain of Agent

Carregue apenas conhecimento e workflows pertinentes ao pedido. Para
estratégia, casos, regras de negócio, bugs, automação e avaliação de IA,
leia [a skill QA](brains/qa/SKILL.md), que direciona para as referências.

| Intenção | Fonte do workflow |
| --- | --- |
| Explorar uma ideia | `vendor/gstack/office-hours/SKILL.md` |
| Revisar produto/escopo | `vendor/gstack/plan-ceo-review/SKILL.md` |
| Revisar arquitetura/fluxos/testes | `vendor/gstack/plan-eng-review/SKILL.md` |
| Revisar código | `vendor/gstack/review/SKILL.md` |
| Investigar falha | `vendor/gstack/investigate/SKILL.md` |
| Testar, corrigir e reverificar | `vendor/gstack/qa/SKILL.md` |
| Testar/relatar sem corrigir produto | `vendor/gstack/qa-only/SKILL.md` |
| Preparar entrega/PR | `vendor/gstack/ship/SKILL.md` |
| Documentar entrega | `vendor/gstack/document-release/SKILL.md` |
| Outros workflows | `registry/skills.json` |

Nossa skill mantém o nome `qa`. Workflows instalados com prefixo usam
`gstack-*`, por exemplo `gstack-qa`.

Combine a base QA para definir risco, dados e oráculos com o workflow adequado
para execução. Um pedido simples pode usar somente QA. Separe observado,
inferido, suposição e não executado na entrega.

O gstack foi importado como fonte. Passos que pressupõem runtime, ferramentas
ou host precisam do setup compatível; consulte [a integração](docs/integration.md).
Não invente ferramentas disponíveis nem evidência. Selecionar `ship` não
autoriza por si só merge, deploy ou ações fora do pedido do usuário.
