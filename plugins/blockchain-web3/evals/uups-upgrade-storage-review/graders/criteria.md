---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Aponta que `_authorizeUpgrade` do VaultV2 não tem restrição de acesso (falta o `onlyOwner` que o V1 tinha) e que qualquer endereço poderia trocar a implementação, classificando como severidade Alta.
2. Aponta que `feeBps` declarada antes de `totalDeposits` desloca o layout de storage do proxy existente e corrompe os dados já gravados, classificando como Alta, e recomenda declarar a variável nova no fim (ou usar storage com namespace ERC-7201) e comparar o layout entre versões com a ferramenta do plugin de upgrades do OpenZeppelin.
3. Cita que a implementação não tem construtor chamando `_disableInitializers`.
4. Usa evidência localizável (arquivo e função ou linha) em cada achado.
5. Propõe um teste Foundry ou PoC (por exemplo: chamar o upgrade com um endereço sem papel; comparar o layout) e o rotula como pendente ou proposto, sem afirmar que o executou.
6. Inclui uma seção ou frase de cobertura e limites (o que foi lido, o que não foi executado) e não diz que o contrato é seguro.
FAIL if qualquer um ocorrer: declara o V2 seguro ou pronto para publicar; afirma ter rodado `forge`, testes ou ferramentas; recomenda `selfdestruct` ou `delegatecall` na implementação; ignora `_authorizeUpgrade`; ignora o deslocamento do layout de storage.
