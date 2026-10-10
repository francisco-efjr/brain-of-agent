# Unity C#: regras de runtime e exemplos

Sumário: [Antes e depois](#antes-e-depois) · [Awaitable](#awaitable) · [ScriptableObject](#scriptableobject) · [Ciclo de vida](#ciclo-de-vida) · [Testes](#testes) · [Unity com MCP](#unity-com-mcp) · [Checklist de revisão](#checklist-de-revisão)

Fontes: V-16 (manual 6000.0), V-18 (ScriptableObjects, 2020), V-21 (Test Framework 1.4), V-31 (Unity-MCP, classe B), V-17 (profiling). Rótulos: Verificado (no manual citado), Inferido (conhecimento estável da API, fora do VALIDATED: confirme na versão do projeto), Não verificado. Código em redação própria (MIT do plugin), não compilado pelo plugin: compile e rode no projeto do usuário.

## Antes e depois

Antes (problemas numerados no comentário):

```csharp
void Update() {
    var inimigos = FindObjectsOfType<Enemy>().Where(e => e.IsAlive).ToList(); // 1 LINQ + busca global por frame
    var rb = GetComponent<Rigidbody>();                                         // 2 busca por frame
    hud.text = "HP: " + hp + "/" + maxHp;                                       // 3 string nova por frame
    foreach (var e in inimigos)
        if (Vector3.Distance(transform.position, e.transform.position) < 5f) Attack(e);
}
async void Start() { var dados = Carregar().Result; }                           // 4 bloqueia a thread principal
```

Depois:

```csharp
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class PlayerCombat : MonoBehaviour
{
    [SerializeField] private TMP_Text hud;
    [SerializeField] private float attackRange = 5f;

    private Rigidbody rb;          // cache (V-16)
    private int lastHp = -1;
    private int lastMaxHp = -1;

    private void Awake() => rb = GetComponent<Rigidbody>();

    private void Update()
    {
        RefreshHud();

        float sqrRange = attackRange * attackRange;
        Vector3 pos = transform.position;
        IReadOnlyList<Enemy> enemies = Enemy.Active;           // registro mantido por OnEnable/OnDisable
        for (int i = enemies.Count - 1; i >= 0; i--)           // laço reverso: Attack pode remover da lista
        {
            Enemy e = enemies[i];
            if (e.IsAlive && (e.transform.position - pos).sqrMagnitude < sqrRange)
                Attack(e);
        }
    }

    private void RefreshHud()
    {
        if (hp == lastHp && maxHp == lastMaxHp) return;         // só quando muda
        hud.SetText("HP: {0}/{1}", hp, maxHp);                  // formato sem concatenar string (Inferido: API do TextMeshPro)
        lastHp = hp; lastMaxHp = maxHp;
    }
}

public class Enemy : MonoBehaviour
{
    private static readonly List<Enemy> active = new();
    public static IReadOnlyList<Enemy> Active => active;

    private void OnEnable() => active.Add(this);
    private void OnDisable() => active.Remove(this);

    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]
    private static void ResetStatics() => active.Clear();       // Enter Play Mode sem recarregar domínio (Inferido)
}
```

O que mudou e por quê: sem LINQ nem lista nova por frame (V-16); `GetComponent` só em `Awake` (V-16); texto só quando o valor muda; `sqrMagnitude` evita a raiz quadrada (Inferido); registro em `OnEnable`/`OnDisable` troca a busca global. `hp`, `maxHp`, `Attack` e `Enemy.IsAlive` vêm do resto do código do usuário. `FindObjectsOfType` foi substituído por `FindObjectsByType` nas versões recentes (Inferido); o registro dispensa os dois. O ganho real se confirma no Profiler, não aqui.

## Awaitable

Padrão oficial do manual 6000.0 (V-16). Exemplo: ler/parsear um arquivo fora da thread principal e voltar para aplicar:

```csharp
private async Awaitable LoadAsync()
{
    await Awaitable.BackgroundThreadAsync();
    SaveData data = ParseSaveFile();        // sem tocar em GameObject, Transform ou assets (V-16)
    await Awaitable.MainThreadAsync();
    Apply(data);                            // API Unity só aqui
}

private void Start()
{
    _ = RunSafe(LoadAsync());
}

private async Awaitable RunSafe(Awaitable work)
{
    try { await work; }
    catch (System.Exception ex) { Debug.LogException(ex); }
}
```

Notas (Inferido; confirme `Awaitable` na versão): chamar sem `await` descarta a exceção, por isso o `try/catch`; `destroyCancellationToken` (propriedade de `MonoBehaviour` em versões recentes) permite cancelar quando o objeto é destruído; `Awaitable.NextFrameAsync()`, `WaitForSecondsAsync()` e `EndOfFrameAsync()` substituem corrotinas simples. Nunca `Task.Result` nem `.Wait()` na thread principal (deadlock). UniTask é opção de comunidade e só se o projeto já o usa.

## ScriptableObject

Estado compartilhado entre sistemas sem singleton novo (V-18; página de janeiro de 2020, padrão útil, confirme contra a documentação atual):

```csharp
using System;
using UnityEngine;

[CreateAssetMenu(menuName = "Game/Int Variable")]
public class IntVariable : ScriptableObject
{
    [SerializeField] private int initialValue;
    [NonSerialized] private int runtimeValue;   // runtime separado do inicial

    public event Action<int> Changed;
    public int Value
    {
        get => runtimeValue;
        set { runtimeValue = value; Changed?.Invoke(value); }
    }

    private void OnEnable() => runtimeValue = initialValue;
}
```

Canal de evento, com ouvinte registrado e removido (V-18):

```csharp
[CreateAssetMenu(menuName = "Game/Void Event Channel")]
public class VoidEventChannel : ScriptableObject
{
    public event Action Raised;
    public void Raise() => Raised?.Invoke();
}

public class DoorListener : MonoBehaviour
{
    [SerializeField] private VoidEventChannel channel;
    private void OnEnable()  => channel.Raised += OnRaised;
    private void OnDisable() => channel.Raised -= OnRaised;   // sem isso: vazamento e chamada em objeto destruído
    private void OnRaised() { /* abrir porta */ }
}
```

Cuidados: editar o asset em runtime no editor persiste no asset (por isso o valor de runtime separado do inicial); o comportamento de `OnEnable` em ScriptableObject e a recarga de domínio variam por configuração (Inferido); projeto pequeno pode dispensar o padrão.

## Ciclo de vida

| Callback | Use para | Evite |
| --- | --- | --- |
| `Awake` | inicializar a si mesmo, `GetComponent`, criar estruturas | depender de outros objetos já prontos |
| `OnEnable` | registrar eventos, entrar em listas | trabalho pesado |
| `Start` | usar referências a outros objetos (todos os `Awake` já rodaram) | cache que o objeto já poderia ter feito em `Awake` |
| `Update` | entrada, lógica visual por frame | alocação, LINQ, string, busca |
| `FixedUpdate` | física (`Rigidbody`) em passo fixo | entrada discreta isolada (pode perder quadros) |
| `LateUpdate` | câmera que segue, ajuste pós-animação | lógica de gameplay |
| `OnDisable` | desregistrar eventos, sair de listas | acessar objetos já destruídos |
| `OnDestroy` | liberar recursos nativos | `Destroy` em outros objetos sem checar |

(Tabela de conhecimento estável da API de MonoBehaviour: Inferido. O corte de `FixedUpdate` e física de Unity e Unreal não foi lido no VALIDATED, V-14.)

Erros típicos: `NullReferenceException` em `Start`/`Awake` costuma ser referência serializada não atribuída no Inspetor, ordem de inicialização entre objetos, ou `GetComponent` em objeto sem o componente; `MissingReferenceException` é acesso a objeto já destruído (ouvinte sem `OnDisable`, corrotina sobre objeto destruído). Reproduza com a sonda do `game-verify-by-running`, não por palpite.

## Testes

Unity Test Framework 1.4.6 (NUnit 3.5; Unity 2019.2+; V-21). EditMode para lógica pura, PlayMode para ciclo de vida:

```csharp
using NUnit.Framework;

public class DamageTests
{
    [TestCase(10, 10, 0)]
    [TestCase(11, 10, 1)]
    public void ComputeDamage_RespeitaPiso(int attack, int defense, int expected)
        => Assert.AreEqual(expected, Combat.ComputeDamage(attack, defense));
}
```

```csharp
using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;

public class EnemyPlayModeTests
{
    [UnityTest]
    public IEnumerator Enemy_RegistraEDesregistra()
    {
        var go = new GameObject("e");
        go.AddComponent<Enemy>();
        yield return null;
        Assert.AreEqual(1, Enemy.Active.Count);
        Object.Destroy(go);
        yield return null;
        Assert.AreEqual(0, Enemy.Active.Count);
    }
}
```

`Combat.ComputeDamage` é nome ilustrativo. Limitações de `UnityTest` (V-21): sem a maioria dos testes parametrizados, sem `Repeat`; `Retry` em Play Mode pode lançar `InvalidCastException` (trecho citado da 1.3.x). Os testes ficam em um assembly de teste (`Tests/EditMode`, `Tests/PlayMode`) criado pelo Test Runner. Linha de comando: `Unity.exe -runTests -batchmode -projectPath <pasta> -testPlatform EditMode|PlayMode -testResults <xml>` consta na documentação do Test Framework 1.4 (Verificado); não foi executado pelo plugin, então use o comando que o CLAUDE.md fixar e confira na sua versão.

## Unity com MCP

Só quando o projeto aprovou Unity-MCP (V-31, classe B; Apache-2.0 na página, mínimo Unity 2022.3). Nada é instalado por esta skill; o JSON de instalação não está no VALIDATED, então não o invente: leia o README do projeto antes.

- Confirmar o status da conexão antes de agir.
- Chamadas da API Unity passam por `MainThread.Instance.Run()`.
- Editor compilando: o MCP não responde; aguarde e leia `Editor.log` do disco.
- Scripts temporários em `Editor/TemporaryGeneratedScripts`, apagados ao fim da tarefa.
- GameObjects e prefabs via MCP, nunca por YAML à mão; sem suprimir warning com `#pragma`.
- Pedir aprovação antes de apagar assets. O repositório cita `start_mcp_inspector.bat`: não executar sem aprovação.
- Regras de Devin Reimer (26/02/2026) são subjetivas, segundo o próprio autor: tratar como sugestão.

## Checklist de revisão

- [ ] versão do Unity, pipeline e entrada conhecidos; APIs do 6000.0 conferidas se for 2022 LTS
- [ ] sem LINQ, string concatenada, `new` de coleção, closure nova em `Update`/`FixedUpdate`
- [ ] `GetComponent` em `Awake`/`OnEnable` ou referência serializada
- [ ] `Awaitable`, sem `Task.Result`/`.Wait()`; sem API Unity fora da thread principal
- [ ] eventos registrados em `OnEnable` e removidos em `OnDisable`
- [ ] `Destroy` em runtime; `DestroyImmediate` só no editor
- [ ] estáticos mutáveis limpos para Enter Play Mode sem recarga de domínio
- [ ] valores de gameplay em ScriptableObject/dados, não fixos
- [ ] testes EditMode/PlayMode ou "Não verificável"; Profiler numa cena representativa antes de "ok"
