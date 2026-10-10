---
name: godot-fisica-delta
description: Caso de correção de movimento no Godot 4. Mede se o plugin move o código para _physics_process, remove a multiplicação da velocidade por delta explicando que move_and_slide já considera o passo, tipa as variáveis, trata o travamento em parede como hipótese e não afirma ter rodado.
tags: [game-development, godot-gdscript, godot, physics, delta]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Identifica velocity multiplicada por delta antes de move_and_slide como causa de andar devagar, move o movimento para _physics_process, tipa o script (speed como float exportado), trata o travar em paredes como hipótese a verificar (camadas e máscaras, callback) e não afirma ter testado."
model: sonnet
---
Godot 4. Meu personagem anda devagar demais e às vezes trava nas paredes:

```gdscript
extends CharacterBody2D
var speed = 200
func _process(delta):
    var dir = Input.get_vector("left", "right", "up", "down")
    velocity = dir * speed * delta
    move_and_slide()
```

O que está errado? Pode me devolver o script corrigido.
