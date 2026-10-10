# Checklist de conformidade ERC-20, ERC-721, ERC-1155 e integração

Fontes: EIP-20, EIP-721, EIP-1155 (eips.ethereum.org, Final, CC0), lidas em V-11. Redação própria. Rótulos: **Verificado** = presente em V-11; **Inferido** = texto da EIP ou conhecimento estável não registrado em V-11 (confira na EIP antes de citar em relatório); **Suposição** = prática comum sem fonte validada (token atípico, lacuna L6).

Use junto com os IDs `W3-ERC-01..04` do playbook: 01 interfaces, eventos e ERC-165; 02 integração com token arbitrário; 03 hooks de recebimento como reentrância; 04 `tokenURI` e metadados como dado externo.

## ERC-20 (W3-ERC-01)

| # | Verificação | Rótulo | Se falhar |
|---|---|---|---|
| 1 | Existem `totalSupply`, `balanceOf`, `transfer`, `transferFrom`, `approve`, `allowance` | Verificado | Não é ERC-20; integrações quebram |
| 2 | `name`, `symbol`, `decimals` são tratados como opcionais por quem consome; o contrato os implementa se o front depende deles | Verificado | Consumidor que lê `decimals()` de token sem a função reverte |
| 3 | `Transfer` é emitido também em transferência de valor 0 (`transfer` e `transferFrom`) | Verificado | Indexadores e integrações perdem eventos |
| 4 | `Approval` emitido em `approve`; `transferFrom` respeita e atualiza `allowance` | Inferido | Gasto indevido de saldo de terceiros |
| 5 | Saldo insuficiente reverte (ou retorna `false` de forma documentada); mint emite `Transfer` com `from == address(0)`, burn com `to == address(0)` | Inferido | Contabilidade off-chain divergente |
| 6 | O contrato não impõe "zerar antes de mudar" no `approve`: a EIP deixa isso para os clientes | Verificado | Incompatibilidade com integrações (falsa falha) |
| 7 | Se usa extensão (`Permit`, `Votes`, `Capped`, `Pausable`...), ela existe na versão instalada do OZ; `ERC20Snapshot` não existe na API do OZ 5.x | Verificado (ausência em 5.x) | Código que não compila ou cópia de regra desatualizada |

## ERC-721 (W3-ERC-01, W3-ERC-03)

| # | Verificação | Rótulo | Se falhar |
|---|---|---|---|
| 1 | Implementa ERC-165 (`supportsInterface`) e responde `true` para o id do ERC-721 (`0x80ac58cd`) e, se houver, metadados (`0x5b5e139f`) e enumeração (`0x780e9d63`) | ERC-165 exigido: Verificado; ids: Inferido (confira na EIP) | Marketplaces e carteiras não reconhecem o token |
| 2 | `safeTransferFrom` e `_safeMint` chamam `onERC721Received` no receptor com código; retorno diferente do valor mágico (`0x150b7a02`) reverte | Verificado (comportamento); valor: Inferido | NFT preso em contrato que não sabe tratá-lo |
| 3 | `transferFrom` não chama o hook; o contrato sabe que enviar com ele a um contrato sem suporte pode prender o NFT | Verificado | Perda por UX; documentar |
| 4 | O hook é chamada externa: o estado do contrato já está consistente quando `_safeMint`/`safeTransferFrom` chamam o receptor? Há `nonReentrant` onde preciso? | Verificado (reentrância, V-01) | Reentrância (SC05): mint acima do limite, saque duplo |
| 5 | Aprovação individual é limpa na transferência; `ownerOf` de id inexistente reverte | Inferido | Aprovação residual dá controle a quem não deveria |
| 6 | `tokenURI` e JSON de metadados são tratados como dado externo não confiável (HTML/SVG/URL) pelo front e por qualquer contrato que os leia (W3-ERC-04) | Verificado | XSS no front, conteúdo falso, injeção em agentes |

## ERC-1155 (W3-ERC-01, W3-ERC-03)

| # | Verificação | Rótulo | Se falhar |
|---|---|---|---|
| 1 | `safeBatchTransferFrom` reverte se `_ids` e `_values` têm tamanhos diferentes | Verificado | Transferência parcial ou fora de ordem |
| 2 | A ordem crescente de IDs é recomendação; não a trate como requisito nem como falha | Verificado | Falso positivo |
| 3 | Receptores com código recebem `onERC1155Received`/`onERC1155BatchReceived`; retorno inválido reverte (`0xf23a6e61` e `0xbc197c81`) | Verificado (comportamento); valores: Inferido | Tokens presos |
| 4 | Mint emite evento com `_from == address(0)`; burn com `_to == address(0)` | Verificado | Indexadores inconsistentes |
| 5 | Hooks de recebimento tratados como reentrância (batch com laço longo também é vetor de gás, SC10) | Verificado (V-01) | Reentrância, DoS |
| 6 | `supportsInterface` retorna `true` para `0xd9b67a26` | Inferido (id: confira na EIP) | Descoberta falha |

## Integração com token arbitrário (W3-ERC-02)

Perguntas por token aceito (o template completo está em `${CLAUDE_PLUGIN_ROOT}/skills/playbook/assets/templates/checklist-token-integracao.md`). A base normativa é V-11 (não assumir `decimals`, tratar retorno, taxa, rebase, hooks, `SafeERC20`); a lista de tipos atípicos abaixo é conhecimento estável e fica rotulada **Suposição** até a leitura do checklist da Trail of Bits (lacuna L6).

| Tipo de token | Comportamento | O que o protocolo precisa fazer | Rótulo |
|---|---|---|---|
| Sem retorno em `transfer`/`approve` | Algumas implementações antigas não retornam `bool` | `SafeERC20` (`safeTransfer`, `safeTransferFrom`, `forceApprove`) | Verificado (V-11 manda usar `SafeERC20`); exemplos de tokens: Suposição |
| Com taxa na transferência | Quem recebe obtém menos que `amount` | Contabilizar a diferença de saldo (`balanceAfter - balanceBefore`), não o valor pedido; ou proibir o token | Verificado (V-11) |
| Rebase | Saldo muda sem `Transfer` | Não guardar saldo por conta própria; usar o token de "shares" ou ler saldo no momento | Verificado (V-11) |
| Com hooks (ERC-777 e similares) | Chama receptor/remetente na transferência | Tratar `transfer` como chamada externa (CEI, `nonReentrant`) | Verificado (V-11, hooks); ERC-777 citado: Suposição |
| `decimals` diferentes de 18 | 6, 8, 2 etc. | Ler `decimals()` na escala; nunca fixar 18 | Verificado (V-11) |
| Pausável, com blacklist, upgradeable | O token pode reverter transferências do protocolo ou mudar de comportamento | Saída de emergência que não dependa de um único token; documentar premissa | Suposição |
| Revert em transferência de valor 0 ou aprovação de valor diferente de 0 para diferente de 0 | Idiossincrasias de implementações | Evitar transferir 0; `forceApprove` | Suposição |

Regra: a severidade de um achado de integração usa o pior token que o sistema aceita de fato. Lista fixa de tokens reduz o risco; "qualquer ERC-20" o multiplica.

## Como registrar

Uma linha por item na tabela de conformidade do relatório, com `arquivo:linha`. Item que depende de execução vira teste proposto (ver [erc4626-inflacao.md](erc4626-inflacao.md) para o 4626); nunca afirme que o teste passou sem rodar `forge`.
