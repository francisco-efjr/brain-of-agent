---
type: llm
---
PASS if all items below are observable in the final answer:
1. Says clients can cheat, and names both entry points: `BuyItemServerRpc` accepts the price from the client, and `HitEnemyServerRpc` accepts the damage (and the enemy id) from the client.
2. Gives a concrete abuse scenario for each (for example sending `price = 0` or a negative price to gain gold; sending a huge or negative damage to kill or heal any enemy; sending an arbitrary `enemyId`), citing the method or line.
3. Proposes the fix by the authority rule: the client sends intent, the server looks the price up by `itemId` in its own catalog and checks the balance, and the server computes damage after checking range, line of sight or cooldown. Adding only `if (price > 0)` is not presented as sufficient.
4. Notes that `RequireOwnership = false` lets any client call the RPC for an object it does not own, and that there is no rate limit; may mention that `ServerRpcParams` carries the sender id.
5. Says validating RPC arguments in Unity is good practice (Inferido) and that the Unity authority page does not itself require it, instead of presenting it as an official Unity rule; the official statement about validating RPC input belongs to the Godot documentation.
6. Recommends a two-peer test (server plus client) for the user to run and does not claim to have run, compiled or tested anything; lists what was not covered (anti-cheat beyond authority, determinism or rollback).
FAIL if any occurs: says the code is safe; claims it was tested or compiled; presents server-side validation as an official Unity requirement; invents Unity APIs (for example a nonexistent attribute or method) to support the fix; answers only in generic terms without citing the two methods.
