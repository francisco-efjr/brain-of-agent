# Unreal C++: padrão da Epic e Gameplay Framework

Sumário: [Prefixos](#prefixos) · [Regras com exemplos](#regras-com-exemplos) · [Lambda diferida](#lambda-diferida) · [Gameplay Framework](#gameplay-framework) · [Formato de skill de engine](#formato-de-skill-de-engine) · [Checklist de revisão](#checklist-de-revisão) · [Cobertura e lacunas](#cobertura-e-lacunas)

Fontes: V-19 (Epic C++ coding standard, UE 5.8, classe A), V-20 (Gameplay Framework, classe A), V-34 (quodsoler/unreal-engine-skills, MIT, classe B, só formato). Rótulos: Verificado (na página da Epic citada), Inferido (conhecimento estável do UE, fora do VALIDATED: confirme nos headers e na doc da versão), Não verificado. Código em redação própria (MIT do plugin), não compilado pelo plugin.

## Prefixos

| Prefixo | Uso | Exemplo |
| --- | --- | --- |
| `U` | classe derivada de `UObject` | `UInventoryComponent` |
| `A` | classe derivada de `AActor` (inclui `APawn`, `ACharacter`) | `APlayerCharacter` |
| `S` | widget Slate (`SWidget`) | `SInventoryGrid` |
| `I` | interface | `IInteractable` |
| `C` | conceito (C++20) | `CHasHealth` |
| `T` | template | `TArray`, `TWeakObjectPtr` |
| `E` | enum | `EMoveState` |
| `b` | variável booleana | `bIsDead` |
| `F` | demais classes e structs | `FDamageEvent` |

(V-19 lista U, A, S, I, C, T, E, b, F.) UObject é passado e guardado por ponteiro; a referência a `UObject*` em membro precisa de `UPROPERTY` para o GC enxergá-la (Inferido, estável).

## Regras com exemplos

Namespaces em tipos reflexivos (V-19): não permitidos.

```cpp
// Errado: namespace envolvendo UCLASS
namespace Game { UCLASS() class UThing : public UObject { GENERATED_BODY() }; }

// Certo: sem namespace; o prefixo e o nome do módulo desambiguam
UCLASS()
class MYGAME_API UThing : public UObject
{
    GENERATED_BODY()
};
```

Enum para Blueprint (V-19):

```cpp
UENUM(BlueprintType)
enum class EMoveState : uint8
{
    Idle,
    Run
};
```

Classe de Actor completa, com reflexão e membro tipado:

```cpp
// PlayerCharacter.h
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "PlayerCharacter.generated.h"

UCLASS()
class MYGAME_API APlayerCharacter : public ACharacter
{
    GENERATED_BODY()

public:
    void StartRegen();

protected:
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Stats")
    int32 Health = 100;

private:
    FTimerHandle RegenHandle;
};
```

Pontos (Inferido, estáveis, confirme nos headers da versão): `MYGAME_API` é a macro de exportação do módulo `MyGame`; `*.generated.h` entra por último na lista de includes; `UPROPERTY` em tipo reflexivo; `int32` em vez de `int` para propriedades; `Category` para expor no editor. Em UE 5, `TObjectPtr<T>` é recomendado para membros `UPROPERTY` de ponteiro para UObject (Inferido).

## Lambda diferida

Código com defeito (V-19): lambda diferida com captura por referência.

```cpp
GetWorldTimerManager().SetTimer(
    RegenHandle,
    FTimerDelegate::CreateLambda([&]() { Health += 5; }),   // captura por referência: o Actor pode ser destruído antes do timer
    1.0f, true);
```

Correção com delegate fraco (V-19: `CreateWeakLambda`/`CreateSPLambda` ou `TWeakObjectPtr`/`TWeakPtr`):

```cpp
void APlayerCharacter::StartRegen()
{
    GetWorldTimerManager().SetTimer(
        RegenHandle,
        FTimerDelegate::CreateWeakLambda(this, [this]() { Health += 5; }),
        1.0f, true);
}
```

`CreateWeakLambda(this, ...)` não executa o lambda se o objeto já foi destruído. Alternativa com ponteiro fraco explícito:

```cpp
TWeakObjectPtr<APlayerCharacter> WeakThis(this);
GetWorldTimerManager().SetTimer(RegenHandle, FTimerDelegate::CreateLambda([WeakThis]()
{
    if (APlayerCharacter* Self = WeakThis.Get()) { Self->Health += 5; }
}), 1.0f, true);
```

Se precisar se desviar do padrão (por exemplo, capturar por referência algo cujo tempo de vida é garantido), deixe um comentário dizendo por quê (V-19). Limpar o timer em `EndPlay` é complemento sensato (Inferido). Assinaturas de `SetTimer` e `CreateWeakLambda` variam por versão: confirme nos headers.

## Gameplay Framework

(V-20, paráfrase da página da Epic; a página não detalha a replicação das demais classes.)

| Classe | Papel | Detalhe |
| --- | --- | --- |
| GameMode | regras da partida | existe só no servidor; não persiste entre níveis |
| GameState | estado compartilhado da partida (placar, fase) | replica do servidor para os clientes |
| PlayerState | estado por jogador (vida, munição, nome) | replica |
| PlayerController | entrada do jogador | possui um Pawn |
| Pawn | representação física | Character é um Pawn com capsule e movimento |
| HUD | interface do jogador | por jogador |
| GameInstance | existe em cada máquina | não replica; vive enquanto o processo roda (Inferido) |

Decisões comuns:

- "Onde guardo a vida?" PlayerState quando a vida é do jogador e deve sobreviver ao respawn do corpo (Inferido); componente no Pawn quando a vida pertence ao corpo. Trade-off de design, registre em ADR curto se for decisão material (`adr-tecnico.md` do playbook).
- "Onde fica a condição de fim de partida?" GameMode (só servidor). O resultado a exibir vai para o GameState para os clientes verem.
- "Preciso de dado entre níveis?" GameInstance, sem esperar replicação; para multiplayer, replique o que importa por GameState/PlayerState.

Replicação (Actor replication, RPC, relevância) e GAS não foram lidos: não afirme regras de replicação. Para a parte conceitual de autoridade, use `game-netcode-review`.

## Formato de skill de engine

Convenções da skill de engine com versão declarada (V-34, adaptadas ao formato de plugin deste projeto):

- `name` igual à pasta; `description` começando com o que faz e quando usar, com gatilhos PT-BR e EN e a engine+versão. O `plugin-format-spec.md` do projeto não admite `metadata`: a versão-alvo vai na primeira linha do corpo.
- Tabela de APIs depreciadas com a versão que as trocou. O VALIDATED não traz API depreciada de Unreal verificada; por isso a tabela desta skill fica vazia em vez de preenchida de memória. Ao encontrar uma API substituída, confirme nos headers e no changelog da versão e registre a versão que a trocou.
- `references/` linkado direto do `SKILL.md`; corpo curto; avaliação com e sem a skill (V-08).

## Checklist de revisão

- [ ] versão do UE fixada (a página do padrão é da 5.8); headers conferidos antes de afirmar API
- [ ] prefixos corretos por tipo base (U, A, S, I, C, T, E, b, F)
- [ ] `UCLASS`/`USTRUCT` com `GENERATED_BODY()`; `UPROPERTY` só em tipo reflexivo; `int32` nas propriedades
- [ ] sem namespace em `UCLASS`/`USTRUCT`
- [ ] lambdas diferidas sem captura por referência; `CreateWeakLambda`/`CreateSPLambda` ou ponteiro fraco; desvio comentado
- [ ] enums de Blueprint com `uint8`
- [ ] dado no lugar certo do Gameplay Framework; nada de ler GameMode no cliente
- [ ] build/automação rodados e saída colada, ou "Não verificável: sem build"
- [ ] lacunas declaradas: Blueprints, GAS, replicação, Chaos

## Cobertura e lacunas

Coberto com fonte: padrão C++ da Epic (UE 5.8) e papéis das classes do framework. Sem fonte validada: Blueprints, Gameplay Ability System, replicação detalhada, Chaos Physics, ferramentas de profiling (`stat unit`, Insights), comando de automação por linha de comando, pipeline de assets, UI (UMG). Nesses temas, aplique só princípios gerais, rotule Suposição e diga a lacuna.
