# Núcleo técnico engine-agnóstico

Base: V-13, V-14, V-15, V-17 (2026-10-10). Textos de Nystrom e Fiedler têm licença não declarada: o conteúdo aqui é destilação com pseudocódigo próprio. Vale também para jogos web no nível de princípio (frameworks de jogo web e export HTML5 são lacuna sem fonte).

## Sumário

- [Game loop e timestep](#game-loop-e-timestep)
- [Física e movimento](#física-e-movimento)
- [Determinismo](#determinismo)
- [Performance: orçamento e método](#performance-orçamento-e-método)
- [Autoridade de rede](#autoridade-de-rede)
- [Lacunas](#lacunas)

## Game loop e timestep

Fontes: Robert Nystrom, *Game Programming Patterns*, capítulo Game Loop (classe B); Glenn Fiedler, "Fix Your Timestep" (publicado em 10/06/2004, classe B); introdução à física do Godot (classe A).

Problema: simulação atrelada ao tempo de quadro varia com a máquina e fica instável com passos grandes. Solução: **passo fixo para atualizar, renderização variável, interpolação**.

```
acumulador += min(tempo_do_quadro, TETO)      # TETO ~ 0,25 s (Fiedler) evita a espiral
processar_input()
iter = 0
enquanto acumulador >= PASSO e iter < MAX_ITER:
    simular(PASSO); acumulador -= PASSO; iter += 1
renderizar(acumulador / PASSO)                # alpha para interpolar estado anterior e atual
```

- **Teto no tempo de quadro:** sem ele, um quadro longo gera muitos passos, que levam mais tempo, que geram mais passos (a "espiral da morte"; o termo não aparece na página de Nystrom, o conceito sim).
- **Teto de iterações** do laço interno: Nystrom sugere limitá-las. Se estourar, descarte o excedente do acumulador em vez de acumular dívida.
- **Interpolação:** `estado_visual = lerp(estado_anterior, estado_atual, alpha)`; para rotações use slerp em quaternions (Fiedler).
- Escolha PASSO e valores (60 por segundo é o padrão de física do Godot) pelo projeto; não é lei.
- UI, câmera suave e efeitos puramente visuais rodam no quadro; lógica de gameplay que lê ou altera corpos físicos roda no passo fixo.
- O corte para Unity (`FixedUpdate`) e Unreal não foi lido: **Inferido**; confirme na documentação da versão antes de afirmar valores.

## Física e movimento

Godot (V-14, classe A): código que lê ou altera propriedades de corpo físico vai em `_physics_process`; o tick padrão é 60 por segundo; `move_and_slide()` já considera o passo, então não multiplique `velocity` por `delta`; gravidade é aceleração e usa `delta`; camadas e máscaras de colisão (32 camadas) devem estar documentadas no projeto.

Exemplo de movimento correto (GDScript, redação própria):

```gdscript
extends CharacterBody2D

@export var speed: float = 200.0
@export var gravity: float = 900.0

func _physics_process(delta: float) -> void:
    var dir := Input.get_vector("left", "right", "up", "down")
    velocity.x = dir.x * speed          # sem * delta
    velocity.y += gravity * delta       # aceleração usa delta
    move_and_slide()
```

Sintomas e causas comuns: personagem lento (velocidade multiplicada por `delta` com `_process`), treme na parede (movimento em `_process` com corpo físico), atravessa parede (velocidade muito alta por passo, colisão fina; reduza o passo ou use detecção contínua da engine, **Inferido**: confira o nome na versão).

## Determinismo

Mesma sequência de tempos e inputs produz o mesmo estado final. Teste: grave `--drive`, rode duas vezes, compare as saídas de `--probe`. É pré-requisito de replay e de lockstep. Não use `randf()` global sem semente fixa nos testes; registre a semente. Rollback e netcode determinístico não têm fonte validada.

## Performance: orçamento e método

Fontes: Unity "best practices for profiling game performance" (V-17, classe A); Godot "general optimization" (V-13, classe A); skill `perf-profile` do Donchitos (V-25, MIT, só o padrão).

1. **Orçamento primeiro.** Meça em milissegundos, não só FPS: a média esconde engasgos. Referências: 33,33 ms para 30 fps e 16,66 ms para 60 fps. O orçamento do **projeto** vem do config do projeto (fps alvo, memória, draw calls, tempo de carga, tamanho de build); 16,67 ms genérico não vale como orçamento do projeto. Estourar em menu ou carregamento é aceitável, em gameplay não.
2. **Hardware-alvo.** Meça em build no dispositivo-alvo, com V-Sync desligado. Em mobile deixe cerca de 35% do quadro livre (22 ms a 30 fps) para térmica e variação (V-17).
3. **CPU ou GPU.** O quadro é limitado pela unidade mais lenta; olhe profiler de CPU e de GPU separadamente (ferramentas de GPU: Nsight, RGP, PIX, Xcode, citadas pela doc do Godot).
4. **Bisseção.** Sem profiler claro, desligue metade das rotinas do quadro, meça, repita (busca binária).
5. **Uma mudança por medição**, remedindo o mesmo cenário. Deep Profiling (Unity) distorce tempos.
6. **Análise estática gera candidato; o profiler confirma.** Candidatos clássicos: alocação por quadro, busca de nó em `_process`, LINQ, `GetComponent` por quadro, muitos nós com `_process`.
7. **Veredito:** COMPLETO só com orçamento definido e dados de profiler no hardware-alvo; senão NÃO AVALIADO, com a lista do que faltou.

Exemplo de linha de relatório: `Gargalo: GPU-bound (CPU 6,1 ms, GPU 19,8 ms em 1080p, hardware X). Candidato: sombras dinâmicas. Ganho esperado: Inferido. Medir: desligar sombras e remedir a mesma cena.`

Unreal: use as ferramentas da engine para medir tempos por thread (por exemplo `stat unit`; **não verificado** neste plugin). Project Auditor e Frame Debugger são ferramentas Unity; não assuma em Godot.

## Autoridade de rede

Fontes: Unity NGO (autoridade e ownership) e Godot "high-level multiplayer" (V-15, classe A).

- Cada objeto de rede tem **uma e somente uma** autoridade. Em cliente-servidor, o servidor é a autoridade final sobre spawn e despawn (página de ownership).
- Estado autoritativo muda só em código de servidor; o cliente envia **intenção** (input), não resultado.
- Todo RPC valida faixa, dono e frequência antes de aplicar. No Godot isso é oficial (valide argumentos, limite a taxa de ações frequentes, não confie em posições, relógios ou recursos informados pelo cliente; `multiplayer.get_remote_sender_id()` identifica o chamador). No Unity é boa prática, **Inferido** (a página de autoridade não menciona validar RPC).
- Unity: `HasAuthority` checa autoridade por objeto e vale nas duas topologias; `IsServer` é a checagem tradicional só de cliente-servidor.
- Visual derivado localmente do estado sincronizado; previsão do cliente só com reconciliação.
- Teste de dois pares (servidor e cliente) antes de "pronto".

Exemplo de falha e correção (Godot, redação própria):

```gdscript
# Ruim: o cliente decide o resultado.
@rpc("any_peer")
func apply_damage(target_path: NodePath, amount: int): get_node(target_path).health -= amount

# Melhor: o cliente pede a ação; o servidor valida e calcula.
@rpc("any_peer", "call_remote", "reliable")
func request_attack(target_id: int) -> void:
    if not multiplayer.is_server(): return
    var sender := multiplayer.get_remote_sender_id()
    if not _can_attack(sender, target_id): return   # alcance, cooldown, dono, taxa
    _apply_damage(target_id, _damage_for(sender))   # dano vem de dados do servidor
```

## Lacunas

Replicação do Unreal, rollback e rede determinística, física em Unity (`FixedUpdate`, `Rigidbody`) e Unreal (Chaos), ECS/DOTS: sem fonte validada. Diga a lacuna, rotule Suposição e peça a documentação da versão.
