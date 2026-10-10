# Checklists de prontidão e matriz do modo completo

Checklists verificáveis por leitura. Marque cada item como `ok`, `falha` ou `n/a (motivo)` e cole o resultado na entrega; item sem evidência vale como falha. Fontes: V-02, V-04, V-05, V-11, V-18, V-27, V-44 e a base própria (V-42).

## Sumário

- [1. Antes de codar](#1-antes-de-codar)
- [2. spec-readiness](#2-spec-readiness)
- [3. prd-readiness](#3-prd-readiness)
- [4. story-ready](#4-story-ready)
- [5. sprint-ready](#5-sprint-ready)
- [6. experiment-design](#6-experiment-design)
- [7. priorizacao-ok](#7-priorizacao-ok)
- [8. skill-publishing](#8-skill-publishing)
- [9. Matriz de aplicabilidade do modo PRODUTO-COMPLETO](#9-matriz-de-aplicabilidade-do-modo-produto-completo)
- [10. Registro de leitura](#10-registro-de-leitura)

## 1. Antes de codar

Checklist de V-02 (documentação do Claude Code, destilado), a ser colado no pedido de implementação:

- [ ] O diff cabe numa frase? Se sim, faça direto (sem spec).
- [ ] Se não: exploração sem editar, plano com arquivos, fluxo e riscos, e aprovação do plano.
- [ ] Cada requisito lista o check que o prova (comando, teste, comparação de captura de tela).
- [ ] Ao terminar, mostrar a saída real dos checks e dizer o que não foi verificado.
- [ ] Se o check falhar duas vezes, parar, resumir o que foi tentado e pedir direção.

## 2. spec-readiness

Aplicável a spec de feature, curta e de bugfix. Resultado colado na resposta.

- [ ] SR-01 Problema, usuário e resultado mensurável estão declarados.
- [ ] SR-02 Cada requisito `FR` tem check observável e oráculo com dado concreto.
- [ ] SR-03 Cada `FR` mapeia a pelo menos um `SC` ou critério (rastreabilidade).
- [ ] SR-04 Nenhum nome de tecnologia, tabela ou biblioteca em `FR` e `SC`.
- [ ] SR-05 Nenhuma palavra vaga sem número (varredura da tabela em [criterios-e-historias.md](criterios-e-historias.md)).
- [ ] SR-06 Seção Fora de escopo presente e específica.
- [ ] SR-07 Histórias priorizadas P1, P2, P3, cada uma entrega valor sozinha e tem teste independente.
- [ ] SR-08 Pelo menos um caminho negativo por história; bordas em forma de pergunta respondidas ou abertas.
- [ ] SR-09 Regras implícitas e NFR varridos (permissão, estados, dados existentes, limites, concorrência, falhas, desfazer, efeitos em volta, canais; performance, segurança, acessibilidade, logs, i18n, LGPD).
- [ ] SR-10 Premissas listadas e rotuladas; nada inventado no corpo.
- [ ] SR-11 Todo `[NEEDS CLARIFICATION]` e `TBD` listado ao fim, com dono.
- [ ] SR-12 Sem contradição entre histórias, `FR` e `SC` (ex.: campo opcional numa seção e obrigatório em outra).
- [ ] SR-13 Um padrão principal de critério por spec.
- [ ] SR-14 Teste do estranho: alguém que não participou da entrevista consegue implementar sem perguntar de novo.
- [ ] SR-15 Aprovação G1 citada, ou "sem aprovação" declarado.

## 3. prd-readiness

- [ ] PR-01 Problema e usuário nomeados, com evidência rotulada (dado, relato, Suposição).
- [ ] PR-02 Pelo menos uma métrica mensurável, com definição operacional (nome, fórmula, fonte, janela, baseline ou `TBD`, meta).
- [ ] PR-03 Não-objetivos presentes.
- [ ] PR-04 Premissas e perguntas abertas separadas do corpo.
- [ ] PR-05 Nenhum número sem origem (mercado, KPI, concorrente) e nenhum adjetivo vago; limites no lugar.
- [ ] PR-06 Riscos pela matriz dos quatro riscos, cada um com dono.
- [ ] PR-07 Faseamento (MVP, v1.1, v2.0) com resultado esperado por fase.
- [ ] PR-08 Tamanho entre 600 e 1.000 palavras (alvo; desvio justificado).
- [ ] PR-09 Seção de IA presente apenas se o produto usa IA.
- [ ] PR-10 Caminho do arquivo confirmado com o usuário; G1 citado.

## 4. story-ready

A definição de "ready" é construção deste plugin (Suposição); o Scrum Guide 2020 não a prescreve (V-44).

- [ ] SD-01 INVEST: Independente, Negociável, Valiosa, Estimável, Pequena, Testável (uma linha por letra).
- [ ] SD-02 Cartão no formato Como/quero/para, com benefício específico.
- [ ] SD-03 Critérios em um padrão, com exemplos concretos, caminho negativo e oráculo.
- [ ] SD-04 Palavras vagas resolvidas ou viradas em perguntas com dono.
- [ ] SD-05 Regras implícitas e NFR relevantes tratados ou declarados fora de escopo.
- [ ] SD-06 Nenhuma pergunta vermelha (Example Mapping) sem dono.
- [ ] SD-07 Dependências e dados de teste identificados.
- [ ] SD-08 Cabe numa iteração e, para execução por agente, numa sessão focada.

## 5. sprint-ready

Apoio ao time, que é quem planeja (V-44). Template: [sprint-planning.md](../assets/templates/sprint-planning.md).

- [ ] SP-01 Meta da Sprint em uma frase (por que a Sprint é valiosa).
- [ ] SP-02 Itens selecionados cabem na capacidade informada (PTO, reuniões, carry-over); a conta está visível, a estimativa é do time.
- [ ] SP-03 Cada item passa `story-ready`.
- [ ] SP-04 Itens decompostos em tarefas de até um dia (como será feito).
- [ ] SP-05 Definition of Done conhecida e aplicada ao conjunto.
- [ ] SP-06 Risco e dependência externa listados com dono.
- [ ] SP-07 O que fica de fora da Sprint está explícito.

## 6. experiment-design

Base: V-27.

- [ ] EX-01 Hipótese com mudança, população e efeito esperado.
- [ ] EX-02 Métrica primária com definição operacional; métricas de guarda.
- [ ] EX-03 Efeito mínimo de interesse (δ) e variância (σ²) declarados.
- [ ] EX-04 Amostra fixa por braço calculada antes de começar (regra de bolso do autor `n ≈ 16 σ² / δ²`, rotulada).
- [ ] EX-05 Critério de parada escrito antes; nenhuma parada por significância espiada.
- [ ] EX-06 Alternativa sequencial ou bayesiana, se for preciso monitorar, com checkpoints combinados antes.
- [ ] EX-07 Decisão pré-registrada: o que fazemos se ganhar, perder ou empatar.
- [ ] EX-08 Aleatorização e unidade (usuário, sessão) declaradas; interferência entre braços considerada (Inferido, conhecimento estável).
- [ ] EX-09 Limite declarado: análise avançada pertence a `/data-science-ml:playbook`.

## 7. priorizacao-ok

- [ ] PZ-01 Objeto da priorização identificado e framework coerente com ele.
- [ ] PZ-02 Versão da escala registrada (RICE Intercom, ICE 1 a 10...).
- [ ] PZ-03 Cada número com origem (dado, estimativa, Suposição).
- [ ] PZ-04 Aritmética recalculada.
- [ ] PZ-05 Sensibilidade: o que muda o ranking.
- [ ] PZ-06 MoSCoW com "não nesta entrega" e "reavaliar em"; Kano usado para classificar, não ordenar.
- [ ] PZ-07 Decisão final atribuída ao humano.

## 8. skill-publishing

Para quem estende este plugin ou escreve skills próprias (V-04, documentação de skills da Anthropic; V-05, `skill-creator`, Apache-2.0).

- [ ] SK-01 `name` com até 64 caracteres, letras minúsculas, números e hífens, igual à pasta, sem as palavras reservadas "anthropic" e "claude".
- [ ] SK-02 `description` não vazia, até 1024 caracteres, em terceira pessoa, com o que faz e quando usar, sem tags XML.
- [ ] SK-03 Corpo do `SKILL.md` com menos de 500 linhas; detalhe em `references/`, a um nível; sumário em arquivos com mais de 100 linhas.
- [ ] SK-04 Barras normais em caminhos; sem informação com data que envelheça.
- [ ] SK-05 Pelo menos três avaliações (disparo, não disparo, falha comum); testar em modelos de tamanhos diferentes. No `claude plugin eval`, o caso de não disparo usa `tool_used` de `Skill` com `min: 0`, `max: 0` e `arm: both`, porque em execução com baseline os graders de `Skill` saem do score; `Write` e `Bash` só existem na execução com `--allow-tools` (Verificado em https://code.claude.com/docs/en/plugin-evals, 2026-10-10).
- [ ] SK-06 Otimização da `description` com cerca de 20 consultas (8 a 10 devem disparar, 8 a 10 não), priorizando quase-casos negativos e dividindo treino e teste (V-05).
- [ ] SK-07 Skill com efeito colateral usa `disable-model-invocation: true` e `allowed-tools` mínimos.
- [ ] SK-08 Explica o porquê em vez de ordens soltas em maiúsculas.
- [ ] SK-09 O script de avaliação do `skill-creator` executa Python local e `claude -p`; revise antes de rodar.

## 9. Matriz de aplicabilidade do modo PRODUTO-COMPLETO

Preencha uma linha por área. Estado: **Aplicável**, **Não aplicável** (com motivo) ou **Sem dados** (não verificável; vira pergunta). Justificativa de uma linha. Não escreva artefato para área não aplicável.

| Área | Pergunta que decide | Estado | Justificativa | Artefato ou skill |
| --- | --- | --- | --- | --- |
| Descoberta | Há dado de usuário ou premissa a validar? | | | `run-discovery`, `quatro-riscos.md` |
| PRD | É iniciativa ou produto (N4)? | | | `write-prd` |
| Spec | Há feature com regras de negócio (N3) ou mudança pequena (N2)? | | | `write-spec`, `spec.md` |
| Critérios | Existem histórias ou requisitos sem oráculo? | | | `acceptance-criteria` |
| Histórias | Há história grande, vaga ou sem INVEST? | | | `refine-backlog` |
| Priorização | Há lista a ordenar com objeto e dado definidos? | | | `prioritize-roadmap`, `rice.md` |
| Roadmap e OKR | Há horizonte de trimestre ou mais? | | | `roadmap-nnl.md`, `okr.md` |
| Experimentos | Há hipótese que um teste responde? | | | `run-discovery experiment` |
| Sprint | O time pediu planejamento? | | | `refine-backlog`, `sprint-planning.md` |
| Tarefas e handoff | Existe spec aprovada para executar em outra sessão? | | | `spec-to-tasks`, `handoff.md` |
| Manutenção da spec | Já houve implementação que divergiu da spec? | | | `write-spec` (atualização) |
| Segurança e escopo | Há PII, ação externa, texto não confiável ou permissão a ampliar? | | | regras de CLAUDE.md; confirmação por ação |

## 10. Registro de leitura

Tabela a manter no modo completo (um registro por arquivo realmente aberto):

| Arquivo | Estado (lido / parcial / ausente) | Decisões extraídas | Relação com o pedido |
| --- | --- | --- | --- |
| `references/entrevista-e-clarificacao.md` | | | |

Leitura truncada é parcial; continue do ponto seguinte. Ver só o nome ou o sumário não conta como lido.
