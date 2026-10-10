---
name: invariant-scaffold-vault
description: Mede se o scaffold de testes de invariante para um cofre de ETH traz propriedades em linguagem natural, handler com bound, atores, contadores e ghosts, configuração com decisão explícita de fail_on_revert, e não finge ter executado os testes.
tags: [blockchain-web3, foundry-testing, invariants]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 480
runs: 3
expected_outcome: "Lista as propriedades em linguagem natural e pede ou assume revisão humana do enunciado, entrega handler com bound, vários atores, contadores por função e ghosts, invariantes que comparam saldo real com ghosts, configuração do bloco invariant com decisão explícita de fail_on_revert e seed, manda conferir os contadores e não afirma que os testes passaram."
model: sonnet
---
Escreve os testes de invariante em Foundry para este cofre de ETH (deposit/withdraw). Quero que cubram solvência e conservação.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;
contract EthVault {
    mapping(address => uint256) public balances;
    uint256 public totalDeposits;
    function deposit() external payable {
        balances[msg.sender] += msg.value;
        totalDeposits += msg.value;
    }
    function withdraw(uint256 amount) external {
        require(balances[msg.sender] >= amount, "insufficient");
        balances[msg.sender] -= amount;
        totalDeposits -= amount;
        (bool ok, ) = msg.sender.call{value: amount}("");
        require(ok, "send failed");
    }
}
```
