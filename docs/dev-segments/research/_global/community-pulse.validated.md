# Pulso da comunidade — validado (condensado)

Validação: 2026-10-09 · Validador independente (claude-sonnet-5-5; o pesquisador foi outro modelo) · Original: `community-pulse.md` (30 itens). Aprovados: 27 · Rejeitados: 3 · Itens re-verificados com ferramenta: 17 (~57%) + 2 checagens de injeção.
Rótulos: Verificado / Inferido / Suposição / Não verificável. Textos de comunidade são sinal de prática; nada vira regra sem cruzar com fonte A/B.

## Resultado da re-verificação (resumo)
- Confirmados nesta validação (Verificado): estrelas/licença/push de obra/superpowers (296.930★, MIT, push 2026-10-10 UTC), shanraisshan (67.314★, MIT), ykdojo (10.206★, licença `NOASSERTION` → só destilar), mattpocock/skills (282.946★, MIT — o original dizia "não verificado"); arXiv 2608.11095 (números batem); Anthropic Research (16/06/2026, 400k sessões, 15% vs 28–33%, 70%/80%); HN: Boris 568/403, Tane 976/591, HumanLayer 748/290, Amplifying 611/235, Ask HN 461/455; Amplifying (2.430 runs, v2.1.39, 12/20 "Custom", Railway 82%); doc oficial best-practices (existe, contém o prompt de entrevista, `/goal`, Stop hook, falhas comuns); support power-user tips (existe; `--bare` ~10x é alegação da página); Sanity (3 tentativas, 3 regras de paralelismo); rmoff (11/03/2026, 1.493 de ~5.458 estações); Breunig (04/05/2026, 10 lições); Dan Luu (existe; o repro falso veio do **Codex**, não do Claude — o original generalizava "agente"); Thariq tips (9 dicas, sem injeção).
- Observação: `pushed_at` 2026-10-10 aparece como "futuro" só por fuso (UTC); não é erro.
- Injeção: nenhuma nas fontes lidas. `harperreed/dotfiles/.claude/CLAUDE.md` confirmado como conteúdo com instruções a IA (postar em redes sociais, "não responde a ninguém", diário) — **não reaproveitar** (já marcado pelo pesquisador).
- Literal: único trecho literal é de superpowers/brainstorming (MIT, atribuído, ≤ 40 linhas; o arquivo real tem ~228 linhas, o trecho é parcial com "[...]"). Aceitável; manter atribuição. Demais textos são destilados.
- Não verificado nesta rodada (herdado do original): R-06 (talk), R-12, R-15, R-17 (Reddit espelho), R-19, R-25, R-27, R-16 (blogs). Mantidos com a classe rebaixada onde indicado.

---

## Itens aprovados

### R-01 — Setup do criador do Claude Code (Boris Cherny), 13+15 dicas
- URL: https://news.ycombinator.com/item?id=46470017 · thread https://twitter-thread.com/t/2007179832300581177 · compilação https://raw.githubusercontent.com/shanraisshan/claude-code-best-practice/main/tips/claude-boris-15-tips-30-mar-26.md · Classe A (9) · Licença: social (destilar); compilação MIT
- Verificado: HN 568/403 (2026-01-02). Métricas "2–3x" são autoavaliação.
- Reutilizável: (1) dar ao agente um comando de verificação antes de automatizar; (2) fluxos diários viram skill/comando versionado; (3) formatação por hook `PostToolUse`, não prosa; (4) allowlist em `.claude/settings.json` em vez de pular permissões; (5) tarefa longa termina com verificação independente (subagente novo ou Stop hook); (6) erro recorrente vira uma linha no CLAUDE.md.
- Ressalva: comandos mudam a cada 1–2 meses; conferir code.claude.com.
- [seg:git-workflow-release] [seg:web-frontend] [seg:code-quality-refactoring] [seg:llm-ai-agents] [seg:cli-desktop-tooling]

### R-02 — Best practices for Claude Code (doc oficial)
- URL: https://code.claude.com/docs/en/best-practices · Classe A (9) · Licença: proprietária (destilar)
- Verificado: página existe e contém tudo citado.
- Reutilizável: gradação de verificação (prompt → `/goal` → Stop hook → subagente verificador); Explore → Plan → Implement → Commit, pular plano se o diff cabe em uma frase; prompt de entrevista (AskUserQuestion) → `SPEC.md` → sessão nova; teste de corte do CLAUDE.md ("remover causaria erro?"); revisor adversarial só reporta lacunas de correção/requisito; 5 falhas comuns (kitchen sink, corrigir repetido, CLAUDE.md inchado, trust-then-verify, exploração infinita); após 2 correções, `/clear`.
- [seg:product-discovery-specs] [seg:qa-testing] [seg:code-quality-refactoring] [seg:technical-writing-docs] [seg:llm-ai-agents] [seg:architecture-design]

### R-03 — "How I use Claude Code" (Boris Tane)
- URL: https://boristane.com/blog/how-i-use-claude-code/ · Classe B (6) · Licença: não observada (destilar)
- Verificado: HN 976/591 (2026-02-22).
- Reutilizável: `research.md` → `plan.md` (arquivos, snippets, trade-offs) → ciclo de anotação humana → checklist de fases; implementação mecânica com typecheck contínuo; direção errada = `git revert` e re-escopo.
- Ressalva: preferir plano em markdown ao plan mode nativo é opinião isolada; "sem degradação após 50% de contexto" contradiz R-06/R-14.
- [seg:architecture-design] [seg:code-quality-refactoring] [seg:product-discovery-specs]

### R-04 — "Writing a good CLAUDE.md" (HumanLayer)
- URL: https://www.humanlayer.dev/blog/writing-a-good-claude-md · Classe B (6) · Licença: não observada
- Verificado: HN 748/290 (2025-11-30).
- Reutilizável: estrutura WHAT/WHY/HOW (incluindo como verificar); excluir comandos exaustivos, estilo, snippets; raiz curto (<60 linhas no autor, teto citado 300); progressive disclosure via `agent_docs/`; ponteiros `arquivo:linha`; linter/formatter em hook, não o LLM.
- Ressalva: sem benchmark; céticos no HN; tratar como consenso de prática.
- [seg:technical-writing-docs] [seg:llm-ai-agents] [seg:code-quality-refactoring]

### R-05 — "Why does CLAUDE.md keep growing?" (arXiv) + dissidentes
- URL: https://arxiv.org/abs/2608.11095 · https://alex-jacobs.com/posts/claudemd/ · https://zander.wtf/blog/claude-md-agents-md/ · https://news.ycombinator.com/item?id=48160604 · Classe B (5)
- Verificado: arXiv (11/08/2026): 247.694 instruções, 1.867 repositórios, +226%; comentários de raciocínio removem 99,3% do excesso e melhoram até 23,1% (WildIFEval). Autor único, sem revisão por pares (Não verificável).
- Reutilizável: toda regra comportamental com comentário `<!-- motivo: falha observada em data -->`; adicionar só na 2ª ocorrência; frasear positivamente; fatos > regras especulativas; poda trimestral ou a cada troca de modelo; `@AGENTS.md` como fonte única entre ferramentas.
- [seg:technical-writing-docs] [seg:llm-ai-agents] [seg:code-quality-refactoring]

### R-06 — Research → Plan → Implement e compactação intencional (Dex Horthy)
- URL: https://www.ai.engineer/talks/rmvDxxNubIg-context-engineering-for-complex-codebases · Classe B (5) · Licença: não aplicável (talk)
- Não verificado nesta rodada. Números de throughput são relatos de time.
- Reutilizável: `handoff.md` (objetivo, estado com arquivos/linhas, decisões e porquê, próximos passos com teste, riscos, comandos de verificação); gerar handoff antes de ~40% de contexto (guia aproximado, medir); escalar processo ao tamanho da tarefa; informação errada no contexto é o pior caso.
- [seg:architecture-design] [seg:code-quality-refactoring] [seg:llm-ai-agents]

### R-07 — Como escrever skills (Thariq Shihipar, Anthropic), 9 dicas
- URL: https://raw.githubusercontent.com/shanraisshan/claude-code-best-practice/main/tips/claude-thariq-tips-17-mar-26.md · Classe A (8; autoridade 3, mas via compilação de terceiro) · Licença: compilação MIT
- Verificado: as 9 dicas existem; sem instruções a IA.
- Reutilizável (checklist de SKILL.md): `description` = condição de disparo (PT-BR + EN); não declarar o óbvio; seção Gotchas viva; detalhes em `references/`; metas e restrições, não roteiro rígido; config do usuário em arquivo + perguntas estruturadas; scripts reutilizáveis; dados persistentes em pasta estável do plugin; hooks sob demanda documentados (sem hook ativo por padrão).
- [seg:llm-ai-agents] [seg:automation-integrations] [seg:technical-writing-docs] [seg:cli-desktop-tooling]

### R-08 — shanraisshan/claude-code-best-practice
- URL: https://github.com/shanraisshan/claude-code-best-practice · Classe B (7) · Licença: MIT (Verificado), 67.314★
- Reutilizável: tabela "onde colocar cada coisa" (hook = sempre/sem exceção; settings.json = permissão/modelo; skill = uso eventual; `.claude/rules` com `paths` = regra por caminho; CLAUDE.md = fato universal; subagente read-only = trabalho ruidoso/revisão); Command → Agent → Skill; fatias verticais (Pocock).
- Ressalva: compilação de terceiros; conferir cada dica na fonte; números como 40% vêm de falas.
- [seg:llm-ai-agents] [seg:technical-writing-docs] [seg:automation-integrations] [seg:git-workflow-release]

### R-09 — obra/superpowers (brainstorming + TDD)
- URL: https://github.com/obra/superpowers · https://raw.githubusercontent.com/obra/superpowers/main/skills/brainstorming/SKILL.md · Classe A (9) · Licença: MIT (Verificado), 296.930★, push 2026-10-10 UTC
- Reutilizável: brainstorming com decisão inicial (tudo no pedido → fazer; falta algo → conversar), uma pergunta por mensagem, "play back" curto, gate duro de aprovação, design doc revisado por subagente novo; TDD: sem produção sem teste vermelho pelo motivo certo, verde com suíte inteira, bug = teste antes do fix, exceções só com autorização humana.
- Literal (MIT, © Jesse Vincent/obra; trecho parcial do original): ver `community-pulse.md` R-09 — não duplicado aqui.
- Ressalva: tom "You MUST"/"1% de chance" conflita com D10; adaptar o tom. Estrelas = popularidade, não qualidade.
- [seg:product-discovery-specs] [seg:qa-testing] [seg:architecture-design] [seg:llm-ai-agents]

### R-10 — mattpocock/skills
- URL: https://github.com/mattpocock/skills · Classe B (7) · Licença: MIT (Verificado), 282.946★, push 2026-10-09
- Reutilizável: skills pequenas e componíveis; `grill-me` (`disable-model-invocation: true`); anti-padrões de teste (acoplado à implementação, tautológico, fatiamento horizontal, seam não acordado); testar por interface pública; nomear testes no glossário do domínio.
- Ressalva: arquivos auxiliares não lidos.
- [seg:qa-testing] [seg:product-discovery-specs] [seg:architecture-design] [seg:technical-writing-docs]

### R-11 — Agentic Engineering Patterns (Simon Willison)
- URL: https://simonwillison.net/guides/agentic-engineering-patterns/ · Classe B (6) · Licença: não observada
- Reutilizável: "Use red/green TDD" e **confirmar o vermelho**; testes manuais agentic (curl, `python -c`, browser automation, screenshots) e depois teste permanente; registrar comando + saída real (Showboat) contra relato "esperado"; roles `reviewer`, `test-runner`, `debugger`; não fragmentar em dezenas de especialistas.
- [seg:qa-testing] [seg:web-frontend] [seg:ux-ui-design] [seg:code-quality-refactoring] [seg:technical-writing-docs]

### R-12 — Agentic Coding Recommendations (Armin Ronacher)
- URL: https://lucumr.pocoo.org/2025/6/12/agentic-coding/ · Classe B (6) · Licença: não observada
- Não reverificado. HN 296/203 (original).
- Reutilizável: checklist de ferramenta pronta para agente (rápida, saída curta, erros acionáveis, idempotente/pidfile, logs em caminho fixo no CLAUDE.md, timeout); CLI antes de MCP; stacks estáveis e explícitas; refatorar quando o projeto excede o que o agente processa.
- Ressalva: `--dangerously-skip-permissions` em Docker contraria a regra da casa.
- [seg:backend-api] [seg:cli-desktop-tooling] [seg:automation-integrations] [seg:devops-cloud-infra]

### R-13 — Agentic coding and persistent returns to expertise (Anthropic Research)
- URL: https://www.anthropic.com/research/claude-code-expertise · Classe A (8)
- Verificado: 2026-06-16; ~400k sessões/~235k pessoas; sucesso verificado 15% vs 28–33%; humano ~70% do planejamento, Claude ~80% da execução. Achados preliminares segundo a própria Anthropic.
- Reutilizável: todo pedido gerado pelos plugins inclui escopo preciso, o que verificar (comando literal), critério de pronto e o que não mudar; em problema, re-planejar em vez de abandonar ou empilhar correção.
- [seg:product-discovery-specs] [seg:qa-testing] [seg:llm-ai-agents]

### R-14 — Claude Code power user tips (Anthropic Support)
- URL: https://support.claude.com/en/articles/14554000-claude-code-power-user-tips · Classe A (8)
- Verificado: página existe; `/batch`, `/simplify`, PostCompact, `--worktree`, `/loop` (até 3 dias), `--bare` presentes.
- Reutilizável: mapa evento → uso (SessionStart contexto; PreToolUse negar/logar; PostToolUse formatter; PermissionRequest roteamento; Stop checks; PostCompact reinjetar regras); worktrees por sessão; "prove o comportamento diffando main vs branch"; re-planejar em vez de corrigir.
- Ressalva: recursos novos/experimentais; conferir plano/versão.
- [seg:devops-cloud-infra] [seg:git-workflow-release] [seg:web-frontend] [seg:data-engineering] [seg:data-science-ml] [seg:code-quality-refactoring]

### R-15 — How Anthropic teams use Claude Code + sessões Code w/ Claude 2026
- URL: https://claude.com/blog/how-anthropic-teams-use-claude-code · Classe B (7) · Licença: proprietária
- Não reverificado. Estudo de 2025-07-24 (anterior a skills/plugins); métricas autodeclaradas.
- Reutilizável: descrever comportamento observado, não a mudança de código; segurança: pseudocódigo primeiro + TDD com check-ins; Terraform plan explicado para aprovação; pergunta de triagem "skill (o que sabe) / subagente (quem faz) / tool (o que o sistema pode)" com eval mínimo por decomposição.
- [seg:security-appsec] [seg:devops-cloud-infra] [seg:sre-observability] [seg:data-science-ml] [seg:ux-ui-design] [seg:llm-ai-agents]

### R-16 — Subagentes na prática (Zach Wills, Prab, HAMY, 3 blogs BR)
- URL: https://zachwills.net/how-to-use-claude-code-subagents-to-parallelize-development/ · https://software.rajivprab.com/2026/07/13/using-subagents-to-improve-claude-code/ · https://hamy.xyz/blog/2026-02_code-reviews-claude-subagents · https://thalesgomes.com/blog/subagentes-claude-code-quando-usar/ · Classe B (5; fontes individuais C, corroboradas por R-02/R-14) · Licença: não observada
- Não reverificado. Sem medição controlada; custo de paralelismo é estimativa de terceiros.
- Reutilizável: um escritor por arquivo; revisor read-only em contexto novo, achados critical/major/minor, "não altere código, não elogie", veredito final; test-author separado do implementer, proibido enfraquecer testes; grave SHA literal (variável vazia no shell novo do subagente); subagente só para escopo fechado, saída ruidosa ou paralelo; se depende do contexto acumulado, fica no principal; `description` comportamental; ferramentas mínimas; Explore/Plan não leem CLAUDE.md; não encadear subagentes.
- [seg:qa-testing] [seg:code-quality-refactoring] [seg:security-appsec] [seg:llm-ai-agents]

### R-17 — Ralph Wiggum loop (Geoffrey Huntley)
- URL: https://ghuntley.com/ralph/ · Classe B (5; rebaixada: Reddit via espelho, autoridade individual) · Licença: não observada
- Reutilizável (checklist pré-loop): specs revisadas por humano com critérios **na spec**; um item por iteração; back pressure determinístico (testes + tipos/lint); proibido apagar/afrouxar testes; commit só com verde; limite de iterações/orçamento; só greenfield ou sandbox.
- Ressalva: conflita com a regra da casa de autorização para ações externas; usar só em sandbox com permissões explícitas.
- [seg:llm-ai-agents] [seg:automation-integrations] [seg:git-workflow-release] [seg:qa-testing]

### R-18 — ykdojo/claude-code-tips
- URL: https://github.com/ykdojo/claude-code-tips · Classe B (6) · Licença: **NOASSERTION** (API) — destilar apenas; 10.206★, push 2026-09-25
- Reutilizável: higiene de contexto (tarefa nova → `/clear`; handoff antes da compactação; 2 correções → recomeçar; `/btw`; exploração em subagente); `TESTING.md` gerado pelo agente (o que foi testado, comando, saída, o que não foi testado) revisado pelo humano; ambientes isolados para tarefas arriscadas.
- [seg:git-workflow-release] [seg:qa-testing] [seg:devops-cloud-infra] [seg:llm-ai-agents]

### R-19 — Hooks como guardrails determinísticos
- URL: https://aitmpl.com/blog/secure-git-workflow/ · https://dev.to/oikon/24-claude-code-tips-claudecodeadventcalendar-52b5 · Classe B (6; princípio corroborado por A: R-02/R-14) · Licença: não observada
- Reutilizável: `PreToolUse/Bash` lê JSON do stdin, sai `0` se irrelevante, `exit 2` + motivo para negar (`rm -rf` fora de paths, `git push --force` em main, `DROP TABLE`, `terraform apply`, `kubectl delete`, migrate em prod, leitura de `.env`); `PreToolUse/Edit|Write` nega `migrations/`, locks, infra de produção; `PostToolUse` formatter; `Stop` roda testes respeitando o cap de bloqueios; `PostCompact` reinjeta regras; cada hook documenta evento, matcher, script stdlib, exit codes, teste, desativação.
- Ressalva: plugins não trazem hooks ativos; **não** executar `npx` de terceiros — reescrever em stdlib; regex não substitui gitleaks; validar o esquema em code.claude.com/docs/en/hooks.
- [seg:security-appsec] [seg:git-workflow-release] [seg:database-data-modeling] [seg:devops-cloud-infra] [seg:automation-integrations]

### R-20 — Vozes críticas e evidência (Dan Luu, Lars Faye, Four Horsemen)
- URL: https://danluu.com/ai-coding/ · https://larsfaye.com/articles/agentic-coding-is-a-trap · https://distantprovince.substack.com/p/the-four-horsemen-of-agentic-coding · Classe B (7 pela parte empírica)
- Verificado (Dan Luu): o repro falso em vídeo foi produzido pelo **Codex** em ambiente de browser artificial; fuzzing tende a vencer LLM na busca de bugs, com variância alta entre execuções.
- Reutilizável: nunca aceitar "pronto" sem saída de comando/teste/screenshot gerados na sessão; vídeo não prova ambiente real (exigir comando e stdout); bug = reprodução executada, depois teste permanente; análise de dados com loop humano e rótulo Inferido até reexecução; limitar diff ao que se revisa; avaliar abordagem com ≥3 execuções e distribuição.
- Ressalva: ensaios de opinião; "47% de queda em debugging" atribuído à Anthropic não verificado.
- [seg:qa-testing] [seg:data-science-ml] [seg:code-quality-refactoring] [seg:security-appsec]

### R-21 — Ask HN: evidência de que agentic coding funciona
- URL: https://news.ycombinator.com/item?id=46691243 · Classe B (6)
- Verificado: 461 pts / 455 comentários (2026-01-20).
- Reutilizável: consenso — medir é difícil, escopo e stack importam, disciplina de processo decide; fronteiras de módulo fortes; reset de contexto ao derivar; logar para o agente "ver"; texto de calibração para README ("organiza processo, não promete ganhos; medir no seu contexto, mais de uma execução").
- Ressalva: comentários anônimos, viés de autosseleção.
- [seg:product-discovery-specs] [seg:qa-testing] [seg:architecture-design] [seg:mobile-apps]

### R-22 — "First attempt will be 95% garbage" (Sanity)
- URL: https://www.sanity.io/blog/first-attempt-will-be-95-garbage · Classe B (6)
- Verificado: Vincent Quigley, 2025-09-02; regra das três tentativas; 3 regras de paralelismo; HN 550/396 (original).
- Reutilizável (`team-adoption.md`): nenhuma sessão paralela no mesmo módulo; toda tarefa de agente tem ticket; marcar código editado por humano; revisão em 3 camadas (Claude → engenheiro → time); DB de produção nunca conectado ao agente (read-only em não-prod); começar por tarefas repetitivas; orçamento mensal explícito.
- Ressalva: percentuais e "2–3x" informais; custo de 2025.
- [seg:code-quality-refactoring] [seg:git-workflow-release] [seg:database-data-modeling]

### R-23 — 10 Lessons for Agentic Coding (Drew Breunig)
- URL: https://www.dbreunig.com/2026/05/04/10-lessons-for-agentic-coding.html · Classe B (7)
- Verificado: 2026-05-04, as 10 lições.
- Reutilizável: três artefatos vivos por feature (SPEC.md, testes e2e comportamentais, notas de intenção); ao final, diffar spec vs construído; implementar para aprender; achar o difícil (design, performance, segurança, resiliência).
- Ressalva: ensaio de opinião, sem dados.
- [seg:product-discovery-specs] [seg:qa-testing] [seg:technical-writing-docs] [seg:architecture-design]

### R-24 — What Claude Code actually chooses (Amplifying)
- URL: https://amplifying.ai/research/claude-code-picks · Classe B (7)
- Verificado: 2.430 execuções, 3 modelos, 20 categorias, v2.1.39, "Custom/DIY" em 12/20, Railway 82% (Python), HN 611/235.
- Reutilizável: skill de bootstrap sempre declara stack, hospedagem, ORM, auth e flags antes de gerar código; proibir auth/cripto/flags/cache próprios quando há biblioteca padrão (lista aceita em `references/`).
- Ressalva: preferência do modelo, muda por versão; estudo de empresa.
- [seg:web-frontend] [seg:backend-api] [seg:database-data-modeling] [seg:devops-cloud-infra] [seg:saas-multitenant] [seg:security-appsec]

### R-25 — Spec-driven na comunidade (Dwyer, Show HN SDD)
- URL: https://www.dwyer.co.za/static/claude-code-is-all-you-need.html · Classe B (5)
- Não reverificado. Repo do Show HN com baixa adoção (licença Não verificável) — não usar.
- Reutilizável: `SPEC.md` ≤ ~500 palavras (problema, usuários/cenário, requisitos testáveis, fora de escopo, arquivos/interfaces, restrições, verificação e2e); spec revisada → sessão nova só com a spec → registrar divergências ao final; promoção a produção em etapas.
- Ressalva: Dwyer usa `--dangerously-skip-permissions` (contra a casa); falhas relatadas (deps de 500MB, métricas alucinadas, DB derrubado).
- [seg:product-discovery-specs] [seg:backend-api] [seg:cli-desktop-tooling] [seg:automation-integrations]

### R-26 — dbt real com eval harness (Robin Moffatt)
- URL: https://rmoff.net/2026/03/11/claude-code-isnt-going-to-replace-data-engineers-yet/ · Classe B (6)
- Verificado: 2026-03-11; Opus 4.6 + dbt-agent-skills; ~1.493 de ~5.458 estações carregadas (causa exata, limite de 2000 vs paginação, "não totalmente estabelecida" na própria página).
- Reutilizável (checklist de pipeline): contagem origem vs destino; campos origem vs colunas; idempotência; testes unique/not null/relationships/freshness; revisar decisões "literais do prompt" (SCD2 só numa entidade); coerência SQL vs Python. Prompt e skills pesam mais que o modelo.
- Ressalva: um projeto, harness próprio.
- [seg:data-engineering] [seg:database-data-modeling] [seg:data-science-ml]

### R-27 — Embarcados: loop com hardware real (Bitcraze)
- URL: https://www.bitcraze.io/?p=14780 · Classe B (5)
- Não reverificado. Experimento único, tarefa simples.
- Reutilizável: daemon local para link stateful + comandos one-shot (`flash`, `reset`, `console --since`, `log`, `param`) com saída curta e exit code; skill do ciclo build → flash → observar → corrigir com limites (não inferir registradores; exigir header/datasheet); nunca flashar fora da bancada sem autorização.
- [seg:systems-embedded-iot] [seg:cli-desktop-tooling] [seg:llm-ai-agents]

---

## Rejeitados

| Item | Motivo |
| --- | --- |
| R-28 — Mobile e game dev (thepromptshelf, dev.to Godot, Reddit 2 pts) | Classe C (4): guia sem autor, devlog abandonado, 1 post com 2 pontos; nenhuma fonte A/B. Conteúdo útil (separar terminal/Xcode, "limites do agente" no CLAUDE.md) só entra como princípio rotulado Inferido, cruzado com R-13/R-21. Lacuna aberta para `mobile-apps` e `game-development`. |
| R-29 — Skill multiagente de auditoria Solidity (r/ethdev) | Classe C (3): 3 pontos/1 comentário, repo não localizado, licença e estrelas não verificáveis; auditoria por LLM tem alta variância (R-20). Esqueleto (inventário de entry points, PoC executável, nunca descartar em silêncio) permanece apenas como Suposição a validar por lente authoritative/github. |
| R-30 — SRE/DevOps (Towards AI, newsletter AWS Fundamentals, skill Terraform) | Classe C (3): newsletter promocional, post Medium não lido na íntegra, métricas autodeclaradas, repo da skill não verificado. A regra "leitura livre, escrita confirmada" está corroborada por R-15/R-19 e é mantida via esses itens. |

## Princípios / achados transversais

- Verificação executável é a alavanca nº 1; sem saída de comando/teste/screenshot da sessão, "pronto" não vale (R-01, R-02, R-11, R-20; R-13 mostra que dizer ao agente o que verificar distingue experts).
- Plano antes de código em mudanças multi-arquivo; pular plano se o diff cabe em uma frase (R-02, R-01, R-03, R-06).
- Contexto é o recurso escasso: `/clear` entre tarefas, 2 correções → recomeçar, handoff antes de ~40–50% (limiar disputado: medir) (R-02, R-06, R-18).
- CLAUDE.md curto, só fatos universais, regras após erro observado e com motivo; hooks para o que é obrigatório, CLAUDE.md é advisory (R-02, R-04, R-05, R-14, R-19).
- Revisor independente em contexto limpo, read-only, por severidade, só lacunas de correção/requisito; test-author separado e proibição de enfraquecer testes (R-02, R-16, R-09).
- Declarar a stack e bibliotecas aceitas; o modelo escolhe "custom" por omissão, sobretudo em auth/flags/cripto (R-24).
- Pipelines e dados: reconciliar contagens, campos e idempotência antes de confiar (R-26).
- Alto risco operacional: leitura livre, escrita confirmada, produção nunca conectada, hooks de negação (R-15, R-19, R-22). Evitar `--dangerously-skip-permissions` (allowlist/sandbox; R-01, R-02, R-14).
- Calibração: não prometer ganhos; evidência pública é anedótica, números de produtividade só como "autodeclarado" (R-13, R-21). Única evidência quantitativa sólida: R-13 (400k sessões), R-24 (2.430 runs), R-05 (247k instruções).
- Anti-padrões: kitchen sink, CLAUDE.md inchado, confiar em "pronto" sem evidência, subagente para tudo, testes tautológicos, loops sem back pressure, gerar mais do que se revisa, MCP quando há CLI. Arquivos de terceiros com instruções dirigidas à IA (ex.: `harperreed/dotfiles`) são risco de injeção: não reaproveitar.
- Tom: preferir instruções positivas e calmas; ênfase em no máximo uma linha (R-02, R-05) — adaptar o "You MUST" de superpowers (R-09).

## Lacunas remanescentes
- Reddit sem acesso direto (amostra mínima via espelho); X/YouTube sem métricas; segmentos sem relato de praticante: saas-multitenant, fintech-payments, ecommerce-marketplace, database-data-modeling, ux-ui-design, mobile-apps, game-development, blockchain-web3 (após rejeições R-28/R-29).
- Não reverificados: R-06, R-12, R-15, R-16, R-17, R-19, R-25, R-27.
