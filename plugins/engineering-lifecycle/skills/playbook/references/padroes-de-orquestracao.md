# Padrões de orquestração, anti-padrões e reconciliação com o ORCHESTRATOR

Base: [orchestration-patterns.md](../../../references/orchestration-patterns.md) do agent-skills (Addy Osmani, MIT; commit `aeac41d4d005999432bb7312f7ff06383a91d59d`), `docs/agents.md` do mesmo repositório e `publish/ORCHESTRATOR.md` do brain. Este arquivo descreve; **não decide pelo dono**. As decisões já tomadas estão na seção 5.

**Regra de ouro do upstream:** o usuário (ou um comando) é o orquestrador; personas não invocam personas; skills são saltos dentro do fluxo de uma persona. No brain, quem orquestra é a **sessão principal**, com profundidade 1 (ORCHESTRATOR §2 B).

## 1. Cinco padrões endossados

| # | Padrão | Use quando | Custo | No brain |
| --- | --- | --- | --- | --- |
| 1 | **Invocação direta** | Uma perspectiva sobre um artefato; descrevível em uma frase | Uma ida e volta; é a linha de base | Um especialista, uma rota de tag (§3 passo 3) |
| 2 | **Comando de persona única** | A mesma invocação se repete com a mesma preparação | Igual à direta; é um prompt salvo | `review`, `test`, `code-simplify`, `webperf` |
| 3 | **Fan-out paralelo com merge** | Subtarefas independentes, cada uma com contexto próprio, merge pequeno o bastante para a sessão principal, latência importa | N contextos mais um turno de merge | `/ship`; ORCHESTRATOR §3.1 passos 2 e 3 |
| 4 | **Pipeline sequencial conduzido pelo usuário** | Há dependência entre etapas e o julgamento humano entre elas agrega | Um contexto por etapa; sem agente orquestrador | `spec` → `plan` → `build` → `test` → `review` → `ship` (uso avulso) |
| 5 | **Isolamento de pesquisa** | Leitura grande que não deve poluir o contexto principal; o resultado é bem menor que a entrada | Um contexto isolado | §3.1 passo 2: o subagente devolve resumo, o relatório completo vai a arquivo |

**Quatro checagens antes de adotar o padrão 3** (o upstream pede todas):
1. Posso rodar todos ao mesmo tempo, sem ordem entre eles?
2. Cada persona produz um *tipo* diferente de achado, e não o mesmo achado por outro ângulo?
3. O merge cabe no contexto que sobra à sessão principal?
4. A espera do usuário é longa o bastante para o paralelismo compensar?

Qualquer "não": volte ao padrão 2 ou 1. No Claude Code, o paralelo exige **várias chamadas Agent na mesma rodada do assistente**; chamadas em turnos separados serializam.

## 2. Quatro anti-padrões

| | Anti-padrão | Por que falha | Em vez disso | Situação no brain |
| --- | --- | --- | --- | --- |
| A | **Persona roteadora** | Camada sem valor de domínio; dois saltos de paráfrase, ~2x de custo; o usuário já sabia o que queria | Comando ou mapeamento de intenção documentado | O roteamento é dado lido pela sessão principal (registro de tags), não persona. O `demand-router` é a exceção consciente (seção 5, tensão A) |
| B | **Persona que chama persona** | Quebra a visão única; o resumo perde contexto; falhas se multiplicam; esconde custo | A persona **recomenda** o segundo passe no relatório; a sessão principal despacha | Nenhum agente do brain declara a ferramenta `Agent` (conferido por busca no VALIDATED); o único caso de texto "delegue" já foi corrigido (tensão F) |
| C | **Orquestrador sequencial que parafraseia** | Perde os checkpoints humanos, acumula desvio a cada resumo, dobra o custo | O usuário orquestra | Desvio consciente: a autonomia do ORCHESTRATOR §0 é decisão do dono (tensão B). Atenuantes: três paradas, decisão pendente em patch, validadores, relatório completo em arquivo |
| D | **Árvore profunda de personas** | Cada camada soma latência e tokens sem decisão; o folha perde contexto | Profundidade máxima 1: comando para personas; merge na sessão principal | Igual ao §2 B "Profundidade 1" |

## 3. Árvore de decisão (8 linhas)

Adaptada de `references/orchestration-patterns.md` — Addy Osmani, agent-skills, MIT. Em inglês, como no original.

```text
1. Is it one perspective on one artifact?                  Yes -> direct invocation. Stop.
2. Will the same composition repeat?                       No  -> ad hoc direct invocation. Stop.
3. Are the sub-tasks independent?                          No  -> sequential commands run by the user (pattern 4).
4. Do the four fan-out checks pass?                        Yes -> parallel fan-out, merge in the main agent (pattern 3).
5. Does any check fail?                                    Yes -> single-persona command (pattern 2).
6. Large read, small result, main context must stay clear? Yes -> research isolation, digest only (pattern 5).
7. Must the investigators challenge each other?            Yes -> Agent Teams (experimental, costs more).
8. Never build: router persona, persona-calls-persona, paraphrasing sequential orchestrator, depth > 1.
```

## 4. Coincidências com o ORCHESTRATOR

| # | Padrão do upstream | No ORCHESTRATOR | Observação |
| --- | --- | --- | --- |
| 1 | Profundidade 1; merge no principal | §2 B "Profundidade 1" | O ORCHESTRATOR já cita a coincidência |
| 2 | Fan-out com merge | §3.1 passos 2 e 3 | O brain acrescenta deduplicação com IDs de origem e validador por área; o `/ship` não tem |
| 3 | Isolamento de pesquisa | §3.1 passo 2 | Igual |
| 4 | Especialista recomenda; o principal decide | §2 B | Nenhum agente do brain declara `Agent` |
| 5 | Verificação no merge | §3 passo 6: validador independente, outro papel, se possível outro modelo | O brain é mais forte |
| 6 | Limites no texto do prompt (o plugin ignora `hooks`, `mcpServers`, `permissionMode`) | Bloco de limites do §2 B | Mesmo princípio |
| 7 | Modelo por custo | §5 Custo | Mesmo princípio |
| 8 | Gates humanos pontuais (`/plan`, `/build auto` com aprovação única) | §0: três paradas | Compatível |
| 9 | `/build auto` exige árvore limpa | §0 e §3.1 passo 1 | Igual |

## 5. Decisões do SYNTHESIS (caminho conservador)

Tensões levantadas no VALIDATED §8.2 e a decisão registrada no SYNTHESIS §3 item 3. Nada aqui é novo; é o que o playbook aplica.

| ID | Tensão | Decisão |
| --- | --- | --- |
| A | `demand-router` × anti-padrão A | Vira **opcional**: plano em contexto novo ou validação do plano da sessão principal; fora do caminho crítico |
| B | Autonomia do §0 × anti-padrão C | Fica, como decisão do dono. Gates do upstream viram suposição registrada ou decisão pendente (precedência, item 10) |
| C | Agent Teams | Não adotado; descrito na seção 6 |
| D | `general-purpose` não herda `tools` | Copie o `tools` do frontmatter do agente para o prompt do subagente; `Explore` serve só a busca (tem Bash e não é auditoria) |
| E | Profundidade 1 | Resolvida no ORCHESTRATOR §2 B |
| F | "delegue a `db-security-auditor`" em `database-data-modeling/agents/db-reviewer.md` | Resolvida fora deste plugin: `db-reviewer.md:83` agora diz "recomende no relatório uma passagem de `db-security-auditor` (quem despacha é a sessão principal)" (Verificado na validação de qualidade, 2026-10-13) |
| G | `code-reviewer` do upstream × `code-quality-refactoring:code-reviewer` | No `/ship`, nomes qualificados `engineering-lifecycle:<persona>` |

**Quem valida o quê** (ORCHESTRATOR §3.1 passo 3) e a lacuna que este plugin preenche:

| Artefato | Validador independente |
| --- | --- |
| Arquitetura | `architecture-design:skeptic-architect` |
| Código | `code-quality-refactoring:finding-validator` |
| Segurança | `security-appsec:finding-verifier` |
| Testes | `qa-testing:test-auditor` |
| Spec | `product-discovery-specs:spec-reviewer` |
| Decisão, plano ou afirmação sem dono | `engineering-lifecycle:fresh-context-doubter` (revisor genérico; só a sessão principal o aciona) |

## 6. Agent Teams: descrito, não adotado

- **O que é (segundo o upstream):** colegas que trocam mensagens e compartilham uma lista de tarefas, em vez de só reportar à sessão principal. Serve a **hipóteses concorrentes** que precisam se desafiar (por exemplo, um travamento intermitente com quatro causas plausíveis).
- **Estado:** experimental, ligado por `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, Claude Code 2.1.32 ou superior, segundo o upstream. **Não verificado na documentação oficial da Anthropic** (sem acesso web nesta construção).
- **Custo:** cada colega é uma instância; a conclusão tende a ser melhor e o gasto, maior.
- **Por que o brain não adota:** não há suporte no protocolo; mudar o ambiente do usuário (variável de ambiente) exige confirmação; o ganho aparece só em investigação com hipóteses concorrentes. Se o dono quiser, a opção é opt-in por pedido, com a flag e o custo declarados.
- **Não reconstrua como subagentes:** um `/debug` com fan-out de subagentes perde o debate, que é o que dá valor ao padrão.

## 7. Regras de plataforma citadas pelo upstream

Rótulo: **Não verificado** na documentação oficial da Anthropic; vêm do texto do próprio upstream.
- Subagentes não criam subagentes.
- Agentes de plugin ignoram os campos `hooks`, `mcpServers` e `permissionMode`; valem `name`, `description`, `tools`, `disallowedTools`, `model`, `maxTurns`, `skills`, `memory`, `background`, `effort`, `isolation`, `color`, `initialPrompt`.
- `allowed-tools` pré-aprova e não restringe; `disallowed-tools` remove.
- Persona definida pelo usuário em `.claude/agents/` vence a do plugin com o mesmo nome.
- Subagentes embutidos: `Explore` (busca), `Plan` (pesquisa em modo de plano), `general-purpose`. Não redefina.
