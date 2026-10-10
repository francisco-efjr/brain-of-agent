# Fontes (bibliografia validada)

Todas as URLs foram abertas pelo validador do segmento em **2026-10-10** (coluna "Consulta"). Este plugin releu em 2026-10-10 apenas a página de configuração de testes do Foundry (`ffi`, chaves de `[fuzz]` e `[invariant]`) e confirmou a existência da página do cheatcode `ffi`. Classe A = documentação oficial ou norma; B = autor ou projeto reconhecido; C = sinal de prática. Metadados de repositório (estrelas, último push, licença) vieram da API pública de busca do GitHub em 2026-10-10. "Licença: destilar" significa que o plugin usa redação própria, sem texto da fonte.

## Sumário

- [Como ler e como citar](#como-ler-e-como-citar)
- [Classe A](#classe-a)
- [Classe B](#classe-b)
- [Classe C, rebaixadas e rejeitadas](#classe-c-rebaixadas-e-rejeitadas)
- [Conteúdo próprio e créditos](#conteúdo-próprio-e-créditos)
- [Lacunas conhecidas](#lacunas-conhecidas)
- [Limites da validação](#limites-da-validação)

## Como ler e como citar

- `V-nn` aponta para o item correspondente da pesquisa deste segmento; cite-o ao justificar uma recomendação.
- Flags, APIs e números de versão mudam: confirme na versão instalada (`forge --version`, `/permissions`, `/hooks`).
- Estrelas e licenças são fotos de 2026-10-10. Estrelas não são prova de qualidade.
- Números de benchmark de terceiros são autorreportados e não entram como argumento de qualidade.

## Classe A

| Item | Título | URL | Licença | Consulta | Uso no plugin |
| --- | --- | --- | --- | --- | --- |
| V-01 | Solidity: Security Considerations | https://docs.soliditylang.org/en/latest/security-considerations.html | não verificada: destilar | 2026-10-10 | SOL-01..09 |
| V-02 | Foundry: Invariant testing; Fuzz testing | https://getfoundry.sh/forge/invariant-testing ; https://getfoundry.sh/forge/fuzz-testing | repositório Apache-2.0 (10.650★, push 2026-10-10); licença do site não verificada | 2026-10-10 | TST-01..05; handler, ghost, `bound()` |
| V-03 | anthropics/claude-code-security-review (command.md, prompts.py, README) | https://raw.githubusercontent.com/anthropics/claude-code-security-review/main/.claude/commands/security-review.md ; https://raw.githubusercontent.com/anthropics/claude-code-security-review/main/claudecode/prompts.py | MIT (6.329★, push 2026-02-11) | 2026-10-10 | Estrutura do revisor reescrito; aviso: a Action não é endurecida contra injeção |
| V-04 | Claude Code: Permissions | https://code.claude.com/docs/en/permissions | doc oficial: destilar | 2026-10-10 | AGT-01..04; deny `Read(...)`; bypass |
| V-05 | Claude Code: Hooks guide | https://code.claude.com/docs/en/hooks-guide | doc oficial: destilar | 2026-10-10 | AGT-06; `PreToolUse`, `exit 2` |
| V-08 | OpenZeppelin Contracts 5.x: Access Control | https://docs.openzeppelin.com/contracts/5.x/access-control | MIT (27.268★, push 2026-10-09) | 2026-10-10 | ACC-01..05 |
| V-09 | OpenZeppelin Upgrades Plugins; Writing upgradeable; README do repositório | https://docs.openzeppelin.com/upgrades-plugins/ ; https://docs.openzeppelin.com/upgrades-plugins/writing-upgradeable | contratos MIT; plugins: não verificada | 2026-10-10 | UPG-01..05 |
| V-10 | EIP-4626; OpenZeppelin ERC4626 | https://eips.ethereum.org/EIPS/eip-4626 ; https://docs.openzeppelin.com/contracts/5.x/erc4626 | EIPs CC0; OZ MIT | 2026-10-10 | VLT-01..05; inflação |
| V-11 | EIP-20; EIP-721; EIP-1155 | https://eips.ethereum.org/EIPS/eip-20 ; https://eips.ethereum.org/EIPS/eip-721 ; https://eips.ethereum.org/EIPS/eip-1155 | CC0 | 2026-10-10 | ERC-01..04 |
| V-19 | Chainlink Data Feeds: using; API reference | https://docs.chain.link/data-feeds/using-data-feeds ; https://docs.chain.link/data-feeds/api-reference | doc de fornecedor: destilar | 2026-10-10 | ORA-01..05 |
| V-20 | Chainlink L2 Sequencer Feeds; Optimism: differences | https://docs.chain.link/data-feeds/l2-sequencer-feeds ; https://docs.optimism.io/stack/differences | não verificada: destilar | 2026-10-10 | L2-01..05 |
| V-21 | Anchor: Account constraints | https://www.anchor-lang.com/docs/references/account-constraints | não verificada: destilar | 2026-10-10 | SVM-01..06 (parcial) |
| V-22 | EIP-1193; EIP-712 | https://eips.ethereum.org/EIPS/eip-1193 ; https://eips.ethereum.org/EIPS/eip-712 | CC0 | 2026-10-10 | SIG-01..04 |
| V-23 | Foundry: Gas tracking; Solidity: optimizer | https://getfoundry.sh/forge/gas-tracking ; https://docs.soliditylang.org/en/latest/internals/optimizer.html | Foundry Apache-2.0; Solidity não verificada | 2026-10-10 | GAS-01..04 |
| V-24 | Claude Code: Sub-agents | https://code.claude.com/docs/en/sub-agents | doc oficial: destilar | 2026-10-10 | Formato de agente; plugins ignoram `hooks`, `mcpServers`, `permissionMode`; aviso sobre `Bash` em revisor |
| V-27 | Claude Code: Best practices | https://code.claude.com/docs/en/best-practices | doc oficial: destilar | 2026-10-10 | Verificação executável, poda de CLAUDE.md, revisor em contexto novo, `/clear` |
| Foundry config | Foundry: Testing configuration | https://getfoundry.sh/reference/config/testing | não verificada | 2026-10-10 (releitura deste plugin) | `ffi = false` por padrão; chaves de `[fuzz]` e `[invariant]` |

## Classe B

| Item | Título | URL | Licença | Consulta | Uso no plugin |
| --- | --- | --- | --- | --- | --- |
| V-06 | Simon Willison: The lethal trifecta (2025-06-16) | https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ | blog: destilar | 2026-10-10 | AGT-05 |
| V-07 | Dan Luu: AI coding; Trail of Bits: Auditing in the age of good-enough AI (2026-09-18) | https://danluu.com/ai-coding/ ; https://blog.trailofbits.com/2026/09/18/auditing-in-the-age-of-good-enough-ai/ | não verificada: destilar | 2026-10-10 | Calibração de auditoria por LLM (a ToB trata de zkVM, não EVM) |
| V-12 | Slither README | https://raw.githubusercontent.com/crytic/slither/master/README.md | AGPL-3.0 (6.374★, push 2026-10-06): só ferramenta, nenhum código copiado | 2026-10-10 | Fluxo de triagem |
| V-13 | OWASP Smart Contract Top 10 (2025); SWC Registry; EthTrust v3 (EEA) | https://owasp.org/www-project-smart-contract-top-10/ ; https://swcregistry.io/ ; https://hub.entethalliance.org/wg-ethtrust-site/spec/v3/ | OWASP BY-SA/NC-SA ambíguo: destilar; EthTrust Apache-2.0; SWC desatualizado | 2026-10-10 | Rótulos SC01..SC10; `swc_id` opcional |
| V-14 | krait (Zealynx Security) README, corroborado por proofhound, gebug-audit, awarexone, RugProof | https://raw.githubusercontent.com/ZealynxSecurity/krait/main/README.md | MIT (23★, push 2026-09-29) | 2026-10-10 | Portões de validação; benchmark cego autorreportado |
| V-16 | plamen README | https://raw.githubusercontent.com/PlamenTSV/plamen/main/README.md | MIT (303★, push 2026-09-26) | 2026-10-10 | Marcador de conclusão, estados de PoC. **Não instalar nem referenciar a instalação** |
| V-17 | Trail of Bits: Building secure Uniswap v4 hooks (2026-07-30) | https://blog.trailofbits.com/2026/07/30/building-secure-uniswap-v4-hooks/ | não verificada: destilar | 2026-10-10 | HOOK-01..07 |
| V-18 | rekt.news (listagem) | https://rekt.news/ | não verificada: destilar | 2026-10-10 | SCN-01..06 como perguntas, não fatos |
| V-25 | awesome-cursorrules `solidity-foundry` (.mdc) | https://raw.githubusercontent.com/PatrickJS/awesome-cursorrules/main/rules/solidity-foundry-cursorrules-prompt-file.mdc | CC0-1.0 (40.891★, push 2026-05-30); só tópicos, reescritos | 2026-10-10 | Tópicos de S01..S07; tom e `ERC20Snapshot` rejeitados |
| V-26 | Trail of Bits: building-secure-contracts; skills; Echidna | https://raw.githubusercontent.com/crytic/building-secure-contracts/master/README.md ; https://raw.githubusercontent.com/trailofbits/skills/main/README.md ; https://raw.githubusercontent.com/crytic/echidna/master/README.md | AGPL-3.0 / CC-BY-SA-4.0: só destilação | 2026-10-10 | Ordem do fluxo de 5 passos; catálogo |

## Classe C, rebaixadas e rejeitadas

| Item | Fonte | Decisão e motivo |
| --- | --- | --- |
| V-15 | gebug-audit (MIT, 4★) e scv-scan (sem licença, 109★) READMEs | Classe C: só padrão corroborado (fases, aprovação de custo). Não copiar scv-scan |
| Rebaixado | wshobson/agents `blockchain-web3` (MIT, 40.318★) | Erros verificados (ethers v5, Goerli, `testFail`, plugin Hardhat descontinuado, `vm.assume`); exemplo do que não copiar |
| Rebaixado | awarexone (MIT, 162★) | Regra das funções irmãs aproveitada; números sem metodologia descartados |
| Rebaixado | decipher-gas-optimizoor (7★, sem licença) | Só a regra de evidência de gás |
| Rebaixado | RugProof, Sperax skills, Demeter claude-solidity-security, farrellh1, proofhound | Pouca tração; instalações inseguras (editam `settings.json`, `curl \| bash`); só padrões |
| Rejeitado | Aboudjem solidity-style-guide | Contradições internas verificadas |
| Rejeitado | iktok90 ai-smart-contract-auditor | Contagens infladas, recall sem dataset; anti-padrão |
| Rejeitado | finite-monkey-engine | Licença conflitante, ganhos sem benchmark |
| Rejeitado | acai-dag-auditor, arbitrum-dapp-skill, glider-skills (não reverificados) | GPL-3.0 / sem licença / pouca tração |
| Rebaixado | MCPs weasel e solidity-audit-mcp (não reverificados) | Instalação por `curl`/dependências |
| Rebaixado | Comentários do HN sobre allowlist | Anedótico; só contexto de V-04/V-05 |
| Candidato futuro | scsfg.io (Smart Contract Security Field Guide) | Existe, não lido; sem licença declarada |

## Conteúdo próprio e créditos

- **brain-of-agent** (francisco-efjr/brain-of-agent, MIT, conteúdo do próprio usuário): estrutura do `WEB3-COMPLETO` (protocolo completo de `brains/fullstack`), `handoff-checkpoint.md`, `adr.md`, `registro-evidencias-qa.md` e a convenção de rótulos epistêmicos, adaptados.
- **gstack** (Garry Tan, MIT): inspiração para "evidência antes de garantia" (`cso`), com atribuição; nada copiado em bloco. Licença em `vendor/gstack/LICENSE` do brain-of-agent.
- **anthropics/claude-code-security-review** (MIT): estrutura do revisor (escopo, contexto, análise por entry point, relatório) reescrita com limiar único e DoS por gás no escopo.
- **krait** (MIT) e **plamen** (MIT): padrões de portões e de conclusão verificável, destilados.
- OWASP, Trail of Bits (Slither, Echidna, building-secure-contracts, skills) e documentações oficiais: apenas destilação, sem texto copiado.

## Lacunas conhecidas

| ID | Lacuna | Comportamento do plugin |
| --- | --- | --- |
| L1 | Descoberta por busca web não ocorreu na pesquisa; uma pesquisa recente da Anthropic sobre agentes explorando contratos é **Não verificável** | Não citar |
| L2 | Indexação (The Graph, reorg/finalidade, Ponder, Envio) | Fora da cobertura; pergunta de revisão sobre finalidade |
| L3 | Hardhat 3 | Foundry-first; dizer que não há fonte validada |
| L4 | Oráculos além de Chainlink (TWAP, Pyth); heartbeat por feed | Mandar consultar a página do feed |
| L5 | EIP-2612, ERC-1271, malleabilidade de ECDSA, ERC-4337, EIP-7702 | Comentário vira **Suposição** |
| L6 | Token Integration Checklist da ToB; "weird ERC20" | Checklist marca o que é V-11 e o que é Suposição |
| L7 | Medusa, Halmos/Certora, Echidna além do README | "A avaliar" |
| L8 | Solana: Sealevel Attacks, Footguns, guia oficial, CPI, Token-2022, Anchor 1.0 notes | `solana-anchor-review` com cobertura parcial |
| L9 | L2: Arbitrum, Base, zk; finalidade e retiradas | Pesquisar por rede; declarar |
| L10 | Foundry: `forge script` com keystore, `cast`, `anvil --fork-url`, `forge verify` | Só a política de recusa |
| L11 | ERC-7201, ERC-1967, ERC-1822 (texto das EIPs) | V-09 sem confirmação direta das EIPs |
| L12 | MEV, front-running, flash loan (Flashbots, commit-reveal, slippage) | Fora da cobertura |
| L13 | Pontes e mensageria cross-chain | Fora da cobertura |
| L14 | Avaliação do próprio plugin; `audit-contracts` e `exploit-poc` sem eval automático | 10 casos de eval; ampliar |
| L15 | Foundry e Slither em Windows | Não verificável; página oficial |
| L16 | Sem benchmark independente de auditoria assistida por LLM | Declarar no README |

## Limites da validação

- Notas D1–D12 dos artefatos coletados são de validador LLM (outro modelo, mas ainda LLM): não são revisão humana nem auditoria externa.
- Páginas longas lidas em parte (Dan Luu 100 mil de 110.862 caracteres; OZ ERC20 100 mil de 116.972; sub-agents 100 mil de 108.415; EthTrust v3 só cabeçalho e níveis).
- Sintaxe de `allowed-tools` em skills, de `tools` com restrição fina de Bash em agentes e do JSON de hooks é **Inferida**: confira com `claude plugin validate` e `/permissions`/`/hooks`.
- Cheatcodes de teste unitário (`vm.expectRevert`, `vm.prank`, `vm.expectEmit`, `vm.createSelectFork`, `vm.envString`, `makeAddr`, `bound`) e `StdInvariant` são conhecimento estável do Foundry/forge-std, **Inferido**: nomes não confirmados linha a linha na documentação nesta sessão; confira no `Vm.sol` da versão instalada.
