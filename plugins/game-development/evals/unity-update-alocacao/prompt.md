---
name: unity-update-alocacao
description: Caso de revisão de C# de runtime no Unity. Mede se o plugin aponta LINQ, ToList, concatenação de string e GetComponent por frame, Task.Result na thread principal e busca global por frame (esta como Inferido), recomenda Awaitable sem impor UniTask, manda confirmar no Profiler no aparelho e não promete ganho numérico.
tags: [game-development, unity-csharp, unity, allocation, async]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Lista os achados com trecho ou linha e rótulos (LINQ e ToList por frame, string concatenada por frame, GetComponent por frame, busca global por frame como Inferido, Task.Result na thread principal), recomenda Awaitable como padrão do manual, manda perfilar em build no aparelho Android, não promete percentuais e declara que não executou."
model: sonnet
---
Unity 6, URP, o jogo roda num Android intermediário e dá stutter. Esse script de ataque é o suspeito, revisa:

```csharp
void Update() {
    var inimigos = FindObjectsOfType<Enemy>().Where(e => e.IsAlive).ToList();
    var rb = GetComponent<Rigidbody>();
    hud.text = "HP: " + hp + "/" + maxHp;
    foreach (var e in inimigos)
        if (Vector3.Distance(transform.position, e.transform.position) < 5f) Attack(e);
}
async void Start() { var dados = Carregar().Result; }
```
