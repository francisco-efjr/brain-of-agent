# Checklist completo (índice mestre dos IDs `W3-*`)

Conferido em 2026-10-10 contra as fontes de [fontes.md](fontes.md). Este arquivo é a lista canônica de IDs citáveis: skills, agentes e relatórios referenciam `W3-<ÁREA>-NN` (nas skills aparece abreviado, por exemplo `ORA-01..05`). O detalhe técnico, os exemplos e as ressalvas de cada área estão nos arquivos temáticos indicados na coluna "Detalhe". Versões de OpenZeppelin, Foundry, Anchor e dos feeds mudam: confirme a instalada antes de citar API.

## Sumário

- [Como usar](#como-usar)
- [Ordem de uso](#ordem-de-uso)
- [Matriz área × skill/agente](#matriz-área--skillagente)
- [Os IDs](#os-ids)
- [Critérios de saída por fase](#critérios-de-saída-por-fase)
- [Rótulos epistêmicos aplicados](#rótulos-epistêmicos-aplicados)
- [Rótulos OWASP SC Top 10 (2025)](#rótulos-owasp-sc-top-10-2025)

## Como usar

1. Escolha as áreas pertinentes ao contrato (nem toda área se aplica; "Não aplicável" exige motivo de uma linha).
2. Percorra os IDs da área; para cada um registre o estado: **Verificado** (lido no código com `arquivo:linha`, ou executado com saída), **Inferido**, **Suposição**, **Não verificável**, **Não aplicável**.
3. Um ID só vira achado quando há caminho de ataque (pré-condições, quem perde o quê) e sobreviveu à refutação ([validacao-de-achados.md](validacao-de-achados.md)).
4. Todo achado cita o ID `W3-…` e, quando houver, o rótulo `OWASP-SCnn`. `swc_id` é opcional.
5. "Todos os IDs ok" não prova segurança: o relatório declara a Cobertura (o que foi lido, o que foi executado, o que ficou de fora).

## Ordem de uso

1. Escopo e versões (pragma, `foundry.toml`, OpenZeppelin em `lib/` ou remappings, plugin de upgrades, Anchor).
2. Mapa do sistema: contratos, herança, entry points que mudam estado, papéis, chamadas externas, proxies, oráculos, tokens aceitos.
3. `SOL` e `ACC` em todo contrato; depois as áreas que o mapa acionar (`UPG`, `VLT`, `ERC`, `ORA`, `L2`, `HOOK`, `SIG`, `SVM`).
4. `SCN` como perguntas de revisão baseadas em incidentes recentes (cenário, não fato técnico).
5. `TST` e `GAS` para provar (invariantes, fuzz, snapshot); `AGT` quando o agente tocar o repositório.

## Matriz área × skill/agente

| Área | Tema | Skill | Agente | Detalhe |
| --- | --- | --- | --- | --- |
| SOL | Pitfalls do Solidity | `contract-security-review` | `solidity-security-reviewer` | [solidity-seguranca.md](solidity-seguranca.md) |
| ACC | Controle de acesso (OpenZeppelin) | `contract-security-review` | `solidity-security-reviewer` | [solidity-seguranca.md](solidity-seguranca.md) |
| UPG | Proxies, initializers, layout | `contract-security-review` | `solidity-security-reviewer` | [solidity-seguranca.md](solidity-seguranca.md) |
| VLT | Cofres ERC-4626 | `token-standards-review` | `solidity-security-reviewer` | [padroes-erc-e-assinaturas.md](padroes-erc-e-assinaturas.md) |
| ERC | ERC-20/721/1155 e integração | `token-standards-review` | `solidity-security-reviewer` | [padroes-erc-e-assinaturas.md](padroes-erc-e-assinaturas.md) |
| ORA | Oráculos de preço (Chainlink) | `defi-oracle-l2-review` | `defi-protocol-analyst` | [oraculos-l2-defi.md](oraculos-l2-defi.md) |
| L2 | Sequenciador e OP Stack | `defi-oracle-l2-review` | `defi-protocol-analyst` | [oraculos-l2-defi.md](oraculos-l2-defi.md) |
| HOOK | Hooks do Uniswap v4 e tokens atípicos | `defi-oracle-l2-review` | `defi-protocol-analyst` | [oraculos-l2-defi.md](oraculos-l2-defi.md) |
| SCN | Cenários de incidente | `defi-oracle-l2-review` | `defi-protocol-analyst` | [oraculos-l2-defi.md](oraculos-l2-defi.md) |
| SIG | Assinaturas EIP-712 e carteiras EIP-1193 | `wallet-signing-review` | `solidity-security-reviewer` | [padroes-erc-e-assinaturas.md](padroes-erc-e-assinaturas.md) |
| SVM | Solana/Anchor (parcial) | `solana-anchor-review` | `solidity-security-reviewer` | `${CLAUDE_PLUGIN_ROOT}/skills/solana-anchor-review/references/solana-anchor.md` |
| TST | Invariantes e fuzz | `foundry-testing` | `invariant-test-engineer` | [foundry-testes-gas.md](foundry-testes-gas.md) |
| GAS | Gás com evidência | `foundry-testing` | `invariant-test-engineer` | [foundry-testes-gas.md](foundry-testes-gas.md) |
| AGT | Segurança do agente e das chaves | `playbook` | `web3-agent-safety-auditor` | [seguranca-do-agente-e-chaves.md](seguranca-do-agente-e-chaves.md) |

## Os IDs

Cada linha: ID · verificação (o que fazer) · fonte (item V em [fontes.md](fontes.md)). A redação é destilação própria.

### SOL — pitfalls do Solidity (V-01)

| ID | Verificação | Como conferir |
| --- | --- | --- |
| W3-SOL-01 | Toda chamada externa é ponto de reentrada: validar, atualizar estado, só então chamar fora (Checks-Effects-Interactions). Pagamento por saque (pull) em vez de envio direto. | Para cada `call`, `transfer`, `safeTransfer*`, hook de token: o estado já mudou antes? Há `nonReentrant` ou equivalente justificado? |
| W3-SOL-02 | Checar o retorno de chamadas de baixo nível; `call` falha pode devolver `false` sem reverter. | Buscar `.call(`, `.send(`, `.delegatecall(`: o booleano é usado? |
| W3-SOL-03 | Autorização com `msg.sender`, nunca `tx.origin`. | Buscar `tx.origin` em condições de acesso. |
| W3-SOL-04 | Laço sobre storage que cresce por ação de usuário precisa de limite ou paginação (risco de travar função por gás, inclusive `view` chamada por outro contrato). | Buscar `for`/`while` sobre arrays/mappings enumeráveis sem teto. |
| W3-SOL-05 | Dados `private` são legíveis on-chain; aleatoriedade on-chain pode ser manipulada por quem constrói o bloco. | Buscar uso de segredo em `private` e fontes de aleatoriedade. |
| W3-SOL-06 | `unchecked`, conversões de tipo e divisão: revisar cada bloco; versões ≥ 0.8 revertem por padrão fora de `unchecked`. | Buscar `unchecked`, casts `uintN(`, divisões antes de multiplicações. |
| W3-SOL-07 | `delete` não limpa mappings; array de structs com mapping deixa valores. | Buscar `delete` em structs com mapping. |
| W3-SOL-08 | Proxy que repassa chamadas arbitrárias não deve ter permissões próprias. | Verificar que o proxy não é dono/papel de nada. |
| W3-SOL-09 | Limitar o valor retido; prever modo fail-safe (pausa, limites); compilar com versão atual e zerar warnings. | Saída de `forge build` sem warnings; existência de pausa/limites onde cabe. |

### ACC — controle de acesso (V-08)

| ID | Verificação | Como conferir |
| --- | --- | --- |
| W3-ACC-01 | Toda função que muda estado tem dono explícito (papel); testar com ator sem papel. | Tabela entry point × modificador; teste com `vm.prank` de endereço sem papel. |
| W3-ACC-02 | Papéis com admin definido; `DEFAULT_ADMIN_ROLE` em uma conta (ou `AccessControlDefaultAdminRules`) e, em produção, multisig. | Constructor/initializer: quem recebe o admin? |
| W3-ACC-03 | Operações sensíveis atrás de timelock; plano de recuperação **antes** de renunciar ao admin (renunciar pode travar o sistema). | Existe `TimelockController` ou equivalente? Há quem possa recuperar? |
| W3-ACC-04 | Eventos `RoleGranted`/`RoleRevoked` monitorados. | Pergunta ao dono da operação; fora do código (Suposição se não há evidência). |
| W3-ACC-05 | Funções irmãs: uma com modificador e a vizinha sem ele exige justificativa escrita. | Comparar pares (`deposit`/`depositFor`, `setX`/`setXBatch`, `pause`/`unpause`). |

### UPG — upgradeability (V-09)

| ID | Verificação | Como conferir |
| --- | --- | --- |
| W3-UPG-01 | Padrão de proxy escolhido e justificado; em UUPS, `_authorizeUpgrade` restrito. | Ler `_authorizeUpgrade`; ADR do padrão. |
| W3-UPG-02 | Implementação chama `_disableInitializers` no construtor; initializers chamam os dos pais; sem estado em construtor nem em valor inicial de campo. | Buscar `constructor`, `initializer`, `onlyInitializing`, `= <valor>` em campos de estado. |
| W3-UPG-03 | Comparar layout de storage entre versões com a ferramenta do plugin de upgrades; variável nova só no fim ou em namespace ERC-7201; sem `delegatecall`/`selfdestruct` na implementação. | Diff de declarações; saída da validação de layout (executada pelo usuário). |
| W3-UPG-04 | Um `ProxyAdmin` novo por deploy; troca de versão maior do OpenZeppelin exige plano de migração de storage. | Versão do OZ antes/depois. |
| W3-UPG-05 | Pinar a tag auditada; ler `audits/` antes de adotar versão. | `foundry.toml`/remappings/submódulo apontam para tag, não `master`. |

### VLT — cofres ERC-4626 (V-10)

| ID | Verificação | Como conferir |
| --- | --- | --- |
| W3-VLT-01 | Funções e eventos obrigatórios; `max*`/`preview*` coerentes; shares são EIP-20; implementa a especificação, não só a interface. | Comparar com a EIP-4626. |
| W3-VLT-02 | Arredondamento a favor do cofre em todo caminho; teste de round-trip na mesma transação. | Direção do arredondamento em `convert*`, `preview*`, `deposit/mint/withdraw/redeem`. |
| W3-VLT-03 | Defesa contra inflação (virtual shares/offset ou depósito inicial morto) com teste: atacante doa, vítima deposita, perda ≤ limite definido. | Ler a versão instalada do OZ para saber o offset aplicado; teste Foundry. |
| W3-VLT-04 | Nenhum contrato externo usa `preview*` como preço. | Buscar consumidores de `previewRedeem`/`previewWithdraw`. |
| W3-VLT-05 | Invariante: ativos totais coerentes com shares emitidas. | `foundry-testing` modo `invariants`. |

### ERC — padrões de token (V-11)

| ID | Verificação | Como conferir |
| --- | --- | --- |
| W3-ERC-01 | Interfaces e eventos completos; `supportsInterface` correto (ERC-165). | Comparar com a EIP; `Transfer` também em valor zero (ERC-20). |
| W3-ERC-02 | Integração com token arbitrário: não assumir `decimals`, tratar retorno de `transfer`, taxa, rebase e hooks (`SafeERC20`). | Chamadas diretas a `transfer/transferFrom/approve` de tokens externos. |
| W3-ERC-03 | Hooks de recebimento (721/1155) avaliados como superfície de reentrância. | `onERC721Received`, `onERC1155Received`, `_safeMint`, `safeTransferFrom` antes de atualizar estado. |
| W3-ERC-04 | `tokenURI` e metadados são dados externos não confiáveis. | Qualquer decisão on-chain ou off-chain baseada em conteúdo do URI. |

### ORA — oráculos de preço (V-19)

| ID | Verificação | Como conferir |
| --- | --- | --- |
| W3-ORA-01 | Validar `updatedAt` contra limite de idade por feed (heartbeat da página do feed escolhido; não inventar o valor). | `block.timestamp - updatedAt <= limite` presente? O limite tem fonte? |
| W3-ORA-02 | `answer > 0` e `decimals()` lidos do próprio feed; escala explícita ao combinar dois feeds. | Conversões com `1e8`/`1e10` fixos são suspeitas. |
| W3-ORA-03 | Endereço do feed conferido por rede na lista oficial; fallback ou pausa se o feed falhar. | Endereço por chain em config; comportamento em revert. |
| W3-ORA-04 | Preço de pool de DEX com pouca liquidez nunca é fonte única. | Fontes de preço e quem as consome (colateral, liquidação, mint). |
| W3-ORA-05 | Em L2, aplicar `W3-L2-*`. `answeredInRound` está marcado obsoleto na doc atual; não use como controle de idade. | Ver [oraculos-l2-defi.md](oraculos-l2-defi.md). |

### L2 — sequenciador e OP Stack (V-20)

| ID | Verificação | Como conferir |
| --- | --- | --- |
| W3-L2-01 | Liquidações e preços verificam o feed de uptime do sequenciador e um período de carência após o retorno. | Chamada ao feed de uptime e comparação `block.timestamp` com `startedAt`. |
| W3-L2-02 | Não depender de `msg.sender` para identificar contrato L1 sem tratar alias de endereço. | Lógica de acesso vinda de mensagens L1 para L2. |
| W3-L2-03 | Estimar taxa total com a taxa de dados L1, além do gás L2. | Custos assumidos em incentivos/keepers. |
| W3-L2-04 | Não assumir mempool público como proteção contra MEV. | Premissas de front-running. |
| W3-L2-05 | Confirmar finalidade antes de liberar valor (cabeças unsafe/safe/finalized). | Ações irreversíveis ligadas a estado não finalizado. |

### HOOK — hooks do Uniswap v4 e tokens atípicos (V-17)

| ID | Verificação |
| --- | --- |
| W3-HOOK-01 | Callbacks verificam o chamador (PoolManager) por base contract ou checagem explícita. |
| W3-HOOK-02 | Não confiar em qualquer pool: derivar `PoolId` da `PoolKey` e usar allowlist. |
| W3-HOOK-03 | Contabilidade sem mistura de sinal, arredondamento e baldes; testar conservação e round-trips. |
| W3-HOOK-04 | Lógica no hook certo: `beforeSwap` vê o estado anterior, `afterSwap` o posterior. |
| W3-HOOK-05 | Bits do endereço do hook são a API de permissões: alinhados aos callbacks implementados. |
| W3-HOOK-06 | Falhas de código opcional não bloqueiam saída: isolar com `try`/`catch`. |
| W3-HOOK-07 | Estado temporário em chamadas aninhadas: chavear por `PoolId` e chamador, rejeitar operações sobrepostas, limpar. |
| W3-HOOK-08 | Tokens com taxa de transferência: o valor recebido difere do enviado. |
| W3-HOOK-09 | Tokens com rebase: saldo muda sem `Transfer`. |
| W3-HOOK-10 | Tokens com hooks de callback (777, 1363, 721/1155 seguros) como superfície de reentrância. |

### SCN — cenários de incidente como perguntas (V-18)

| ID | Pergunta de revisão |
| --- | --- |
| W3-SCN-01 | Um preço vindo de pool raso pode inflar o valor de colateral e permitir empréstimo sem lastro? |
| W3-SCN-02 | Existe caminho em que mint ou bridge crie ativo sem lastro (falha de encaminhamento, mensagem repetida)? |
| W3-SCN-03 | Chaves de cache ou hashes podem colidir entre entradas distintas? |
| W3-SCN-04 | Assinaturas estão presas a cadeia, contrato, nonce e validade? |
| W3-SCN-05 | Custódia e rotação de chaves: quem pode assinar, com que controle, e como se troca após suspeita? |
| W3-SCN-06 | Serviços de terceiros podem mudar configuração (infraestrutura, produtos de segurança) e abrir caminho de ataque? |

Os cenários vêm de uma listagem jornalística de incidentes; causas podem mudar com post-mortems. Use como pergunta, não como fato.

### SIG — assinaturas e carteiras (V-22)

| ID | Verificação | Como conferir |
| --- | --- | --- |
| W3-SIG-01 | Assinatura presa a cadeia e contrato: domínio EIP-712 com `name`, `version`, `chainId`, `verifyingContract` (e `salt` se usado). | Construção do `DOMAIN_SEPARATOR` e do digest. |
| W3-SIG-02 | Nonce, validade e idempotência no verificador (EIP-712 não protege contra replay); considerar frontrunning de assinatura. | Consumo do nonce; `deadline`; efeito repetido da mesma assinatura. |
| W3-SIG-03 | Dapp trata erros 4001/4100/4900/4901 e reage a `chainChanged` e `accountsChanged`; o Provider é código não confiável. | Handlers no front-end. |
| W3-SIG-04 | Nunca pedir chave privada ou seed ao usuário; os dados exibidos ao assinar batem com o que será executado. | Texto exibido × calldata/estrutura assinada. |

### SVM — Solana/Anchor, cobertura parcial (V-21)

| ID | Verificação |
| --- | --- |
| W3-SVM-01 | Toda conta de entrada tem tipo e constraint; `UncheckedAccount` exige `/// CHECK:` com justificativa e revisão. |
| W3-SVM-02 | `Signer` onde há autoridade. |
| W3-SVM-03 | PDAs com `seeds` e `bump` canônicos. |
| W3-SVM-04 | `init_if_needed` só com defesa contra reuso de conta (a doc não descreve os riscos: **Suposição**). |
| W3-SVM-05 | `realloc` e `close` não esvaziam contas que guardam fundos. |
| W3-SVM-06 | Versão do Anchor conferida (1.0 mudou discriminadores). |

### TST — invariantes e fuzz (V-02)

| ID | Verificação |
| --- | --- |
| W3-TST-01 | Invariantes escritas como propriedades que valem após qualquer sequência de chamadas (conservação, solvência, monotonicidade, limites, acesso); um humano revisa o enunciado. |
| W3-TST-02 | Handler expõe só ações válidas, usa `bound()`, vários atores e contadores por função; nos contadores, toda função alvo foi chamada. |
| W3-TST-03 | Ghosts por fluxo de valor; a invariante compara saldo real com os ghosts. |
| W3-TST-04 | `fail_on_revert` decidido de propósito e documentado (quais reverts são esperados). |
| W3-TST-05 | `runs`, `depth` e `seed` registrados; repetir com outras seeds; falha reproduzida vira teste de regressão. |

### GAS — gás com evidência (V-23)

| ID | Verificação |
| --- | --- |
| W3-GAS-01 | Toda alegação de economia vem com antes e depois (`forge snapshot --diff` ou `--gas-report`) do mesmo teste. |
| W3-GAS-02 | Ganho abaixo do limite acordado não entra. |
| W3-GAS-03 | Otimização nunca troca segurança por gás sem registro; `unchecked` só com prova de limite. |
| W3-GAS-04 | `optimizer_runs` escolhido conforme o perfil de uso e registrado (é estimativa de execuções, não número de passes). |

### AGT — agente, chaves e deploy (V-04, V-05, V-06)

| ID | Verificação |
| --- | --- |
| W3-AGT-01 | Segredos (chave, seed, `.env`) fora do repositório e do contexto; o agente cita só o nome da variável. |
| W3-AGT-02 | Regras `Read(...)` de deny para `.env*`, `secrets/**`, `keys/**` (`.claudeignore` não tem efeito para isso). |
| W3-AGT-03 | `bypassPermissions` e `--dangerously-skip-permissions` desabilitados no repositório. |
| W3-AGT-04 | Deploy, assinatura e envio de fundos são do usuário; deny de comandos que movem fundos, ciente de que o deny de Bash não pega caminho absoluto nem `sh -c`. |
| W3-AGT-05 | Triagem da tríade letal por ferramenta/MCP/skill: lê segredo? processa texto de terceiros? pode enviar rede/transação? Três "sim" = dividir ou bloquear. |
| W3-AGT-06 | Hook de guarda e sandbox de rede como camadas extras, nunca como fronteira única. |

## Critérios de saída por fase

| Fase | Pronto quando |
| --- | --- |
| Escopo | Contratos/diff, cadeia, o que pode ser alterado e versões registrados; sem diff ou sem versão, o relatório diz "Não verificável". |
| Mapa | Tabela entry point × modificador × chamadas externas completa; funções irmãs comparadas. |
| Varredura | Cada área pertinente tem estado por ID; candidatos com ID e `arquivo:linha`. |
| Refutação | Cada candidato mantido ou descartado, com motivo. |
| Prova | Alta severidade tem teste/PoC executado (comando e saída) ou está em "Verificação pendente". |
| Relatório | Achados no formato de [validacao-de-achados.md](validacao-de-achados.md), Cobertura e apêndices A e B presentes. |
| Entrega | Handoff com entregue, verificado/inferido, pendências, riscos e próxima ação. |

## Rótulos epistêmicos aplicados

- Leitura de código não é teste executado. Relatório vazio do Slither não é "sem bugs".
- CI verde com asserção fraca não prova que a invariante cobre a função: confira os contadores.
- Revisão pelo mesmo modelo não é auditoria externa; declare.
- Sem `forge`, `slither` ou RPC disponíveis, marque execuções como **Não verificável** e entregue o comando como proposta.
- Comentário sobre EIP-2612, ERC-1271, malleabilidade de ECDSA, ERC-4337 ou EIP-7702: **Suposição** (fora das fontes lidas).

## Rótulos OWASP SC Top 10 (2025)

Rótulo principal dos achados. Cada um com uma verificação concreta; detalhes em [solidity-seguranca.md](solidity-seguranca.md#mapa-owasp-sc-top-10-2025).

| Rótulo | Tema | IDs relacionados |
| --- | --- | --- |
| SC01 | Controle de acesso | ACC-01..05, UPG-01 |
| SC02 | Manipulação de oráculo | ORA-01..05, L2-01, SCN-01 |
| SC03 | Erros de lógica | VLT-01..05, HOOK-03..07, SCN-02 |
| SC04 | Validação de entrada | SIG-01..02, SVM-01 |
| SC05 | Reentrância | SOL-01, ERC-03, HOOK-10 |
| SC06 | Chamadas externas sem checagem | SOL-02, ERC-02 |
| SC07 | Flash loan | ORA-04, SCN-01 (MEV e flash loan são lacuna L12) |
| SC08 | Overflow/underflow | SOL-06 |
| SC09 | Aleatoriedade insegura | SOL-05 |
| SC10 | Negação de serviço | SOL-04, SOL-09 |
