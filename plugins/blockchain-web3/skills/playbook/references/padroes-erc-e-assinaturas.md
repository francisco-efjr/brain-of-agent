# Padrões ERC, cofres ERC-4626, assinaturas EIP-712 e carteiras EIP-1193

Itens V-10, V-11 e V-22 de [fontes.md](fontes.md); IDs em [checklist-completo.md](checklist-completo.md). As EIPs são o oráculo normativo (texto CC0); a documentação do OpenZeppelin é MIT. Os exemplos são redação própria. Confirme a versão do OpenZeppelin instalada: a 5.x removeu extensões antigas (por exemplo, `ERC20Snapshot` não consta da API do ERC-20 5.x).

## Sumário

- [ERC-20 (ERC-01, ERC-02)](#erc-20-erc-01-erc-02)
- [ERC-721 e ERC-1155 (ERC-01, ERC-03, ERC-04)](#erc-721-e-erc-1155-erc-01-erc-03-erc-04)
- [Integração com token arbitrário (ERC-02)](#integração-com-token-arbitrário-erc-02)
- [ERC-4626 (VLT-01 a VLT-05)](#erc-4626-vlt-01-a-vlt-05)
- [EIP-712: assinaturas (SIG-01, SIG-02)](#eip-712-assinaturas-sig-01-sig-02)
- [EIP-1193: carteira e provider (SIG-03, SIG-04)](#eip-1193-carteira-e-provider-sig-03-sig-04)
- [Fora da cobertura](#fora-da-cobertura)

## ERC-20 (ERC-01, ERC-02)

Normativo na EIP-20 (criada em 2015-11-19, Final):

- Obrigatórias: `totalSupply`, `balanceOf`, `transfer`, `transferFrom`, `approve`, `allowance` e os eventos.
- **Opcionais**: `name`, `symbol`, `decimals`. Ninguém deve esperá-las: código que lê `decimals()` de token arbitrário precisa de `try`/fallback ou lista de tokens aceitos.
- `Transfer` é obrigatório **inclusive em valor zero**.
- Corrida do `approve`: os clientes devem zerar a permissão antes de mudar o valor, mas o contrato **não** deve impor isso.

Armadilha de revisão: contrato que "implementa ERC-20" sem emitir `Transfer` em mint/burn, ou que falha com valor zero, quebra indexadores e integradores.

## ERC-721 e ERC-1155 (ERC-01, ERC-03, ERC-04)

ERC-721 (Final, 2018-01-24): requer EIP-165 (`supportsInterface`). A transferência segura chama `onERC721Received` no receptor contrato e deve reverter se o retorno diferir do valor mágico. `transferFrom` **não** chama o hook.

ERC-1155 (Final, 2018-06-17): `safeBatchTransferFrom` deve reverter se `_ids` e `_values` têm tamanhos diferentes. Ordenar IDs em ordem crescente é **recomendação**, não obrigação. Receptores implementam `onERC1155Received`/`onERC1155BatchReceived`. No evento, mint tem `_from` zero e burn tem `_to` zero.

Pontos de revisão:

- **ERC-03** Cada hook de recebimento devolve controle ao receptor: `_safeMint` e `safeTransferFrom` antes de atualizar estado reabrem reentrância (ex.: mint de NFT que verifica `balanceOf` depois do callback).
- **ERC-04** `tokenURI` e metadados são dados externos controlados por terceiros. Contratos, front-ends e agentes não os tratam como instrução nem como fonte de decisão de segurança.
- Nenhum dos três padrões foi lido nos anexos de implementação de referência (limitação das fontes).

## Integração com token arbitrário (ERC-02)

Quando o protocolo aceita tokens de terceiros, use este checklist (o template [checklist-token-integracao.md](../assets/templates/checklist-token-integracao.md) o transforma em perguntas por token):

| Pergunta | Por quê |
| --- | --- |
| `decimals` é lido de forma defensiva? | Opcional na EIP |
| O retorno de `transfer`/`transferFrom`/`approve` é tratado? | Alguns tokens devolvem `false` em vez de reverter, outros não devolvem nada: use `SafeERC20` |
| O token cobra taxa na transferência? | Valor recebido menor que o enviado quebra contabilidade que assume igualdade (HOOK-08) |
| O saldo muda sem `Transfer` (rebase)? | Saldos em cache ficam errados (HOOK-09) |
| O token tem hooks de callback? | Superfície de reentrância (HOOK-10, SOL-01) |
| Há pausa, blacklist ou upgrade controlados por terceiro? | O token pode bloquear seu contrato (Suposição quando não há leitura do token) |

O Token Integration Checklist e o catálogo de tokens atípicos da Trail of Bits **não foram lidos** (copyleft; lacuna L6): o que está acima vem da EIP-20 e da prática estável. Tudo que passar disso é **Suposição**.

```solidity
// Sem SafeERC20: um token que devolve false deixa o estado seguir como pago.
token.transferFrom(msg.sender, address(this), amount);
// Com SafeERC20 (using SafeERC20 for IERC20): reverte em falha.
token.safeTransferFrom(msg.sender, address(this), amount);
// Contabilidade correta para token com taxa: meça o saldo antes e depois.
uint256 before = token.balanceOf(address(this));
token.safeTransferFrom(msg.sender, address(this), amount);
uint256 received = token.balanceOf(address(this)) - before;
```

## ERC-4626 (VLT-01 a VLT-05)

Fonte: EIP-4626 (Final, criada em 2021-12-22, requer EIP-20) e a doc do OpenZeppelin 5.x.

### Regras de arredondamento (VLT-02)

`convertToShares`/`convertToAssets` arredondam para baixo. Princípio: **sempre a favor do cofre** — para baixo ao emitir shares ou enviar ativos ao usuário, para cima quando o usuário precisa fornecer mais. Teste de round-trip: depositar e resgatar na mesma transação nunca pode dar mais ativos do que entraram.

### `preview*` não é oráculo (VLT-04)

`preview*` é manipulável (depende do estado atual do cofre, incluindo doações diretas). A própria EIP sugere `convert*` (com TWAP) para esse papel. Contrato externo que usa `previewRedeem` como preço de colateral herda a manipulação.

### Ataque de inflação (VLT-03)

A EIP **não trata** de inflação/donation (ausente, verificado). A doc do OpenZeppelin explica o ataque e a defesa por offset de precisão com shares e ativos virtuais. A doc **não confirma** qual mitigação a implementação base ativa por padrão: leia o código da versão instalada.

Exemplo numérico (redação própria; ativos em wei, sem decimais virtuais):

1. Cofre vazio. Atacante deposita 1 wei: recebe 1 share (supply = 1, assets = 1).
2. Atacante doa 5e18 direto ao cofre (sem mint): assets = 5e18 + 1, supply = 1.
3. Vítima deposita 9e18: `shares = floor(9e18 × 1 / (5e18 + 1)) = 1`. Supply = 2, assets = 14e18 + 1.
4. Atacante resgata 1 share ≈ 7e18; gastou 5e18 + 1 wei. Lucro ≈ 2e18; a vítima, dona de 1 share ≈ 7e18, perdeu ≈ 2e18.

Se a doação é maior que o depósito, a vítima recebe 0 shares e perde tudo. Defesas: shares/ativos virtuais com offset de precisão (OpenZeppelin), ou depósito inicial "morto" feito pelo deployer. Cada uma tem custo (precisão adicional, capital preso): veja [decisoes-e-tradeoffs.md](decisoes-e-tradeoffs.md) (T-04). O teste mínimo: atacante doa, vítima deposita, a perda da vítima fica abaixo do limite definido.

### Conformidade (VLT-01) e invariante (VLT-05)

Funções e eventos obrigatórios presentes; `max*` e `preview*` coerentes com o comportamento real; shares são EIP-20; o contrato **cumpre a especificação**, não só a interface. Invariante útil: ativos totais coerentes com as shares emitidas (veja [foundry-testes-gas.md](foundry-testes-gas.md)).

## EIP-712: assinaturas (SIG-01, SIG-02)

EIP-712 (criada em 2017-09-12) define dados tipados assináveis. O domínio inclui `name`, `version`, `chainId`, `verifyingContract` e `salt`. A norma **não oferece proteção contra replay**: a aplicação precisa rejeitar ou tornar idempotente a repetição. Também trata de frontrunning de assinaturas.

```solidity
// Vulnerável: assinatura sem domínio, nonce nem validade.
bytes32 h = keccak256(abi.encodePacked(to, amount));
require(ECDSA.recover(h, sig) == owner, "bad sig");
token.transfer(to, amount);   // a mesma assinatura serve repetidas vezes, em outra cadeia e em outro contrato
```

Correção conceitual: digest EIP-712 com domínio (cadeia e contrato), campo `nonce` consumido no verificador, `deadline` e efeito idempotente. Teste de replay: mesma assinatura em outra cadeia (fork com outro `chainId`), em outro contrato, com nonce reutilizado e expirada. O cálculo exato do digest (`_hashTypedDataV4` do `EIP712` do OpenZeppelin) deve ser conferido na versão instalada (**Inferido**, API estável).

## EIP-1193: carteira e provider (SIG-03, SIG-04)

EIP-1193 (criada em 2018-06-30): `request(args)` e eventos `accountsChanged`, `chainChanged`, `connect`, `disconnect`, `message`. Códigos de erro: 4001 (usuário rejeitou), 4100, 4200, 4900, 4901. O Provider **não gerencia chaves** e a página o trata como código não confiável. Contas não são expostas por padrão (`eth_requestAccounts`).

Revisão do dapp:

- Trata 4001 como cancelamento normal (não como falha), 4100 (não autorizado), 4900/4901 (desconectado / cadeia não conectada).
- Reage a `chainChanged` e `accountsChanged`: não mantém estado de conta ou cadeia antiga.
- Nunca pede chave privada ou seed; nada de "importar chave" no front-end.
- O que é exibido ao usuário ao assinar é o que será executado (texto, valores, destinatário).
- A implementação de UI, estado e acessibilidade do dapp pertence ao plugin `web-frontend`; aqui só a segurança de assinatura e provider.

## Fora da cobertura

EIP-2612 (`permit`), ERC-1271 (assinaturas de contratos), malleabilidade de ECDSA, ERC-4337 e EIP-7702 não foram lidos (lacuna L5): qualquer comentário sobre eles leva rótulo **Suposição**. Vyper: Suposição. ERC-6909 e outros padrões: sem fonte.
