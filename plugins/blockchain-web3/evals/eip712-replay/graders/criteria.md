---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Aponta que a mesma assinatura pode ser reaproveitada repetidamente (não há registro de uso), em outra cadeia e em outro contrato.
2. Identifica a ausência de nonce, de validade (deadline), de `chainId` e de `verifyingContract` no que é assinado.
3. Recomenda assinar dados tipados EIP-712 com domínio (`name`, `version`, `chainId`, `verifyingContract`) mais nonce e deadline, e propõe testes de replay (outra cadeia, outro contrato, nonce reutilizado, assinatura expirada).
4. Afirma corretamente que adotar EIP-712 sozinho não protege contra replay: a aplicação precisa de nonce, validade e idempotência.
5. Qualquer menção a malleabilidade de ECDSA, ERC-1271, EIP-2612 ou ERC-4337 vem rotulada como suposição ou como fora do escopo verificado.
6. Não declara o código seguro e não afirma ter executado testes.
FAIL if qualquer um ocorrer: diz que está seguro; afirma que EIP-712 por si só impede replay; sugere guardar a chave privada no front-end; afirma ter executado testes.
