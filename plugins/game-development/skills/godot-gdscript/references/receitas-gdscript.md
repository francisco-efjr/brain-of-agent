# Receitas de GDScript (Godot 4)

Sumário: [Arquivo no estilo oficial](#arquivo-no-estilo-oficial) · [Máquina de estados](#máquina-de-estados) · [Resource para dados](#resource-para-dados) · [Sinais](#sinais) · [Carregar cena sem travar](#carregar-cena-sem-travar) · [Teste com GUT](#teste-com-gut) · [TileMap para TileMapLayer](#tilemap-para-tilemaplayer) · [Checklist de revisão](#checklist-de-revisão)

Fontes: V-11 (guia de estilo oficial), V-12 (GUT, CLI), V-32 (CLAUDE.md Godot), V-14 (física). Rótulos: Verificado (na doc citada), Inferido (conhecimento estável do Godot a conferir na versão), Suposição. Código em redação própria (MIT do plugin), não executado pelo plugin: rode e leia a saída real. Padrões de design de terceiros (EventBus, uma classe por estado) são opções, não regra (V-32).

## Arquivo no estilo oficial

```gdscript
class_name Enemy
extends CharacterBody2D
## Inimigo que persegue o jogador dentro de um raio.

signal died(enemy: Enemy)

enum Mode { IDLE, CHASE }

const DEFAULT_SPEED: float = 90.0

@export var stats: EnemyStats
@export_range(0.0, 600.0, 10.0) var chase_radius: float = 240.0

var _mode: Mode = Mode.IDLE
var _target: Node2D

@onready var _sprite: Sprite2D = $Sprite2D


func _ready() -> void:
	_target = get_tree().get_first_node_in_group("player") as Node2D


func _physics_process(_delta: float) -> void:
	if _target == null:
		return
	var to_target := _target.global_position - global_position
	_mode = Mode.CHASE if to_target.length() <= chase_radius else Mode.IDLE
	velocity = to_target.normalized() * stats.move_speed if _mode == Mode.CHASE else Vector2.ZERO
	move_and_slide()
```

Pontos do guia aplicados (V-11): ordem `class_name`, `extends`, doc, sinais, enums, constantes, `@export`, variáveis, `@onready`, callbacks; `snake_case` para funções e variáveis; `PascalCase` para classe e enum; sinal no passado; tipos em tudo; `:=` com tipo óbvio; `as` seguido de tratamento de `null`; filho em `@onready` tipado; física em `_physics_process`.

## Máquina de estados

Com tabela de transições, estados inválidos ficam inalcançáveis (padrão do `gameplay-programmer`, V-23):

```gdscript
enum State { IDLE, RUN, JUMP, FALL }

const TRANSITIONS: Dictionary = {
	State.IDLE: [State.RUN, State.JUMP, State.FALL],
	State.RUN: [State.IDLE, State.JUMP, State.FALL],
	State.JUMP: [State.FALL],
	State.FALL: [State.IDLE, State.RUN],
}

var _state: State = State.IDLE


func _change_state(next: State) -> void:
	if next == _state:
		return
	if not (TRANSITIONS[_state] as Array).has(next):
		push_error("Transição inválida: %s -> %s" % [State.keys()[_state], State.keys()[next]])
		return
	_state = next
```

Testar a tabela com GUT (uma asserção por transição inválida) vale mais do que olhar a animação. Use `match _state:` para o comportamento de cada estado; classes `State` separadas são opção para estados complexos.

## Resource para dados

Valores de gameplay em `Resource`, não no código (V-32, V-23):

```gdscript
class_name EnemyStats
extends Resource

@export var max_health: int = 30
@export var move_speed: float = 120.0
@export var contact_damage: int = 5
```

Crie `res://data/enemies/goblin.tres` pelo editor e atribua ao `@export var stats`. Cuidado (Inferido): um `Resource` carregado é compartilhado; se cada inimigo precisa de vida própria, mantenha a vida atual numa variável do nó, ou chame `stats.duplicate()`; alterar o recurso compartilhado altera todos. Autoload só para estado global único (por exemplo, configurações do jogador).

## Sinais

```gdscript
signal health_changed(old_value: int, new_value: int)

func take_damage(amount: int) -> void:
	var old := _health
	_health = maxi(_health - amount, 0)
	health_changed.emit(old, _health)
```

Conectar (Godot 4): `enemy.died.connect(_on_enemy_died)`; para desconectar ao sair, `enemy.died.disconnect(_on_enemy_died)` ou deixar o nó ser liberado. Sinais sobem (filho avisa o pai) e chamadas descem (pai chama método do filho); autoload global para tudo vira acoplamento oculto (V-32: opção, não regra). Confirme a sintaxe de sinais tipados na versão do projeto.

## Carregar cena sem travar

Causas comuns de "trava ao carregar a cena" (Inferido; confirme com o log do editor):

| Causa | Sinal | Ajuste |
| --- | --- | --- |
| `load()` de recurso grande no meio da partida | quadro longo na troca | carregar antes, ou assíncrono (abaixo) |
| laço pesado ou instanciar centenas de nós em `_ready()` | travada logo ao entrar | instanciar em lotes ao longo de quadros |
| `await` que nunca resolve (sinal que nunca é emitido) | cena fica parada sem erro | logar antes do `await`; garantir quem emite |
| erro em `_ready()` de um autoload | tela preta ou parada | ler o console; testar com `--headless --import` e abrir a cena |
| dependência circular de `preload` | erro de recursão cíclica | trocar por `load()` tardio ou desacoplar |
| `@onready` com caminho errado | `null` e erro em cadeia | conferir o caminho na árvore da cena |

Carga assíncrona (API do Godot 4, Inferido):

```gdscript
var _path: String = ""


func start_loading(path: String) -> void:
	_path = path
	ResourceLoader.load_threaded_request(path)
	set_process(true)


func _process(_delta: float) -> void:
	var status := ResourceLoader.load_threaded_get_status(_path)
	if status == ResourceLoader.THREAD_LOAD_LOADED:
		var scene := ResourceLoader.load_threaded_get(_path) as PackedScene
		set_process(false)
		get_tree().change_scene_to_packed(scene)
```

(Trate também `THREAD_LOAD_FAILED`; chame `set_process(false)` em `_ready()` para só rodar durante a carga.) Reproduza com a sonda `--level` e meça o tempo antes de otimizar.

## Teste com GUT

Só se o projeto adotou GUT (MIT; V-12). Escolha um framework por projeto.

```gdscript
extends GutTest

func test_transicao_invalida_nao_muda_estado() -> void:
	var player := preload("res://player/player.tscn").instantiate()
	add_child_autofree(player)
	player._change_state(Player.State.JUMP)
	player._change_state(Player.State.IDLE)  # JUMP -> IDLE é inválida
	assert_eq(player._state, Player.State.JUMP)
```

Rodar: `godot --headless --path . -s addons/gut/gut_cmdln.gd -gdir=res://test/unit -gexit`; exit 0 passa e 1 falha (V-12). Nomes de asserção e helpers (`add_child_autofree`) devem ser conferidos na versão do GUT instalada. Testar `_state` privado no exemplo é por brevidade; prefira uma API pública quando houver.

## TileMap para TileMapLayer

`TileMap` está deprecated e `TileMapLayer` é o substituto (V-32). A versão que o depreciou não foi confirmada no VALIDATED; o conhecimento geral aponta a série 4.3 (Inferido; confirme na página da classe e no changelog da sua versão).

1. Fixe a versão (`godot --version`). Se for anterior à que traz `TileMapLayer`, não migre.
2. Faça backup (commit limpo) antes de qualquer conversão; a migração mexe em cenas `.tscn`.
3. O editor oferece uma ferramenta de conversão ao selecionar o `TileMap` (Inferido; o nome do botão muda por versão). Prefira-a a editar a cena à mão.
4. Troque no código as chamadas por camada (`set_cell(layer, ...)`) pelas do nó `TileMapLayer` correspondente (cada camada vira um nó; Inferido).
5. Verifique: `godot --headless --path . --import`, abrir as cenas afetadas, comparar o mapa visualmente (humano) e rodar os testes.

## Checklist de revisão

- [ ] versão do Godot conhecida e docs da série 4 usadas (não 3.5)
- [ ] variáveis, parâmetros e retornos tipados; `as` com tratamento de `null`
- [ ] nomes: arquivo/função `snake_case`, classe `PascalCase`, constante `CONSTANT_CASE`, sinal no passado, privado com `_`
- [ ] ordem de membros conforme o guia; filhos com `@onready` tipado, nunca em `_init()`
- [ ] física em `_physics_process`; `move_and_slide()` sem `velocity * delta`; gravidade com `delta`
- [ ] busca de nós fora de `_process`; referências guardadas
- [ ] valores de gameplay em `@export`/`Resource`, não fixos
- [ ] sem edição em `.godot/` nem `addons/`
- [ ] comandos headless rodados e exit code registrado; pendências humanas listadas
