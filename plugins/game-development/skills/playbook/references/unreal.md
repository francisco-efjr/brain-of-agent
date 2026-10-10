# Unreal Engine (C++)

Engine e versão-alvo: Unreal Engine 5.8 (página do padrão C++ da Epic, lida em 2026-10-10). Base: V-19, V-20, V-34. Cobertura **parcial**: nada foi lido sobre Blueprints, Gameplay Ability System (GAS), replicação detalhada nem Chaos Physics. Confira headers e a documentação da versão do projeto (`.uproject`, `EngineAssociation`) antes de afirmar API.

## Sumário

- [Padrão de código C++ da Epic](#padrão-de-código-c-da-epic)
- [Exemplo de revisão](#exemplo-de-revisão)
- [Onde cada dado mora](#onde-cada-dado-mora)
- [Formato de skill de engine](#formato-de-skill-de-engine)
- [Lacunas](#lacunas)

## Padrão de código C++ da Epic

Fonte: "Epic C++ coding standard for Unreal Engine" (V-19, classe A, UE 5.8).

| Regra | Detalhe |
| --- | --- |
| Prefixos | U (UObject), A (AActor), S (Slate), I (interface), C (conceito), T (template), E (enum), b (booleano), F (struct e demais) |
| UObject | passado por ponteiro |
| Lambdas diferidas | sem captura por referência de locais ou membros; use `CreateWeakLambda`/`CreateSPLambda` ou `TWeakObjectPtr`/`TWeakPtr`; comente quando se desviar |
| Enums para Blueprint | baseados em `uint8` |
| Namespaces | sem namespace em `UCLASS`/`USTRUCT` |

## Exemplo de revisão

Entrada (trecho de um pedido de revisão) e achados:

```cpp
class Player : public ACharacter {
  UPROPERTY() int Health;
  void StartRegen() {
    GetWorldTimerManager().SetTimer(Handle, FTimerDelegate::CreateLambda([&]() { Health += 5; }), 1.f, true);
  }
};
namespace Game { UCLASS() class UThing : public UObject { GENERATED_BODY() }; }
UENUM(BlueprintType) enum class EState { Idle, Run };
```

| # | Achado | Fonte | Correção |
| --- | --- | --- | --- |
| 1 | classe derivada de `ACharacter` deve ter prefixo `A` (`APlayer`) | V-19 | renomear |
| 2 | `UPROPERTY` em classe sem `UCLASS()`/`GENERATED_BODY()` não entra no sistema de reflexão | conhecimento estável do UE, Inferido | declarar `UCLASS()` e `GENERATED_BODY()` |
| 3 | lambda diferida com `[&]` captura `this`/membros por referência e pode rodar depois que o objeto morreu | V-19 | `CreateWeakLambda(this, ...)` ou captura de `TWeakObjectPtr` |
| 4 | `UCLASS` dentro de `namespace` | V-19 | remover o namespace |
| 5 | `UENUM(BlueprintType)` sem base `uint8` | V-19 | `enum class EState : uint8` |

Diga que não compilou nem testou se não houver build no ambiente ("Não verificável: sem build").

## Onde cada dado mora

Fonte: Gameplay Framework (V-20, classe A; paráfrase; versão da página não lida).

| Dado ou responsabilidade | Classe |
| --- | --- |
| Regras da partida (existe só no servidor; não persiste entre níveis) | GameMode |
| Placar e fase do jogo (replica do servidor aos clientes) | GameState |
| Vida e munição por jogador (replica) | PlayerState |
| Input humano; possui um Pawn | PlayerController |
| Corpo físico; Character é Pawn com cápsula e movimento | Pawn / Character |
| UI por jogador | HUD |
| Dados que sobrevivem a trocas de nível naquela máquina (existe em cada máquina; não replica) | GameInstance |

A página não detalha a replicação das demais classes; não assuma.

## Formato de skill de engine

Convenções do repositório de terceiros `quodsoler/unreal-engine-skills` (V-34, MIT, 363 estrelas, classe B; mira UE 5.8 e diz ter conferido headers, sem verificação independente): `name` igual à pasta; `description` começando com "Use when" com gatilhos e skill irmã; versão e engine declaradas; SKILL.md até 500 linhas; `references/` linkado; tabela "Deprecated, do not use" por skill com a versão que trocou a API. Neste plugin a engine e a versão ficam na primeira linha do corpo (o frontmatter do plugin não admite `metadata`).

## Lacunas

Blueprints, GAS, replicação de Actors e RPCs, Chaos Physics, ferramentas de profiling do Unreal (`stat unit` não verificado), pipeline de conteúdo, publicação. Peça a documentação da versão e rotule Suposição qualquer princípio geral aplicado.
