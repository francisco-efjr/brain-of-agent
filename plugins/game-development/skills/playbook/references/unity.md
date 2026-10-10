# Unity (C#)

Engine e versão-alvo: Unity 6000.0 (manual lido em 2026-10-10); 2022.3 LTS a conferir. Base: V-15, V-16, V-17, V-18, V-21, V-31, V-33. Fixe versão do Unity, pipeline de render (URP, HDRP, Built-in) e input (Input System ou legacy) antes de aplicar regra.

## Sumário

- [Regras de runtime C#](#regras-de-runtime-c)
- [Exemplo de revisão](#exemplo-de-revisão)
- [Profiling](#profiling)
- [ScriptableObjects](#scriptableobjects)
- [Testes](#testes)
- [Netcode for GameObjects](#netcode-for-gameobjects)
- [Unity-MCP no editor](#unity-mcp-no-editor)
- [Plugin oficial da Unity](#plugin-oficial-da-unity)
- [Deprecados e armadilhas](#deprecados-e-armadilhas)

## Regras de runtime C#

Fonte: manual 6000.0, "programming best practices" (V-16, classe A).

| Regra | Detalhe |
| --- | --- |
| Alocação por quadro | evite alocações em `Update`/`FixedUpdate`/`LateUpdate`. A página diz "avoid"; "zero bytes por quadro" não consta no manual 6000.0 (era do 2022.3) |
| LINQ e concatenação de string | evite em runtime, sobretudo por quadro |
| `GetComponent` | cacheie em `Awake`/`OnEnable` ou use referência serializada |
| Async | `Awaitable` no lugar de `Task`; nunca `Task.Result`/`Wait()` na thread principal (risco de deadlock) |
| Threads | nenhuma API de GameObject, Transform, componente ou asset fora da thread principal |
| Finalizadores C# | evite (rodam em outras threads e pesam no GC) |
| Destruição | `Object.Destroy` em runtime; `DestroyImmediate` só no editor |
| Estrutura | Assembly Definitions; Profiler, Project Auditor e analisadores Roslyn como ferramentas |

Conflito resolvido (K1): a comunidade recomenda UniTask; o manual oficial recomenda `Awaitable`. O plugin adota `Awaitable`; UniTask só se o projeto já o usa.

## Exemplo de revisão

Entrada (trecho com problemas) e a análise esperada. Itens 1 a 4 e 6 estão em V-16; o item 5 é conhecimento estável, rotulado Inferido.

```csharp
void Update() {
    var inimigos = FindObjectsOfType<Enemy>().Where(e => e.IsAlive).ToList();   // 1, 5
    var rb = GetComponent<Rigidbody>();                                          // 3
    hud.text = "HP: " + hp + "/" + maxHp;                                        // 2
}
async void Start() { var dados = Carregar().Result; }                            // 4
```

| # | Achado | Severidade | Correção |
| --- | --- | --- | --- |
| 1 | LINQ e `ToList()` por quadro alocam | média | manter lista de inimigos mantida por eventos de spawn e morte |
| 2 | concatenação de string por quadro | média | atualizar o texto só quando `hp` muda; formatar com buffer reutilizado |
| 3 | `GetComponent` por quadro | baixa | cachear em `Awake` |
| 4 | `.Result` na thread principal | alta (deadlock) | `await` com `Awaitable` |
| 5 | busca global por quadro; `FindObjectsOfType` foi substituído por `FindObjectsByType` nas versões recentes | média, Inferido | evitar busca por quadro; confirmar o nome na versão |

Antes de marcar como resolvido, abra o Profiler numa cena representativa (V-17). Sem ganho numérico prometido.

## Profiling

Fonte: Unity "best practices for profiling game performance" (V-17; a página não declara data de publicação). Meça tempo de quadro em ms (33,33 ms a 30 fps, 16,66 ms a 60 fps); perfile builds no dispositivo-alvo; o gargalo é a unidade ou thread mais lenta (CPU ou GPU); Deep Profiling distorce os tempos; em mobile deixe cerca de 35% do quadro livre; Project Auditor aponta alocações gerenciadas; Frame Debugger ajuda em batching. Método completo em `nucleo-tecnico.md`.

## ScriptableObjects

Fonte: Unity "architect game code with ScriptableObjects" (V-18, classe B; a página diz "Last updated January 2020", anterior ao Unity 6: **confira contra a documentação atual** antes de virar regra firme).

- Estado compartilhado entre sistemas em ScriptableObject (variável ou canal de evento), em vez de novo singleton.
- Ouvinte registra em `OnEnable` e remove em `OnDisable`.
- Edição em runtime persiste no asset **no editor**: separe valor inicial de valor de runtime.
- Projetos pequenos podem dispensar o padrão (comentário de terceiros, Inferido).

```csharp
[CreateAssetMenu(menuName = "Game/Int Variable")]
public class IntVariable : ScriptableObject {
    [SerializeField] int initialValue;
    [System.NonSerialized] public int Runtime;
    void OnEnable() => Runtime = initialValue;   // runtime não suja o asset
}
```

## Testes

Unity Test Framework 1.4.6, baseado em NUnit 3.5, exige Unity 2019.2 ou superior (V-21, classe A). EditMode para lógica pura; PlayMode para ciclo de vida. Rode pelo Test Runner ou pelo comando que o CLAUDE.md fixar. Linha de comando (Verificado na documentação do Test Framework 1.4, página `reference-command-line`, lida em 2026-10-10; não executado pelo plugin): `-runTests` roda os testes, `-testPlatform` escolhe `EditMode`, `PlayMode` ou um BuildTarget (sem ele, Edit Mode), `-testResults` define o XML NUnit de saída e `-batchmode` evita interação. Exemplo da documentação: `Unity.exe -runTests -batchmode -projectPath <pasta> -testResults <xml> -testPlatform <plataforma>`. Limitações documentadas: `UnityTest` não suporta WSA nem a maioria dos testes parametrizados, não suporta `Repeat`; fixtures aninhadas não rodam na interface; `Retry` em Play Mode lança `InvalidCastException` (a seção cita 1.3.x, trecho possivelmente desatualizado).

## Netcode for GameObjects

Fontes: páginas "authority" (2.7) e "ownership" (2.5) (V-15). Cada `NetworkObject` tem uma e somente uma autoridade; em cliente-servidor o servidor é a autoridade final sobre spawn e despawn (página de ownership); use `HasAuthority` por objeto (vale nas duas topologias; `IsServer` é a checagem tradicional só de cliente-servidor). A página de autoridade **não** manda validar ServerRpc nem trata `IsHost`: validar faixa, dono e frequência de RPC é boa prática (Inferido). Checklist em `checklist-completo.md`.

## Unity-MCP no editor

Fontes: CLAUDE.md do Unity-MCP (Apache-2.0 na página; mínimo Unity 2022.3) e o artigo "CLAUDE.md for Unity" de Devin Reimer, 26/02/2026 (V-31, classe B; o autor diz que as regras são subjetivas). Só vale com MCP de editor **aprovado pelo usuário** (ver `ferramentas-e-mcp.md`). Regras: chamadas da API Unity passam por `MainThread.Instance.Run()`; caminho do projeto sem espaços; durante a recompilação o MCP não responde, então confirme a conexão e leia `Editor.log` do disco; scripts temporários em `Editor/TemporaryGeneratedScripts`, apagados ao fim; GameObjects e prefabs por MCP, nunca editando YAML de cena ou prefab à mão; aprovação antes de apagar assets; evite `GetComponent`/`GetChild` em runtime; não suprima warning com `#pragma`. Sem MCP, a regra não vale.

## Plugin oficial da Unity

Blog da Unity, 09/09/2026 (V-33, classe B, promocional): 29 skills em 9 domínios (primeiros passos e CLI, UI e texto, 2D, gráficos e render, áudio, cena e gameplay, monetização, multiplayer, plataforma e localização) e `/unity-cli`. A página não cita MCP nem traz medição de ganho. Uso aqui: lista de domínios como checklist de cobertura; nenhuma regra derivada; nada instalado.

## Deprecados e armadilhas

- `FindObjectsOfType` -> `FindObjectsByType` em versões recentes (Inferido; confirme na versão).
- "Aspects" do ECS/Entities: Não verificado; não recomendar (V-35).
- Física (`FixedUpdate`, `Rigidbody`), Addressables, UI Toolkit, shaders/Shader Graph: sem fonte validada.
- Em 2022 LTS, confirme cada API de `Awaitable` e do manual 6000.0.
