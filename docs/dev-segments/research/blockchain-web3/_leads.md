# blockchain-web3 — pistas do atlas global

Data: 2026-10-09 · Indexador do atlas (Claude Sonnet 5.5) · Origem: `docs/research/_global/*.validated.md` (IDs: AO, EC, CT, PC, CP, BR).
Cobertura do atlas: uma única fonte específica (Solidity + Foundry). Princípios comuns: `docs/foundation/prompt-principles.md`.

## 1. Pistas aprovadas aplicáveis

| Pista | URL | Classe | O que aproveitar |
| --- | --- | --- | --- |
| Solidity + Foundry .mdc (CT-09) | https://github.com/PatrickJS/awesome-cursorrules | B (6) | Checks-Effects-Interactions + ReentrancyGuard, AccessControl, pull-over-push, custom errors, eventos, Solidity ≥ 0.8; fuzz/invariantes/fork tests; Slither/Mythril; alerta se chave privada fora de `.env`. CC0; literais Verificados. Sem SWC/ERCs; conferir versões de OpenZeppelin e Foundry. |
| Trail of Bits skills (EC-12) | https://github.com/trailofbits/skills | B (6) | `building-secure-contracts`, static-analysis, variant-analysis, differential-review. CC-BY-SA-4.0 (7.455★, Verificado): destilar sem texto literal. |
| wshobson/agents, `blockchain-web3` (EC-10) | https://github.com/wshobson/agents | B | Plugin citado; abrir e verificar. MIT. |
| claude-code-security-review (AO-24) | https://github.com/anthropics/claude-code-security-review | A | Metodologia de achados (confiança > 80%, JSON, exploit_scenario) aplicável a contratos. MIT. |
| security-and-owasp (CT-16) | https://github.com/github/awesome-copilot | B | Molde `ID · severidade · detecção · referência · correção`; "Always verify webhook signatures". MIT. |
| security-devsecops (CT-13) | https://github.com/PatrickJS/awesome-cursorrules | B | Sem segredos hardcoded. CC0. |
| Willison, lethal trifecta (PC-21) | https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ | A | Agentes com chaves e carteiras: nunca combinar dados privados + conteúdo não confiável + saída externa. |
| Dan Luu e vozes críticas (CP-20) | https://danluu.com/ai-coding/ | B | Fuzzing vence LLM em busca de bugs; variância alta: auditoria por LLM exige ≥ 3 execuções. |
| Boris Cherny, allowlist (CP-01) | https://news.ycombinator.com/item?id=46470017 | A | Evitar `--dangerously-skip-permissions`. |
| Hooks guardrail (CP-19) | https://aitmpl.com/blog/secure-git-workflow/ | B | Negar leitura de `.env` e comandos destrutivos; reescrever em stdlib. |
| NestJS anti-hallucination (CT-08) | https://github.com/PatrickJS/awesome-cursorrules | B | Padrão "tabela de substitutos por versão" transferível a ethers/viem/OpenZeppelin (Inferido). |

## 2. Repositórios e arquivos a abrir
- `PatrickJS/awesome-cursorrules/rules/solidity-foundry-cursorrules-prompt-file.mdc`.
- `trailofbits/skills` (building-secure-contracts, static-analysis).
- `wshobson/agents/plugins/blockchain-web3`.
- SWC Registry, EIPs/ERCs, Foundry Book, OpenZeppelin docs, Anchor/Solana, Slither não estão no atlas (SWC e Foundry citados só como semente): lente authoritative.
- awesome-copilot não cobre blockchain (CT-14).

## 3. Materiais oficiais Anthropic pertinentes
AO-24 (security-review), AO-23, AO-30 (`claude-security`, verificadores independentes que refutam achados), AO-29.

## 4. Padrões da comunidade
- Nenhum padrão aprovado. O item r/ethdev (skill multiagente de auditoria Solidity) foi rejeitado (CP-29): 3 pontos, repo não localizado.
- Princípio mantido só como Suposição: inventário de entry points, PoC executável, nunca descartar em silêncio.

## 5. O que o brain-of-agent já oferece
- `brain_refs` vazio: sem brain específico (BR transversais: web3 praticamente nulo).
- Transversais: BR-14 (OWASP Top 10:2025), BR-22 (cobertura declarada estática vs runtime; `/cso`), BR-16 (formato de achado), BR-26 (credenciais nunca passam pelo agente).
- BR-03: modo `WEB3-COMPLETO`.

## 6. Lacunas e cuidados
- Sem fonte para oráculos, upgradeability, ERC (20/721/1155/4626), gas, L2, wallets, indexação, DeFi, Solana/Anchor.
- Única fonte específica é regra comunitária CC0 de qualidade B.
- Nunca manipular chaves privadas, seeds ou transações reais; deploy e assinatura só pelo usuário.
