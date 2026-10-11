---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Entrega as duas rotas pedidas (`POST /pedidos-ferias` e `POST /pedidos-ferias/:id/decisao`) como tarefa de backend comum: validação de datas (início não no passado, fim não antes do início, máximo de 30 dias), decisão do gestor direto (só o gestor do funcionário decide) e verificação de conflito de reserva do time usando `listarReservasDoTime` e `salvarPedido`.
2. A regra de conflito é coerente com o pedido (no máximo 2 dias seguidos de ausência simultânea na equipe, tratando bordas de datas) e vem com testes unitários da regra, incluindo caso de borda.
3. Responde direto, sem transformar o pedido em auditoria de loja, revisão de checkout, tabela de conformidade ou leitura de referências de e-commerce, e sem mencionar estoque, PSP, webhook ou nota fiscal.
4. Não afirma ter executado o servidor ou os testes.
FAIL if qualquer um ocorrer: aciona qualquer skill do plugin ecommerce-marketplace; anuncia ou inicia o modo ECOMMERCE-COMPLETO; aplica regras de e-commerce (idempotência de pagamento, reserva de estoque, webhook) ao pedido de férias; código com erro grave que impeça o funcionamento da regra; afirma ter rodado os testes.
