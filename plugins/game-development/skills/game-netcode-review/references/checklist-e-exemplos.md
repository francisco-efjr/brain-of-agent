# Netcode: vetores de abuso, código corrigido e roteiro de teste

Sumário: [Vetores de abuso](#vetores-de-abuso) · [Godot: código corrigido](#godot-código-corrigido) · [Unity NGO: código corrigido](#unity-ngo-código-corrigido) · [Roteiro de teste de dois pares](#roteiro-de-teste-de-dois-pares) · [Cobertura e lacunas](#cobertura-e-lacunas)

Fontes: V-15 (Unity NGO autoridade 2.7 e ownership 2.5; Godot high-level multiplayer; classe A), V-14 (determinismo), V-36 (anti-padrões). Rótulos: Verificado (na doc citada), Inferido (boa prática ou conhecimento estável: confirme na versão), Suposição, Não verificável. Código em redação própria (MIT do plugin), não executado pelo plugin: rode com dois pares reais.

## Vetores de abuso

Procedência por linha: a coluna "Fonte" diz se é recomendação oficial (Verificado) ou análise (Inferido).

| Vetor | Como aparece no código | Abuso | Fonte |
| --- | --- | --- | --- |
| Posição do cliente | RPC recebe `pos` e aplica | teletransporte, atravessar parede | Godot: não confiar em posições do cliente (V-15) |
| Relógio do cliente | RPC recebe timestamp para cooldown ou animação | adiantar cooldown, trapacear ordem | Godot: não confiar em relógios (V-15) |
| Recurso do cliente | RPC recebe `price`, `gold`, `amount` | moeda infinita, dano arbitrário | Godot: não confiar em recursos (V-15) |
| Argumento sem validação | RPC sem checagem de faixa | valores negativos, NaN, infinito | Godot: validar argumentos (V-15) |
| Spam | RPC sem limite de frequência | negação de serviço, vantagem de cadência | Godot: limitar a taxa (V-15) |
| Remetente não checado | `any_peer` sem `get_remote_sender_id()` | agir em nome de outro jogador | Godot (V-15) |
| `NodePath`/id do cliente | `get_node(path)` com valor vindo do cliente | acessar ou destruir nó arbitrário | Inferido |
| Spawn pelo cliente | cliente instancia objeto de rede | itens, inimigos e projéteis forjados | Unity: servidor decide spawn/despawn (V-15) |
| Tamanho de payload | array ou string sem teto | uso excessivo de memória | Inferido |
| Segredo no cliente | chave de API ou senha embutida | vazamento do backend | Inferido (regra da casa: nenhum segredo em arquivos) |

## Godot: código corrigido

Princípios: servidor (peer 1) é a autoridade padrão; o cliente chama `rpc_id(1, ...)` com intenção; o servidor valida remetente, faixa, dono e frequência e calcula o resultado. `@rpc` aceita modo (`authority` ou `any_peer`), sincronização (`call_remote` ou `call_local`), modo de transferência (`reliable`, `unreliable`, `unreliable_ordered`) e canal; o padrão equivale a `authority`, `call_remote`, `reliable`, canal 0 (V-15). `multiplayer.get_remote_sender_id()` identifica quem chamou (V-15). Confirme as assinaturas na página da sua série do Godot (Inferido para o que não está em V-15).

Entrada de movimento (intenção, não posição):

```gdscript
var _inputs: Dictionary = {}          # peer_id -> Vector2
var _last_request_ms: Dictionary = {} # "peer:chave" -> ticks


@rpc("any_peer", "call_remote", "unreliable_ordered")
func submit_input(direction: Vector2) -> void:
	if not multiplayer.is_server():
		return
	var sender := multiplayer.get_remote_sender_id()
	if not _players.has(sender):                # peer desconhecido
		return
	if not direction.is_finite():               # NaN ou infinito
		return
	_inputs[sender] = direction.limit_length(1.0)   # módulo máximo 1; a velocidade é do servidor
```

Compra (preço vem do servidor, não do cliente):

```gdscript
@rpc("any_peer", "call_remote", "reliable")
func request_buy_item(item_id: String) -> void:
	if not multiplayer.is_server():
		return
	var sender := multiplayer.get_remote_sender_id()
	if not _allow(sender, "buy", 250):          # frequência mínima de 250 ms por peer
		return
	if not ItemCatalog.has_item(item_id):       # id desconhecido é recusado
		return
	var player := _players.get(sender) as PlayerData
	var price: int = ItemCatalog.price_of(item_id)
	if player == null or player.gold < price:
		return
	player.gold -= price
	player.inventory.append(item_id)
	_sync_inventory.rpc_id(sender, player.inventory)   # servidor informa o resultado


func _allow(peer_id: int, key: String, min_interval_ms: int) -> bool:
	var now := Time.get_ticks_msec()
	var k := "%d:%s" % [peer_id, key]
	if now - int(_last_request_ms.get(k, -min_interval_ms)) < min_interval_ms:
		return false
	_last_request_ms[k] = now
	return true
```

Ataque (intenção; o servidor decide o dano e o alvo):

```gdscript
@rpc("any_peer", "call_remote", "reliable")
func request_attack(target_id: int) -> void:
	if not multiplayer.is_server():
		return
	var sender := multiplayer.get_remote_sender_id()
	var attacker := _players.get(sender) as PlayerData
	var target := _entities.get(target_id) as Entity    # registro do servidor, não NodePath do cliente
	if attacker == null or target == null:
		return
	if not _allow(sender, "attack", attacker.attack_cooldown_ms):
		return
	if attacker.position.distance_to(target.position) > attacker.attack_range:
		return
	target.apply_damage(attacker.compute_damage())      # dano calculado no servidor
```

`_players`, `_entities`, `ItemCatalog`, `PlayerData`, `Entity` e `_sync_inventory` (um RPC `@rpc("authority", "call_remote", "reliable")` que o servidor chama em cada cliente) são nomes ilustrativos do jogo. Se `request_*` não for chamado pelo servidor localmente, as checagens `is_server()` são redundantes com `authority`; mantê-las é defesa em profundidade (Inferido). Em `any_peer`, sempre trate o remetente como não confiável.

O que não resolve: `if amount > 0` apenas. O cliente continua escolhendo o dano.

## Unity NGO: código corrigido

Versão: páginas lidas do NGO 2.5 (ownership) e 2.7 (autoridade). `[Rpc(SendTo.Server)]` e `RpcParams` são da API universal do 2.x (Inferido; no 1.x existiam `[ServerRpc]` e `ServerRpcParams`); métodos `[Rpc]` terminam em `Rpc` por convenção do pacote (Inferido). Confirme na versão instalada.

```csharp
using Unity.Netcode;
using UnityEngine;

public class PlayerNet : NetworkBehaviour
{
    private Vector2 pendingInput;

    // O cliente envia intenção; o servidor decide.
    [Rpc(SendTo.Server)]
    private void SubmitInputRpc(Vector2 direction, RpcParams rpcParams = default)
    {
        ulong sender = rpcParams.Receive.SenderClientId;
        if (sender != OwnerClientId) return;                     // só o dono controla este jogador
        if (!float.IsFinite(direction.x) || !float.IsFinite(direction.y)) return;
        pendingInput = Vector2.ClampMagnitude(direction, 1f);    // módulo máximo 1
    }

    private void FixedUpdate()
    {
        if (!HasAuthority) return;       // HasAuthority serve às duas topologias (V-15)
        // o servidor integra o movimento com a velocidade dele
    }
}
```

Notas:
- Cada `NetworkObject` tem uma e somente uma autoridade; em cliente-servidor o servidor tem a autoridade final sobre spawn e despawn (V-15). Spawn e despawn por RPC do cliente sem validação são achado de severidade Alta.
- Estado replicado via `NetworkVariable`: por padrão só o servidor escreve (Inferido); conceder escrita ao dono é decisão de design com risco (o dono passa a poder forjar o valor).
- Validação de RPC não consta na página de autoridade do Unity; é boa prática (Inferido). A documentação oficial do Godot é a que a recomenda (V-15).

## Roteiro de teste de dois pares

Para o usuário rodar (o plugin não executa; sem execução, o veredito de segurança é parcial):

1. Servidor e um cliente na mesma máquina ou em duas, com a versão exata do build de teste.
2. Normal: o cliente anda, ataca e compra; o servidor aplica e o cliente vê o resultado sincronizado.
3. Abuso 1: o cliente envia posição ou dano fora da faixa (modificando o cliente de teste ou um RPC de debug). Esperado: o servidor recusa, estado inalterado, log do motivo.
4. Abuso 2: frequência alta de RPCs (por exemplo 100 por segundo). Esperado: o servidor ignora o excedente.
5. Abuso 3: o cliente tenta agir em nome de outro jogador (id de outro peer). Esperado: recusado.
6. Abuso 4: id ou caminho inexistente. Esperado: recusado sem exceção no servidor.
7. Desconectar o cliente no meio de uma ação. Esperado: o servidor limpa o estado, sem objeto órfão.
8. Registre: comandos, saída do servidor, o que foi aceito e o que foi recusado. Item não executado fica NÃO AVALIADO.

## Cobertura e lacunas

Coberto com fonte: autoridade e ownership (Unity NGO), validação de RPC e confiança no cliente (Godot). Sem fonte validada: replicação de Unreal (Actor replication, RPC, relevância), rollback e netcode determinístico, lag compensation, anti-cheat avançado, infraestrutura de servidor dedicado. Nesses temas, aplique só o princípio geral, rotule Suposição e diga a lacuna (V-14, V-15).
