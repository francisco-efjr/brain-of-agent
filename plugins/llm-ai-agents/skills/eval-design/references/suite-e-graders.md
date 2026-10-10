# Suíte de avaliação, conjuntos e graders

Base: V-09 (Demystifying evals, 09/01/2026), V-12 e V-41 (plugin eval), brain `qa/references/ia-e-llm.md` e `fullstack/references/agentes-e-ia.md` (MIT, conteúdo do usuário; adaptado com atribuição ao repositório francisco-efjr/brain-of-agent). Conferido em 2026-10-10. Comando e formato de `claude plugin eval` podem mudar: confirme com `claude plugin eval --help` na versão instalada.

## Resultado observável e falha que a média esconde (brain `ia-e-llm`, adaptado)

| Produto | Resultado observável | Falha que a média não pode esconder |
| --- | --- | --- |
| Classificador | classe vs rótulo adjudicado; matriz de confusão por classe | falso negativo na classe crítica |
| Extração | campos exatos vs documento; valor ausente fica ausente | inventar CPF, valor ou data |
| Assistente RAG | afirmações sustentadas pelos trechos recuperados e autorizados | citar fonte inexistente; recuperar dado de outro tenant |
| Agente de execução | estado final do sandbox + registro de ações | duplicar operação; agir fora da autorização |
| Skill ou plugin | disparo correto, artefato utilizável, evidência honesta | declarar teste executado sem execução; disparar em pedido alheio |

Pesos e limites de aprovação são decisões do produto. 90% ou 95% não são padrões universais.

## Conjuntos

| Conjunto | Para quê | Regra |
| --- | --- | --- |
| Desenvolvimento | Orientar edições do prompt | Pode ser visto e usado |
| Regressão | Falhas já corrigidas que não podem voltar | Roda sempre; perto de 100% é esperado |
| Validação reservada | Medir de verdade | Nunca usado para editar; se usado, passa a desenvolvimento |
| Produção monitorada | Amostra autorizada e minimizada de uso real | Reavaliar segmentos quando a distribuição mudar |

Separe documentos, usuários, famílias de perguntas e períodos quando duplicatas puderem atravessar conjuntos. Capacidade (taxa inicial baixa, sobe com o trabalho) e regressão (perto de 100%) são suítes diferentes; saturação pede tarefas novas (V-09).

## Esquema de caso (brain `ia-e-llm`, MIT; ilustrativo, sem dependência de fornecedor)

```json
{
  "id": "rag-politica-ausente",
  "input": "Quanto custa cancelar meu plano?",
  "context": [{"id": "doc-1", "text": "O plano mensal custa R$ 40."}],
  "permissions": ["read_context"],
  "expected": "Informar que o contexto não contém a taxa de cancelamento; pedir a política aplicável.",
  "critical_failures": ["Inventar taxa", "Citar trecho inexistente"],
  "grading": ["revisão factual por trecho", "rastreio de citações"],
  "segment": "insuficiencia",
  "origin": "ticket-4812 (ilustrativo)"
}
```

O executor recebe entrada e artefatos; o avaliador recebe os critérios. Não entregue a resposta esperada ao executor. Inclua perguntas respondíveis: premiar toda recusa cria um modelo inútil; conte recusas corretas e indevidas separadamente.

## Escolha do grader (V-12, V-41)

| O que medir | Grader | Custo de modelo |
| --- | --- | --- |
| Texto observável na resposta | `regex` | nenhum |
| Uma ação concreta (a skill foi usada, uma tool foi chamada) | `tool_used` | nenhum |
| Ordem das ações | `tool_order` | nenhum |
| Artefato criado | `file_exists` (+ `regex` sobre o arquivo) | nenhum |
| Qualidade subjetiva em saída curta | `llm` com PASS/FAIL concretos; o juiz vota PASS em pelo menos 2 de 3 votos | 3 chamadas curtas por grader e execução |
| Regressão contra uma referência | `baseline` | chama juiz |

Regras: saída longa nunca passa por `llm`; use `regex` sobre arquivo. Um juiz por modo de falha. Se o delta fica perto de zero com `tool_used: Skill` falhando, o modelo não escolhe a skill: ajuste a `description`. Se o delta é negativo com `tool_used: Skill` passando, suspeite do juiz antes do plugin.

## Oráculos para produtos com LLM (brain `ia-e-llm`, adaptado)

1. Código para o que tem resposta verificável: JSON válido, soma exata, arquivo produzido, IDs permitidos, efeito persistido, nenhuma chamada extra.
2. Rubrica 0/1/2 para adequação, completude e ambiguidade, com trecho da saída que sustenta cada nota.
3. Juiz LLM calibrado contra amostra humana; desacordos registrados.
4. A/B com versão oculta e ordem alternada.

## Casos de `claude plugin eval` (formato do blueprint deste projeto)

`evals/<caso>/prompt.md`:

```markdown
---
description: Revisão de system prompt com CAPS e prefill
tags: [llm-ai-agents, llm-prompt-review]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---
Revise este system prompt do meu assistente de suporte (modelo-alvo: Sonnet 5.5) e devolva uma
versão melhor. Na API eu também preencho a resposta do assistente com "{" para forçar JSON.

YOU ARE A SUPPORT BOT. CRITICAL: YOU MUST ALWAYS ANSWER IN JSON. NEVER, EVER mention competitors.
```

`evals/<caso>/graders/criteria.md`:

```markdown
---
type: llm
---
PASS se a resposta (a) troca a ênfase em CAPS por motivo e linguagem calma; (b) dá o motivo da regra
e uma alternativa positiva; (c) aponta que prefill não é mais suportado em modelos 4.6+ e sugere
saída estruturada; (d) inclui plano de teste e não afirma ter testado.
FAIL se aumenta a ênfase, mantém prefill, reescreve sem explicar ou afirma que o prompt foi validado.
```

`evals/<caso>/graders/skill-fired.md`:

```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?llm-prompt-review"'
---
```

Caso negativo: o mesmo arquivo com `min: 0` e `max: 0`. Para o grader de `Skill` não sair do score no braço sem plugin, pode ser necessário `arm: both` (campo citado em outra skill do projeto; **conferir** na documentação da versão instalada). O workspace do eval começa vazio: o prompt embute o texto de que precisa. Rubricas ficam fora do contexto do executor.

Comandos para o usuário (o plugin não os executa): `claude plugin eval .` na raiz do plugin, com `--runs` e `--threshold` explícitos. Custo = casos × execuções × 2 braços + chamadas do juiz.

## Tabelas por produto (esqueleto de métricas)

| Produto | Métrica primária | Controle | Observação |
| --- | --- | --- | --- |
| Classificador | precisão e recall por classe (V-11) | matriz de confusão | acurácia sozinha esconde a classe crítica |
| Extração | campo exato | valor ausente permanece ausente | invenção é falha crítica |
| Resumo | consistência factual (NLI, V-11) | relevância | métricas aprendidas mais revisão humana |
| RAG | recall@k do trecho de referência; fidelidade da resposta | citação válida; insuficiência | avaliar recuperação e geração separadamente (ver `llm-decision-gates`) |
| Agente | estado final do sandbox | chamadas, custo, tempo, erros de tool | cenários de falha de tool (ver `agent-security-review`) |
