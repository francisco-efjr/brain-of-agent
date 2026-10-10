# Ecossistema comunitário do Claude Code — atlas global VALIDADO (condensado)

Validador: claude-sonnet-5-5 (independente do pesquisador claude-haiku-5-5) · Data: 2026-10-09 · Original: `claude-code-ecosystem.md` (36 itens).
Rótulos: Verificado / Inferido / Suposição / Não verificável. Reuso literal só com licença permissiva (MIT, Apache-2.0, CC0) ≤ ~40 linhas com atribuição; caso contrário, destilar com redação própria.

## Método de validação
- Re-verificados nesta execução (20 de 36 itens, ~55%, acima da meta de 30%): API GitHub de obra/superpowers, github/spec-kit, anthropics/skills, anthropics/claude-code, anthropics/claude-plugins-official, Piebald-AI, garrytan/gstack, hesreallyhim, wshobson/agents, vercel-labs, trailofbits/skills, VoltAgent subagents, automazeio/ccpm, PatrickJS, buildermethods/agent-os; página HTML do OpenSpec; raw de `spec-template.md` (spec-kit), `systematic-debugging/SKILL.md` (superpowers) e `skills/docx/LICENSE.txt` (anthropics/skills).
- Resultado: todas as estrelas, forks, licenças e datas de push conferem exatamente com o atlas (Verificado). Divergências de licença (API null/NOASSERTION) confirmadas.
- Injeção: nenhuma instrução embutida a IAs nos arquivos relidos (spec-template, systematic-debugging); `$ARGUMENTS` e comentários HTML do spec-kit são variáveis de template normais. Não encontrei texto sem licença copiado literalmente no atlas.
- Não re-verificados (mantêm o rótulo do original): ECC (API 403 para o validador), SuperClaude, BMAD, Composio, travisvn, godogen, K-Dense, supabase, davila7, centminmod e docs oficiais code.claude.com.
- Ajustes de classe feitos pelo validador: Piebald A→B; vercel-labs A→A- (licença nula); gstack e awesome-claude-code mantidos B.

## Itens aprovados

### 1. obra/superpowers — Classe A (8)
- https://github.com/obra/superpowers · MIT · 296.930★ (Verificado), push 2026-10-10
- Iron Law do TDD (sem código sem teste que falhou antes); tabelas de racionalização com contra-argumento; red flags que forçam reinício.
- Debug sistemático: causa raiz antes de corrigir, 4 fases, parar e rever a arquitetura após 3 correções falhas (Verificado).
- Ressalva: longo/prescritivo para tarefas pequenas. MIT permite reuso, mas destilar.
- [seg:qa-testing] [seg:code-quality-refactoring] [seg:sre-observability] [seg:product-discovery-specs] [seg:architecture-design] [seg:git-workflow-release] [seg:automation-integrations]

### 2. github/spec-kit — Classe A (8)
- https://github.com/github/spec-kit · MIT · 140.622★ · `templates/spec-template.md`
- Histórias priorizadas P1/P2/P3 testáveis de forma independente com Given/When/Then; requisitos FR-NNN e critérios SC-NNN agnósticos de tecnologia; seção Assumptions; marcador `[NEEDS CLARIFICATION]` (Verificado).
- Sem detalhes de implementação na spec. Só o template foi lido (plan/tasks não).
- [seg:product-discovery-specs] [seg:architecture-design]

### 3. anthropics/skills (skill-creator, frontend-design) — Classe A (9)
- https://github.com/anthropics/skills · licença do repo: null (API); 180.191★
- skill-creator: captura de intenção, entrevista de bordas, instruções imperativas com o porquê, 2–3 prompts de teste com/sem skill, SKILL.md < ~500 linhas, loop de otimização da `description` (~20 consultas positivas/negativas).
- frontend-design: definir produto/público antes do visual, plano de tokens, lista de anti-padrões genéricos, reduced motion e foco visível, revisar screenshots.
- Licença: tratar como destilação; docx/pdf/pptx/xlsx são proprietários (LICENSE.txt Verificado: proibido copiar, derivar, redistribuir).
- [seg:automation-integrations] [seg:llm-ai-agents] [seg:ux-ui-design] [seg:web-frontend] [seg:qa-testing] [seg:technical-writing-docs]

### 4. Docs oficiais: sub-agents, best-practices, skills, CLAUDE.md blog — Classe A (8)
- https://code.claude.com/docs/en/sub-agents · /best-practices · /skills · https://www.claude.com/blog/using-claude-md-files (não re-lidas pelo validador; conteúdo oficial, Verificado só pelo pesquisador)
- Subagentes: `description` como gatilho; `tools` allowlist ou `disallowedTools`; subagentes não herdam CLAUDE.md com garantia, repetir regras críticas na delegação; formato de saída no corpo.
- Boas práticas: dar meio de verificação (testes/build/screenshot); explorar→planejar→implementar→commitar; CLAUDE.md curto com teste de remoção; revisão adversarial em contexto limpo; padrão Writer/Reviewer.
- Skills: progressive disclosure, < 500 linhas, avaliar com/sem skill. CLAUDE.md: sem credenciais, tratar como potencialmente público.
- Licença: documentação proprietária, destilar.
- [seg:automation-integrations] [seg:llm-ai-agents] [seg:qa-testing] [seg:git-workflow-release] [seg:technical-writing-docs] [seg:security-appsec]

### 5. anthropics/claude-plugins-official — Classe A (9)
- https://github.com/anthropics/claude-plugins-official · Apache-2.0 · 37.592★ · push 2026-10-09
- Referência oficial de formato de marketplace/plugin (`plugins/`, `external_plugins/`, `.claude-plugin/`). Itens internos não enumerados.
- [seg:automation-integrations] [seg:cli-desktop-tooling]

### 6. anthropics/claude-code — Classe A (9)
- https://github.com/anthropics/claude-code · licença: null (Verificado) · 149.899★
- Fonte primária de issues e comportamento de hooks/plugins/subagentes. Sem reuso de texto.
- [seg:automation-integrations] [seg:llm-ai-agents]

### 7. vercel-labs/agent-skills — Classe A- (7–8)
- https://github.com/vercel-labs/agent-skills · API: licença null (SKILL.md declara MIT, conflito) · 32.134★ · push 2026-08-28
- 70 regras em 8 categorias ordenadas por impacto (waterfalls e bundle críticos); um arquivo por regra com motivo, exemplo ruim e bom. Sem etapa de verificação.
- Reuso literal bloqueado até confirmar LICENSE; usar o formato.
- [seg:web-frontend] [seg:mobile-apps] [seg:devops-cloud-infra] [seg:code-quality-refactoring]

### 8. Piebald-AI/claude-code-system-prompts — Classe B (7) (rebaixado de A)
- https://github.com/Piebald-AI/claude-code-system-prompts · MIT (do repo) · 12.868★ · push 2026-10-09
- Motivo do rebaixamento: terceiro, autoridade 1; os textos extraídos são prompts da Anthropic, e a licença MIT do repo não garante direitos sobre eles. Destilar apenas.
- `agent-prompt-claude-md-creation.md`: incluir comandos de build/lint/teste, arquitetura em alto nível; excluir conselho genérico e seções inventadas; sugerir melhorias se CLAUDE.md já existe.
- [seg:technical-writing-docs] [seg:llm-ai-agents] [seg:automation-integrations] [seg:security-appsec]

### 9. VoltAgent/awesome-claude-code-subagents — Classe B (7)
- https://github.com/VoltAgent/awesome-claude-code-subagents · MIT · 25.612★ · push 2026-10-05
- `categories/04-quality-security/security-auditor.md`: tools somente leitura (Read, Grep, Glob), `model: inherit`, fases, checklist, severidade, mapeamento a SOC 2/ISO/PCI/GDPR/NIST.
- Ressalvas: prompts longos, risco de compliance theater, sem evals; contagem total de agentes não verificável.
- [seg:security-appsec] [seg:qa-testing] [seg:code-quality-refactoring] [seg:architecture-design] [seg:sre-observability] [seg:saas-multitenant]

### 10. wshobson/agents — Classe B (7)
- https://github.com/wshobson/agents · MIT · 40.308★ · push 2026-10-05 · 92 pastas em `plugins/` (relatado pelo pesquisador)
- `debugging-toolkit/agents/debugger.md`: fluxo de 5 passos (capturar, reproduzir, isolar, correção mínima, verificar) e saída com causa raiz, evidência, correção, teste, prevenção. Sem `tools` (herda tudo): corrigir ao destilar.
- Plugins por área: security-scanning, database-design, kubernetes-operations, incident-response, tdd-workflows, git-pr-workflows, c4-architecture, documentation-generation, game-development, blockchain-web3, payment-processing, cicd-automation, entre outros.
- [seg:code-quality-refactoring] [seg:sre-observability] [seg:security-appsec] [seg:database-data-modeling] [seg:data-engineering] [seg:data-science-ml] [seg:llm-ai-agents] [seg:devops-cloud-infra] [seg:qa-testing] [seg:git-workflow-release] [seg:architecture-design] [seg:technical-writing-docs] [seg:game-development] [seg:blockchain-web3] [seg:fintech-payments] [seg:web-frontend] [seg:mobile-apps]

### 11. garrytan/gstack — Classe B (7)
- https://github.com/garrytan/gstack · MIT · 135.745★ · push 2026-10-09
- `plan-eng-review`: escopo obrigatório antes da revisão, Scope Challenge, seções (arquitetura, fluxo de dados, bordas, testes, performance), decisões com recomendação e trade-offs, relatório com gate, só revisa.
- Segurança: `bin/`, `setup`, `setup.ps1` e preâmbulo com scripts locais. Documentar, não executar.
- [seg:architecture-design] [seg:product-discovery-specs] [seg:ux-ui-design] [seg:qa-testing] [seg:security-appsec] [seg:git-workflow-release] [seg:sre-observability] [seg:mobile-apps]

### 12. trailofbits/claude-code-config e trailofbits/skills — Classe B (7 / 6)
- https://github.com/trailofbits/claude-code-config (sem licença declarada) · https://github.com/trailofbits/skills (CC-BY-SA-4.0, 7.455★, Verificado)
- Config: sandbox, deny rules para credenciais, hooks PreToolUse que bloqueiam `rm -rf` e push na main, `.mcp.json` de projeto desativado por padrão; hooks são guardrail, não fronteira de segurança.
- Skills: differential-review, static-analysis (CodeQL/Semgrep), variant-analysis, building-secure-contracts. CC-BY-SA impede texto literal; destilar.
- [seg:security-appsec] [seg:blockchain-web3] [seg:cli-desktop-tooling] [seg:automation-integrations]

### 13. affaan-m/ECC (ex-everything-claude-code) — Classe B (6–7)
- https://github.com/affaan-m/ECC · MIT · 276.047★ (relatado; API deu 403 ao validador, Não re-verificado)
- Princípio "otimizar a janela de contexto, persistir o resto"; hooks de ciclo de vida; README alerta contra instalações sobrepostas e re-uploads maliciosos. Contagens internas divergem.
- Instalação executa código (`npx`, `install.sh`): não executar. Paridade Windows limitada.
- [seg:automation-integrations] [seg:architecture-design] [seg:code-quality-refactoring]

### 14. SuperClaude-Org/SuperClaude_Framework — Classe B (6)
- https://github.com/SuperClaude-Org/SuperClaude_Framework · MIT · ~23,9k★ (relatado)
- 30 comandos `/sc:*`, 20 agentes, 7 modos (relatado). Alegações de ganho de velocidade/tokens sem benchmark: descartar. Não afiliado à Anthropic.
- [seg:product-discovery-specs] [seg:qa-testing] [seg:llm-ai-agents]

### 15. bmad-code-org/BMAD-METHOD — Classe B (6)
- https://github.com/bmad-code-org/BMAD-METHOD · licença NOASSERTION (tratar como não licenciada) · ~54k★ (relatado)
- Papéis ágeis (analista, PM, arquiteto, dev, QA) como skills; v6 em `.claude/skills/bmad-*`, v4 em `.claude/commands/`. Só destilar ideias; não lido.
- [seg:product-discovery-specs] [seg:architecture-design] [seg:qa-testing]

### 16. automazeio/ccpm — Classe B (5) por obsolescência
- https://github.com/automazeio/ccpm · MIT · 8.407★ · último push 2026-03-18 (Verificado, > 6 meses)
- Pipeline PRD→épico→issues→worktrees paralelos. O projeto desaconselha uso em debug/teste/review. Conteúdo não lido (Suposição).
- [seg:product-discovery-specs] [seg:git-workflow-release]

### 17. buildermethods/agent-os — Classe B (6)
- https://github.com/buildermethods/agent-os · MIT · 5.490★ · push 2026-10-07 (Verificado)
- Ideia: extrair standards do próprio codebase e injetá-los nas tarefas (`/discover-standards`, `/inject-standards`, `/shape-spec`). Detalhes vieram de busca: Suposição.
- [seg:code-quality-refactoring] [seg:backend-api] [seg:web-frontend]

### 18. Fission-AI/OpenSpec — Classe B (6)
- https://github.com/Fission-AI/OpenSpec · MIT · 71,5k★ (HTML, Verificado, aproximado) · data do último commit não exibida
- Deltas de spec por mudança (adicionado/modificado/removido) e fluxo proposta→spec→design→tarefas; agregadores traziam estrelas defasadas.
- [seg:product-discovery-specs] [seg:architecture-design]

### 19. PatrickJS/awesome-cursorrules — Classe B (5–6)
- https://github.com/PatrickJS/awesome-cursorrules · CC0-1.0 · 40.894★ · push 2026-05-30 (Verificado)
- Regras por stack em formato Cursor; CC0 permite reuso literal com atribuição, mas qualidade variável e formato de outra ferramenta. Converter e revisar.
- [seg:web-frontend] [seg:backend-api] [seg:mobile-apps]

### 20. Listas e índices (usar só para descoberta, nunca como fonte de prompt)
- hesreallyhim/awesome-claude-code · https://github.com/hesreallyhim/awesome-claude-code · licença NOASSERTION (Verificado; ignorar a alegação CC0 de agregador) · 55.329★ · Classe B (7). [seg:automation-integrations]
- ComposioHQ/awesome-claude-skills · https://github.com/ComposioHQ/awesome-claude-skills · API null, README declara Apache-2.0 (conflito) · ~76,8k★ · conteúdo promocional · Classe B (5). [seg:automation-integrations]
- VoltAgent/awesome-agent-skills · https://github.com/VoltAgent/awesome-agent-skills · MIT · ~35,4k★ · 1000+ skills impossíveis de vetar · Classe B (6). [seg:automation-integrations]

### 21. Coleções de domínio (índice; conteúdo não lido, Suposição de qualidade)
- K-Dense-AI/claude-scientific-skills · https://github.com/K-Dense-AI/claude-scientific-skills · MIT · ~48,2k★ (HTML) · tem scanners de skills · Classe B (6). [seg:data-science-ml] [seg:data-engineering]
- supabase/agent-skills · https://github.com/supabase/agent-skills · MIT (HTML) · ~2,7k★ · regras de Postgres em 8 categorias (query, conexões, schema, locks, RLS, monitoramento) · Classe B (6). [seg:database-data-modeling] [seg:saas-multitenant]
- htdt/godogen · https://github.com/htdt/godogen · MIT · ~7,1k★ (HTML); HN 337 pts em 2026-03-16 · executa engine e gera assets: não executar · Classe B (6). [seg:game-development]

## Rejeitados

| Item | Motivo |
| --- | --- |
| R-global-03 travisvn/awesome-claude-skills | Licença desconhecida, atualização de 2026-04-28 (> 5 meses), redundante com outras listas |
| R-global-14 davila7/claude-code-templates | Conteúdo dos templates não lido; ferramenta que instala configuração; sem valor reutilizável comprovado |
| R-global-26 disler/claude-code-hooks-mastery | Classe C, sem licença, código não lido, push de 2026-03 e hooks executam shell |
| R-global-30 Dimillian/Skills | Classe C, nenhum SKILL.md lido, origem possivelmente adaptada de Codex (não verificado) |
| R-global-32 centminmod/my-claude-code-setup | Templates não lidos; alegação de seguir práticas da Anthropic é autodeclarada |
| R-global-33 MuhammadUsmanGM/claude-code-best-practices | 93★, autoria individual, templates não lidos, mapeamento de stacks é Suposição |
| R-global-34 NeoLabHQ/context-engineering-kit | Só sinal de HN (44 pts); estrelas, licença e conteúdo não verificados |
| R-global-36 Lacuna MCP/cookbooks | Placeholder de lacuna, não é fonte |

## Princípios e achados transversais
- Dar ao agente um meio de verificar o próprio trabalho antes de declarar pronto (docs oficiais best-practices; superpowers `verification-before-completion`; Trail of Bits).
- Subagentes com `tools` restrito e escopo estreito; evitar herdar tudo (docs oficiais sub-agents; VoltAgent `security-auditor`). Crítica: `wshobson/debugger.md` herda tudo.
- Repetir regras críticas no prompt de delegação: subagentes não herdam CLAUDE.md com garantia (docs oficiais sub-agents).
- CLAUDE.md curto com teste de remoção, sem conselho genérico e sem segredos (docs oficiais; Piebald `claude-md-creation`).
- Especificação antes do código com critérios testáveis e marcador de dúvida aberta (spec-kit, OpenSpec, ccpm, BMAD).
- Regras anti-racionalização e escalada após 3 falhas combatem atalhos de agentes (superpowers, Verificado).
- Revisão em contexto limpo / Writer-Reviewer (docs oficiais best-practices; gstack `plan-eng-review`).
- Formato "uma regra por arquivo com exemplo ruim e bom" (vercel-labs).
- Hooks são guardrail, não fronteira de segurança; `.mcp.json` de projeto desativado por padrão (Trail of Bits config).
- Estrelas de agregadores são defasadas e erradas (OpenSpec, godogen); popularidade não prova qualidade. Licenças divergem entre API e README: o LICENSE do arquivo decide. Redirecionamentos de nomes antigos: usar nome canônico.
- Plugin dev-segments seguro por padrão: sem hooks que executem shell, sem `.mcp.json` ativo; documentar instaladores (ECC, gstack, godogen, templates) em `references/` sem executá-los (regra 7 de `00-LEIA-PRIMEIRO.md`).
- Lacunas abertas: coleções de MCP, claude-cookbooks, Reddit/X, domínios sem coleção (e-commerce, fintech, embarcados, data engineering com dbt/Airflow, mobile além de SwiftUI), conteúdo interno de `claude-plugins-official`.
