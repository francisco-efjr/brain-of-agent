# Decisões e trade-offs

Conferido em 2026-10-10 · Rótulos: Verificado, Inferido, Suposição, Não verificável · Árvores de decisão destiladas de `V-nn` (`docs/dev-segments/research/llm-ai-agents/VALIDATED.md`); as árvores são síntese (Inferido), cada critério ligado à fonte · Toda decisão registra a alternativa mais simples descartada e a data (use `assets/templates/adr.md` quando a decisão for material).

## Sumário

1. Workflow, agente ou multiagente
2. Onde colocar a instrução
3. Prompt, RAG ou fine-tuning
4. Modelo e `effort`
5. Superfície de agente
6. Técnica de contexto
7. Grader: código ou juiz
8. Prompt de sistema curto ou skill
9. Tensões a decidir por medição
10. Conflitos resolvidos (C1 a C12)

## 1. Workflow, agente ou multiagente (V-04, V-07)

| Pergunta | Sim | Não |
| --- | --- | --- |
| Uma chamada bem instruída resolve (medida na suíte)? | Pare | Próxima |
| Passos conhecidos de antemão? | Workflow: encadeamento, roteamento ou paralelização | Próxima |
| Subtarefas imprevisíveis? | Orquestrador-trabalhadores | Próxima |
| Critério de qualidade verificável? | Avaliador-otimizador com limite de iterações | Próxima |
| Passos imprevisíveis e ambiente confiável? | Agente com parada, tetos, sandbox, aprovação de escrita externa | Volte a workflow |
| Pesquisa ampla com partes independentes? | Multiagente, com custo ~15x tokens em medição interna | Agente único |

Trade-off: cada parte a mais é superfície de falha e de custo (agente ~4x, multiagente ~15x os tokens de um chat, medição interna de 2025). Multiagente ganha em amplitude e isolamento de contexto e perde em código com dependências compartilhadas.

## 2. Onde colocar a instrução (V-40, Verificado)

| Pergunta | Superfície |
| --- | --- |
| Isto precisa acontecer sempre? | **Hook** (garantia; roda com as permissões do usuário; não é fronteira de segurança) |
| Fato do projeto, vale em toda sessão? | **CLAUDE.md** curto (< 200 linhas) |
| Só vale ao mexer em certa área? | **Regra com escopo de caminho** (`.claude/rules/`) |
| Procedimento que o modelo escolhe quando o caso aparece? | **Skill** (gatilho na `description`) |
| Tarefa lateral que encheria o contexto? | **Subagente** (contexto isolado, devolve resumo) |
| Ação com efeito colateral disparada pelo usuário? | **Skill ou comando com `disable-model-invocation: true`** |
| Limite rígido? | **Hook ou permissão**, não CLAUDE.md |
| Estilo de saída ou acréscimo ao prompt de sistema | Só no post oficial, não na documentação lida; estilos de saída substituem o prompt padrão e podem perder instruções de engenharia: use com parcimônia |

Custo: um plugin habilitado mantém nome e descrição de cada skill invocável no contexto a cada turno; descrições curtas (< ~600 caracteres nas de tarefa).

## 3. Prompt, RAG ou fine-tuning (V-25, V-34, V-36)

1. Prompt + few-shot medidos na suíte própria? Se não, pare e meça.
2. A base cabe em ~200 mil tokens? Prompt completo com cache; sem RAG.
3. Não cabe e muda com frequência: RAG medido (100 perguntas, recall/precisão).
4. Falta comportamento/estilo que prompt e exemplos não alcançam, há holdout, exemplos de especialista e o modelo tem pesos abertos: considerar fine-tuning (gate de seis perguntas em `rag-custo-observabilidade.md`).
Trade-off: RAG custa infraestrutura e pontos de falha (ingestão, filtro, recuperação, citação); fine-tuning custa manutenção a cada troca de modelo base.

## 4. Modelo e `effort` (V-38; preços datados em `rag-custo-observabilidade.md`)

Monte a suíte; comece pelo modelo mais barato que a suíte aceitar; varie o `effort` antes de trocar de modelo; suba só nos casos que falham. Efficiency-first (começar no Haiku 5.5) contra capability-first (começar no Opus 5.5): escolha pelo custo de erro. Reconte tokens ao trocar de modelo (tokenizador novo, ~30% mais tokens). Fast mode (pesquisa): opção paga, não combina com Batch.

## 5. Superfície de agente (V-39)

Agent SDK (agente de código pronto no seu processo) · CLI (interativo ou pontual) · SDK cliente (controle total do laço) · Managed Agents (sem operar infraestrutura) · CLI com `-p` para outras linguagens. Trade-off: controle contra esforço de operar. Detalhes e restrições de marca em `agentes-contexto-harness.md`.

## 6. Técnica de contexto (V-06)

Conversa longa ⇒ compactação · marcos ⇒ notas externas · leitura volumosa ⇒ subagentes · estável e pequeno ⇒ pré-carga · grande ou mutável ⇒ referência e busca na hora. Trade-off: pré-carga favorece cache e perde espaço; busca na hora economiza janela e adiciona latência e pontos de falha.

## 7. Grader: código ou juiz (V-12)

Observável em texto ⇒ `regex`; ação ⇒ `tool_used`/`tool_order`; artefato ⇒ `file_exists`; saída longa ⇒ `regex` sobre o arquivo; qualidade subjetiva em saída curta ⇒ `llm` com PASS/FAIL concreto; regressão ⇒ `baseline`. Código primeiro, juiz depois, juiz calibrado com TPR/TNR.

## 8. Regra no system prompt ou em tool/skill (V-03)

Instrução de uso de tool mora na descrição da tool; conhecimento ocasional vira skill; exemplos que travam a exploração viram enum ou parâmetro; só o que o código não revela fica no CLAUDE.md. Trade-off: carga antecipada gasta contexto em todo turno; carga sob demanda depende do gatilho da `description` (subdisparo).

## 9. Tensões a decidir por medição (prompt-principles §5)

- Número de exemplos (zero a 12 ou mais), XML contra Markdown, posição da instrução, role prompting: sem consenso entre laboratórios.
- "Description insistente" do skill-creator contra tom calmo: gatilhos concretos e "não use para…", sem CAPS (C4).
- Limiar de contexto para handoff (cerca de 40% contra "sem degradação até 50%"): disputado (C7).
- Think tool e self-check: em grande parte superados por thinking adaptativo; a documentação cita que o Opus 5 não precisa de self-check (Inferido).
- Doc atual prevalece sobre repositórios quando divergem (hooks, output styles).

## 10. Conflitos resolvidos (SYNTHESIS §3.2)

| ID | Conflito | Resolução |
| --- | --- | --- |
| C1 | Aninhamento de subagentes: três camadas (documentação) contra cinco níveis (post de 2026-06-18) | Prevalece a documentação; conferir na versão instalada; os agentes do plugin não dependem de aninhamento |
| C2 | CLAUDE.md: < 200 (oficial) contra < 300 consenso e < 60 raiz própria (HumanLayer) | Limite duro 200; meta menor pelo teste de remoção; não citar "150-200 instruções" |
| C3 | Amostra do juiz: 30-50 por rótulo contra ~100 por modo | ~30 até cessarem modos novos; ~100 por modo só para alegar TPR/TNR; registrar escolha |
| C4 | Descrição "pushy" contra tom calmo | Gatilhos concretos; medir com 20 consultas |
| C5 | Multiagente +90,2% em pesquisa contra pior em código | Agente único por padrão |
| C6 | Onde repetir a instrução | Para Claude: documentos no topo, tarefa no fim; não repetir sem medir |
| C7 | Limiar de handoff: cerca de 40% da janela (comunidade) contra "sem degradação até 50%" | Disputado; gerar handoff por marco ou decisão, não por porcentagem; medir no próprio fluxo |
| C8 | Prompt contra barreira arquitetural | As duas, em camadas; nunca vender a política como segurança |
| C9 | CoT explícita contra thinking adaptativo | Pedir verificação; em schema, explicação curta |
| C10 | Chunk 800/400 contra 200 recursivo | Só a metodologia vale |
| C11 | AGENTS.md: agents.md não lista Claude Code; docs do Claude Code dizem que lê | Prevalece a documentação oficial; ponte via `CLAUDE.md` curto, sintaxe conferida na versão instalada |
| C12 | Fine-tuning de Claude: sem página oficial contra notebook de Bedrock | Não afirmar disponibilidade |

## Gotchas

- Registrar a decisão sem a alternativa mais simples descartada.
- Tratar árvore como lei: é síntese; meça no seu caso.
- Esquecer a data nas decisões de modelo, preço e limite.
