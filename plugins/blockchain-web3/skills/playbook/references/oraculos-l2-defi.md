# Oráculos, L2, hooks do Uniswap v4 e cenários de incidente

Itens V-17, V-18, V-19 e V-20 de [fontes.md](fontes.md); IDs em [checklist-completo.md](checklist-completo.md). A documentação de fornecedor (Chainlink, Optimism) muda: **antes de citar endereço de feed, heartbeat ou parâmetro de rede, abra a página do feed e da rede na data da revisão**. Este plugin não inventa esses valores.

## Sumário

- [Consumo seguro de preço Chainlink (ORA)](#consumo-seguro-de-preço-chainlink-ora)
- [L2: sequenciador e OP Stack (L2)](#l2-sequenciador-e-op-stack-l2)
- [Hooks do Uniswap v4 e tokens atípicos (HOOK)](#hooks-do-uniswap-v4-e-tokens-atípicos-hook)
- [Cenários de incidente como perguntas (SCN)](#cenários-de-incidente-como-perguntas-scn)
- [Fora da cobertura](#fora-da-cobertura)

## Consumo seguro de preço Chainlink (ORA)

Fatos conferidos nas páginas oficiais (2026-10-10):

- `latestRoundData` devolve `roundId`, `answer`, `startedAt`, `updatedAt`, `answeredInRound`.
- `updatedAt` serve para medir a **idade** da resposta. `answeredInRound` está marcado como **obsoleto: não usar**. Guias de auditoria antigos mandam checá-lo; a doc atual prevalece (veja [decisoes-e-tradeoffs.md](decisoes-e-tradeoffs.md), T-11).
- `latestAnswer()` não traz timestamp.
- `decimals()` é necessário para converter.
- A página "Using Data Feeds" **não** traz verificação de staleness, de preço positivo, heartbeat nem desvio. A checagem de idade se apoia na referência da API. Os exemplos da página são "não usar em produção".

Exemplo (redação própria) do que revisar e do que falta:

```solidity
// Incompleto: sem idade, sem answer > 0, decimals fixo, answeredInRound obsoleto.
(uint80 roundId, int256 answer, , , uint80 answeredInRound) = feed.latestRoundData();
require(answeredInRound >= roundId, "stale");
return uint256(answer) * 1e10;

// Direção correta (o limite MAX_AGE vem da página do feed escolhido, não de chute).
(, int256 answer, , uint256 updatedAt, ) = feed.latestRoundData();
if (answer <= 0) revert InvalidPrice();
if (block.timestamp - updatedAt > MAX_AGE) revert StalePrice();
uint8 dec = feed.decimals();          // escale a partir do decimals do próprio feed
```

| ID | Pergunta | Evidência esperada |
| --- | --- | --- |
| ORA-01 | A idade usa `updatedAt` e um limite por feed vindo do heartbeat publicado do feed escolhido? | Linha da checagem e fonte do limite; sem fonte, "Não verificável" |
| ORA-02 | `answer > 0`; `decimals()` do próprio feed; escala explícita ao combinar dois feeds (ex.: ETH/USD × USD/BRL)? | Código de conversão |
| ORA-03 | Endereço do feed conferido na lista oficial **por rede**; o que acontece se o feed falhar ou reverter (fallback ou pausa)? | Config por chain; teste com mock que reverte |
| ORA-04 | Preço de pool de DEX com pouca liquidez é fonte única? Nunca deve ser | Mapa de fontes de preço e consumidores |
| ORA-05 | Em L2, `L2-01..05` | Seção seguinte |

Quem consome o preço importa: colateral, liquidação e mint por preço têm risco maior que exibição. Não confie em `view` de pool (`slot0`, `getReserves`) como preço na mesma transação em que alguém pode movê-lo (flash loan). TWAP, Pyth e outros oráculos não têm fonte validada neste plugin (lacuna L4): rotule **fora da cobertura**.

## L2: sequenciador e OP Stack (L2)

### Feed de uptime do sequenciador (L2-01)

Em L2, o sequenciador pode ficar fora do ar enquanto o último preço continua "recente" de forma enganosa. A Chainlink publica um feed de uptime: 0 = no ar, 1 = fora. Padrão: reverter se estiver fora do ar e aplicar **período de carência** após o retorno, comparando `block.timestamp` com `startedAt` (o exemplo da doc usa 3600 s; o valor adequado é decisão do protocolo e deve ser registrado).

```solidity
(, int256 status, uint256 startedAt, , ) = sequencerFeed.latestRoundData();
if (status != 0) revert SequencerDown();
if (block.timestamp - startedAt <= GRACE_PERIOD) revert GracePeriodNotOver();
```

Ressalvas: na Arbitrum, `startedAt` pode ser 0 se o feed não foi inicializado (trate); o status vem do L1 e pode atrasar; as redes listadas incluem Arbitrum, Base, OP Mainnet, Scroll e ZKsync; a Chainlink não adiciona feeds a redes novas. Confirme na página se há feed de uptime para a rede alvo.

### Diferenças do OP Stack (L2-02 a L2-05)

Fonte: página "differences" da Optimism.

- **L2-02** `ORIGIN`/`CALLER` mostram endereço com **alias** em depósitos L1 → L2 (endereço L1 + offset fixo). Não use `msg.sender` para identificar contrato L1 sem tratar o alias.
- **L2-03** Taxa de dados L1 soma-se ao gás: estimativas de custo para keepers/liquidadores precisam incluí-la.
- **L2-04** Não há mempool público: não assuma essa propriedade como proteção contra MEV nem como ausência dela sem pesquisar a rede.
- **L2-05** Cabeças unsafe/safe/finalized: confirme finalidade antes de liberar valor irreversível.
- `COINBASE` é a carteira de taxas do sequenciador; `PREVRANDAO` traz o RANDAO do L1.

A página do OP **não cita** `block.number`, `block.timestamp`, precompiles nem `PUSH0` (ausentes, verificado): pesquise por rede. Arbitrum, Base e zk rollups têm diferenças próprias **não lidas** (lacuna L9): declare "fora da cobertura" em vez de generalizar.

Testes: use fork local da rede alvo (RPC por variável de ambiente, nunca o valor no chat) e simule o feed de sequenciador como mock com `status = 1` e com retorno recente.

## Hooks do Uniswap v4 e tokens atípicos (HOOK)

Fonte: Trail of Bits, "Building secure Uniswap v4 hooks" (2026-07-30), sete padrões; HOOK-08 a HOOK-10 são acréscimos deste plugin (tokens com taxa, rebase e hooks). Específico de Uniswap v4; sem números.

| ID | Padrão de falha | Pergunta de revisão | Teste sugerido |
| --- | --- | --- | --- |
| HOOK-01 | Callback sem verificação do chamador | Só o PoolManager consegue chamar os callbacks? (base contract ou checagem explícita) | Chamar o callback direto de um EOA: deve reverter |
| HOOK-02 | Confiar em qualquer pool | O hook deriva `PoolId` da `PoolKey` e restringe pools por allowlist? | Registrar o hook em pool não previsto |
| HOOK-03 | Contabilidade misturada | Sinal, arredondamento e baldes (deltas) conferem? | Invariante de conservação; round-trips |
| HOOK-04 | Lógica no hook errado | `beforeSwap` vê o estado anterior, `afterSwap` o posterior: a regra está no lugar certo? | Teste com preço antes/depois |
| HOOK-05 | Bits do endereço como API | Permissões no endereço alinhadas aos callbacks implementados? | Deploy de teste com endereço minerado coerente |
| HOOK-06 | Falha bloqueia saída | Código opcional (taxas, métricas) está isolado em `try`/`catch` de modo a não impedir saque/swap? | Fazer o opcional reverter e conferir que a saída funciona |
| HOOK-07 | Estado temporário em chamadas aninhadas | Chave por `PoolId` e chamador? Operações sobrepostas rejeitadas? Limpeza ao fim? | Chamada aninhada dentro de callback |
| HOOK-08 | Token com taxa de transferência | Valor recebido ≠ enviado: contabilidade mede saldo? | Mock com taxa |
| HOOK-09 | Token com rebase | Saldo em cache fica errado após rebase? | Mock com rebase |
| HOOK-10 | Token com hooks de callback | Reentrada via 777/1363/721/1155? | Mock com callback reentrante |

A fonte recomenda fuzzing com Echidna e Medusa. Medusa não foi lido (lacuna L7); prefira invariantes Foundry ([foundry-testes-gas.md](foundry-testes-gas.md)).

## Cenários de incidente como perguntas (SCN)

A listagem do rekt.news (oito incidentes entre 2026-09-14 e 2026-10-08, conferidos) alimenta seis perguntas. São **cenários de teste**, não fatos técnicos: causas mudam com post-mortems e valores não foram verificados de modo independente.

| ID | Incidente-modelo (listagem) | Pergunta de revisão |
| --- | --- | --- |
| SCN-01 | Preço de token inflado cerca de 300x como colateral; oráculo adulterado por pool manipulada | Pool raso pode inflar colateral? A fonte de preço tem piso de liquidez? |
| SCN-02 | Falha de encaminhamento que cunhou token sem lastro | Existe caminho em que mint/bridge crie ativo sem lastro ou aceite mensagem repetida? |
| SCN-03 | Colisão de chave de cache em verificação de prova | Chaves/hashes de entradas distintas podem colidir (concatenação ambígua, `abi.encodePacked` com tipos dinâmicos)? |
| SCN-04 | Autorizações assinadas válidas abusadas | Assinaturas presas a cadeia, contrato, nonce e validade (SIG-01, SIG-02)? |
| SCN-05 | Suspeita de chave privada comprometida | Quem custodia as chaves, com qual controle, e como se faz a rotação após suspeita? |
| SCN-06 | Infraestrutura de nuvem e produtos de segurança de terceiros | Serviços de terceiros podem mudar configuração e abrir caminho de ataque? |

## Fora da cobertura

TWAP e Pyth (L4), Arbitrum/Base/zk (L9), MEV e flash loan em profundidade (L12), pontes e mensageria cross-chain (L13), indexação e reorg (L2), serviços off-chain (relayers, keepers, bots: plugins `backend-api` e `automation-integrations`). Diga isso no relatório.
