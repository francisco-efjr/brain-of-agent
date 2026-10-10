---
name: oracle-staleness-l2
description: Mede se a revisão do consumo de um feed Chainlink numa L2 aponta a ausência de checagem de idade por updatedAt, de preço positivo, de decimals do feed e do feed de uptime do sequenciador, sem inventar heartbeat.
tags: [blockchain-web3, defi-oracle-l2-review, oracle, l2]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 420
runs: 3
expected_outcome: "Aponta a falta de checagem de idade por updatedAt contra o heartbeat do feed sem inventar o valor, a falta de answer maior que zero, o uso de 1e10 fixo em vez de decimals, o tratamento de answeredInRound como obsoleto, a falta do feed de uptime do sequenciador com período de carência na Base, e não aprova o contrato."
model: sonnet
---
Meu contrato de empréstimo vai rodar na Base. A liquidação usa o preço ETH/USD do Chainlink como abaixo. Está certo? O que falta?

```solidity
contract Lending {
    AggregatorV3Interface public immutable feed; // ETH/USD
    function ethPrice() public view returns (uint256) {
        (uint80 roundId, int256 answer, , , uint80 answeredInRound) = feed.latestRoundData();
        require(answeredInRound >= roundId, "stale");
        return uint256(answer) * 1e10;
    }
    function liquidate(address user) external { uint256 p = ethPrice(); /* ... */ }
}
```
