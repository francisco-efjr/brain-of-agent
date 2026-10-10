# Fontes e bibliografia — Automação, integrações e MCP

Consulta: 2026-10-10. Todas as páginas e repositórios abaixo foram lidos por pesquisadores e reconferidos por um validador (modelos Claude de portes diferentes: a independência é parcial, pois todos são da família Claude). Nenhum conteúdo de terceiros foi executado. Toda recomendação do playbook cita um item `V-xx` desta lista ou é marcada como Inferido (conhecimento estável do domínio, a conferir na documentação do provedor).

Sumário: 1. Como ler · 2. Top 20 · 3. Fontes de apoio · 4. Descartadas · 5. Índice V-01..V-33 · 6. Créditos e licenças · 7. Onde conferir versões

## 1. Como ler

- **Classe A**: documentação oficial, norma ou mantenedor do produto. **B**: autor ou empresa reconhecida, ou repositório com uso comprovado. **C**: só descoberta (nenhum conteúdo reutilizado).
- **Licença** é a observada pelo validador. Para páginas de documentação a licença **não foi verificada**: o plugin só destila (redação própria) e cita a URL. Texto literal só do conteúdo próprio do usuário (MIT) com atribuição.
- Estrelas e datas de push, quando citadas, são de 2026-10-09/10 e servem de sinal, nunca de prova de qualidade.
- Versões mínimas de flags e campos (por exemplo `v2.1.259`, `v2.1.295`) vêm das páginas oficiais na data da consulta. Confira `claude --version` e a página atual antes de depender delas.

## 2. Top 20 (ordenadas por utilidade × autoridade)

| # | Título | URL | Classe | Licença | Consulta | Itens |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Claude Code Hooks (referência) | https://code.claude.com/docs/en/hooks | A | não verificada | 2026-10-10 | V-02 |
| 2 | Manifest reference de plugins | https://code.claude.com/docs/en/plugins/manifest-reference | A | não verificada | 2026-10-10 | V-01 |
| 3 | Agent Skills best practices | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices | A | não verificada | 2026-10-10 | V-04 |
| 4 | Skills no Claude Code | https://code.claude.com/docs/en/skills | A | não verificada | 2026-10-10 | V-05 |
| 5 | Configuração de MCP no Claude Code | https://code.claude.com/docs/en/mcp | A | não verificada | 2026-10-10 | V-15 |
| 6 | mcp-builder (SKILL.md) | https://raw.githubusercontent.com/anthropics/skills/main/skills/mcp-builder/SKILL.md | A | nula na API; frontmatter remete a LICENSE.txt (não lido): só destilar | 2026-10-10 | V-12 |
| 7 | Writing effective tools for agents | https://www.anthropic.com/engineering/writing-tools-for-agents | A | não verificada | 2026-10-10 | V-09 |
| 8 | Webhooks Stripe · Best practices GitHub | https://docs.stripe.com/webhooks · https://docs.github.com/en/webhooks/using-webhooks/best-practices-for-using-webhooks | A | docs proprietárias; destilar | 2026-10-10 | V-18 |
| 9 | Plugin evals | https://code.claude.com/docs/en/plugin-evals | A | não verificada | 2026-10-10 | V-06 |
| 10 | Execução não interativa (headless) | https://code.claude.com/docs/en/headless | A | não verificada | 2026-10-10 | V-32 |
| 11 | Segurança do Claude Code | https://code.claude.com/docs/en/security | A | não verificada | 2026-10-10 | V-14 |
| 12 | MCP: construir um servidor | https://modelcontextprotocol.io/docs/develop/build-server | A | não verificada | 2026-10-10 | V-16 |
| 13 | Features overview · blog de steering | https://code.claude.com/docs/en/features-overview · https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more | A | não verificada | 2026-10-10 | V-03 |
| 14 | Building effective agents | https://www.anthropic.com/engineering/building-effective-agents | A | não verificada | 2026-10-10 | V-08 |
| 15 | Code execution with MCP | https://www.anthropic.com/engineering/code-execution-with-mcp | A | não verificada | 2026-10-10 | V-10 |
| 16 | Equipping agents with Agent Skills | https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills | A | não verificada | 2026-10-10 | V-11 |
| 17 | skill-creator (SKILL.md) · repositório anthropics/skills | https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md · https://github.com/anthropics/skills | A | nula na API: só destilar | 2026-10-10 | V-07 |
| 18 | The lethal trifecta (Simon Willison) | https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ | B | texto de blog; destilar | 2026-10-10 | V-20 |
| 19 | claude-plugins-official | https://github.com/anthropics/claude-plugins-official | A | Apache-2.0 (Verificado) | 2026-10-10 | V-13 |
| 20 | RFC 9309 (Robots Exclusion Protocol) | https://www.rfc-editor.org/rfc/rfc9309 | A | RFC do IETF; destilar | 2026-10-10 | V-33 |

## 3. Fontes de apoio

| Título | URL | Classe | Licença / nota | Consulta | Itens |
| --- | --- | --- | --- | --- | --- |
| claude-code-action | https://github.com/anthropics/claude-code-action | A | MIT (README); YAML não está no README: conferir `docs/usage.md` | 2026-10-10 | V-25 |
| Segurança de servidores MCP (Kadenge, 2026-10-07) | https://les-k.github.io/field-notes.html | B | blog pessoal; achados de um autor | 2026-10-10 | V-27 |
| Trail of Bits `claude-code-config` | https://github.com/trailofbits/claude-code-config | B | licença nula na API: não copiar template | 2026-10-10 | V-21 |
| HumanLayer, "Writing a good CLAUDE.md" | https://www.humanlayer.dev/blog/writing-a-good-claude-md | B | blog de empresa; destilar | 2026-10-10 | V-23 |
| n8n, tratamento de erro | https://docs.n8n.io/flow-logic/error-handling/ | B | doc do fornecedor; não embutir texto | 2026-10-10 | V-19 |
| hookdeck/webhook-skills | https://github.com/hookdeck/webhook-skills | B | MIT; ignorar a parte comercial | 2026-10-10 | V-18 |
| cc-safety-net | https://github.com/kenryu42/claude-code-safety-net | B | MIT; instalação `@latest` não recomendada | 2026-10-10 | V-24 |
| gstack (`/careful`, `/freeze`, `scrape`, `skillify`) | https://github.com/garrytan/gstack | B | MIT, Copyright (c) 2026 Garry Tan | 2026-10-10 | V-29 |
| Thariq, dicas de SKILL.md (espelho) | https://raw.githubusercontent.com/shanraisshan/claude-code-best-practice/main/tips/claude-thariq-tips-17-mar-26.md | B | espelho MIT de terceiro; arquivo sem aviso de licença | 2026-10-10 | V-22 |
| andrej-karpathy-skills | https://github.com/multica-ai/andrej-karpathy-skills | B | MIT; popularidade não prova qualidade | 2026-10-10 | V-26 |
| ruler | https://github.com/intellectronica/ruler | B | MIT | 2026-10-10 | V-28 |
| gentle-ai | https://github.com/Gentleman-Programming/gentle-ai | B | MIT; instalador `curl \| bash` é anti-padrão | 2026-10-10 | V-30 |
| Especificação MCP | https://github.com/modelcontextprotocol/modelcontextprotocol | A | README MIT; API marcou NOASSERTION | 2026-10-10 | V-17 |
| Servidores de referência MCP | https://github.com/modelcontextprotocol/servers | A/B | Apache-2.0 (novos) e MIT (antigos) | 2026-10-10 | V-17 |
| Licença do n8n | https://raw.githubusercontent.com/n8n-io/n8n/master/LICENSE.md | B | Sustainable Use License (não permissiva) | 2026-10-10 | V-31 |
| brain-of-agent (conteúdo próprio do usuário) | https://github.com/francisco-efjr/brain-of-agent | próprio | MIT; snapshot no commit 0d025fb | 2026-10-10 | processo, templates |

## 4. Fontes descartadas ou só de descoberta

| Fonte | Motivo |
| --- | --- |
| awesome-copilot, awesome-claude-code | listas de terceiros; sem conteúdo verificável de prática |
| wshobson/agents | contagens autodeclaradas; juízes por LLM não validados contra rótulos humanos |
| Ouroboros (Q00) | sem benchmark; só inspiração de "entrevistar antes de especificar" |
| claude-code-ultimate-guide | CC-BY-SA-4.0 e contém instrução dirigida a IA ("Fetch and follow…"): tratada como dado, não seguida |
| codesmith.in (webhooks n8n) | lista genérica; nada além de V-18 |
| aari-ai/n8n-webhook-idempotency | rejeitada: depende de serviço hospedado de terceiro que recebe as chaves de cada evento |
| davila7/claude-code-templates | usado só como anti-padrão de instalação (`npx ...@latest ... --yes`, sem versão fixada) |

## 5. Índice dos itens V (conteúdo reutilizável vive aqui, em redação própria)

| V | Tema | Classe | Nota de prompt | Onde entra |
| --- | --- | --- | --- | --- |
| V-01 | Manifesto, layout, nomes reservados | A | 85 | autoria, M-xx |
| V-02 | Hooks: eventos, exit codes, matcher | A | 90 | hooks, H-xx |
| V-03 | Escada de direcionamento | A | 85 | decisões, snippet 1 |
| V-04 | Boas práticas de skills | A | 88 | autoria, K-xx |
| V-05 | Frontmatter de skill no Claude Code | A | 87 | autoria, template de skill |
| V-06 | `claude plugin eval` | A | 85 | autoria |
| V-07 | Calibração da `description` | A | 87 | autoria |
| V-08 | Workflow ou agente | A | 78 | decisões |
| V-09 | Desenho de tools | A | 82 | mcp-servers, T-xx |
| V-10 | Código sobre MCP | A | 78 | decisões, mcp-servers |
| V-11 | Auditoria de terceiros | A | 88 | segurança, A-xx |
| V-12 | mcp-builder: 4 fases e 10 perguntas | A | 92 | mcp-servers |
| V-13 | Plugins de referência oficiais | A | ref. | ferramentas, autoria |
| V-14 | Segurança do Claude Code | A | 85 | segurança |
| V-15 | MCP: escopos, aprovação, variáveis | A | 88 | segurança, ferramentas |
| V-16 | stdio: nunca escrever em stdout | A | 88 | mcp-servers |
| V-17 | Spec MCP e servidores de referência | A/B | ref. | mcp-servers, ferramentas |
| V-18 | Receptor de webhook | A | 92 | webhooks, W-xx |
| V-19 | Fluxo de erro do n8n | B | 72 | jobs-workflows |
| V-20 | Trifecta letal | B | 88 | segurança, R-xx |
| V-21 | Baseline de endurecimento | B | 82 | segurança, hooks |
| V-22 | Dicas de SKILL.md | B | 75 | autoria, K-07..K-10 |
| V-23 | CLAUDE.md curto | B | 83 | snippets |
| V-24 | Padrões de bloqueio (cc-safety-net) | B | 83 | hooks |
| V-25 | claude-code-action | A | 77 | jobs-workflows |
| V-26 | Quatro regras de comportamento | B | 75 | snippet 10 |
| V-27 | Revisão de segurança de servidor MCP | B | 80 | mcp-servers, S-xx |
| V-28 | ruler | B | ref. | ferramentas |
| V-29 | `/careful`, `/freeze` | B | 72 | hooks, ferramentas |
| V-30 | Instalador com backup e `doctor` | B | 70 | segurança |
| V-31 | Licença do n8n e fontes não permissivas | B | 80 | segurança, snippet 9 |
| V-32 | `claude -p` para jobs e CI | A | 85 | jobs-workflows, J-xx |
| V-33 | `robots.txt` (RFC 9309) | A | 75 | jobs-workflows, X-xx |

Itens com nota 70–78 (V-08, V-10, V-19, V-22, V-25, V-26, V-29, V-30, V-33) são "aprovados com ressalvas": use como apoio, não como regra rígida.

## 6. Créditos e licenças de terceiros

- **brain-of-agent** (Francisco Edson, MIT, commit 0d025fb): o template `assets/templates/handoff-checkpoint.md` reproduz literalmente `brains/fullstack/assets/templates/handoff-checkpoint.md` (menos de 40 linhas, conteúdo próprio). `plano-de-integracao.md`, `adr-workflow-ou-agente.md`, `registro-leitura-completo.md` e a seção do modo `AUTOMACAO-COMPLETO` adaptam `plano-incremento.md`, `adr.md` e `protocolo-completo.md`. Princípios de contrato de tarefa/ferramenta e de entrega vêm de `agentes-e-ia.md` e `entrega-e-operacao.md` do mesmo repositório.
- **gstack** (Garry Tan, MIT, Copyright (c) 2026 Garry Tan): o processo de scraping somente leitura (intenção em uma linha, recusa de intenção mutante, estrutura antes da extração, 3 a 4 tentativas, falha sem resultado parcial, JSON único) e o fluxo de codificação de skill aprovada (guarda de proveniência, staging, teste, gate de aprovação, gravação atômica, verificação posterior) foram **destilados com redação própria** de `vendor/gstack/scrape/SKILL.md` e `vendor/gstack/skillify/SKILL.md`. Nenhum trecho foi copiado em bloco; nada do runtime (Aside, `$B`, telemetria, instaladores) foi incorporado.
- **Todas as demais fontes** são destilação com redação própria. Documentação da Anthropic, do projeto MCP, de Stripe, GitHub e n8n: licenças não permissivas ou não verificadas; só citação da URL. A licença do n8n (Sustainable Use License) proíbe tratar texto ou código como material embutível: nenhum foi incluído. Isto não é aconselhamento jurídico.

## 7. Onde conferir versões (antes de usar uma flag ou campo)

| O que | Onde |
| --- | --- |
| Eventos e schemas de hook, `onFailure` | https://code.claude.com/docs/en/hooks (a página tem mais de 260 mil caracteres; só ~38% foi lido na consulta) |
| Campos de manifesto e validação | https://code.claude.com/docs/en/plugins/manifest-reference · `claude plugin validate --help` |
| Flags de `claude -p` | https://code.claude.com/docs/en/headless · `claude --help` · `claude --version` |
| Formato de `evals/` e graders | https://code.claude.com/docs/en/plugin-evals (exige Claude Code ≥ 2.1.269) |
| Versão da spec MCP em uso | pasta `schema/<data>/` em https://github.com/modelcontextprotocol/modelcontextprotocol (a consulta viu `2026-07-28`) |
| Rotação de segredo, prazos de retry, tolerância de timestamp | documentação do **provedor** do webhook; prazos de Stripe/GitHub não valem para outros |

Lacunas conhecidas (sem fonte validada): n8n Retry/Continue On Fail, Zapier, Make, Shopify, Slack, `Idempotency-Key`, fila de mortas de um provedor específico, termos de uso e proteção de dados em scraping, páginas de subagentes/memória/`scheduled-tasks` do Claude Code. O playbook rotula esses pontos como Não verificável.
