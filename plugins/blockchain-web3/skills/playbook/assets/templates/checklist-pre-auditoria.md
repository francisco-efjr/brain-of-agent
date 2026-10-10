# Checklist pré-auditoria

Estados: Verificado (código lido com `arquivo:linha`, ou comando executado) · Inferido · Suposição · Não verificável · N/A (com motivo). Os textos completos e como conferir cada ID estão em `references/checklist-completo.md`. Ausência de problema nos itens não prova segurança.

| ID | Item (resumo) | Status | Evidência (`arquivo:linha` / comando) | Nota |
| --- | --- | --- | --- | --- |
| W3-SOL-01 | Reentrância: CEI, pull payments | | | |
| W3-SOL-02 | Retorno de chamada de baixo nível checado | | | |
| W3-SOL-03 | `msg.sender`, nunca `tx.origin` | | | |
| W3-SOL-04 | Laços sobre storage crescente com limite | | | |
| W3-SOL-05 | `private` não é secreto; aleatoriedade | | | |
| W3-SOL-06 | `unchecked`, conversões, divisão | | | |
| W3-SOL-07 | `delete` e mappings | | | |
| W3-SOL-08 | Proxy sem permissões próprias | | | |
| W3-SOL-09 | Valor retido, fail-safe, warnings zerados | | | |
| W3-ACC-01 | Todo entry point tem dono; teste com ator sem papel | | | |
| W3-ACC-02 | Admin definido; multisig em produção | | | |
| W3-ACC-03 | Timelock; plano de recuperação antes de renunciar | | | |
| W3-ACC-04 | `RoleGranted`/`RoleRevoked` monitorados | | | |
| W3-ACC-05 | Funções irmãs justificadas | | | |
| W3-UPG-01 | Padrão de proxy justificado; `_authorizeUpgrade` restrito | | | |
| W3-UPG-02 | `_disableInitializers`; sem estado em construtor | | | |
| W3-UPG-03 | Layout comparado; novas variáveis no fim/ERC-7201 | | | |
| W3-UPG-04 | `ProxyAdmin` novo por deploy; migração entre versões maiores | | | |
| W3-UPG-05 | Tag auditada pinada | | | |
| W3-VLT-01 | ERC-4626 conforme a especificação | | | |
| W3-VLT-02 | Arredondamento a favor do cofre; round-trip | | | |
| W3-VLT-03 | Defesa contra inflação testada | | | |
| W3-VLT-04 | `preview*` nunca como preço | | | |
| W3-VLT-05 | Invariante ativos × shares | | | |
| W3-ERC-01 | Interfaces, eventos e ERC-165 completos | | | |
| W3-ERC-02 | Integração com token arbitrário | | | |
| W3-ERC-03 | Hooks 721/1155 como reentrância | | | |
| W3-ERC-04 | `tokenURI`/metadados como dado externo | | | |
| W3-ORA-01 | Idade por `updatedAt` contra heartbeat | | | |
| W3-ORA-02 | `answer > 0`; `decimals()` do feed | | | |
| W3-ORA-03 | Endereço por rede; fallback ou pausa | | | |
| W3-ORA-04 | Pool raso nunca é fonte única | | | |
| W3-L2-01 | Feed de uptime do sequenciador + carência | | | |
| W3-L2-02 | Alias de endereço tratado | | | |
| W3-L2-03 | Taxa de dados L1 considerada | | | |
| W3-L2-04 | Sem premissa de mempool público | | | |
| W3-L2-05 | Finalidade antes de liberar valor | | | |
| W3-SIG-01 | Domínio EIP-712 completo | | | |
| W3-SIG-02 | Nonce, validade e idempotência | | | |
| W3-SIG-03 | Erros EIP-1193 e eventos tratados | | | |
| W3-SIG-04 | Exibido = executado; sem pedir chave | | | |
| W3-TST-01..05 | Invariantes e fuzz conforme a especificação | | | |
| W3-GAS-01..04 | Alegações de gás com antes/depois | | | |
| W3-AGT-01..06 | Configuração do agente e das chaves | | | |

Áreas HOOK (Uniswap v4), SCN (cenários) e SVM (Anchor, parcial) entram quando aplicáveis: copie as linhas de `references/checklist-completo.md`.

Cobertura: [o que foi lido] · [o que foi executado] · [o que ficou de fora]
