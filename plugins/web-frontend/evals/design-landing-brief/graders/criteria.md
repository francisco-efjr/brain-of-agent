---
type: llm
---
PASS if todos os itens abaixo são observáveis no transcript e na resposta final:
1. Antes de qualquer código de página (antes do primeiro arquivo gravado ou bloco de código de componente), apresenta um brief de três linhas (assunto, público, tarefa principal: pedir amostra) e um plano com: 4 a 6 cores nomeadas em hex ou oklch, papéis tipográficos (uma ou duas famílias), conceito de layout com wireframe em ASCII e princípios derivados do assunto (café especial de cooperativa), não regras genéricas.
2. Faz uma revisão explícita do plano contra o genérico e registra pelo menos uma troca no formato "mudei X porque Y".
3. Depois do plano, ou espera confirmação, ou, em execução sem interação, segue como rascunho listando as confirmações pendentes; em ambos os casos a ordem plano antes do código é respeitada.
4. A implementação usa tokens como variáveis em `@theme` (Tailwind v4) e não cria `tailwind.config.js` em estilo v3; contempla 320 px sem rolagem horizontal, foco visível em links e botões, contrapartida em `prefers-reduced-motion` para qualquer animação e HTML semântico; o CTA é específico (por exemplo "Pedir amostra"), não genérico.
5. O conteúdo é em português do Brasil, sem lorem ipsum; qualquer fato da cooperativa que o usuário não forneceu (certificações, prêmios, números de produtores ou de sacas, endereços) fica fora ou aparece marcado como texto de exemplo a substituir.
6. Fecha dizendo o que fez e o que não foi verificado (por exemplo captura de tela em 320 px e desktop, contraste medido, build); não afirma ter capturado screenshots nem rodado o build sem ter executado.
FAIL if qualquer um ocorrer: despeja código antes do plano; usa o gradiente roxo-azul padrão, fonte padrão sem motivo ou kit de três cartões iguais como identidade sem justificar; usa lorem ipsum; inventa certificações, prêmios ou números como fatos; afirma ter tirado screenshot ou rodado build sem ferramenta para isso; usa convenção Tailwind v3 num projeto declarado v4.
