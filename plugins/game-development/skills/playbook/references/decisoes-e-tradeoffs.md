# Decisões e trade-offs

Base: V-05, V-12, V-14, V-16, V-18, V-22, V-24, V-35 (2026-10-10). Formato: critério para decidir, padrão do plugin e quando mudar. Decisão material vira ADR curto (`assets/templates/adr-tecnico.md`); o plugin propõe 2 a 3 opções e espera o responsável decidir (V-22).

## Sumário

- [GDScript x C# x GDExtension](#gdscript-x-c-x-gdextension)
- [Awaitable x UniTask](#awaitable-x-unitask)
- [Harness completo x execução solo](#harness-completo-x-execução-solo)
- [Perguntar x executar](#perguntar-x-executar)
- [Passo fixo x passo variável](#passo-fixo-x-passo-variável)
- [Headless x jogar](#headless-x-jogar)
- [Instalar x destilar catálogo de terceiros](#instalar-x-destilar-catálogo-de-terceiros)
- [ScriptableObject x singleton](#scriptableobject-x-singleton)
- [Framework de teste](#framework-de-teste)
- [Hook x instrução](#hook-x-instrução)
- [Modelo do revisor](#modelo-do-revisor)

## GDScript x C# x GDExtension

Fonte: padrão do agente `game-engine-specialist` (V-24, Donchitos MIT, redação própria). O guia compara por **custo de build, desempenho e integração com o editor**; nenhum benchmark foi validado neste plugin, então os números ficam com o projeto.

| Opção | Custo de build | Desempenho | Integração com o editor | Use quando |
| --- | --- | --- | --- | --- |
| GDScript | nenhum passo de compilação separado | adequado à maioria da lógica de gameplay (Suposição; meça) | máxima | padrão para gameplay, protótipo, UI |
| C# (Godot .NET) | build do .NET; exige build de engine com .NET | melhor em laços numéricos pesados (Suposição; meça) | boa | equipe C#, bibliotecas .NET, código compartilhado |
| GDExtension (C++ etc.) | toolchain nativo por plataforma | máximo | menor (recompilar e recarregar) | hot path medido no profiler, biblioteca nativa |

Padrão: GDScript tipado; mude de linguagem só com hotspot confirmado no profiler. Rótulo: Inferido (critérios do V-24; classificação de desempenho é Suposição).

## Awaitable x UniTask

Conflito K1 (V-16): o manual oficial 6000.0 recomenda `Awaitable` no lugar de `Task`; a comunidade usa UniTask. Padrão: `Awaitable`. UniTask só se o projeto já o usa (não migre por gosto). Em 2022 LTS confirme a disponibilidade e as APIs. Nunca `Task.Result`/`Wait()` na thread principal.

## Harness completo x execução solo

Fonte: V-05 (relato do autor em app web, não de jogos): solo cerca de US$ 9; harness completo cerca de US$ 200; versão atualizada US$ 124,70; com o Opus 4.6 ele removeu o sprint e passou a rodar o avaliador uma vez no fim. Decida por:

| Situação | Escolha |
| --- | --- |
| pergunta pontual, correção localizada, mudança trivial | solo, sem avaliador |
| funcionalidade média | solo + `game-verify-by-running`; revisor `gameplay-reviewer` (barato, somente leitura) |
| funcionalidade difícil ou de alto risco, fim do trabalho, ou pedido do usuário | avaliador cético `game-evaluator` uma vez no fim |
| projeto de várias sessões | `features.json` + progresso (V-04); avaliador só nas funcionalidades difíceis |

Custos são relatos de um autor em outro domínio; use como ordem de grandeza.

## Perguntar x executar

Conflito K2: o protocolo "perguntar, propor, esperar, rascunho, gravar" (V-22, V-23) reduz autonomia. Padrão em duas velocidades: **design, arquitetura e mudança multiarquivo** = proposta e aprovação antes de gravar; **tarefa mecânica e delimitada** (renomear, formatar, aplicar uma regra de estilo) = executar. Pergunta sem resposta não é permissão. Commit só se o usuário pedir.

## Passo fixo x passo variável

| Critério | Passo fixo (acumulador) | Passo variável (`delta` direto) |
| --- | --- | --- |
| Determinismo, replay, lockstep | exige | inviável |
| Física estável com quadros longos | sim (com teto) | instável |
| Custo | mais código; interpolação para suavizar | simples |
| Use quando | física, colisão, lógica de simulação | efeitos visuais, UI, câmera suave |

Padrão: fixo para simulação e física, variável para visual (V-14). Engines já fazem isso (Godot: `_physics_process`); só reimplemente em engine própria ou jogo web.

## Headless x jogar

| Critério | Headless/sondas | Humano joga |
| --- | --- | --- |
| Sintaxe, import, regressão de lógica, valores internos | sim | caro e inconsistente |
| Sensação, áudio, legibilidade, "parece certo" | não prova (V-12, V-30) | único meio |
| Custo por iteração | baixo | alto |

Padrão: headless e sondas em toda iteração; humano antes de fechar marco. Conflito K4: o agente julga itens objetivos do contrato; o restante é NÃO AVALIADO.

## Instalar x destilar catálogo de terceiros

| Opção | Risco | Decisão do plugin |
| --- | --- | --- |
| Instalar catálogos (Donchitos: 12 hooks automáticos; GodotPrompter: hook SessionStart; cc-godot: hook e `.mcp.json`; GD-Agentic: `npx`, LGPL-3.0; godogen: chaves pagas, instalação de pacotes) | execução automática de código, injeção, supply chain | não instalar |
| Ler e destilar o padrão com redação própria | baixo | padrão do plugin |
| Usar como índice de domínios | baixo | permitido (V-35) |

Estrelas não entram na decisão técnica (K10): só licença, manutenção e leitura do conteúdo. Ao propor instalar algo, descreva ganho e risco e espere o "sim" do usuário no chat.

## ScriptableObject x singleton

Fonte V-18 (jan/2020, classe B; conferir contra a documentação atual). ScriptableObject para estado compartilhado e eventos: testável, cenas independentes, valor inicial separado do de runtime. Singleton: simples, acopla cenas e dificulta teste. Projeto pequeno pode dispensar o padrão (Inferido). Padrão: ScriptableObject para dados e eventos; singleton só para serviço global único e justificado.

## Framework de teste

Godot: GUT (MIT, Godot 4) ou GdUnit4: **um só** (V-12, V-32). Unity: Test Framework 1.4 (EditMode para lógica pura, PlayMode para ciclo de vida) (V-21). Unreal: o que o projeto fixar (sem fonte validada).

## Hook x instrução

Instrução em CLAUDE.md é pedido; hook ou permissão é garantia (V-01, V-02). O que deve valer sempre (não editar `.godot/`, `Library/`) pode virar hook do **projeto do usuário**, documentado em `ferramentas-e-mcp.md`, desativado aqui. Hook é guardrail, não fronteira de segurança.

## Modelo do revisor

`gameplay-reviewer` usa `model: inherit`; `haiku` como opção de custo é Inferido e deve ser validado com avaliações (V-03, V-06). Revisão do mesmo modelo não é validação externa: declare.
