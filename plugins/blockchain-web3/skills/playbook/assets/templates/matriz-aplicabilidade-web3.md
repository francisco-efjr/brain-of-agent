# Matriz de aplicabilidade (WEB3-COMPLETO)

Modelada a partir do protocolo completo do brain-of-agent (MIT). "Completo" é cobertura desta matriz com limitações honestas, não caixas artificialmente verdes. Estados: **Aplica** · **Não aplica** (motivo obrigatório) · **Lacuna** (área sem fonte validada neste plugin). Sem acesso ou ferramenta: Não verificável.

## Inventário de leitura (registrar por arquivo)

| Arquivo | Estado (lida / parcial / ausente) | Decisão extraída |
| --- | --- | --- |
| `references/checklist-completo.md` | | |
| `references/solidity-seguranca.md` | | |
| `references/padroes-erc-e-assinaturas.md` | | |
| `references/oraculos-l2-defi.md` | | |
| `references/foundry-testes-gas.md` | | |
| `references/validacao-de-achados.md` | | |
| `references/decisoes-e-tradeoffs.md` | | |
| `references/seguranca-do-agente-e-chaves.md` | | |
| `references/padroes-e-antipadroes.md` | | |
| `references/claude-md-snippets.md` | | |
| `references/ferramentas-e-mcp.md` | | |
| `references/fontes.md` | | |
| `skills/solana-anchor-review/references/solana-anchor.md` | | |
| 10 templates em `assets/templates/` | | |

Arquivo ausente ou ilegível torna a cobertura **parcial**, nunca integral.

## Matriz

| Área | Aplica / Não aplica / Lacuna | Justificativa | Skill ou agente | Evidência |
| --- | --- | --- | --- | --- |
| Contratos EVM (SOL) | | | `contract-security-review` | |
| Tokens e ERC (ERC, VLT) | | | `token-standards-review` | |
| Controle de acesso (ACC) | | | `contract-security-review` | |
| Upgradeability (UPG) | | | `contract-security-review` | |
| Oráculos (ORA) | | | `defi-oracle-l2-review` | |
| L2 (L2) | | | `defi-oracle-l2-review` | |
| Assinaturas e carteiras (SIG) | | | `wallet-signing-review` | |
| Hooks/AMM (HOOK) | | | `defi-oracle-l2-review` | |
| Cenários de incidente (SCN) | | | `defi-protocol-analyst` | |
| Testes e invariantes (TST) | | | `foundry-testing` | |
| Gás (GAS) | | | `foundry-testing` | |
| Solana/Anchor (SVM) | | parcial por definição | `solana-anchor-review` | |
| Segurança do agente e chaves (AGT) | | | `web3-agent-safety-auditor` | |
| Indexação (reorg, finalidade) | Lacuna | sem fonte validada (L2) | — | |
| Hardhat | Lacuna | sem fonte validada (L3) | — | |
| MEV e flash loan em profundidade | Lacuna | L12 | — | |
| Pontes e mensageria cross-chain | Lacuna | L13 | — | |
| Relayers, keepers e bots off-chain | Lacuna | fora de escopo (`backend-api`, `automation-integrations`) | — | |

## Fechamento

Resultado: **concluído no escopo** · **parcial** · **impedido**. Falta de leitura obrigatória, de execução material ou de revalidação torna o modo parcial. Média de notas não compensa falha crítica. Nunca escreva "auditoria completa aprovada" com leitura ou execução parcial. Revisão por quem implementou é autoavaliação.
