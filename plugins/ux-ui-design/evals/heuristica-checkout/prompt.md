---
name: heuristica-checkout
description: Mede se, ao pedirem avaliação de usabilidade de um fluxo de checkout descrito em texto, o plugin faz avaliação heurística com heurísticas nomeadas, severidade 0 a 4 justificada, separa trade-offs a validar, declara que é opinião de modelo e propõe o que testar com usuários, sem projetar taxa de abandono.
tags: [ux-ui-design, heuristic-eval, usabilidade]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Achados com heurística de Nielsen nomeada, local exato, evidência, severidade 0 a 4 com frequência, impacto e persistência, trade-offs marcados a validar, top 3, o que testar com usuários e declaração de que é opinião de modelo; nenhuma previsão de taxa de abandono."
model: sonnet
---
Avalia a usabilidade desse fluxo de checkout de uma loja de móveis. A maioria dos clientes compra pelo celular. Não tenho capturas; é a descrição do que o time implementou:

Passo 1, carrinho: lista os itens com foto, preço e botão "Enviar". Não há indicador de quantos passos faltam.
Passo 2, endereço: formulário com 11 campos, todos obrigatórios, inclusive "Complemento" e "Telefone fixo". O CEP não preenche os outros campos. O botão é "Enviar".
Passo 3, pagamento: cartão, boleto ou Pix, em abas. Se o cartão é recusado aparece um aviso vermelho no topo da página com o texto "Falha na operação" e o formulário volta vazio. O botão é "Enviar".
Passo 4, revisão: resumo do pedido e o campo "Cupom de desconto". Se o cupom é inválido, aparece "Erro" e o carrinho é esvaziado. O botão é "Enviar".
Não existe botão de voltar dentro do fluxo; o botão voltar do navegador leva ao passo 1 e perde o endereço digitado.

O time está discutindo se vale refazer o fluxo. Preciso de algo para levar à reunião.
