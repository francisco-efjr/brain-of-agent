# Notas (incertezas)

- Respondi só com conhecimento próprio, sem skill, sem rede, sem ler skills/ nem evals/ além da pasta de saída.
- Ordem dos passos: o usuário só disse "aplica o cupom, troca o endereço pra outro CEP, pagamento". Passos 1 (carrinho/itens/CEP inicial), 4 (olhar resumo) e 5 (finalizar) são reconstrução minha; avisei no texto para o usuário confirmar.
- Ambíguo: "o desconto some da tela mas o total continua com desconto". Entendi como: linha de desconto sumiu, total continuou descontado. Não sei em qual tela isso aparece (carrinho, resumo do checkout) nem se a tela de pagamento mostrava o total com ou sem desconto antes de cobrar.
- Não sei se o pedido 88123 é uma das 2 ocorrências, se é pedido de cliente real ou de teste, nem os valores. Deixei como pergunta/placeholder em vez de supor.
- "2 vezes de 5": interpretei como 2 de 5 tentativas no A54. Pode ser 2 de 5 pedidos/ocorrências reportadas por usuários. Escrevi como tentativas no A54 e deixei campo para esclarecer.
- Não inventei: versão do Android, ambiente (prod/homolog), CEPs, itens, valores, modelo do iPhone, usuário. Todos como [preencher].
- Severidade "Alta" é julgamento meu (cobrança maior que o exibido, impacto financeiro e de consumidor); o time pode ter escala própria.
- Não incluí hipótese de causa (ex.: recálculo do frete/região invalidando cupom no backend com estado local desatualizado, condição de corrida entre recálculos). Seria palpite sem dado; só registrei o fato de que tela e cobrança divergem.
- Avisei que "não acontece no iPhone" pode ser falta de amostra; não sei quantas vezes foi testado.
- Sugeri tratar a cobrança a mais do 88123 à parte (estorno), condicionado a ser cliente real. É fora do escopo estrito do bug report, mas relevante.
- Resposta mais longa que o mínimo por incluir as 5 perguntas finais; considerei que valem o custo porque o relato tem lacunas que o dev vai perguntar de qualquer forma.
