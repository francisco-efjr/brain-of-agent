# dev-segments: fábrica dos plugins por segmento

Esta pasta registra como os plugins de `plugins/` foram produzidos e como reproduzir o processo. Para usar os plugins, comece pelo [ORCHESTRATOR.md](../../ORCHESTRATOR.md) da raiz e pelo [catálogo](CATALOGO.md).

## Como foi feito (resumo)

1. **Base compartilhada** (`foundation/`): especificação de plugin do Claude Code conferida na documentação oficial, blueprint de plugin, rubrica de qualidade de prompt (12 dimensões), rubrica de fonte (A/B/C), estilo da casa herdado do brain-of-agent e lista de 25 segmentos (`segments.json`).
2. **Atlas global** (`research/_global/*.validated.md`): corpus oficial da Anthropic, ecossistema do Claude Code, regras de outras ferramentas (Cursor, Copilot, AGENTS.md), cânone de engenharia de prompt, pulso da comunidade e o próprio brain-of-agent. Cada tópico passou por um validador independente. Daí saíram `foundation/prompt-principles.md` e as pistas por segmento (`research/<segmento>/_leads.md`).
3. **Pesquisa por segmento:** 3 lentes (autoridade, GitHub e comunidade/redes sociais) com pesquisadores em Haiku 5.5. Um validador independente em Sonnet 5.5 reverifica as URLs, pontua os prompts e rejeita o que não se sustenta (`VALIDATED.md`). Quando havia lacunas, rodou uma etapa de complemento.
4. **Síntese e crítica:** desenho do plugin (`SYNTHESIS.md`) em Sonnet 5.5 e um crítico independente em Opus 5.5.
5. **Construção:** 3 construtores em paralelo (Sonnet 5.5), validador estrutural (`verify_plugin.py` + `claude plugin validate`), validador independente de qualidade de prompt e conteúdo técnico (Opus 5.5, ou Sonnet 5.5 nos segmentos de nicho) e um gate final (`BUILD-REPORT.md`).
6. **Teste real:** o plugin architecture-design foi aplicado a um app Android e as lições voltaram para o construtor: contrato de entrega coerente com as ferramentas, modo sem interação e cobertura de plataforma.

A primeira tentativa usou o modelo mais caro em todos os agentes e esgotou a janela de uso. Por isso o processo final usa modelos por camada e roda em lotes, com um disjuntor que interrompe o lote quando os agentes começam a falhar.

## Reproduzir ou adicionar um segmento

- Os scripts de orquestração ficam em `tools/dev-segments/workflows/`. `research-v2.js` cobre atlas e segmentos; `build-v2.js` cobre plugins, integração e contexto. Os dois rodam com a ferramenta Workflow do Claude Code, com `args` `{root, date, mode, segments, only}`.
- Eles esperam a estrutura de fábrica `<root>/docs/foundation`, `<root>/docs/research`, `<root>/plugins` e `<root>/tools/verify_plugin.py`. Para recriá-la, copie `docs/dev-segments/foundation` → `<root>/docs/foundation` e `docs/dev-segments/research` → `<root>/docs/research`.
- Verificação estrutural de qualquer plugin: `python tools/dev-segments/verify_plugin.py plugins/<slug>`.

## Limites honestos

- A validação foi feita por modelos de IA, com modelo diferente do autor sempre que possível. Não houve revisão humana.
- Os evals dos plugins estão em `designed_not_executed`. `claude plugin eval` exige Claude Code 2.1.269 ou superior.
- As fontes são mutáveis. As datas de consulta estão em cada `VALIDATED.md` e em `fontes.md`.
- A pesquisa bruta, sem validação, não foi publicada, porque pode conter trechos sem licença verificada.
