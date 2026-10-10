---
name: erc4626-inflation-and-preview
description: Mede se a revisão de um cofre de shares aponta o ataque de inflação por doação, o uso de previewRedeem como preço, a não conformidade com a interface ERC-4626 e o retorno não checado de transferências de token.
tags: [blockchain-web3, token-standards-review, erc4626]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 420
runs: 3
expected_outcome: "Aponta o ataque de inflação com doação direta e a defesa por offset ou shares virtuais com teste, aponta que previewRedeem é manipulável e não serve como preço de colateral, diz que a interface ERC-4626 não está completa, aponta o retorno não checado de transferFrom e transfer e não afirma qual offset a biblioteca aplica sem ler a versão."
model: sonnet
---
Esse cofre segue o ERC-4626? Está seguro para receber depósitos de usuários e para ser usado como colateral pelo meu contrato de empréstimo (que usa previewRedeem como preço da share)?

```solidity
contract SimpleVault is ERC20 {
    IERC20 public immutable asset;
    constructor(IERC20 a) ERC20("Vault", "vSHR") { asset = a; }
    function totalAssets() public view returns (uint256) { return asset.balanceOf(address(this)); }
    function previewRedeem(uint256 shares) public view returns (uint256) {
        return totalSupply() == 0 ? shares : shares * totalAssets() / totalSupply();
    }
    function deposit(uint256 assets) external returns (uint256 shares) {
        uint256 supply = totalSupply();
        shares = supply == 0 ? assets : assets * supply / totalAssets();
        asset.transferFrom(msg.sender, address(this), assets);
        _mint(msg.sender, shares);
    }
    function redeem(uint256 shares) external returns (uint256 assets) {
        assets = previewRedeem(shares);
        _burn(msg.sender, shares);
        asset.transfer(msg.sender, assets);
    }
}
```
