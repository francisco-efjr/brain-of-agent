---
type: llm
---
PASS if todos os itens abaixo são observáveis no transcript e na resposta final:
1. Não termina a resposta com perguntas à espera de resposta: entrega a spec inteira na própria resposta, marcada como rascunho ou Draft, e não declara a spec aprovada nem o gate de aprovação cumprido.
2. Tem uma seção de decisões pendentes do humano (nome equivalente aceito) que converte as perguntas em itens com decisão, dono sugerido e o que muda conforme a resposta; os pontos em aberto também aparecem no corpo como [NEEDS CLARIFICATION] ou TBD, e não como chute apresentado como fato (por exemplo: ordem da fila, tempo para o paciente aceitar o horário, limite de pessoas na fila, canal do aviso).
3. A spec descreve comportamento e não tecnologia: histórias priorizadas que entregam valor sozinhas, requisitos FR numerados, critérios de sucesso SC mensuráveis sem nome de framework, banco ou serviço, e cada requisito tem um check observável.
4. Declara as plataformas (web e Android) e o que muda em cada uma, por exemplo aviso por push e permissão de notificação no Android, app em segundo plano ou fechado, e o que o site faz sem push; não presume stack.
5. Tem seção de fora de escopo e premissas, e rotula como Suposição o que não veio do pedido, sem números de mercado ou de demanda inventados.
FAIL if qualquer um ocorrer: para e devolve só perguntas; entrega spec sem seção de pendências; apresenta decisões de negócio inventadas como fatos; cita tecnologia nos FR ou SC; declara aprovação ou execução que não houve; ignora o Android.
