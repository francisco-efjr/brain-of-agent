---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Explica corretamente que flexbox organiza itens em uma dimensão por vez (linha ou coluna) e grid organiza em duas dimensões (linhas e colunas ao mesmo tempo), e que os dois podem ser combinados.
2. Inclui um exemplo curto e coerente com o contexto de galeria de fotos (por exemplo grid com `repeat(auto-fill, minmax(...))` para a galeria e flexbox para a barra de legenda ou de filtros), com código que funcionaria.
3. Responde direto, em tamanho proporcional à pergunta, sem transformar o pedido em auditoria de UI, plano de design, checklist de acessibilidade ou revisão de tokens.
FAIL if qualquer um ocorrer: aciona qualquer skill ou agente do plugin ux-ui-design; afirma que um dos dois é sempre melhor; erra a definição (por exemplo diz que grid é unidimensional); entrega diretrizes de design, paleta ou acessibilidade que ninguém pediu.
