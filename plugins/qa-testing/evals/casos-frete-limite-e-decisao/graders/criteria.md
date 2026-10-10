---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Usa tabela de decisão (completa com 8 combinações ou colapsada com «–» e justificativa) para as condições subtotal a partir de 199, cupom válido e cliente VIP.
2. Aplica valor-limite com três valores no subtotal (198,99, 199,00 e 199,01) e deixa claro que o limite é a partir de 199,00.
3. Cada caso tem dados concretos e esperado calculado em reais (por exemplo VIP com cupom e subtotal 150,00: desconto 15,00, frete 0,00, sem os 5%), ID, prioridade e técnica.
4. Declara ou pergunta as ambiguidades antes de assumi-las: o limite de 199 vale antes ou depois do cupom, e o limite é inclusivo; marca o esperado afetado como «a confirmar» ou declara a suposição.
5. A entrega vem em tabela fácil de colar e mantém uma condição inválida por caso.
FAIL if qualquer um ocorrer: casos genéricos sem dados («testar com cupom válido»); esperado «funciona corretamente»; ignora o limite de 199,00; mistura duas condições inválidas no mesmo caso; assume em silêncio uma resposta para a ambiguidade.
