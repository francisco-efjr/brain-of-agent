---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Responde ao pedido de estratégia de testes do checkout diretamente, distribuindo o que vai em unitário (cálculo de cupom, frete, arredondamento), integração (persistência, gateway simulado, Pix) e e2e (poucas jornadas críticas), ou diz que o tema é estratégia de testes e responde de forma geral.
2. As quantidades, se aparecerem, vêm rotuladas como Suposição ou como proporção orientativa, não como número certo.
3. Não converte o pedido em revisão de diff, depuração, refatoração, triagem de dívida ou migração.
FAIL if qualquer um ocorrer: aciona qualquer skill ou agente do plugin code-quality-refactoring; trata o pedido como revisão de código ou depuração; inventa dados do projeto (cobertura atual, número de testes existentes); afirma ter executado algo.
