---
name: prompts
description: Biblioteca de prompts curados de Produto, descoberta e especificação. Use quando pedirem prompt, template ou mensagem pronta para entrevista de requisitos, SPEC.md, PRD, spec com FR/SC, critérios de aceite (Given/When/Then, EARS), histórias INVEST, Example Mapping, priorização (RICE, ICE, MoSCoW, Kano), roadmap Now-Next-Later, OKR, roteiro de entrevista JTBD, árvore de oportunidades, quatro riscos, experimento A/B, sprint planning, tarefas a partir da spec, revisão adversarial de spec, briefing de subagente, handoff, prompt de sistema ou mensagem inicial do projeto. Gatilhos PT-BR - "prompt pronto para PRD", "template de critérios de aceite", "me dê um prompt para entrevistar usuários". EN - "PRD prompt", "spec interview prompt", "acceptance criteria template". Para executar a tarefa em si, use a skill de tarefa correspondente.
---

# Prompts de produto, descoberta e especificação

Entrega prompts prontos, com variáveis `[EM_COLCHETES]`, para as tarefas recorrentes do segmento. São 40 prompts, cada um com quando usar, variáveis, texto, por que funciona e fonte com classe. Ficam em três arquivos:

- [references/prompt-library.md](references/prompt-library.md): índice completo, convenções e 20 prompts de uso mais frequente (entrevista, PRD, spec, revisão, palavras vagas, critérios, INVEST, delegação, decisão, handoff, prompt de sistema, mensagem inicial).
- [references/prompts-criterios-e-priorizacao.md](references/prompts-criterios-e-priorizacao.md): EARS, Example Mapping, história, RICE, Kano, MoSCoW, pitch, OKR, roadmap, sprint.
- [references/prompts-descoberta-e-execucao.md](references/prompts-descoberta-e-execucao.md): entrevista JTBD, síntese, árvore de oportunidades, quatro riscos, premissas, experimento, tarefas, plano, lista de features, regras de negócio.

## Quando usar esta skill e quando não usar

- Use quando a pessoa quer o texto do prompt para colar em outro chat, subagente, CLAUDE.md ou pipeline, ou quer adaptá-lo ao projeto.
- Não use para executar a tarefa. "Escreva o PRD disso" ou "critérios para esta história" com o material anexado são das skills `write-prd` e `acceptance-criteria`; entregar um prompt em vez do resultado frustra quem esperava o documento. Se o pedido for ambíguo ("preciso de um prompt para X" contra "faça X"), entregue o prompt e ofereça executar.
- Pedido com `PRODUTO-COMPLETO` escrito pelo usuário é do `playbook`.

## Processo

1. **Identifique a tarefa** e escolha o prompt na tabela abaixo. Se dois servem, entregue o mais específico e cite o outro em uma linha.
2. **Leia só a seção necessária**: use `Grep` por `^## P-NN` no arquivo indicado e leia aquele trecho. Não carregue a biblioteca inteira.
3. **Preencha as variáveis** que a conversa já responde. Para as demais, deixe `[VARIÁVEL]` visível e liste o que falta; pergunte apenas se a resposta mudar o prompt de forma material. Nunca invente nome, número, métrica ou plataforma para preencher.
4. **Entregue** em bloco de código: o prompt, uma linha de "onde rodar" (plan mode ou subagente para revisões; gravação de arquivo só quando o prompt disser) e uma linha de "por que funciona". Tom calmo, sem CAPS.
5. **Adapte com critério**: preserve o formato de saída, o aviso de que o material colado é dado, a política de incerteza, o bloco para execução sem interação e o limite de escrita. Se a mudança pedida remover um deles, diga o que se perde.
6. **Não afirme eficácia.** Nenhum prompt foi medido. Existem fontes, estrutura e os casos de `evals/`, ainda não executados.

## Qual prompt para qual tarefa

| Tarefa | Prompt | Arquivo | Skill ou agente que executa |
| --- | --- | --- | --- |
| Entrevistar antes de especificar; gerar `SPEC.md` | P-01 | biblioteca | `spec-interview` |
| Pedido vago, usuário explorando; decidir se executa ou conversa | P-02 | biblioteca | `playbook`, `spec-interview` |
| PRD enxuto; PRD com limites mensuráveis | P-04, P-05 | biblioteca | `write-prd` |
| Spec completa; achar e resolver lacunas | P-06, P-07 | biblioteca | `write-spec` |
| Revisão adversarial do diff ou da spec; gate de fase | P-09, P-10 | biblioteca | agente `spec-reviewer` |
| Palavras vagas; regras implícitas e NFR | P-11, P-12 | biblioteca | `acceptance-criteria` |
| Critérios Given/When/Then declarativos; INVEST e divisão | P-13, P-17 | biblioteca | `acceptance-criteria`, `refine-backlog` |
| Escolher framework de priorização | P-19 | biblioteca | `prioritize-roadmap` |
| Briefing de subagente; spec de bugfix; decisão; spec viva; handoff | P-36, P-37, P-39, P-40, P-41 | biblioteca | agentes do plugin, `write-spec` |
| Prompt de sistema; primeira mensagem do projeto | P-42, P-43 | biblioteca | `playbook` |
| EARS; Example Mapping e three amigos; história (cartão, conversa, confirmação) | P-15, P-16, P-18 | critérios e priorização | `acceptance-criteria`, `refine-backlog` |
| RICE; Kano; MoSCoW | P-20, P-21, P-22 | critérios e priorização | `prioritize-roadmap` |
| Pitch com apetite; OKR; Now-Next-Later; sprint planning | P-28, P-30, P-31, P-32 | critérios e priorização | `prioritize-roadmap`, `refine-backlog` |
| Roteiro de entrevista; síntese; árvore; quatro riscos | P-23, P-24, P-25, P-26 | descoberta e execução | `run-discovery`, agente `discovery-synthesizer` |
| Desafio de premissas; experimento A/B | P-27, P-29 | descoberta e execução | `run-discovery` |
| Tarefas, plano, lista de features, regras de negócio de código legado | P-33, P-34, P-35, P-38 | descoberta e execução | `spec-to-tasks` (manual), agente `plan-writer` |

Os identificadores P-03, P-08 e P-14 foram fundidos em P-02, P-10 e P-13 e não são reutilizados.

## Checklist para adaptar ou criar um prompt do segmento

1. Papel e resultado esperado em uma frase; o que está fora de escopo.
2. Contexto e o porquê de cada regra; cada proibição com a alternativa.
3. Material colado dentro de tags e declarado como dado, não instrução.
4. Formato de saída explícito (tabela, `arquivo:linha`, severidade, confiança).
5. Critério de pronto verificável; rótulos Verificado, Inferido, Suposição; proibição de afirmar execução que não houve.
6. Política de incerteza: lacuna vira `[NEEDS CLARIFICATION]` ou `TBD`, nunca chute no corpo.
7. Execução sem interação: perguntas e gates viram "Decisões pendentes do humano" e o trabalho segue em rascunho.
8. Plataforma: o prompt pede para declarar onde roda (web, Android, iOS, desktop, servidor) ou aponta o plugin certo (`/mobile-apps:playbook` para mobile).
9. Autorização: gravar só em caminho nomeado; nenhuma ação externa (issue, comentário, roadmap publicado) sem confirmar o texto exato.

## Gotchas

- Perguntas demais matam a entrevista: o limite adotado é 3 por rodada, e é Suposição de calibração. O checklist geral da casa pede uma pergunta por vez; o desvio vale só dentro de rodada de requisitos com play back. Fora dela, dúvida material no meio de outra tarefa é uma pergunta por vez.
- Revisor sem o limite "só lacunas de correção e de requisito" produz lista de preferências; mantenha a restrição de P-09 e P-10.
- Número de priorização sem origem e sem versão da escala é Suposição; os prompts RICE e ICE exigem as duas coisas.
- Faixas e limiares (3 perguntas, 85%, 7 de 10, amostra pequena abaixo de 8) são configuráveis e não foram medidos.
- O plugin não ativa hooks nem MCP. Prompt não substitui regra de permissão nem revisão humana quando uma decisão não pode falhar.
- Os prompts citam agentes pelo nome (`spec-reviewer`, `plan-writer`); sem o plugin instalado, mande fazer a tarefa direto em modo somente leitura.
