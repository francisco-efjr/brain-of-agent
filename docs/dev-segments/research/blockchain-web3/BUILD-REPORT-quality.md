# BUILD-REPORT de qualidade: blockchain-web3

Data: 2026-10-10 · Papel: validador independente de qualidade de prompt e conteúdo técnico · Plugin: `C:\Users\Francisco Edson\dev-segments\plugins\blockchain-web3`
Rubrica: `docs/foundation/prompt-quality-rubric.md` (D1–D12, 0–100). Rótulos: **Verificado** (lido ou executado nesta sessão), **Inferido**, **Suposição**, **Não verificável**.

Declaração de independência: os construtores foram outro modelo, mas o validador é da mesma família de modelos Claude. Pontos cegos compartilhados são possíveis; as notas D1–D12 são julgamento por leitura, não medição, e não equivalem a auditoria externa nem à execução dos evals (todos `designed_not_executed`).

## 1. Resumo

- Lidos por inteiro: README, `plugin.json`, os 10 `SKILL.md`, os 5 agentes, `evals/README.md` e os 12 casos originais (prompt + graders), `ferramentas-e-mcp.md`, `seguranca-do-agente-e-chaves.md`, `claude-md-snippets.md`, `solidity-seguranca.md`, `padroes-e-antipadroes.md` (parte), `eip712-replay.md`, `oraculo-e-sequenciador.md`, `erc4626-inflacao.md`, `hooks-v4-e-cenarios.md`, `foundry-toml-e-comandos.md`, `modo-gas.md`, `modo-unit-e-fork.md`, `handler-invariante-exemplo.md`, `poc-fork-exemplo.md`, `exemplo-reentrancia-com-injecao.md`, `calibracao-de-severidade.md`, `sinais-por-classe.md`, `fases-e-marcadores.md` (início), 3 templates.
- Biblioteca de prompts: amostra de 17 prompts lidos por inteiro (P01, P02, P03, P08, P09, P10, P11, P12 e P21 a P29), acima do mínimo de 10.
- Não lidos linha a linha: P04 a P07, P13 a P20 (só índice e estrutura), `checklist-completo.md`, `fontes.md`, `decisoes-e-tradeoffs.md`, `padroes-erc-e-assinaturas.md`, `oraculos-l2-defi.md`, `foundry-testes-gas.md`, `validacao-de-achados.md` (parte), `checklist-erc.md`, `solana-anchor.md`, `provider-eip1193.md`, `slither-e-triagem.md`, 7 dos 10 templates. Nota para esses: Suposição (herdam o padrão dos lidos; a estrutura foi conferida por `verify_plugin.py`).
- Média antes: 88,7 · depois: 90,1 · mínimo depois: 86 (`solana-anchor-review`, limitado por D12 por cobertura declaradamente parcial) · nenhum item abaixo de 80 antes ou depois · nenhum critério de reprovação automática encontrado.
- Verificadores no fim: `verify_plugin.py` PASS (10 skills, 5 agents, 15 evals, 104 arquivos) e `claude plugin validate` "Validation passed" (Verificado).

## 2. Tabela arquivo | antes | depois | correções

| Arquivo | Antes | Depois | Correções |
| --- | --- | --- | --- |
| `skills/playbook/SKILL.md` | 90 | 90 | Sem alteração. Gatilhos PT/EN, exclusões ("assinatura" de SaaS), princípios com porquê, modo `WEB3-COMPLETO` com ativação restrita, gates e matriz |
| `skills/prompts/SKILL.md` | 91 | 91 | Sem alteração |
| `skills/contract-security-review/SKILL.md` | 88 | 90 | Passo 6 reconciliado com o portão estrito: revisão rápida põe no corpo o achado de cadeia completa rotulado Inferido; "só PoC-passed no corpo" vale em `audit-contracts`. "NÃO" em caixa alta virou minúscula |
| `skills/token-standards-review/SKILL.md` | 90 | 90 | Sem alteração |
| `skills/defi-oracle-l2-review/SKILL.md` | 90 | 90 | Sem alteração |
| `skills/wallet-signing-review/SKILL.md` | 89 | 90 | "achado crítico" (fora da escala Alta/Média/Baixa) trocado por "severidade Alta" |
| `skills/foundry-testing/SKILL.md` | 90 | 90 | Sem alteração |
| `skills/exploit-poc/SKILL.md` | 89 | 90 | SKILL sem alteração; o modelo de PoC referenciado tinha erro de saldo (ver `poc-fork-exemplo.md`) |
| `skills/audit-contracts/SKILL.md` | 90 | 90 | Sem alteração |
| `skills/solana-anchor-review/SKILL.md` | 86 | 86 | Sem alteração. Cobertura parcial declarada no topo de todo relatório; D12 limitado pela fonte única (V-21) |
| `agents/solidity-security-reviewer.md` | 91 | 91 | "NÃO" em caixa alta removido. Somente leitura (`Read, Grep, Glob`) |
| `agents/finding-refuter.md` | 92 | 92 | Idem |
| `agents/invariant-test-engineer.md` | 84 | 90 | Exemplo de invariante `invariant_callSummary` com `assertGt` podia falhar de forma espúria logo na primeira chamada (chamada revertida descartada com `fail_on_revert = false`, contadores em zero). Trocado por `afterInvariant()` com `console.log` dos contadores, mais o aviso do porquê; import de `console` acrescentado; passo 7 ajustado |
| `agents/defi-protocol-analyst.md` | 90 | 90 | Sem alteração |
| `agents/web3-agent-safety-auditor.md` | 86 | 91 | JSON de permissões propunha `Bash(slither *)` pré-aprovado, em conflito com `audit-contracts` ("cada execução passa pela confirmação") e com `ferramentas-e-mcp.md` ("o plugin não pré-aprova"). Removido, com a razão (o Slither compila o projeto e pode acionar o build do framework, isto é, código do repositório). "NÃO" em caixa alta removido |
| `skills/prompts/references/prompt-library.md` (P01–P20) | 90 | 91 | "NÃO" em caixa alta removidos; exemplos P01 conferidos (linhas 8 e 10 do contrato batem com o cenário) |
| `skills/prompts/references/prompt-library-processo.md` (P21–P29) | 87 | 91 | CAPS removidos: "NÃO leia" (P24), "Você NÃO faz deploy" (P27), "PEÇA aprovação" (P22) |
| `evals/` (12 casos originais, 15 depois) | 87 | 89 | 3 casos novos preenchendo lacunas apontadas pelo validador estrutural: `poc-without-executor` (PoC sem executor, `needs-execution`), `agent-settings-triage` (settings com bypass e deny vazio, tema do `web3-agent-safety-auditor`), `web3-completo-explicit` (caso positivo da keyword). Todos com PASS/FAIL observáveis e `no-env-read`/`skill-fired` quando cabe. `evals/README.md` atualizado (contagem, custo 45 execuções, cobertura) |
| `README.md` | 88 | 89 | Limitação sobre evals de `audit-contracts` e `exploit-poc` atualizada para refletir o novo caso |
| `skills/playbook/references/ferramentas-e-mcp.md` | 86 | 90 | `Bash(slither *)` removido do JSON de permissões, nota 5 reescrita; hook `web3_guard.py` bloqueava a leitura de `script/Deploy*.s.sol`, que o agente de segurança precisa ler: o padrão passou a valer só para `Edit` e `Write` |
| `skills/contract-security-review/references/exemplo-reentrancia-com-injecao.md` | 84 | 90 | Teste proposto não funcionava: `vm.deal(address(this), 5 ether)` deixava o contrato de teste com 0 ETH depois do depósito da vítima, então `attack{value: 1 ether}` falharia por falta de saldo. Agora o teste recebe 6 ETH e o atacante começa com 0 (saldo final 6 ETH confere) |
| `skills/exploit-poc/references/poc-fork-exemplo.md` | 83 | 90 | O PoC dava 1 ETH ao atacante com `vm.deal` e mais 1 ETH por `msg.value`: saldo final 7 ETH, e a asserção `== 6 ether` falharia. `vm.deal` do atacante removido nos dois testes (ataque e correção) |
| `skills/foundry-testing/references/handler-invariante-exemplo.md` | 89 | 90 | `invariant_callSummary` (função de invariante só com log, executada após cada chamada) virou `afterInvariant()`; texto da seção 5 alinhado |
| `references` Foundry (`foundry-toml-e-comandos`, `modo-gas`, `modo-unit-e-fork`) | 90 | 90 | Sem alteração; flags e cheatcodes coerentes com o Foundry estável (Inferido) |
| `wallet-signing-review/references/eip712-replay.md` | 90 | 90 | Sem alteração; código conferido (domínio OZ, `_useNonce`, `ECDSA.recover`) |
| `defi-oracle-l2-review/references/oraculo-e-sequenciador.md` | 91 | 91 | Sem alteração; escalas de `decimals`, carência e `startedAt == 0` conferidas |
| `token-standards-review/references/erc4626-inflacao.md` | 91 | 91 | Sem alteração; aritmética do ataque (0 shares; variação 15.000e18 com perda de 2.500e18) recalculada e correta |
| `playbook/references/solidity-seguranca.md` | 90 | 90 | Sem alteração |
| `seguranca-do-agente-e-chaves.md` e `claude-md-snippets.md` | 90 | 90 | Sem alteração |
| Templates amostrados (`relatorio-de-achados`, `matriz-aplicabilidade-web3`, `checklist-pre-deploy-usuario`) | 89 | 89 | Sem alteração |

## 3. Fidelidade técnica (conferida contra fonte oficial nesta sessão)

| Afirmação | Fonte | Resultado |
| --- | --- | --- |
| `startedAt` do feed do sequenciador retorna 0 só na Arbitrum quando o contrato de uptime não foi inicializado; resposta 0 = no ar, 1 = fora | https://docs.chain.link/data-feeds/l2-sequencer-feeds | **Verificado** |
| OpenZeppelin 5.0.0 removeu `ERC20Snapshot`; `ReentrancyGuard` e `Pausable` foram movidos para `utils` | https://raw.githubusercontent.com/OpenZeppelin/openzeppelin-contracts/master/CHANGELOG.md (seção 5.0.0; li os primeiros 100 mil de 156 mil caracteres) | **Verificado** |
| EIP-4626: `preview*` manipulável e não seguro como oráculo; `convert*` pode ser oráculo robusto, com TWAP | https://eips.ethereum.org/EIPS/eip-4626 (Security Considerations) | **Verificado** |
| Subagentes de plugin ignoram `hooks`, `mcpServers` e `permissionMode` | https://code.claude.com/docs/en/sub-agents | **Verificado** |
| O campo `tools` de subagente aceita só nomes de ferramenta; restrição de `Bash` por padrão de comando exige regra de deny/allow nas configurações ou hook | idem | **Verificado**. Consequência: `invariant-test-engineer` com `Bash` amplo depende de instrução (já declarado no agente) |
| Anchor: `dup`, `init_if_needed`, discriminador pré-1.0 | `VALIDATED.md` (V-21) | **Verificado** contra o arquivo de validação, não reconferido na página do Anchor |
| Alias de endereço OP Stack, `COINBASE`, `PUSH0` | `VALIDATED.md` (V-20) | Não reconferido na página do Optimism |

Nenhuma afirmação técnica errada foi encontrada nos textos; os erros achados estavam em código de exemplo (saldos, invariante de cobertura), não em prosa.

## 4. Direitos autorais e segurança

- Literal: só texto de redação própria do projeto e do brain-of-agent (MIT), com atribuição; fontes AGPL, CC-BY-SA e OWASP aparecem destiladas, conforme `README.md` e `prompt-library.md`. Nenhum trecho de terceiros acima de 40 linhas encontrado nos arquivos lidos. Não verificado nos arquivos não lidos.
- Segredos: nenhum valor secreto; as URLs de exemplo usam `example.invalid`, `0x...01` e a palavra `CHAVE-DE-EXEMPLO` (caso de eval).
- Fluxos destrutivos ou externos: nenhum autoriza deploy, assinatura, `--broadcast` ou leitura de `.env`; `exploit-poc` e `audit-contracts` têm `disable-model-invocation: true`; revisores (`solidity-security-reviewer`, `finding-refuter`, `defi-protocol-analyst`, `web3-agent-safety-auditor`) têm só `Read, Grep, Glob`.
- Conteúdo externo como dado: presente em todas as skills e agentes; o exemplo de injeção em NatSpec (`exemplo-reentrancia-com-injecao.md`) e o comentário do eval `reentrancy-with-injection` são fixtures declaradas, tratadas como dado.
- Evals: PASS/FAIL observáveis em todos; casos negativos presentes (`negative-unrelated-request`, `keyword-in-readme-does-not-activate`).
- Bypass: citado só como risco; nenhuma recomendação como padrão.

## 5. Pendências

1. **Evals não executados** (todos os 15). Nenhuma taxa de acerto pode ser alegada; rodar `claude plugin eval .` com Claude Code 2.1.269 ou superior e ler transcritos antes de confiar nos juízes LLM.
2. **`invariant-test-engineer` com `Bash` amplo** (limite do formato: `tools` não restringe por padrão de comando e plugins ignoram hooks). Mitigação do usuário: regras de deny/allow em `settings.json` (documentadas); decisão de manter o agente com `Bash` é do dono do plugin.
3. **Sem caso de eval** para `finding-refuter`, `invariant-test-engineer`, `defi-protocol-analyst` (delegação via `Agent`), `audit-contracts` e triagem do Slither; exigiriam `allowed_tools` com `Agent`/`Bash` ou fixtures de arquivos.
4. **Referências não lidas linha a linha** (lista na seção 1): recomenda-se uma segunda leitura de `checklist-completo.md`, `oraculos-l2-defi.md`, `padroes-erc-e-assinaturas.md`, `foundry-testes-gas.md` e `solana-anchor.md`, em especial os trechos de código.
5. **Cobertura declaradamente parcial**: Solana/Anchor (só constraints), Hardhat, indexação, MEV, pontes, TWAP/Pyth, L2 além de OP Stack, EIP-2612, ERC-1271, ERC-4337, EIP-7702, Vyper. Decisão de ampliar é do dono; o plugin rotula como Suposição ou "fora da cobertura".
6. **Windows**: comportamento de Foundry e Slither, e da sandbox de Bash, segue Não verificável.
7. Datas de incidentes do `rekt.news` (V-18) e posts de 2026 do Trail of Bits (V-17) não foram reconferidos nesta sessão (Não verificável).
8. Os eval prompts novos usam `model: sonnet` e `runs: 3` como os demais; o caso `web3-completo-explicit` tem `max_turns: 20` e `timeout_seconds: 900`, valores a ajustar após a primeira rodada.
