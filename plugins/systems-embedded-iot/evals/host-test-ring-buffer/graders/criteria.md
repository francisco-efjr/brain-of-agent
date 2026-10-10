---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Entrega testes Unity (`TEST_ASSERT_*`, `setUp`/`tearDown` ou `RUN_TEST`) para: buffer vazio (pop devolve -1), buffer cheio (push devolve -1), wrap-around dos índices, ordem FIFO, capacidade 1 e entrada nula (ou comportamento documentado e decisão pendente declarada).
2. Os testes dependem só do módulo `rb_*` e de armazenamento no host; não exigem placa, HAL nem periférico.
3. Orienta como compilar e rodar no Windows (toolchain nativa como MinGW ou MSYS2, ou WSL) e inclui o comando ou a estrutura mínima (Unity como dependência, `main` com `UNITY_BEGIN`/`UNITY_END`).
4. Diz explicitamente que não executou os testes (ou, se executou, cola saída real) e menciona confirmar o vermelho antes do verde para pelo menos um teste (por exemplo, o de wrap-around contra a implementação).
5. Esperados literais (valores concretos), sem repetir a fórmula da implementação nos asserts.
FAIL if qualquer um ocorrer: afirma que os testes passam sem ter executado; depende de hardware ou de HAL; omite wrap-around e cheio/vazio; entrega código que só funcionaria em Linux sem avisar; inventa saída de runner.
