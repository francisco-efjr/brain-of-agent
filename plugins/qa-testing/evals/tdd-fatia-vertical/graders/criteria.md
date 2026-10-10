---
type: llm
---
PASS if todos os itens abaixo são observáveis no transcript e na resposta final:
1. O primeiro teste é escrito (ou apresentado) antes da implementação de `src/frete.py`; a ordem das escritas no transcript mostra o teste primeiro.
2. Declara qual falha vermelha espera e por quê (função ou comportamento ausente, não erro de import ou sintaxe) e diz que não pôde executar; se executar, cola a falha real.
3. Os valores esperados são literais independentes (1500 para sul, 3000 para norte, 0 para frete grátis) e os limites do frete grátis são testados com 19899, 19900 e 19901 centavos.
4. Trabalha em fatias verticais (um comportamento por vez), não todos os testes e depois todo o código.
5. Cobre a região desconhecida com `ValueError`.
6. Implementa o mínimo para passar e menciona o mutation check (por exemplo trocar `>=` por `>` deve derrubar o teste do limite 19900) ou o motivo de não fazê-lo.
FAIL if qualquer um ocorrer: implementa antes de testar; calcula o esperado chamando `calcular_frete`; escreve todos os testes de uma vez e depois todo o código sem fatias; afirma que os testes passaram sem ter executado; omite o limite de 199,00; edita ou apaga testes para fazer passar.
