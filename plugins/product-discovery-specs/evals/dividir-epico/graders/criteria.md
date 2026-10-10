---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Entrega fatias numeradas em que cada uma tem valor perceptível para o lojista sozinha (por exemplo: ver a lista de pedidos com status, ver o detalhe, marcar como enviado, cancelar com motivo), na forma de história com benefício.
2. Aplica INVEST ao épico ou às fatias, apontando ao menos qual letra o épico original falha (pequena, estimável ou testável) e por quê.
3. Lista regras implícitas e perguntas abertas com dono (por exemplo permissões de quem altera pedido, estados permitidos, pedido já pago, cancelamento e estoque, notificação ao cliente, canais web e app) em vez de decidi-las em silêncio.
4. Não divide por camada técnica (banco, API, tela) e cada fatia tem critério resumido com exemplo concreto.
5. Não promete que cabe na sprint de 2 semanas nem trata estimativa como fato; se menciona tamanho, rotula como Suposição.
FAIL if qualquer um ocorrer: divisão horizontal por camada; histórias sem valor visível; promessa de prazo; decide regras de negócio como fatos.
