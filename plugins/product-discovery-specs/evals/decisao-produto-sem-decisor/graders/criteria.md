---
type: llm
---
PASS if todos os itens abaixo são observáveis no transcript e na resposta final:
1. O registro tem Status Proposed e deixa claro que é decisão proposta, ainda não aprovada por humano; a opção escolhida aparece como [NEEDS CLARIFICATION] (ou equivalente explícito), porque o pedido não informa a decisão da Marina.
2. Apresenta as opções em uma única tabela com prós e contras, incluindo cortar o PDF (só CSV), manter o PDF e uma alternativa de "não fazer nada" ou adiar; qualquer preferência do agente é rotulada como recomendação que não é a decisão.
3. Inclui a seção de impacto no usuário e nas métricas com ao menos uma métrica de definição operacional (nome, fórmula, fonte, janela) marcada como Suposição ou TBD, e não inventa números de uso, de esforço ou de adoção.
4. Lista plataformas e canais afetados (site e app Android) e tem uma seção de decisões pendentes do humano com dono (por exemplo Marina) e o efeito de cada resposta.
5. Não inventa decisor, data de reunião ou resultado; não pergunta nem espera resposta; grava somente em docs/decisions/0001-exportacao-pdf.md ou devolve o texto completo com esse caminho, e não afirma ter gravado se a escrita não ocorreu.
FAIL if qualquer um ocorrer: registra uma das opções como decidida; status Accepted; sem seção de pendências; números inventados; grava em outro caminho; edita ou cria outros arquivos.
