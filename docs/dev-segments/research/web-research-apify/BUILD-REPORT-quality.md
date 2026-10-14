# BUILD-REPORT de qualidade: web-research-apify

Data: 2026-10-14 · Plugin: `plugins/web-research-apify` v0.1.0 · Papel: validador independente de prompt e conteúdo técnico (e da integração Apify na fábrica).
Independência: o validador (claude-opus-5-5) é da mesma família de modelos dos construtores (Sonnet) e do crítico (Opus). As notas D1 a D12 são estimativas de leitura pela rubrica `prompt-quality-rubric.md`, não medição, e não equivalem a validação externa.

## 1. Método

- Li a rubrica, o blueprint (qualidade mínima), o estilo da casa, a "Revisão do crítico" da `SYNTHESIS.md` e o formato deste relatório em `automation-integrations`.
- Li inteiros os 9 `SKILL.md`, os 3 agentes, o README e os graders determinísticos dos 10 evals (um caso completo com `criteria.md`). Na biblioteca de prompts li o índice e as entradas que gastam ou delegam (P-06, P-07, P-10, P-14, P-21, P-22). Nas referências de afirmação técnica de risco li `catalogo-de-tools.md` e `custo-e-orcamento.md` inteiros, e amostrei `conexao-e-perfis.md` (perfis, receitas, permissões) e `seguranca-e-privacidade.md`.
- Conferi contra `VALIDATED.md` (V-02 a V-06, V-20 a V-25, catálogo verificado, tabela de Actors) os nomes de tools, o perfil `?tools=actors,docs` (9 tools), a auto-injeção, `callOptions` (`maxTotalChargeUsd` só PPE, `timeout` 0 = sem limite, `maxItems` legado), `waitSecs` 0 a 45, os preços e mínimos datados e o 404 de `curious_coder/youtube-transcript-scraper`.
- Coerência por script: todos os IDs citados (V-01..V-34, P-01..P-22, WR-01..15, PAD-01..08, AP-01..16, H-01..H-15 com H-02b e H-05b, S0..S13 com S10b, R-A..R-F) existem na definição. Todo caminho `${CLAUDE_PLUGIN_ROOT}/...` e todo link relativo do `playbook` resolve. As skills e agentes citados em outros plugins (tag e fronteiras) existem.
- Integração: li o bloco Apify inteiro de `tools/workflows/research-v2.js`, METODO §10, os trechos Apify de `research-file-format.md` e de `publish/ORCHESTRATOR.md` e a tag `pesquisa-web-apify.json`.
- Reprovação automática: nada encontrado. Nenhum fluxo autoriza gasto, re-run, `claude mcp add`, push ou envio sem confirmação (`conectar-apify` espera o "sim" deste chat; `pesquisa-com-orcamento` tem `disable-model-invocation: true` e um portão de orçamento em US$). Token nunca é pedido no chat nem na URL (`?token=` é antipadrão AP-05). Conteúdo raspado é tratado como dado em todas as superfícies. O único "segredo" é o fixture `apify_api_FICTICIO0000`. Frontmatter: as `description` estão entre aspas e `name` = pasta.

## 2. Notas por componente (D1 a D12, média x 20)

| Arquivo | Antes | Depois | Correções |
| --- | --- | --- | --- |
| `skills/playbook/SKILL.md` | 87 | 89 | Gotcha de `waitSecs` reescrito: dizia que passar de 30 "arrisca o teto de 60 s". O certo é que o servidor aceita até 45 por causa desse teto, e 30 é margem do plugin. Gotcha de `get-dataset-items` ("só existe se…") restrito aos perfis de pesquisa. 149 linhas |
| `skills/prompts/SKILL.md` + `prompt-library.md` | 86 | 88 | P-21 não exigia `timeout` nem o teto por run em `callOptions` (acrescentados). A fonte "P-18 da fábrica" se confundia com o P-18 da biblioteca (desambiguada). Gatilhos PT/EN, variáveis e exemplo de preenchimento estão adequados |
| `skills/pesquisa-com-orcamento/SKILL.md` | 89 | 90 | `waitSecs` corrigido como acima. `disable-model-invocation: true` presente; portão de orçamento, um `call-actor`, exceção estreita para erro sem `runId`, conta do exemplo conferida (0,12 / teto 0,15 / saldo 0,15) |
| `skills/conectar-apify/SKILL.md` | 87 | 89 | Para evitar disputa de gatilho com `diagnosticar-apify`, a `description` ganhou o ponteiro "para só checar o que já está carregado, use diagnosticar-apify". As receitas estão rotuladas NÃO ATIVAS e o "sim" vem antes de qualquer comando |
| `skills/diagnosticar-apify/SKILL.md` | 88 | 90 | Ponteiro recíproco para `conectar-apify` na `description`; gotcha de `get-dataset-items` corrigido |
| `skills/escolher-actor/SKILL.md` | 89 | 89 | Sem alteração. Confirma existência, tier GOLD e limite de volume obrigatório; restringe o WebFetch pré-aprovado a `api.apify.com` e às docs |
| `skills/dataset-para-itens/SKILL.md` | 90 | 90 | Sem alteração. Sem Write, Edit nem WebFetch pré-aprovados, triagem de injeção item a item, contagens coerentes |
| `skills/auditoria-de-custo/SKILL.md` | 89 | 89 | Sem alteração. As contas do exemplo conferem (tetos 0,35 ≤ 0,40, saldo 0,05) |
| `skills/consultar-docs-apify/SKILL.md` | 88 | 88 | Sem alteração |
| `agents/apify-researcher.md` | 85 | 88 | O passo 7 mandava ler o log "se a tool existir", mas `get-actor-run-log` não está no `tools` do agente: agora diz para não procurá-lo. `waitSecs` em `get-actor-run` foi marcado como Inferido. A orientação do crítico (só a lista de Actors ⇒ `model: sonnet`) não estava no agente e foi acrescentada. A allowlist `tools` é coerente com P2 sem `abort-actor-run`/`get-key-value-store-record` e com o modo gratuito |
| `agents/apify-source-verifier.md` | 89 | 89 | Sem alteração; somente leitura, sem tools da Apify |
| `agents/apify-cost-auditor.md` | 86 | 89 | Duas divergências com a skill: R6 não exigia `callOptions.timeout` ≠ 0, e "run sem plano" não estava na severidade Alta. Ambas alinhadas à skill |
| `evals/` (10 casos + README) | 88 | 89 | O README citava IDs antigos (E-02, E-05) e `seguranca-e-privacidade.md` citava E-04 e E-09: trocados pelos nomes das pastas. "tres" virou "três". Os graders estão bem formados (`type`, `tool`, `input_match`, `min`/`max`, `arm: both` no negativo), com 2 negativos e efeitos observáveis |

Média antes: 87,8 · Média depois: 89,0 · Mínimo depois: 88 (`prompts`, `consultar-docs-apify`, `apify-researcher`) · Todos ≥ 80 antes e depois.
Integração na fábrica (não pontuada no blueprint): bloco Apify do `research-v2.js` 86 → 89; METODO §10, `research-file-format.md`, ORCHESTRATOR e tag sem alteração (corretos e enxutos).

## 3. Correções técnicas de substância

1. **`maxResults` como antipadrão (AP-02 e gotcha de `custo-e-orcamento.md`).** O texto dizia que `maxResults` dentro do `input` "não é teto", e isso contradiz a seção 5 da mesma referência e o V-05: `maxResults` é o limite de volume legítimo do crawler e do `rag-web-browser`. O que não limita a run, quando posto no `input`, são os campos de `callOptions` (`maxTotalChargeUsd`, `timeout`, `memory`). Os dois trechos foram corrigidos. Um Haiku que seguisse a versão antiga poderia tirar o limite de volume do `input`.
2. **`waitSecs` (playbook, `checklist-completo.md`, `pesquisa-com-orcamento`).** V-05 e V-06 dizem que o servidor aceita 0 a 45, e o limite de 45 existe justamente para caber no teto de 60 s de vários clientes. "Acima de 30 arrisca o teto" era uma inferência sem base; ≤ 30 continua como margem do plugin.
3. **`get-dataset-items` "só existe se…" (4 arquivos).** Também carrega pela categoria `storage` ou pelo nome em `tools=` (catálogo verificado). A frase agora vale para os perfis de pesquisa, onde é verdadeira.
4. **`research-v2.js` (só o bloco Apify, regras 2 e 3 do preâmbulo).** Para o pesquisador Haiku, o texto agora diz `maxTotalChargeUsd` entre o mínimo do Actor e `US$ ${AP.maxUsdPerRun}`, e `timeout` nunca 0. "Não repita call-actor" deixava ambíguo se uma segunda tentativa com outro input contava como repetição: agora conta ("mesmo Actor e objetivo, mesmo com outro input"). `get-actor-run` fica limitado a 3 vezes. A edição está dentro de `apifyPreamble()`, que só é chamada com `args.apify` válido, então os prompts sem Apify não mudam. `node --check` passa, e um teste do template com `AP` fictício interpola o valor.
5. **Agentes alinhados às skills:** log fora do `tools` do `apify-researcher`; R6 e severidade do `apify-cost-auditor`.

## 4. Pendências

- **Só o smoke test com o MCP conectado confirma:** nomes e prefixo reais das tools e o perfil P2 com 9 tools (H-01, H-02); recusa de teto abaixo de `minimalMaxTotalChargeUsd` (H-03); o teto PPE cortando a run (H-04); custo invisível e `apify-api-read` (H-05, H-05b); `deny` inofensivo para tool não carregada (H-07); `ask` em modo não interativo (H-08); expansão de `${APIFY_MCP_TOKEN}` (H-09); agentes do Workflow enxergando as tools MCP (H-15). Também os argumentos marcados como Inferidos: ID em `get-dataset-items` e `get-actor-run`, formato de `fields` e de `output`, e `waitSecs` em `get-actor-run`.
- **Evals:** `designed_not_executed`. O CLI local (2.1.128) é anterior ao exigido (2.1.269). Graders sobre `mcp__apify__call-actor`, `Bash`, `Write` e `Edit` passam por vacuidade sem o MCP e sem `--allow-tools`.
- **Risco residual aceito (decisão do usuário):** o `apify-researcher` combina Read, conteúdo de terceiros e WebFetch, uma trifecta parcial. A mitigação é só textual (abrir apenas o permalink do item) mais o prompt de permissão por domínio. Se o arquivo de saída já vier no prompt, dá para remover `Read`/`Grep`/`Glob` do agente.
- `model: haiku` é fixo no agente; a troca para Sonnet com lista aberta depende de quem delega.
- `conectar-apify` não pré-aprova `ToolSearch`, embora o passo 1 use o roteiro de diagnóstico. É inofensivo (ToolSearch não pede permissão); mantido.
- Do crítico, ainda abertas e fora deste escopo: rodar `tools/publish_brain.py` e conferir avisos de agente no `KNOWLEDGE.md` (item 7). A fusão opcional `diagnosticar-apify` → `conectar-apify` (item 8) não é necessária: os ponteiros recíprocos resolvem a disputa por leitura, e os evals confirmarão.
- `graphify update .` não rodou: não existe `graphify-out/` neste projeto nem na pasta do usuário.

Resultados das ferramentas (2026-10-14, depois das correções):

- `node --check tools\workflows\research-v2.js`: OK.
- `python tools\verify_plugin.py plugins\web-research-apify`: **PASS** (9 skills, 3 agentes, 10 evals, 83 arquivos).
- `claude plugin validate …\plugins\web-research-apify`: **Validation passed**.

## 5. Veredito

**APROVADO.** Todos os componentes ficaram com nota ≥ 80 (média 89,0, mínimo 88), nenhum critério de reprovação automática apareceu, e `verify_plugin.py` e `claude plugin validate` passam. O comportamento em runtime continua Suposição até o smoke test.
