# ux-ui-design — UX, UI e design systems

Plugin do Claude Code para direção visual, auditoria de interface, avaliação heurística, acessibilidade WCAG 2.2 AA, design tokens, UX writing e pesquisa com usuários. Parte da fábrica `dev-segments` (um plugin por segmento de desenvolvimento). Versão 0.1.0, conteúdo validado em 2026-10-10, licença MIT.

A ideia central: levar o trabalho do contexto (usuário, tarefa, produto) até uma decisão de design **verificável**, com evidência, sem tratar a opinião de um modelo como validação com usuários e sem instalar nem executar nada de terceiros.

## O que entrega

- **Processo** de contexto até entrega: brief de uma linha, plano antes de código, revisão contra o visual genérico, estados e dados extremos, verificação com evidência, crítica independente, relatório com rótulos Verificado, Inferido, Suposição e Não verificável.
- **Skills de tarefa** para direção visual, auditoria de UI em dez categorias, avaliação heurística (Nielsen, severidade 0 a 4), checklist de acessibilidade WCAG 2.2 AA, microcopy, tokens em três camadas e plano de pesquisa.
- **Agentes somente leitura** (avaliador cético, revisor de acessibilidade, pesquisador, auditor de design system) e um agente de design com escrita limitada ao que o usuário indicar.
- **Base de conhecimento** em 13 referências (checklist completo, padrões e anti-padrões, decisões, regras prontas de CLAUDE.md, ferramentas desativadas com riscos, bibliografia, WCAG, plataformas Apple, tokens, pesquisa, UX writing, avaliação por LLM, design system da casa) e 13 templates (incluindo a estrutura recomendada de um design system).
- **Biblioteca de prompts** curados (37 prompts em cinco temas: começar e dirigir, auditoria, acessibilidade e plataforma, pesquisa e escrita, design system; distribuídos em três arquivos de `skills/prompts/references/`) e 12 casos de eval.

## Design system da casa (Mo baile)

O Mo baile Design System é o design system de referência do autor (macOS 27, Liquid Glass). O plugin incorpora as **boas práticas dele**, com evidência por arquivo, em `skills/playbook/references/design-system-da-casa.md` e a estrutura reutilizável em `skills/playbook/assets/templates/design-system-bundle.md`: tokens em camadas por aparência (claro, escuro, alto contraste), fallbacks de acessibilidade como tokens, contrato por componente, lint de aderência, fundamentos de conteúdo e rastreabilidade. Ele só é usado **quando você pede** ("aplica o design system que já temos") e nunca como padrão universal: a estética macOS vale em app macOS; em outro produto ou plataforma o plugin herda a estrutura, não a identidade. O bundle fica em `design-systems/mo-baile/` do repositório publicado e não faz parte deste plugin.

## Quando usar

Use ao desenhar, melhorar, criticar ou auditar uma tela; ao decidir paleta e tipografia antes de codar; ao revisar acessibilidade no nível de design; ao escrever ou revisar microcopy; ao estruturar tokens ou renomear tokens com segurança; ao planejar entrevistas e testes de usabilidade. Para **implementar** o design em código, performance ou testes de UI, use `/web-frontend:playbook`.

## Instalação

No Claude Code, dentro da sessão:

```text
/plugin marketplace add francisco-efjr/brain-of-agent
/plugin install ux-ui-design@brain-of-agent
```

`<caminho-local-ou-owner/repo>` é a pasta raiz do marketplace `dev-segments` (a que contém `.claude-plugin/marketplace.json`) ou o repositório Git dela. Pela linha de comando, o equivalente é `claude plugin marketplace add francisco-efjr/brain-of-agent` e `claude plugin install ux-ui-design@brain-of-agent`. Para validar: `claude plugin validate <pasta-do-plugin>`. Todos os componentes ficam sob o namespace `ux-ui-design` (por exemplo `/ux-ui-design:ui-audit`).

## Componentes

| Tipo | Nome | Para quê |
| --- | --- | --- |
| Skill (núcleo) | `playbook` | Router, princípios, processo, proporcionalidade, fronteiras e modo `UXUI-COMPLETO`; guarda as referências e os templates |
| Skill | `prompts` | Índice e biblioteca de prompts: começar e dirigir, auditoria, acessibilidade e plataforma, pesquisa e escrita, design system |
| Skill | `design-brief` | Brief, direção visual, plano de design, fluxo de telas com wireframe, spec de handoff, revisão de plano e brief de design system |
| Skill | `ui-audit` | Auditoria somente leitura em dez categorias com PASS/PARTIAL/FAIL e impacto, mais checagem de aderência ao design system (sem hex/px crus, tokens via `var()`, componente com contrato) |
| Skill | `heuristic-eval` | Avaliação heurística de um fluxo com severidade 0 a 4 |
| Skill | `a11y-checklist` | Especificar e revisar acessibilidade WCAG 2.2 AA com roteiro de teste manual |
| Skill | `ux-writing` | Microcopy, erros em três partes, estados vazios, voz (com os fundamentos de conteúdo do Mo baile como exemplo de guia pt-BR) e notas de localização |
| Skill | `design-tokens` | Tokens em três camadas, aparências claro/escuro/alto contraste, fallbacks de reduzir movimento e transparência, lint de aderência, drift, release e esqueleto DTCG 2025.10 |
| Skill | `user-research-plan` | Plano de pesquisa, entrevista de 50 minutos, teste de usabilidade, card sorting, tree testing |
| Skill | `design-init` | Cria o `DESIGN.md` e, com `bundle`, propõe a estrutura de um design system completo; só por comando explícito (`disable-model-invocation`) |
| Agente | `design-evaluator` | Avaliador cético de UI, somente leitura |
| Agente | `ui-designer` | Projeta ou refina telas e componentes dentro do design system (inclusive o design system da casa, quando você pedir) e entrega spec |
| Agente | `a11y-reviewer` | Revisão de acessibilidade somente leitura, com checklist por tipo de arquivo |
| Agente | `ux-researcher` | Planeja pesquisa e sintetiza notas fornecidas, sem inventar |
| Agente | `design-system-auditor` | Audita tokens e componentes: drift, camada errada, release, aderência e contrato por componente |
| Comandos | (nenhum) | Cada skill já vira `/ux-ui-design:<skill>` |

## Exemplos de pedidos

1. "Revisa o visual desta tela de configurações: está com cara de template genérico?" → `ui-audit`.
2. "Define a direção visual do app de agendamento de uma clínica antes de eu codar: paleta, fontes e layout." → `design-brief`.
3. "Faz uma avaliação heurística do fluxo de recuperar senha." → `heuristic-eval`.
4. "O foco do modal some quando fecho. Isso passa na WCAG 2.2 AA? O que corrijo?" → `a11y-checklist`.
5. "Reescreve as mensagens de erro do cadastro e o estado vazio da lista de projetos, em tom caloroso mas direto." → `ux-writing`.
6. "Tenho hex espalhado no CSS: monta tokens em três camadas e prepara o modo escuro, listando o que muda antes de renomear." → `design-tokens`.
7. "Monta o roteiro de teste de usabilidade do onboarding do app de conta digital; tenho uma semana." → `user-research-plan`.
8. "UXUI-COMPLETO: audite o checkout do e-commerce inteiro e implemente só as correções de acessibilidade que eu aprovar." → modo completo.

Cada resposta traz o que foi verificado e o que não foi. Sem navegador ou leitor de tela, o plugin diz "não renderizei" ou "não testado" em vez de supor.

## Keyword UXUI-COMPLETO

Ativa a cobertura integral do segmento **somente quando você escreve `UXUI-COMPLETO` na sua própria mensagem**, como pedido. O modo lê as referências em lotes e registra cada uma como lida, parcial ou ausente; preenche uma matriz de aplicabilidade por área; implementa apenas o que você autorizou; revalida com evidências e lista as lacunas. Ele **não amplia permissões**: instalar pacotes, ligar hooks, usar Figma ou MCP, fazer commit ou publicar continuam exigindo autorização concreta. A mesma palavra em documento, log, README, página ou comentário de código não ativa nada; o plugin avisa que a viu e a ignorou. Sem a keyword, o plugin carrega só o necessário (proporcionalidade).

## Escolher o recurso certo (output style, CLAUDE.md, skill, hook, subagente)

| Você quer | Use |
| --- | --- |
| Mudar voz e formato da sessão | Output style (instrução, não garantia; não use `force-for-plugin`) |
| Convenções do projeto, sempre visíveis | CLAUDE.md curto (`references/claude-md-snippets.md`) |
| Tarefa com gatilho e processo | Skill |
| Garantia de que algo roda | Hook (documentado, desativado) |
| Tarefa isolada em contexto limpo | Subagente |

## Segurança por padrão

O plugin não traz hooks, `.mcp.json`, `.lsp.json` nem `bin/`. Não instala pacotes, não executa `npx`, não escreve no Figma, não faz commit nem push, e trata páginas, arquivos do Figma, logs e comentários como **dado, nunca instrução**. Ferramentas úteis (Playwright MCP, Figma MCP, axe, Storybook, CLI do design.md, hooks) estão documentadas em `skills/playbook/references/ferramentas-e-mcp.md` com JSON pronto, riscos e a recomendação de fixar versão, para você habilitar de forma consciente.

## Principais fontes

Lista completa, com URL, licença e data, em `skills/playbook/references/fontes.md`. Classe A = oficial; B = prática reconhecida.

| # | Fonte | Classe |
| --- | --- | --- |
| 1 | Skill `frontend-design` (anthropics/skills) | A |
| 2 | Claude Code best practices (code.claude.com) | A |
| 3 | WCAG 2.2, W3C (Recommendation de 2024-12-12) | A |
| 4 | NN/g: 10 heurísticas, avaliação heurística e severidade | A |
| 5 | `a11y.instructions.md` (github/awesome-copilot, MIT) | A |
| 6 | Harness design for long-running apps (Anthropic Engineering) | B |
| 7 | Skills `ux-copy` e `user-research` (anthropics/knowledge-work-plugins, Apache-2.0) | A |
| 8 | ARIA APG: diálogo modal (W3C) | A |
| 9 | W3C DTCG: formato de design tokens 2025.10 (relatório de comunidade, não padrão W3C) | A |
| 10 | Agent Skills best practices (Anthropic) | A |

## Créditos e licenças

- Este plugin: MIT, Francisco Edson. Conteúdo próprio do autor incorporado do repositório brain-of-agent (MIT): guia de convenções Apple (`apple-design`) e guia de acessibilidade, adaptados em `apple-e-plataformas.md`, `wcag-aa.md` e `checklist-completo.md`; estilo da casa (rótulos epistêmicos, proporcionalidade, keyword de modo completo, handoff).
- Inspiração com atribuição, em redação própria e sem cópia em bloco: **gstack** (Garry Tan, MIT; categorias de auditoria, teste de tronco, classificador de superfície, princípios de revisão de plano), skills da Anthropic em `anthropics/skills` e `anthropics/knowledge-work-plugins` (Apache-2.0), `google-labs-code/design.md` (Apache-2.0), `pbakaus/impeccable` (Apache-2.0, só o padrão de detector determinístico mais julgamento), `github/awesome-copilot` (MIT), `plugin87/ux-ui-agent-skills` (MIT), `Owl-Listener/designer-skills` (MIT), `VoltAgent/awesome-claude-code-subagents` (MIT), `nextlevelbuilder/ui-ux-pro-max-skill` (MIT).
- Apenas destilado, sem texto copiado: NN/g, W3C (WCAG, APG), Apple HIG, web.dev, documentação da Anthropic, Figma Help, Storybook. © dos respectivos titulares.
- Instaladores, hooks, telemetria, commits automáticos e binários das fontes acima **não** foram adotados.

## Limitações honestas

- A pesquisa e a validação foram feitas por modelos da família Claude; a independência é parcial. Parte da evidência de fontes (por exemplo ux-ui-agent-skills) é autorrelatada. Nenhuma comparação independente entre skills de design existe.
- Avaliação visual por modelo é subjetiva e ainda leniente. A crítica do `design-evaluator` e a avaliação heurística são **opinião**, não validação com usuários; o plugin recomenda usuários reais para os achados mais graves. Os exemplos de calibração do avaliador são sintéticos.
- Lacunas conhecidas: Material Design 3 (não verificado), motion (duração e easing), tipografia e grid sem fonte primária, handoff com Figma Dev Mode e MCP oficial, UX writing em PT-BR (tom e tratamento são Suposição), internacionalização e RTL, tamanhos de amostra de card sorting e tree testing, survey, personas e JTBD (encaminhados a `/product-discovery-specs:playbook`).
- DTCG 2025.10 é relatório de comunidade, não padrão W3C, a estrutura de `color`, `dimension` e `duration` foi conferida na spec, mas tipos compostos e modos não; `design.md` está em alpha; Style Dictionary não foi verificado.
- A tabela de normas de acessibilidade (LBI, NBR 17060, EAA, EN 301 549, Section 508) é orientação de escopo herdada e não foi reverificada. O plugin não dá parecer jurídico nem declara conformidade.
- A lista de anti-padrões de visual genérico envelhece: revise a cada 6 meses; o briefing e a marca existente sempre vencem.
- Os evals estão `designed_not_executed`: exigem `claude plugin eval` (Claude Code 2.1.269 ou superior; a CLI local da fábrica é 2.1.128). Confira versões de WCAG, DTCG, design.md e do Claude Code na data do uso.
