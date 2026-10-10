---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Lista pelo menos 4 riscos escritos como falha → efeito (e não como nome de funcionalidade), cobrindo ao menos quatro destes: webhook perdido ou atrasado, webhook duplicado, webhook forjado ou sem verificação de origem, valor pago divergente do pedido, pagamento após expiração do PIX, estoque preso por pedido pendente; cada risco com nível (probabilidade e impacto, ou Alto, Médio, Baixo).
2. Define profundidade por nível e a menor camada que prova cada risco: por exemplo unitário para cálculo e estados, integração do handler com banco real para idempotência e duplicidade, contrato ou virtualização do PSP, poucos E2E no sandbox.
3. Entrega um plano que cabe em dois dias (blocos de tempo ou ordem de execução), diz o que fica fora do plano e inclui ao menos uma linha não funcional (segurança do webhook, desempenho ou acessibilidade) ou justifica a ausência.
4. Responde «está pronto?» como parecer condicional (GO com condições ou NO-GO) com critérios objetivos, e declara risco residual em linguagem de negócio (se evento, então efeito).
5. Sugere liberação gradual por flag e monitoramento, e não promete ausência de defeitos.
FAIL if qualquer um ocorrer: lista exaustiva sem prioridade; afirma «100% pronto» ou «sem bugs»; omite o risco residual; ignora a idempotência do webhook; trata números regulatórios como certos sem sinalizar que são a confirmar.
