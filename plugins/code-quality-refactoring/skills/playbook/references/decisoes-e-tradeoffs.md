# Decisões e trade-offs

Sumário: D-01 quantas correções falhas · D-02 README x arquivo · D-03 revisor que acha sempre algo · D-04 revisor edita ou propõe · D-05 lista humana x filtro de agente · D-06 padrão de aprovação · D-07 1 revisor x N · D-08 plano antes de codar · D-09 caracterização x escopo · D-10 limiar de PR pequeno · D-11 reescrever x modernizar · D-12 autoavaliação x independência · D-13 instalar ferramentas da comunidade · D-14 hooks de terceiros · D-15 nativo x plugin · D-16 codemod x agente · D-17 refatorar já x rede primeiro · D-18 dividir PR

Cada decisão: condição → escolha → porquê → fonte. Rótulo da escolha entre parênteses quando não vem de fonte. As decisões D-01 a D-15 resolvem conflitos reais entre fontes (SYNTHESIS 3.2); D-16 a D-18 são regras de uso.

## D-01 Quantas correções falhas antes de parar?

- A doc oficial manda, depois de duas correções falhas no mesmo problema, limpar a sessão e reescrever o pedido (V-01). Superpowers e gstack mandam parar após três correções ou hipóteses falhas e discutir o desenho (V-04).
- Escolha (Inferido): são contadores diferentes. **Sessão**: 2 correções falhas = resumir o aprendido e recomeçar com pedido mais específico. **Hipótese**: 3 hipóteses refutadas = parar e propor rever o desenho com o usuário, com três opções (nova hipótese descrita, escalar para quem conhece o sistema, instrumentar e esperar a próxima ocorrência).

## D-02 README do plugin x arquivo do plugin (caso `code-review` oficial)

- README descreve nota 0–100 com limiar 80 e agente de histórico; o arquivo atual usa filtro binário com validação por achado (V-06, Verificado nos dois).
- Escolha: prevalece o arquivo. Aqui a validação por achado é a prova e as faixas de V-07 só ordenam e rotulam.

## D-03 Revisor que "acha sempre algo" x revisor que deixa passar

- Escolha: critério declarado ("só lacuna de correção ou requisito"), obrigação de escrever "nenhuma lacuna encontrada" com o que foi checado, baixo impacto como opcional, validação por achado derruba falso positivo (V-02, V-06).

## D-04 Corrigir direto (fix-first) x revisor somente leitura

- O `/review` do gstack aplica AUTO-FIX; revisor somente leitura não edita (V-09, V-30).
- Escolha: `review-diff` e `code-reviewer` nunca editam; AUTO-FIX vira proposta (ASK) em diff de texto. A correção acontece em outro passo, por pedido do usuário, com teste de regressão.

## D-05 Lista humana do Google x filtro de ruído de agente

- Google inclui nomes, comentários, estilo e documentação (V-17); o pipeline da Anthropic corta estilo (V-06).
- Escolha: modo `agente` (padrão) segue V-06; modo `humano` usa a lista completa de 8 dimensões.

## D-06 Padrão de aprovação x busca de lacunas

- Escolha: veredito pelo padrão do Google (aprovar se melhora a saúde do código, mesmo imperfeito; aprovar com ressalvas; bloquear). Bloquear só por lacuna de correção, requisito, segurança ou quebra de contrato (V-17).

## D-07 Um revisor ou vários em paralelo?

| Situação | Escolha | Fonte |
| --- | --- | --- |
| Diff pequeno, sem área sensível | 1 revisor + `finding-validator` por achado | Suposição, custo (V-35) |
| Diff grande ou sensível (auth, dinheiro, concorrência, dados) | 2–3 revisores por aspecto (regras, bugs, segurança/lógica) | V-06, V-08 |
| "Um agente por aspecto" sempre | Não por padrão: só quando o diff justificar | V-08 |
| Mesmo espaço de problema em paralelo | Evitar: não paralelizar o mesmo espaço de problema | V-24 |

## D-08 Plano antes de codar x pular o plano

- Escolha: plano (research → plan) para mudança multiarquivo ou maior que uma frase (V-25); correção localizada vai direto ao teste que falha (V-01: pule o plano se o diff cabe em uma frase). `codebase-onboarding` usa research/plan.

## D-09 Caracterização trava bugs x escopo mínimo

- Escolha: o teste fixa o comportamento atual com a marca "comportamento atual, possível defeito"; o bug vira follow-up; a correção só ocorre por pedido (V-36, V-10).

## D-10 Limiar de PR pequeno

- Google: cerca de 100 linhas costuma ser razoável, cerca de 1000 é grande demais, a critério do revisor (V-18, Verificado). O "400 linhas ou 10 arquivos" é Suposição; use como alerta configurável ("proponha dividir") e ajuste no CLAUDE.md do projeto (snippet S-09).

## D-11 Reescrever (reimagine) x modernizar incrementalmente

| Tipo | Quando | Condição |
| --- | --- | --- |
| Uplift | Mesma tecnologia, versão nova | Padrão |
| Transform | Outra tecnologia, módulo a módulo | Juiz com entradas iguais nos dois lados |
| Reimagine | Nova arquitetura a partir de spec extraída | Só com spec extraída e plano aprovado; nunca o padrão (V-15, V-21) |
| Strangler | Substituir partes de um sistema vivo | Entregar partes e aposentar a antiga com data (V-21) |

## D-12 Autoavaliação do modelo x independência

- Reflexion mostra ganho com reflexão guiada por feedback externo, em benchmark de geração (V-31, C). Revisão por outro agente do mesmo modelo é independência parcial (V-35).
- Escolha: o sinal externo (teste, compilador, juiz) valida; a revisão por agente é declarada como parcial e acompanha leitura humana.

## D-13 Instalar ferramentas da comunidade (gstack, agent-os)

- Escolha: nunca instalar nem copiar scripts, hooks ou binários. Só ideias em prosa. Motivo: `./setup` compila binário, baixa Chromium, edita CLAUDE.md, registra hooks e tem telemetria opcional (aviso 3 de VALIDATED).

## D-14 Plugin oficial `code-modernization` traz hooks e telemetria

- Escolha: extrair o método (veredito de paridade, legado somente leitura); nenhum hook entra (aviso 4).

## D-15 Comandos nativos x skills do plugin

| Tarefa | Nativo | Skill do plugin | Use o plugin quando |
| --- | --- | --- | --- |
| Revisão de diff | `/code-review` | `review-diff` | quer filtro de falsos positivos, evidência por linha, rótulos e veredito padronizado |
| Simplificar | `/simplify` | `simplify-safe` | quer garantia de comportamento (teste antes e depois) |
| Mudança em massa | `/batch` | `migration-parity` | precisa de juiz, rulebook e paridade; o plugin não reimplementa worktrees |

Confira os comandos na versão instalada do Claude Code (V-13: dependem da versão).

## D-16 Codemod/receita determinística x agente

- Se existe receita (OpenRewrite, codemod oficial do framework, Dependabot para versões): usá-la primeiro, sob juiz; o agente trata o resto. Mudança que depende de contexto semântico (regras de negócio, nomes) vai ao agente em lotes pequenos. Instalar a ferramenta só com pedido do usuário (V-40, V-14).

## D-17 Refatorar já x construir rede de segurança primeiro

| Estado | Escolha |
| --- | --- |
| Há testes que cobrem o trecho e passam | Refatorar em passos, rodando a suíte |
| Há testes, mas não cobrem o trecho | Caracterizar o trecho, depois refatorar |
| Não há testes e é possível testar | Caracterização completa antes |
| Não é possível testar (efeito externo, UI sem harness) | Passo menor, preservação só por leitura, rótulo Inferido, avisar o usuário |

## D-18 Dividir PR

- Diff acima do limiar, ou mistura de refatoração e comportamento: dividir com `assets/templates/pr-split-plan.md` (refatoração pura primeiro, comportamento depois, testes junto de cada commit). Commit e push só a pedido do usuário; branching e merge ficam em `git-workflow-release`.
