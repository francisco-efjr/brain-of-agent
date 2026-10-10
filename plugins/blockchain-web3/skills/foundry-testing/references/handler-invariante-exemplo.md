# Exemplo completo: handler, ghosts, contadores e invariantes

Padrão de V-02 (Foundry, Verificado): contrato handler que limita entradas e mantém variáveis ghost; `bound()` em vez de `vm.assume()`; `targetContract`/`targetSelector`/`excludeSelector`; contadores por seletor para provar cobertura. O código abaixo é exemplo próprio (**Inferido**: sintaxe de forge-std e do OpenZeppelin 5.x; confira as versões instaladas). Contrato didático; os valores numéricos são ilustrativos.

## 1. Contrato sob teste (`src/SimpleVault.sol`)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

contract SimpleVault {
    using SafeERC20 for IERC20;

    error ZeroAmount();
    error Insufficient();

    IERC20 public immutable asset;
    mapping(address => uint256) public balanceOf;
    uint256 public totalDeposits;

    constructor(IERC20 asset_) { asset = asset_; }

    function deposit(uint256 amount) external {
        if (amount == 0) revert ZeroAmount();
        balanceOf[msg.sender] += amount;
        totalDeposits += amount;
        asset.safeTransferFrom(msg.sender, address(this), amount);
    }

    function withdraw(uint256 amount) external {
        if (amount == 0) revert ZeroAmount();
        if (balanceOf[msg.sender] < amount) revert Insufficient();
        balanceOf[msg.sender] -= amount;
        totalDeposits -= amount;
        asset.safeTransfer(msg.sender, amount);
    }
}
```

## 2. Propriedades em linguagem natural (para o humano aprovar antes do código)

1. Solvência: o cofre sempre tem em tokens pelo menos o que registra dever (`totalDeposits`).
2. Consistência: a soma dos saldos individuais é igual a `totalDeposits`.
3. Conservação: o saldo em tokens do cofre é igual ao depositado menos o sacado mais o doado diretamente.

Propriedade nova a cada função nova; peça confirmação do enunciado ao usuário (V-07, item 5).

## 3. Mock e handler (`test/handlers/VaultHandler.sol`)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Test} from "forge-std/Test.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {SimpleVault} from "../../src/SimpleVault.sol";

contract MockERC20 is ERC20 {
    constructor() ERC20("Mock", "MOCK") {}
    function mint(address to, uint256 amount) external { _mint(to, amount); }
}

contract VaultHandler is Test {
    SimpleVault public vault;
    MockERC20 public asset;

    address[] public actors;
    address internal current;

    // ghosts: fluxo de valor
    uint256 public ghostDeposited;
    uint256 public ghostWithdrawn;
    uint256 public ghostDonated;

    // contadores de chamadas bem-sucedidas por seletor
    mapping(bytes4 => uint256) public calls;

    constructor(SimpleVault vault_, MockERC20 asset_) {
        vault = vault_;
        asset = asset_;
        for (uint256 i = 0; i < 3; ++i) {
            actors.push(makeAddr(string.concat("actor", vm.toString(i))));
        }
    }

    modifier useActor(uint256 seed) {
        current = actors[bound(seed, 0, actors.length - 1)];
        vm.startPrank(current);
        _;
        vm.stopPrank();
    }

    function deposit(uint256 seed, uint256 amount) external useActor(seed) {
        amount = bound(amount, 1, 1_000_000e18);
        asset.mint(current, amount);
        asset.approve(address(vault), amount);
        vault.deposit(amount);
        ghostDeposited += amount;
        calls[this.deposit.selector]++;
    }

    function withdraw(uint256 seed, uint256 amount) external useActor(seed) {
        uint256 bal = vault.balanceOf(current);
        if (bal == 0) return;                       // sem saldo: nada a sacar (não é revert)
        amount = bound(amount, 1, bal);
        vault.withdraw(amount);
        ghostWithdrawn += amount;
        calls[this.withdraw.selector]++;
    }

    function donate(uint256 seed, uint256 amount) external useActor(seed) {
        amount = bound(amount, 1, 1_000e18);
        asset.mint(current, amount);
        asset.transfer(address(vault), amount);     // doação direta, fora de deposit()
        ghostDonated += amount;
        calls[this.donate.selector]++;
    }

    function actorsLength() external view returns (uint256) { return actors.length; }
}
```

Por que assim: `bound` mantém toda execução útil; vários atores cobrem acesso cruzado; o modelo inclui `donate` porque tokens chegam ao cofre sem passar por `deposit` (cenário real de inflação em cofres); `return` com saldo zero evita revert artificial; contadores contam só chamadas que completaram.

## 4. Teste de invariantes (`test/Vault.invariants.t.sol`)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Test} from "forge-std/Test.sol";
import {StdInvariant} from "forge-std/StdInvariant.sol";
import {console} from "forge-std/console.sol";
import {SimpleVault} from "../src/SimpleVault.sol";
import {VaultHandler, MockERC20} from "./handlers/VaultHandler.sol";

contract VaultInvariants is StdInvariant, Test {
    SimpleVault vault;
    MockERC20 asset;
    VaultHandler handler;

    function setUp() public {
        asset = new MockERC20();
        vault = new SimpleVault(asset);
        handler = new VaultHandler(vault, asset);

        targetContract(address(handler));
        bytes4[] memory selectors = new bytes4[](3);
        selectors[0] = handler.deposit.selector;
        selectors[1] = handler.withdraw.selector;
        selectors[2] = handler.donate.selector;
        targetSelector(FuzzSelector({addr: address(handler), selectors: selectors}));
    }

    // 1) solvência
    function invariant_solvency() public view {
        assertGe(asset.balanceOf(address(vault)), vault.totalDeposits());
    }

    // 2) consistência
    function invariant_sumOfBalancesEqualsTotal() public view {
        uint256 sum;
        for (uint256 i = 0; i < handler.actorsLength(); ++i) {
            sum += vault.balanceOf(handler.actors(i));
        }
        assertEq(sum, vault.totalDeposits());
    }

    // 3) conservação com ghosts
    function invariant_conservation() public view {
        assertEq(
            asset.balanceOf(address(vault)),
            handler.ghostDeposited() - handler.ghostWithdrawn() + handler.ghostDonated()
        );
    }

    // cobertura: resumo de chamadas bem-sucedidas ao fim de cada rodada (leia com -vv; confira a versão do Foundry)
    function afterInvariant() public view {
        console.log("deposit", handler.calls(handler.deposit.selector));
        console.log("withdraw", handler.calls(handler.withdraw.selector));
        console.log("donate", handler.calls(handler.donate.selector));
    }
}
```

Comando: `forge test --match-contract VaultInvariants -vvv`. Registre `forge --version`, `runs`, `depth`, `fail_on_revert` e `seed` (ver [foundry-toml-e-comandos.md](foundry-toml-e-comandos.md)).

## 5. Como provar que o teste não é vazio

1. Contadores: `deposit`, `withdraw` e `donate` devem aparecer com chamadas bem-sucedidas maiores que zero na saída de `afterInvariant()` (roda uma vez por rodada e seu estado não persiste). Se a saída não aparecer na sua versão, use o resumo por seletor que versões recentes do Foundry imprimem (Inferido: confirme na versão instalada).
2. Mutação temporária (em cópia do contrato ou revertida logo depois): remova a linha `totalDeposits -= amount;` de `withdraw`. Esperado: `invariant_sumOfBalancesEqualsTotal` e `invariant_solvency` caem depois de uma sequência `deposit` seguida de `withdraw`. Se nada cair, o handler não alcança o ponto ou a propriedade é fraca (Inferido: boa prática de verificação).
3. Falha reproduzida: `forge test --match-test invariant_sumOfBalancesEqualsTotal -vvvv` mostra a sequência; copie-a para um teste unitário de regressão com valores concretos.

## 6. Pontos de atenção

- Funções públicas do handler que não são ações (ajudantes) viram alvo se você não restringir; `targetSelector` evita isso.
- Handler com `vm.assume` desperdiça execuções; use `bound`.
- `fail_on_revert = true` pede que toda ação do handler seja válida; com `false`, só os contadores dizem se o handler funciona.
- Adicione ações conforme o contrato cresce (liquidação, taxa, pausa); cada função de estado sem ação no handler é uma lacuna de cobertura a registrar.
- Para cofres ERC-4626, reaproveite o handler com `donate` e adicione a invariante de arredondamento (ver `token-standards-review`).
