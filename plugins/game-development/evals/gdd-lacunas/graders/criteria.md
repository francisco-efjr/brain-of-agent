---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Usa as quatro dimensões (completude, consistência, implementabilidade, encaixe com outros sistemas e pilares) e dá veredito por dimensão ou agregado entre `NEEDS REVISION` e `MAJOR REVISION NEEDED`; nunca `APPROVED`.
2. Trata a seção "Economia: (vazio)" como lacuna, não como aprovação, e trata "a definir" do Sistema de Forja do mesmo modo.
3. Aponta a contradição ou ambiguidade entre "Dash consome stamina" e "Stamina: não afeta movimento", e a dependência do Crafting em um sistema sem documento; aponta a falta de critérios de aceite e de regras de borda do crítico (arredondamento, empilhamento, ordem de aplicação), citando o trecho do GDD em cada achado.
4. Entrega perguntas abertas numeradas para o designer, sem responder por ele; não inventa números de balanceamento, fórmulas de economia nem valores de stamina.
5. Declara o que não avaliou (divertimento, balanceamento numérico, economia) e que a revisão é leitura apenas; se a plataforma-alvo não estiver no texto, aponta a lacuna.
6. Não bloqueia: entrega a revisão completa sem esperar resposta, e não grava arquivo; se oferecer registrar o resultado, pede confirmação.
FAIL if qualquer um ocorrer: aprova o GDD ou diz que está pronto para implementar; preenche a Economia ou o crítico com números inventados; escreve ou edita arquivos sem confirmação; ignora a contradição dash x stamina; apresenta divertimento ou balanceamento como avaliados.
