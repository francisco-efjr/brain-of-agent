# Fontes do plugin security-appsec

Bibliografia validada em 2026-10-10 (consulta: 2026-10-10 para todas as URLs abaixo, salvo indicação). Classe pela rubrica de fontes: A (8 a 10, oficial ou norma), B (5 a 7, autor reconhecido ou repositório mantido), C (até 4, sinal prático). "n/i" = licença não informada na validação; "n/a" = documentação sem licença de texto aplicável. Nenhum texto literal de fonte foi reproduzido neste plugin: o conteúdo é destilação com redação própria e atribuição.

Limitações da validação: o `WebFetch` devolve resumo por modelo auxiliar, então números e nomes foram conferidos assim; reler a fonte antes de citação literal. Data de último push dos repositórios: Não verificável. Pesquisador e validador são da família Claude (independência parcial), e a síntese é do mesmo modelo do validador: autoavaliação não é validação externa.

## Sumário

1. Atribuição e licenças (leia antes de reutilizar)
2. Fontes Claude Code e Anthropic
3. Taxonomias e padrões OWASP, NIST e Microsoft
4. Cheat Sheets OWASP (CC BY-SA 4.0)
5. Skills, regras e repositórios de terceiros
6. Conteúdo próprio do usuário (brain-of-agent) e gstack
7. Rejeitados
8. Lacunas

## 1. Atribuição e licenças

- OWASP Cheat Sheet Series, ASVS e Trail of Bits `differential-review`/catálogo: CC BY-SA 4.0. Este plugin destila com redação própria e atribui. Adaptar de perto o texto pode atrair ShareAlike: revisão humana antes de publicar (Suposição de leitura jurídica).
- anthropics/claude-code-security-review: MIT. getsentry/skills: Apache-2.0 (as referências adaptadas de OWASP nessa fonte são CC BY-SA: não copiadas). github/awesome-copilot: MIT. brexhq/prompt-engineering: MIT. PatrickJS/awesome-cursorrules: CC0-1.0.
- Atribuições obrigatórias no texto dos componentes: "Triagem de risco inspirada em trailofbits/skills `differential-review` (CC BY-SA 4.0); pipeline inspirado em anthropics/claude-code-security-review (MIT) e getsentry/skills `security-review` (Apache-2.0)."
- brain-of-agent (francisco-efjr, MIT): conteúdo próprio do usuário, incorporado e adaptado. gstack (garrytan/gstack, MIT): `cso` e `careful` destilados com atribuição; créditos em `THIRD_PARTY_NOTICES.md` e licença em `vendor/gstack/LICENSE` do snapshot.

## 2. Fontes Claude Code e Anthropic

| Item | Título | URL | Classe | Licença |
| --- | --- | --- | --- | --- |
| V-01 | Security (modelo de segurança do Claude Code) | https://code.claude.com/docs/en/security | A (9) | n/a |
| V-02 | Security guidance plugin | https://code.claude.com/docs/en/security-guidance | A (9) | doc n/a; plugin Apache-2.0 (marketplace oficial) |
| V-03 | Comando `/security-review` (arquivo) e repositório | https://raw.githubusercontent.com/anthropics/claude-code-security-review/main/.claude/commands/security-review.md · https://github.com/anthropics/claude-code-security-review · https://code.claude.com/docs/en/commands | A (9) | MIT |
| V-03 | Blog: automate security reviews with Claude Code (2025-08-06) | https://claude.com/blog/automate-security-reviews-with-claude-code | A | n/i |
| V-04 | README da Action claude-code-security-review | https://raw.githubusercontent.com/anthropics/claude-code-security-review/main/README.md | A (8) | MIT |
| V-05 | Permissions | https://code.claude.com/docs/en/permissions | A (9) | n/a |
| V-06 | Hooks e hooks-guide | https://code.claude.com/docs/en/hooks · https://code.claude.com/docs/en/hooks-guide | A (9) | n/a |
| V-08 | Subagents | https://code.claude.com/docs/en/sub-agents | A (8) | n/a |
| V-09 | Claude Code sandboxing (engenharia, 2025-10-20) e doc | https://www.anthropic.com/engineering/claude-code-sandboxing · https://code.claude.com/docs/en/sandboxing | A (8) | n/a |
| V-10 | Prompt injection defenses (2025-11-24) | https://www.anthropic.com/research/prompt-injection-defenses | A (8) | n/i |
| V-12 | Reasoning models don't always say what they think (2025-04-03) | https://www.anthropic.com/research/reasoning-models-dont-say-think | A (8) | n/i |
| V-29 | Claude Security (doc e README do plugin) | https://code.claude.com/docs/en/claude-security · https://raw.githubusercontent.com/anthropics/claude-plugins-official/main/plugins/claude-security/README.md | A (9) | n/i (ver LICENSE do plugin) |
| V-32 | anthropics/claude-plugins-official (README) | https://github.com/anthropics/claude-plugins-official | A (8) | Apache-2.0 (licença de cada plugin: ver o LICENSE próprio) |

Notas de uso: V-01 inclui modos auto e manual, WebFetch isolado, aviso de WebDAV e cinco práticas para conteúdo não confiável; V-05 traz deny primeiro e os limites das regras de Bash; V-06, a semântica `exit 2` e `onFailure: "block"` (2.1.295+); V-09, que o Windows nativo roda sem sandbox. Os artigos `claude-code-auto-mode` e `code-review` citados pela doc não foram lidos (lacuna).

## 3. Taxonomias e padrões OWASP, NIST e Microsoft

| Item | Título | URL | Classe | Licença |
| --- | --- | --- | --- | --- |
| V-13 | OWASP Top 10:2025 | https://top10.owasp.org/2025 | A (9) | n/i |
| V-14 | OWASP Top 10 for LLM Applications 2025 | https://genai.owasp.org/llm-top-10/ | A (8) | n/i |
| V-15 | OWASP API Security Top 10 2023 | https://api-security.owasp.org/editions/2023/en/0x11-t10 | A (9) | n/i |
| V-16 | OWASP ASVS 5.0.0 | https://owasp.org/www-project-application-security-verification-standard/ · https://github.com/OWASP/ASVS | A (8) | CC BY-SA 4.0 |
| V-26 | NIST SSDF (SP 800-218 v1.1) | https://csrc.nist.gov/projects/ssdf | A (9) | n/i (publicação do governo dos EUA) |
| V-17 | Microsoft: Threat Modeling Tool threats (definições STRIDE) | https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats | A (8) | n/i |
| V-31 | Microsoft: advanced prompt engineering (contraste) | https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/advanced-prompt-engineering | B (7) | n/i |

## 4. Cheat Sheets OWASP (CC BY-SA 4.0; todos classe A, 8)

| Item | Tema | URL |
| --- | --- | --- |
| V-17 | Threat Modeling | https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html |
| V-18 | Authorization | https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html |
| V-19 | Secrets Management | https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html |
| V-20 | Input Validation | https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html |
| V-21 | SQL Injection Prevention | https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html |
| V-22 | Cross Site Scripting Prevention | https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html |
| V-23 | Server Side Request Forgery Prevention | https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html |
| V-24 | Password Storage | https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html |
| V-25 | Dependency Graph SBOM | https://cheatsheetseries.owasp.org/cheatsheets/Dependency_Graph_SBOM_Cheat_Sheet.html |
| V-36 | Session Management | https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html |
| V-37 | Cross-Site Request Forgery Prevention | https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html |
| V-38 | Docker Security | https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html |
| V-39 | Cryptographic Storage | https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html |
| V-40 | Vulnerability Disclosure | https://cheatsheetseries.owasp.org/cheatsheets/Vulnerability_Disclosure_Cheat_Sheet.html |
| extra (validador de qualidade) | CVSS v4.0 Specification, Tabela 22 (faixas qualitativas de severidade) | https://www.first.org/cvss/v4.0/specification-document |

Notas: V-24 (parâmetros de senha) são "mínimos hoje": reconferir na página antes de citar. V-18 não tem seção dedicada a tenant: o tratamento de tenant neste plugin é Inferido (derivado de IDOR mais ABAC). V-19 ordena revogar, rotacionar, apagar e registrar. Os checklists V-36 a V-40 foram abertos pelo validador nesta data; os valores de timeout de V-36 são referência por risco.

## 5. Skills, regras e repositórios de terceiros

| Item | Título | URL | Classe | Licença | Uso |
| --- | --- | --- | --- | --- | --- |
| V-07 | dev.to: "I wrote a safety mod that crashes on purpose" (relato; 5 de outubro) e HN | https://dev.to/aidiveyt/i-wrote-a-safety-mod-that-crashes-on-purpose-claude-code-ran-the-command-anyway-323b · https://news.ycombinator.com/item?id=46412347 | B (6) | n/i | Teste de guard com marcador; o relato trata de mods e o comportamento de hooks foi confirmado na doc (V-06) |
| V-11 | Simon Willison: the lethal trifecta (2025-06-16) | https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ | B (6) | n/i | Tríade; princípio de um autor, não norma |
| V-27 | github/awesome-copilot: `security-and-owasp.instructions.md` | https://raw.githubusercontent.com/github/awesome-copilot/main/instructions/security-and-owasp.instructions.md · https://github.com/github/awesome-copilot | B (6) | MIT (repositório; o arquivo não declara licença própria) | Molde ID, severidade, detecção |
| V-28 | trailofbits/skills `differential-review` | https://raw.githubusercontent.com/trailofbits/skills/main/plugins/differential-review/skills/differential-review/SKILL.md · https://github.com/trailofbits/skills | B (6) | CC-BY-SA-4.0 | Triagem por risco, raio de impacto; destilado |
| V-30 | getsentry/skills `security-review` | https://raw.githubusercontent.com/getsentry/skills/main/skills/security-review/SKILL.md · https://github.com/getsentry/skills | B (7) | Apache-2.0 | Níveis de confiança, VULN/VERIFY; destilado |
| V-33 | brexhq/prompt-engineering | https://github.com/brexhq/prompt-engineering | C (5) | MIT | Só o princípio "nada que não se mostraria na tela" |
| V-34 | awesome-cursorrules: `security-devsecops-ssdls-appsec.mdc` | https://github.com/PatrickJS/awesome-cursorrules · https://raw.githubusercontent.com/PatrickJS/awesome-cursorrules/main/rules/security-devsecops-ssdls-appsec.mdc | C (4) | CC0-1.0 | Base do bloco de CLAUDE.md, reescrito |
| V-35 | Catálogo de skills da Trail of Bits | https://github.com/trailofbits/skills | C (5) | CC-BY-SA-4.0 | Só nomes verificados |
| V-32 | wshobson/agents (avisos de instalação) | https://github.com/wshobson/agents | A/B (exemplo) | MIT (plugins externos com licenças próprias) | Só avisos de instalação |

Sinais de repositório observados em 2026-10-10 nas páginas HTML (não é prova de qualidade): security-review 6,3 mil estrelas; claude-plugins-official 37,6 mil; awesome-copilot 39,9 mil; trailofbits/skills 7,5 mil; getsentry/skills 1,0 mil; awesome-cursorrules 40,9 mil; brex 9,6 mil; wshobson/agents 40,3 mil. Data de último push: Não verificável.

## 6. Conteúdo próprio do usuário (brain-of-agent) e gstack

Rótulo: Inferido (brain, não reconferido). Snapshot: `docs/foundation/brain-of-agent-snapshot/` (commit 0d025fb).

| Arquivo | Uso |
| --- | --- |
| `brains/fullstack/references/seguranca-e-privacidade.md` | Modelo de ameaça orientado ao fluxo, autenticação não é autorização, privacidade por fluxo, checklist de 9 itens, formato do achado |
| `brains/qa/references/seguranca.md` | Escopo e ética, matriz papel por ação por recurso, sentinelas, autenticação e sessão, headers, comandos de scanner, ZAP, lógica de negócio, como reportar |
| `vendor/gstack/cso/SKILL.md` (gstack, MIT) | Rubrica de evidência, desafio independente, completo/parcial/não avaliado, busca de variantes; não portado: launcher `gstack-cso` e execução |
| `vendor/gstack/careful/SKILL.md` (gstack, MIT) | Guard ask/deny, exceções seguras, padrões aditivos; não portada: gravação de analytics |

Itens do brain que não foram reconferidos em fonte oficial: RFC 9700, "ASVS com cerca de 350 requisitos e 17 capítulos", data de publicação do Top 10:2025 (novembro de 2025) e absorção do SSRF por A01, incidente `tj-actions/changed-files` (março de 2025), Resolução CD/ANPD nº 15/2024, versões de flags dos scanners. As faixas qualitativas CVSS foram conferidas na especificação v4.0 do FIRST em 2026-10-10 (ver tabela da seção 3).

## 7. Rejeitados (não usar como fonte)

| Item | Motivo |
| --- | --- |
| VoltAgent `security-auditor` | Números fictícios de conformidade (347 controles, 87%), agentes inexistentes; compliance theater |
| code-review-generic (awesome-copilot) | Mistura estilo e segurança; sem ganho |
| Deploy gate (Yureki Lab) | Fora do escopo; alegações sem validação |
| Ask HN sobre modelo para revisão de segurança | Sem técnica reaproveitável; conteúdo promocional |
| sergiodxa/agent-skills | Existência da skill não confirmada |
| Leads de incidentes de prompt injection (Google Cloud TI, Ars Technica) | Títulos confirmados, conteúdo não lido; só motivação, nunca detalhe |
| Limiar "80", subagentes paralelos e taxas de falso positivo do security-guidance; `SG_DUAL_OR`; "27 µs" | Não confirmados nas fontes; removidos |

## 8. Lacunas (declaradas nos relatórios do plugin)

LGPD/GDPR sem norma primária lida (Lei 13.709/2018 não abriu: não citar artigos nem resoluções da ANPD); JWT, MFA e recuperação de conta sem fonte primária (cheat sheet de JWT retornou 404; RFC 8725 não lido); ASVS 5.0.0 sem extração de capítulos e níveis (sem números de requisito); SAST, DAST e segredos sem documentação oficial de CodeQL, Semgrep, gitleaks, ZAP; cloud, IaC e Kubernetes (só Docker); TLS e gestão de chaves em trânsito; modo auto (artigos não lidos) e parte final da doc de hooks; comunidade social (Reddit, X, YouTube) sem itens; eficácia (nenhuma taxa confiável de falso positivo ou negativo por modelo); privacidade de código enviado ao modelo; mobile, firmware, blockchain e fintech/PCI; processo interno de triagem de vulnerabilidades (SLA por severidade).
