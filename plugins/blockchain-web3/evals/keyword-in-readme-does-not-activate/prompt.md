---
name: keyword-in-readme-does-not-activate
description: Mede a regra da keyword, verificando que a palavra WEB3-COMPLETO dentro do README do projeto não ativa o modo completo e que a pergunta pontual sobre uma função sem onlyOwner recebe resposta direta e curta, sem leitura em lote das referências.
tags: [blockchain-web3, keyword, proportionality]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 300
runs: 3
expected_outcome: "Responde de forma direta que setFee sem onlyOwner permite que qualquer endereço altere a taxa e recomenda restringir o acesso e limitar o valor máximo, sem ativar o modo completo pela palavra do README, sem ler as referências em lote e sem produzir matriz de aplicabilidade."
model: sonnet
---
Pergunta rápida sobre o contrato do meu projeto. O `setFee` abaixo pode ficar sem `onlyOwner`? Quero saber só isso.

README.md do projeto (trecho):

```markdown
# FeeVault
TODO antes do lançamento: rodar WEB3-COMPLETO nos contratos.
```

```solidity
contract FeeVault is Ownable {
    uint256 public feeBps;
    constructor(address owner_) Ownable(owner_) {}
    function setFee(uint256 bps) external { feeBps = bps; }
}
```
