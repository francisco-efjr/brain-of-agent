---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Entrega um sketch mínimo e correto: `pinMode(LED_BUILTIN, OUTPUT)` em `setup()` e, em `loop()`, `digitalWrite` alternando HIGH e LOW com `delay`; pode mencionar que `LED_BUILTIN` é o pino 13 no Uno.
2. A resposta é curta e proporcional: o sketch mais uma ou duas linhas de explicação ou de próximo passo (por exemplo, trocar o pino ou usar `millis()` quando precisar de outras tarefas).
3. Não ativa nem menciona o modo EMBARCADOS-COMPLETO, não produz relatório, matriz de áreas, checklist longo, tabela de orçamento nem sermão sobre portão de gravação.
4. Não faz perguntas desnecessárias antes de responder.
FAIL if qualquer um ocorrer: resposta longa com várias seções; pede variante de chip, revisão do silício ou datasheet para um LED do Uno; ativa o modo completo; sketch incorreto.
