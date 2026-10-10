# Godot 4 (GDScript)

Engine e versão-alvo: Godot 4.x (fixe com `godot --version`). Base: V-11, V-12, V-13, V-14, V-15, V-24, V-32; páginas `stable` da documentação lidas em 2026-10-10 (a versão exata de `stable` não foi registrada; reconfira). Documentação do Godot 3.5 não vale para o 4.

## Sumário

- [Estilo oficial](#estilo-oficial)
- [Estrutura de script e ordem de membros](#estrutura-de-script-e-ordem-de-membros)
- [Física e movimento](#física-e-movimento)
- [CLI headless e testes](#cli-headless-e-testes)
- [Performance](#performance)
- [Multiplayer](#multiplayer)
- [Especialista de engine](#especialista-de-engine)
- [Deprecados e armadilhas](#deprecados-e-armadilhas)
- [Opções de design (sem imposição)](#opções-de-design-sem-imposição)

## Estilo oficial

Guia de estilo GDScript (V-11, classe A):

| Elemento | Convenção | Exemplo |
| --- | --- | --- |
| arquivo, função, variável, sinal | snake_case | `player_controller.gd`, `take_damage` |
| classe e `class_name` | PascalCase | `PlayerController` |
| constante | CONSTANT_CASE | `MAX_SPEED` |
| sinal | snake_case no passado | `door_opened` |
| enum | PascalCase no singular; membros CONSTANT_CASE | `enum Element { EARTH, WATER }` |
| privado e virtual sobrescrito | prefixo `_` | `_physics_process`, `_hp` |

Tipagem: tipar variáveis, parâmetros e retornos. `:=` só quando o tipo está claro na mesma linha; com `get_node()` use tipo explícito (`var body: Sprite2D = $Body`). O operador `as` falha em silêncio devolvendo `null` quando o tipo é incompatível: trate o retorno.

```gdscript
var enemy := body as Enemy          # pode ser null
if enemy == null:
    push_warning("body não é Enemy: %s" % body.name)
    return
```

## Estrutura de script e ordem de membros

Ordem (V-11): anotações de ferramenta, `class_name`, `extends`, doc, sinais, enums, constantes, variáveis estáticas, `@export`, demais variáveis, `@onready`, callbacks (`_init`, `_ready`, `_process`...), métodos, classes internas. Filhos em `@onready` tipado, nunca em `_init()` (a árvore ainda não existe). Não busque nós em `_process`: guarde a referência uma vez.

```gdscript
class_name Spawner
extends Node2D
## Instancia inimigos até um limite.

signal enemy_spawned(enemy: Node2D)

@export var enemy_scene: PackedScene
@export_range(1, 100) var max_enemies: int = 10

var _alive: Array[Node2D] = []

@onready var _timer: Timer = $Timer

func _ready() -> void:
    _timer.timeout.connect(_spawn)

func _spawn() -> void:
    if _alive.size() >= max_enemies:
        return
    var e := enemy_scene.instantiate() as Node2D
    if e == null:
        push_error("enemy_scene não é Node2D")
        return
    add_child(e)
    _alive.append(e)
    enemy_spawned.emit(e)
```

Dados compartilhados em `Resource` (`.tres`) com `@export`; `autoload` só para estado global único. Não edite `.godot/` (cache gerado) nem `addons/` (terceiros) sem autorização.

## Física e movimento

Ver `nucleo-tecnico.md`. Resumo: tudo que toca corpo físico em `_physics_process`; `move_and_slide()` sem `velocity * delta`; gravidade com `delta`; visual e UI em `_process`; camadas e máscaras documentadas (por exemplo em `docs/camadas.md`).

## CLI headless e testes

Fonte: tutorial de linha de comando do Godot e documentação do GUT (V-12). Da raiz do projeto, leia a saída real:

```text
1. checkout limpo:     godot --headless --path . --import
2. sintaxe de script:  godot --headless --path . --check-only -s res://scripts/x.gd
3. testes (GUT):       godot --headless --path . -s addons/gut/gut_cmdln.gd -gdir=res://test/unit -gexit
```

- `--headless` equivale a driver de vídeo headless com áudio Dummy; `--import` abre o editor, espera a importação e sai; `--check-only` analisa o script e sai, usado com `-s`; `--path` aponta o projeto (precisa de `project.godot`).
- A combinação `--headless` + `--check-only` foi montada a partir de opções documentadas e **não foi executada**: Inferido. `--check-only` existe em builds de editor/templates estendidos. Confirme com `godot --help` na sua versão e aceite o comando que o CLAUDE.md do projeto fixar.
- GUT 9 exige Godot 4 (docs atuais miram 4.6); exit 0 se tudo passa, 1 se falhar; o texto sobre linha de comando não menciona `--headless`, então a combinação é Inferido.
- Exit code diferente de 0 ou `ERROR` no log = não está pronto. **Um** framework de teste por projeto (GUT ou GdUnit4).
- Não prova: aparência, animação, áudio, sensação.
- Exemplo de teste GUT (redação própria; confira a API na versão instalada):

```gdscript
extends GutTest

func test_damage_never_negative() -> void:
    var d := Combat.damage(10, 25)   # ataque 10, defesa 25
    assert_eq(d, 0, "dano mínimo é 0")
```

## Performance

Fonte: "General optimization" (V-13). Perfile antes; bisseção desligando metade das rotinas do quadro; teste em mais de um dispositivo (sobretudo mobile); V-Sync desligado; CPU e GPU olhados separadamente. Checklist: medição antes e depois, mesmo cenário, V-Sync off; uma mudança por medição; gargalo no profiler ou por bisseção; CPU e GPU separados; hardware de referência; orçamento em ms. Correção do validador: "evitar chamadas que bloqueiam o servidor a cada quadro" **não** está nessa página.

Candidatos estáticos típicos (rotule "candidato"): `get_node()` ou `find_child` em `_process`; centenas de nós com `_process` desnecessário; instanciar cenas no meio do quadro sem pool; carregamento síncrono de recurso grande em gameplay.

## Multiplayer

Fonte: "High-level multiplayer" (V-15). O servidor (peer 1) é a autoridade padrão; `@rpc` com modo, sync, transfer_mode e canal (padrão equivalente a authority, call_remote, reliable, canal 0); trate input do cliente como não confiável; valide argumentos de RPC; limite a taxa de ações frequentes; `multiplayer.get_remote_sender_id()` identifica o chamador. Veja o exemplo em `nucleo-tecnico.md`.

## Especialista de engine

O agente `game-engine-specialist` (V-24): leia a versão fixada em `project.godot` e no CLAUDE.md antes de sugerir API; rotule "não verificado" o que não estiver na referência da versão; escolha GDScript x C# x GDExtension por custo de build, desempenho e integração com o editor (tabela em `decisoes-e-tradeoffs.md`); proponha antes de pedir gravação. Dica de busca: para `.gd` use glob `*.gd`, não `type "gdscript"` (aviso do arquivo original, não conferido).

## Deprecados e armadilhas

| Padrão antigo | Use | Observação |
| --- | --- | --- |
| `TileMap` | `TileMapLayer` | a página da classe confirma a depreciação; a versão que depreciou não foi confirmada (V-32) |
| documentação 3.5 / `yield` / `onready` sem `@` | docs do 4; `await`; `@onready` | resultados de busca podem trazer sintaxe do Godot 3 (conhecimento estável do 4; Inferido) |
| `velocity * delta` em `move_and_slide()` | `velocity` direto | V-14 |
| busca de nó em `_process` | `@onready` tipado | V-32 |

## Opções de design (sem imposição)

EventBus, uma classe State por estado, sinais em vez de globals: vêm de terceiros (V-32), são padrões de design e não de estilo. Ofereça como opção com trade-off; não imponha. `gdtoolkit` (`gdlint`/`gdformat`): só se o projeto já usa; versão e comandos não verificados (V-32).
