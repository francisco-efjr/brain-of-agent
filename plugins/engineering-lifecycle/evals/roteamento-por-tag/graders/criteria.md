---
type: llm
---
PASS se todos os itens abaixo são observáveis na resposta final, usando apenas o trecho do registro que veio no prompt:
1. Pedido 1 ("testar no navegador"): tag principal `testes-funcionais-playwright`; líder `qa-playwright` (playbook); fundamentos incluem `engineering-lifecycle` com `browser-testing-with-devtools` e `test-driven-development` (agente `test-engineer`), além de `qa-testing` e `web-frontend`; validador `qa-testing:test-auditor`. Não escolhe `tdd` nem `ui-producao` como tag principal.
2. Pedido 2 ("tem erro no console"): tag principal `ui-producao`; líder `web-frontend`; fundamentos incluem `engineering-lifecycle` com `frontend-ui-engineering` e `browser-testing-with-devtools`, além de `ux-ui-design`; validador `web-frontend:ui-evaluator`. Não escolhe `depuracao-causa-raiz` nem `testes-funcionais-playwright` como tag principal.
3. Pedido 3 ("refatora sem mudar o comportamento"): tag principal `simplificar-codigo`; líder `code-quality-refactoring`; fundamentos incluem `engineering-lifecycle` com `code-simplification`; validador `qa-testing:test-auditor`. Não escolhe `revisao-de-codigo` como tag principal: se a citar, é para dizer que ela não se aplica porque ninguém pediu revisão de um diff.
4. Cada linha traz a justificativa de uma frase sobre a tag mais parecida que ficou de fora.
5. Não inventa tag, plugin, skill ou agente que não esteja no trecho, e não afirma ter lido arquivos ou executado algo.
FAIL se qualquer pedido for roteado para outra tag principal, se líder e fundamentos forem trocados entre si, ou se algum nome vier de fora do trecho.
