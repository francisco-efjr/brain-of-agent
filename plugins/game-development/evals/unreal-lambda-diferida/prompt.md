---
name: unreal-lambda-diferida
description: Caso de revisão de C++ de Unreal Engine 5.8. Mede se o plugin aplica prefixo de classe, aponta UPROPERTY sem UCLASS como Inferido, lambda diferida com captura por referência, namespace em UCLASS e enum de Blueprint sem uint8, pede para confirmar headers e versão, declara os limites de cobertura e não afirma ter compilado.
tags: [game-development, unreal-cpp, unreal, cpp, epic-standard]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Aponta prefixo A para classe derivada de ACharacter, UPROPERTY em classe sem UCLASS e GENERATED_BODY como Inferido, lambda diferida capturando por referência (usar CreateWeakLambda ou TWeakObjectPtr), namespace em UCLASS, enum de Blueprint sem base uint8, pede para confirmar headers e versão, declara que Blueprints, GAS e replicação não estão cobertos e não afirma ter compilado."
model: sonnet
---
Unreal 5.8, C++. Revisa esse trecho:

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
