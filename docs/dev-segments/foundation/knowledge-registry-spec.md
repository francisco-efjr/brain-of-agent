# Registro de conhecimento por tag (knowledge registry)

Criado em 2026-10-13 (item 33 do plano). Objetivo: **cada conhecimento adquirido pelo brain-of-agent tem uma tag**, e o orquestrador usa as tags para casar a demanda do usuário ("edição de vídeo", "escreva a spec antes", "teste funcionalidade por funcionalidade") com o plugin, as skills e o agente que carregam aquele know-how, mais o validador independente.

Pensado para **várias sessões publicando em paralelo**: nenhum arquivo compartilhado é editado à mão. Cada tag é um arquivo; o índice é gerado.

## 1. Onde fica o quê

| Caminho | O que é | Quem escreve |
| --- | --- | --- |
| `docs/foundation/knowledge/<tag>.json` (fábrica) | **Uma tag por arquivo.** Curada: gatilhos em PT-BR e EN e rotas para um ou mais plugins | A sessão que adquire o conhecimento (aditivo; não edite a tag de outra sessão sem motivo) |
| `plugins/<slug>/.claude-plugin/plugin.json`, campo `keywords` | Vocabulário de gatilho da **tag automática** do plugin | O construtor do plugin |
| `docs/dev-segments/knowledge.json` e `KNOWLEDGE.md` (brain) | Índice gerado: tags curadas + uma tag automática por plugin publicado | `tools/publish_brain.py` (nunca à mão) |
| `plugins/orchestrator/skills/playbook/references/conhecimento.md` | Cópia do índice dentro do plugin orquestrador | `tools/publish_brain.py` |
| `docs/research/<slug>/PUBLISH.json` (fábrica) | Sidecar de publicação do plugin: `mode_keyword` e, se não for o padrão, `validation_report` | A sessão do plugin (alternativa a editar `EXTRA_PLUGINS` no script) |

## 2. Esquema de `<tag>.json`

```json
{
  "tag": "video-edicao",
  "label": "Edição e produção de vídeo com código",
  "description": "Uma ou duas frases: que conhecimento é este e que resultado entrega.",
  "triggers": ["edição de vídeo", "editar vídeo", "renderizar vídeo", "video editing", "hyperframes"],
  "routes": [
    { "plugin": "video-hyperframes", "skills": ["playbook"], "agents": [], "role": "lider" },
    { "plugin": "design-engineering-kit", "skills": ["animate"], "agents": ["motion-polish-reviewer"], "role": "apoio" }
  ],
  "validators": ["qa-testing:test-auditor"],
  "sources": ["docs/dev-segments/research/video-hyperframes/VALIDATED.md"],
  "notes": "Texto livre opcional: pré-requisitos, limites, decisões."
}
```

Regras:
- `tag`: kebab-case em PT-BR, igual ao nome do arquivo, curta e estável. Prefira o tema (`tdd`) ao nome da ferramenta, salvo quando a ferramenta é o conhecimento (`playwright`).
- `triggers`: 6 a 15 frases que o usuário realmente diria, em PT-BR e EN, em minúsculas. É por elas que o orquestrador acha a tag. Inclua sinônimos e a keyword `*-COMPLETO` do plugin quando houver.
- `routes[].role`: `lider` (o especialista principal; só um por tag), `fundamentos` (know-how que o subagente deve carregar junto, por exemplo a skill vendorizada do agent-skills) ou `apoio` (entra se o contexto pedir).
- `routes[].skills` e `routes[].agents`: nomes simples; o gerador prefixa o plugin e **avisa** se não existirem no plugin publicado. `playbook` sempre existe.
- `validators`: `plugin:agente` do validador independente (outro papel; se possível outro modelo).
- Rota para plugin **ainda não publicado** é permitida: aparece como "em construção" e vira "publicado" sozinha quando o plugin entrar no brain. Plugin desconhecido (não é segmento, não tem pasta, não tem sidecar) gera aviso.

## 3. Tag automática por plugin

Para cada plugin publicado (menos `orchestrator`), o gerador cria a tag `<slug>` com `label` igual ao `displayName`, `triggers` iguais aos `keywords` do `plugin.json` mais a keyword de modo completo, e uma rota `lider` para `<slug>` (`playbook` + todos os agentes). Se existir uma tag curada com o mesmo nome do slug, a curada manda e os `keywords` são **acrescentados** aos gatilhos dela.

Consequência: um plugin novo entra no registro **sem nenhuma ação** além de ter bons `keywords`. A tag curada é o passo seguinte, para gatilhos em linguagem de usuário e rotas cruzadas.

## 4. Como o orquestrador usa (ORCHESTRATOR.md §3, passo 3)

1. Case a demanda com os `triggers` (sinônimos, PT-BR ou EN). Pode casar mais de uma tag.
2. Para cada tag: o especialista vem da rota `lider`; o subagente recebe também as skills das rotas `fundamentos`; `apoio` entra se o contexto pedir; o validador vem de `validators`.
3. Tag "em construção": declare a lacuna e use a rota publicada mais próxima (ou o catálogo).
4. Sem tag casando: use o catálogo (`CATALOGO.md`) e a tabela de combinações do §4. Registre a lacuna no relatório; é sinal de que falta uma tag.

## 5. Sidecar `PUBLISH.json`

```json
{ "mode_keyword": "LIFECYCLE-COMPLETO", "validation_report": "docs/research/engineering-lifecycle/BUILD-REPORT-quality.md" }
```

`validation_report` é opcional (padrão: `docs/research/<slug>/BUILD-REPORT-quality.md`). O script continua aceitando `EXTRA_PLUGINS`; o sidecar só evita edição concorrente do script por sessões paralelas.

## 6. Checklist para quem adquire um conhecimento novo

1. Plugin com `keywords` bons no `plugin.json` (vira a tag automática).
2. `docs/research/<slug>/PUBLISH.json` com `mode_keyword`.
3. Uma ou mais tags curadas em `docs/foundation/knowledge/`, com gatilhos em linguagem de usuário e rotas cruzadas para plugins existentes.
4. `python tools/publish_brain.py <brain>`; conferir o `KNOWLEDGE.md` gerado (status, avisos de skill ou agente inexistente).
5. Pull com rebase no brain antes do commit: outras sessões também publicam, e o gerador regenera o índice a partir do estado de **todas** as tags em disco.
