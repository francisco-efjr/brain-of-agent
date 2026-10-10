# Método de performance e catálogo de candidatos

Sumário: [Orçamento e conversões](#orçamento-e-conversões) · [Confirmar com medição](#confirmar-com-medição) · [Candidatos por engine](#candidatos-por-engine) · [Exemplo de hotspots](#exemplo-de-hotspots)

Fontes: V-13 (Godot, doc oficial), V-17 (Unity, método geral), V-16 (manual Unity 6000.0), V-25 (estrutura da auditoria). Rótulos: Verificado (na fonte citada), Inferido (conhecimento estável ou análise a confirmar na versão), Não verificado. Nada aqui foi executado pelo plugin.

## Orçamento e conversões

O orçamento é do projeto, não da skill. Peça ao responsável ou leia de CLAUDE.md, config ou GDD.

| Item | Valor de referência | Fonte |
| --- | --- | --- |
| 30 fps | 33,33 ms por quadro | V-17 |
| 60 fps | 16,66 ms por quadro | V-17 |
| Mobile | deixar cerca de 35% do quadro livre (22 ms a 30 fps) | V-17 |
| Conversão | `ms = 1000 / fps`; 40 fps = 25 ms; 144 fps = 6,94 ms | aritmética |
| Menu e carregamento | estourar é aceitável | V-17 |
| Gameplay | estourar não é aceitável | V-17 |

Métricas do orçamento que um projeto costuma declarar: fps alvo, ms de CPU e de GPU por quadro, memória, draw calls, tempo de carga, tamanho do build. Qualquer uma sem valor é NÃO AVALIADO. Um número genérico (16,67 ms) serve de contexto, nunca de veredito (V-25).

## Confirmar com medição

Ordem recomendada (V-13, V-17), executada pelo usuário ou por `game-verify-by-running` com permissão:

1. Build no hardware-alvo (ou no mais fraco disponível), não o editor. V-Sync desligado, para não limitar o quadro (V-13).
2. Anote o ms por quadro e por thread. O quadro é limitado pelo mais lento entre CPU e GPU (V-13, V-17).
3. **Classificar**: se o ms de CPU domina, o jogo é CPU-bound; se a GPU domina, GPU-bound. Um ganho em CPU não melhora um jogo GPU-bound. Use profiler de CPU e de GPU separados (V-13 cita Nsight, RGP, PIX e Xcode para GPU).
4. **Bisseção**: desligue metade das rotinas do quadro; se o custo cai, o gargalo está nessa metade; repita (V-13). Útil quando o profiler não aponta com clareza.
5. **Uma mudança por medição.** Meça de novo no mesmo cenário (mesma cena, mesmo caminho de câmera, mesmo número de objetos) antes e depois.
6. **Repetir em mais de um dispositivo**, sobretudo mobile (V-13).
7. Deep Profiling e instrumentação pesada distorcem os tempos; use-os para achar o quê, e um perfil leve para quanto (V-17).

Ferramentas por engine (nomes de painéis mudam por versão; confirme):

| Engine | Onde olhar | Status |
| --- | --- | --- |
| Godot 4 | Debugger > Profiler (CPU/scripts), Monitors, Visual Profiler (GPU); profilers externos de GPU | Verificado em V-13 para o fluxo; nomes dos painéis: Inferido |
| Unity | Profiler, Frame Debugger (batching), Project Auditor (alocações gerenciadas) | Verificado (V-17) |
| Unreal | `stat unit` e Unreal Insights | Não verificado (fora do VALIDATED) |

## Candidatos por engine

Tudo abaixo é candidato (análise estática). O profiler confirma.

### Qualquer engine

| Candidato | Sinal no código | Alternativa |
| --- | --- | --- |
| Alocação por quadro | `new`/lista/string criada em `_process`/`Update`/`Tick` | reusar buffer, pool, mover para fora do laço |
| Busca por quadro | `get_node`, `find_*`, `GetComponent`, `FindObjectOfType` no laço | guardar referência na inicialização |
| Muitos objetos com laço próprio | centenas de nós/componentes com `_process`/`Update` | um gerenciador que itera uma lista |
| Instanciar e destruir em rajada | spawn/queue_free/Destroy por tiro ou partícula | pool de objetos |
| Carga síncrona em gameplay | `load()`/`Resources.Load`/`LoadObject` durante a partida | carregar antes, em tela de carga ou assíncrono |
| Física desnecessária | colisores/raycast por quadro em tudo | camadas e máscaras, consultar só o necessário, ritmo menor |

### Godot 4

- `get_node()` ou `find_child()` dentro de `_process`: use `@onready` (V-11 pede filhos em `@onready` tipado).
- Lógica de movimento em `_process` com física: física em `_physics_process` (V-14); mover lógica que não é visual para o passo de física evita trabalho por quadro de render variável.
- Muitos `Node` com `_process` ativo: use `set_process(false)` quando ocioso (Inferido, API estável); considere um nó gerenciador.
- `TileMap` está deprecated; `TileMapLayer` é o substituto (V-32; a versão do depreciamento não foi confirmada).
- Documentação do Godot 3.5 não vale para o 4 (V-13).

### Unity

- Em `Update`/`FixedUpdate`: LINQ, concatenação de string, `GetComponent` por quadro, `Task.Result` (V-16). O manual 6000.0 diz "evitar" alocações, não "zero bytes" (V-16).
- Texto de HUD concatenado por quadro: atualize só quando o valor muda, ou use API de texto sem alocação do pacote de UI (Inferido; conferir o pacote em uso).
- `FindObjectsOfType` por quadro: caro; em versões recentes foi substituído por `FindObjectsByType` (Inferido, fora do VALIDATED); melhor ainda, manter uma lista registrada.
- `Vector3.Distance` em muitos pares: comparar `sqrMagnitude` evita a raiz (Inferido, estável).
- Project Auditor aponta alocações gerenciadas; Frame Debugger ajuda em batching (V-17).
- Finalizadores C# pesam no GC (V-16).

### Unreal

- Tick habilitado em todos os atores: desligue em atores que não precisam; use timers/eventos (Inferido, estável).
- Lambdas em timers capturando por referência: além de crash, geram trabalho inútil; use `CreateWeakLambda` (V-19).
- Ferramentas de medição: `stat unit`/Insights são Não verificados aqui; peça ao responsável o comando da versão.

## Exemplo de hotspots

| # | Onde | Por quê | Impacto | Esforço | Estado |
| --- | --- | --- | --- | --- | --- |
| 1 | `enemy.gd:14` `get_node("../Player")` em `_process` | busca de nó por quadro x 300 inimigos | provável | P | candidato (Inferido) |
| 2 | `hud.cs:41` `text = "HP: " + hp` em `Update` | string nova por quadro | provável | P | candidato (Inferido) |
| 3 | `spawner.gd:30` `instantiate()` por tiro | rajada de alocação | possível | M | candidato; decisão do usuário |
| 4 | frame time no build do alvo | - | - | - | NÃO AVALIADO (sem perfil) |

Veredito do exemplo: NÃO AVALIADO. Faltam orçamento em ms, perfil de CPU/GPU no alvo e build de teste.
