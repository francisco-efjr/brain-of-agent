# Roteiro de teste de usabilidade moderado

Base: "Usability Testing 101", Kate Moran, NN/g, publicado em 2019-12-01 e revisado em 2026-07-15 (https://www.nngroup.com/articles/usability-testing-101/; V-17). Conteúdo © NN/g: abaixo só há destilação. A fonte não cobre recrutamento nem análise quantitativa. O modelo de registro e os exemplos de tarefa são do plugin (Inferido).

## Sumário

- [O que o teste é e o que não é](#o-que-o-teste-é-e-o-que-não-é)
- [Roteiro da sessão](#roteiro-da-sessão)
- [Como escrever tarefas](#como-escrever-tarefas)
- [Exemplo de roteiro (onboarding de conta digital)](#exemplo-de-roteiro-onboarding-de-conta-digital)
- [Registro de problemas](#registro-de-problemas)
- [Sinais de que a sessão foi contaminada](#sinais-de-que-a-sessão-foi-contaminada)

## O que o teste é e o que não é

- É observação de pessoas do perfil tentando fazer tarefas realistas com a interface, para achar problemas de usabilidade.
- Para um estudo qualitativo com um único grupo de usuários, cinco participantes costumam revelar a maioria dos problemas comuns. Grupos diferentes (por exemplo clientes novos e antigos) precisam de participantes próprios.
- Não é pesquisa de opinião, não mede preferência, não dá significância estatística. Não use percentuais de n=5 como prevalência.
- Não confundir com avaliação heurística, que inspeciona o artefato com especialistas ou com um modelo.

## Roteiro da sessão

Duração típica de 45 a 60 minutos (ajuste ao número de tarefas).

1. **Abertura (3 a 5 min).** Apresentação; "estamos testando o produto, não você"; não há resposta errada; peça para pensar em voz alta; informe a gravação e peça confirmação do consentimento; a pessoa pode parar quando quiser.
2. **Perguntas iniciais (5 min).** Experiência anterior com o tipo de produto, sem entrar no que será testado.
3. **Tarefas (25 a 35 min).** Uma por vez, em ordem planejada (as mais críticas primeiro; ordem rotativa se as tarefas forem independentes). Entregar a tarefa por escrito; **o participante lê em voz alta** (a redação da tarefa influencia o comportamento, o que a literatura chama de priming). Observe sem ajudar; encerre quando a pessoa concluir, desistir ou o tempo planejado acabar.
4. **Fechamento (5 a 10 min).** "O que foi mais difícil?", "O que você mudaria?", "O que ficou confuso?", e a pergunta aberta "Algo mais que você queira dizer?". Agradecer.
5. **Pós-sessão.** Anotações limpas, marcar os momentos para revisar na gravação.

Durante a tarefa, as intervenções permitidas são neutras: "Continue pensando em voz alta", "O que você está procurando?", "O que você esperava que acontecesse?". Evite: "Clique ali", "Tente o menu", "Está certo?".

## Como escrever tarefas

| Ruim | Problema | Boa |
| --- | --- | --- |
| "Clique em Gerenciar plano e cancele" | entrega o caminho | "Você decidiu parar de pagar este serviço. Faça isso." |
| "Use a busca para achar um tênis" | entrega a ferramenta | "Você quer comprar um tênis de corrida até R$ 300. Encontre um que lhe interesse." (valor fictício) |
| "Avalie a página inicial" | sem tarefa | "Você acabou de ouvir falar desta empresa. O que você acha que ela oferece? Mostre onde descobriria mais." |

Cada tarefa tem: cenário (motivo realista), objetivo observável, critério de sucesso ("chega à tela de confirmação sem ajuda"), limite de tempo para parar, e os dados de apoio que a pessoa precisa (conta de teste, cartão fictício, documentos de exemplo).

## Exemplo de roteiro (onboarding de conta digital)

Pedido: "1 semana para testar a usabilidade do onboarding do app de conta digital; as pessoas travam na etapa de selfie e documento." (Cenário fictício.)

| # | Tarefa | Sucesso | Hipótese a observar |
| --- | --- | --- | --- |
| T1 | "Você acabou de baixar o app e quer abrir uma conta. Faça isso até onde conseguir." | chega ao fim do cadastro sem ajuda | onde hesita antes da selfie |
| T2 | (etapa de documento) "O app pede um documento. Envie o seu (use o documento de teste)." | envia a foto aceita na 1ª ou 2ª tentativa | qualidade de foto, instrução de enquadramento |
| T3 | "A foto foi recusada. Descubra o que fazer." | refaz a foto com sucesso | clareza da mensagem de erro |

Recrutamento: cinco pessoas do perfil "ainda sem conta, usam banco no celular", com alguma sobra para faltas. Não inventar resultados. O estudo **não** responde: taxa real de conclusão, motivo de abandono em escala, preferência de design.

## Registro de problemas

Tabela por participante e tarefa; depois consolidada.

| Tarefa | Participante | Resultado (concluiu / com ajuda / não concluiu) | Onde hesitou | Citação literal | Problema | Severidade 0 a 4 (complemento Inferido) |
| --- | --- | --- | --- | --- | --- | --- |
| T2 | P3 | concluiu na 2ª tentativa | enquadramento do documento | "não sei se coube tudo" | falta guia de enquadramento | 2 |

Consolidação: por problema, registre quantos dos participantes o apresentaram (frequência observada, contagem simples), a severidade e a correção sugerida. A escala 0 a 4 vem do artigo de Nielsen de 1994 e aqui é só complemento.

## Sinais de que a sessão foi contaminada

- O moderador explicou a interface antes da tarefa ou respondeu perguntas sobre como usar.
- A tarefa continha o rótulo exato do botão.
- O participante é amigo, colega ou já conhecia o protótipo.
- Alguém na sala reagiu em voz alta.
- O participante fez a tarefa sem pensar em voz alta e o moderador não lembrou.
Registre a contaminação nas anotações e trate a sessão com cautela; não esconda.
