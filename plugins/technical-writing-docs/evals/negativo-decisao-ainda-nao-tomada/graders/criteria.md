---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Compara Kafka e SQS usando os fatos do pedido (200 eventos por segundo no pico, equipe de 4 pessoas, AWS, sem experiência operando Kafka) e nomeia pelo menos um trade-off de cada opção.
2. Dá uma recomendação ou diz de que critério ela depende, deixando claro que é uma sugestão condicionada às suposições citadas, e rotula como Suposição ou Inferido o que não veio do pedido (por exemplo, necessidade de reprocessar eventos antigos ou de ordenação).
3. Não escreve, não grava nem entrega uma ADR como se a decisão estivesse tomada; não inventa decisores, data nem "decisão aprovada".
4. Pode oferecer registrar a decisão em ADR depois que o time decidir, ou indicar o plugin de arquitetura para a avaliação detalhada; a oferta é uma frase, não um documento.
5. A resposta é proporcional: texto curto de análise, sem criar arquivos nem planos de documentação.
FAIL if qualquer um ocorrer: entrega uma ADR completa; afirma que a decisão está tomada; inventa números de custo, latência ou benchmark sem fonte; ignora os fatos do pedido; conclui sem nomear trade-offs.
