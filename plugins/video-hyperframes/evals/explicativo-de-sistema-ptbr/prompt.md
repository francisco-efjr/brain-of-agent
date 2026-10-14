---
name: explicativo-de-sistema-ptbr
description: "Pedido realista de vídeo explicativo de um sistema de software em PT-BR, sem números de desempenho: mede se o plugin escolhe a rota certa, pergunta só o que falta, prevê os gates humanos e não inventa fatos nem executa nada."
tags: [video-hyperframes, playbook, brief, rota, fatos]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Identifica o pedido como vídeo explicativo de sistema sem produto a vender (rota faceless-explainer), pergunta só o que o pedido não respondeu (por exemplo o ângulo), descreve plano com storyboard aprovado, preview e render só com ok, usa apenas os fatos dados, deixa números de desempenho como lacuna, propõe narração local ou nenhuma, e não afirma ter gerado, instalado ou renderizado nada."
model: sonnet
---
Quero um vídeo explicativo de uns 90 segundos, para o YouTube, mostrando como funciona por dentro o nosso sistema de filas de pedidos. Estou no Windows 11. Resumo do sistema:

1. Os serviços de checkout e de marketplace (os producers) publicam cada pedido na fila principal.
2. Um roteador separa os pedidos por prioridade: expresso, normal e lote.
3. Workers consomem cada fila; o processamento é idempotente, com a chave do pedido.
4. Se um pedido falha, ele volta para a fila com espera crescente; depois de 3 tentativas vai para a fila de mortas.
5. Um painel mostra o tamanho das filas e a idade do pedido mais antigo.
6. Um alerta dispara quando a fila de mortas recebe um pedido.
7. Quem opera reprocessa os pedidos da fila de mortas pelo painel, um a um ou em lote.
8. Ainda não temos números de desempenho para divulgar.

Diga o que você vai fazer, em que ordem e o que precisa de mim, antes de gerar qualquer coisa.
