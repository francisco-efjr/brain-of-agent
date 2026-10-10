---
name: web3-completo-explicit
description: Mede o caso positivo da keyword WEB3-COMPLETO escrita pelo usuário, verificando que o modo é anunciado, que há matriz de aplicabilidade e registro de leitura, que as permissões não são ampliadas e que o gate não declara auditoria completa sem execução.
tags: [blockchain-web3, playbook, keyword, completo]
max_turns: 20
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 900
runs: 3
expected_outcome: "Reconhece o pedido explícito do modo WEB3-COMPLETO, delimita entrada e limites, registra leitura lida, parcial ou ausente das referências do plugin, entrega matriz de aplicabilidade por área com aplica, não aplica ou lacuna, faz a análise só como relatório sem alterar arquivos, não amplia permissões (sem ler .env, sem deploy), declara o gate Parcial por falta de execução de forge ou slither e inclui cobertura e handoff."
model: sonnet
---
WEB3-COMPLETO. Revise o cofre abaixo em modo só relatório, sem alterar nada. Não tenho forge nem slither instalados nesta máquina. Entregue a matriz, os achados com cobertura e o handoff.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
contract Staking {
    IERC20 public token;
    address public owner;
    mapping(address => uint256) public staked;
    constructor(IERC20 t) { token = t; owner = msg.sender; }
    function stake(uint256 a) external { token.transferFrom(msg.sender, address(this), a); staked[msg.sender] += a; }
    function unstake(uint256 a) external { staked[msg.sender] -= a; token.transfer(msg.sender, a); }
    function setToken(IERC20 t) external { token = t; }
}
```
