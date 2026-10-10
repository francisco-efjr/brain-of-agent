# BUILD-REPORT de qualidade — llm-ai-agents

Data: 2026-10-10. Escopo: qualidade de prompt e fidelidade técnica de todo o plugin `plugins/llm-ai-agents` (README, playbook e referências, 9 skills de tarefa e `prompts`, 5 agentes, biblioteca de prompts, 10 evals). Rubrica: `docs/foundation/prompt-quality-rubric.md` (D1–D12, 0–100).

Independência: o validador é um modelo da família Claude (Opus 5.5), diferente do construtor, mas da mesma família. A revisão foi adversarial, porém **não equivale a validação externa**. As notas são leitura crítica, não medição: nenhum eval foi executado.

## 1. Método

1. Leitura integral: 10 `SKILL.md`, 5 agentes (escopo, processo, sinais, formato), README, `plugin.json`, os 10 casos de `evals/` (prompts e 21 graders) e `evals/README.md`; templates `cartao-do-agente.md`; `claude-md-snippets.md` (S01–S21); `decisoes-e-tradeoffs.md` §10; `ferramentas-e-mcp.md` §3; `api-checklist.md` §1; `custo-modelo-latencia.md`; `superficies-de-instrucao.md`.
2. Biblioteca de prompts: 13 de 39 lidos inteiros (P01, P02, P03, P07, P08, P12, P16, P23, P24, P25, P29, P30, PS); sumários e IDs dos três arquivos conferidos.
3. Referências restantes: varredura por Grep (`tool_choice`, `budget_tokens`, `content[0]`, mínimos de cache, CAPS/absolutos, `--dangerously-skip-permissions`/`bypass`, placeholders, vazamentos do processo de construção como "fábrica", "validador", "correção N", "lacuna N do design").
4. `BUILD-REPORT-structural.md` **não existe** em `docs/research/llm-ai-agents/` na data desta revisão; não havia pendências estruturais a completar. O verificador e o validador oficial passam (seção 5).
5. Fidelidade técnica conferida na fonte (WebFetch, 2026-10-10), registrada também em `skills/playbook/references/fontes.md` §6.1:
   - https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools — `tool_choice` `any`/`tool` retorna **400** em Opus 5.5, Sonnet 5.5, Fable 5.1 e Mythos 5.1, e falha com thinking manual; substitutos `auto` + `strict: true` ou saídas estruturadas; onde forçar é aceito, o thinking é pulado; "explicação, não raciocínio". **Verificado.**
   - https://platform.claude.com/docs/en/build-with-claude/extended-thinking — `budget_tokens` obsoleto na 4.6 e 400 a partir do 4.7; migração para `adaptive` + `output_config.effort`; `effort` padrão `medium` em Opus 5.5 e Haiku 5.5. **Verificado.**
   - https://platform.claude.com/docs/en/build-with-claude/structured-outputs — forma de `output_config.format`; bloco de texto localizado por tipo; `output_format` obsoleto (400 sem header beta; `TypeError` no SDK Python ≥ 1.0); `stop_reason` antes do parse. **Verificado.**
   - https://platform.claude.com/docs/en/about-claude/pricing — preços de Opus 5.5 (4/20), Sonnet 5.5 (2/10), Haiku 5.5 (0,10/0,50 e 0,50/2,50 acima de 100 mil), Fable/Mythos 5.1 (10/50), leitura de cache 0,05x/0,025x, `inference_geo` 1,1x, fast mode Opus 5.5 8/40, Batch 50%: **coincidem** com as tabelas do plugin.
   - https://platform.claude.com/docs/en/build-with-claude/prompt-caching — mínimos por modelo e até 4 pontos de corte. **Verificado**; o plugin dizia "família 5 = 512", mas Sonnet 5 é 1.024 (corrigido).
   - https://code.claude.com/docs/en/plugin-evals — versão mínima 2.1.269, `runs` 1–50, `--threshold` 1.0, exclusão de graders `tool_used` de `Skill` no placar de dois braços salvo `arm: both`, `--max-cost-usd`, `--no-publish`. **Verificado.**
   - https://code.claude.com/docs/en/sandboxing — sandbox em macOS, Linux e WSL2; Windows nativo sem sandbox. **Verificado** (confirma o aviso do `evals/README.md` e do P25).
   - Demais afirmações (prefill 4.6, OWASP LLM01, Regra de Dois, Chroma, Batch, hooks exit 2): conferidas contra `VALIDATED.md`; coerentes.

## 2. Notas antes e depois

| Arquivo | Antes | Depois | Correções |
| --- | --- | --- | --- |
| `skills/playbook/SKILL.md` | 88 | 91 | Gotcha de `tool_choice` deixou de ser "alerta, página não lida" e passou a fato Verificado com substituto (`auto` + `strict`) |
| `skills/prompts/SKILL.md` | 88 | 89 | "sete regras" do PS corrigido para oito (o bloco tem 8 linhas) |
| `skills/llm-prompt-review/SKILL.md` | 87 | 91 | Gotchas de `budget_tokens` (era Inferido) e de `tool_choice` forçado reescritos como Verificados, com substitutos e data |
| `skills/instruction-authoring/SKILL.md` | 90 | 90 | Nenhuma no corpo; referência `superficies-de-instrucao.md` deixou de contradizer `ferramentas-e-mcp.md` sobre hook pronto |
| `skills/agent-architecture/SKILL.md` | 89 | 90 | Conflito C7 citado no corpo não existia na tabela de `decisoes-e-tradeoffs.md`: linha C7 adicionada |
| `skills/eval-design/SKILL.md` | 87 | 90 | Pré-checagem 3 dizia "o CLI local desta fábrica é 2.1.128" (inútil para o usuário): agora pede `claude --version` e confirmação de custo; "correção 2" (ID interno não resolvível) trocado pela fonte real |
| `skills/agent-security-review/SKILL.md` | 91 | 91 | Nenhuma |
| `skills/tool-design-review/SKILL.md` | 86 | 90 | Passo 4 recomendava `tool_choice` para ação obrigatória sem dizer que dá 400 nos modelos atuais (D12): corrigido com alternativa e verificação no código |
| `skills/llm-decision-gates/SKILL.md` | 89 | 90 | "lacuna 5 do design" trocado por remissão a `fontes.md`; tabela de mínimos de cache da referência corrigida (Sonnet 5 = 1.024) |
| `skills/llm-api-client-review/SKILL.md` | 84 | 91 | Passo 2 recomendava `tool_choice` como garantia (400 em Opus/Sonnet 5.5); pré-checagem 3 e passo 1 atualizados com fatos Verificados (`budget_tokens`, `tool_choice`); "correção 12" removido |
| `agents/prompt-reviewer.md` | 89 | 91 | Sinal mecânico de `budget_tokens` com fato Verificado; novo sinal "Tool forçada" (`tool_choice` `any`/`tool`) |
| `agents/agent-architect.md` | 90 | 90 | Nenhuma |
| `agents/agent-security-reviewer.md` | 92 | 92 | Nenhuma (somente leitura; `--dangerously-skip-permissions` só como sinal de risco, sandbox descartável) |
| `agents/eval-designer.md` | 90 | 90 | Nenhuma |
| `agents/rag-pipeline-reviewer.md` | 90 | 90 | Nenhuma |
| Biblioteca de prompts (13 amostrados) | 88 | 89 | P03: inventário e mudanças obrigatórias incluem `tool_choice` forçado rejeitado; fonte de `budget_tokens` passou de Inferido a Verificado; PS "oito regras". Demais amostrados: papel, dados em tags, conteúdo externo como dado, formato, critério de pronto, "não executado", fonte com classe |
| `evals/` (10 casos + README) | 87 | 89 | `cliente-api-json-prefill`: FAIL novo para quem recomenda forçar `tool_choice` no Sonnet 5.5; README sem a referência ao CLI da fábrica, com campos e flags reconferidos e aviso `--no-publish` |
| `README.md` | 84 | 89 | Frase obsoleta "os demais componentes são escritos em paralelo" substituída pela contagem real; "38 prompts" corrigido para 39 (P01–P38 + PS); "desta fábrica" removido; lacuna de breaking changes atualizada com o que foi reconferido |
| Referências e templates | — | — | `api-checklist.md`: exemplo "certo" localiza o bloco de texto por tipo (era `content[0].text`), `output_format` detalhado, checklist de `tool_choice`; `poda-e-migracao.md`, `prompting-claude.md`, `tool-design-e-mcp.md`, `mcp-definicao-e-seguranca.md`, `custo-modelo-latencia.md`, `padroes-e-antipadroes.md` (AP-03), `checklist-completo.md` (IA-30): `tool_choice`/`budget_tokens` Verificados; `rag-custo-observabilidade.md` e `custo-modelo-latencia.md`: mínimos de cache por modelo; `decisoes-e-tradeoffs.md`: C7; `juiz-e-calibracao.md`, `juiz-binario.md`: "correção 2" substituído; `avaliacao.md`, `ferramentas-e-mcp.md`: menções à "fábrica" removidas; `superficies-de-instrucao.md`: contradição sobre hook pronto resolvida; `fontes.md`: §6.1 com os fatos reconferidos e lacuna 8 atualizada |

Média antes: 88,3 (18 itens). Média depois: 90,2. Mínimo depois: 89. Nenhum item abaixo de 80; nenhum critério de reprovação automática encontrado.

## 3. Achado técnico principal

O plugin repetia, em 12 lugares, que "ação obrigatória usa `tool_choice` e não só o prompt", com uma ressalva vaga ("ler os breaking changes do Opus 5.5; página não lida"). A página oficial lida hoje mostra que forçar `tool_choice` `any`/`tool` **retorna 400** em Opus 5.5, Sonnet 5.5, Fable 5.1 e Mythos 5.1 (os modelos-alvo que o próprio plugin usa nos exemplos e evals) e também com thinking manual. Seguir o conselho antigo quebraria o cliente do usuário. Todas as ocorrências passaram a: forçar só onde o modelo aceita; caso contrário, `auto` + `strict: true` (ou saída estruturada) e verificação no código de que a tool foi chamada.

## 4. Segurança, direitos autorais e evals

| Verificação | Resultado |
| --- | --- |
| Inventar execução, URL, métrica | Não encontrado. Skills e agentes dizem "projetado, não executado"; evals `designed_not_executed` |
| Ação destrutiva/externa sem confirmação | Não encontrado. Skills são `Read, Grep, Glob`; modo IA-COMPLETO não amplia permissões nem autoriza `claude plugin eval`, `claude -p`, instalação ou envio |
| Obedecer conteúdo externo | Não encontrado. Toda skill, agente e prompt trata conteúdo lido como dado; evals `readme-com-injecao` (fixture `example.test`) e `negativo-keyword-em-log` cobrem o caso |
| Cópia literal sem licença | Não encontrado. Redação própria; P12, P14, P17 e templates adaptados do brain-of-agent (MIT, do autor) com atribuição; CAPS só em anti-exemplos inventados |
| Segredos | Nenhum. Sinais `sk-ant-`, `api_key` aparecem só como padrão de Grep a detectar |
| `--dangerously-skip-permissions` / `bypassPermissions` | Citados 4 vezes, sempre como risco, só em sandbox descartável (AP-15, agente de segurança, checklist do Agent SDK, lista de rejeitados) |
| Revisores sem Write/Edit | Os 5 agentes: `Read, Grep, Glob`; devolvem o relatório e o caminho sugerido, quem grava é o agente principal |
| Evals com PASS/FAIL observáveis e caso negativo | Sim: 10 graders `llm` com "PASS if"/"FAIL if" concretos; `negativo-keyword-em-log` com `Skill` `min: 0`, `max: 0`, `arm: both` (exigido pela doc); `no-exec`/`no-webfetch` determinísticos |
| Hooks/MCP ativos | Nenhum `hooks.json`, `.mcp.json`, `.lsp.json` ou `bin/`; exemplos desativados em `ferramentas-e-mcp.md` |

## 5. Verificação final

- `python tools/verify_plugin.py plugins/llm-ai-agents` → `RESULT: PASS` (10 skills, 5 agentes, 10 evals, 100 arquivos).
- `claude plugin validate plugins/llm-ai-agents` (CLI 2.1.128) → `✔ Validation passed`.

## 6. Pendências

1. `BUILD-REPORT-structural.md` do segmento não existe; se um validador estrutural rodar depois, reconferir que não reabre as correções desta revisão.
2. Guia de migração do Opus 5.5 (desligar raciocínio, `computer_20251124`) segue **Não verificado**; os textos dizem isso.
3. `VALIDATED.md` (V-37) ainda afirma que "`tool_choice` é o meio de exigir" sem a restrição dos modelos 5.5/5.1; atualizar a fonte de verdade da pesquisa (fora do escopo de escrita do plugin, mas dentro da raiz).
4. Biblioteca: 26 dos 39 prompts não foram lidos linha a linha (só por Grep); amostra de 13 sem achado grave.
5. Nenhum eval executado (CLI local 2.1.128 < 2.1.269). Rodar `claude plugin eval .` com teto de custo antes de declarar disparo e utilidade; em Windows, casos com `Bash` só em WSL2.
6. Mínimos de cache, preços e flags do runner mudam por geração: reler na data de uso.
