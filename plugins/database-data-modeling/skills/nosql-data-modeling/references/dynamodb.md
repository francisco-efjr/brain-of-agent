# DynamoDB: do padrão de acesso às chaves

Conferido em 2026-10-10 contra V-26 (AWS DynamoDB Developer Guide, "NoSQL design best practices", classe A, página lida inteira). A página **não** trata de capacidade/throughput nem de single-table design em detalhe (L-07): onde este arquivo vai além, está rotulado Inferido e deve ser conferido na documentação atual. Nenhum número de capacidade é afirmado aqui. Texto é redação própria; os exemplos de chave são didáticos, não fonte.

Sumário
1. Princípios (V-26)
2. Processo: perguntas antes das tabelas
3. Exemplo: pedidos de e-commerce
4. GSIs e alta cardinalidade
5. Armadilhas
6. Lacunas e o que conferir

## 1. Princípios (V-26)

1. **Não desenhe o schema antes de saber as perguntas** que o sistema vai responder.
2. Levante tamanho, forma e velocidade dos dados.
3. Use **o menor número possível de tabelas**; exceções: séries temporais de alto volume e padrões de acesso muito diferentes.
4. Mantenha dados relacionados **juntos** (mesma partição) para buscá-los numa consulta.
5. Use a **ordenação** (sort key) para consultas por faixa e ordem.
6. Distribua o tráfego com chaves de **alta cardinalidade**.
7. Use **GSIs** para as consultas adicionais.
8. NoSQL Workbench (ferramenta da AWS) ajuda a modelar e visualizar.

## 2. Processo: perguntas antes das tabelas

Preencha a ficha de acesso (`${CLAUDE_PLUGIN_ROOT}/skills/playbook/assets/templates/ficha-de-padroes-de-acesso.md`). Para cada AP-n registre: operação (leitura/escrita), atributos de entrada, resultado esperado (um item, lista ordenada, faixa), frequência, latência-alvo, cardinalidade e consistência exigida.

Perguntas mínimas (faça **uma por vez**, a de maior impacto primeiro):
1. Quais são as consultas e escritas, em linguagem do negócio?
2. Qual o volume (itens, itens por consulta, crescimento) e o tamanho médio/máximo do item?
3. Alguma consulta precisa de leitura fortemente consistente?
4. Quais consultas são frequentes e quais são raras (relatórios)?
5. O acesso é por tenant/cliente? Há tenants muito maiores que os demais (risco de partição quente)?
6. Há retenção (TTL) ou arquivamento?

Sem respostas, entregue apenas a lista de perguntas e, no máximo, um modelo condicional rotulado Suposição.

## 3. Exemplo: pedidos de e-commerce (caso E-06)

Suponha estas respostas (hipotéticas, para ilustrar o método):

| AP | Operação | Entrada | Resultado |
| --- | --- | --- | --- |
| AP-1 | Obter pedido | `orderId` | 1 pedido com seus itens |
| AP-2 | Listar pedidos do cliente | `customerId` | Lista, mais recentes primeiro, paginada |
| AP-3 | Listar pedidos por status numa janela | `status`, intervalo de datas | Lista por data (consulta de operação, menos frequente) |

Proposta condicional (Inferido: padrão de uma tabela com chaves compostas; conferir com NoSQL Workbench):

| Entidade | PK | SK | Observação |
| --- | --- | --- | --- |
| Pedido (cabeçalho) | `CUSTOMER#<customerId>` | `ORDER#<isoTimestamp>#<orderId>` | AP-2 = `Query` na PK com SK decrescente; itens da lista em páginas |
| Item do pedido | `ORDER#<orderId>` | `ITEM#<lineNo>` | AP-1 = `Query` na PK `ORDER#...` traz cabeçalho (SK `META`) e itens |

Observações:
- AP-1 por `orderId` exige conhecer o `customerId` ou um GSI `GSI1`: PK `ORDER#<orderId>`. Escolha conforme o acesso real; o ideal é o mesmo registro responder AP-1 e AP-2, o que pode levar à duplicação de dados do cabeçalho (custo de escrita contra custo de leitura).
- AP-3: GSI com PK `STATUS#<status>#<yyyymm>` e SK `<isoTimestamp>#<orderId>`. Incluir `yyyymm` (ou outro particionador) evita concentrar todos os pedidos "pending" numa partição quente (V-26: chaves de alta cardinalidade). Cada GSI tem custo de escrita adicional (Inferido).
- Contadores por cliente/relatórios: considere outra ferramenta (fora do DynamoDB) para consultas ad hoc (segmento data-engineering).

## 4. GSIs e alta cardinalidade

- Um GSI por consulta adicional (V-26); não crie GSI "por precaução".
- Chave de alta cardinalidade distribui tráfego; chave com poucos valores (`status`, `country`) cria partição quente. Remédio comum: sufixo de particionamento (data, hash curto) com consulta fan-out (Inferido).
- Projeção do GSI: projete só os atributos necessários para reduzir custo (Inferido; conferir na doc).
- Consistência de GSI: tipicamente eventual (Inferido). Se a consulta exige leitura forte, planeje a chave na tabela base (conferir a doc).

## 5. Armadilhas

- `Scan` como padrão de acesso: lê a tabela inteira; aceitável só em operações raras/administrativas (Inferido).
- Replicar tabelas relacionais 1:1 (uma tabela por entidade) sem motivo: contraria a diretriz de menos tabelas (V-26).
- Esquecer o crescimento: itens grandes e coleções embutidas têm limites de tamanho por item (conferir o limite atual na doc; não citado na página lida).
- Modelar sem a pergunta sobre transações: cobertura de transações e consistência é lacuna (L-07).
- Atribuir a custos "milhões por segundo" sem fonte (Não verificável).
- Esquecer segurança: privilégio mínimo por tabela/índice nas políticas de acesso; credenciais por ambiente (V-37 como justificativa).

## 6. Lacunas e o que conferir

| Tema | Estado | Ação |
| --- | --- | --- |
| Capacidade e throughput (provisionado vs sob demanda), limites por partição | Sem fonte validada (L-07) | Peça ao usuário a configuração e remeta à doc atual |
| Single-table design em detalhe | Sem fonte validada (L-07) | Use a proposta como condicional |
| GSI vs LSI em detalhe | Sem fonte validada (L-07) | Conferir na doc |
| Transações (`TransactWriteItems`) | Sem fonte validada (L-07) | Idem |
| PITR/backup do DynamoDB | Sem fonte validada (L-06) | Ver `backup-restore-runbook` (modo genérico) |
| Limite de tamanho de item e de página de `Query` | Conhecimento geral, não na página lida | Conferir na doc antes de afirmar números |
