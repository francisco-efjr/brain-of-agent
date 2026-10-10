# Sinais de busca por classe (apoio à varredura)

Uso: pistas para `Grep`, não detectores. Um sinal sem caminho de ataque não é achado; um contrato sem sinais ainda pode ter erro de lógica (SC03), que não se acha por busca. Rótulos: **Verificado** = presente nas fontes validadas (V-…); **Inferido** = conhecimento estável de Solidity, fora de VALIDATED, confira na doc da versão em uso.

Padrões em `rg`/`Grep` (regex); ajuste a pasta para `src/` e exclua `test/`, `lib/`, `script/` quando for revisar produção.

| Classe (OWASP, ID) | Sinais de busca | Pergunta que o sinal abre | Rótulo |
|---|---|---|---|
| Reentrância (SC05, W3-SOL-01) | `\.call\{`, `\.call\(`, `\.transfer\(`, `\.send\(`, `safeTransferFrom`, `_safeMint`, `onERC721Received`, `onERC1155Received`, chamadas a interfaces externas | Há escrita de estado depois da chamada? Hook de recebimento 721/1155 é superfície de reentrância (W3-ERC-03). Leitura de estado durante reentrância (view reentrancy) engana contratos que consultam este | Verificado (CEI, V-01); view reentrancy Inferido |
| Retorno de chamada de baixo nível (SC06, W3-SOL-02) | `\.call\(`, `\.delegatecall\(`, `\.staticcall\(`, `\.send\(` sem `require`/`if` no retorno | O `bool success` é checado? Chamada a endereço sem código "sucede" | Verificado (V-01) |
| Autenticação (SC01, W3-SOL-03) | `tx\.origin` | Autorização por `tx.origin` permite phishing via contrato intermediário; use `msg.sender` | Verificado (V-01) |
| Controle de acesso (SC01, W3-ACC-01..05) | `function \w+\(.*\) (external\|public)` sem `onlyOwner\|onlyRole\|auth\|restricted\|whenNotPaused`; `initialize\(`; `grantRole`, `DEFAULT_ADMIN_ROLE`, `renounceRole`, `transferOwnership`, `Ownable` | Cada função que muda estado tem dono explícito? A irmã vizinha tem o modificador que esta não tem? Quem administra o papel de admin? | Verificado (V-08, V-03) |
| DoS por gás (SC10, W3-SOL-04) | `for \(`, `while \(` sobre `.length` de array em storage; `push\(` em array alimentado por usuário; `.transfer\(` dentro de laço | O array cresce por ação de usuário? Um endereço pode travar a função (pagamento que reverte dentro do laço)? | Verificado (V-01) |
| Aleatoriedade e dados secretos (SC09, W3-SOL-05) | `block\.timestamp`, `blockhash`, `block\.prevrandao`, `block\.difficulty`, `private` guardando segredo | Quem constrói o bloco influencia o resultado? Variável `private` guarda segredo? A doc do Solidity trata do tema em geral; não atribua a ela as variáveis acima (V-01 registra a ausência) | Verificado (tema); lista de variáveis Inferido |
| Aritmética (SC08, W3-SOL-06) | `unchecked`, casts `uint\d+\(`, `int\d+\(`, divisão antes de multiplicação (`/ .* \*`), `mulDiv`, `Math\.` | O bloco `unchecked` tem prova de limite? O cast trunca? O arredondamento favorece o protocolo (W3-VLT-02)? | Verificado (V-01, V-10) |
| `delete`/mappings (W3-SOL-07) | `delete \w+`, `struct` com `mapping` dentro, arrays de structs | `delete` em struct com mapping deixa valores; basta zerar entradas relevantes | Verificado (V-01) |
| Proxy e delegatecall (W3-SOL-08, W3-UPG) | `delegatecall`, `selfdestruct`, `fallback`, `upgradeTo`, `_authorizeUpgrade`, `initializer`, `reinitializer`, `_disableInitializers`, `__gap`, `constructor` em contrato upgradeable | `_authorizeUpgrade` é restrito? A implementação chama `_disableInitializers`? Há estado em construtor ou valor inicial de campo? O layout só cresce no fim? | Verificado (V-09, V-01) |
| Oráculo e preço (SC02, W3-ORA) | `latestRoundData`, `latestAnswer`, `getReserves`, `slot0`, `balanceOf\(address\(this\)\)` usado como preço ou contabilidade, `convertToAssets`, `previewRedeem` | Há checagem de idade por `updatedAt`, `answer > 0`, `decimals()`? O preço vem de pool raso? Alguém consome `preview*` como preço? Saldo medido por `balanceOf` aceita doação direta | Verificado (V-19, V-10); `balanceOf` como contabilidade Inferido |
| Assinaturas (W3-SIG) | `ecrecover`, `ECDSA\.recover`, `keccak256\(abi\.encodePacked\(`, `block\.chainid`, `nonce`, `deadline`, `DOMAIN_SEPARATOR`, `_hashTypedDataV4` | A assinatura cobre cadeia, contrato, nonce e validade? O nonce é consumido? | Verificado (V-22) |
| Colisão de hash (SCN-03) | `abi\.encodePacked\(` com mais de um tipo dinâmico (`string`, `bytes`, arrays) dentro de `keccak256` | `("ab","c")` e `("a","bc")` geram o mesmo hash; use `abi.encode` | Inferido (conhecimento estável; V-18 cita colisão de chave de cache) |
| Valor retido e fail-safe (W3-SOL-09) | `payable`, `receive\(\)`, `address\(this\)\.balance`, `Pausable`, `whenNotPaused` | Há limite de valor retido e modo de pausa? Cuidado: pausa sem plano de saída também trava usuários | Verificado (V-01) |
| Entrada e multicall (SC04) | `multicall`, `msg\.value` dentro de laço ou de função chamada por `delegatecall` interno | O mesmo `msg.value` é contado mais de uma vez? Parâmetros de endereço/valor validados (zero, limites)? | Inferido |
| Flash loan e MEV (SC07) | `flashLoan`, `onFlashLoan`, `swap`, `slippage`, `minOut`, `deadline` | Slippage e prazo vêm do chamador? Preço instantâneo pode ser movido na mesma transação? MEV está fora da cobertura validada (lacuna L12) | Inferido; lacuna declarada |

## Roteiro de leitura por arquivo (ordem sugerida)

1. Interfaces e eventos: o que o sistema promete.
2. Contratos base e modificadores: o que cada papel pode fazer.
3. Entry points de dinheiro (depósito, saque, mint, burn, liquidação, claim): maior impacto primeiro.
4. Funções administrativas (pausa, parâmetros, upgrade): quem as aciona e com que atraso.
5. Integrações externas (oráculo, DEX, token arbitrário): o que acontece se o outro lado mentir, atrasar ou reverter.

## Quando o sinal não aparece

- Erros de lógica de negócio (SC03) exigem a propriedade esperada: peça ao usuário ou extraia do NatSpec e confirme com ele. Sem propriedade, proponha invariantes por `foundry-testing` e registre "lógica de negócio não coberta" em Cobertura.
- Dependências em `lib/` não fazem parte do diff: diga que não foram revisadas, a menos que o diff altere versão ou faça fork delas.
