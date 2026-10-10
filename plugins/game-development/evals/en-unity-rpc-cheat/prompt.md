---
name: en-unity-rpc-cheat
description: Caso de disparo em inglês. Revisão de RPC em Unity Netcode for GameObjects. Mede se a skill de netcode dispara por um pedido em inglês e se a resposta aponta o cliente informando preço e dano, dá cenário de abuso, separa o que é oficial do que é boa prática no Unity e não afirma ter testado.
tags: [game-development, game-netcode-review, unity, english, trigger]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Em inglês, identifica que os dois RPCs aceitam valores do cliente (preço e dano), descreve o abuso de cada um, propõe que o servidor derive preço de um catálogo e calcule o dano, trata RequireOwnership falso e a falta de limite de taxa, diz que validar RPC no Unity é boa prática e não regra da página de autoridade, recomenda teste com dois pares e não afirma ter executado nada."
model: sonnet
---
Can clients cheat in this Unity Netcode for GameObjects code? Quick review please.

```csharp
public class Shop : NetworkBehaviour
{
    public NetworkVariable<int> Gold = new NetworkVariable<int>(100);

    [ServerRpc(RequireOwnership = false)]
    public void BuyItemServerRpc(int itemId, int price, ServerRpcParams p = default)
    {
        Gold.Value -= price;
        Inventory.Add(itemId);
    }

    [ServerRpc]
    public void HitEnemyServerRpc(ulong enemyId, int damage)
    {
        NetworkManager.SpawnManager.SpawnedObjects[enemyId].GetComponent<Health>().Value -= damage;
    }
}
```
