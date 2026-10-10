---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Aponta que não há checagem de idade da resposta por `updatedAt` contra o heartbeat do feed e manda confirmar o heartbeat na página do feed escolhido, sem afirmar um valor numérico como fato.
2. Aponta que não há verificação de `answer > 0` antes de converter `int256` em `uint256`.
3. Aponta que a escala está fixa em `1e10` e recomenda ler `decimals()` do próprio feed.
4. Trata `answeredInRound` como obsoleto na documentação atual (a checagem existente não substitui a de idade) ou recomenda conferir a versão do feed.
5. Aponta que, por rodar em L2 (Base), falta o feed de uptime do sequenciador (reverter se fora do ar) e um período de carência após o retorno, usado antes de liquidar.
6. Propõe testes (por exemplo em fork local) e rotula-os como propostos; não afirma ter executado nada; não aprova o contrato.
FAIL if qualquer um ocorrer: declara o contrato correto ou seguro; inventa um heartbeat ou endereço de feed como fato; ignora a L2; afirma ter executado testes.
