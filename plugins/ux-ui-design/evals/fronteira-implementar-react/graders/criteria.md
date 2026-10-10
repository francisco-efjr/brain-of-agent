---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Entrega o código do componente `ProductCard` em TypeScript com Tailwind, com interface de props tipada conforme o pedido, e um exemplo de uso curto; responde direto, no tamanho pedido, sem preâmbulo longo.
2. O preço é recebido em centavos e formatado em reais com `Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' })` ou equivalente correto (divisão por 100), sem concatenar "R$" manualmente com número de ponto flutuante mal formatado.
3. Implementa os estados pedidos: carregando (esqueleto no lugar do conteúdo) e esgotado (botão indisponível com o texto "Esgotado"), e o botão normal chama `onAdd`.
4. O código é minimamente correto e acessível sem virar tema do pedido: `<button type="button">`, `alt` na imagem (nome do produto ou `alt=""` justificado), classes de foco visível do Tailwind no botão; qualquer nota sobre acessibilidade é curta.
5. Não impõe etapa de plano de design, brief, aprovação nem auditoria antes de entregar o código; não pergunta nada que bloqueie a entrega.
FAIL if qualquer um ocorrer: entrega só um plano, uma auditoria ou perguntas em vez do código; recusa por "ser design"; aciona design-brief ou ui-audit; usa classes ou APIs inexistentes de forma que o código não funcione; formata o preço em reais de modo incorreto (por exemplo mostrar centavos como reais); omite um dos estados pedidos.
