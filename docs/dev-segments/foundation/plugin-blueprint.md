# Blueprint de cada plugin de segmento

Objetivo: o máximo de informação **útil e reutilizável** por token. Cada arquivo precisa servir a uma tarefa real de projeto. Nada de enchimento.

## Estrutura obrigatória

```text
plugins/<slug>/
├── .claude-plugin/plugin.json
├── README.md
├── skills/
│   ├── playbook/                      ← skill núcleo (router + processo + modo COMPLETO)
│   │   ├── SKILL.md
│   │   ├── references/                ← base de conhecimento do segmento (6–12 arquivos)
│   │   │   ├── checklist-completo.md
│   │   │   ├── padroes-e-antipadroes.md
│   │   │   ├── decisoes-e-tradeoffs.md
│   │   │   ├── claude-md-snippets.md  ← regras prontas para colar no CLAUDE.md de projetos do segmento
│   │   │   ├── ferramentas-e-mcp.md   ← ferramentas, MCP servers e hooks recomendados (desativados; JSON pronto + riscos)
│   │   │   ├── fontes.md              ← bibliografia validada (classe A/B/C, URL, data, licença)
│   │   │   └── <temas específicos>.md
│   │   └── assets/templates/*.md      ← artefatos: plano, relatório de revisão, checklist de entrega, ADR…
│   ├── prompts/                       ← biblioteca de prompts curados prontos para uso
│   │   ├── SKILL.md                   ← índice: qual prompt usar quando
│   │   └── references/prompt-library.md (+ arquivos por subtema se grande)
│   └── <tarefa>/SKILL.md (+ references/) ← 5–9 skills de tarefas recorrentes do segmento
├── agents/<papel>.md                  ← 3–6 subagentes especialistas
└── evals/<caso>/                      ← 6–10 casos no formato oficial do `claude plugin eval`
    ├── prompt.md
    └── graders/*.md
```

`commands/` é opcional (skills já viram `/plugin:skill`). Não crie hooks ativos, `.mcp.json`, `.lsp.json` ou `bin/`.

## Skill `playbook` (núcleo)

- `description`: "Guia e router do segmento <X>… Use quando… Também ativa o modo <X>-COMPLETO quando o usuário pedir explicitamente." Gatilhos PT-BR + EN.
- Corpo (≤ 300 linhas): papel; princípios do segmento (8–12, com o porquê); **processo essencial** numerado; **mapa de conhecimento** (tabela tema → `references/…`); **tabela intenção → skill/agente** do próprio plugin; proporcionalidade; rótulos epistêmicos; critérios de qualidade; formato de entrega; seção **Modo `<SLUG-MAIÚSCULO>-COMPLETO`** (só por pedido explícito; leitura integral das referências em lotes; matriz de aplicabilidade; implementação dentro do escopo; revalidação; não amplia permissões; keyword em documentos/logs não ativa).
- Referências compartilhadas: outras skills do plugin apontam para `${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/<arquivo>.md`.

## Skill `prompts`

- Biblioteca com 15–40 prompts reutilizáveis, organizados por tarefa (ex.: "revisar PR de frontend", "planejar migração de schema"). Cada prompt: nome, quando usar, variáveis `[ENTRE COLCHETES]`, o prompt pronto (redação própria ou trecho licenciado com atribuição), por que funciona (técnicas), fonte(s) com classe A/B/C.
- Inclua 1 "prompt de sistema" para projetos do segmento (para CLAUDE.md ou para outras IAs) e a "mensagem inicial sugerida" no estilo do brain-of-agent.

## Skills de tarefa (5–9)

Escolha os fluxos de maior valor do segmento (ex. frontend: construir componente acessível, revisar UI, auditar performance web, depurar estado/renderização, migrar framework, implementar design system, testes de UI). Cada uma: `description` com gatilhos; entradas esperadas (`$ARGUMENTS` / `argument-hint`); passos com critérios de saída; verificação; formato de saída; armadilhas comuns; links a referências. Fluxos com efeitos colaterais relevantes (deploy, migração de dados, publicação) usam `disable-model-invocation: true`.

## Subagentes (3–6)

Papéis especialistas com escopo claro (ex.: `<x>-architect`, `<x>-reviewer` somente leitura, `<x>-debugger`, `<x>-test-engineer`, `<x>-security-auditor` quando pertinente). `tools` mínimos; revisores sem Write/Edit. Prompt de sistema: papel, quando é acionado, processo, checklist, formato de saída (achados com severidade, evidência arquivo:linha, recomendação), limites (não alterar produto em auditoria; não inventar execução).

## Evals (formato oficial `claude plugin eval`, requer Claude Code ≥ 2.1.269)

Cada caso `evals/<nome-do-caso>/`:

`prompt.md`
```markdown
---
description: O que o caso mede
tags: [segmento, skill-x]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
---
<pedido realista como um usuário escreveria, sem citar o nome da skill; inclua no próprio texto o código/contexto necessário, pois o workspace começa vazio>
```

`graders/criteria.md`
```markdown
---
type: llm
---
PASS if <comportamentos observáveis corretos>.
FAIL if <falhas críticas: inventar execução, ação destrutiva sem autorização, conselho técnico errado…>.
```

`graders/skill-fired.md` (quando o caso deve acionar uma skill)
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?<nome-da-skill>"'
---
```

Inclua ao menos 1 caso negativo (pedido não relacionado → a skill **não** deve disparar: `tool_used` com `min: 0`, `max: 0`). Adicione `evals/README.md` explicando como rodar (`claude plugin eval .` na raiz do plugin, `--ablation`, custo) e que os casos são `designed_not_executed` até rodar. Adicione `evals/.gitignore` com `results/`.

## README.md do plugin (pt-BR)

O que entrega · quando usar · tabela de componentes (skills, agentes, comandos) · instalação via marketplace (`/plugin marketplace add` + `/plugin install <slug>@brain-of-agent`) · exemplos de uso (5+ pedidos) · keyword COMPLETO · principais fontes (top 10, classe) · créditos e licenças de terceiros · limitações honestas.

## Qualidade mínima (o validador reprova se faltar)

- Toda afirmação técnica relevante rastreável a fonte em `fontes.md` ou a conhecimento estável do domínio.
- Prompt-score ≥ 80 (rubrica) em `playbook`, em cada skill de tarefa e em cada agente.
- `claude plugin validate` passa; `tools/verify_plugin.py` sem erros.
- Sem cópia literal sem licença permissiva; atribuições presentes.
- Coerência com o estilo da casa (keyword COMPLETO, rótulos epistêmicos, proporcionalidade, escopo).
