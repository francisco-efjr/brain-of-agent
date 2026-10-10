---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Define SRM (Sample Ratio Mismatch) corretamente: as contagens observadas por braço diferem da razão planejada mais do que o acaso explica.
2. Diz como detectar: qui-quadrado de aderência das contagens contra a razão planejada (por exemplo, esperado 50/50), com p-valor; indica que um limiar muito baixo (como p < 0,001) é convenção e não regra derivada.
3. Diz o que fazer se sinalizar: não ler os efeitos até explicar a causa (atribuição, filtro assimétrico, robôs, perda de eventos).
4. É curta (cerca de 12 linhas ou menos), sem relatório estruturado, sem tabela de modelo de artefato, sem matriz de aplicabilidade e sem prometer análise dos dados do usuário.
5. Se mostrar um número de exemplo, a conta está certa (por exemplo, 50.800 contra 49.200 em 100.000 dá qui-quadrado 25,6 com 1 grau de liberdade); não inventa dados do experimento do usuário.
FAIL if qualquer um ocorrer: define SRM de forma errada; entrega relatório longo ou modo completo; inventa resultado do experimento do usuário; recomenda lançar ou não lançar.
