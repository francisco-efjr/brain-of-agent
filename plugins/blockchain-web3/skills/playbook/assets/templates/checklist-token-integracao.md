# Checklist de integração com token de terceiro

Preencha uma linha por token aceito (ou uma coluna "qualquer token" se o protocolo aceita tokens arbitrários). Origem: EIP-20/721/1155 (V-11) e conhecimento estável de tokens atípicos; o Token Integration Checklist da Trail of Bits não foi lido (lacuna L6), então itens marcados **(Suposição)** vão além das fontes validadas. Tokens de teste são aceitos só com a leitura do código do token ou por mock.

| Pergunta | Token: [endereço/nome] | Origem |
| --- | --- | --- |
| Padrão alegado e implementado (ERC-20/721/1155)? `supportsInterface` correto? | | V-11 |
| `decimals()` existe? É lido de forma defensiva? (opcional na EIP-20) | | V-11 |
| `transfer`/`transferFrom`/`approve` devolvem `bool`, nada, ou revertem? Uso de `SafeERC20`? | | V-11 |
| Cobra taxa na transferência (valor recebido ≠ enviado)? Contabilidade mede saldo antes/depois? | | V-17 (HOOK-08) |
| Saldo muda sem evento `Transfer` (rebase)? Há saldo em cache? | | V-17 (HOOK-09) |
| Tem hooks de callback (777, 1363, `safeTransfer*` 721/1155) que permitem reentrada? | | V-11, V-01 (ERC-03, HOOK-10) |
| `Transfer` é emitido também em valor zero? O protocolo depende disso? | | V-11 |
| Pausa, blacklist ou lista de bloqueio controlada por terceiro? O protocolo sobrevive se o token bloquear seu contrato? | | Suposição |
| Token é upgradeable? Quem atualiza? Há timelock? | | Suposição (V-09 para o lado do protocolo) |
| Pode ter supply mintável por terceiro que dilua colateral? | | Suposição |
| Aprovação ilimitada (`type(uint256).max`) é aceitável? Alguma corrida de `approve` relevante? (o contrato não deve impô-la) | | V-11 |
| `tokenURI`/metadados (NFT) são tratados como dado externo não confiável? | | V-11 (ERC-04) |
| 1155: `safeBatchTransferFrom` com `_ids` e `_values` de tamanhos diferentes reverte? Ordem de IDs não é assumida? | | V-11 |
| Preço do token vem de fonte com liquidez adequada (nunca pool raso único)? | | V-19, V-18 |

Resultado por token: [aceitar | aceitar com ressalvas: … | rejeitar] · Estado epistêmico: [Verificado (leu o código do token) | Inferido | Suposição]
