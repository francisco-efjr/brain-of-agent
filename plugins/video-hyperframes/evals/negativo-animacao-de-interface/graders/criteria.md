---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Responde direto com código de um modal em React com Tailwind: usa classes de transição ou animação do Tailwind (por exemplo `transition`, `duration-200`, `opacity-0`, `scale-95`), cobre fade e scale e a duração de 200 ms, e controla a entrada com estado (montar o elemento e depois aplicar o estado final) ou com keyframes.
2. Respeita `prefers-reduced-motion`: por exemplo com a variante `motion-reduce:` do Tailwind, com uma media query, ou removendo a transição nesse caso.
3. Não menciona HyperFrames, storyboard, quadros, contact sheet, MP4 ou render, e não propõe criar um vídeo.
FAIL if qualquer um ocorrer: menciona ou usa HyperFrames, storyboard, GSAP de vídeo, snapshot ou render; trata o pedido como produção de vídeo; ignora `prefers-reduced-motion`; devolve só texto sem código.
