# Requisitos EARS e rastreio para testes

Sumário: 1. Padrões EARS · 2. Exemplos arquiteturais · 3. O que a spec não deve conter · 4. Rastreio requisito -> teste · 5. Estrutura de fases · 6. Gotchas

Validado em 2026-10-10. O formato `WHEN ... THE SYSTEM SHALL ...` e a sequência requisitos, design e tarefas vêm de V-18 (awesome-copilot, MIT; Verificado em VALIDATED). Os cinco padrões completos de EARS (Easy Approach to Requirements Syntax, Alistair Mavin e colegas) são conhecimento estável do domínio e não foram reabertos nesta execução (Inferido). Os exemplos são ilustrativos.

## 1. Padrões EARS

| Padrão | Forma | Uso |
| --- | --- | --- |
| Ubíquo | `O <sistema> deve <resposta>.` | Propriedade sempre verdadeira |
| Orientado a evento | `QUANDO <gatilho>, O <sistema> deve <resposta>.` | Reação a evento (WHEN) |
| Orientado a estado | `ENQUANTO <estado>, O <sistema> deve <resposta>.` | Comportamento dependente de estado (WHILE) |
| Comportamento indesejado | `SE <condição indesejada>, ENTÃO O <sistema> deve <resposta>.` | Falhas e entradas inválidas (IF/THEN) |
| Opcional | `ONDE <recurso presente>, O <sistema> deve <resposta>.` | Variantes por configuração (WHERE) |

Em inglês: `WHEN <trigger> THE SYSTEM SHALL <response>`. Use o idioma do projeto e mantenha a mesma palavra para "deve" em todos os requisitos. Um requisito, uma resposta verificável.

## 2. Exemplos arquiteturais

| ID | Requisito | Tipo |
| --- | --- | --- |
| REQ-001 | QUANDO um pedido é confirmado, O serviço de pedidos deve gravar o estado do pedido e o evento `PedidoConfirmado` na mesma transação. | Evento |
| REQ-002 | QUANDO o consumidor recebe duas vezes a mesma mensagem, ELE deve produzir o efeito de negócio uma única vez. | Evento |
| REQ-003 | SE o provedor de pagamento não responder em 5 s (Suposição), ENTÃO O serviço deve tratar o resultado como desconhecido e consultar o estado antes de repetir a cobrança. | Indesejado |
| REQ-004 | ENQUANTO o disjuntor do provedor estiver aberto, O serviço deve responder 503 com `Retry-After` sem chamar o provedor. | Estado |
| SEC-001 | O serviço deve verificar, em todo acesso a pedido, que o usuário autenticado é dono do pedido ou tem papel autorizado. | Ubíquo |
| CON-001 | O módulo `billing` não deve importar pacotes de `orders/internal`. | Restrição (verificada por teste de arquitetura) |

Prefixos: `REQ` funcional, `SEC` segurança, `CON` restrição de arquitetura (V-17). Números como 5 s são Suposição até medição.

## 3. O que a spec não deve conter

- Detalhe de implementação que o design decide (nome de classe, biblioteca), a menos que seja restrição real (`CON`).
- Palavras vagas: "rápido", "robusto", "escalável", "adequado" sem número ou critério.
- Dois comportamentos no mesmo requisito ("grava e notifica").
- Requisitos sem verificação possível: se não dá para escrever o teste, reescreva.
- Decisões humanas escondidas: marque `[NEEDS CLARIFICATION: ...]` e liste na seção de decisões pendentes (V-18 não define o que a spec não deve conter; esta lista é do plugin, Inferido).

## 4. Rastreio requisito -> teste

Tabela no `plan.md`:

| Requisito | Teste | Tipo | Fase | Comando de verificação |
| --- | --- | --- | --- | --- |
| REQ-001 | `OrderConfirmTransactionTest` simula falha após gravar estado e verifica que evento e estado persistem juntos ou nenhum | integração | 1 | `<comando de teste do projeto>` |
| REQ-002 | Teste entrega a mesma mensagem 2x e conta o efeito | integração | 2 | idem |
| CON-001 | Teste de arquitetura ou `grep` falha com import proibido | arquitetura | 1 | `<comando do verificador>` |

Regra: todo REQ tem pelo menos um teste; todo teste cita o REQ. O comando entre colchetes angulares é preenchido com o comando real do projeto (descoberto no repositório ou perguntado); não invente comandos.

## 5. Estrutura de fases

Cada fase do plano:

```markdown
### Fase 2: consumidor idempotente (fatia vertical)
Objetivo: mensagem duplicada não duplica o efeito.
Arquivos: src/orders/consumer.ts (alterar), src/orders/inbox.sql (criar), test/orders/consumer.test.ts (criar)
Requisitos: REQ-002
Critério de conclusão: `<comando>` passa e o teste de duplicata falha sem a alteração (vermelho confirmado antes do verde).
Rollback: reverter o commit; a tabela `inbox` pode permanecer (não afeta o fluxo antigo).
- [ ] Marcador criado  - [ ] Teste de duplicata  - [ ] Evidência colada
```

"Vermelho confirmado": o teste novo deve falhar pelo motivo certo antes da implementação (PAD-07), senão não prova nada.

## 6. Gotchas

- EARS não substitui modelo de domínio: requisitos soltos sem estados e invariantes geram buracos; escreva as transições de estado no plano.
- Requisitos demais: 20 a 40 por mudança já é muito; priorize por risco.
- Limiares numéricos de confiança (85% e 66%) são Suposição (V-18); registre a confiança como alta, média ou baixa.
- Copiar requisitos de outra feature "por padrão" importa restrições que não se aplicam; revise cada um.
