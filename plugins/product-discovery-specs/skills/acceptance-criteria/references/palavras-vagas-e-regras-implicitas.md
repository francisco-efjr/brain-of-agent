# Palavras vagas, regras implícitas e requisitos não funcionais

Checklist de revisão de requisito antes do código. Base própria (MIT, Francisco Edson): `brains/qa/references/requisitos-e-bdd.md` (V-42), adaptado para escrita de requisitos. O arquivo completo, com Example Mapping e três amigos, está em `${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/criterios-e-historias.md`.

## Sumário

- [Palavras vagas](#palavras-vagas)
- [Regras implícitas](#regras-implícitas)
- [Requisitos não funcionais esquecidos](#requisitos-não-funcionais-esquecidos)
- [Ruim x bom](#ruim-x-bom)
- [Uso nesta skill](#uso-nesta-skill)

## Palavras vagas

| Trecho | Problema | Pergunta que o substitui |
| --- | --- | --- |
| "rápido", "performático" | sem número, nenhum teste falha | "Em quanto tempo, com quantos usuários, medido onde?" (ex.: p95 < 800 ms com 200 simultâneos) |
| "fácil", "intuitivo", "amigável" | opinião | "Que tarefa, em quantos passos, para qual usuário?" |
| "etc.", "entre outros" | lista aberta: o dev faz 3 itens, o PO esperava 5 | "Qual é a lista completa?" |
| "normalmente", "geralmente" | esconde as exceções | "E quando não é o normal, o que acontece?" |
| "suportar", "permitir", "lidar com" | não diz o comportamento | "O que o sistema faz, exatamente, com X?" |
| "seguro", "robusto" | genérico | "Contra o quê? Quem pode e quem não pode?" |
| "todos", "sempre", "nunca" | absoluto raramente é verdade | "Inclusive inativos, bloqueados, administradores?" |
| "validar", "tratar erros" | quais regras, que mensagem? | "Que regra, que mensagem, o que fica gravado?" |
| "corretamente", "adequadamente" | não há oráculo | "Qual é o resultado esperado, com valores?" |
| "em tempo real" | segundos? milissegundos? | "Qual atraso máximo é aceitável?" |
| "igual ao sistema antigo" | comportamento não documentado | "Quem conhece o antigo? Inclusive os defeitos?" |
| "prazo", "data" sem fuso | qual relógio? | "Horário de Brasília ou do usuário? Dias úteis ou corridos?" |

Os números entre parênteses são exemplos de formato de resposta, não valores recomendados.

## Regras implícitas

O que a história não diz, mas alguém vai decidir. Melhor que seja o dono do produto no refinamento do que o desenvolvedor no fim do dia.

| Categoria | Pergunta |
| --- | --- |
| Permissão | Quem pode, quem não pode, outro cliente ou outro tenant/plano? |
| Estados | O que muda para registros em cada status existente? |
| Dados existentes | Registros antigos sem o campo novo; migração? |
| Limites | Tamanhos, quantidades, valores máximos, paginação? |
| Concorrência e repetição | Dois usuários ao mesmo tempo; duplo envio? |
| Falhas | Dependência fora do ar, timeout, retry que duplica? |
| Desfazer | Dá para cancelar, editar, excluir? Com que efeito? |
| Efeitos em volta | Relatórios, integrações, e-mails, exportações? |
| Canais | A regra vale igual na web, no app e na API? |

## Requisitos não funcionais esquecidos

| Tipo | Pergunta | Exemplo de critério mensurável (formato, não recomendação) |
| --- | --- | --- |
| Performance | quanto tempo, com que carga? | busca em p95 < 1 s com 100 usuários simultâneos |
| Segurança | quem acessa, o que proteger, como abusariam? | só o titular vê o pedido; 5 tentativas por minuto por IP |
| Acessibilidade | WCAG 2.2 AA? teclado e leitor de tela? | todo campo com rótulo; fluxo completo só com teclado |
| Logs e observabilidade | como saberemos que quebrou em produção? | erro de pagamento gera log com ID de correlação, sem dados do cartão |
| i18n e l10n | idiomas, moedas, formatos, fusos? | pt-BR exibe 05/10/2026 e R$ 1.234,56 |
| LGPD | que dado pessoal, para quê, por quanto tempo, quem vê? | CPF mascarado no atendimento; exclusão a pedido do titular (conferir com jurídico) |
| Compatibilidade | navegadores, versões do app, dispositivos? | duas últimas versões de Chrome, Safari, Firefox e Edge |
| Recuperação | o que acontece se cair no meio? | após retry, o pedido não é duplicado |

Quando o usuário não der o número, escreva a pergunta e deixe o critério como Suposição ou aberto. O valor da coluna da direita ilustra como um critério mensurável se parece.

## Ruim x bom

| Ruim | Por quê | Bom |
| --- | --- | --- |
| "O cupom deve ser aplicado corretamente" | sem oráculo | "Cupom DEZ10 em carrinho de R$ 200,00: desconto de R$ 20,00 e subtotal de R$ 180,00" |
| "A busca deve ser rápida" | sem número | "Busca por nome responde em até 1 s (p95) com 50 mil produtos" |
| "Validar o CPF" | quais regras? | "CPF com dígito verificador errado ou com 11 dígitos iguais é recusado com 'CPF inválido'; nada é gravado" |
| "Usuário pode exportar relatórios" | quais, em que formato, até quanto? | "Exporta as vendas do período filtrado em CSV (UTF-8, separador ;) até 100 mil linhas; acima disso, envia por e-mail" |
| "Clicar em Salvar e ver a mensagem" | descreve clique, não regra | "Endereço salvo passa a ser o padrão da próxima compra" |
| "Tratar erros do pagamento" | quais erros? | "Sem resposta do gateway em 10 s, o pedido fica 'aguardando pagamento' e o cliente vê 'Estamos confirmando seu pagamento'" |

Um bom critério tem um comportamento, dado concreto, resultado observável, pelo menos um caminho negativo e nenhuma dependência do desenho da tela. Os números dos exemplos são ilustrativos.

## Uso nesta skill

- Passo 1 percorre a primeira tabela; passo 2, a segunda; passo 3, a terceira.
- A `spec-interview` reutiliza estas tabelas na Rodada 3.
- Pergunte só o que se aplica à história: lista de 40 perguntas é ruído (limite prático: as 5 de maior risco primeiro).
