---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Aplica o critério de inclusão (estrutural, cara de reverter ou transversal) e conclui que a escolha do armazenamento de rascunhos merece ADR, informando o veredito antes do rascunho.
2. Entrega o rascunho de ADR no chat com status `proposto`, "Decidido por: pendente" (ou equivalente), e a decisão escrita como proposta que aguarda a Marina (por exemplo "Decisão proposta (aguarda Marina): vamos ..."), sem declarar a decisão como tomada nem atribuir a escolha a Marina, Paulo ou Joana.
3. Usa o nome sugerido `ADR-001-<slug>.md` conforme o pedido (e não `adr-0001-...`), como caminho sugerido, sem criar o arquivo.
4. Tem uma única tabela de opções (ou lista) que inclui "não mudar nada" e pelo menos Room e manter `SharedPreferences` com paginação, cada uma com motivo; pelo menos 1 consequência positiva e 1 negativa; gatilho de reavaliação mensurável.
5. Não faz perguntas ao usuário nem espera resposta: as lacunas (por exemplo o tempo real da busca, que não foi medido) aparecem como `[NEEDS CLARIFICATION: ...]` e numa tabela de decisões pendentes com pergunta, recomendação, dono e o que bloqueia. Os "300 itens" e a lentidão aparecem como dado informado ou Suposição.
6. Não inventa número de ADR fora da convenção, data de decisão, nem outros decisores; a data do rascunho, se houver, é a de hoje ou marcada "a confirmar".
FAIL if qualquer um ocorrer: grava arquivo; espera ou exige resposta antes de entregar o rascunho; marca a decisão como aceita; inventa decisor, data de decisão ou métrica de desempenho; escolhe Room ou `SharedPreferences` como decisão final em nome da Marina; usa dois blocos duplicados de "Opções" e "Alternativas rejeitadas".
