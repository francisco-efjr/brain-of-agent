# Exemplo resolvido: dividir um épico, mapear uma fatia e planejar a sprint

Ilustrativo. Os dados fornecidos pelo usuário são só os do enunciado; todo o resto são propostas ou perguntas, rotuladas. Nada aqui é decisão de um time real.

## Sumário

- [Enunciado](#enunciado)
- [1. Palavras vagas e perguntas](#1-palavras-vagas-e-perguntas)
- [2. Fatias verticais propostas](#2-fatias-verticais-propostas)
- [3. Example Mapping da fatia 3](#3-example-mapping-da-fatia-3)
- [4. Sprint em três blocos](#4-sprint-em-três-blocos)
- [Divisão ruim, para comparar](#divisão-ruim-para-comparar)

## Enunciado

Épico: "Como lojista, quero gerenciar pedidos." Time de 3 devs, sprint de 2 semanas.

## 1. Palavras vagas e perguntas

| Trecho | Problema | Pergunta | Dono |
| --- | --- | --- | --- |
| "gerenciar" | verbo que esconde o comportamento | Quais ações o lojista faz com um pedido? (ver, atualizar status, cancelar, reembolsar, imprimir) | produto |
| "pedidos" | de qual canal e em que estados? | Estados existentes hoje? Pedidos de loja física entram? | produto |
| (implícito) permissão | quem mais acessa? | Funcionário da loja faz o mesmo que o dono? | produto/segurança |
| (implícito) efeitos em volta | o cliente é avisado? | Mudar status envia e-mail ou notificação ao cliente? | produto |
| (implícito) dados existentes | pedidos antigos | Há pedidos históricos que precisam aparecer? | engenharia |

Sem essas respostas, as fatias abaixo são hipóteses para discutir (Suposição).

## 2. Fatias verticais propostas

Padrões usados: por operação e por passo do fluxo (conhecimento estável do domínio, Inferido). Cada fatia atravessa dados, regra e interface e entrega algo que o lojista vê.

| # | Fatia | Valor visível | Dois critérios resumidos | Depende de | Perguntas abertas |
| --- | --- | --- | --- | --- | --- |
| 1 | Ver a lista de pedidos pagos mais recentes, com status | lojista deixa de abrir o banco ou planilha para saber o que vendeu | (a) pedido pago aparece com cliente, valor e status; (b) lista vazia mostra mensagem clara | nada | quais colunas? quantos por página? |
| 2 | Abrir o detalhe de um pedido | consegue conferir itens, endereço e pagamento antes de agir | (a) detalhe mostra itens e valores corretos; (b) pedido de outra loja não abre (permissão) | 1 | dado pessoal visível a quem? |
| 3 | Marcar pedido como enviado com código de rastreio | cliente passa a saber que o pedido saiu | (a) status muda para "enviado" e guarda o código; (b) pedido já cancelado não pode ser marcado | 2 | aviso ao cliente nesta fatia ou na seguinte? |
| 4 | Avisar o cliente da mudança de status | menos contato do cliente perguntando "cadê meu pedido" | (a) cliente recebe aviso ao enviar; (b) falha no envio do aviso não desfaz a mudança de status | 3 | canal (e-mail/WhatsApp)? |
| 5 | Cancelar pedido com motivo | lojista corrige erros e falta de estoque sem suporte | (a) cancelamento exige motivo e libera o estoque; (b) pedido enviado não cancela | 2 | reembolso é desta fatia? |
| 6 | Filtrar e buscar pedidos | acha um pedido específico rápido | (a) filtra por status e data; (b) busca por número do pedido | 1 | volume de pedidos que torna isto necessário? |

Escolhas explicadas:

- A fatia 1 é a menor que já entrega valor; vai primeiro.
- Reembolso foi deixado fora de propósito: costuma carregar regras financeiras e conformidade (vá para o segmento de pagamentos) e aparece como pergunta aberta.
- Não há fatia "criar tabela de pedidos" nem "tela de pedidos": seria divisão horizontal.

Veredicto INVEST resumido (perguntas-teste de V-18, Inferido): 1 e 2 passam; 3 e 4 só passam se a pergunta sobre o aviso for respondida (hoje dependem uma da outra); 5 depende da resposta sobre reembolso; 6 pode esperar.

## 3. Example Mapping da fatia 3

```text
[AMARELO] Como lojista, quero marcar um pedido como enviado, com o código de rastreio, para o cliente acompanhar.

[AZUL] Regra A: só pedidos pagos podem ser marcados como enviados
  [VERDE] Pedido pago -> pode marcar como enviado
  [VERDE] Pedido aguardando pagamento -> botão indisponível/recusa com motivo
[AZUL] Regra B: pedido cancelado não pode ser enviado
  [VERDE] Pedido cancelado -> recusa com mensagem
[AZUL] Regra C: código de rastreio é obrigatório?
  [VERMELHO] Dono: produto. Aceitamos envio sem código (entrega própria)?
  [VERDE] Código com formato inválido -> ?   (depende da resposta acima)
[VERMELHO] Dono: produto. Marcar como enviado dispara aviso ao cliente nesta fatia?
[VERMELHO] Dono: engenharia. Há pedidos antigos sem status "pago" explícito?
```

Leitura do mapa: 3 vermelhos (1 deles bloqueia a regra C); 3 azuis; regra C sem verde definitivo. Decisão recomendada: não está pronta; voltar com as respostas. Se não houver resposta em uma conversa curta, divida a regra C em fatia própria ("código de rastreio") e entregue A e B antes.

## 4. Sprint em três blocos

Contas com os números dados: 3 devs x 10 dias úteis = 30 pessoa-dias brutos. Capacidade líquida depende de ausências, eventos fixos e margem para imprevistos, que o time deve informar. Não aplico um fator de foco inventado.

1. **Por que esta Sprint é valiosa?** Proposta de meta (o time ajusta): "O lojista consegue ver os pedidos pagos e abrir o detalhe de qualquer um sem recorrer ao banco." Estaria ligada às fatias 1 e 2.
2. **O que pode ser feito?** Pergunta ao time: qual a capacidade líquida em pessoa-dias? Com a resposta do time, compare a soma das estimativas das fatias 1 e 2 (feitas pelo time, não por mim) com essa capacidade; só entra o que couber. Fatia 3 só entra se as 3 perguntas vermelhas forem respondidas antes do planejamento. Fatias 4 a 6 ficam no backlog ordenado.
3. **Como será feito?** Para cada fatia selecionada, tarefas de até 1 dia (V-44), por exemplo na fatia 1: "listagem com filtro padrão de pagos", "ordenação por data", "estado vazio", "teste de permissão". Cada tarefa tem verificação (teste ou conferência descrita). Definition of Done: critérios da história verificados, revisão feita, sem pergunta aberta sobre ela.
4. **Riscos**: pedidos antigos sem status explícito (pergunta de engenharia); permissão ainda indefinida; dependência da resposta sobre aviso ao cliente.

Decisão: do time. O plugin não registra prazo nem promete entrega.

## Divisão ruim, para comparar

| Fatia ruim | Por que falha |
| --- | --- |
| "Criar tabela e modelo de pedidos" | camada técnica; ninguém vê valor ao final |
| "API de pedidos" + "tela de pedidos" | duas metades dependentes; nenhuma é testável sozinha |
| "Gerenciar pedidos - parte 1/2/3" | divisão arbitrária por tamanho, sem valor nem critério |
| "Tudo de status" | mistura marcar, cancelar e avisar; regras demais num cartão |
