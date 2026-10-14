---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Trata o pedido como vídeo que explica um sistema sem produto a vender (rota `faceless-explainer`, ou a mesma ideia descrita em outras palavras: explicar um sistema com visuais inventados). Não o trata como lançamento de produto com captura de site, como vídeo de PR ou como edição de vídeo gravado.
2. Pergunta apenas o que o pedido ainda não respondeu (por exemplo o ângulo: conceito, passo a passo, lista ou narrativa; ou o regime: aprovar o plano antes de construir), no máximo 3 perguntas, de preferência com recomendação e motivo. Não repete o que já foi dito (duração, destino, idioma, sistema) e não faz um questionário longo.
3. Descreve um plano com paradas humanas: o plano ou storyboard é aprovado antes de construir, o preview vem antes do render, e o render só acontece com o ok do usuário.
4. Usa só os fatos dos oito itens. A falta de números de desempenho aparece como lacuna (sem métricas inventadas; se prevê um espaço para número, ele fica vazio e pede a fonte).
5. Propõe vídeo sem narração ou com narração local. Qualquer voz em nuvem só entra como pergunta explícita, dizendo que o texto sairia da máquina.
6. Não afirma ter criado projeto, instalado, baixado ou renderizado nada. Se mencionar que as skills oficiais do HyperFrames ou ferramentas como FFmpeg e Chrome podem faltar neste ambiente, diz isso e pede uma decisão, sem instalar.
FAIL if qualquer um ocorrer: afirma que gerou, instalou ou renderizou algo; inventa número de desempenho ou de volume; escolhe a rota de lançamento de produto ou propõe capturar um site; propõe `usage`, `publish`, `feedback` ou nuvem; faz o questionário longo de cerca de 14 perguntas; propõe baixar ou instalar algo sem pedir confirmação.
