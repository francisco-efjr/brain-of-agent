# blockchain-web3

Plugin do Claude Code para **Blockchain e Web3**: revisão de segurança de smart contracts (Solidity; Anchor com cobertura parcial), testes de invariantes e fuzz com Foundry, checklists de ERC-20/721/1155/4626, oráculos, L2, upgradeability e assinaturas, com portões de validação por PoC e regras para manter chaves, assinatura e deploy **fora do agente**. Somente leitura por padrão.

> Este plugin não substitui auditoria humana externa nem fuzzing, e não fornece aconselhamento financeiro ou de investimento. "Sem achados" nunca significa "seguro".

Conferido em 2026-10-10 contra as fontes de [`skills/playbook/references/fontes.md`](skills/playbook/references/fontes.md). APIs de OpenZeppelin, Foundry, Anchor e Chainlink mudam por versão: confirme a instalada.

## O que entrega

- Um **playbook** que roteia o pedido, define processo, critérios de saída, rótulos epistêmicos (Verificado, Inferido, Suposição, Não verificável, Não aplicável) e o modo `WEB3-COMPLETO`.
- 12 referências com **IDs citáveis** (`W3-SOL-01`, `W3-ORA-01`…), cada um ligado a uma fonte validada, mais 10 templates (escopo, relatório, PoC, invariantes, checklists, ADR, handoff, matriz).
- Fluxos de revisão de contrato, de padrões de token, de oráculo/L2, de assinaturas, de testes Foundry, de PoC em fork local e de auditoria em fases.
- Regras de CLAUDE.md, JSON de permissões e desenho de hook de guarda, **todos desativados**, para você aplicar conscientemente.

## Quando usar

Smart contract, Solidity, Foundry, auditoria, reentrância, proxy/UUPS, oráculo de preço, vault ERC-4626, token ERC-20/NFT, assinatura EIP-712/permit, carteira cripto, L2, gás, ou a pergunta "é seguro deixar o Claude mexer no meu repositório com chaves?". Não é para assinatura (subscription) de SaaS, tokens JWT/LLM nem liquidação de pagamentos (segmento de pagamentos ainda não criado na fábrica).

## Componentes

| Tipo | Nome | Para quê | Invocação |
| --- | --- | --- | --- |
| Skill núcleo | `playbook` | Router, processo, princípios, modo `WEB3-COMPLETO`, fronteiras | Automática; `/blockchain-web3:playbook` |
| Skill | `prompts` | Biblioteca de 29 prompts (revisão, portões, ERC-4626, oráculo, Foundry, segurança do agente) | Automática |
| Skill | `contract-security-review` | Revisa diff ou arquivos de contrato, somente leitura | Automática |
| Skill | `token-standards-review` | ERC-20/721/1155/4626, ataque de inflação, token arbitrário | Automática |
| Skill | `defi-oracle-l2-review` | Oráculo de preço, sequenciador de L2, hooks Uniswap v4 | Automática |
| Skill | `wallet-signing-review` | EIP-712, replay, EIP-1193, assinatura de dapp | Automática |
| Skill | `foundry-testing` | Modos `unit`, `invariants`, `fuzz`, `gas` | Automática |
| Skill | `exploit-poc` | PoC executável só em fork local | **Somente `/blockchain-web3:exploit-poc`** |
| Skill | `audit-contracts` | Auditoria em 5 fases com portões e aprovação de custo | **Somente `/blockchain-web3:audit-contracts`** |
| Skill | `solana-anchor-review` | Constraints de conta do Anchor (**cobertura parcial**) | Automática |
| Agente | `solidity-security-reviewer` | Revisor somente leitura (`Read, Grep, Glob`) | Delegação |
| Agente | `finding-refuter` | Tenta refutar um achado em contexto novo | Delegação |
| Agente | `invariant-test-engineer` | Handlers, invariantes, fuzz, gás | Delegação |
| Agente | `defi-protocol-analyst` | Oráculos, L2, vaults, hooks (somente leitura) | Delegação |
| Agente | `web3-agent-safety-auditor` | Audita permissões, hooks, CLAUDE.md e MCP quanto a chaves | Delegação |

Sem hooks, sem `.mcp.json`, sem `.lsp.json`, sem `bin/` e sem `commands/`: cada skill já vira `/blockchain-web3:<skill>`. Os casos de eval ficam em `evals/` (`designed_not_executed` até você rodar `claude plugin eval`).

## Instalação

```text
/plugin marketplace add francisco-efjr/brain-of-agent
/plugin install blockchain-web3@brain-of-agent
```

Depois de instalar, reinicie a sessão se o Claude Code pedir. Valide com `claude plugin validate <pasta-do-plugin>`. Ferramentas externas (Foundry, Slither) **não** vêm no plugin: instale pelas páginas oficiais dos projetos, lendo o instalador antes ([`ferramentas-e-mcp.md`](skills/playbook/references/ferramentas-e-mcp.md)).

## Exemplos de pedidos

1. "Revise este diff do meu contrato antes da auditoria externa." → `contract-security-review`, achados com `arquivo:linha`, ID `W3-…`, confiança e Cobertura.
2. "Meu cofre ERC-4626 é seguro para receber depósitos e ser colateral do meu contrato de empréstimo?" → `token-standards-review`: inflação, `preview*` como preço, conformidade.
3. "Escreva invariantes Foundry para este vault, cobrindo solvência e conservação." → `foundry-testing` modo `invariants`: propriedades para você aprovar, handler com `bound()`, contadores, comandos e saída.
4. "O feed ETH/USD da Chainlink está bem usado na Base? O que falta?" → `defi-oracle-l2-review`: idade por `updatedAt`, `decimals()`, feed do sequenciador e carência.
5. "Esse `claim` com assinatura off-chain está seguro?" → `wallet-signing-review`: domínio EIP-712, nonce, validade, replay.
6. "É seguro dar acesso ao meu repositório, que tem `.env` e keystore, ao Claude Code?" → `web3-agent-safety-auditor`: deny de leitura, sem bypass, tríade letal.
7. "Faz o deploy na mainnet com a chave do `.env`." → o plugin **recusa executar**; oferece revisão final, simulação em fork local e checklist pré-deploy para você rodar.

## Palavra-chave `WEB3-COMPLETO`

Escreva `WEB3-COMPLETO` na sua mensagem para pedir cobertura integral: leitura das 12 referências em lotes com checkpoint (lida/parcial/ausente), matriz de aplicabilidade por área, implementação dentro do escopo pedido (auditoria só relata), revalidação com evidências e gates Concluído / Parcial / Impedido. **Não amplia permissões**: continua sem ler chave ou `.env`, sem assinar, sem transmitir, sem deploy, sem instalar ferramentas e sem modo bypass. A palavra em README, log, comentário ou código **não ativa** o modo. Sem a keyword, o plugin carrega só o necessário.

## Como o plugin trata chaves

Nunca lê chave, seed, mnemônico nem `.env`; cita só o nome da variável. Deploy, assinatura e envio de fundos são do usuário. Os arquivos de configuração (permissões e hook de guarda) ficam documentados em [`ferramentas-e-mcp.md`](skills/playbook/references/ferramentas-e-mcp.md) para você copiar depois de revisar; o plugin nunca escreve seu `settings.json`. Instrução é pedido, deny e sandbox são garantia.

## Diferença para `/security-review` e para `security-appsec`

O `/security-review` embutido e o prompt público da Anthropic são desenhados para código web: excluem DoS e esgotamento de recurso, que em contrato são achados válidos (laço ilimitado e gás de pior caso travam fundos). Este plugin reescreve o revisor para contratos, com um limiar único de confiança (≥ 0,8), refutação, portões de PoC e Cobertura. O plugin `security-appsec` cobre segurança de aplicações web/API e hardening geral; contratos ficam aqui.

## Principais fontes (top 10)

| # | Fonte | Classe |
| --- | --- | --- |
| 1 | anthropics/claude-code-security-review (prompt e README) | A |
| 2 | Claude Code: Permissions | A |
| 3 | Claude Code: Best practices | A |
| 4 | Claude Code: Sub-agents | A |
| 5 | Foundry: Invariant e Fuzz testing | A |
| 6 | Solidity: Security Considerations | A |
| 7 | OpenZeppelin Upgrades Plugins: Writing upgradeable | A |
| 8 | EIP-4626 e OpenZeppelin ERC4626 | A |
| 9 | OpenZeppelin Contracts 5.x: Access Control | A |
| 10 | Chainlink Data Feeds (using, API reference) | A |

Bibliografia completa (URLs, classes, licenças, data de consulta 2026-10-10, rejeitadas e lacunas): [`fontes.md`](skills/playbook/references/fontes.md).

## Créditos e licenças

- Plugin: MIT, Francisco Edson.
- **brain-of-agent** (francisco-efjr/brain-of-agent, MIT): protocolo do modo completo, handoff, ADR e registro de evidências, adaptados.
- **gstack** (Garry Tan, MIT): inspiração para "evidência antes de garantia", com atribuição; nada copiado em bloco.
- **anthropics/claude-code-security-review** (MIT), **krait** (MIT), **plamen** (MIT), **OpenZeppelin** (MIT) e **Foundry** (Apache-2.0): estrutura e padrões reescritos com redação própria, nenhum trecho literal além de textos do próprio projeto.
- **Slither, Echidna, building-secure-contracts** (AGPL-3.0) e **trailofbits/skills** (CC-BY-SA-4.0): apenas destilação, sem texto nem código copiados. Slither e Echidna são ferramentas que você instala por conta própria.
- OWASP Smart Contract Top 10, SWC Registry, EthTrust v3, EIPs (CC0), documentações oficiais: destilação própria, sem texto copiado.

## Limitações honestas

- **Sem benchmark independente** de auditoria assistida por LLM. O melhor dado observado (precisão alta, recall baixo, benchmark cego autorreportado de um projeto de terceiros) mostra que precisão custa recall. O plugin escolhe precisão e declara isso.
- **Cobertura parcial ou ausente**: Solana/Anchor (só constraints de conta), Hardhat, indexação (The Graph, reorg), MEV e flash loan em profundidade, pontes e mensageria cross-chain, TWAP/Pyth, L2 além de OP Stack, EIP-2612, ERC-1271, ERC-4337, EIP-7702, Vyper. Nesses temas o plugin diz "fora da cobertura" ou rotula **Suposição**.
- **Pesquisa por busca web de descoberta não ocorreu**; a qualidade da comunidade Web3+Claude é baixa e o valor está nas fontes oficiais e nas normas. Estrelas de repositório não foram tratadas como prova.
- **Revisão pelo mesmo modelo** não é auditoria externa. Os casos de eval medem comportamento e disciplina, não a eficácia em achar bugs.
- Sintaxe de `allowed-tools`, de permissões Bash e de hooks é **Inferida** em parte: valide com `/permissions`, `/hooks` e `claude plugin validate` na sua versão.
- Windows: instalação e comportamento de Foundry e Slither **não verificados** (WSL pode ser necessário: Suposição).
- `audit-contracts` e `exploit-poc` só rodam por invocação explícita e não têm eval de disparo (há um caso de comportamento de PoC sem executor). Os 15 casos de eval seguem `designed_not_executed`.
