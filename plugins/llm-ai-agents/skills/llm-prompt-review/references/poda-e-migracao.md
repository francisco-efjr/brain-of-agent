# Poda de prompt e migração entre modelos

Base: V-03 (regras de context engineering para a geração Claude 5; artigo de opinião do fabricante, sem medição publicada na página lida), V-01 (migração de prefill), V-02 (blocos da família 5.1) e prompt-principles P-11. Registre modelo-alvo e data em toda poda; resultado de um modelo não vale para o outro.

## Poda: 6 perguntas (rodar a cada troca de modelo)

| # | Pergunta | Como testar | Se a resposta for sim |
| --- | --- | --- | --- |
| 1 | Cada regra "sempre/nunca" ainda é necessária? | Remover a regra e rodar as 3 tarefas de teste | Se o comportamento não piorou, a regra sai |
| 2 | Algum exemplo trava a exploração do modelo? | Comparar saída com e sem o exemplo; ver se a saída copia o exemplo | Trocar o exemplo por um parâmetro, enum ou critério |
| 3 | A instrução de uso de uma tool está no system prompt e na descrição da tool? | Grep pelo nome da tool no prompt | Manter só na descrição da tool (não repetir instruções entre system prompt e tool) |
| 4 | O conhecimento é ocasional (usado em 1 de cada 10 turnos)? | Contar quando é relevante | Virar skill ou referência carregada sob demanda |
| 5 | O prompt (ou CLAUDE.md) só tem o que o código não revela? | Para cada linha: "o modelo descobriria isso lendo o repositório?" | Remover a linha |
| 6 | Uma referência executável substitui a prosa? | Existe suíte de testes, mockup ou rubrica que diga o mesmo? | Apontar para o artefato em vez de descrever |

Princípio por trás: preferir julgamento a regra rígida ("escreva código que lê como o código ao redor" em vez de "sem comentários") e interfaces expressivas (enums, parâmetros) a listas de exemplos (V-03). O resultado da poda é uma hipótese até a rodada de teste: **Inferido** até medir.

## Migração entre modelos: procedimento

1. Congelar a baseline: as 3 tarefas de teste (uma falha conhecida, uma que já funcionava, uma de borda), prompt atual e saída atual salvos.
2. Remover truques de geração antiga: ameaça, gorjeta, repetição, anti-preguiça ("seja exaustivo"), CAPS, "pense passo a passo" como muleta (prompt-principles AP-01, AP-04, AP-05, AP-08).
3. Reconstruir do menor prompt que preserva o contrato (objetivo, formato, limites, verificação) e acrescentar regra só após falha observada, cada uma com motivo.
4. Rodar as mesmas tarefas no modelo novo. Subir `effort` só se houver ganho medido (V-38).
5. Registrar modelo, data e resultado na ficha do prompt.
6. Ler os avisos de mudança do modelo novo. **Verificado** (página "Define tools", 2026-10-10): `tool_choice` `any`/`tool` retorna 400 em Opus 5.5, Sonnet 5.5, Fable 5.1 e Mythos 5.1; substituto: `auto` com `strict: true` ou saída estruturada. Desligar o raciocínio e usar `computer_20251124` no Opus 5.5: ler a página de migração antes (**Não verificado**).

## Tabela de obsoletos e substitutos

| Padrão antigo | Substituto | Rótulo |
| --- | --- | --- |
| Prefill (preencher a última mensagem do assistente, por exemplo com `{`) | Instrução de formato; saída estruturada (`output_config.format` com `json_schema`); tool use | **Verificado**: a página de prompting diz que prefill na última mensagem do assistente não é mais suportado a partir dos modelos Claude 4.6 (V-01) |
| `budget_tokens` em extended thinking | Thinking adaptativo com `effort` | **Verificado** (página de extended thinking, 2026-10-10): obsoleto na 4.6, erro 400 a partir do 4.7; usar `type: "adaptive"` com `output_config.effort` |
| CAPS, `CRITICAL: You MUST`, "NEVER" repetido | Motivo + linguagem normal; ênfase em uma linha após falha observada | **Verificado**: a página diz que Opus 4.5/4.6 podem acionar ferramentas em excesso com esse tom (V-01) |
| "Se em dúvida, use a ferramenta" | Critério de quando buscar e orçamento de chamadas | **Inferido** (prompt-principles AP-08) |
| "Pense passo a passo" em modelo com raciocínio | Pedir verificação contra critério; ajustar `effort` | **Verificado** em parte: V-01 e V-37 (em campo de schema pode causar recusa `reasoning_extraction`) |
| Tabela de 40 casos "se A então B" | Princípio + 3 a 5 exemplos canônicos + caso de borda | **Verificado** (V-06, V-03) |
| `temperature`/`top_p` ajustados por hábito | Padrão do modelo; mudar só com medição | **Inferido** (prompt-principles AP-06) |

## Blocos de comportamento da família Fable/Mythos 5.1 (V-02): condicionais

Aplique um bloco por vez, só se o comportamento correspondente foi observado, comparando com e sem o bloco em 3 tarefas reais. Em outro modelo, podem causar excesso de autonomia. Redação própria (V-02, classe A, ressalvas na fonte):

- Autonomia: "Execute o pedido até o fim. Passos reversíveis que fazem parte do pedido não precisam de autorização. Pare e pergunte antes de ação destrutiva, irreversível ou que amplie o escopo. Antes de encerrar, se o último parágrafo for um plano ou uma promessa, execute-o com as ferramentas."
- Escopo: "O pedido define o entregável. Problemas encontrados fora dele entram numa lista de sugestões no fim do resumo, sem alterar nada."
- Ambiguidade: "Se houver duas leituras, adote a mais direta, declare a suposição no resumo e pergunte só se as leituras levariam a trabalhos materialmente diferentes."
- Compactação: "Ao resumir, preserve problemas e como foram resolvidos, opções descartadas, pendências e restrições do usuário."

Por que não ativar por padrão: a fonte lista essas seções por título; a utilidade dos blocos é **Inferida** (V-02).

## Contraste com outros fabricantes (V-46, classe B, só contraste)

Convergências com o guia da Anthropic, tratáveis como consenso: confirmar antes de ação irreversível, delimitadores e estrutura, contexto longo antes da instrução, few-shot sem exagero, decompor tarefas, dar uma saída ao modelo, pedir citação. Divergências a medir, não adotar: repetir a instrução no fim (guia da Microsoft, com aviso de que as técnicas não valem para modelos de raciocínio), temperatura (Google: manter o padrão no Gemini 3.x; Microsoft: mudar um parâmetro por vez), cadeia de pensamento explícita. Duas afirmações dessas páginas não foram reconfirmadas pelo validador (data da página do Google; recomendação de temperature/top_p da OpenAI): **Não verificado**.

## Quando a poda não vale

- Prompt de segurança (política de conteúdo não confiável, confirmação de ação irreversível): não podar por "ainda funcionar sem"; o teste de remoção não mede o que só aparece sob ataque.
- Prompt sem baseline: sem as 3 tarefas, a poda é palpite; primeiro monte o teste.
