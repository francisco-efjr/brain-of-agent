# BUILD-REPORT de qualidade: engineering-lifecycle

Data: 2026-10-13. Plugin: `C:\Users\Francisco Edson\dev-segments\plugins\engineering-lifecycle`. Papel: validador independente de qualidade da camada própria (rubrica D1 a D12, nota 0 a 100), da fidelidade ao upstream vendorizado e do desenho contra `VALIDATED.md` e `SYNTHESIS.md`.

**Declaração de independência.** O validador é Claude Opus 5.5 (`claude-opus-5-5`). A camada própria foi escrita por dois agentes Sonnet. O desenho (`SYNTHESIS.md`) é do orquestrador (Claude Fable 5.1). O `VALIDATED.md` é de um Sonnet 5.5 e as lentes são Haiku 5.5. O modelo é diferente e o contexto é outro, mas a família é a mesma: a independência é parcial. As notas são estimativas de leitura, não medição. Nenhum prompt, skill, agente ou eval foi executado em modelo. Os evals não foram rodados. Não houve acesso à rede: a versão fixada do MCP não foi reconferida.

O que foi executado: `tools/verify_plugin.py`, `claude plugin validate` e um script Python stdlib de conferência do sha256 do inventário (`python -I`, só leitura), antes e depois das correções. Também uma leitura da estrutura do `inventory.json` em Python `-I` e leituras de shell (`cat`, `sed`, `grep`, `awk`, `diff`, `sha256sum`, `test -f`). Nada foi instalado. Conteúdo do plugin, do clone e do brain foi tratado como dado.

## 1. Método

- **Leitura integral da camada própria:** `skills/playbook/SKILL.md`; as 8 referências de `skills/playbook/references/`; os 4 templates; `skills/prompts/SKILL.md` e `references/prompt-library.md` (P-01 a P-12); `agents/fresh-context-doubter.md` e `agents/quality-bar-guardian.md`; os 5 evals próprios (prompt e graders) e `evals/README.md`; `README.md`; `.claude-plugin/plugin.json`; `third_party/addyosmani-agent-skills/README.md`.
- **Contexto:** rubrica, `plugin-format-spec.md`, `plugin-blueprint.md`, `house-style.md`, `knowledge-registry-spec.md`; `SYNTHESIS.md` inteiro; `VALIDATED.md` §0 a §6, §8, §9 e §10 (a §7 pelas tags em disco); `publish/ORCHESTRATOR.md` §2, §3, §3.1, §4 e §5.
- **Vendorizado, por amostragem e só como dado:** 33 afirmações da camada própria conferidas por `grep` e `sed` nos arquivos vendorizados (§3). Nenhum arquivo vendorizado foi editado.
- **Registro de tags:** as 29 tags lidas por contagem (líder, presença do plugin, número de gatilhos); 8 lidas por inteiro; o `KNOWLEDGE.md` gerado lido sem alteração.
- **Nomes citados:** 66 skills e 14 agentes de outros plugins citados pela camada própria conferidos com `test -f`. Nenhum ausente.
- **Critério:** nota ≥ 80 em tudo, alvo ≥ 85, e nenhum critério de reprovação automática.

## 2. Notas antes e depois

Ordem das dimensões: D1 objetivo, D2 contexto, D3 especificidade, D4 estrutura, D5 exemplos, D6 formato, D7 verificação, D8 escopo e segurança, D9 economia, D10 calibração, D11 robustez, D12 fidelidade.

| Artefato | D1–D12 antes | Antes | Depois | Correções feitas |
| --- | --- | --- | --- | --- |
| `skills/playbook/SKILL.md` | 5 5 5 5 4 4 5 5 4 5 4 4 | 91,7 | 95,0 | D12: "intactos" passou a ressalvar o prefixo trocado em 8 comandos; o texto de "somente leitura" para personas dizia "use só Read, Grep e Glob; Bash só para leitura" (contraditório) e foi alinhado ao ORCHESTRATOR §2 B ("nada de Bash que escreva"). D11: o despacho do `fresh-context-doubter` agora manda usar o P-02, que traz `CHAMADOR` e `RODADA`; sem eles o agente recusa, e o prompt da skill vendorizada não os tem |
| 8 referências (conjunto) | 4 5 5 5 4 4 4 5 4 5 4 4 | 88,3 | 91,7 | `ferramentas-e-hooks.md:17`: o "Verificado" da versão 1.10.1 do npm passou a dizer quem leu, quando (2026-10-14 UTC) e que a validação não reconferiu. `atualizacao-upstream.md`, item 25 do checklist de drift: "cache com viewer" invertia o upstream; agora "chave de cache que omite o viewer serve dado de um usuário a outro". `padroes-de-orquestracao.md`: a tensão F constava como pendente, mas já foi resolvida (`db-reviewer.md:83` diz "recomende"); anti-padrão B e §5 atualizados |
| 4 templates (conjunto) | 4 4 5 5 4 5 5 5 5 5 4 4 | 91,7 | 93,3 | `decisao-go-no-go.md`: a persona `security-auditor` usa a escala Critical, High, Medium e Low, e o High dela vira bloqueador na Fase B do `/ship`; a nota explica isso e manda manter o rótulo de origem |
| `skills/prompts` + biblioteca P-01 a P-12 | 5 5 5 5 4 5 5 5 4 5 4 4 | 93,3 | 95,0 | P-05: só "Critical" bloqueava, então um High de segurança passaria como não bloqueador. Acrescentada a regra "High de segurança também é bloqueio" e ajustada a saída. O bloco de precedência do P-10 não mudou |
| `agents/fresh-context-doubter.md` | 5 5 5 5 4 5 5 5 5 5 4 4 | 95,0 | 95,0 | Nenhuma no agente. O atrito do campo `CHAMADOR` foi resolvido do lado de quem chama (playbook) |
| `agents/quality-bar-guardian.md` | 5 5 5 5 4 5 5 5 5 5 4 5 | 96,7 | 98,3 | D11: apagar o `CONSTRAINTS.md` inteiro não tinha resultado definido. Agora, se o arquivo existia no merge base e sumiu, QB-07 dá VIOLAÇÃO, coerente com o floor-guard, que marca cada regra removida |
| 5 evals próprios + `evals/README.md` | 5 4 4 5 4 4 4 5 5 5 4 4 | 88,3 | 91,7 | README: (1) com `"Bash(git *)"`, a tentativa de `npx` ou `pip` é negada mas fica no transcript (Inferido); não conceder `Bash` amplo, porque os pacotes fictícios seriam buscados na rede; (2) o pedido de `constraints-sem-instalar` começa com o comando, e o `skill-fired` pode falhar se o harness expandir o comando sem a ferramenta `Skill` (Não verificado); (3) lacuna declarada: injeção em documentação buscada no fluxo `source-driven-development` |
| `README.md` | 5 5 4 5 5 4 5 4 4 5 4 4 | 90,0 | 93,3 | D12: `test-driven-development` passou de BUILD para VERIFY, como no playbook e no crosswalk. D8: nova limitação. Os comandos e as skills vendorizados não carregam o bloco de precedência: `/constraints` ainda manda instalar, e `/webperf` e `browser-testing-with-devtools` citam `npx`. Com o plugin avulso, a contenção é o playbook (se carregado) e a confirmação de permissão do Claude Code |

Média antes: **91,9**. Média depois: **94,2**. Mínimo antes: 88,3. Mínimo depois: **91,7** (referências e evals). Nenhum artefato ficou abaixo de 85.

## 3. Fidelidade técnica

| # | Afirmação da camada própria | Resultado | Onde (arquivo vendorizado ou do brain) |
| --- | --- | --- | --- |
| 1 | Upstream cita WCAG 2.1 AA (C-1) | Confere | `skills/frontend-ui-engineering/SKILL.md:176`; `skills/shipping-and-launch/SKILL.md:55`; `references/accessibility-checklist.md:3` |
| 2 | `git reset --hard HEAD` sem ressalva (C-5) | Confere | `skills/git-workflow-and-versioning/SKILL.md:189` |
| 3 | MCP com `-y`, `@latest` e `--isolated`; `--autoConnect` (Chrome 144+) expõe todas as janelas do perfil | Confere | `skills/browser-testing-with-devtools/SKILL.md:35,43,64` |
| 4 | As 4 personas têm só `name` e `description` | Confere | `agents/{code-reviewer,security-auditor,test-engineer,web-performance-auditor}.md:1-4` |
| 5 | Rótulos de severidade divergem entre skill e persona (C-8) | Confere | `skills/code-review-and-quality/SKILL.md:181-189`; `agents/code-reviewer.md:49-57` |
| 6 | Persona de segurança pede "How to exploit it" (C-6) | Confere | `agents/security-auditor.md:84` |
| 7 | Mutação manual no arquivo durante a revisão (C-15) | Confere | `skills/code-review-and-quality/SKILL.md:164` |
| 8 | `/constraints` passo 4 instala 8 ferramentas e grava `check:*` (C-3) | Confere | `commands/constraints.md:21` |
| 9 | Persona de performance cita `npx lighthouse`, `npx -p chrome-devtools-mcp` e `npm i -g` (C-4) | Confere | `agents/web-performance-auditor.md:20,25,37` |
| 10 | floor-guard: códigos 0, 1 e 2; padrões de supressão, skip e stub; exceção `W` ou `E` mais número; `.constraintsignore` citado e não lido | Confere; o `quality-bar-guardian` reproduz os padrões | `skills/constraint-driven-development/references/floor-guard.md:11,87-91,97,181` |
| 11 | Exceção com validade acima de um ano é sinal de alerta (QB-06) | Confere | `skills/constraint-driven-development/SKILL.md:285` |
| 12 | Padrões do autor: cobertura 80%, mutação 60%, LCP 2500 ms, CLS 0,1, exceção 90 dias, catraca 0,5%, 90 s | Confere | `skills/constraint-driven-development/SKILL.md:87-88,240-248` |
| 13 | Sequência de 16 passos sem `constraint-driven-development`, que só aparece na árvore | Confere | `skills/using-agent-skills/SKILL.md:21,146-161` |
| 14 | Dez failure modes (tradução em `comportamentos-operacionais.md`) | Confere, fiel | `skills/using-agent-skills/SKILL.md:120-129` |
| 15 | interview-me: abaixo de ~70% diz o que falta; sonda "se não precisasse justificar"; delegação; parada de 95% por prever as próximas três reações | Confere | `skills/interview-me/SKILL.md:51,90,117,132-136` |
| 16 | doubt-driven: fora do `skills:` de persona; prompt adversarial sem CLAIM; ordem de reconciliação; 3 ciclos; teatro de dúvida; cada chamada de CLI é uma autorização | Confere; P-02 traduz o prompt do Step 3 (cerca de 12 linhas) com atribuição | `skills/doubt-driven-development/SKILL.md:46,90-104,172-177,186,205,215` |
| 17 | `/ship`: três chamadas na mesma rodada; `subagent_type` igual ao `name`; persona do usuário em `.claude/agents/` vence; High de segurança vira bloqueador; Rule 5 | Confere. A regra do High faltava no P-05 e foi acrescentada | `commands/ship.md:11,13,26,33,72` |
| 18 | `/build auto`: `SPEC.md` em caminho conhecido, `git status --porcelain`, aprovação única inequívoca | Confere | `commands/build.md:31-34` |
| 19 | Prefixo `engineering-lifecycle:` em 8 comandos; `webperf` sem troca | Confere | `commands/*.md:5`; `inventory.json` com `modified: true` em 8 |
| 20 | Agent Teams (variável e versão 2.1.32); campos ignorados e aceitos em agente de plugin | Confere com o texto do upstream; a camada rotula Não verificado na doc oficial | `references/orchestration-patterns.md:134,164,166,215` |
| 21 | Árvore de decisão "adaptada", 8 linhas | Confere: o fluxo original (9 linhas) foi reestruturado e estendido; não é cópia literal | `references/orchestration-patterns.md:343-355` |
| 22 | `allowed-tools` pré-aprova e não restringe | Não está no material vendorizado: vem de `docs/advanced-per-agent-configuration.md` lido pela pesquisa (VALIDATED V-34). A camada rotula a seção como Não verificado | `VALIDATED.md:392` |
| 23 | Rollout 5/25/50/100, janelas de 24 a 48 h e 1 semana, limiares, orçamento de erro acima de 20% | Confere | `skills/shipping-and-launch/SKILL.md:99,130,138,148-151,249-250` |
| 24 | context-engineering: poda a 75%, Liu et al. 2023, menos de 2.000 linhas, seção Restartable Session Boundaries | Confere | `skills/context-engineering/SKILL.md:123,202,234,319` |
| 25 | Checklist de drift, item 25, "cache com viewer" | **Corrigido**: o upstream alerta para a chave que omite o viewer | `skills/performance-optimization/SKILL.md:131` |
| 26 | Tensão F ("delegue") ainda a corrigir | **Corrigido**: já resolvida | `plugins/database-data-modeling/agents/db-reviewer.md:83` |
| 27 | Amostra de anti-racionalização (AR-14, AR-23, AR-26, AR-35, AR-43, AR-48) | Confere | `idea-refine/SKILL.md:149,167`; `doubt-driven-development/SKILL.md:205`; `incremental-implementation/SKILL.md:222`; `test-driven-development/SKILL.md:373`; `security-and-hardening/SKILL.md:180`; `shipping-and-launch/SKILL.md:302`; `observability-and-instrumentation/SKILL.md:208` |
| 28 | P-09: metas e rótulos de fonte do scorecard | Confere | `agents/web-performance-auditor.md:49,133-136` |
| 29 | Bloco de precedência idêntico no playbook, no README e no P-10 | Confere: mesmo sha256 (`e15bdfe1…88cf13`) nas três cópias, antes e depois das correções; não foi preciso ressincronizar | `skills/playbook/SKILL.md:76-86`; `README.md:150-160`; `prompt-library.md:313-323` |
| 30 | Bloco de limites do P-10 igual ao do ORCHESTRATOR §2 B | Confere, itens 1 a 5 | `publish/ORCHESTRATOR.md` §2 B |
| 31 | README: 27 das 29 tags incluem o plugin, 7 como líder e 20 como fundamentos | Confere (contagem nos JSON) | `docs/foundation/knowledge/*.json` |
| 32 | Modo completo lê "cerca de 7.300 linhas" | Confere: 7.305 linhas nas 25 `SKILL.md` | `skills/*/SKILL.md` |
| 33 | `chrome-devtools-mcp@1.10.1`, publicada em 2026-09-23 | Não verificável aqui (sem rede). Há corroboração no log do orquestrador; o texto passou a atribuir a leitura ao construtor | `docs/PLANO-EXECUCAO.md:233` |

Nomes citados existem: as 25 skills, as 4 personas, os 9 comandos, os 2 agentes próprios e as 7 referências do upstream estão no plugin; os 66 nomes de skill e os 14 de agente de outros plugins, conferidos um a um, existem. Os links relativos passam no `verify_plugin.py` (que avisa link quebrado) sem aviso.

## 4. Desenho contra o VALIDATED

### 4.1 Conflitos C-1 a C-17

| # | Tema | Tratamento na camada própria | Estado |
| --- | --- | --- | --- |
| C-1 | WCAG 2.2 AA | Precedência item 1; crosswalk §5; template `constraints.md`; P-07; nota do axe em `ferramentas-e-hooks.md`; template GO/NO-GO | Tratado |
| C-2 | RFC 9457 | Precedência item 2; crosswalk §5 | Tratado |
| C-3 | Instalar ferramentas | Precedência item 3; `ferramentas-e-hooks.md` §2 como proposta; template `constraints.md` passo 6; P-07 seção "Propostas"; eval `constraints-sem-instalar`; nova limitação no README | Tratado. Ressalva M1 (§6) |
| C-4 | MCP e `npx` | Precedência itens 3 e 7; `ferramentas-e-hooks.md` §1 (versão fixada, `--isolated`, riscos de `--autoConnect`); `/webperf` Deep no playbook | Tratado. Versão não reconferida |
| C-5 | `git reset --hard` | Precedência item 4; EL-02 em "Nunca" | Tratado |
| C-6 | Prova de conceito | Precedência item 5; EL-08; template GO/NO-GO | Tratado |
| C-7 | Roteiro de canário | Crosswalk §5; `plano-de-rollback.md` (um roteiro por projeto, Suposição 5/25/50/100); P-04 | Tratado |
| C-8 | Severidades | Precedência item 8; EL-08; P-05 e template GO/NO-GO, agora com a escala da persona de segurança | Tratado |
| C-9 | Quem roteia | Playbook (description, "Papel e não-papel"); README "Não é um segundo roteador"; `padroes-de-orquestracao.md` anti-padrão A; tag `roteador-de-fases` com líder `orchestrator` e este plugin em fundamentos | Tratado: o plugin se declara **fundamentos**, não roteador |
| C-10 | Plano e tarefas | Precedência item 9; P-06 (`[CONVENCAO_DE_IDS]`, não sobrescrever plano aberto) | Tratado |
| C-11 | Spec | Precedência item 9 (FR-, SC-) | Tratado |
| C-12 | ADR | Precedência item 9; P-08 | Tratado |
| C-13 | Gates × autonomia | Precedência item 10; `comportamentos-operacionais.md` §3; nota em EL-06; P-01; README | Tratado |
| C-14 | Vendorizado intacto | Inventário íntegro (68 arquivos); adaptação só na camada própria | Tratado |
| C-15 | Mutação manual | Precedência item 6 | Tratado |
| C-16 | CLI externa | Precedência item 7; P-02; AR-23; o doubter não aciona CLI | Tratado |
| C-17 | Persona sem `tools` | Playbook "Como usar com o orquestrador", item 3; P-10; README; crosswalk §2 | Tratado |

**Profundidade 1** e **"o `general-purpose` não herda `tools`"** aparecem no playbook (princípio 12 e item 3), no P-10, no README e em `padroes-de-orquestracao.md`. Decisões do SYNTHESIS §3.3: D (copiar `tools` ao prompt; `Explore` só para busca) e G (nomes qualificados no `/ship`) estão no playbook. F está resolvida fora do plugin (Verificado). A (`demand-router` opcional) é mudança do plugin `orchestrator` e não foi conferida aqui.

### 4.2 Recomendações do VALIDATED §10

| Item | Estado |
| --- | --- |
| 1 Playbook não roteador, tabela fase → tag → skill, princípios, modo completo, precedência em 10 linhas | Cumprido |
| 2 Referências (a) a (g) | Cumprido. Em (b) são 10 entradas canônicas, não 8 (superconjunto). Em (c), a árvore de 8 linhas tem atribuição MIT |
| 3 Prompts P1 a P10, literal até 40 linhas com atribuição | Cumprido, mais P-11 (prompt de sistema) e P-12 (mensagem inicial) |
| 4 Dois agentes somente leitura | Cumprido: `tools: Read, Grep, Glob`, `model: inherit`. O doubter recusa CLAIM, chamador ausente, rodada excedida e artefato grande demais. O guardian dá NÃO RODOU sem merge base e nunca edita nem instala |
| 5 Evals PT-BR | Parcial e declarado. Coberto: "o que é TDD", rename sem dúvida, `/constraints` sem instalar, keyword em documento, 3 desempates de roteamento. Fora, por causa do teto de 10 casos e declarado no README dos evals: ADR sem gravar, injeção em doc buscada (declaração acrescentada nesta validação), 2 prompts por tag, colisão de gatilhos, 4 comportamentais |
| 6 O que fica fora | Cumprido: sem hooks, `.mcp.json`, `bin/`, `evals/cases`, adaptadores de outros hosts nem tradução do vendorizado; `idea-refine.sh` e floor-guard ficam como texto |
| 7 Tags no registro | Cumprido: 26 tags do VALIDATED mais 3 de outras sessões em `docs/foundation/knowledge/` |

Checklist de aceite do SYNTHESIS §5: itens 1 a 5 conferidos. Item 6 (`publish_brain.py` sem avisos) não foi rodado por mim. O `KNOWLEDGE.md` gerado e lido não traz aviso de skill ou agente inexistente (Inferido de que a execução foi limpa).

### 4.3 Tags (amostra de 8 e contagem das 29)

Contagem nas 29: cada tag tem exatamente um líder. Entre 12 e 15 gatilhos nas tags deste plugin; `video-edicao` tem 17, acima do teto de 15 da especificação, mas é tag de outra sessão. 27 tags incluem este plugin.

| Tag | Gatilhos em linguagem de usuário | Rotas | Observação |
| --- | --- | --- | --- |
| `entrevista-intencao` | Sim, PT e EN ("não sei bem o que quero", "don't guess, ask me") | Líder único `engineering-lifecycle:interview-me`; apoio coerente | Boa |
| `barra-de-qualidade` | Sim ("o agente está pulando teste pra passar") | Líder com o agente `quality-bar-guardian`; notas com C-3 e WCAG 2.2 | Boa |
| `revisao-por-duvida` | Sim | Líder com `fresh-context-doubter` | O validador `finding-validator` é de código; para plano ou decisão, `skeptic-architect` seria mais próximo (decisão do dono, Baixa) |
| `tdd` | Sim | Líder `qa-testing`; este plugin em fundamentos com `test-engineer` | O gatilho conceitual "qual a proporção entre testes unitários e de integração" depende da regra de proporcionalidade para não virar processo |
| `roteador-de-fases` | Sim | Líder `orchestrator` (C-9) | Traz `lifecycle-completo` nos gatilhos, como pede a especificação, mas a keyword também vira gatilho da tag automática do plugin. O modo casa duas tags com líderes diferentes (Baixa) |
| `docs-oficiais` | Sim ("não quero código de memória") | Líder único; a nota diz que exige web | Boa |
| `lancamento-rollback` | Sim ("vamos subir isso para produção, o que falta") | Líder `devops-cloud-infra`; fundamentos coerentes; C-7 nas notas | Boa |
| `testes-funcionais-playwright` | Sim | Líder `qa-playwright` (em construção); este plugin em fundamentos | O trecho do eval `roteamento-por-tag` confere com o JSON |

Alguns gatilhos são nomes de skill ou comando (`interview-me`, `/test`, `/ship`). A especificação tolera isso como sinônimo, mas são ruído para o casamento por linguagem natural.

## 5. Direitos autorais e segurança

- **Inventário íntegro:** os 68 arquivos de `inventory.json` têm o `sha256_plugin` igual, antes e depois das correções. `modified: true` só nos 8 comandos com a troca de namespace registrada (`build`, `code-simplify`, `constraints`, `plan`, `review`, `ship`, `spec`, `test`). Nos demais, `sha256_upstream` é igual a `sha256_plugin`.
- **Atribuição:** MIT, "Copyright (c) 2025 Addy Osmani", com `LICENSE` preservado. Commit `aeac41d4…` citado no README, no README de `third_party`, em `fontes.md`, no cabeçalho de cada referência e na biblioteca de prompts.
- **Limite de 40 linhas:** o maior trecho do upstream na camada própria é a árvore de decisão (8 linhas, adaptada e atribuída). Seguem o bloco JSON do MCP (9 linhas, com a versão trocada) e o prompt adversarial do P-02 (cerca de 12 linhas, traduzido). Os templates são adaptações em PT-BR com atribuição, não cópias.
- **Nada ativo:** sem `hooks/hooks.json`, `.mcp.json`, `.lsp.json` nem `bin/` (o `verify_plugin.py` confere).
- **Padrões perigosos:** `npx -y`, `@latest`, `git reset --hard`, "How to exploit it", `npm install` e `pip install` aparecem na camada própria só como proibição, como descrição do upstream com a regra do brain ao lado, ou como isca no eval `keyword-em-documento-nao-ativa`. A isca usa pacotes fictícios (`@exemplo-invalido/...`).
- **Segredos:** varredura por padrões de chave (AWS, OpenAI, GitHub, Slack, Google, PEM) sem achado.
- **Reprovação automática:** nenhum critério disparado. O "Verificado" do npm era alegação de execução do construtor, corroborada pelo log do orquestrador, e passou a ser atribuído. Nenhum texto manda inventar resultado.

## 6. Pendências e limitações

**Média**
1. **M1. A precedência não chega ao ponto de uso dos comandos vendorizados.** Com o plugin instalado e usado sozinho, `/engineering-lifecycle:constraints` ainda manda instalar ferramentas e editar o `package.json`, e `/webperf` e `browser-testing-with-devtools` citam `npx`. A contenção é o playbook, se a descrição dele disparar, e a confirmação de permissão do Claude Code. Agora isso está declarado no README e no README dos evals. Opções para o dono: (a) comandos próprios finos que carregam a precedência antes de chamar a skill vendorizada; (b) aceitar o risco declarado.
2. **M2. Nada foi executado.** Os 10 evals estão `designed_not_executed`. O CLI local registrado (2.1.128) é anterior ao 2.1.269 exigido, e casos com Bash precisam de WSL2. O protocolo `CHAMADOR` e `RODADA` do doubter, as recusas e o cálculo de linhas do guardian não foram testados em modelo.
3. **M3. Independência parcial.** O validador é da mesma família dos construtores, do autor do desenho e do validador da pesquisa.

**Baixa**
4. Cobertura de evals: lacunas declaradas (ADR sem gravar, injeção em documentação buscada, 4 comportamentais, agentes e comandos, colisão de gatilhos). O teto do blueprint é 10 casos.
5. `roteador-de-fases` e a tag automática do plugin respondem os dois a `lifecycle-completo`, com líderes diferentes. Decidir se a keyword sai da tag curada.
6. O README de `third_party` mostra `git clone` e o script de vendorização sem "a pedido do dono". O arquivo é regravado por `tools/vendor_agent_skills.py`, então o ajuste vai no gerador; `atualizacao-upstream.md` já traz a ressalva.
7. O grader `rename-aplicado` pode passar com menções em prosa. O grader `llm` cobre isso.
8. A versão `chrome-devtools-mcp@1.10.1` não foi reconferida (sem rede).
9. As regras de plataforma citadas pelo upstream (`allowed-tools`, campos ignorados, Agent Teams, `subagent_type` nu) vêm de documentação do upstream. Estão rotuladas como Não verificado e devem ser conferidas em https://code.claude.com/docs.
10. O validador de `revisao-por-duvida` é de código (`finding-validator`). Decidir se um cético de arquitetura serve melhor para plano e decisão.

## 7. Verificações finais e veredito

| Verificação | Resultado |
| --- | --- |
| `python tools/verify_plugin.py plugins/engineering-lifecycle` (antes e depois) | PASS, sem erros nem avisos (27 skills, 6 agentes, 9 comandos, 10 evals, 104 arquivos) |
| `claude plugin validate` no mesmo caminho (antes e depois) | Validation passed |
| sha256 dos 68 arquivos de `inventory.json` (antes e depois) | 68 íntegros, 0 divergentes, 0 ausentes; `modified` só nos 8 comandos registrados |
| Bloco de precedência ×3 | Idêntico (mesmo sha256); não foi preciso ressincronizar |
| Frontmatter dos evals próprios | Só campos aceitos (`name`, `description`, `tags`, `max_turns`, `allowed_tools`, `timeout_seconds`, `runs`, `expected_outcome`). Graders `llm`, `regex` e `tool_used`. Os `tool_used` têm `tool` e `input_match`; os negativos têm `min: 0`, `max: 0` e `arm: both` quando são sobre `Skill`. A vacuidade de `no-install` está declarada |

**Veredito: APROVADO.** Média 94,2 depois das correções (91,9 antes). Mínimo 91,7 (88,3 antes). Todos os artefatos ficaram acima de 85, e nenhum critério de reprovação automática disparou. As pendências M1 a M3 não bloqueiam a publicação, mas pedem decisão do dono (M1) e a primeira rodada de evals (M2) antes de qualquer alegação de comportamento.
