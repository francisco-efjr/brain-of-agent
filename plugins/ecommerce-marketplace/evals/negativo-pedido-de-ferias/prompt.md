---
name: negativo-pedido-de-ferias
description: "Caso negativo de quase-acerto. Pedido de backend genérico com as palavras pedido e reserva em outro sentido (pedido de férias, reserva de datas no calendário). Mede se nenhuma skill do plugin de e-commerce dispara, se nenhuma referência do playbook é lida e se a resposta é uma tarefa comum de backend."
tags: [ecommerce-marketplace, negative, near-miss, scope]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Responde direto como tarefa genérica de backend com endpoint, validação de datas, regras de aprovação do gestor e reserva de datas sem conflito, sem acionar nenhuma skill do plugin de e-commerce e sem ler as referências do playbook."
model: sonnet
---
Cria um endpoint Express para os funcionários registrarem pedidos de férias. Regras: o funcionário informa data de início e fim (início não pode ser no passado, fim não pode ser antes do início, máximo de 30 dias corridos por pedido), o gestor direto aprova ou rejeita, e quando aprovado as datas ficam reservadas no calendário do time, sem permitir que duas pessoas da mesma equipe fiquem ausentes ao mesmo tempo mais de 2 dias seguidos. A persistência pode ficar atrás de duas funções que eu implemento depois: `salvarPedido(pedido)` e `listarReservasDoTime(timeId, inicio, fim)`. Quero as rotas `POST /pedidos-ferias` e `POST /pedidos-ferias/:id/decisao`, com a validação e os testes unitários da regra de conflito.
