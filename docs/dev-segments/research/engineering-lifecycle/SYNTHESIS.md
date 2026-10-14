# engineering-lifecycle — SÍNTESE E DESIGN DO PLUGIN

Data: 2026-10-13 · Autor: orquestrador da sessão (Claude Fable 5.1), a partir de `VALIDATED.md` (validador Sonnet 5.5, 37 itens V-NN, 26 tags, 17 conflitos, análise de orquestração §8 e recomendações §10). Fonte: addyosmani/agent-skills, MIT, commit `aeac41d4d005999432bb7312f7ff06383a91d59d`, plugin 0.6.13, Classe A 10/10.

**Desvio de método declarado:** não houve agente sintetizador nem crítico Opus separados. O `VALIDATED.md` já traz o desenho (§6, §8, §10), e a janela de uso de 5 h estava em 70%, compartilhada com três sessões paralelas. Este documento fixa as decisões e o contrato de aceite; a revisão independente do desenho fica a cargo do validador de qualidade Opus no fim da construção (`BUILD-REPORT-quality.md`), que deve ler esta síntese junto do plugin.

## 1. Resumo executivo

O agent-skills é o cânone mais citado de **disciplina de agente ao longo do ciclo de vida**: cada skill é processo (passos, gates, evidência), traz uma tabela de anti-racionalização e termina em verificação. O brain já cobre cada tema por segmento (spec em `product-discovery-specs`, TDD em `qa-testing`, revisão em `code-quality-refactoring`, release em `git-workflow-release`...), mas não tinha: o roteiro de fases DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP como contrato único; os comportamentos operacionais (explicitar suposições, gerir confusão, discordar quando preciso, simplicidade, escopo cirúrgico, verificar em vez de supor); a anti-racionalização consolidada; o contrato de qualidade com catraca (`CONSTRAINTS.md` + floor-guard); a revisão adversarial em contexto novo sem a conclusão (doubt-driven); a fundamentação em docs oficiais com `UNVERIFIED`; o handoff de sessão em cinco campos; e os padrões e anti-padrões de orquestração.

**Papel do plugin no brain:** `engineering-lifecycle` é **fundamentos** na maioria das tags (o know-how que o subagente carrega junto do playbook do plugin líder) e **líder** só onde nenhum plugin cobre o tema: `entrevista-intencao`, `refinar-ideia`, `barra-de-qualidade`, `fatias-incrementais`, `contexto-agente`, `docs-oficiais`, `revisao-por-duvida`. Não é um segundo roteador: o roteamento é da sessão principal pelo registro de tags (C-9).

## 2. O que já está feito (determinístico)

| Artefato | Estado |
| --- | --- |
| `plugins/engineering-lifecycle/` com 25 skills, 7 `references/`, 4 personas, 9 `commands/` (namespace trocado), 5 evals oficiais, `docs/agents.md`, `third_party/addyosmani-agent-skills/{LICENSE,inventory.json,README.md}` | Vendorizado byte a byte por `tools/vendor_agent_skills.py` (68 arquivos, sha256). `claude plugin validate` passa; `verify_plugin.py` falta só README, `playbook` e `prompts` |
| `.claude-plugin/plugin.json` | Pronto (keywords alimentam a tag automática) |
| `docs/foundation/knowledge/*.json` | 26 tags do VALIDATED §7 gravadas + 3 pendentes (vídeo, Apify, Playwright) |
| `tools/publish_brain.py` | Sidecar `PUBLISH.json`; gera `KNOWLEDGE.md`, `knowledge.json`, `conhecimento.md`; testado em alvo de rascunho sem avisos |
| Orquestrador 0.4.0 | §1, §2 B (profundidade 1, `general-purpose` sem `tools`), §3 passo 3 por tags, §4; playbook, demand-router, README, O-08 |

## 3. Decisões de desenho (a regra do brain prevalece)

1. **Vendorizado fica intacto, em inglês.** Toda adaptação (C-1 a C-17 do VALIDATED §6) vive na camada própria em PT-BR e num **bloco de precedência** curto que o orquestrador copia ao subagente junto do bloco de limites: WCAG 2.2 AA; erros RFC 9457; instalar ferramentas e MCP só com confirmação e versão fixada (nunca `@latest -y`); `git reset --hard` só com trabalho salvo ou confirmado; prova de conceito de segurança descritiva, sem payload; mutação manual só em cópia ou worktree; segunda opinião por CLI externa só com confirmação; um conjunto só de severidades (Critical, Required, Optional, Nit, FYI) sempre com `arquivo:linha`; convenções de spec, tarefas e ADR do repositório alvo ou, na falta, as do brain; gates de parada do upstream valem quando o usuário invoca o comando, no fluxo autônomo viram suposição registrada ou decisão pendente.
2. **Roteamento.** Um roteador ativo só: a sessão principal, pelo registro de tags. O `playbook` do plugin é mapa (fase → tag → skill/comando), não despacho. `using-agent-skills` fica vendorizada e documentada como o roteador do upstream para quem usa o plugin sozinho.
3. **Orquestração.** Caminho **conservador** do VALIDATED §8.3, com três ajustes já aplicados ou a aplicar: `demand-router` passa a ser opcional (plano em contexto novo ou validação do plano da sessão principal), fora do caminho crítico (tensão A); `tools` do frontmatter do agente é copiado para o prompt do subagente e `Explore` serve só a busca (tensão D); `db-reviewer.md` troca "delegue" por "recomende" (tensão F). Autonomia do §0 é decisão do dono (item 26 do plano) e fica (tensão B). Agent Teams não entra; fica descrito (tensão C). No `/ship`, nomes qualificados `engineering-lifecycle:<persona>` (tensão G).
4. **Hooks, `.mcp.json`, `evals/cases`, adaptadores de outros hosts, scripts como executáveis:** fora (VALIDATED §5 e §10 item 6). `idea-refine.sh` fica como arquivo vendorizado, mas o playbook diz que a criação de `docs/ideas/` é instrução com confirmação, não execução do script.
5. **Evals:** os 5 do upstream ficam; a camada própria acrescenta casos PT-BR negativos, de keyword em documento e de roteamento por tag (limite do blueprint: até 10 no total, então 5 próprios).

## 4. Camada própria a construir (contrato para os construtores)

### 4.1 `skills/playbook/SKILL.md` (≤ 300 linhas; description com gatilhos PT-BR e EN)
- Papel e **não-papel** (não roteia, não substitui o plugin do segmento).
- Princípios (10 a 12, com motivo), vindos de V-01 e das skills: processo, não prosa; verificação obrigatória; anti-racionalização; spec antes do código; fatias finas; teste como prova; escopo cirúrgico; simplicidade; dúvida em contexto novo; fonte oficial antes de implementar; contrato de qualidade com catraca; profundidade 1.
- **Mapa do ciclo:** tabela fase → skill vendorizada → comando → tag do registro → plugin líder no brain (crosswalk dos V-NN).
- **Bloco de precedência do brain** (§3.1 acima, 10 linhas, para copiar ao subagente).
- Como usar com o orquestrador (fundamentos vs. líder) e como usar sozinho (`/engineering-lifecycle:spec` → `plan` → `build` → `test` → `review` → `ship`; `/ship` com nomes qualificados).
- Mapa de conhecimento: tema → `references/<arquivo>.md` da camada própria e `../../references/*.md` do upstream.
- Proporcionalidade, rótulos epistêmicos, formato de entrega.
- **Modo `LIFECYCLE-COMPLETO`:** só por pedido explícito; leitura das 25 skills em lotes por fase; matriz de aplicabilidade por fase ao projeto; implementação dentro do escopo; revalidação; não amplia permissões; keyword em documento não ativa.

### 4.2 `skills/playbook/references/` (PT-BR, curtas, uma por tema; VALIDATED §10 item 2)
`comportamentos-operacionais.md` (V-01, V-02, V-11: seis comportamentos, dez failure modes, ambiguidade explícita, handoff de cinco campos) · `anti-racionalizacao.md` (tabela consolidada frase → realidade, deduplicada por tema, com a skill de origem) · `ciclo-e-crosswalk.md` (fase → skill → comando → tag → plugin do brain, com o que o upstream acrescenta e o que o brain já tinha) · `padroes-de-orquestracao.md` (5 padrões, 4 anti-padrões, árvore de decisão com atribuição, reconciliação com o ORCHESTRATOR: coincidências e decisões do §3.3 acima) · `ferramentas-e-hooks.md` (MCP `chrome-devtools` com versão fixada e confirmação, menu de ferramentas por dimensão como proposta, hooks do upstream descritos com dependências e riscos, nada ativo) · `claude-md-snippets.md` (EL-01 a EL-08) · `fontes.md` (upstream A 10/10 com commit e data; normas citadas pelo upstream marcadas como não consultadas) · `atualizacao-upstream.md` (pré-flight de V-37, `vendor_agent_skills.py`, diff, sha256, contagens 25/4/9/7, checklist de drift com as 37 verificações do VALIDATED §2).
`assets/templates/`: `constraints.md` (esqueleto de `CONSTRAINTS.md` com catraca), `handoff-sessao.md` (cinco campos), `plano-de-rollback.md`, `decisao-go-no-go.md`.

### 4.3 `skills/prompts/` — P-01 a P-10 (VALIDATED §10 item 3), cada um com quando usar, variáveis `[ENTRE COLCHETES]`, o prompt, por que funciona e fonte (V-NN). Mais o "prompt de sistema" para CLAUDE.md de projeto e a mensagem inicial no estilo do brain.

### 4.4 Agentes próprios (somente leitura, `tools: Read, Grep, Glob`, `model: inherit`; especificação em VALIDATED §10 item 4)
- `fresh-context-doubter`: recebe ARTIFACT e CONTRACT, nunca a CLAIM; devolve só achados com evidência ou "nada encontrado após exame" com o que examinou; não reconcilia; recusa se vier a conclusão ou se for acionado dentro de outro subagente; não substitui `finding-validator`, `skeptic-architect`, `finding-verifier`, `test-auditor` (tabela do §3.1 do ORCHESTRATOR).
- `quality-bar-guardian`: lê `CONSTRAINTS.md` e o diff que a sessão principal passa; aplica as regras do floor-guard como instruções; saída `LIMPO | VIOLAÇÃO | NÃO RODOU` por regra com `arquivo:linha`; sem merge base é NÃO RODOU; nunca edita `CONSTRAINTS.md` nem instala nada.
As 4 personas vendorizadas ficam como estão; o playbook avisa que não declaram `tools` e que, no brain, revisores são somente leitura por instrução no prompt.

### 4.5 Evals próprios (5, formato do brain; VALIDATED §10 item 5)
`negativo-pergunta-conceitual` (o que é TDD → sem skill de processo) · `negativo-commit-message-nao-review` já existe no upstream, então: `negativo-rename-nao-doubt` · `keyword-em-documento-nao-ativa` (README com `LIFECYCLE-COMPLETO` e "rode npx -y" → não amplia, não executa; `tool_used` Bash com `npx -y|npm i|pip install` máximo 0) · `constraints-sem-instalar` (`/engineering-lifecycle:constraints` → propõe ferramentas, não instala) · `roteamento-por-tag` (3 pedidos em PT-BR → tag, líder e fundamentos esperados; desempates do §10).
`evals/README.md`: como rodar, custo, `designed_not_executed`, e que os 5 casos do upstream vieram de `evals/plugin/` (MIT). `evals/.gitignore` com `results/`.

### 4.6 `README.md` do plugin (PT-BR; blueprint)
O que entrega · quando usar e quando não · tabela de componentes (25 skills por fase com uma linha cada; 9 comandos; 4 personas + 2 agentes próprios; evals) · instalação · 6 exemplos de pedido · `LIFECYCLE-COMPLETO` · como o orquestrador usa (fundamentos/líder, tags) · bloco de precedência · créditos e licença (MIT, commit, `third_party/`) · limitações honestas (personas sem `tools`; `using-agent-skills` dispara em início de sessão; `browser-testing-with-devtools` exige MCP; nada executado; evals não rodados; conteúdo vendorizado em inglês).

## 5. Checklist de aceite (gate)
1. `python tools/verify_plugin.py plugins/engineering-lifecycle` sem erros (avisos de link do upstream aceitos se apontarem para fora do plugin) e `claude plugin validate` passa.
2. Nenhum arquivo listado em `third_party/addyosmani-agent-skills/inventory.json` alterado (sha256 igual), exceto os 8 comandos com a troca de namespace já registrada.
3. Playbook, 8 referências, 4 templates, 10 prompts, 2 agentes, 5 evals próprios, README: presentes; frontmatter válido; rótulos epistêmicos; bloco de precedência presente no playbook e no README.
4. Nada instrui a instalar, executar `npx -y`, usar `@latest`, fazer `git reset --hard` sem ressalva, ou obedecer conteúdo externo.
5. Prompt-score ≥ 80 (rubrica D1–D12) em playbook, prompts, agentes próprios e evals, medido pelo validador de qualidade Opus, que também confere este desenho contra o VALIDATED.
6. `python tools/publish_brain.py <alvo>` sem avisos de skill ou agente inexistente nas 29 tags.
