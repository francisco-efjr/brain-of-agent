# security-appsec — pistas do atlas global

Data: 2026-10-09 · Indexador do atlas (Claude Sonnet 5.5) · Origem: `docs/research/_global/*.validated.md` (IDs: AO, EC, CT, PC, CP, BR).
Pista é ponto de partida: reabrir a URL antes de citar. Princípios comuns: `docs/foundation/prompt-principles.md`.

## 1. Pistas aprovadas aplicáveis

| Pista | URL | Classe | O que aproveitar |
| --- | --- | --- | --- |
| claude-code-security-review (AO-24) | https://github.com/anthropics/claude-code-security-review | A | Foco no que a PR introduz, confiança > 80%, "melhor perder issues teóricas que inundar de falsos positivos", saída JSON (file, line, severity, category, description, exploit_scenario, recommendation, confidence), filtro de falsos positivos. MIT; 6.329★; push 2026-02-11; atribuição obrigatória; README admite não ser endurecido contra prompt injection. |
| Segurança, auto mode, security-guidance (AO-23) | https://code.claude.com/docs/en/security | A | Escopo estreito, classificador não vê tool results, revisor em contexto fresco, defesa em profundidade. Filtro 8,5% → 0,4% de falsos positivos (Verificado). Também: https://code.claude.com/docs/en/security-guidance |
| claude-code `plugins/` (AO-29) | https://github.com/anthropics/claude-code/tree/main/plugins | A | `security-guidance`, limiar ≥ 80, validação por subagente fresco, paralelismo de 2 a 4 agentes. Repo sem licença: destilar. |
| claude-plugins-official, `claude-security` (AO-30) | https://github.com/anthropics/claude-plugins-official | A | Verificadores independentes que tentam refutar achados. Apache-2.0. |
| Subagentes: security-reviewer read-only (AO-09) | https://code.claude.com/docs/en/subagents | A | Exemplo oficial. |
| Hooks (AO-10) | https://code.claude.com/docs/en/hooks | A | Guardrail PreToolUse; hooks rodam com privilégios do usuário. |
| security-and-owasp.instructions.md (CT-16) | https://github.com/github/awesome-copilot | B (7) | Molde `ID · severidade · detecção · OWASP · correção`; seção AI/LLM; "Never trust LLM output as safe." MIT; ~1.000 linhas. |
| security-devsecops-ssdls-appsec.mdc (CT-13) | https://github.com/PatrickJS/awesome-cursorrules | B | Sem segredos hardcoded, queries parametrizadas, nova dependência com aprovação, SAST/SCA no CI. CC0. |
| Solidity + Foundry .mdc (CT-09) | https://github.com/PatrickJS/awesome-cursorrules | B | Checks-Effects-Interactions, ReentrancyGuard; ver blockchain-web3. CC0. |
| code-review-generic e Codex Code Review Rules (CT-20, CT-03) | https://github.com/github/awesome-copilot | B/A | Três níveis (bloqueia/discutir/sugestão); regra de revisão "comportamento a sinalizar + exceção segura". MIT. |
| VoltAgent `security-auditor.md` (EC-09) | https://github.com/VoltAgent/awesome-claude-code-subagents | B | Tools somente leitura, `model: inherit`, mapeamento SOC 2/ISO/PCI/GDPR/NIST. Risco de compliance theater. MIT. |
| Trail of Bits skills e config (EC-12) | https://github.com/trailofbits/skills | B | differential-review, static-analysis (CodeQL/Semgrep), variant-analysis, building-secure-contracts. CC-BY-SA-4.0: destilar. Config: https://github.com/trailofbits/claude-code-config (sem licença). |
| wshobson `security-scanning` (EC-10) | https://github.com/wshobson/agents | B | Plugin citado; abrir. |
| Willison, lethal trifecta (PC-21) | https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ | A | Teste da tríade; conteúdo não confiável não dispara ações consequentes. arXiv 2506.08837. |
| Anthropic Research CoT (PC-24) | https://www.anthropic.com/research/reasoning-models-dont-say-think | A | Raciocínio exibido não é prova. |
| Microsoft system message design (PC-10) | https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/advanced-prompt-engineering | A | Testar com prompts adversariais; system message não garante conformidade. |
| Brex (PC-29) | https://github.com/brexhq/prompt-engineering | B | Nunca colocar em prompt o que não se mostraria na tela. MIT. |
| Hooks como guardrails (CP-19) | https://aitmpl.com/blog/secure-git-workflow/ | B | Negar `.env`, `rm -rf`; reescrever em stdlib; regex não substitui gitleaks. |
| OWASP Top 10:2025 (BR-14) | https://top10.owasp.org/2025 | A | A03 Software Supply Chain Failures, A10 Mishandling of Exceptional Conditions (Verificado). |

## 2. Repositórios e arquivos a abrir
- `anthropics/claude-code-security-review/.claude/commands/security-review.md` (literais conferidos, MIT).
- `anthropics/claude-code/plugins/security-guidance`; `claude-plugins-official/plugins/claude-security`.
- `github/awesome-copilot/instructions/security-and-owasp.instructions.md`.
- `trailofbits/skills` (differential-review, static-analysis, variant-analysis) e `claude-code-config`.
- ASVS 5.0, OWASP API Top 10 2023, LLM Top 10, STRIDE, LGPD/GDPR não estão no atlas (ASVS e API: Não verificado): lente authoritative.

## 3. Materiais oficiais Anthropic pertinentes
AO-09, AO-10, AO-22, AO-23, AO-24, AO-26 (CI), AO-29, AO-30; AO-18 (revisão multiagente).

## 4. Padrões da comunidade
- Revisor read-only por severidade; só lacunas de correção (CP-16).
- Desenvolvimento seguro com pseudocódigo primeiro + TDD com check-ins (CP-15).
- Proibir auth, cripto e flags próprios (CP-24).
- Auditoria de smart contract por LLM tem alta variância; item r/ethdev rejeitado (CP-29).
- Evidência: Dan Luu sobre fuzzing (CP-20).

## 5. O que o brain-of-agent já oferece
- `brains/fullstack/references/seguranca-e-privacidade.md`, `brains/qa/references/seguranca.md`, `vendor/gstack/cso/SKILL.md`, `vendor/gstack/careful/SKILL.md`.
- BR-22: severidade, confiança e evidência separadas; cobertura declarada (estática vs runtime); pausar antes de comando destrutivo.
- BR-14: OWASP Top 10:2025 verificado; ASVS 5.0 e NBR 17060 não verificados. BR-26: modelo de segurança de automação.
- BR-03: modo `SEGURANCA-COMPLETO`.

## 6. Lacunas e cuidados
- Sem fonte para STRIDE, SBOM, segurança de containers/cloud, privacidade (LGPD) com norma primária.
- Exclusões do security-review (rate limiting) não servem a fintech; modelo padrão antigo.
- Ferramentas de scan (CodeQL, Semgrep) não devem ser instaladas pelo plugin; documentar comandos.
- Texto do CT-09/CT-16 traz ALWAYS/NEVER: calibrar tom.
