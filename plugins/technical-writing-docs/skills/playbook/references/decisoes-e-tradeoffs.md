# Decisões e trade-offs

Validado em 2026-10-10. Cada decisão traz critérios, recomendação padrão, quando inverter e rótulo. Códigos C-nn são os conflitos entre fontes resolvidos no design do plugin; V-nn em [fontes](fontes.md).

## Sumário

1. Onde mora cada instrução (e output style)
2. AGENTS.md ou CLAUDE.md
3. Tamanho da raiz do CLAUDE.md
4. Gerar o CLAUDE.md com `/init` ou à mão
5. Completude ou economia (dois regimes)
6. Gerar ou escrever o changelog
7. Mermaid, ASCII ou PlantUML
8. Dialeto de docstring por linguagem
9. Fonte única da API
10. Links: offline ou online
11. Correção factual direta ou pergunta
12. Estilo: Vale, output style ou CLAUDE.md
13. Hook de lint ou CI
14. Editar ou criar nova ADR
15. Onboarding: tutorial ou how-to

## 1. Onde mora cada instrução

| Critério | Destino | Quando inverter | Rótulo |
| --- | --- | --- | --- |
| Vale em toda sessão, curta, universal | `CLAUDE.md`/`AGENTS.md` | Se um linter já garante, apague | Verificado (V-01) |
| Vale só para certos arquivos | `.claude/rules/*.md` com `paths:` | Se o glob não casa, a regra nunca carrega: teste | Verificado (V-01) |
| Procedimento com etapas, usado de vez em quando | Skill | Se é fato de uma linha, CLAUDE.md | Verificado (V-01) |
| Tem que acontecer sempre ou ser bloqueado | Hook, linter ou CI | Se aceita falha ocasional, uma regra basta | Verificado (V-01, V-15) |
| Muda o tom e o formato da sessão inteira | Output style (vale para a conversa principal, não para subagentes) | Atrapalha tarefas de código não relacionadas: prefira skill por tarefa | Verificado (V-08) |
| Preferência individual | `CLAUDE.local.md` no `.gitignore` | Com `CLAUDE.local.md` presente, o AGENTS.md deixa de ser lido (ver 2) | Verificado (V-01, V-48) |

Output style: use `keep-coding-instructions: true` quando o estilo é usado dentro de repositório (edita docs e código de exemplo); omita em sessão só de redação; nunca `force-for-plugin` (intrusivo) (C-13, V-08).

## 2. AGENTS.md ou CLAUDE.md

| Cenário | Recomendação |
| --- | --- |
| Só Claude Code, sem outras ferramentas | `CLAUDE.md` |
| Várias ferramentas de agente, sem `CLAUDE.local.md` | `AGENTS.md` como fonte única; Claude Code ≥ 2.1.277 lê sozinho se não houver `CLAUDE.md` |
| Várias ferramentas e `CLAUDE.local.md` em uso | `AGENTS.md` fonte + `CLAUDE.md` com `@AGENTS.md` e extras do Claude |
| Claude Code anterior à 2.1.277 | `CLAUDE.md` com `@AGENTS.md` |

Rótulo: Verificado (V-48, C-02). Reconfirme as versões na instalação do usuário.

## 3. Tamanho da raiz do CLAUDE.md (C-01)

| Fonte | Número |
| --- | --- |
| Doc oficial | alvo abaixo de 200 linhas por arquivo |
| HumanLayer | raiz do autor < 60; "consenso" < 300 (não vale: o oficial é 200) |
| Augment | 100 a 150 no experimento deles |
| agent-md-refactor | < 50 |

Padrão: **200 é o teto**; 100 a 150 é preferência do plugin; raiz mínima com links é estilo, não regra. Inverta quando o projeto tem poucas armadilhas (menos) ou muitos comandos distintos (mais, mas mova detalhe para `agent_docs/`). Para decidir com dados, compare tarefas com e sem a seção (T-11 da lista de ferramentas, só em sandbox). Rótulo: Inferido.

## 4. Gerar o CLAUDE.md com `/init` ou à mão (C-03)

Estudo (preprint) diz que contexto gerado não ajuda em média (V-17); Augment e Osmani ressalvam que ajuda quando não há outra documentação (V-16); o prompt do `/init` pede arquitetura e comandos (V-27). Padrão: gerar apenas com revisão humana; manter comandos e o que exige ler vários arquivos; nada que um `ls` mostre. Se o arquivo já existe, propor diff. Rótulo: Inferido.

## 5. Completude ou economia: dois regimes (C-07)

| Regime | Regra |
| --- | --- |
| Documentação para humanos | Completa na superfície pública (referência cobre 100%; how-tos cobrem as tarefas principais); sem enchimento |
| Arquivos de contexto de agente (CLAUDE.md, AGENTS.md, rules) | Mínimos; só o não descobrível |

O princípio "boil the ocean" do gstack vale para o primeiro regime, nunca para o segundo. Concisão forçada em doc de usuário foi rejeitada (prejudica tutorial e how-to; V-18 e a tabela de rejeitados). Rótulo: Inferido.

## 6. Gerar ou escrever o changelog (C-12)

| Opção | Quando |
| --- | --- |
| Escrito para humanos (Keep a Changelog) | Texto voltado ao usuário (padrão) |
| `release.yml` / notas geradas | Rascunho e lista de PRs; revisar antes de publicar |
| Ferramenta que gera tudo a partir de commits | Só se o time aceita texto de commit como texto de produto; quem corta a versão é `git-workflow-release` |

Rótulo: Inferido (V-13, V-42).

## 7. Mermaid, ASCII ou PlantUML (C-10, C-11)

| Opção | Use quando | Cuidado |
| --- | --- | --- |
| Mermaid | Destino renderiza (GitHub, MkDocs com plugin) | Testar render; C4 e ER são experimentais |
| ASCII | Renderizador não confirmado; diff legível | Não em comentário de API (AIP-192) |
| PlantUML | O projeto já usa | Editar no formato existente; sem migrar nem instalar renderizador sem pedido; "render não verificado" |

Rótulo: Inferido.

## 8. Dialeto de docstring por linguagem (C-06, C-14)

Python: guia do projeto; senão Google com seções nomeadas. TS: TSDoc ou JSDoc conforme as ferramentas que leem os comentários (TSDoc é proposta). Rust: rustdoc com `# Examples`. Java: Javadoc conforme o JDK do projeto. Rótulo: Verificado (V-33 a V-36).

## 9. Fonte única da API

Padrão: contrato versionado (OpenAPI/protobuf) como fonte; descrição escrita nele; anotações no código só se geram o contrato. Se houver duas fontes, checagem de consistência em CI. Inverter: nunca duplicar à mão. Rótulo: Verificado (V-41).

## 10. Links: offline ou online

Offline em todo PR (rápido, determinístico, bloqueia). Online em job agendado (oscila, não bloqueia, abre issue). Inverter só em projeto com poucos links externos críticos. Rótulo: Verificado em parte (V-39; `--offline` via `args` Inferido).

## 11. Correção factual direta ou pergunta (C-08)

| Tipo de mudança | Ação |
| --- | --- |
| Fato derivado do diff (caminho, contagem, nome, referência cruzada, versão) | Aplicar com diff listado ao final |
| Remover conteúdo, mudar narrativa ou filosofia, tocar segurança, reescrever muito, mexer em CHANGELOG ou ADR existente | Perguntar |
| Qualquer arquivo de instrução de agente (CLAUDE.md, AGENTS.md, rules, SKILL.md) | Sempre aprovação |

Rótulo: Inferido (gstack corrige fatos sozinho; auditores V-02 e V-45 pedem aprovação por arquivo).

## 12. Estilo: Vale, output style ou CLAUDE.md

Decisão de prosa em PR: Vale + markdownlint (garantia, objetiva). Tom em sessão de redação: output style `escritor-tecnico` ([template](../assets/templates/output-style-escritor-tecnico.md)). CLAUDE.md: só regras de tom que o linter não captura. Rótulo: Verificado (V-01, V-08, V-37, V-38).

## 13. Hook de lint ou CI

CI é a garantia compartilhada e auditável; hook PostToolUse local dá retorno imediato ao agente, mas executa shell em cada edição e é guardrail, não fronteira de segurança. Padrão: CI; hook só por escolha consciente do usuário ([ferramentas-e-mcp](ferramentas-e-mcp.md), T-12). Formato do hook: Não verificável aqui. Rótulo: Verificado para CI (V-37 a V-39), Não verificável para hook.

## 14. Editar ou criar nova ADR

ADR aceita não é editada: nova ADR cita a anterior, a antiga só recebe a linha de status. Erro de digitação ou link quebrado: edição mínima com aprovação. Inverter: ADR ainda em "proposta" pode ser reescrita. Rótulo: Verificado (V-30).

## 15. Onboarding: tutorial ou how-to

Onboarding é primeiro tutorial (aprender fazendo, resultado visível, trilha única) e depois how-tos por tarefa. Equipe: camadas e passos verificáveis (Suposição, V-47 só cobre contribuidor). Rótulo: Suposição.
