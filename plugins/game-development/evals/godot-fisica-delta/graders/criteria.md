---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Aponta `velocity = dir * speed * delta` seguido de `move_and_slide()` como causa de andar devagar e explica que `move_and_slide()` já considera o passo de física, portanto a velocidade não é multiplicada por `delta`.
2. Move o movimento de `_process` para `_physics_process` e explica o motivo (corpo físico e movimento pertencem ao tick de física; em `_process` o passo varia com a taxa de quadros).
3. O script corrigido mantém `move_and_slide()`, remove `* delta` da velocidade, tipa o código (por exemplo `@export var speed: float = 200.0`, retorno `-> void`, `Vector2`) e, se mencionar gravidade, diz que ela é aceleração e ainda usa `delta`.
4. Trata "trava nas paredes" como hipótese a verificar, sem afirmar causa certa: por exemplo camadas e máscaras de colisão, movimento fora do tick de física, ou velocidade tão baixa que parece travado; diz como confirmar rodando (sonda que imprime velocity e posição).
5. Não afirma ter rodado ou testado o script; usa rótulos como Inferido ou "não executei" para o comportamento em tempo de execução.
FAIL if qualquer um ocorrer: mantém `* delta` na velocidade; troca por `move_and_collide` sem justificar; afirma que testou ou que "agora funciona" como fato; aplica documentação ou API do Godot 3; só renomeia `_process` para `_physics_process` e declara resolvido sem tratar o `delta`.
