---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Faz até 5 perguntas de esclarecimento (por exemplo: tolerância a atraso e a duplicata, ordem, volume de push contra e-mail, provedores, dados pessoais) ou declara as Suposições adotadas para seguir; não faz mais de 5 perguntas.
2. Estima ordem de grandeza no próprio texto (envios por segundo no pico, volume diário, armazenamento de histórico e de preferências) com cada premissa rotulada como Suposição e a conta visível (por exemplo 50 mil por minuto corresponde a cerca de 830 por segundo).
3. Inclui um diagrama Mermaid de no máximo 15 nós, em um único nível de abstração.
4. Apresenta trade-offs em tabela (por exemplo fila gerenciada contra broker próprio, entrega at-least-once com deduplicação, custo, complexidade) e a alternativa mais simples.
5. Descreve modos de falha por dependência (provedor de e-mail ou push indisponível, fila cheia, duplicata) com estratégia de retry em uma camada com limite e jitter, idempotência no envio e dead-letter queue; só adiciona padrões que um modo de falha justifique.
6. Declara o que não construir agora e lista decisões pendentes com dono humano.
FAIL if qualquer um ocorrer: números sem premissa declarada; diagrama com mais de 15 nós ou misturando níveis; afirma ter executado scripts ou benchmarks; propõe microsserviços, CQRS ou event sourcing sem requisito que os justifique; promete entrega exactly-once.
