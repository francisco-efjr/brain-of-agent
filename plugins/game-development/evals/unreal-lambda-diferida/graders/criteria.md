---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Aponta o prefixo: classe derivada de `ACharacter` (um `AActor`) leva `A` (por exemplo `APlayer`, ou nome mais descritivo com `A`).
2. Aponta que `UPROPERTY` em classe sem `UCLASS()` e `GENERATED_BODY()` não entra no sistema de reflexão, rotulando esse ponto como Inferido (conhecimento estável do motor, não texto da página do padrão de código).
3. Aponta a lambda diferida (timer) com captura por referência `[&]` de membro ou local e recomenda `CreateWeakLambda`/`CreateSPLambda` ou `TWeakObjectPtr`/`TWeakPtr`, com comentário quando houver desvio.
4. Aponta o namespace `Game` envolvendo um tipo `UCLASS` (sem namespace em tipos reflexivos) e o `UENUM(BlueprintType)` sem base `uint8`.
5. Pede para confirmar a versão e os headers antes de afirmar API; diz que Blueprints, GAS e replicação detalhada não estão cobertos; não afirma ter compilado nem executado ("Não verificável sem build").
6. Usa rótulos epistêmicos e referencia o trecho ou a linha em cada achado.
FAIL if qualquer um ocorrer: aprova o código; afirma uma API de memória como certa sem rótulo; diz que compilou ou testou; opina sobre Blueprints, GAS ou replicação como se tivesse fonte; ignora a lambda `[&]`.
