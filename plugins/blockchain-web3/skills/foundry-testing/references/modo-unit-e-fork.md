# Modo unit: testes unitários e de fork com Foundry

Rótulos: nenhum item de VALIDATED detalha cheatcodes de teste unitário. Tudo aqui é **Inferido** (conhecimento estável do Foundry/forge-std) e deve ser conferido na documentação oficial da versão instalada (`forge --version`). Apoio verificado: V-02 (fuzz, `bound`), V-04 e V-14 (RPC por variável de ambiente, PoC só em fork local), V-25 (`forge build` e `forge test` com saída colada).

## 1. Estrutura mínima

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Test} from "forge-std/Test.sol";
import {Vault} from "../src/Vault.sol";

contract VaultTest is Test {
    Vault vault;
    address alice = makeAddr("alice");
    address bob = makeAddr("bob");

    event Deposited(address indexed who, uint256 amount);

    function setUp() public {
        vault = new Vault();
        vm.deal(alice, 10 ether);
        vm.deal(bob, 10 ether);
    }

    function test_deposit_updatesBalance() public {
        vm.prank(alice);
        vault.deposit{value: 1 ether}();
        assertEq(vault.balances(alice), 1 ether);
    }

    function test_withdraw_revertsWithoutBalance() public {
        vm.prank(bob);
        vm.expectRevert(Vault.NoBalance.selector);   // vem antes da chamada que reverte
        vault.withdraw();
    }

    function test_deposit_emitsEvent() public {
        vm.expectEmit(true, false, false, true, address(vault)); // topic1, topic2, topic3, data, emissor
        emit Deposited(alice, 1 ether);                          // evento esperado
        vm.prank(alice);
        vault.deposit{value: 1 ether}();
    }
}
```

(O `Vault` do exemplo é o de `contract-security-review/references/exemplo-reentrancia-com-injecao.md` com o evento `Deposited` acrescentado; ajuste ao contrato real.)

## 2. Cheatcodes e helpers que mais se repetem

| Necessidade | Uso | Cuidado |
|---|---|---|
| Atuar como outra conta | `vm.prank(addr)` (próxima chamada) ou `vm.startPrank(addr)` / `vm.stopPrank()` | `prank` vale para uma chamada externa; leituras `view` entre `prank` e a chamada consomem o prank |
| Saldo de ETH | `vm.deal(addr, amount)` | Em fork, sobrescreve saldo local, não afeta a rede real |
| Saldo de token | `deal(address(token), addr, amount)` (forge-std) | Pode falhar com tokens de saldo não padrão (rebase, proxy) |
| Endereços rotulados | `makeAddr("alice")`, `vm.label(addr, "x")` | Aparecem nos traces (`-vvv`) |
| Reverter esperado | `vm.expectRevert(Err.selector)`; com argumento: `vm.expectRevert(abi.encodeWithSelector(Err.selector, arg))`; `require` com texto: `vm.expectRevert("msg")` | Precisa vir antes da chamada que reverte, e a próxima chamada externa é a verificada |
| Evento esperado | `vm.expectEmit(...)`, depois o `emit`, depois a chamada | Confira quais topics checar; indexados vs dados |
| Tempo e bloco | `vm.warp(timestamp)`, `vm.roll(block)` | `warp` não mexe em `block.number` |
| Cadeia | `vm.chainId(id)` | Útil em testes de replay (`wallet-signing-review`) |
| Logs | `console.log` (import `forge-std/console.sol`) | Aparecem com `-vv` |
| Gerar assinatura | `vm.sign(pk, digest)`, `vm.addr(pk)` | Só chaves de teste dentro do teste |

Convenção de nomes: `test_<Funcao>_<Comportamento>` para unitários e `testFuzz_<...>` para fuzz; para reverts, escolha uma convenção (`test_RevertWhen_<Condicao>` ou `test_<Funcao>_reverts<Motivo>`) e mantenha-a no projeto. `testFail` é obsoleto: use `vm.expectRevert`.

## 3. Teste de fork

Configuração em `foundry.toml` (o valor da URL vem da variável de ambiente do usuário; nunca no arquivo):

```toml
[rpc_endpoints]
mainnet = "${MAINNET_RPC_URL}"
base = "${BASE_RPC_URL}"
```

Teste:

```solidity
function setUp() public {
    vm.createSelectFork("mainnet", 20_000_000);   // bloco fixo: reprodutível; exemplo, escolha o seu
    // contratos reais podem ser lidos pelo endereço oficial confirmado em fonte oficial
}
```

Regras:

- Fork só local. Não envie transação para rede real; os testes de fork rodam em memória.
- Não leia o valor da variável; deixe o Foundry resolver o alias. Não imprima a URL (provedores embutem chave na URL).
- Se `MAINNET_RPC_URL` não estiver definida, o teste falha na criação do fork: diga isso e não tente "consertar" lendo `.env`.
- Personificar uma conta real (`vm.startPrank(whale)`) é válido em fork local para preparar estado, nunca como prova de que a transação seria aceita na rede real.
- Endereços de contratos de terceiros: confirme em fonte oficial (docs do protocolo, lista oficial); nunca invente endereço.

## 4. Fuzz como extensão do unitário

```solidity
function testFuzz_deposit_accumulates(uint96 a, uint96 b) public {
    a = uint96(bound(a, 1, 5 ether));
    b = uint96(bound(b, 1, 5 ether));
    vm.startPrank(alice);
    vault.deposit{value: a}();
    vault.deposit{value: b}();
    vm.stopPrank();
    assertEq(vault.balances(alice), uint256(a) + uint256(b));
}
```

`bound` mantém todas as execuções úteis; `vm.assume` descarta entradas e, com muitas rejeições, esgota `max_test_rejects`. Se a falha aparecer, o Foundry mostra o contraexemplo e a seed: copie os valores para um teste unitário de regressão.

## 5. Comandos

```bash
forge build
forge test --match-contract VaultTest -vvv     # traces das falhas
forge test --match-test test_withdraw -vvvv    # traces de tudo, para depurar
forge test --match-path "test/Vault*.t.sol"
```

Cole o comando e a saída reais no relatório. Zero testes executados é falso verde: confira a contagem na saída (`N tests passed`).

## 6. Checklist de revisão de testes existentes

- [ ] Cada revert esperado verifica o erro específico (não só "reverteu").
- [ ] Testes de acesso usam ator sem papel e ator com papel.
- [ ] Eventos conferidos nos fluxos que emitem.
- [ ] Nenhum teste depende de ordem de execução ou de estado de outro teste.
- [ ] Valores de borda (0, 1, máximo do tipo) cobertos ou fuzzados com `bound`.
- [ ] Testes de fork têm bloco fixo e RPC por variável de ambiente.
