# Validação inicial do brain fullstack

Data: 09/10/2026. Revisão por agentes de IA e checks locais. Não é revisão
humana, certificação de competência, comparação controlada de modelos ou
validação funcional do runtime gstack.

## Pesquisa e elaboração

Fontes primárias e síntese em `docs/research/agentes-desenvolvimento.md`.
O corpus cobre nove referências técnicas, protocolo, quatro templates e
16 casos sintéticos públicos de desenvolvimento, ainda não executados como
suite comportamental. O modo completo incorpora também o conhecimento QA.
Volume maior não demonstra qualidade superior; a hipótese precisa de
comparação equivalente baseline/skill/workflow.

## Revisão editorial e correções

Um agente que escreveu referências técnicas revisou integração, protocolo,
Apple e exportação produzidos pelo coordenador. Essa revisão não foi cega
a todo o corpus e não deve ser descrita como independente do conhecimento.

Dois achados foram corrigidos:

1. Router obrigatório na origem não estava exportado. Agora o entrypoint
   exportado é suficiente e o router original é condicional à sua presença.
2. Recursos compartilhados podiam ser omitidos silenciosamente. Agora
   `availability.json` registra disponibilidade e o CLI informa ausências.

O revisor confirmou as correções por inspeção. Testes executáveis verificam
exportação de múltiplos brains, contexto, colisões e referências ausentes.

## Forward-test de revisão estática

Tarefa inédita: revisar handler React/Node de salvamento de cliente com JWT,
consulta por ID, confirmação visual por HTTP200 e proposta de migração
SwiftUI para obter aparência Apple. Auditoria apenas, sem acesso a runtime.
O candidato recebeu tarefa e artefatos brutos, sem rubricas do dataset.

Resultados observados: achados de fronteira de tenant ausente no trecho,
tratamento de inexistência, ambiguidade criar/editar, validação e falso verde.
A revisão diferenciou risco estático de exploração operacional não demonstrada,
preservou o escopo e não tratou Apple como justificativa automática de migração.
Propôs 15 verificações com oráculos e revalidação. A leitura inicial teve
truncamento/recursos em elaboração e foi corretamente marcada parcial;
o relatório bruto `fullstack-review-response.md` registra a retomada e o
inventário final de leitura integral concluída em lotes. Produto real permanece
não executado, e portanto a validação operacional é parcial/NV.

## Forward-test de implementação em fixture

Tarefa inédita, modo seletivo: editar nome de cliente SQLite apenas para
tenant autenticado, normalizar entrada, preservar estado em erro e não
revelar diferença de contrato entre recurso inexistente e inacessível.

Artefatos em `brains/fullstack/evals/fixtures/tenant-edit/`:

- `customer_baseline.py`: implementação deliberadamente incorreta, para
  reprodução de autorização insuficiente; não é exemplo de produção.
- `before.txt` e `before.exit`: um teste de acesso cruzado falhou (exit1).
- `customer.py`: candidata corrigida, UPDATE parametrizado por ID e tenant.
- `test_customer.py`: nove verificações, incluindo limites, ausência de
  mutação indevida e persistência após reconexão.
- `after.txt` e `after.exit`: nove testes passaram (exit0).
- `handoff.md`, ambiente e hashes: decisões e limitações originais.

O coordenador repetiu o teste contra a baseline em cópia temporária e a
suite contra a candidata versionada. Isso confirma o comportamento da fixture,
não o ganho causal da skill em relação a modelo sem skill.

Limitações: SQLite sintético; função titular da transação; sem autenticação
HTTP, concorrência distribuída, UI ou ambiente de produção. Comprimento é
medido por pontos de código Python, não grafemas. Erro externo equivalente
não prova resistência a todo canal lateral. Não reutilizar como contrato
universal sem adaptação ao sistema alvo.

## Checks de integração

- Integridade: 3.133 arquivos upstream; catálogo com 64 entradas.
- Helpers QA: 34 testes.
- Ferramentas/integração: 25 testes.
- Fixture fullstack: 9 testes.
- Total: 68 testes determinísticos próprios passaram.
- Validação de frontmatter: router, QA e fullstack válidos.
- Estrutura: 12 casos QA e 16 fullstack válidos; não executados como benchmark.
- Smoke de exportação real para diretório temporário: gstack, fullstack,
  QA, contexto compartilhado e referências adjacentes presentes; nenhum setup.

## Trabalho restante

Executar benchmark controlado com modelos/hosts de uso, calibrar julgamentos
com revisão humana, manter holdout reservado e medir custo/latência da leitura
integral. Executar smoke operacional do gstack por host conforme
`docs/runtime-validation.md`. Não declarar portabilidade universal nem
superioridade antes dessas evidências.
