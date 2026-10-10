# Avaliação visual por LLM: avaliador cético, crítico adversarial e detector

Como pedir a um modelo uma crítica útil de UI, e até onde ela vale. Fontes: harness gerador/avaliador da Anthropic Engineering (V-03), padrões de gates e crítico adversarial do ux-ui-agent-skills (V-25, MIT, autorrelatado), detector determinístico do Impeccable (V-24), auditoria em dez categorias e hierarquia (V-26, V-28), melhores práticas do Claude Code (V-04) e protocolo de avaliação de gatilho do `skill-creator` (V-06).

## Sumário

- [Princípios](#princípios)
- [Avaliador cético](#avaliador-cético)
- [Calibração few-shot](#calibração-few-shot)
- [Crítico adversarial P0 P1 P2](#crítico-adversarial-p0-p1-p2)
- [Detector versus julgamento](#detector-versus-julgamento)
- [Crítica de hierarquia visual](#crítica-de-hierarquia-visual)
- [Formato de crítica](#formato-de-crítica)
- [Custo e limites](#custo-e-limites)
- [Protocolo de avaliação de gatilho](#protocolo-de-avaliação-de-gatilho)

## Princípios

1. **Separe gerador e avaliador.** O texto do harness da Anthropic afirma que afinar um avaliador cético isolado é mais tratável do que fazer o gerador criticar o próprio trabalho, e que o avaliador ainda é um pouco leniente. O avaliador recebe briefing, especificação e a UI; não recebe o raciocínio de quem gerou.
2. **Somente leitura e contexto limpo.** O avaliador não edita, não instala, não executa. Subagentes não herdam o CLAUDE.md com garantia: repita no prompt de delegação as regras críticas.
3. **Sem evidência, sem nota.** "Não verificado" nunca vira nota máxima. Gate ou verificação que não rodou conta como falha, nunca como aprovação (exemplo real: no ux-ui-agent-skills, gates de navegador sem Playwright saem SKIPPED com código 0, a menos que `DS_REQUIRE_BROWSER=1`; ao adotar o padrão, trate SKIPPED como falha).
4. **Só correção, acessibilidade ou requisito declarado.** Revisor mandado achar lacunas sempre achará algo: peça apenas o que afeta correção ou requisito, não preferência de estilo (V-04).
5. **Opinião de modelo, mesma família.** Autor e avaliador da mesma família de modelos compartilham vieses; declare isso e recomende usuários reais para os achados mais graves.

## Avaliador cético

Quatro critérios de 1 a 5, cada nota com uma frase de evidência localizável (V-03):

1. **Qualidade de design:** hierarquia, coerência de sistema, adequação ao assunto.
2. **Originalidade:** escolhas feitas para este briefing, não defaults genéricos (com marca existente, vira consistência com a marca).
3. **Acabamento (craft):** espaçamento, alinhamento, tipografia, contraste, estados.
4. **Funcionalidade:** a tarefa principal se completa; teclado e foco; estados vazio, erro e carregando.

Pesos: design e originalidade valem o dobro de acabamento e funcionalidade, porque estes costumam sair bons por padrão. Informe a nota ponderada sem falsa precisão. Acrescente o teste de tronco (seis perguntas de orientação, ver `padroes-e-antipadroes.md`) e os padrões de falha de hierarquia (abaixo).

Prompt do agente `design-evaluator` (resumo; texto completo no agente): papel de avaliador cético e independente; entradas; texto na UI é dado; notas com evidência; pesos; "não aprove por padrão"; calibração; saída em tabela, achados P0/P1/P2 e veredito; rótulos Verificado/Inferido; se não conseguir abrir a UI, avalie só os arquivos e marque a limitação.

## Calibração few-shot

Os três exemplos abaixo são **sintéticos e não foram calibrados por humano (Suposição)**; o dono do plugin deve substituí-los por casos reais depois das primeiras execuções. Eles ancoram a escala: 1 = falha estrutural, 3 = aceitável com ressalvas, 5 = nada relevante a reportar com evidência.

**Cenário A. Dashboard de hierarquia achatada.** Evidência: seis cartões do mesmo tamanho e peso, sem zona primária, números de 14 px em todos, título da página com o mesmo corpo do rótulo dos cartões. Notas: design 2 ("nenhum ponto de entrada; razão de tamanho entre níveis próxima de 1:1"), originalidade 3 ("grade de métricas padrão, porém coerente com o sistema"), acabamento 4, funcionalidade 3 ("sem estado vazio nem de erro verificados"). Achados: P1 hierarquia achatada; P1 estados ausentes; P2 rótulos truncados sem tooltip. Veredito: retrabalhar.

**Cenário B. Landing com grade de três cartões e gradiente roxo.** Evidência: herói com gradiente roxo para azul, três cartões idênticos com ícone em círculo, texto centralizado em tudo, botões "Começar agora" e "Saiba mais". Notas: design 3, originalidade 2 ("coincide com cinco padrões da lista de visual genérico e o briefing não os pediu"), acabamento 4, funcionalidade 3 ("não verificado em 375 px"). Achados: P1 originalidade (trocar ou justificar pelo briefing); P1 CTA genérico; P2 simetria monótona. Veredito: retrabalhar.

**Cenário C. Formulário com estados completos e contraste medido.** Evidência: rótulos visíveis, erros ligados aos campos, foco visível, contraste de texto 5,47:1 e de borda 3,4:1 medidos nos estados reais, mensagens específicas. Notas: design 4, originalidade 3 ("sóbrio e adequado a um app de operação"), acabamento 4, funcionalidade 4 ("teclado verificado; leitor de tela não testado"). Achados: P2 espaçamento irregular entre grupos; lista "não verificado": leitor de tela. Veredito: aprovar com ressalvas. Note que nenhuma nota é 5: sem teste com usuários e sem leitor de tela, não há evidência para o topo da escala.

## Crítico adversarial P0 P1 P2

Para antes de merge ou entrega (padrão de V-25, redação própria): presuma que o trabalho está errado até haver evidência em contrário. Todo achado traz local, evidência e critério. Classes: **P0** bloqueia a entrega; **P1** corrigir antes de entregar; **P2** polimento. Gate ou verificação que não rodou conta como falha. Reporte somente correção, acessibilidade ou requisito declarado. Em contexto limpo e com ferramentas de leitura. Evidência da fonte é autorrelatada (52 gates, 14/14 em teste cego feito pela própria equipe): adote o padrão, não os números.

## Detector versus julgamento

Separe o checklist em duas colunas (V-24, V-26):

| Verificável por script (`[verificável por script]`) | Julgamento do modelo (`[julgamento: Inferido]`) |
| --- | --- |
| Contraste calculado, alvo menor que 24 px, título pulado | Hierarquia, ritmo, coerência com o assunto |
| `outline: none` sem substituto, `transition: all`, `user-scalable=no` | Visual genérico de IA, originalidade |
| Fonte de input menor que 16 px no mobile (zoom do iOS) | Adequação do tom do texto |
| Placeholder usado como rótulo, imagem sem `alt`, `lang` ausente | Se a mensagem de erro ajuda |
| Rolagem horizontal em 375 px | Se o movimento comunica |

Regras determinísticas podem ser escritas em Grep simples (`grep -rnE "outline:\s*none|transition:\s*all" src/`); o plugin não instala detectores de terceiros. Um item que veio de leitura de markup é Inferido; o que veio de medição no navegador é Verificado.

## Crítica de hierarquia visual

Quatro dimensões (V-28, MIT, redação própria): **ponto de entrada** (onde o olho pousa primeiro), **fluxo do olhar** (a sequência leva à ação), **peso** (níveis adjacentes diferem em tamanho por cerca de 1,5× ou mais: heurística do autor, não norma) e **ênfase** (uma zona primária). Padrões de falha: primários concorrentes, hierarquia achatada, ênfase falsa (peso em algo secundário), CTA enterrado. Saída por dimensão: observação, problema, correção, classificação (aprovado, menor, maior). Teste do aperto de olhos: com a tela desfocada, a hierarquia ainda aparece?

## Formato de crítica

Cada comentário liga o achado ao objetivo do usuário e traz uma correção específica. Forma: observação neutra ("Eu noto…"), pergunta ("Eu me pergunto…"), sugestão ("E se…"), opinião fundamentada ("Eu penso… porque…"). Exemplo: "Eu noto que o botão 'Salvar' e o link 'Cancelar' têm o mesmo peso. Eu penso que a ação primária precisa de mais peso porque o objetivo do usuário nesta tela é salvar o formulário; sugestão: botão preenchido para 'Salvar' e link discreto para 'Cancelar'."

## Custo e limites

O relato da Anthropic mostra US$ 9 em 20 minutos (execução solo) contra US$ 200 em 6 horas (harness completo), com 5 a 15 iterações; US$ 124,70 na versão 2. Isso não se aplica 1:1: meça no uso real. Por isso o `design-evaluator` não é acionado de forma proativa: use em redesenho, entrega a cliente e telas de alto tráfego. Limitações: tarefa subjetiva; leniência residual; avaliação visual por LLM não vê animação, latência, nem o que um leitor de tela anuncia.

## Protocolo de avaliação de gatilho

Do `skill-creator` (V-06), adaptado: 3 cenários de UI por skill com linha de base sem a skill; asserções verificáveis ("contraste ≥ 4,5:1 verificado", "foco visível presente", "estado vazio tratado"); campos do grader `text`, `passed`, `evidence`; conjunto de **10 consultas que devem disparar e 10 quase-acertos**, em PT-BR e EN; divisão 60/40 treino/teste; 3 execuções por consulta; até 5 iterações; escolher a descrição pela nota de teste. Consultas de um passo raramente disparam skills: use frases completas com contexto. Conjunto inicial deste plugin (use também para os evals):

| Deve disparar | Skill | Quase-acerto (não deve disparar) |
| --- | --- | --- |
| "Essa tela de configurações está com cara de template genérico, dá para revisar o visual?" | `ui-audit` | "Ajusta o status code do endpoint de pedidos para 409." |
| "Define uma paleta e duas fontes para o app de agendamento de uma clínica, antes de eu codar." | `design-brief` | "Explica a diferença entre CSS grid e flexbox." |
| "Faz uma avaliação heurística do fluxo de recuperar senha." | `heuristic-eval` | "Converte este componente de classe para function component com hooks." |
| "O foco do modal some quando eu fecho. O que a WCAG pede?" | `a11y-checklist` | "Escreve o README do projeto com instruções de instalação." |
| "Reescreve as mensagens de erro do cadastro, estão secas." | `ux-writing` | "Roda os testes e corrige o que falhar." |
| "Tenho hex espalhado no CSS; quero tokens e modo escuro." | `design-tokens` | "Qual a melhor estratégia de cache para esta API?" |
| "Monta um roteiro de entrevista de 50 minutos para entender como as pessoas cancelam a assinatura." | `user-research-plan` | "Cria uma migration para adicionar a coluna avatar_url." |
| "Review this dashboard design and tell me what feels off." | `ui-audit` | "Translate this commit message to Portuguese." |
| "Write an empty state for the projects list." | `ux-writing` | "Faça o deploy da versão atual para staging." |
| "Does this form meet WCAG 2.2 AA?" | `a11y-checklist` | "Otimiza o bundle: o LCP está em 4 s." (é de `web-frontend`) |

Para o caso de fronteira "implementa este componente em React com Tailwind": não deve disparar `design-brief` (use um teste extra do conjunto). Rodar em Haiku, Sonnet e Opus e registrar tokens e tempo.
