# Foundry: testes unitários e de fork, fuzz, invariantes e gás

Itens V-02, V-23 e V-07 de [fontes.md](fontes.md). Conferido em 2026-10-10 contra as páginas oficiais de invariantes, fuzz, gás e configuração do Foundry e do otimizador do Solidity. Recursos recentes variam por versão: rode `forge --version` e confirme na documentação correspondente. Os exemplos são redação própria; nomes de cheatcodes de teste unitário são **Inferido** (conhecimento estável, não detalhados nas fontes validadas): confira no `Vm.sol` da versão instalada.

## Sumário

- [Regra de ouro](#regra-de-ouro)
- [Modo unit: testes unitários e de fork](#modo-unit-testes-unitários-e-de-fork)
- [Fuzz](#fuzz)
- [Invariantes (TST)](#invariantes-tst)
- [Configuração](#configuração)
- [Gás com evidência (GAS)](#gás-com-evidência-gas)
- [Riscos de execução: FFI](#riscos-de-execução-ffi)
- [Saída esperada do trabalho](#saída-esperada-do-trabalho)

## Regra de ouro

O LLM propõe propriedades e hipóteses; execução decide. Na média, fuzzing teve menor latência e menos falso positivo do que pedir a um LLM que ache bugs, e o LLM varia entre execuções (desvio de 7,5% numa tarefa específica relatada por Dan Luu). Por isso: o humano revisa o **enunciado das propriedades** (não o código gerado), o teste roda, a saída real é colada. Sem `forge` no ambiente, entregue os arquivos como "não executado".

## Modo unit: testes unitários e de fork

Padrões (cheatcodes **Inferido**, estáveis):

```solidity
// test/Vault.t.sol
import {Test} from "forge-std/Test.sol";

contract VaultTest is Test {
    Vault vault;
    address alice = makeAddr("alice");

    function setUp() public { vault = new Vault(); vm.deal(alice, 10 ether); }

    function test_withdraw_revertsWithoutBalance() public {
        vm.expectRevert(Vault.Insufficient.selector);
        vm.prank(alice);                    // próxima chamada vem de alice
        vault.withdraw(1 ether);
    }

    function test_deposit_emitsEvent() public {
        vm.expectEmit(true, false, false, true);  // topic1 indexado, data
        emit Vault.Deposited(alice, 1 ether);
        vm.prank(alice);
        vault.deposit{value: 1 ether}();
    }
}
```

- Um teste por comportamento; nome diz o comportamento (`test_withdraw_revertsWithoutBalance`).
- Controle de acesso: um teste com ator sem papel para cada função protegida (ACC-01).
- Teste de fork (somente leitura de estado real): `vm.createSelectFork(vm.envString("RPC_URL_NOME"))` com a URL na variável de ambiente; **cite o nome da variável, nunca o valor**. Fixe o número do bloco para reprodutibilidade quando o teste depender de estado.
- Teste de regressão: toda falha encontrada por fuzz/invariante vira teste determinístico com os argumentos que falharam.
- Sem transmissão de transações reais: testes rodam na EVM local ou em fork local. Deploy não é tarefa do agente ([seguranca-do-agente-e-chaves.md](seguranca-do-agente-e-chaves.md)).

## Fuzz

Fonte: página de fuzz do Foundry. Teste com parâmetros é fuzzado; 256 execuções por padrão. Em `[fuzz]`: `runs`, `max_test_rejects`, `seed` (e outras chaves; veja a página de configuração).

- Restrinja entradas com `bound(x, min, max)` em vez de `vm.assume()`: `assume` descarta a entrada e, em excesso, estoura `max_test_rejects` e reduz cobertura.
- `seed` fixo reproduz; registre-o no relatório.

```solidity
function testFuzz_deposit_increasesBalance(uint96 amount) public {
    amount = uint96(bound(amount, 1, 100 ether));
    vm.deal(alice, amount);
    vm.prank(alice);
    vault.deposit{value: amount}();
    assertEq(vault.balances(alice), amount);
}
```

## Invariantes (TST)

Fonte: página de invariantes do Foundry. Uma invariante é uma propriedade que vale após **qualquer sequência de chamadas** aos contratos-alvo (conservação, solvência, monotonicidade, limites, acesso).

### Estrutura

1. **Enunciado em linguagem natural** (template [especificacao-de-invariantes.md](../assets/templates/especificacao-de-invariantes.md)), revisado por um humano. Ex.: "O saldo de ETH do cofre é sempre ≥ soma dos saldos dos usuários."
2. **Handler**: contrato intermediário que expõe só ações válidas, limita entradas com `bound()`, usa **vários atores** e mantém **contadores por função** e variáveis **ghost**.
3. **Ghosts por fluxo de valor** (depósito, saque, taxa); a invariante compara o saldo real com os ghosts.
4. **Alvos**: `targetContract(address(handler))`, `targetSelector(...)`, `excludeSelector(...)` para limitar o universo de chamadas.
5. **`afterInvariant()`**: roda uma vez por rodada, no máximo um por contrato, e seu estado não persiste; use para checar contadores.

```solidity
contract VaultHandler is Test {
    Vault public vault;
    uint256 public ghostDeposited;
    uint256 public ghostWithdrawn;
    uint256 public calls_deposit;
    uint256 public calls_withdraw;
    address[] public actors;

    constructor(Vault v) {
        vault = v;
        for (uint160 i = 1; i <= 3; ++i) { actors.push(address(0xA11CE0 + i)); }
    }

    function deposit(uint256 seed, uint96 amount) external {
        address a = actors[seed % actors.length];
        amount = uint96(bound(amount, 1, 10 ether));
        vm.deal(a, amount);
        vm.prank(a);
        vault.deposit{value: amount}();
        ghostDeposited += amount; calls_deposit++;
    }

    function withdraw(uint256 seed, uint96 amount) external {
        address a = actors[seed % actors.length];
        uint256 bal = vault.balances(a);
        if (bal == 0) return;                       // ação inválida: não polui com revert
        amount = uint96(bound(amount, 1, bal));
        vm.prank(a);
        vault.withdraw(amount);
        ghostWithdrawn += amount; calls_withdraw++;
    }
}

contract VaultInvariants is StdInvariant, Test {
    Vault vault; VaultHandler handler;
    function setUp() public {
        vault = new Vault(); handler = new VaultHandler(vault);
        targetContract(address(handler));
    }
    function invariant_solvency() public view {
        assertEq(address(vault).balance, handler.ghostDeposited() - handler.ghostWithdrawn());
    }
    function afterInvariant() public view {   // prova de cobertura
        assertGt(handler.calls_deposit() + handler.calls_withdraw(), 0);
    }
}
```

### Cobertura: o ponto que mais engana

Invariante que nunca chama a função alvo não prova nada. Confirme nos **contadores** (ou nas métricas da versão instalada, se oferecidas) que cada função alvo foi chamada, e que a ação inválida não consome todas as rodadas. Relatório "passou" sem contadores é **Inferido**.

### `fail_on_revert` (TST-04)

A página só mostra `false` no exemplo, sem recomendar. A ideia de que `false` pode esconder falhas se o handler não restringe entradas é **Inferido**. Padrão deste plugin: handler restritivo (ações inválidas retornam cedo) e `fail_on_revert` escolhido **conscientemente**, com a lista de reverts esperados no relatório. Detalhe em [decisoes-e-tradeoffs.md](decisoes-e-tradeoffs.md) (T-02).

### Falha encontrada (TST-05)

Registre `runs`, `depth` e `seed`; rode de novo com outras seeds; use `-vvvv` para ver a sequência; transforme a sequência mínima em teste de regressão determinístico. Valores numéricos recomendados de `runs` e `depth`: **a página não os dá**; não os cite como recomendação.

## Configuração

Chaves documentadas na página de configuração de testes (2026-10-10): `[fuzz]` — `runs`, `timeout`, `fail_on_revert`, `max_test_rejects`, `seed`, `dictionary_weight`, `include_storage`, entre outras; `[invariant]` — `runs`, `depth`, `timeout`, `fail_on_revert`, `call_override`, `shrink_run_limit`, `max_assume_rejects`, `max_time_delay`, `max_block_delay`, `check_interval`, `show_metrics`, entre outras. `ffi` vale `false` por padrão. Exemplo ilustrativo (os números são do exemplo, não recomendação):

```toml
[profile.default.invariant]
runs = 256
depth = 128
fail_on_revert = false   # decisão documentada: o handler retorna cedo em ações inválidas
```

Recursos como `check_interval`, modo de otimização (`int256` a maximizar) e métricas dependem da versão do Foundry.

## Gás com evidência (GAS)

Fontes: página de gas tracking do Foundry e página do otimizador do Solidity; o repositório `decipher-gas-optimizoor` (sem licença) contribuiu **só a regra** de evidência, nada do texto.

| Comando | Para quê |
| --- | --- |
| `forge test --gas-report` | Tabela de gás por função |
| `forge snapshot` | Gera `.gas-snapshot` |
| `forge snapshot --diff` | Compara com o snapshot anterior |
| `forge snapshot --check` | Falha se um teste gastar mais (bom para CI) |
| `vm.startSnapshotGas` / `vm.stopSnapshotGas`, `pauseGasMetering` | Medição dentro do teste |

Regras:

1. **GAS-01** Toda alegação de economia vem com antes e depois do **mesmo teste** (`snapshot --diff` ou `--gas-report`). Sem medição não há número, nem "cerca de 30%".
2. **GAS-02** Ganho abaixo do limite acordado não entra. Combine o limite antes (a ferramenta de referência usa 500 gás no hook e 100 no relatório, como exemplos de prática; não é norma).
3. **GAS-03** Segurança não se troca por gás sem registro. `unchecked` só com prova de limite escrita.
4. **GAS-04** `optimizer_runs` (`--optimize-runs`) é uma **estimativa** de quantas vezes o opcode executa ao longo da vida do contrato (troca custo de deploy por custo de execução); **não é número de passes**. Escolha por perfil de uso e registre. O pipeline via-IR altera os resultados: meça com a configuração de produção.

Candidatos comuns (hipóteses a medir, não promessas): cachear `length` de array de storage em laço, erros customizados no lugar de strings de `require`, `immutable`/`constant`, `calldata` em vez de `memory` em parâmetros externos, empacotamento de variáveis de storage, visibilidade correta, eventos em vez de storage quando o dado só é lido off-chain.

## Riscos de execução: FFI

Com `ffi = true` em `foundry.toml` (ou `vm.ffi` nos testes), **rodar testes executa programas definidos no repositório**. A página de configuração confirma `ffi = false` por padrão e avisa que ligar permite executar programas arbitrários. Antes de `forge build`/`forge test` em código de terceiros ou não revisado: procure `ffi` em `foundry.toml` e `vm.ffi` em `test/`/`script/`; se houver, pare e peça confirmação ao usuário.

## Saída esperada do trabalho

Arquivos de teste; tabela `invariante · enunciado · cobertura por contadores · resultado · seed`; bloco de configuração; comandos executados com **saída colada**; lista de lacunas. Sem execução: "não executado" no topo, tudo **Não verificável**. Windows: instalação e comportamento de Foundry no ambiente do usuário não foram verificados aqui (lacuna L15); consulte a página oficial (WSL pode ser necessário: **Suposição**).
