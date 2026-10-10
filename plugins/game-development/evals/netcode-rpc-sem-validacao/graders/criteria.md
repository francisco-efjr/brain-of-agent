---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Não aprova o código. Afirma o princípio: o servidor é a autoridade e o cliente envia intenção (input ou pedido), não resultado; o RPC `any_peer` aceita chamadas de qualquer par e por isso os argumentos são não confiáveis.
2. Trata cada RPC com cenário de abuso concreto: `set_position_from_client` permite teletransporte e atravessar paredes; `apply_damage` permite um cliente causar dano a qualquer nó (inclusive `amount` negativo ou `target_path` arbitrário); `buy_item` permite um preço informado pelo cliente (zero ou negativo, item inexistente).
3. Recomenda que dano e preço sejam calculados no servidor a partir de dados do servidor, e que a posição seja derivada de input validado no servidor (com limite de velocidade e colisão), não aceita do cliente.
4. Recomenda validar remetente (`multiplayer.get_remote_sender_id()`), faixa, dono e frequência em todo RPC, e não apenas acrescentar uma checagem do tipo `if amount > 0`; menciona limitar a taxa de ações frequentes.
5. Recomenda teste com dois pares (servidor e cliente) antes de considerar pronto, e declara o que não avaliou (por exemplo reconciliação, previsão, anti-cheat além de autoridade, que encaminha a segurança); não afirma ter executado nada.
6. Se mencionar Unity ou outras engines, não afirma que a documentação do Unity manda validar RPC (isso é oficial no Godot; no Unity é boa prática, Inferido).
FAIL if qualquer um ocorrer: aprova o código; sugere só `if amount > 0` como correção suficiente; mantém dano, preço ou posição calculados pelo cliente; afirma validação oficial do Unity por RPC; afirma ter rodado o jogo ou o servidor.
