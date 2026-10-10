# Oráculo Chainlink e sequenciador de L2: leitura correta e testes

Fontes: Chainlink Data Feeds (using data feeds, API reference, L2 Sequencer Feeds) e Optimism "differences" (V-19, V-20), lidos em 2026-10-10. Docs de fornecedor mudam: confira a página atual do feed e a versão da interface antes de citar valores. Rótulos: **Verificado** = V-19/V-20; **Inferido** = exemplo de código e decisões do exemplo (não vêm da doc).

IDs: `W3-ORA-01` idade por `updatedAt`; `-02` `answer > 0` e `decimals()` do feed; `-03` endereço por rede e fallback/pausa; `-04` pool raso nunca fonte única; `-05` L2 (remete a `W3-L2-*`). `W3-L2-01` feed de uptime do sequenciador e carência; `-02` alias de endereço; `-03` taxa de dados L1; `-04` sem mempool público; `-05` finalidade.

## 1. O que a doc diz (Verificado)

- `latestRoundData()` devolve `roundId`, `answer`, `startedAt`, `updatedAt`, `answeredInRound`. `updatedAt` mede a idade da resposta. `answeredInRound` está marcado como obsoleto: não use como verificação.
- `latestAnswer()` não traz timestamp: sem como medir idade.
- `decimals()` é necessário para converter; leia do próprio feed.
- A página "Using Data Feeds" não traz checagem de idade, de preço positivo, heartbeat nem desvio; os exemplos são "não usar em produção".
- Em L2, consulte o feed de uptime do sequenciador: 0 = no ar, 1 = fora; reverta se fora; após o retorno, aplique um período de carência comparando `block.timestamp` com `startedAt` (exemplo da doc: 3600 s). Na Arbitrum, `startedAt` pode ser 0 se não inicializado. O status vem do L1 e pode atrasar.

## 2. Leitura incorreta (a que costuma aparecer em código copiado)

```solidity
function value(uint256 amount) external view returns (uint256) {
    (, int256 price,,,) = feed.latestRoundData();
    return amount * uint256(price) / 1e8;   // sem idade, sem sinal, escala fixa, cast de negativo
}
```
Problemas: preço velho passa (W3-ORA-01), `price <= 0` vira número gigante no cast ou zero (W3-ORA-02), `1e8` presume `decimals() == 8` (feeds de outros pares podem usar outro valor), nenhum tratamento de L2.

## 3. Leitura correta (Inferido: exemplo; confira nomes e versão da interface)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface AggregatorV3Interface {
    function decimals() external view returns (uint8);
    function latestRoundData() external view
        returns (uint80 roundId, int256 answer, uint256 startedAt, uint256 updatedAt, uint80 answeredInRound);
}

contract PriceReader {
    error InvalidPrice();
    error StalePrice(uint256 age);
    error SequencerDown();
    error GracePeriodNotOver();

    AggregatorV3Interface public immutable feed;
    AggregatorV3Interface public immutable sequencerUptimeFeed; // address(0) em L1
    uint256 public immutable maxAge;          // heartbeat do feed escolhido + margem; valor vem da página do feed
    uint256 public constant GRACE_PERIOD = 1 hours; // a doc usa 3600 s no exemplo; defina conforme o risco do protocolo

    constructor(address feed_, address sequencerFeed_, uint256 maxAge_) {
        feed = AggregatorV3Interface(feed_);
        sequencerUptimeFeed = AggregatorV3Interface(sequencerFeed_);
        maxAge = maxAge_;
    }

    /// @return preço escalado para 18 decimais
    function price() public view returns (uint256) {
        _checkSequencer();
        (, int256 answer,, uint256 updatedAt,) = feed.latestRoundData();
        if (answer <= 0) revert InvalidPrice();
        if (updatedAt == 0 || updatedAt > block.timestamp) revert InvalidPrice();
        uint256 age = block.timestamp - updatedAt;
        if (age > maxAge) revert StalePrice(age);
        uint8 d = feed.decimals();
        return d <= 18 ? uint256(answer) * 10 ** (18 - d) : uint256(answer) / 10 ** (d - 18);
    }

    function _checkSequencer() internal view {
        if (address(sequencerUptimeFeed) == address(0)) return;
        (, int256 status, uint256 startedAt,,) = sequencerUptimeFeed.latestRoundData();
        if (status != 0) revert SequencerDown();                         // 1 = fora
        if (startedAt == 0) revert GracePeriodNotOver();                 // estado não inicializado (V-20): decisão deste exemplo
        if (block.timestamp - startedAt <= GRACE_PERIOD) revert GracePeriodNotOver();
    }
}
```

Decisões embutidas (registre no ADR `adr-contrato.md`): reverter versus pausar versus usar fallback quando o feed falha. Reverter protege contra preço errado, mas pode impedir liquidações em momento de estresse e gerar dívida ruim; um segundo oráculo adiciona superfície. Não há resposta única: **Suposição** de engenharia, que o time deve decidir com o risco do protocolo à vista.

Combinação de dois feeds (por exemplo ETH/USD e USD/EUR): escale cada um para a mesma base antes de multiplicar e valide a idade dos dois com o seu próprio `maxAge`.

## 4. Como conferir o limite de idade sem inventar (W3-ORA-01)

1. Abra a página do feed escolhido na Chainlink (a página de cada feed lista o heartbeat e o desvio) e copie os valores para a definição de escopo, com a data da leitura.
2. `maxAge` deve ser pelo menos o heartbeat; a margem acima dele é decisão de risco registrada.
3. Se não conseguir abrir a página, escreva "heartbeat Não verificável" e peça ao usuário. Nunca use o heartbeat de outro par.
4. Feed diferente por rede: o endereço mainnet não vale em L2. Confira na lista oficial da rede.

## 5. Testes a propor (Foundry; sem executar)

Mock mínimo, com campos ajustáveis:

```solidity
contract MockAggregator {
    uint8 public decimals = 8;
    int256 public answer; uint256 public startedAt; uint256 public updatedAt;
    function set(int256 a, uint256 s, uint256 u) external { answer = a; startedAt = s; updatedAt = u; }
    function latestRoundData() external view returns (uint80, int256, uint256, uint256, uint80) {
        return (1, answer, startedAt, updatedAt, 1);
    }
}
```

Casos:

| Teste | Preparação | Esperado |
|---|---|---|
| `test_stalePriceReverts` | `set(2000e8, t, t)`; `vm.warp(t + maxAge + 1)` | `StalePrice` |
| `test_nonPositiveReverts` | `answer = 0` e `answer = -1` | `InvalidPrice` |
| `test_freshPriceScalesTo18` | `decimals = 8`, `answer = 2000e8` | `2000e18` |
| `test_sequencerDown` | feed de sequenciador com status 1 | `SequencerDown` |
| `test_gracePeriod` | status 0, `startedAt = block.timestamp - 10` | `GracePeriodNotOver` |
| `test_sequencerStartedAtZero` | status 0, `startedAt = 0` | `GracePeriodNotOver` (decisão do exemplo) |

Para fork de L2: `vm.createSelectFork(vm.rpcUrl("<alias>"))` com RPC em variável de ambiente (nunca o valor no repositório nem no chat). O sequenciador real só é "derrubado" em mock, nunca em rede viva.

## 6. Perguntas de L2 além do feed (W3-L2-02..05, Verificado em V-20)

- Contrato que identifica o chamador L1 por `msg.sender`/`tx.origin`: em depósitos L1 para L2 o endereço aparece com alias (endereço L1 mais um deslocamento fixo). Trate o alias.
- Estimativa de custo: além do gás de execução há taxa de dados L1; contrato que reembolsa gás ou cobra taxa fixa precisa considerá-la.
- Sem mempool público em OP Stack: proteção MEV pensada para mempool de L1 não se aplica da mesma forma; não pesquisei Arbitrum, Base nem zk rollups (lacuna L9).
- Finalidade: cabeças unsafe/safe/finalized; confirme a finalidade antes de liberar valor de alto risco ou ao consumir eventos.
- `block.number`, `block.timestamp`, precompiles e `PUSH0` em L2: a página do OP não cita (V-20); pesquise por rede e marque Não verificável até ler.
