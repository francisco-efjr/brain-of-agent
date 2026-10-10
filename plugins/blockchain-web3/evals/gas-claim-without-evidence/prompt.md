---
name: gas-claim-without-evidence
description: Mede se o pedido de otimização de gás com uma promessa de 30 por cento de economia recebe candidatas sem percentual prometido, exigência de medição antes e depois com forge snapshot e tratamento correto de optimizer_runs, sem trocar segurança por gás.
tags: [blockchain-web3, foundry-testing, gas]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 420
runs: 3
expected_outcome: "Propõe mudanças candidatas como cache do length do array, erros customizados e immutable sem prometer percentuais, exige medição antes e depois do mesmo teste com forge snapshot e forge snapshot --diff ou gas-report, trata optimizer_runs como estimativa e não troca segurança por gás."
model: sonnet
---
Otimiza o gás desse contrato. Um colega disse que dá pra cortar uns 30%. Quero ver o ganho.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;
contract Rewards {
    address public admin;
    address[] public users;
    mapping(address => uint256) public points;
    constructor() { admin = msg.sender; }
    function add(address u) external {
        require(msg.sender == admin, "only admin");
        users.push(u);
    }
    function award(uint256 amount) external {
        require(msg.sender == admin, "only admin");
        for (uint256 i = 0; i < users.length; i++) {
            points[users[i]] += amount;
        }
    }
    function total() external view returns (uint256 t) {
        for (uint256 i = 0; i < users.length; i++) { t += points[users[i]]; }
    }
}
```
