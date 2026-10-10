---
name: eip712-replay
description: Mede se a revisão de uma função claim com assinatura off-chain do dono aponta replay por falta de nonce, validade, chainId e verifyingContract, recomenda domínio EIP-712 e teste de replay e rotula como suposição o que está fora da fonte validada.
tags: [blockchain-web3, wallet-signing-review, signatures]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 420
runs: 3
expected_outcome: "Aponta o replay da mesma assinatura em repetição, em outra cadeia e em outro contrato, a falta de nonce, validade, chainId e verifyingContract, recomenda domínio EIP-712 com nonce e deadline e teste de replay, afirma que EIP-712 sozinho não protege contra replay e rotula como suposição o que fala de malleabilidade ECDSA ou ERC-1271."
model: sonnet
---
O dono assina off-chain e o usuário envia a assinatura para sacar tokens. Esse `claim` está seguro?

```solidity
function claim(address to, uint256 amount, bytes calldata sig) external {
    bytes32 h = keccak256(abi.encodePacked(to, amount));
    address signer = ECDSA.recover(h, sig);
    require(signer == owner, "bad sig");
    token.transfer(to, amount);
}
```
