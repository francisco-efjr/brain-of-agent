# Global — brain-of-agent (VALIDADO, condensado)

Data: 2026-10-09 · Validador independente (Claude Sonnet 5.5; o pesquisador foi outro modelo) · Original: `brain-of-agent.md` (R-global-01..30).
Snapshot = `docs/foundation/brain-of-agent-snapshot/`. Rótulos: Verificado / Inferido / Suposição / Não verificável.

## Resultado da validação

- Itens recebidos: 30 (R-global-01..30). Aprovados: 29 (3 com ressalva de classe/nota). Rejeitados: 1 (proposta de correção ao `house-style.md`, linha 3) + notas autoavaliadas D1–D12 descartadas.
- Reverificado com ferramentas (~40% dos itens/afirmações): estrelas/licenças/push de 6 repositórios (API GitHub), HN 47418576 e 47436453, OWASP Top 10:2025, RFC 9457, página oficial `plugin-evals`, `manifest-reference`, Agent Skills best practices, e contagens/trechos no snapshot local.
- Injeção: nenhuma instrução endereçada a IAs encontrada no atlas nem (por grep) nos SKILL.md do gstack do snapshot. Textos "NEVER/IRON LAW" do gstack são prompts do próprio gstack, não ataques; não obedecidos.
- Licença/cópia literal: as duas citações do `qa/SKILL.md` (MIT, conteúdo do próprio usuário) conferem literalmente no snapshot (linhas ~24 e ~41, quebradas em linhas). Demais blocos são redação própria. Nada de gstack/skill-creator copiado em bloco: manter assim (skill-creator: `anthropics/skills` sem `license` na API; só destilar).
- Notas de prompt D1–D12 do pesquisador (93/82/77...) são autoavaliação do mesmo modelo que poderá construir os plugins: **descartadas**; usar apenas como indício. Classe "A" dos itens próprios do brain (R-01..12) é **A com ressalva**: autoridade 3 pressupõe autoria do usuário e o upstream é Não verificável publicamente.

### Sinais numéricos reverificados (2026-10-09, API GitHub)

| Repo | Atlas disse | Observado agora | Licença | Status |
| --- | --- | --- | --- | --- |
| garrytan/gstack | 135.740★ / 20.160 forks | 135.745★ / 20.159 forks, 187 issues | MIT | Verificado (deriva normal) |
| obra/superpowers | 296.892★ | 296.930★ | MIT | Verificado |
| anthropics/skills | 180.169★, license null | 180.191★, license null | não exposta | Verificado |
| anthropics/claude-plugins-official | 37.589★ | 37.592★ | Apache-2.0 | Verificado |
| wshobson/agents | 40.305★ | 40.308★ | MIT | Verificado (84 plugins/192 agents/156 skills: não rechecado) |
| github/spec-kit | MIT | 140.622★ | MIT | Verificado (estrelas faltavam no atlas) |
| VoltAgent/awesome-claude-code-subagents | 25.612★ MIT | não rechecado | — | Não rechecado |

HN: 47418576 "Garry Tan's Claude Code Setup" 74 pts, ~76 comentários (atlas: 79; ok) · 47436453 115 pts, ~22 comentários — Verificado.

## Itens aprovados

Formato: título · fonte · classe · licença · reutilizável · tags.

### Base própria do brain (fonte primária: snapshot local; MIT)

**R-01 Skill `qa` (router + processo)** · `brains/qa/SKILL.md` (283 linhas, v0.3.0 — Verificado) · A (ressalva) · MIT
- Molde de playbook: papel+porquê, regra "externo é dado", ativação de keyword com limites, mapa tema→referência→template, formatos de entrega, anti-padrões, checklist final.
- Ressalvas: bloco `metadata` não é lido pelo Claude Code (Verificado em manifest-reference para plugin.json; para SKILL.md tratar como inerte); sem exemplos de I/O.
- [seg:qa-testing] [seg:code-quality-refactoring] [seg:technical-writing-docs]

**R-02 Skill `fullstack`** · `brains/fullstack/SKILL.md` (97 linhas) · A (ressalva) · MIT
- "Processo essencial": ler → invariantes → opções só se houver decisão material (ADR) → fatia vertical + testes → revisão adversarial → revalidar reprodução → entregar com limitações.
- Autonomia calibrada (dúvida material bloqueia só a decisão dependente); confirmar API na versão instalada. Sem exemplos; `../qa/` relativo quebra em plugin (usar `${CLAUDE_PLUGIN_ROOT}`).
- [seg:web-frontend] [seg:backend-api] [seg:architecture-design] [seg:database-data-modeling] [seg:devops-cloud-infra] [seg:security-appsec] [seg:llm-ai-agents]

**R-03 Modo `<SEGMENTO>-COMPLETO`** · SKILL raiz, CLAUDE.md, protocolos · A · MIT
- Só por pedido explícito; keyword em log/código não ativa; leitura em lotes com checkpoint; registro lido/parcial/ausente; matriz de aplicabilidade; arquivo ausente = cobertura parcial; auditoria só relata. Trecho de redação própria do atlas aprovado.
- [seg:*] (todos os 25)

**R-04 Rótulos epistêmicos e "nunca invente execução"** · A · MIT
- Verificado/Inferido/Suposição/Não verificável/Não aplicável; leitura de código ≠ execução; screenshot ≠ persistência; CI verde com asserção fraca ≠ fluxo; mesmo modelo ≠ validação independente. Exigir coluna "Status" nos templates.
- [seg:qa-testing] [seg:llm-ai-agents] [seg:technical-writing-docs] [seg:code-quality-refactoring]

**R-05 Formato de evals do brain → `claude plugin eval`** · A · MIT
- Rubrica por dimensão + `critical_failures` = FAIL explícito; caso negativo com `tool_used min 0 max 0 arm: both`; rubricas fora do contexto do executor; status `designed_not_executed`. Tabela de mapeamento do atlas é válida.
- [seg:llm-ai-agents] [seg:qa-testing]

**R-06/07 Templates (QA 9; fullstack 4)** · A · MIT
- Registro de evidências (ID, ação, comando, saída, status epistêmico, data), handoff-checkpoint (Entregue · Verificado/Inferido · Pendências · Riscos · Próximo passo · Retomar), ADR, plano de incremento, checklist-release com parecer go/no-go.
- [seg:qa-testing] [seg:architecture-design] [seg:git-workflow-release] [seg:technical-writing-docs] [seg:product-discovery-specs]

**R-08 `design-de-testes.md`** · A · MIT
- BVA 2/3 valores (ISTQB, Verificado pelo pesquisador; não rechecado por mim), tabela de decisão, estados, pairwise, SBTM/SFDPOT. Receita de 7 passos para skill "derivar casos".
- [seg:qa-testing] [seg:backend-api] [seg:fintech-payments] [seg:ecommerce-marketplace] [seg:data-engineering]

**R-09 `dominios.md` (regras BR)** · B · MIT
- Pix/boleto/cartão/e-commerce/SaaS/ETL como sementes; manter "não verificado" e datar normas (CBS-IBS, CNPJ alfanumérico — primária gov.br Não verificável).
- [seg:fintech-payments] [seg:ecommerce-marketplace] [seg:saas-multitenant] [seg:data-engineering]

**R-10 Scripts Python stdlib** (5 scripts + teste; 1.676 linhas — Verificado) · A · MIT
- `documentos_br.py` (validar contra norma oficial antes de confiar), `pairwise.py`, `valores_limite.py`, `repetir_teste.py`, `auditoria_axe.py` (depende de axe-core via browser). Chamar por caminho explícito; sem `bin/`.
- [seg:qa-testing] [seg:fintech-payments] [seg:ecommerce-marketplace] [seg:web-frontend] [seg:ux-ui-design]

**R-11 Contexto portátil / mensagem inicial** · A · MIT
- Esqueleto de briefing (produto, pedido, escopo, stack, fontes, ambiente, restrições, entrega, aceite) + regras de rótulo e autorização.
- [seg:*] [seg:llm-ai-agents] [seg:technical-writing-docs]

**R-12 Disciplina de validação própria** · A · MIT
- Tabela "resposta a revisão": ID | achado | severidade | resposta | evidência | status; testes determinísticos de estrutura antes de evals caras.
- [seg:technical-writing-docs] [seg:code-quality-refactoring] [seg:llm-ai-agents]

**R-13 Router + `registry/skills.json`** · A · MIT
- Tabela intenção→fonte; "selecionar `ship` não autoriza merge/deploy". Registry: 64 entradas (Verificado). Colisão `qa` some com namespace de plugin; evitar skill `qa` dentro de `qa-testing` (usar `playbook`).
- [seg:architecture-design] [seg:cli-desktop-tooling] [seg:automation-integrations]

**R-14 Referências de segurança e acessibilidade** · A · MIT
- OWASP Top 10:2025 A01–A10 com A03 Software Supply Chain Failures e A10 Mishandling of Exceptional Conditions — **Verificado agora** em top10.owasp.org/2025. WebAIM Million 2026 verificado pelo pesquisador (não rechecado por mim). ASVS 5.0, API Top 10 2023, NBR 17060, EAA: Não verificado.
- [seg:security-appsec] [seg:web-frontend] [seg:ux-ui-design] [seg:mobile-apps] [seg:qa-testing]

### Processo inspirado no gstack (garrytan/gstack, MIT, © 2026 Garry Tan; 135.745★; destilação com atribuição, nunca cópia de bloco)

**R-15 Preâmbulo: Completion Status, "limitações precisam de evidência", Search Before Building, decision brief** · A (9)
- Confirmado no snapshot: DONE/DONE_WITH_CONCERNS/BLOCKED/NEEDS_CONTEXT e "escalar após 3 tentativas" em `review/SKILL.md`.
- Adotar o processo; não o bloco (~400 linhas/skill, acoplado a Bun/`$B`/telemetria). Críticas HN: custo de tokens, overengineering.
- [seg:*] [seg:llm-ai-agents] [seg:code-quality-refactoring]

**R-16 `/review`** (1.118 linhas — Verificado) · A · MIT
- Achado = severidade + confiança 1–10 + `arquivo:linha` + cenário concreto + ação AUTO-FIX|ASK|INFO; em agente somente leitura tudo vira ASK; máx. 3 ciclos; review-log.
- [seg:code-quality-refactoring] [seg:backend-api] [seg:web-frontend] [seg:security-appsec]

**R-17 `/investigate`** · A · MIT
- "Iron Law" sem correção antes da causa raiz (Verificado, linha ~393); regra dos 3 strikes (Verificado, linha ~588); teste de regressão que falhava antes. Unificar com `testes-e-debugging.md`.
- [seg:code-quality-refactoring] [seg:sre-observability] [seg:backend-api] [seg:data-engineering]

**R-18 `/qa` e `/qa-only`** · A · MIT
- Tiers por risco, regression-before-repair, "value card" com seção "Não coberto", par executar/relatar. Browser daemon não portado.
- [seg:qa-testing] [seg:web-frontend] [seg:backend-api]

**R-19 `/ship`, `/land-and-deploy`, `/document-release`, `/retro`** · A · MIT
- "Sem alegação de conclusão sem evidência fresca" (Verificado, ship linha ~900); "Never force-push" (Verificado, linha ~1108); coverage map Diátaxis; checklist pré-PR. Skills de push/deploy com `disable-model-invocation: true`.
- [seg:git-workflow-release] [seg:technical-writing-docs] [seg:devops-cloud-infra]

**R-20 `/office-hours`, `/plan-ceo-review`, `/spec`** · A · MIT
- Premissas e alternativas antes da solução; esqueleto de spec (problema, resultado mensurável, não-objetivos, REQ-NN, bordas, aceite, perguntas abertas). `spec` cria issue: exigir autorização. Tirar o jargão "CEO/10-star".
- [seg:product-discovery-specs] [seg:saas-multitenant] [seg:ecommerce-marketplace]

**R-21 `/plan-eng-review` e `/diagram`** · A · MIT
- Checklist de revisão de arquitetura (limites, estados, falhas parciais/idempotência, concorrência, migração/rollback, authz, observabilidade, testes por camada, alternativa mais simples, ADR). Entregar só mermaid.
- [seg:architecture-design] [seg:backend-api] [seg:database-data-modeling]

**R-22 `/cso`, `/careful`, `/guard`, `/freeze`** · A · MIT
- Severidade/confiança/evidência separadas e cobertura declarada (estática vs runtime); regra de pausar antes de comando destrutivo (confirmação explícita). Hook `PreToolUse` só como exemplo desativado; regex não é fronteira de segurança.
- [seg:security-appsec] [seg:devops-cloud-infra] [seg:database-data-modeling] [seg:git-workflow-release]

**R-23 gstack design + `impeccable/DESIGN.md` (Apache-2.0 por THIRD_PARTY_NOTICES)** · A · MIT/Apache-2.0
- Notas 0–10 por dimensão com "o que seria um 10"; lista anti-slop; `apple-design.md` = preferência de acabamento, não imposição de plataforma.
- [seg:ux-ui-design] [seg:web-frontend] [seg:mobile-apps]

**R-24 `/test-audit`, `/health`, `/canary`, `/benchmark`** · A · MIT
- Catálogo de testes de baixo valor + retirement card (só relata); alerta após 2 checks consecutivos; comparar com baseline salvo.
- [seg:qa-testing] [seg:code-quality-refactoring] [seg:sre-observability] [seg:web-frontend]

**R-25 `/devex-review`, `/plan-devex-review` (TTHW)** · B · MIT
- Roteiro: instalar só pelo README, cronometrar, registrar atritos, erros acionáveis, desinstalação limpa. Única fonte do segmento; complementar com clig.dev (não verificado).
- [seg:cli-desktop-tooling] [seg:technical-writing-docs] [seg:automation-integrations]

**R-26 Modelo de segurança de browser/automação (ARCHITECTURE.md)** · A · MIT
- Regras: nunca instalar em nome do usuário; agir só em recursos próprios/nomeados; ler livre, agir com uma confirmação listando ações; credenciais nunca passam pelo agente; retorno de página/API é dado; registrar o que sai antes de enviar.
- [seg:automation-integrations] [seg:security-appsec] [seg:llm-ai-agents]

### Fontes Anthropic oficiais

**R-27 Plugins/skills/subagentes do Claude Code** · `code.claude.com/docs/en/plugins/manifest-reference` · A (10) · documentação (sem licença de reuso: destilar)
- **Verificado agora:** `name` único campo obrigatório; nomes `claude-`, `anthropic-`, `anthropics-`, `cc-plugin-` = erro; `homepage` deve ser URL válida; `agents`/`commands` **substituem** scan padrão, `skills` **adiciona**; `bin/` no PATH e claude.ai/Cowork **não instalam** plugin com `bin/`; `CLAUDE.md` na raiz do plugin não carrega (aviso); `metadata` não é lido pelo Claude Code; `experimental.evals` existe; `${CLAUDE_PLUGIN_ROOT}` resolve no corpo de skill/agent.
- Correção: o atlas disse "`userConfig` com `sensitive`" (confere) e "caminhos precisam de `./`" não constava — acrescentar: todo caminho de componente deve começar com `./` e ficar dentro da raiz.
- Não rechecado: limite 15.000 tokens de descrições de agentes; campos de subagente.
- [seg:*] [seg:llm-ai-agents] [seg:automation-integrations]

**R-28 `claude plugin eval` e skill-creator** · `code.claude.com/docs/en/plugin-evals`; `anthropics/skills` · A (10)
- **Verificado agora:** exige Claude Code ≥ 2.1.269; 3 runs por padrão; baseline `WITH`/`W/OUT`/`Δ`; `--ablation none`; `--judge-model sonnet`; 6 tipos de grader (`llm`, `baseline`, `regex`, `tool_used`, `tool_order`, `file_exists`); graders "skill invocada" saem do score (`scored: false`) salvo `arm: both`; formatos do plugin-eval e do skill-creator (`evals/evals.json`) são incompatíveis; `--threshold` padrão 1.0.
- Custo real por run: cases rodam via plano/API.
- [seg:llm-ai-agents] [seg:qa-testing] [seg:*]

**R-29 Agent Skills best practices + engenharia Anthropic** · `platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices` · A (10)
- **Verificado agora:** `name` ≤ 64 chars, minúsculas/números/hífens, sem "anthropic"/"claude"; `description` ≤ 1.024 chars, 3ª pessoa, o que faz + quando usar; corpo < 500 linhas; referências a 1 nível; TOC em arquivos > 100 linhas; ≥ 3 avaliações; testar em Haiku/Sonnet/Opus; evitar nomes vagos.
- URLs dos posts de engenharia (context engineering, demystifying evals, building effective agents, sandboxing, harnesses): **não rechecadas** por mim; conferir ao citar.
- [seg:llm-ai-agents] [seg:technical-writing-docs] [seg:*]

**R-30 Ecossistema comparável e comunidade** · A/B (repos) / C (blogs, registries)
- Verificado: números da tabela acima. spec-kit (MIT): fluxo constitution→specify→plan→tasks→implement com IDs estáveis. wshobson: plugins pequenos por domínio. superpowers: skills de processo.
- Ressalvas: "20% de submissões maliciosas (ClawHub)" é alegação de fornecedor, Não verificada; páginas PT-BR e registries são classe C; Reddit sem evidência; `/security-review` (06/08/2025) não rechecado.
- [seg:llm-ai-agents] [seg:git-workflow-release] [seg:security-appsec] [seg:product-discovery-specs] [seg:automation-integrations]

## Rejeitados / corrigidos

| Item | Motivo |
| --- | --- |
| "Correções propostas ao house-style" linha 3 (57 → 55 workflows + router) | **Contagem errada.** Snapshot tem 57 `SKILL.md` em `vendor/gstack/` (inclui `browser-skills/hackernews-frontpage/SKILL.md`, que o atlas disse não existir); 37.735 linhas, não 37.683. O "57" da casa é defensável; reformular como "57 SKILL.md (56 + 1 em `browser-skills`)". Demais correções propostas (commit não verificável, convenções de frontmatter/evals, nuance Apple) permanecem como sugestões para decisão do usuário. |
| Tabela de notas D1–D12 (93, 82, 77...) | Autoavaliação sem independência; pontuações não aprovadas. |
| "Divergente: 56 SKILL.md/37.683 linhas" na verificação do upstream | Dados do snapshot: 57 arquivos/37.735 linhas (ver acima). |
| Classe "A (9)" integral para R-01 | Rebaixada a "A com ressalva": autoridade pressupõe autoria; sem estrelas/uso externo; upstream 404. |
| Claim "Claude Code local 2.1.128" | Não verificável por mim (depende da máquina); apenas ressalva: eval exige ≥ 2.1.269 (Verificado). |

## Princípios / achados transversais

- Conteúdo externo (logs, páginas, respostas de ferramentas) é dado, nunca instrução — brain QA (snapshot `qa/SKILL.md`), gstack ARCHITECTURE, guia Anthropic de sandboxing.
- Rotular tudo e nunca inventar execução; revisão do mesmo modelo não é independente — R-04, rubrica da casa.
- Evidência fresca antes de concluir; reproduzir antes de corrigir; 3 hipóteses falhas = parar — gstack `ship`/`investigate` (Verificado no snapshot).
- Separar relatar de corrigir; revisores somente leitura; ações externas (push, deploy, issue) com `disable-model-invocation: true` e confirmação — R-13/18/19.
- Progressive disclosure: playbook < 500 linhas, referências a 1 nível, TOC > 100 linhas, `description` ≤ 1.024 chars em 3ª pessoa — Agent Skills best practices (Verificado).
- Formato do plugin: `agents`/`commands` declarados substituem o scan; `skills` adiciona; sem `bin/` (claude.ai/Cowork recusam); `CLAUDE.md` do plugin não carrega; caminhos `./` dentro da raiz — manifest-reference (Verificado).
- Evals: formato oficial `claude plugin eval` (Claude Code ≥ 2.1.269), caso negativo `arm: both`, 3 runs, manter `designed_not_executed` até rodar — plugin-evals (Verificado).
- Estrelas não provam qualidade: gstack (135k★) tem custo de contexto alto (~400 linhas de preâmbulo) e críticas HN — adotar processo, não runtime.
- Cobertura do brain é desigual: QA profundo; web3, game-dev e embarcados praticamente nulos; cli-desktop-tooling, data-science, database, data-engineering rasos — exigir pesquisa adicional nesses segmentos antes de construir.
- Normas em transição (CNPJ alfanumérico, CBS-IBS, NBR 17060) ficam "não verificado" com data até haver fonte primária.

## Lacunas remanescentes (validação)

- Não rechecados: WebAIM Million, ISTQB BVA, ASVS 5.0, OWASP API 2023, NBR 17060/EAA, CNPJ alfanumérico (gov.br 404), VoltAgent, contagens de wshobson, posts de engenharia Anthropic, `/security-review`.
- Upstream `francisco-efjr/brain-of-agent` e commit `0d025fb` continuam Não verificáveis; o snapshot local é a única fonte.
