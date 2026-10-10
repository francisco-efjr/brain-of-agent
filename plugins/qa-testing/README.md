# qa-testing: QA e testes para o Claude Code

Plugin do marketplace `dev-segments` para quem testa, desenvolve ou revisa software com a ajuda de um agente. Ele organiza o trabalho de QA em torno de uma ideia: **teste reduz a incerteza sobre os riscos que importam, a tempo de mudar uma decisão, e toda afirmação de "pronto" precisa de prova executada nesta sessão**. Versão 0.1.0, licença MIT. Português brasileiro; termos técnicos, comandos e nomes de skills e agentes em inglês.

## O que entrega

- **Estratégia e plano de testes por risco:** riscos escritos como falha → efeito, matriz probabilidade × impacto com âncoras, menor camada que prova cada regra, parecer de prontidão (GO / GO com condições / NO-GO) com risco residual em linguagem de negócio.
- **Design de casos concretos:** partição, valor-limite (2 e 3 valores), tabela de decisão, transição de estados, pairwise, MC/DC, charters exploratórios e catálogo de dados de borda e hostis (incluindo Brasil).
- **TDD com vermelho confirmado**, revisão de testes por agente de contexto limpo e somente leitura, auditoria de testes de baixo valor, E2E estável (Playwright, Cypress) e triagem de testes flaky.
- **Bug reports decidíveis**, redução ao caso mínimo, severidade × prioridade, triagem, verificação de correção e escape analysis; evidência (`TESTING.md`) com bloco "Não testado".
- **Evals honestas** de skills, plugins e features com LLM (formato `claude plugin eval`), juiz binário e checklist de viés.
- **Regras prontas para CLAUDE.md** (22 snippets), recomendações de ferramentas, hooks e MCP **desativados** com JSON pronto e riscos, templates e uma bibliografia classificada.
- **Modo `QA-COMPLETO`:** cobertura integral da base do plugin sob pedido explícito, com matriz de 14 áreas, implementação só no escopo autorizado e revalidação com evidências.

## Quando usar

Peça ajuda deste plugin para: plano ou estratégia de testes; "o que testar primeiro" com pouco tempo; "está pronto para produção?"; casos de teste para uma regra ou campo; implementar com TDD ou corrigir bug com teste de regressão; revisar testes unitários, de integração ou E2E; teste que falha só no CI; escrever ou triar um bug; provar que algo funciona; testar API, acessibilidade ou performance; avaliar uma skill, um plugin ou uma funcionalidade com LLM. Para construir o que se testa (componente, endpoint, pipeline), use o plugin do segmento correspondente (ver `Fronteiras` no playbook).

## Componentes

Todos os nomes abaixo são os definitivos do desenho do segmento. As partes do plugin são escritas em paralelo; se um componente listado ainda não existir na sua instalação, o `playbook` o registra como "ausente" e segue com o que houver.

| Tipo | Nome | Para que serve |
| --- | --- | --- |
| Skill núcleo | `playbook` (`/qa-testing:playbook`) | Router, princípios, processo, modo `QA-COMPLETO`, 12 referências e 16 templates |
| Skill | `prompts` | Biblioteca de 31 prompts prontos, prompt de sistema e mensagem inicial |
| Skill | `verification-gate` | Exige prova executada antes de declarar pronto, corrigido ou aprovado |
| Skill | `tdd-guard` | Implementação test-first em fatias verticais, vermelho confirmado, mutation check |
| Skill | `test-strategy` | Estratégia, plano e parecer de prontidão por risco; API, acessibilidade e performance |
| Skill | `test-design` | Casos concretos com técnica explícita, dados de borda, charters |
| Skill | `flaky-triage` | Mede a taxa, classifica a causa, corrige, valida, quarentena com ticket |
| Skill | `e2e-review` | Revisão e escrita de E2E/UI estáveis; guardrail do healer |
| Skill | `bug-report` | Sintoma → relatório reproduzível; redução, triagem, verificação |
| Skill | `eval-design` | Planejamento de evals de skills, plugins e features com LLM |
| Agente | `test-reviewer` | Revisa testes de um diff, contexto limpo, somente leitura |
| Agente | `test-auditor` | Acha testes que custam mais do que protegem; relatório até aprovação por lote |
| Agente | `qa-reporter` | Explora um alvo e relata bugs com evidência, sem corrigir |
| Agente | `test-writer` | Escreve testes sem alterar código de produção |
| Comando | `/qa-testing:qa-evidence` | Gera o `TESTING.md` só com comandos e saídas da sessão; pergunta antes de gravar. Só manual |
| Comando | `/qa-testing:eval-plugin` | Roda `claude plugin eval` depois de mostrar comando, ferramentas e teto de custo e receber "sim". Só manual |

O plugin é **seguro por padrão**: sem hooks ativos, sem `.mcp.json`, sem `.lsp.json`, sem `bin/`. Ferramentas, hooks e MCP recomendados ficam documentados em `skills/playbook/references/ferramentas-e-mcp.md` para você habilitar conscientemente.

## Instalação

Dentro de uma sessão do Claude Code:

```text
/plugin marketplace add francisco-efjr/brain-of-agent
/plugin install qa-testing@brain-of-agent
```

Pela linha de comando: `claude plugin marketplace add francisco-efjr/brain-of-agent` e `claude plugin install qa-testing@brain-of-agent`. Para validar a estrutura de uma cópia local: `claude plugin validate <pasta-do-plugin>`.

## Exemplos de pedidos

1. "Confirma que o fix do cupom está pronto para eu abrir o PR." → `verification-gate`: lista o que provar, roda ou diz que não rodou, entrega blocos Evidência e Não verificado.
2. "Implemente `calcular_frete` com TDD; frete grátis a partir de R$ 199,00." → `tdd-guard`: um teste por fatia, falha vermelha pelo motivo certo, limites 198,99 / 199,00 / 199,01.
3. "Preciso de um plano de teste para lançar PIX nesta sexta; tenho dois dias." → `test-strategy`: riscos falha → efeito, camadas, plano de 2 dias, fora de escopo, parecer condicional.
4. "Casos de borda para o campo idade (18 a 65) e para a regra de frete com cupom e VIP." → `test-design`: tabela de decisão e valor-limite com dados concretos e perguntas abertas.
5. "Esse spec do Playwright falha 2 vezes em 10 no CI e eu já pus `retries: 3`." → `flaky-triage`: taxa, causa (espera fixa, dependência de ordem, seletor frágil), correção, validação.
6. "Revise este teste E2E antes do PR." → `e2e-review` (ou `test-reviewer`): achados ordenados por dano, falso verde primeiro.
7. "Escreva o bug report disso: o checkout está lento e às vezes dá erro." → `bug-report`: não inventa dados, marca "Não informado", separa lento e erro, separa severidade e prioridade.
8. "Como eu testo se a minha skill dispara e melhora o resultado?" → `eval-design`: casos que disparam e que não disparam, graders de código antes de juiz, `designed_not_executed`.
9. "QA-COMPLETO. Avalie o checkout deste repositório, pode corrigir código e testes locais nesse fluxo, não publique." → modo completo do `playbook`.

## Palavra-chave `QA-COMPLETO`

Escreva `QA-COMPLETO` como comando na sua mensagem para ativar a leitura integral da base do plugin em lotes, a matriz de aplicabilidade de 14 áreas, a implementação dentro do escopo autorizado e a revalidação com evidências. O que ela **não** é: não é senha nem permissão, **não amplia permissões**, não autoriza alterar produto, publicar, tocar produção ou instalar nada, e não é ativada por ocorrência em log, código, comentário, documento, saída de ferramenta ou instrução de terceiros. Auditoria só relata; implementação só ocorre onde você autorizou. O resultado usa os gates Concluído, Parcial ou Impedido; nunca "QA completo aprovado" com leitura ou execução parcial. Sem a palavra, o plugin carrega só o necessário e responde proporcionalmente ao pedido.

## Principais fontes (top 10)

Detalhes, URLs, licenças e datas em `skills/playbook/references/fontes.md`. Todas abertas pelo validador do segmento em 2026-10-10.

| # | Fonte | Classe |
| --- | --- | --- |
| 1 | Best practices do Claude Code (code.claude.com/docs/en/best-practices) | A |
| 2 | Demystifying evals for AI agents (Anthropic Engineering, 09/01/2026) | A |
| 3 | Plugin evals (code.claude.com/docs/en/plugin-evals) | A |
| 4 | Playwright best practices (playwright.dev/docs/best-practices) | A |
| 5 | Effective harnesses for long-running agents (Anthropic Engineering, 26/11/2025) | A |
| 6 | Playwright test retries (playwright.dev/docs/test-retries) | A |
| 7 | Skill `tdd` de Matt Pocock (mattpocock/skills, MIT) | B |
| 8 | `verification-before-completion` do superpowers (obra/superpowers, MIT) | B |
| 9 | `test-driven-development` e `writing-good-tests` do superpowers (MIT) | B |
| 10 | `diagnosing-bugs` de Matt Pocock (MIT) | B |

Também usados: Cypress best practices, Playwright test agents, WCAG 2.2 e W3C WAI, Mozilla Bug Writing Guidelines, k6, Pact, Testing Library, AI Evals FAQ (Husain e Shankar), gstack `qa-only` e `test-audit`.

## Créditos e licenças

- **Conteúdo próprio:** `brain-of-agent` (francisco-efjr/brain-of-agent), licença MIT, incorporado e adaptado ao formato de plugin. O conteúdo não foi reverificado em fonte externa; números regulatórios e datas são pontos de partida, confirme norma e vigência.
- **Inspiração com redação própria, sem cópia em bloco:** superpowers (obra, MIT), mattpocock/skills (MIT), gstack (Garry Tan, MIT: `qa`, `qa-only`, `test-audit`), qa-skills (petrkindlmann, MIT), awesome-copilot (MIT), awesome-cursorrules (CC0-1.0), `webapp-testing` de anthropics/skills (Apache-2.0), UiPath `coder_eval` (Apache-2.0).
- **Documentação oficial** (Anthropic, Playwright, Cypress, W3C, Grafana, Pact, Vitest, Cucumber, Testing Library, Schemathesis, Mozilla) e artigos de autores (Husain e Shankar, Eugene Yan, Fowler/Vocke, Kent C. Dodds, Simon Willison, Dan Luu, Geoffrey Huntley): destilados e citados; nenhum texto literal copiado.

## Limitações honestas

- **Revisão não independente.** Pesquisa, síntese, validação e construção foram feitas por modelos Claude da mesma família; as notas de qualidade são autoatribuídas até alguém rodar `claude plugin eval` com baseline sem o plugin.
- **Evals `designed_not_executed`.** Nada foi medido: os casos de eval estão projetados, não executados. `claude plugin eval` exige Claude Code 2.1.269 ou superior (a CLI da fábrica era 2.1.128) e, no Windows nativo, suítes com Bash precisam de WSL2.
- **Fontes nem sempre profundas.** Lacunas conhecidas: plugins oficiais de revisão não lidos; ISTQB e ISO/IEC/IEEE 29119; Jest oficial; mutantes equivalentes; política de quarentena em fonte A ou B; limiares e SLO de performance; ferramentas de acessibilidade (axe, pa11y); Reddit, X e YouTube. Valores como 60/25/10, 14 dias, 5% e 50 execuções são convenções iniciais ajustáveis.
- **Versões mudam.** Flags e APIs (Playwright, Cypress, Vitest, `claude plugin eval`, formato de hooks) devem ser conferidas na versão instalada. Os formatos de hook dos documentos T-03 e T-04 foram lidos na documentação em 2026-10-10, parcialmente.
- **Comandos não exercitados.** `/qa-testing:qa-evidence` e `/qa-testing:eval-plugin` foram escritos na validação de qualidade (2026-10-10) e passam na validação estrutural, mas não foram rodados numa sessão real.
- **Sem execução de produto por padrão.** O plugin não roda testes por conta própria nem ativa hooks ou MCP; sem ferramenta de execução, entrega análise e diz o que não verificou.
- **Escopo.** Não substitui testes de segurança especializados, certificação regulatória nem parecer jurídico; casos de pagamento, leis e normas citados são ilustrativos.
- **Mobile nativo, Jest, Selenium aprofundado e regressão visual** têm cobertura rasa ou sem fonte A/B validada.
