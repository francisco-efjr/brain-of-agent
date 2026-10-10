# Decisões e trade-offs

Conflitos reais entre fontes e a resolução adotada, em forma de decisão. Quando duas recomendações parecem disputar, use a árvore correspondente e registre qual caminho foi seguido. Itens `V-nn` estão em `fontes.md`.

## Sumário

- [Tamanho de alvo (C1)](#tamanho-de-alvo-c1)
- [Evitar defaults ou obedecer a marca (C2)](#evitar-defaults-ou-obedecer-a-marca-c2)
- [Hooks e gates automáticos (C3)](#hooks-e-gates-automáticos-c3)
- [Ler código ou só o renderizado (C4)](#ler-código-ou-só-o-renderizado-c4)
- [Auditar e corrigir no mesmo passo (C5)](#auditar-e-corrigir-no-mesmo-passo-c5)
- [Avaliadores humanos ou modelo (C6, C14)](#avaliadores-humanos-ou-modelo-c6-c14)
- [Quantos participantes (C7)](#quantos-participantes-c7)
- [DTCG: padrão ou não (C8)](#dtcg-padrão-ou-não-c8)
- [Contagem e data da WCAG 2.2 (C9)](#contagem-e-data-da-wcag-22-c9)
- [Linter como oráculo de contraste (C10)](#linter-como-oráculo-de-contraste-c10)
- [Apple como referência (C11)](#apple-como-referência-c11)
- [Regras de polegar (C12)](#regras-de-polegar-c12)
- [CLAUDE.md curto contra muitas regras (C13)](#claudemd-curto-contra-muitas-regras-c13)
- [Onde colocar cada coisa](#onde-colocar-cada-coisa)
- [Gate de aprovação humana](#gate-de-aprovação-humana)
- [Quando pedir usuários reais](#quando-pedir-usuários-reais)
- [Card sorting ou tree testing](#card-sorting-ou-tree-testing)

## Tamanho de alvo (C1)

Pergunta: qual tamanho mínimo de alvo adoto?

- Alvo é web e o requisito é WCAG 2.2 AA → **24×24 px CSS** (2.5.8) como piso, com as exceções do critério.
- Alvo é toque em web mobile → meta de **44 px** (convenção; V-27).
- Alvo é iOS, iPadOS ou macOS → números da HIG: iOS/iPadOS 44 pt padrão e 28 pt mínimo; macOS 28 e 20 (V-39).
- Alvo é Android → 48 dp aparece em trechos de busca e no brain, mas é **Não verificável** aqui (Material 3 é lacuna).
- Nunca escreva "44 sempre": a HIG tem 28 pt como mínimo.

## Evitar defaults ou obedecer a marca (C2)

Pergunta: a lista de anti-padrões ou o briefing?

- Existe marca, `DESIGN.md` ou tokens → eles vencem; a lista vira checagem de consistência.
- Não existe marca → aplique a lista, registre a justificativa de cada escolha e teste com e sem o bloco anti-convergência em 3 tarefas.
- A lista coincide com a sua escolha → troque ou justifique pelo briefing. A lista envelhece: revise a cada 6 meses.

## Hooks e gates automáticos (C3)

Pergunta: automatizo a verificação com hook?

- O plugin nunca ativa hooks. Documente o hook em `ferramentas-e-mcp.md` com o risco e deixe o usuário habilitar.
- Se o usuário habilitar, preserve a regra: gate ausente nunca vira aprovação.
- Instrução em CLAUDE.md é pedido; hook é garantia; nenhum dos dois é fronteira de segurança (use sandbox e permissões).

## Ler código ou só o renderizado (C4)

O `design-review` do gstack diz para nunca ler código-fonte; V-26 pede ler o sistema de design do código. Resolução: `ui-audit` avalia o renderizado ou o markup fornecido e lê apenas tokens, variáveis e tema como contexto antes de julgar. Desvio do sistema pesa mais.

## Auditar e corrigir no mesmo passo (C5)

O gstack audita, corrige e comita por achado. Aqui a auditoria é somente leitura; a correção é outro pedido, com diff revisável e sem commit automático. Motivo: auditoria não altera produto, e commit automático é efeito externo.

## Avaliadores humanos ou modelo (C6, C14)

- NN/g pede 3 a 5 avaliadores humanos independentes. Com um modelo: 2 ou 3 passadas independentes em contextos separados, consolidar por agrupamento, rotular Inferido e recomendar usuários reais para os 3 achados mais graves.
- "3 a 5" é o número de **avaliadores** de uma avaliação heurística; "5" é o número de **participantes** de um teste de usabilidade qualitativo. Nunca os troque nem some.

## Quantos participantes (C7)

Cinco para um estudo qualitativo com um grupo de usuários (NN/g). "Recrutar 7 para agendar 5" e "6 de 8 é sinal" são heurísticas do autor de V-16: cite como tal. Com n pequeno não se afirma significância estatística nem taxa.

## DTCG: padrão ou não (C8)

O relatório 2025.10 se descreve como "Final Community Group Report" e também usa "Candidate Recommendation", mas declara não ser padrão W3C. Cite "relatório final de comunidade 2025.10, não padrão W3C"; fixe a versão no nome do arquivo, em `$description` de grupo ou na configuração do build (a spec 2025.10 não define `$schema` na raiz; conferido em 2026-10-10); o rascunho de 2026-09 diz "preview, não implemente": não dependa dele.

## Contagem e data da WCAG 2.2 (C9)

86 critérios (78 do 2.1 mais 9 novos menos 4.1.1); Recommendation vigente de 2024-12-12 (a original é de 2023-10-05). 4.1.1 foi removido: não reporte "HTML inválido", reporte o efeito.

## Linter como oráculo de contraste (C10)

A saída de exemplo do linter do `design.md` (15,42:1 para #FFFFFF sobre #1A1C1E) não bate com a fórmula WCAG (17,09:1). Calcule pela fórmula ou meça no estado real; não use a mensagem do linter como prova.

## Apple como referência (C11)

Os números da HIG valem quando o alvo é iOS, iPadOS ou macOS. Em web e Android são só comparação. Não migre para nativo por estética (brain: "Apple é preferência, não ranking nem norma universal").

## Regras de polegar (C12)

Listas de fontes "banidas", razões de escala, durações de movimento e pesos de nota do gstack são escolhas de um autor: Inferido. Fonte de exibição genérica é sinal de alerta, não erro. Operate pode usar sans neutra no corpo se o `DESIGN.md` disser.

## CLAUDE.md curto contra muitas regras (C13)

Só blocos de 3 a 8 linhas entram no CLAUDE.md (`claude-md-snippets.md`); o conhecimento longo fica em `references/` e skills, carregado sob demanda. Teste de corte: se remover a linha não faria o agente errar, remova.

## Onde colocar cada coisa

Árvore (prompt-principles P-38) e matriz de recurso (V-07):

| Você quer | Recurso | Observação |
| --- | --- | --- |
| Garantia que vale sempre (rodar o build de tokens após editar) | Hook | Executa shell; documentado, nunca ativado pelo plugin; guardrail, não segurança |
| Fato universal e curto do projeto | CLAUDE.md | Menos de 200 linhas; só o que o agente não descobre lendo o repo |
| Regra para certos arquivos | Regra com `paths` (`.claude/rules`) | Conferir a sintaxe na doc da versão instalada |
| Tarefa com gatilho e processo | Skill | Carrega sob demanda |
| Tarefa isolada em contexto limpo | Subagente | Não herda CLAUDE.md nem output style com garantia: repita as regras críticas |
| Voz e formato da sessão | Output style | Instrução, não garantia; não usar `force-for-plugin` (impõe o estilo ao usuário); subagentes (exceto fork) não herdam |
| Capacidade externa (navegador, Figma) | MCP | Superfície de ataque; desativado por padrão |

## Gate de aprovação humana

Pare e espere confirmação (1) depois do plano de design em redesenho amplo, (2) antes de qualquer renomeação de token de marca, (3) antes de gravar `DESIGN.md` ou alterar o CLAUDE.md, (4) antes de qualquer ação externa. Em ajuste pequeno, siga e registre suposições. Cada lacuna de um plano de UI recebe uma decisão individual do usuário, sem aplicar em lote.

## Quando pedir usuários reais

Peça pesquisa com usuários quando: o achado de severidade 3 ou 4 depende de comportamento (não de regra normativa); o trade-off é defensável dos dois lados; há tarefa crítica de negócio (cadastro, pagamento); a decisão é cara de reverter. Dispense quando: a violação é normativa e mecânica (contraste, rótulo ausente, foco invisível); o ajuste é reversível e barato. A crítica do modelo serve para priorizar o que levar aos usuários, não para substituí-los.

## Card sorting ou tree testing

Ainda não sei agrupar → card sorting (descoberta). Já tenho estrutura → tree testing com tarefas de encontrar item (sucesso, caminho direto, tempo). Os dois juntos são o melhor caso. Tamanhos de amostra: lacuna; ler os artigos completos do NN/g antes de afirmar números.
