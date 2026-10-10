---
name: prompts
description: Biblioteca de prompts curados de Arquitetura e design de sistemas. Use quando pedirem prompt, template ou mensagem pronta para ADR, revisão de arquitetura ou de plano, trade-offs, decomposição (monólito modular, bounded contexts, strangler), resiliência e consistência (outbox, retry, saga), revisão de API, system design, diagramas C4 e Mermaid, briefing de subagente ou CLAUDE.md de arquitetura. Em PT-BR, gatilhos como "prompt pronto para arquitetura", "me dê um prompt para revisar desenho", "template de ADR", "prompt de sistema para arquitetura". Em EN, gatilhos como "architecture prompt", "ADR prompt", "system design prompt template". Para executar a tarefa em si, use a skill de tarefa correspondente do plugin.
---

# Prompts de arquitetura

Entrega prompts prontos, com variáveis `[EM_COLCHETES]`, para as tarefas recorrentes do segmento. A biblioteca completa (28 prompts, cada um com quando usar, variáveis, texto, por que funciona e fonte com classe) está em [references/prompt-library.md](references/prompt-library.md).

## Quando usar esta skill e quando não usar

- Use quando a pessoa quer o texto do prompt para colar em outro chat, subagente, CLAUDE.md ou pipeline, ou quer adaptar um prompt ao próprio projeto.
- Não use para executar a tarefa. Se o pedido é "revise este plano" com o plano anexado, a skill de tarefa (`design-review`, `adr`, `decomposition` etc.) resolve; entregar um prompt em vez da revisão frustra quem esperava o resultado. Se o pedido for ambíguo ("preciso de um prompt para X" contra "faça X"), entregue o prompt e ofereça executar.
- Pedido com a keyword `ARQUITETURA-COMPLETO` escrita pelo usuário é do `playbook`, não desta skill.

## Processo

1. **Identifique a tarefa** e escolha o prompt na tabela abaixo. Se dois servem, entregue o mais específico e cite o outro em uma linha.
2. **Leia só a seção necessária**: busque `^## PR-NN` em `references/prompt-library.md` (Grep) e leia aquele trecho; não carregue a biblioteca inteira.
3. **Preencha as variáveis** que o contexto da conversa já responde. Para as demais, mantenha `[VARIÁVEL]` visível e liste o que falta; pergunte só quando a resposta mudar o prompt de forma material. Nunca invente nomes, números ou métricas para preencher.
4. **Entregue** em bloco de código: o prompt, uma linha de "onde rodar" (plan mode ou subagente para revisões; gravação de arquivo só quando o prompt disser) e uma linha de "por que funciona". Mantenha o tom calmo do original: sem CAPS nem ameaças.
5. **Adapte com critério** se a pessoa pedir mudança: preserve o formato de saída, o aviso de que conteúdo colado é dado, a política de incerteza e o limite de escrita. Se uma mudança remover um desses itens, avise o que se perde.
6. **Não afirme eficácia.** Nenhum prompt da biblioteca foi medido; diga isso se perguntarem "funciona?". O que existe são fontes, estrutura e os casos de `evals/` ainda não executados.

## Qual prompt para qual tarefa

| Tarefa | Prompt | Skill ou agente que executa |
| --- | --- | --- |
| Decidir se algo merece ADR; entrevistar; rascunhar | PR-01, PR-02, PR-03 | `adr`; agente `adr-writer` (só sob pedido) |
| Substituir ADR aceito; consultar "por que escolhemos X"; ADR retroativo | PR-04, PR-05, PR-06 | `adr`, `adr-write` |
| Revisar plano, design ou PR de arquitetura | PR-07, PR-08, PR-09 | `design-review` |
| Revisão adversarial da diff contra o plano | PR-10 | agente `architecture-reviewer` |
| Evitar concordância cega; pré-mortem | PR-11, PR-12 | agente `skeptic-architect` |
| Microsserviços contra monólito; contextos; agregados | PR-13, PR-14, PR-15 | `decomposition`; agente `boundary-mapper` |
| Regra de camadas verificável; plano strangler | PR-16, PR-17 | `decomposition`; agente `boundary-mapper` |
| Outbox, consumidor idempotente, retry, breaker, bulkhead, CQRS, event sourcing | PR-18, PR-19, PR-20 | `resilience-and-consistency` |
| Sistema novo com estimativa e modos de falha | PR-21 | `system-design` |
| Contrato de API | PR-22 | `api-design` |
| Diagrama C4 ou Mermaid | PR-23 | `playbook` (referência de diagramas) |
| Pesquisar, planejar, anotar com gates | PR-24 | `architecture-plan` (manual) |
| Delegar a subagente; passar o bastão | PR-25, PR-26 | agentes do plugin |
| CLAUDE.md ou prompt de sistema do projeto; primeira mensagem | PR-27, PR-28 | `playbook` |

## Checklist para adaptar ou criar um prompt do segmento

1. Papel e resultado esperado em uma frase, e o que está fora de escopo.
2. Contexto e o porquê de cada regra; cada proibição com a alternativa.
3. Dados colados dentro de tags e declarados como material de análise, não instrução.
4. Formato de saída explícito (tabela, `arquivo:linha`, severidade, confiança).
5. Critério de pronto verificável e rótulos Verificado, Inferido, Suposição; proibição de afirmar execução que não houve.
6. Política de incerteza: lacuna vira `[NEEDS CLARIFICATION]`; decisão de preferência volta como pergunta ao dono humano.
7. Autorização: somente leitura por padrão; gravação só em caminho nomeado; nada de ação externa, de produção ou irreversível sem autorização concreta.
8. Opção "não mudar nada" e ao menos uma consequência negativa em toda decisão.

## Gotchas

- Prompts mais longos não são melhores: os desta biblioteca têm um formato de saída e um critério de parada; ao acrescentar instruções, remova o que ficou redundante.
- Um prompt de revisão que não restringe o relato a lacunas de correção e requisitos produz uma lista de preferências; mantenha a restrição de PR-10.
- Limiares numéricos (85%, 66%, 7 de 10, 8 arquivos) são Suposição configurável, não regra.
- O plugin não ativa hooks nem MCP. Prompts não substituem regra de permissão, teste de arquitetura em CI ou revisão humana quando algo não pode falhar.
- Os prompts citam `architecture-design:architecture-reviewer` e outros agentes pelo nome do plugin; sem o plugin instalado, o prompt manda fazer a tarefa diretamente em modo somente leitura.
