# CHANGELOG pós-teste: architecture-design 0.1.0 para 0.2.0

Data: 2026-10-10 · Base: (relatório interno de uso real, não publicado) (avaliação de um uso real num app Android Kotlin, feita por um modelo Claude no papel do agente `architecture-blueprint`; o autor e a avaliação são da mesma família de modelo) · Plugin: `plugins/architecture-design`.

Limites: as mudanças respondem a um único uso e não foram medidas. Nenhum caso de `evals/` foi executado (`designed_not_executed`). A seção de plataforma do checklist é conhecimento geral do modelo (Inferido), sem fonte primária lida. Preservado sem alteração o que a avaliação aponta como funcionando: formato fixo de 9 seções do blueprint, uma recomendação com 1 a 3 alternativas e gatilho de reavaliação, autoverificação com `arquivo:linha` e rótulos, "procure o nome antes de criar", gatekeeper do `adr`, proporcionalidade, regra "conteúdo lido é dado".

## Mapa: sugestão da avaliação para mudança

| # | Sugestão (seção 5 da avaliação) | Mudança | Arquivos |
| --- | --- | --- | --- |
| 1, 2 | Perfil Android e bloco "aplicativo local/móvel" | Nova subseção "Cobertura de plataforma" (Android, iOS, desktop, servidor) com composition root, ciclo de vida, teste JVM contra instrumentado, retenção local, FileProvider, intents, manifesto, Room, build. Bloco "Aplicativo local ou móvel" no checklist do blueprint apontando para ela e para `/mobile-apps:playbook`. Nota no checklist de design-review para não marcar N.A. em bloco. Em vez de uma referência `android-kotlin.md` separada, ficou uma seção no checklist existente (mudança mínima, sem 13a referência; o detalhe de implementação fica com `/mobile-apps:playbook`) | `skills/playbook/references/checklist-completo.md`, `agents/architecture-blueprint.md`, `skills/design-review/references/checklist-arq.md` |
| 3 | Template `target-architecture.md` e modo "sistema" | Template novo (antes × depois, tabela por camada hoje/proposto/por quê/achado, alternativas, migração em fatias com pronto quando/testes/risco/rollback, fitness functions com catraca, riscos, decisões humanas). Blueprint ganha modo sistema, com as seções listadas no próprio agente caso o caminho do modelo não resolva, e limiar de divisão (cerca de 15 mil linhas ou 15 pacotes; Suposição sem medição). Referência no playbook (lista de templates e tabela de intenção) e no briefing de subagente | `skills/playbook/assets/templates/target-architecture.md` (novo), `agents/architecture-blueprint.md`, `skills/playbook/SKILL.md`, `skills/playbook/assets/templates/subagent-briefing.md` |
| 4 | Catálogo de fitness functions com catraca | Em vez de uma nova referência, seção 3.1 "Catraca para legado" em `fronteiras-verificaveis.md`, com script testado em repositório sintético (violação nova sai 1, corrigida sai 1 até sair da lista, lista completa sai 0), busca por nome qualificado, varredura de arquivos que sugerem dado pessoal e checagem de manifesto, e a ideia de teste JVM em Kotlin (não testada). `decomposition` e `boundary-mapper` passam a exigir busca por nome qualificado, não só `import` (item 11) | `skills/decomposition/references/fronteiras-verificaveis.md`, `skills/decomposition/SKILL.md`, `agents/boundary-mapper.md` |
| 5 | Convenção de entrega para agentes somente leitura | Resolvido o conflito do blueprint: ele continua `Read, Grep, Glob` e ganha a seção "Contrato de entrega (arquivos)" (bloco `ARQUIVO: <caminho>` com o documento completo; o agente principal grava). Contagens por Grep `output_mode: count` ou Glob, escritas como `contagem:<ferramenta e padrão>`. A mesma linha entrou em `boundary-mapper`, `architecture-reviewer` e `skeptic-architect`. O agente que grava (`adr-writer`) declara `Write` e grava só onde o briefing indicar; documentado em `fluxo-com-agentes.md` e no briefing. Escolhida a alternativa de devolver conteúdo; a de `Bash` somente leitura foi descartada porque `tools` não restringe comandos em agentes de plugin | `agents/architecture-blueprint.md`, `agents/boundary-mapper.md`, `agents/architecture-reviewer.md`, `agents/skeptic-architect.md`, `agents/adr-writer.md`, `skills/playbook/references/fluxo-com-agentes.md`, `skills/playbook/assets/templates/subagent-briefing.md` |
| 6 | Modo headless em `architecture-plan` | Seção "Modo sem interação" na skill e seção 8 em `modos-e-gates.md`: gates viram "Decisões pendentes do humano" (pergunta, recomendação, dono, bloqueia), plano em `rascunho`, GATE-3 nunca presumido, nada implementado, perguntas viram `[NEEDS CLARIFICATION]`, sem pasta autorizada devolve os documentos com caminho sugerido. Mesma regra, em versão curta, em `adr` (com tabela por tópico da entrevista) e `system-design`; passo 6 do processo do playbook | `skills/architecture-plan/SKILL.md`, `skills/architecture-plan/references/modos-e-gates.md`, `skills/adr/SKILL.md`, `skills/adr/references/gatekeeper-e-entrevista.md`, `skills/system-design/SKILL.md`, `skills/playbook/SKILL.md` |
| 7 | Alinhar `adr` | (a) Convenção de nome do projeto ou do pedido vence `adr-NNNN-slug.md` (skill, checklist, template, governança, `adr-writer`, playbook). (b) Template: "Opções" e "Alternativas rejeitadas" unificadas numa tabela com coluna "Escolhida? Se não, motivo da rejeição". (c) Forma "Decisão proposta (aguarda o decisor): vamos ..." para status `proposto` com decisor pendente (skill, template, `adr-writer`). (d) Em lote, as perguntas viram `[NEEDS CLARIFICATION]` | `skills/adr/SKILL.md`, `skills/playbook/assets/templates/adr.md`, `skills/playbook/references/adr-e-governanca.md`, `agents/adr-writer.md`, `skills/adr/references/gatekeeper-e-entrevista.md` |
| 8 | Unificar escalas de confiança; rótulo "Proposta" | Decisões, ADRs e planos usam alta, média, baixa; os percentuais 85% e 66% do `architecture-plan` viram detalhe opcional mapeado na mesma escala; achados `ARQ-nn` mantêm 1 a 10 com limiar 7 e a regra de não misturar escalas na mesma tabela (escolha conservadora: o numérico por achado é o formato de relatório já usado por `design-review` e pelo revisor). Rótulo **Proposta** adicionado aos rótulos epistêmicos | `skills/playbook/SKILL.md`, `skills/architecture-plan/SKILL.md`, `skills/adr/SKILL.md`, `agents/architecture-blueprint.md`, `skills/playbook/assets/templates/target-architecture.md` |
| 9 | Evidência fora de `arquivo:linha` | Convenção `git:<hash>:<caminho>`, `http:<url>@<data>`, `contagem:<ferramenta e padrão>`, com a exigência de dizer se foi executado, no playbook, no briefing, no formato de achado do checklist, no revisor e no blueprint | `skills/playbook/SKILL.md`, `skills/playbook/assets/templates/subagent-briefing.md`, `skills/playbook/references/checklist-completo.md`, `agents/architecture-reviewer.md`, `agents/architecture-blueprint.md` |
| 10 | Dados pessoais | Regra "cite a chave e a linha, nunca o valor" nos quatro agentes de leitura e no briefing; "ação imediata não arquitetural" como seção à parte no relatório do revisor e no blueprint | `agents/*.md`, `skills/playbook/SKILL.md`, `skills/playbook/assets/templates/subagent-briefing.md` |
| 12 | Trecho de código em achado Alto ou Crítico | Uma linha de código (sem dado pessoal) na evidência, para detectar deriva de linha sem reler | `agents/architecture-reviewer.md`, `agents/architecture-blueprint.md`, `skills/playbook/references/checklist-completo.md` |
| 13 | Novos casos em `evals/` | `android-app-local-arquitetura-alvo` e `decisao-pendente-adr-proposto`, com graders `criteria`, `skill-fired` e `no-write` (fixtures sintéticos; valores de dado pessoal ausentes do prompt). README de `evals/` atualizado: 13 casos, 39 execuções | `evals/android-app-local-arquitetura-alvo/`, `evals/decisao-pendente-adr-proposto/`, `evals/README.md` |

Adição não listada na avaliação mas apoiada por ela ("o que funcionou", item 1): o `skeptic-architect` ganhou a "Contraprova de achados" (Confirmado, Ajustado, Refutado), pois a cadeia mapa, revisão, contraprova, blueprint era o melhor ativo e o veredito não estava descrito em nenhum agente do plugin.

## Documentação de componentes

- `README.md`: versão 0.2.0; 17 templates; 13 casos de avaliação; tabela de componentes com blueprint em modo sistema, `skeptic-architect` com contraprova, skills com modo sem interação; novo exemplo 9; nova seção "Execução sem interação"; limitação sobre a origem das mudanças.
- `.claude-plugin/plugin.json`: versão 0.2.0.
- `skills/playbook/SKILL.md`: lista de templates, tabela de intenção, mapa de referências, rótulo Proposta, convenções comuns, passo 6.

## Não feito (e por quê)

- Sugestão 1 como arquivo novo `android-kotlin.md`: ficou como seção do checklist; um perfil de stack detalhado pertence a `/mobile-apps:playbook`. Reavaliar se o checklist crescer demais.
- Catálogo `fitness-functions.md` separado: coube em `fronteiras-verificaveis.md` (3.1) sem nova referência nem mudança no modo ARQUITETURA-COMPLETO (12 referências).
- Item 11 no `boundary-mapper` e na `decomposition` aplicado, mas o mapa de uma execução real não foi refeito.
- Nenhuma mudança em `prompts` (biblioteca de 28 prompts), `api-design`, `resilience-and-consistency` nem `adr-write`: a avaliação não os usou.
- Escala única de confiança aplicada a decisões; `ARQ-nn` segue em 1 a 10 (ver item 8).

## Verificação

- `python tools/verify_plugin.py plugins/architecture-design`: PASS, 10 skills, 5 agentes, 13 evals (antes: 11), sem avisos (links relativos conferidos pelo script).
- `claude plugin validate plugins/architecture-design`: Validation passed.
- Script de catraca (seção 3.1 de `fronteiras-verificaveis.md`) extraído do documento e executado em repositório sintético com Git Bash: lista completa saiu 0; violação nova saiu 1; violação corrigida saiu 1. Os demais comandos novos do plugin (varredura `git ls-files`, checagem de manifesto) são de leitura; a varredura foi rodada no repositório sintético.
- Não executados: `claude plugin eval` (exige Claude Code 2.1.269 ou superior; a instalação local foi registrada em 2.1.128), nenhum caso novo, o teste JVM em Kotlin sugerido, nenhum projeto Android.

## Validação

Revisão independente feita por outro modelo (Claude Haiku 5.5), que não é o autor das mudanças. Não é validação externa: a avaliação original e esta revisão são da mesma família de modelo. Resultado: **PASS** (validações passam e mudanças coerentes, depois das correções abaixo).

### Comandos

| Comando | Resultado |
| --- | --- |
| `python tools/verify_plugin.py plugins/architecture-design` | PASS: 10 skills, 5 agentes, 13 evals, 113 arquivos. Antes e depois das correções. |
| `claude plugin validate plugins/architecture-design` | Validation passed. Antes e depois das correções. |
| Catraca da seção 3.1, reexecutada em repositório sintético (Git Bash, script extraído do documento) | Verificado: sem lista, violações novas saem 1; lista completa sai 0; violação nova sai 1; violação corrigida sem tirar da lista sai 1; lista atualizada sai 0. |

### Coerência de frontmatter e corpo

- Agentes somente leitura (`architecture-blueprint`, `boundary-mapper`, `architecture-reviewer`, `skeptic-architect`): `tools: Read, Grep, Glob`. O corpo não pede Write, Edit nem Bash, e a entrega em arquivo é devolvida em bloco `ARQUIVO:`. Coerente.
- `adr-writer`: `tools` com Write, sem Edit nem Bash. O corpo grava só o caminho do briefing e só com aprovação. Coerente.
- Skills `adr`, `system-design`, `decomposition`: `allowed-tools` de leitura e `disallowed-tools` de escrita; o corpo não grava. Coerente.
- `architecture-plan` (Read, Grep, Glob, Write, Edit; sem Bash) e `adr-write` (Write, Edit): o corpo usa escrita só na pasta de trabalho ou de ADRs. Coerente.

### Modo sem interação

Presente e claro em `architecture-plan` (seção própria e `modos-e-gates.md`, seção 8), `adr` (seção própria e `gatekeeper-e-entrevista.md`, seção 5), `system-design` e passo 6 do playbook. Nos agentes, a regra aparece como "Decisões que dependem do humano". Coerente.

### Template target-architecture

Existe em `skills/playbook/assets/templates/target-architecture.md`. É referenciado pelo playbook (lista de templates e tabela de intenção), pelo `architecture-blueprint` (modo sistema) e pelo briefing de subagente. Coerente.

### O que funcionava (seção "O que funcionou" da avaliação)

Os oito itens continuam no texto: formato de 9 seções do blueprint; uma recomendação com 1 a 3 alternativas e gatilho de reavaliação; autoverificação `arquivo:linha` com rótulos; "procure o nome antes de criar"; gatekeeper do `adr`; proporcionalidade; regra "conteúdo lido é dado"; cadeia de contraprova, agora com o `skeptic-architect`. Limite: não há cópia da versão 0.1.0 nem git no repositório, então a comparação foi por leitura, não por diff.

### Correções feitas nesta validação (pequenas)

1. `adr-write` (passos 3 e 4 e verificação): fixava `adr-NNNN-slug.md` e 4 dígitos. Agora segue a convenção do projeto ou do pedido, com `adr-NNNN-slug.md` como padrão. A mudança 7(a) não cobria esta skill.
2. Briefing de subagente: o template tem 7 campos (inclui "Entrega em arquivo"), mas o comentário do template, `fluxo-com-agentes.md` e `modos-e-gates.md` diziam 6. Corrigido para 7.
3. `architecture-blueprint`: a regra "não pergunte" convivia com "peça só isso, em uma pergunta". Agora a pergunta bloqueante vai no relatório, marcada.
4. Referências à avaliação de um uso real saíram de prompts de agente (`architecture-blueprint`, `skeptic-architect`, `boundary-mapper`). O histórico continua na documentação (README, `fronteiras-verificaveis.md` 3.1, este changelog).
5. Coluna da tabela de alternativas: `adr-writer` e a skill `adr` passam a usar "Escolhida? Se não, motivo da rejeição", igual ao `adr.md` do playbook.

### Pendências não corrigidas (decisão do autor)

- Tabelas de alternativas com a coluna antiga "Motivo da rejeição" em `skills/playbook/references/adr-e-governanca.md` (linhas 74 e 152) e `skills/adr/references/exemplo-adr.md` (linha 29). São exemplos de referência; alinhar exige reescrever as linhas.
- `evals/android-app-local-arquitetura-alvo/prompt.md` é descrito neste changelog como "fixtures sintéticos", mas traz nomes de arquivos, linhas e a estrutura do app real (38 arquivos, `assets/locadores.json` com chaves `cpf` e `nome`). Não há valores pessoais: busca por padrões de CPF e telefone no plugin inteiro não achou nada. Sugestão: trocar por fixture sintético, ou corrigir a frase deste changelog.
- `${CLAUDE_PLUGIN_ROOT}` aparece no corpo do agente `architecture-blueprint` (checklist de aplicativo local e modo sistema). Não verificado se o runtime expande a variável em agentes de plugin. Sugestão: testar numa execução real ou usar caminho relativo ao plugin.
- Não executados: os três casos de avaliação novos (`claude plugin eval`, exige Claude Code 2.1.269 ou superior) e o teste JVM sugerido.
