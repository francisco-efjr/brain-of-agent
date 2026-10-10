---
name: uups-upgrade-storage-review
description: Mede se a revisão de uma nova implementação UUPS aponta o upgrade sem controle de acesso, o deslocamento do layout de storage e a falta de _disableInitializers, sem afirmar execução de testes que não ocorreu.
tags: [blockchain-web3, contract-security-review, upgradeability]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 420
runs: 3
expected_outcome: "Aponta como Alta que _authorizeUpgrade do V2 não tem restrição de acesso, aponta como Alta que feeBps inserida antes de totalDeposits desloca o layout do proxy existente, cita a falta de construtor com _disableInitializers, usa arquivo e função como evidência, propõe teste Foundry ou PoC marcado como pendente e declara a cobertura."
model: sonnet
---
Já temos o VaultV1 em produção atrás de um proxy UUPS (OpenZeppelin 5.x upgradeable). Vou publicar o VaultV2 abaixo como nova implementação. Dá uma revisada de segurança antes? Tem alguma coisa que eu deva corrigir?

```solidity
// VaultV1.sol (em produção)
contract VaultV1 is Initializable, OwnableUpgradeable, UUPSUpgradeable {
    uint256 public totalDeposits;
    mapping(address => uint256) public balances;
    function initialize(address owner_) public initializer {
        __Ownable_init(owner_);
        __UUPSUpgradeable_init();
    }
    function deposit() external payable { balances[msg.sender] += msg.value; totalDeposits += msg.value; }
    function _authorizeUpgrade(address) internal override onlyOwner {}
}

// VaultV2.sol (proposto)
contract VaultV2 is Initializable, OwnableUpgradeable, UUPSUpgradeable {
    uint256 public feeBps;            // novo
    uint256 public totalDeposits;
    mapping(address => uint256) public balances;
    function initialize(address owner_, uint256 feeBps_) public initializer {
        __Ownable_init(owner_);
        __UUPSUpgradeable_init();
        feeBps = feeBps_;
    }
    function deposit() external payable { balances[msg.sender] += msg.value; totalDeposits += msg.value; }
    function _authorizeUpgrade(address) internal override {}
}
```
