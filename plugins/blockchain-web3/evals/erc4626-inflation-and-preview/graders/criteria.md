---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Descreve o ataque de inflação ou doação: primeiro depositante com quantia mínima (por exemplo 1 wei) seguido de doação direta de ativos ao cofre faz depósitos de outras pessoas arredondarem para zero shares; propõe defesa (shares/ativos virtuais com offset de precisão, ou depósito inicial morto) e um teste (atacante doa, vítima deposita, perda limitada).
2. Diz que `previewRedeem` (e `preview*` em geral) é manipulável por doação e não deve ser usado como preço ou colateral pelo contrato de empréstimo; não aprova esse uso.
3. Diz que o contrato não implementa a interface ERC-4626 completa (faltam, por exemplo, `convertToShares`, `convertToAssets`, `max*`, `mint`, `withdraw`, `previewDeposit`, eventos `Deposit` e `Withdraw`) e que a resposta à pergunta "segue o ERC-4626?" é não.
4. Aponta que o retorno de `transferFrom` e `transfer` não é verificado (uso de `SafeERC20`) ou que há efeito antes da interação em `deposit`.
5. Não afirma qual offset de precisão a implementação base do OpenZeppelin aplica sem dizer que depende da versão instalada.
6. Não afirma ter executado testes e inclui cobertura ou limites.
FAIL if qualquer um ocorrer: declara conformidade com a EIP-4626; ignora a inflação; usa `preview*` como preço sem ressalva; afirma ter rodado `forge`.
