# Movimento e física no Godot 4

Sumário: [Diagnóstico de movimento](#diagnóstico-de-movimento) · [Receita: gravidade, pulo e coyote time](#receita-gravidade-pulo-e-coyote-time) · [Top-down](#top-down) · [Passo fixo em uma frase](#passo-fixo-em-uma-frase) · [Verificação](#verificação)

Fontes: V-14 (Godot physics introduction, Nystrom, Fiedler), V-11 (estilo), V-12 (CLI). Rótulos: Verificado (na doc citada), Inferido (conhecimento estável do Godot a confirmar na versão), Suposição. O código é redação própria e não foi executado pelo plugin: rode-o com `game-verify-by-running`.

## Diagnóstico de movimento

Em ordem de custo: leia o script e a cena, depois reproduza com sonda (a cena de teste e uma linha de log da posição e da velocidade), depois mude uma coisa.

| Sintoma | Causa provável | Como confirmar |
| --- | --- | --- |
| Anda lento demais | `velocity = dir * speed * delta`: `move_and_slide()` já aplica o passo (V-14) | logar `velocity` e comparar com `speed`; deve ser igual a `speed` em movimento |
| Lento ou irregular, depende da máquina | física em `_process` (taxa de render variável) em vez de `_physics_process` (V-14) | mover o código e comparar em duas taxas de quadro |
| Treme junto à parede ou à câmera | corpo move no tick de física e câmera/visual no render sem interpolação (Inferido) | desligar a suavização da câmera; ver se o tremor some; interpolação depende da versão: confirme na doc |
| Atravessa o chão ou a parede | sem `CollisionShape2D`/3D; camada e máscara não se encontram; chão é `Area2D` | Depurar > Mostrar formas de colisão; conferir `collision_layer` do chão e `collision_mask` do corpo |
| Não anda | ação inexistente no Mapa de Entrada (erro no console); script em nó sem corpo | ler o console; Projeto > Configurações > Mapa de entrada |
| Pulo falha às vezes | `is_on_floor()` lido antes de `move_and_slide()` no quadro; entrada lida no quadro errado | ordem: `move_and_slide()` atualiza `is_on_floor()`; ler entrada em `_physics_process` |
| Escorrega em rampa/desliza no chão | `floor_stop_on_slope`, `floor_max_angle` e `up_direction` não ajustados (Inferido) | inspecionar as propriedades do `CharacterBody` |
| Personagem top-down "cai" ou trava em quinas | modo de movimento `Grounded` num jogo sem gravidade (Inferido) | usar `motion_mode = MOTION_MODE_FLOATING` (ver Top-down) |

Regra que resolve a maioria: mexer em corpo físico só em `_physics_process`; `velocity` em px/s sem `delta`; gravidade (aceleração) com `delta`; visual e UI em `_process` (V-14, V-11).

## Receita: gravidade, pulo e coyote time

```gdscript
extends CharacterBody2D

@export var speed: float = 200.0
@export var jump_velocity: float = -380.0
@export var coyote_time: float = 0.1  # valor de design; ajustar jogando

var _gravity: float = ProjectSettings.get_setting("physics/2d/default_gravity")
var _coyote_left: float = 0.0


func _physics_process(delta: float) -> void:
	if is_on_floor():
		_coyote_left = coyote_time
	else:
		velocity.y += _gravity * delta
		_coyote_left = maxf(_coyote_left - delta, 0.0)

	if Input.is_action_just_pressed("jump") and _coyote_left > 0.0:
		velocity.y = jump_velocity
		_coyote_left = 0.0

	var axis := Input.get_axis("left", "right")
	velocity.x = axis * speed
	move_and_slide()
```

Notas:
- A gravidade padrão vem das Configurações do Projeto; o nome da chave de 2D (`physics/2d/default_gravity`) deve ser conferido na versão do projeto (Inferido).
- Aceleração, atrito, altura do pulo e a janela do coyote time são decisões de design; o agente pode implementar os parâmetros, mas só um humano jogando julga a sensação (NÃO AVALIADO).
- Valores ficam em `@export` ou em um `Resource`, não fixos no código.
- Um teste automático pode checar a lógica (por exemplo, "pular no quadro 3 depois de sair da plataforma funciona; no quadro 8 não"), não a sensação.

## Top-down

Sem gravidade, defina o modo flutuante do corpo para evitar o tratamento de chão e rampa:

```gdscript
func _ready() -> void:
	motion_mode = CharacterBody2D.MOTION_MODE_FLOATING
```

(Inferido; confirmar na referência da classe `CharacterBody2D` da versão.) O resto é igual: `velocity` em px/s, `move_and_slide()` em `_physics_process`.

## Passo fixo em uma frase

A física roda em passo fixo (padrão de 60 ticks por segundo no Godot, V-14; configurável em `Engine.physics_ticks_per_second`, Inferido) e o render roda em taxa variável. O padrão geral de Nystrom e Fiedler é: acumular o tempo do quadro, limitar o tempo e as iterações para evitar a espiral da morte, simular em passos fixos e interpolar na renderização. No Godot, o motor já faz isso para a física; seu trabalho é deixar a lógica de física no lugar certo. Para determinismo (replay, lockstep), a mesma sequência de tempos e entradas deve produzir o mesmo estado final (V-14).

## Verificação

1. Rode a cena de teste e logue `velocity` e posição por 60 quadros com uma sonda (`--probe`), em vez de "ver se parece ok".
2. Compare duas taxas de quadro se a suspeita é dependência de taxa (o resultado na física não deve mudar).
3. `godot --headless --path . --check-only -s res://player.gd` valida sintaxe (combinação Inferido, V-12); não valida movimento.
4. A sensação, o peso do pulo e o coyote time ficam NÃO AVALIADO até um humano jogar.
