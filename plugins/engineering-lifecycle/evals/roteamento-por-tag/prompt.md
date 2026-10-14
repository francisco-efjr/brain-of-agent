---
name: roteamento-por-tag
description: "Caso de roteamento por tag do registro de conhecimento, com os três desempates do VALIDATED: 'testar no navegador' vai para testes-funcionais-playwright, 'tem erro no console' vai para ui-producao e 'refatora sem mudar comportamento' vai para simplificar-codigo, não para revisao-de-codigo. O trecho do registro vem no prompt porque o workspace começa vazio. Mede se o modelo diz tag principal, líder e fundamentos esperados usando só a tabela."
tags: [engineering-lifecycle, routing, knowledge-registry, tie-break]
max_turns: 4
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 300
runs: 3
expected_outcome: "Pedido 1: testes-funcionais-playwright, líder qa-playwright, fundamentos qa-testing, web-frontend e engineering-lifecycle (browser-testing-with-devtools, test-driven-development, agente test-engineer). Pedido 2: ui-producao, líder web-frontend, fundamentos engineering-lifecycle (frontend-ui-engineering, browser-testing-with-devtools) e ux-ui-design. Pedido 3: simplificar-codigo, líder code-quality-refactoring, fundamentos engineering-lifecycle (code-simplification), e não revisao-de-codigo como tag principal. Sem tag, plugin ou skill inventados."
---
Estou conferindo o roteamento por tag do orquestrador. Abaixo está um trecho do registro de conhecimento (`KNOWLEDGE.md`) com seis tags. Cada tag tem gatilhos, um plugin líder, plugins de fundamentos e um validador. Roteie os três pedidos usando só este trecho; não leia arquivos nem chame ferramentas.

## Registro (trecho)

#### testes-funcionais-playwright
Gatilhos: testar funcionalidade por funcionalidade; validar cada funcionalidade; abrir o app e validar; testes de ponta a ponta; testes e2e; end-to-end; testar no navegador; automação de testes web; playwright; playwright mcp; e2e tests; browser tests; test every feature; feature by feature validation; playwright-completo
Líder: qa-playwright (skills: playbook)
Fundamentos: qa-testing (skills: e2e-review, test-strategy, verification-gate; agentes: test-auditor, test-writer) | web-frontend (skills: e2e-tests, verify-ui; agentes: ui-evaluator) | engineering-lifecycle (skills: browser-testing-with-devtools, test-driven-development; agentes: test-engineer)
Apoio: design-engineering-kit (skills: playbook; agentes: ui-verifier)
Validador: qa-testing:test-auditor

#### ui-producao
Gatilhos: monte esse componente; crie essa tela responsiva; isso parece feito por ia, melhore; faça o formulário acessível; estados de carregando, vazio e erro; tem erro no console da página; inspecione as requisições de rede dessa ação; tire screenshot antes e depois da mudança; chrome devtools; devtools mcp; this ui looks generic; check console errors and network calls in the browser; frontend-ui-engineering; browser-testing-with-devtools
Líder: web-frontend (skills: design-ui, component-review, a11y-review, verify-ui; agentes: frontend-a11y-reviewer, frontend-code-reviewer)
Fundamentos: engineering-lifecycle (skills: frontend-ui-engineering, browser-testing-with-devtools) | ux-ui-design (skills: a11y-checklist, design-tokens)
Apoio: design-engineering-kit (skills: design-taste-frontend, minimalist-ui)
Validador: web-frontend:ui-evaluator

#### simplificar-codigo
Gatilhos: simplifica esse código; deixa isso mais legível; esse código está complicado demais; refatora sem mudar o comportamento; tira o aninhamento e o código morto; posso apagar esse código; clean up this code; make this more readable; simplify this without changing behavior; chesterton's fence; code-simplification; /code-simplify
Líder: code-quality-refactoring (skills: simplify-safe, refactor-seguro, tech-debt-triage)
Fundamentos: engineering-lifecycle (skills: code-simplification)
Apoio: qa-testing (skills: test-design)
Validador: qa-testing:test-auditor

#### revisao-de-codigo
Gatilhos: revisa esse pr; faz o code review desse diff; posso mergear isso; revisa minhas mudanças antes do merge; dá uma olhada nesse diff; revisão em cinco eixos; code review com severidade crítico e nit; mudança grande demais, como dividir o pr; review this before i merge; code review this pr; review my diff; five-axis review; code-review-and-quality; /review
Líder: code-quality-refactoring (skills: review-diff; agentes: code-reviewer)
Fundamentos: engineering-lifecycle (skills: code-review-and-quality; agentes: code-reviewer)
Apoio: security-appsec (skills: security-review-diff) | git-workflow-release (skills: criar-pr; agentes: revisor-diff)
Validador: code-quality-refactoring:finding-validator

#### tdd
Gatilhos: faça isso com tdd; escreva o teste antes do código; crie um teste que reproduza esse bug antes de corrigir; red green refactor; prove-it; teste de regressão para esse bug; qual a proporção entre testes unitários e de integração; pirâmide de testes; devo mockar isso; meus testes quebram quando refatoro; write a failing test first; test pyramid; test-driven-development; /test
Líder: qa-testing (skills: tdd-guard, test-design, test-strategy, flaky-triage; agentes: test-writer, test-reviewer)
Fundamentos: engineering-lifecycle (skills: test-driven-development; agentes: test-engineer)
Apoio: web-frontend (skills: e2e-tests) | backend-api (skills: api-test-suite)
Validador: qa-testing:test-auditor

#### depuracao-causa-raiz
Gatilhos: depura esse erro; por que isso está falhando; os testes quebraram depois da mudança; o build falhou, o que é isso; funcionava ontem e parou; acha o commit que introduziu o bug; reproduz esse bug antes de corrigir; bug intermitente; debug this error; it worked yesterday and now it's broken; bisect this regression; find the root cause; stop the line; debugging-and-error-recovery
Líder: code-quality-refactoring (skills: debug-causa-raiz; agentes: debugger)
Fundamentos: engineering-lifecycle (skills: debugging-and-error-recovery)
Apoio: sre-observability (skills: root-cause-investigation) | backend-api (skills: backend-debugging) | git-workflow-release (skills: bisect-regressao)
Validador: code-quality-refactoring:finding-validator

## Pedidos

1. "Quero testar no navegador cada funcionalidade do checkout, uma por uma, antes de liberar a versão."
2. "A tela de pedidos abre, mas tem erro no console quando clico em Salvar. Quero ver as requisições de rede dessa ação e entender o que está quebrando."
3. "Refatora essa função sem mudar o comportamento: tem aninhamento demais e código morto, só quero que fique mais legível."

## O que responder

Uma tabela com uma linha por pedido: tag principal; plugin líder (com a skill); plugins de fundamentos (para o engineering-lifecycle, as skills e os agentes); validador; e uma frase dizendo por que não é a tag mais parecida. Se um pedido casar mais de uma tag, nomeie a principal e diga por que as outras não mandam. Não invente tag, plugin nem skill que não esteja no trecho.
