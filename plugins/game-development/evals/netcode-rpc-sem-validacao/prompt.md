---
name: netcode-rpc-sem-validacao
description: Caso de revisão de autoridade e RPC em Godot 4. Mede se o plugin trata o servidor como autoridade, rejeita posição, dano e preço vindos do cliente, exige validação de remetente, faixa, dono e frequência com cenário de abuso por RPC, não só um if de sanidade, e declara o que não avaliou.
tags: [game-development, game-netcode-review, godot, multiplayer, authority, security]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Reprova os três RPCs: servidor deve ser a autoridade, cliente envia intenção e não resultado, posição, dano e preço são calculados ou validados no servidor com get_remote_sender_id, faixa, dono e frequência, cada achado traz cenário de abuso, recomenda teste com servidor e cliente e declara o que não avaliou."
model: sonnet
---
Godot 4, jogo multiplayer com servidor dedicado, jogadores conectam pela internet. Revisa a segurança desses RPCs antes de eu subir o servidor de teste:

```gdscript
@rpc("any_peer", "call_remote", "reliable")
func set_position_from_client(pos: Vector2):
    global_position = pos

@rpc("any_peer")
func apply_damage(target_path: NodePath, amount: int):
    get_node(target_path).health -= amount

@rpc("any_peer")
func buy_item(price: int, item_id: String):
    gold -= price
    inventory.append(item_id)
```
