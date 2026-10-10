# Critérios de aceite e histórias

Como revisar uma história antes do código, escrever critérios de aceite testáveis, dividir histórias, conduzir Example Mapping e three amigos e escrever Gherkin ou EARS que funcionem como especificação. Leia ao usar `acceptance-criteria` ou `refine-backlog`.

Base: adaptado de `brains/qa/references/requisitos-e-bdd.md` do brain-of-agent (MIT, Francisco Edson; conteúdo próprio, V-42), combinado com V-16, V-17, V-18, V-19, V-20, V-36, V-37 e V-44 (destilados). Step definitions, ferramentas de BDD e automação ficam em `/qa-testing:playbook`; aqui só a escrita e a revisão de requisitos.

## Sumário

- [1. Palavras vagas](#1-palavras-vagas)
- [2. INVEST](#2-invest)
- [3. Regras implícitas](#3-regras-implícitas)
- [4. Requisitos não funcionais esquecidos](#4-requisitos-não-funcionais-esquecidos)
- [5. Perguntas de refinamento](#5-perguntas-de-refinamento)
- [6. Formato do critério](#6-formato-do-critério)
- [7. Ruim e bom](#7-ruim-e-bom)
- [8. Ordem de escrita e checklist de 6 itens](#8-ordem-de-escrita-e-checklist-de-6-itens)
- [9. Cartão, conversa, confirmação](#9-cartão-conversa-confirmação)
- [10. Example Mapping](#10-example-mapping)
- [11. Three amigos em 25 minutos](#11-three-amigos-em-25-minutos)
- [12. Gherkin](#12-gherkin)
- [13. EARS](#13-ears)
- [14. Divisão de histórias e tamanho](#14-divisão-de-histórias-e-tamanho)
- [15. Sprint planning em três blocos](#15-sprint-planning-em-três-blocos)
- [16. Quando não usar Gherkin](#16-quando-não-usar-gherkin)
- [17. Exemplo completo: recuperação de senha](#17-exemplo-completo-recuperação-de-senha)

## 1. Palavras vagas

Defeito de requisito achado no refinamento custa uma conversa; achado em produção custa retrabalho, suporte e às vezes dinheiro. Quem revisa procura ambiguidade, lacuna e contradição e sai com perguntas, não com a história reescrita sozinho. Template: [revisao-de-historia.md](../assets/templates/revisao-de-historia.md).

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

## 2. INVEST

Uma história é testável quando cada critério tem resultado observável e dá para dizer o que faria o teste falhar. INVEST (Bill Wake, 2003; Mike Cohn, 2004; glossário da Agile Alliance, V-18) lista seis propriedades. A coluna "pergunta-teste" é nossa (Inferido: a página oficial não traz as perguntas).

| Letra | Sinal de problema | Pergunta-teste (Inferido) |
| --- | --- | --- |
| Independente | só dá para testar depois de outra história ficar pronta | Pode ser entregue sem esperar outra? |
| Negociável | chega com a tela fechada, sem espaço para discutir a regra | Descreve objetivo ou já é contrato de implementação? |
| Valiosa | ninguém diz quem ganha o quê; sem isso não há como priorizar riscos | Quem percebe valor se só ela for entregue? |
| Estimável | o time não consegue estimar: falta informação, não esforço | O que falta saber para estimar? |
| Pequena | não cabe na iteração; muitas regras no Example Mapping | Cabe numa iteração (e, com agente, numa sessão focada)? |
| Testável | nenhum critério tem resultado que possa dar errado | Dá para dizer como confirmar que está pronta? |

Se falhar uma letra, reescreva ou divida.

## 3. Regras implícitas

O que a história não diz, mas alguém vai decidir: melhor que seja o PO, no refinamento, e não o dev às 18h.

- **Permissão:** quem pode, quem não pode, outro cliente ou outro tenant.
- **Estados:** o que muda para registros em cada status existente.
- **Dados existentes:** registros antigos sem o campo novo, migração.
- **Limites:** tamanhos, quantidades, valores máximos, paginação.
- **Concorrência e repetição:** dois usuários ao mesmo tempo, duplo envio.
- **Falhas:** dependência fora do ar, timeout, retry que duplica.
- **Desfazer:** dá para cancelar, editar, excluir? Com que efeito?
- **Efeitos em volta:** relatórios, integrações, e-mails, exportações.
- **Canais:** a regra vale igual na web, no app e na API?

## 4. Requisitos não funcionais esquecidos

| Tipo | Pergunta | Critério mensurável de exemplo |
| --- | --- | --- |
| Performance | quanto tempo, com que carga? | busca em p95 < 1 s com 100 usuários simultâneos |
| Segurança | quem acessa, o que proteger, como abusariam? | só o titular vê o pedido; 5 tentativas por minuto por IP |
| Acessibilidade | WCAG 2.2 AA? teclado e leitor de tela? | todo campo com rótulo; fluxo completo só com teclado |
| Logs e observabilidade | como saberemos que quebrou em produção? | erro de pagamento gera log com ID de correlação, sem dados do cartão |
| i18n e l10n | idiomas, moedas, formatos, fusos? | pt-BR exibe 05/10/2026 e R$ 1.234,56 |
| LGPD | que dado pessoal, para quê, por quanto tempo, quem vê? | CPF mascarado no atendimento; exclusão a pedido do titular |
| Compatibilidade | navegadores, versões do app, dispositivos? | duas últimas versões de Chrome, Safari, Firefox e Edge |
| Recuperação | o que acontece se cair no meio? | após retry, o pedido não é duplicado |

Os números são exemplos de formato; use os do produto, nunca estes por padrão.

## 5. Perguntas de refinamento

- Que problema do usuário isto resolve, e como saberemos que resolveu?
- Qual o pior resultado se isto quebrar em produção? (define a prioridade)
- Quem pode fazer isto, e quem não pode?
- Quais são os limites: mínimo, máximo, tamanho, quantidade, prazo?
- O que acontece com os dados que já existem?
- E se o usuário fizer duas vezes, ou parar no meio e voltar?
- E se a dependência X estiver lenta ou fora do ar?
- Que mensagem aparece em cada erro?
- O que muda em relatórios, integrações, e-mails, exportações?
- Do que precisamos para testar: dados, ambiente, simulador de terceiro, flag?
- O que está explicitamente fora do escopo?
- Como saberemos em produção que funciona (métrica, log, alerta)?

## 6. Formato do critério

Escolha **um padrão principal por spec** (V-20).

| Formato | Use quando | Cuidado |
| --- | --- | --- |
| Regra + exemplo | padrão para quase tudo | todo exemplo com dados concretos |
| Given/When/Then (Dado/Quando/Então) | comportamento com contexto e o negócio lê os cenários | declarativo, um comportamento por cenário |
| EARS | requisito de sistema, regulado ou embarcado | mais de 3 pré-condições fica pesado |
| Checklist | verificações simples e independentes (campos, textos, layout) | cada item verificável sozinho |

## 7. Ruim e bom

| Ruim | Por quê | Bom |
| --- | --- | --- |
| "O cupom deve ser aplicado corretamente" | sem oráculo | "Cupom DEZ10 em carrinho de R$ 200,00 → desconto de R$ 20,00 e subtotal de R$ 180,00" |
| "A busca deve ser rápida" | sem número | "Busca por nome responde em até 1 s (p95) com 50 mil produtos" |
| "Validar o CPF" | quais regras? | "CPF com dígito verificador errado ou com 11 dígitos iguais é recusado com 'CPF inválido'; nada é gravado" |
| "Usuário pode exportar relatórios" | quais, em que formato, até quanto? | "Exporta as vendas do período filtrado em CSV (UTF-8, separador ;) até 100 mil linhas; acima disso, envia por e-mail" |
| "Clicar em Salvar e ver a mensagem" | descreve clique, não regra | "Endereço salvo passa a ser o padrão da próxima compra" |
| "Tratar erros do pagamento" | quais erros? | "Sem resposta do gateway em 10 s, o pedido fica 'aguardando pagamento' e o cliente vê 'Estamos confirmando seu pagamento'" |

Um bom critério tem um comportamento, dado concreto, resultado observável, pelo menos um caminho negativo e nenhuma dependência do desenho da tela.

## 8. Ordem de escrita e checklist de 6 itens

Cubra nesta ordem (V-36, destilado): **caminho feliz**, depois **falhas e bordas** com comportamento visível, depois **não funcionais** (desempenho, acessibilidade, segurança, confiabilidade, auditabilidade). Critério subjetivo vira resultado mensurável.

Checklist de revisão do conjunto:

1. Escopo específico (a história não cobre três coisas).
2. Caminho feliz primeiro.
3. Bordas explícitas (limites, vazio, repetição).
4. Erros com recuperação visível (o usuário sabe o que fazer).
5. Testável: cada critério responde "o que faria o teste falhar?".
6. Sem detalhe de implementação (nenhum nome de tabela, endpoint ou componente).

As cinco perguntas por cenário (V-17, Cucumber): descreve o quê e não o como? Sobrevive a uma mudança de implementação? Sem verbos de interação ("clicar", "digitar")? Um comportamento por cenário? O `Then` é observável?

## 9. Cartão, conversa, confirmação

Três Cs (atribuídos a Ron Jeffries; V-19, Mountain Goat, atualizado em 2026-07-12): **cartão** (a história curta), **conversa** (os detalhes surgem do diálogo), **confirmação** (os critérios, na forma de exemplos, regras, testes ou notas). Modelo: "Como [tipo de usuário], quero [fazer algo], para que [benefício]" (a fonte não fixa o verbo "quero"). O entendimento compartilhado vale mais que a forma. Uma história está "pronta para sprint" quando o time entende o que precisa ser verdade para contá-la como concluída (`story-ready` em [checklist-completo.md](checklist-completo.md); a definição de "ready" é construção nossa, o Scrum Guide 2020 não a prescreve, V-44). Template: [historia.md](../assets/templates/historia.md).

## 10. Example Mapping

Técnica de Matt Wynne (Cucumber) para descobrir regras com exemplos antes do código. Cartões coloridos, físicos ou num quadro virtual:

| Cor | Significa |
| --- | --- |
| Amarelo | a história |
| Azul | uma regra (vira critério de aceite) |
| Verde | um exemplo concreto da regra (vira cenário ou caso de teste) |
| Vermelho | uma pergunta que ninguém na sala sabe responder |

1. Ponha a história (amarelo) no topo.
2. Liste as regras conhecidas (azul) lado a lado, abaixo dela.
3. Para cada regra, peça exemplos (verde): "um caso em que acontece" e "um em que não acontece". Frases curtas com dados ("Ana usa o link 29 min depois → troca a senha"), ainda não Gherkin. Exemplos costumam revelar regras novas, que ganham um cartão azul.
4. Dúvida que trava a conversa vira cartão vermelho com dono, e a conversa segue. Não gaste 10 minutos discutindo o que só o jurídico responde.
5. Feche em 25 minutos com voto de polegar: está pronta para desenvolver?

Como ler o mapa:

- **Muitos vermelhos:** não está pronta; responda antes de começar.
- **Muitos azuis:** história grande; divida por regra.
- **Regra com muitos verdes:** regra complexa; considere tabela de decisão ou divisão.
- **Regra sem verde:** ninguém a entendeu de verdade.
- **Não fechou em 25 minutos:** grande ou incerta demais.

Quando o agente conduz sozinho, ele monta o mapa em texto e marca em vermelho as perguntas que só o humano responde; não simula respostas do negócio.

## 11. Three amigos em 25 minutos

Negócio (PO ou analista), desenvolvimento e teste: são perspectivas, não cargos. De 3 a 5 pessoas. Preparo: o PO traz objetivo e regras conhecidas; quem testa lê antes e chega com perguntas e riscos.

| Minutos | O quê | Quem puxa |
| --- | --- | --- |
| 0 a 3 | problema e valor para o usuário (não a solução) | PO |
| 3 a 18 | Example Mapping: regras, exemplos, perguntas | quem testa facilita |
| 18 a 22 | riscos e não funcionais: segurança, dados, performance, acessibilidade, o que quebra em volta | teste e dev |
| 22 a 25 | decisão: pronta, dividir ou voltar com respostas; dono de cada pergunta | todos |

Saída: regras e exemplos registrados na história, perguntas com dono, divisão sugerida e notas de teste. Erros comuns: virar reunião de solução técnica; quem testa só ouvindo; conversa sem exemplos concretos; terminar sem decisão; convidar dez pessoas.

## 12. Gherkin

Fonte de semântica: referência do Cucumber (V-16, destilado). Verificado: um `Feature` por arquivo; `Rule` desde o Gherkin 6; um `Background` por Feature ou Rule; `Scenario` equivale a `Example`; `Scenario Outline` exige `Examples`; `Given` é estado conhecido, `When` é ação ou evento, `Then` é resultado em saída observável (não verifique o banco direto); `And`, `But` e `*` substituem palavras-chave. A página não restringe o `Background` a `Given`; sugere cautela quando passa de 4 linhas.

### Estrutura

```gherkin
Feature: nome curto da capacidade
  Texto livre: valor e contexto.

  Background: passos Given comuns a todos os cenários (opcional)

  Rule: uma regra de negócio
    Scenario: um exemplo da regra
      Given o estado do mundo antes
      When um único evento ou ação
      Then o resultado observável
      And / But continuam o passo anterior
```

`Given` descreve estado, não navegação. `When` é um evento. `Then` é algo que o usuário ou um sistema externo observa. Tags (`@smoke`, `@wip`) selecionam execuções.

### Declarativo e imperativo

Imperativo (ruim): roteiro de cliques que quebra a cada redesenho e esconde a regra.

```gherkin
Cenário: Aplicar cupom
  Dado que eu acesso "https://loja.exemplo.com/login"
  E preencho o campo "#email" com "ana@exemplo.com"
  E clico no botão "Entrar"
  Quando digito "DEZ10" no campo "cupom"
  E clico em "Aplicar"
  Então vejo "R$ 180,00" no elemento ".total"
```

Declarativo (bom): diz o quê.

```gherkin
Cenário: Cupom percentual reduz o subtotal
  Dado que existe o cupom "DEZ10" de 10% de desconto
  E que Ana tem R$ 200,00 em produtos no carrinho
  Quando Ana aplica o cupom "DEZ10"
  Então o subtotal com desconto é R$ 180,00
```

### Um comportamento por cenário

- Um único `Quando`. Se precisa de dois, são dois cenários, ou o primeiro é contexto e vira `Dado`.
- O título diz a regra ("Link expirado não troca a senha"), não "CT-042".
- Cenários independentes: nenhum depende de outro nem da ordem de execução.

### Contexto (Background) com parcimônia

Só passos `Dado` que **todos** os cenários do bloco precisam e que o leitor precisa ver para entender; até três ou quatro linhas. Contexto longo esconde dados relevantes. Preparação técnica (limpar banco, autenticar o cliente HTTP) não é contexto de negócio. Se só parte dos cenários usa o passo, ele pertence a esses cenários.

### Esquema do cenário com exemplos nos limites

Cada linha da tabela representa uma partição ou um limite diferente; trinta linhas da mesma classe só deixam a suíte lenta. Quando o resultado muda de natureza (sucesso e recusa), faça dois esquemas: uma coluna "resultado: sucesso/erro" esconde dois comportamentos em um.

```gherkin
Esquema do Cenário: Frete grátis a partir de R$ 199,00
  Dado um carrinho com subtotal de <subtotal>
  Quando o frete é calculado para o CEP "01310-100"
  Então o frete cobrado é <frete>

  Exemplos: em torno do limite
    | subtotal  | frete    |
    | R$ 198,99 | R$ 19,90 |
    | R$ 199,00 | R$ 0,00  |
    | R$ 199,01 | R$ 0,00  |
```

### Regra (Rule)

`Rule` agrupa cenários sob uma regra de negócio e pode ter seu próprio `Background`. Espelha o Example Mapping: cartão azul vira `Regra`, verdes viram `Cenário`. Implementações antigas de algumas ferramentas não reconhecem a palavra-chave; confirme o suporte na versão que o time usa.

### Gherkin em português

A primeira linha do arquivo é `# language: pt`.

| Inglês | Português (alternativas aceitas) |
| --- | --- |
| Feature | Funcionalidade (Característica) |
| Rule | Regra |
| Background | Contexto (Cenário de Fundo, Fundo) |
| Scenario / Example | Cenário (Exemplo) |
| Scenario Outline | Esquema do Cenário (Delineação do Cenário) |
| Examples | Exemplos (Cenários) |
| Given | Dado, Dada, Dados, Dadas |
| When | Quando |
| Then | Então |
| And / But | E / Mas |

Armadilha: `Exemplo:` é sinônimo de **Cenário**, e `Cenários:` é sinônimo de **Exemplos**; é fácil confundir.

### Anti-padrões

| Anti-padrão | Exemplo | Correção |
| --- | --- | --- |
| Clique a clique | "E clico em 'Entrar'" | intenção: "Dado que Ana está autenticada" |
| `Então` que descreve implementação | "Então é inserida linha em tb_pedido com status 3" | resultado de negócio: "Então o pedido aparece como 'Pago' para Ana" |
| Dados mágicos | "Dado o usuário 4711" | dado com significado: "Dado um cliente VIP com 2 pedidos atrasados" |
| Vários `Quando` | Quando... Então... Quando... Então... | um cenário por comportamento |
| `Então` sem verificação | "Então o sistema processa a solicitação" | algo observável e que possa falhar |
| Esquema com coluna sucesso/erro | `\| resultado \|` com "ok" e "erro" | dois esquemas |
| Passo com conjunções | "Dado que Ana está logada e tem itens e um cupom" | passos separados |
| Contexto longo | dez passos antes de cada cenário | passos no próprio cenário; preparação técnica fora do texto |
| Feature como roteiro de teste | "Cenário: CT-042 caminho feliz" | título que diz a regra |

Para step definitions, ferramentas e automação, use `/qa-testing:playbook`.

## 13. EARS

Sintaxe de requisitos de Mavin et al. (Rolls-Royce, 2009; resumo da Wikipedia, V-20, classe B; artigo original não lido). Forma geral: `ENQUANTO <pré-condições>, QUANDO <gatilho>, o <sistema> DEVE <resposta>`, com zero ou mais pré-condições, zero ou um gatilho, um nome de sistema e uma ou mais respostas.

| Padrão | Modelo em português | Exemplo |
| --- | --- | --- |
| Ubíquo | O `<sistema>` deve `<resposta>`. | O app deve registrar a data e a hora de cada envio. |
| Orientado a evento | QUANDO `<gatilho>`, o `<sistema>` deve `<resposta>`. | QUANDO o pagamento é recusado, o app deve manter o pedido como "aguardando pagamento". |
| Orientado a estado | ENQUANTO `<estado>`, o `<sistema>` deve `<resposta>`. | ENQUANTO o usuário está sem conexão, o app deve guardar os envios em fila local. |
| Funcionalidade opcional | ONDE `<opção presente>`, o `<sistema>` deve `<resposta>`. | ONDE o plano inclui relatórios, o app deve exibir a aba "Relatórios". |
| Comportamento indesejado | SE `<condição indesejada>`, ENTÃO o `<sistema>` deve `<resposta>`. | SE o token expirou, ENTÃO o app deve pedir novo login sem perder o rascunho. |

Limites: fonte secundária; requisitos não condicionais encaixam mal; use EARS como alternativa ao Given/When/Then, não junto.

## 14. Divisão de histórias e tamanho

Divida em **fatias verticais** que entregam valor visível (padrões abaixo são conhecimento estável do domínio, sem fonte A no atlas, Inferido):

| Padrão de divisão | Exemplo |
| --- | --- |
| Por regra de negócio (cartão azul) | "recuperar senha" → link vale 30 min; só o último link vale; limite de pedidos |
| Por fluxo ou etapa de ponta a ponta | caminho feliz de compra → compra com cupom → compra com frete grátis |
| Por variação de dados | exportar CSV → exportar XLSX |
| Por perfil de usuário | gerente → analista |
| Por prioridade P1/P2/P3 independentes | MVP útil sozinho, depois as demais |

Não divida por camada técnica (banco, API, tela): nenhuma das fatias entrega valor sozinha. Tamanho-alvo: cabe numa iteração e, para execução por agente, numa sessão focada (V-37, fonte ralph, MIT). Todo critério observável; critério comum a todas as histórias (build e lint passam) pode ser declarado uma vez.

## 15. Sprint planning em três blocos

Scrum Guide 2020 (V-44; o texto não tem licença de reuso verificável; destilado). A Sprint Planning responde três perguntas: **por que** a Sprint é valiosa (define a meta), **o que** pode ser feito (seleção do backlog), **como** o trabalho escolhido será feito (decomposição em itens de até um dia). O refinamento é contínuo (descrição, ordem, tamanho); existe uma Definition of Done. O guia descreve Scrum e diz que o plano é do time inteiro: este plugin apoia, não prescreve, e não impõe Scrum a quem não usa. Template: [sprint-planning.md](../assets/templates/sprint-planning.md).

## 16. Quando não usar Gherkin

BDD é conversa (descoberta), formulação e automação; Gherkin é só a formulação. Vale quando pessoas de negócio leem e discutem os cenários. Não use quando:

- Ninguém de negócio lê os `.feature`: vira camada de tradução a mais para manter; teste no código com nomes descritivos comunica o mesmo.
- O alvo é cálculo com muitas variações: teste parametrizado é mais direto.
- O teste é técnico: performance, segurança, contrato de API, infraestrutura, layout visual.
- Quem testa escreve sozinho, depois do código: é documentação de teste com sintaxe extra, não BDD.
- O trabalho é exploratório: charter e notas servem melhor.

Example Mapping e three amigos valem mesmo sem Gherkin.

## 17. Exemplo completo: recuperação de senha

### História original

> Como usuário, quero recuperar minha senha para acessar o sistema caso eu a esqueça. Critérios: o usuário recebe um e-mail com um link; o link deve expirar; o processo deve ser seguro e fácil; tratar e-mails inválidos etc.

### Revisão com perguntas

| Trecho | Problema | Pergunta | Resposta do PO |
| --- | --- | --- | --- |
| "recebe um e-mail" | e o e-mail sem conta? | A tela avisa que o e-mail não existe? | Não: mesma mensagem nos dois casos (evita enumeração de contas) |
| "deve expirar" | sem prazo | Em quanto tempo? Pode usar duas vezes? | 30 minutos, inclusive; uso único |
| (implícito) | pedidos repetidos | Pedir de novo invalida o link anterior? | Sim, só o mais recente vale |
| "seguro" | vago | Limite de pedidos? E as sessões abertas? Avisar o titular? | 5 pedidos por e-mail por hora; encerra todas as sessões; e-mail de aviso após a troca |
| "fácil" | opinião | Que uso precisa funcionar? | celular de 360 px de largura e só teclado (WCAG 2.2 AA) |
| "e-mails inválidos etc." | lista aberta | Quais casos? | formato inválido: erro no campo; maiúsculas e espaços nas pontas são normalizados |
| (implícito) | nova senha | Mesmas regras do cadastro? Pode repetir a atual? | mesmas regras; não pode ser igual à atual |
| (implícito) | conta só com login social | Envia o quê? | **pergunta aberta**, dono: PO |
| (não funcional) | token em log | O link aparece em logs ou analytics? | nunca; e-mail em pt-BR |

As respostas do PO são parte do exemplo didático; em um caso real, o agente nunca preenche essa coluna.

### Critérios reescritos (regra + exemplo)

1. A resposta não revela se o e-mail tem conta. Ex.: "ana@" (com conta) e "bia@" (sem conta) veem a mesma mensagem; só Ana recebe e-mail.
2. O link vale por até 30 minutos, inclusive, e uma única vez. Ex.: enviado às 10:00:00, aceito às 10:30:00, recusado às 10:30:01.
3. Só o link mais recente vale. Ex.: links das 10:00 e das 10:05; o das 10:00 é recusado.
4. Trocar a senha encerra todas as sessões e envia aviso ao titular.
5. No máximo 5 pedidos por e-mail por hora. Ex.: o 5º envia; o 6º não.

Ficam fora do Gherkin, como testes técnicos ou checklist: token fora de logs, acessibilidade do fluxo, regras da nova senha (já cobertas no cadastro). O arquivo completo dos cenários está em [exemplo.feature](../assets/templates/exemplo.feature).

### O que a revisão rendeu

Cinco regras explícitas onde havia quatro frases vagas, uma pergunta aberta com dono e uma nova dúvida que só apareceu ao escrever o último cenário: "na última hora" é janela deslizante ou hora cheia? Volta para o PO antes do desenvolvimento.
