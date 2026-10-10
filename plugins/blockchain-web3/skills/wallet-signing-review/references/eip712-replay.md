# EIP-712: assinatura sem replay (padrão correto e testes)

Fontes: EIP-712 (Final) lida em V-22; cenário 4 de V-18. Código: exemplo próprio com OpenZeppelin 5.x (`EIP712`, `Nonces`, `ECDSA`); nomes e caminhos mudam por major, confira a versão instalada. Rótulos: **Verificado** = V-22 (domínio, ausência de proteção contra replay, frontrunning); **Inferido** = código e comportamento de biblioteca; **Suposição** = EIP-2612, ERC-1271, malleabilidade (lacuna L5).

## 1. O que a norma garante e o que não garante

- O domínio tem os campos `name`, `version`, `chainId`, `verifyingContract` e `salt` (opcionais conforme o caso). Ele separa aplicações e cadeias, mas não torna a assinatura de uso único.
- A EIP-712 não oferece proteção contra replay: a aplicação deve rejeitar ou tornar idempotente a repetição (V-22). Isso significa nonce ou marcador de "já usado", e prazo.
- A EIP trata de frontrunning de assinaturas: uma assinatura enviada ao mempool é pública e pode ser submetida por outro antes do dono.

## 2. Versão insegura (padrão frequente)

```solidity
function claim(address account, uint256 amount, bytes calldata sig) external {
    bytes32 h = keccak256(abi.encodePacked(account, amount));
    address signer = ecrecover(
        keccak256(abi.encodePacked("\x19Ethereum Signed Message:\n32", h)),
        uint8(sig[64]), bytes32(sig[0:32]), bytes32(sig[32:64]));
    require(signer == trustedSigner, "bad sig");
    token.transfer(account, amount);
}
```

Falhas: sem nonce (a mesma assinatura repete até esvaziar o contrato), sem prazo, sem `chainId` nem `verifyingContract` (vale em qualquer cadeia e em qualquer cópia do contrato), `ecrecover` cru (inválido retorna `address(0)`; se `trustedSigner` nunca foi configurado, passa), `transfer` sem `SafeERC20`.

## 3. Versão corrigida

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {EIP712} from "@openzeppelin/contracts/utils/cryptography/EIP712.sol";
import {ECDSA} from "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";
import {Nonces} from "@openzeppelin/contracts/utils/Nonces.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

contract Claimer is EIP712, Nonces {
    using SafeERC20 for IERC20;

    error Expired();
    error BadSigner();

    bytes32 private constant CLAIM_TYPEHASH =
        keccak256("Claim(address account,uint256 amount,uint256 nonce,uint256 deadline)");

    IERC20 public immutable token;
    address public immutable signer;

    constructor(IERC20 token_, address signer_) EIP712("Claimer", "1") {
        token = token_;
        signer = signer_;
    }

    function claim(address account, uint256 amount, uint256 deadline, bytes calldata sig) external {
        if (block.timestamp > deadline) revert Expired();
        uint256 nonce = _useNonce(account);                       // consome antes do efeito
        bytes32 digest = _hashTypedDataV4(
            keccak256(abi.encode(CLAIM_TYPEHASH, account, amount, nonce, deadline)));
        if (ECDSA.recover(digest, sig) != signer) revert BadSigner();
        token.safeTransfer(account, amount);
    }
}
```

Por que cada escolha: o domínio do OZ inclui `chainId` e `verifyingContract` e é recalculado se o `chainId` mudar; `_useNonce` impede repetição por conta; `deadline` limita a janela; `abi.encode` evita ambiguidade de `encodePacked`; `ECDSA.recover` do OZ reverte em assinatura inválida em vez de devolver zero (Inferido: confira a versão); `SafeERC20` cobre token sem retorno. O destinatário (`account`) está na struct: quem submete a assinatura não consegue desviar o valor. Se o contrato fosse chamado por qualquer um e o efeito favorecesse o submissor, o frontrunning mudaria o dono do benefício; aqui não muda.

Se o signatário for um contrato (carteira multisig, conta abstrata), `ECDSA.recover` não funciona: seria preciso `SignatureChecker` e ERC-1271. Isso está fora da cobertura validada (**Suposição**).

## 4. Testes de replay a propor

Todos com chave de teste fixa dentro do teste (`vm.addr(PK)`, `vm.sign(PK, digest)`); nunca chave real.

| Teste | Como | Esperado |
|---|---|---|
| `test_replaySameNonceReverts` | usar a mesma assinatura duas vezes | segunda chamada reverte (`BadSigner`, porque o nonce mudou o digest) |
| `test_expiredReverts` | `vm.warp(deadline + 1)` | `Expired` |
| `test_otherChainReverts` | `vm.chainId(otherId)` entre assinar e enviar | `BadSigner` (domínio recalculado) |
| `test_otherContractReverts` | segunda implantação com a mesma assinatura | `BadSigner` (`verifyingContract` diferente) |
| `test_wrongSignerReverts` | assinar com outra chave | `BadSigner` |
| `test_amountTamperedReverts` | alterar `amount` depois de assinar | `BadSigner` |

Esqueleto de geração do digest em teste (o separador de domínio é calculado no próprio teste, sem depender de função pública do contrato):

```solidity
bytes32 domainSeparator = keccak256(abi.encode(
    keccak256("EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)"),
    keccak256(bytes("Claimer")), keccak256(bytes("1")), block.chainid, address(claimer)));
bytes32 structHash = keccak256(abi.encode(
    keccak256("Claim(address account,uint256 amount,uint256 nonce,uint256 deadline)"),
    alice, 100e18, claimer.nonces(alice), deadline));
bytes32 digest = keccak256(abi.encodePacked("\x19\x01", domainSeparator, structHash));
(uint8 v, bytes32 r, bytes32 s) = vm.sign(SIGNER_PK, digest);
bytes memory sig = abi.encodePacked(r, s, v);
```

Se o domínio calculado no teste divergir do que o contrato usa (nome ou versão diferentes), o teste de caminho feliz já falha com `BadSigner`: é o sinal para conferir `EIP712("Claimer", "1")`. O OZ 5.x também expõe `eip712Domain()` (ERC-5267) para ler os campos do domínio (Inferido: confira a versão instalada).

## 5. Dados de assinatura no dapp (cliente)

JSON de `eth_signTypedData_v4` (exemplo; endereço e cadeia de teste):

```json
{
  "types": {
    "EIP712Domain": [
      {"name": "name", "type": "string"},
      {"name": "version", "type": "string"},
      {"name": "chainId", "type": "uint256"},
      {"name": "verifyingContract", "type": "address"}
    ],
    "Claim": [
      {"name": "account", "type": "address"},
      {"name": "amount", "type": "uint256"},
      {"name": "nonce", "type": "uint256"},
      {"name": "deadline", "type": "uint256"}
    ]
  },
  "primaryType": "Claim",
  "domain": {"name": "Claimer", "version": "1", "chainId": 11155111,
             "verifyingContract": "0x0000000000000000000000000000000000000001"},
  "message": {"account": "0x0000000000000000000000000000000000000002",
              "amount": "100000000000000000000", "nonce": "0", "deadline": "1799999999"}
}
```

Conferências: o `chainId` do domínio é o da cadeia ativa na carteira (compare com o valor lido por `eth_chainId` antes de pedir assinatura); o tipo em string do contrato é idêntico à lista de campos (nome, ordem, tipo); o valor mostrado à pessoa em unidades legíveis vem do mesmo `amount` do JSON.

## 6. Frontrunning de `permit` (Suposição, EIP-2612 fora da cobertura)

Padrão conhecido: se um contrato chama `token.permit(...)` com uma assinatura que o usuário também enviou ao mempool, outro endereço pode executar o `permit` primeiro e a chamada do contrato reverte pelo nonce já usado (negação de serviço de baixo custo). Mitigação comum: `try token.permit(...) {} catch {}` seguido de checagem da `allowance`. Rotulado Suposição: a EIP-2612 não foi lida (lacuna L5); confirme na EIP e na versão do token antes de citar em relatório.
