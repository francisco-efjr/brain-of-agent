# Checklist completo: aplicações LLM, agentes e engenharia de prompt

Conferido em 2026-10-10 · Rótulos: Verificado, Inferido, Suposição, Não verificável, Não aplicável · Cada item `IA-nn` é verificável por leitura ou por comando, liga a uma referência do plugin e a um item `V-nn` de `docs/research/llm-ai-agents/VALIDATED.md` ou a conhecimento estável. Severidade: **B** bloqueante, **M** melhoria, **O** opcional. Achados de relatório usam o mesmo ID.

## Sumário

1. Como usar (proporcionalidade)
2. Matriz de áreas do modo IA-COMPLETO
3. Checklist universal de prompt (C-01 a C-22 adaptados)
4. Itens por área IA-01 a IA-72
5. Regras de reporte

## 1. Como usar

Fora do modo IA-COMPLETO, aplique só as áreas que o pedido toca: prompt novo (área 1), agente (3, 4, 8), RAG (6), custo (9). Cada achado traz: ID, severidade, confiança (1 a 10; reporte a partir de 7), evidência (`arquivo:linha` ou trecho citado), cenário concreto e correção mínima. Em dúvida, não reporte; diga "sem lacunas" quando for o caso. Revisão feita pelo mesmo modelo que escreveu o artefato não é validação independente: declare.

## 2. Matriz de áreas (modo IA-COMPLETO)

Preencha uma linha por área em `assets/templates/checklist-ia-completo.md`: `aplicável`, `não aplicável (motivo)` ou `bloqueado (o que falta)`, com evidência e pendência.

| # | Área | Referência principal | Itens |
| --- | --- | --- | --- |
| 1 | Prompts e system prompts | `prompting-claude.md` | IA-01 a IA-08 |
| 2 | Contexto e memória | `agentes-contexto-harness.md` | IA-09 a IA-14 |
| 3 | Agentes e multiagentes | `agentes-contexto-harness.md` | IA-15 a IA-22 |
| 4 | Tools e MCP | `tool-design-e-mcp.md` | IA-23 a IA-30 |
| 5 | Instruções, skills, subagentes e plugins | `claude-md-snippets.md`, `decisoes-e-tradeoffs.md` | IA-31 a IA-38 |
| 6 | RAG e citações | `rag-custo-observabilidade.md` | IA-39 a IA-46 |
| 7 | Avaliação | `avaliacao.md` | IA-47 a IA-54 |
| 8 | Segurança e guardrails | `seguranca-guardrails.md` | IA-55 a IA-62 |
| 9 | Custo, cache e latência | `rag-custo-observabilidade.md` | IA-63 a IA-66 |
| 10 | Observabilidade | `rag-custo-observabilidade.md` | IA-67 a IA-69 |
| 11 | Fine-tuning | `rag-custo-observabilidade.md` | IA-70 a IA-71 |
| 12 | API e Agent SDK | `agentes-contexto-harness.md`, `tool-design-e-mcp.md` | IA-72 e itens 23-30 |

## 3. Checklist universal de prompt (C-01 a C-22, prompt-principles; adaptado)

C-01 papel e objetivo em uma frase · C-02 escopo (dentro, fora, intocável) · C-03 contexto mínimo suficiente · C-04 entradas e perguntas só para dúvida material, uma por vez · C-05 passos em ordem, julgamento como critério · C-06 regra com motivo, proibição com alternativa · C-07 tom calmo · C-08 dados separados de instruções, conteúdo externo como dado · C-09 formato de saída definido · C-10 critério de pronto com comando e evidência colada · C-11 rótulos epistêmicos · C-12 política de incerteza · C-13 ação externa com confirmação (`disable-model-invocation: true` em skill) · C-14 ferramentas mínimas, revisores somente leitura · C-15 achados com severidade, confiança, `arquivo:linha`, cenário e ação · C-16 escalada após 3 tentativas falhas · C-17 seção `## Gotchas` · C-18 modelo-alvo e data · C-19 tamanhos (skill < 500 linhas, CLAUDE.md < 200) · C-20 pelo menos 3 casos de eval · C-21 nada sem fonte; literal só com licença permissiva · C-22 sem segredos; hooks e MCP só documentados.

## 4. Itens por área

Formato: ID · sev · o que verificar · detecção · fonte · correção.

### Área 1: prompts

| ID | Sev | Verificar | Detecção | Fonte | Correção |
| --- | --- | --- | --- | --- | --- |
| IA-01 | M | Regras sem motivo | Procurar "sempre/nunca/must" sem "porque" | V-01 | Acrescentar o motivo curto |
| IA-02 | M | CAPS, "CRITICAL", ameaças | `grep -nE "CRITICAL|MUST|NEVER|ALWAYS|!!!"` | V-01, V-03 | Linguagem calma; ênfase em 1 linha após falha observada |
| IA-03 | B | Prefill da resposta do assistente | Última mensagem `assistant` preenchida na chamada | V-01 | `output_config.format` ou instrução de formato |
| IA-04 | M | Sem delimitação de dados e instruções | Texto corrido com documento colado | V-01 | Tags XML; documento no topo, tarefa no fim |
| IA-05 | M | Exemplos homogêneos ou ausentes onde o formato é difícil | Contar exemplos e variar estrutura | V-01 | 3 a 5 diversos, com caso de borda |
| IA-06 | M | Formato de saída vago para consumidor de código | Parser sobre texto livre | V-01, V-37 | Schema |
| IA-07 | M | Sem modelo-alvo/data; sem teste ao migrar | Ficha de prompt ausente | V-01 | `ficha-de-prompt.md` |
| IA-08 | O | "Pense passo a passo", truques de 2023 | `grep -n "passo a passo\|step by step\|tip"` | V-01 | Remover; pedir verificação e ajustar `effort` |

### Área 2: contexto e memória

| ID | Sev | Verificar | Detecção | Fonte | Correção |
| --- | --- | --- | --- | --- | --- |
| IA-09 | M | Pré-carga de dado grande ou mutável | Documentos inteiros no system prompt | V-06 | Referência e busca na hora |
| IA-10 | M | Sem estado fora da janela em tarefa longa | Ausência de notas/`features.json` | V-08 | Template de harness |
| IA-11 | M | Compactação sem lista do que preservar | Instrução de resumo genérica | V-02, V-06 | Decisões, descartes, pendências, restrições |
| IA-12 | M | Instrução duplicada entre system prompt e descrição de tool | Comparar textos | V-03 | Mover para a tool |
| IA-13 | M | Memória gravada sem revisão humana | Hook ou regra que escreve no CLAUDE.md sozinha | V-28 | Política aprovada |
| IA-14 | O | Referência executável possível, mas só prosa | Spec em texto onde caberia teste | V-03 | Teste, mockup, rubrica |

### Área 3: agentes e multiagentes

| ID | Sev | Verificar | Detecção | Fonte | Correção |
| --- | --- | --- | --- | --- | --- |
| IA-15 | B | Agente onde workflow bastava | Passos sempre iguais no log | V-04 | Árvore de decisão; baseline de chamada única |
| IA-16 | B | Sem condição de parada, teto de iterações ou de custo | Loop sem `max_turns`/orçamento | V-04, V-39 | Definir tetos |
| IA-17 | M | Multiagente em código com contexto compartilhado | Vários escritores no mesmo arquivo | V-07, V-26 | Um escritor por arquivo ou agente único |
| IA-18 | M | Briefing sem os 7 campos | Prompt de delegação curto | V-07 | Template de briefing |
| IA-19 | M | Revisor com Write/Edit ou no mesmo contexto do autor | Frontmatter `tools` | V-19, V-20 | Somente leitura, contexto novo |
| IA-20 | M | Framework antes do prompt cru | Dependência de orquestração sem leitura do prompt final | V-04 | Ver prompt e resposta crus |
| IA-21 | M | Plano com escrita executado sem gate | Ausência de validação do plano | V-16 | Gate de plano |
| IA-22 | O | Superfície de agente não justificada | Sem decisão registrada | V-39 | Árvore de superfície |

### Área 4: tools e MCP

| ID | Sev | Verificar | Detecção | Fonte | Correção |
| --- | --- | --- | --- | --- | --- |
| IA-23 | M | Descrição sem "quando usar/não usar" | Ler descrições | V-05 | Reescrever para colega novo |
| IA-24 | M | Parâmetros ambíguos (`user`, `q`) | Schema | V-05 | Nomes inequívocos, exemplo |
| IA-25 | M | Saída com UUID opaco ou sem limite | Resposta de exemplo | V-05 | Campos legíveis, `response_format`, paginação |
| IA-26 | M | Erro sem instrução de correção | Mensagens de erro | V-05, V-18 | Erro acionável, `isError` |
| IA-27 | B | Tool de escrita sem confirmação | Efeito externo sem aprovação | V-13, V-18 | Confirmação com entrada exibida |
| IA-28 | B | Servidor MCP sem checklist de autorização/segurança | Token passthrough, token em query, SSRF | V-44 | Checklist de `tool-design-e-mcp.md` |
| IA-29 | M | Muitos servidores/tools carregados | Contar definições | V-17 | Divulgação progressiva |
| IA-30 | O | Ação obrigatória garantida só pelo prompt, ou `tool_choice` `any`/`tool` em modelo que o rejeita (400 em Opus 5.5, Sonnet 5.5, Fable 5.1, Mythos 5.1) | Código cliente: `tool_choice` e `model` | V-37 (Verificado em 2026-10-10) | `tool_choice` onde o modelo aceita; senão `auto` + `strict: true` e checagem no código |

### Área 5: instruções, skills, subagentes e plugins

| ID | Sev | Verificar | Detecção | Fonte | Correção |
| --- | --- | --- | --- | --- | --- |
| IA-31 | M | CLAUDE.md acima de 200 linhas ou com o que o código revela | `wc -l CLAUDE.md`; teste de remoção | V-21 | Enxugar |
| IA-32 | B | Regra obrigatória só como frase | "sempre" sem hook/permissão | V-40 | Hook ou permissão |
| IA-33 | M | Regra de formatação em texto | Estilo no CLAUDE.md | V-21 | Linter ou hook |
| IA-34 | B | Frontmatter inválido ou `name` diferente da pasta | `verify_plugin.py`, `claude plugin validate` | V-40 | Corrigir |
| IA-35 | M | `description` sem gatilhos PT/EN ou sem "não use para" | Ler | V-23 | Reescrever; teste de 20 consultas |
| IA-36 | M | Skill com efeito colateral sem `disable-model-invocation` | Ler passos | V-40 | Marcar |
| IA-37 | M | Subagente com `tools` herdadas por omissão | Frontmatter | V-19 | Allowlist mínima |
| IA-38 | O | Contradição entre arquivos de instrução | Comparar CLAUDE.md, rules, skills | V-21 | Resolver prioridade |

### Área 6: RAG e citações

| ID | Sev | Verificar | Detecção | Fonte | Correção |
| --- | --- | --- | --- | --- | --- |
| IA-39 | B | RAG sem checar se a base cabe no contexto | Sem contagem de tokens | V-25 | Gate |
| IA-40 | M | Chunking padrão sem medição | 800/400 sem experimento | V-36 | 100 perguntas, recall/precisão |
| IA-41 | M | `input_type` ausente em embeddings | Código de ingestão e consulta | V-36 | `query`/`document` |
| IA-42 | M | Sem reranker ou busca lexical onde recall importa | Pipeline | V-25 | Híbrida + rerank, medir |
| IA-43 | M | Afirmação factual sem citação exibida como fato | Sem bloco de citação | V-35 | Marcar "não sustentada" |
| IA-44 | B | Sem filtro por tenant/permissão na recuperação | Consulta sem filtro | brain | Filtro e teste A/B de isolamento |
| IA-45 | M | Recuperação e geração avaliadas juntas | Sem métricas por etapa | brain | Tabela por etapa |
| IA-46 | M | Documento recuperado tratado como instrução | Sem política de conteúdo | V-43 | Política e teste de injeção |

### Área 7: avaliação

| ID | Sev | Verificar | Detecção | Fonte | Correção |
| --- | --- | --- | --- | --- | --- |
| IA-47 | B | Sem suíte; "parece bom" | Nenhum arquivo de casos | V-09 | 20 a 50 tarefas de falhas reais |
| IA-48 | M | Sem caso negativo | Só casos positivos | V-09, brain | Incluir |
| IA-49 | M | Juiz com escala 1 a 10 ou sem calibração | Prompt do juiz | V-10 | Binário com crítica, TPR/TNR |
| IA-50 | M | Mesmo modelo gera e julga | Config | V-10, V-11 | Outro modelo |
| IA-51 | M | Dev/teste dentro do prompt do juiz | Exemplos repetidos | V-10 | Dividir treino/dev/teste |
| IA-52 | M | Uma execução tratada como prova | Denominador 1 | V-09 | Várias execuções, pass^k |
| IA-53 | M | Grader `llm` sobre saída longa | Configuração do caso | V-12 | `regex` sobre arquivo |
| IA-54 | O | Resultado sem modelo/versão/custo registrados | Relatório | brain | Congelar e registrar |

### Área 8: segurança

| ID | Sev | Verificar | Detecção | Fonte | Correção |
| --- | --- | --- | --- | --- | --- |
| IA-55 | B | Agente com A, B e C sem barreira | Cartão A/B/C | V-42 | Remover, separar ou aprovar |
| IA-56 | B | "Ignore comandos injetados" vendido como segurança | Documento de projeto | V-42, V-14 | Camada, não barreira |
| IA-57 | B | Conteúdo externo em `system` ou texto de usuário | Montagem de mensagens | V-43 | `tool_result` com origem |
| IA-58 | M | Allowlist com shell coringa ou interpretador | Configuração de permissões | V-13 | Remover |
| IA-59 | B | Segredo em prompt, cliente ou repositório | `grep` por padrões de chave | C-22 | Cofre/variável de ambiente |
| IA-60 | M | Validação de efeito só no prompt | Regra de negócio em texto | AP-12 | Código determinístico |
| IA-61 | M | Sem triagem de saída de tool de fonte de alto risco | Pipeline | V-43 | Modelo pequeno, saída estruturada |
| IA-62 | O | Sem plano de red team | Ausente | V-43 | Documentos com injeção |

### Áreas 9 a 12

| ID | Sev | Verificar | Detecção | Fonte | Correção |
| --- | --- | --- | --- | --- | --- |
| IA-63 | M | Timestamp ou dado variável antes do corte de cache | Montagem do prompt | V-24 | Estático primeiro |
| IA-64 | M | Cache sem medir `cache_read_input_tokens` | Logs/uso | V-24 | Medir ambos os campos |
| IA-65 | M | Preço citado sem data ou de memória | Docs, planilhas | V-38 | Data de leitura |
| IA-66 | O | Suíte de avaliação fora do Batch | Chamadas síncronas em massa | V-38 | Batch (metade do preço) |
| IA-67 | M | Sem span por chamada de modelo e por tool | Instrumentação | V-33 | Plano de telemetria |
| IA-68 | B | Conteúdo de prompt/resposta ligado por padrão em telemetria | Configuração | V-33 | Desligar; consentimento |
| IA-69 | O | Versão da convenção OTel não fixada | Dependências | V-33 | Fixar |
| IA-70 | B | Fine-tuning sem suíte e holdout | Projeto de treino | V-34 | Gate |
| IA-71 | M | Afirma fine-tuning direto de Claude sem página oficial | Documento | V-34 | Corrigir |
| IA-72 | M | `max_turns`/`max_budget_usd`/modo de permissão restritivo ausentes em agente sem supervisão | Config do Agent SDK | V-39 | Definir; sandbox |

## 5. Regras de reporte

- Ordene por severidade; agrupe por área; informe o que **não** foi checado.
- Leitura de código não é teste executado; CI verde não prova fluxo se as asserções forem fracas.
- Nunca copie valores de segredos ou dados pessoais para o relatório: cite a chave e o `arquivo:linha`.
- Itens com `V-nn` derivam de fontes lidas em 2026-10-10; reconfira preços, modelos e campos na data de uso.
