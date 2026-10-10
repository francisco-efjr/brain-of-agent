# Árvore de agência, padrões e orçamento de contexto

Base: V-04 (Building effective agents, 19/12/2024, com aviso de que parte das ferramentas descritas mudou), V-06 (context engineering, 29/09/2025), V-17 (code execution com MCP), V-39 (superfícies de agente), V-07 (custo). Use a taxonomia, não os exemplos de ferramenta do texto de 2024. Conferido em 2026-10-10.

## Árvore de decisão com exemplos

| Pergunta | Se sim | Exemplo | Se não |
| --- | --- | --- | --- |
| 1. Uma chamada bem instruída resolve? | Pare. Meça na tarefa real | Classificar um ticket em uma de 6 categorias com 3 exemplos no prompt | Pergunta 2 |
| 2. Os passos são conhecidos de antemão? | Workflow (abaixo) | Classificar, escolher o modelo por categoria, responder, validar formato | Pergunta 3 |
| 3. As subtarefas são imprevisíveis? | Orquestrador-trabalhadores | Corrigir um bug que pode tocar de 1 a 8 arquivos, descobertos ao ler | Pergunta 4 |
| 4. Existe critério de qualidade verificável? | Acrescentar avaliador-otimizador, com limite de iterações | Tradução revisada até passar num glossário; código até passar nos testes | Seguir sem laço de melhoria |
| 5. Passos imprevisíveis e ambiente confiável? | Agente: parada, teto de custo e de iterações, sandbox, aprovação para escrita externa | Assistente de código que roda testes num sandbox | Mantenha workflow |

Framework: só depois de entender o prompt e a resposta crus da API (V-04). Frameworks acrescentam camadas que escondem o que é enviado ao modelo.

## Os cinco padrões (V-04), em uma linha cada

| Padrão | Quando | Cuidado |
| --- | --- | --- |
| Encadeamento (prompt chaining) | Tarefa decomponível em etapas fixas | Checagem em código entre etapas; cada etapa com saída tipada |
| Roteamento | Entradas de categorias distintas pedem tratamento distinto | Classificador medido; rota padrão para o desconhecido |
| Paralelização (seções ou votação) | Partes independentes, ou várias tentativas para votar | Custo multiplica; defina como combinar |
| Orquestrador-trabalhadores | Subtarefas imprevisíveis | Briefing completo por trabalhador (ver delegacao-e-harness.md) |
| Avaliador-otimizador | Critério de qualidade claro e iteração ajuda | Limite de iterações; avaliador separado do gerador |

## Orçamento de contexto (V-06, V-17, V-03)

Pergunta-guia: qual é o menor conjunto de tokens de alto sinal que torna o resultado correto provável?

| Situação | Técnica | O que preservar |
| --- | --- | --- |
| Conversa longa | Compactação | Decisões, bugs abertos, restrições do usuário; limpar saída antiga de tool primeiro |
| Trabalho por marcos | Notas estruturadas fora da janela (arquivo de progresso, `features.json`) | Estado atual, próximo passo, decisões com motivo |
| Pesquisa paralela ou leitura volumosa | Subagentes com contexto limpo que devolvem resumo | Formato do resumo e fontes |
| Dado pequeno e estável | Pré-carregar no prompt (e cachear: ver `llm-decision-gates`) | Ordem estável para o cache |
| Dado grande ou mutável | Referência (caminho, consulta) e busca na hora | Como buscar, não o conteúdo |
| Muitas tools/servidores MCP | Poucos servidores; filtrar e agregar no ambiente de execução; tokenizar campos sensíveis | Contagem das definições carregadas (V-17: caso de 150.000 para 2.000 tokens é específico, não extrapolar) |

Prompt de sistema: começar mínimo e acrescentar só o que um teste falho revelou; evitar if/else frágil e vagueza; poucos exemplos canônicos em vez de lista de casos (V-06). Em modelos Claude 5, preferir julgamento a regras e referências executáveis a prosa (V-03).

Compactação: o resumo deve preservar problemas resolvidos e como, opções descartadas, pendências e restrições do usuário (V-02). A API de compactação, a memory tool e a edição de contexto **não foram lidas** (lacuna 4 do design): não descreva parâmetros; abra a página da plataforma antes.

## Superfície de agente (V-39)

| Necessidade | Escolha |
| --- | --- |
| Agente de código pronto dentro do meu processo (Python/TypeScript), com tools embutidas, hooks, subagentes, MCP, permissões, sessões | Agent SDK |
| Uso interativo diário ou tarefa pontual | CLI |
| Controle total do laço, do prompt e das tools | SDK cliente (o laço é seu ou do tool runner beta) |
| Não operar a infraestrutura do agente | Managed Agents (a Anthropic hospeda o laço) |
| Outra linguagem | CLI em subprocesso com `-p` e `--output-format json` |

Para agente sem supervisão: limite de turnos e de orçamento, modo de permissão restritivo, hooks de segurança, sandbox; produto de terceiro usa autenticação por chave de API; terceiros não podem oferecer login claude.ai nem limites próprios sem aprovação (V-39). Não li as páginas de agent loop, hooks e permissões do SDK nem os notebooks: **Não verificado**.

## Quando a resposta é "workflow": exemplo do pedido de triagem

Pedido: "classifico tickets em 6 categorias e respondo com modelo por categoria; os passos são sempre os mesmos; tenho 2.000 tickets rotulados; meu colega quer orquestrador com 6 agentes."

1. Baseline: uma chamada com a lista de categorias e 3 exemplos por categoria; medir acerto e matriz de confusão nos 2.000 tickets (reservar parte como validação).
2. Se o acerto basta: pare (chamada única + modelo de resposta por categoria em código).
3. Se há confusão entre classes: roteamento (classificador) + encadeamento (resposta + validação de formato em código). Os passos são conhecidos, então não é caso de orquestrador.
4. Multiagente (6 agentes) só se a medição mostrar ganho que paga cerca de 15 vezes os tokens (ordem de grandeza do fabricante, V-07); caso contrário é complexidade sem retorno.
5. Parada e eval: teto de chamadas por ticket, classe crítica com falso negativo contado à parte, 3 execuções para variabilidade.

Rótulos: a recomendação é **Inferida** a partir de V-04 e V-07; a medição nos 2.000 tickets é o que a confirma ou derruba.
