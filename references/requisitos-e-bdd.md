# Requisitos, critérios de aceite e BDD

Como revisar uma história antes do código, escrever critérios de aceite
testáveis, conduzir Example Mapping e three amigos, e escrever Gherkin que
funciona como especificação. Leia no refinamento, ao escrever critérios ou
cenários BDD, ou ao revisar arquivos `.feature`.

## Sumário

- [Revisão de requisito e de história](#revisão-de-requisito-e-de-história)
- [Critérios de aceite](#critérios-de-aceite)
- [Example Mapping passo a passo](#example-mapping-passo-a-passo)
- [Three amigos em 25 minutos](#three-amigos-em-25-minutos)
- [Gherkin](#gherkin)
- [Step definitions e ferramentas](#step-definitions-e-ferramentas)
- [Quando não usar Gherkin](#quando-não-usar-gherkin)
- [Exemplo completo: recuperação de senha](#exemplo-completo-recuperação-de-senha)

## Revisão de requisito e de história

Defeito de requisito achado no refinamento custa uma conversa; achado em
produção custa retrabalho, suporte e às vezes dinheiro. O QA revisa procurando
ambiguidade, lacuna e contradição, e sai com perguntas, não com a história
reescrita sozinho. Template: `assets/templates/revisao-de-historia.md`.

### Palavras vagas

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

### Testabilidade e INVEST

Uma história é testável quando cada critério tem resultado observável e dá
para dizer o que faria o teste **falhar**. INVEST (Bill Wake) ajuda a ver o
que falta:

| Letra | Sinal de problema para o QA |
| --- | --- |
| Independente | só dá para testar depois de outra história ficar pronta |
| Negociável | chega com a tela fechada, sem espaço para discutir a regra |
| Valiosa | ninguém diz quem ganha o quê; sem isso não há como priorizar riscos |
| Estimável | o time não consegue estimar: falta informação, não esforço |
| Pequena | não cabe na iteração; muitas regras no Example Mapping |
| Testável | nenhum critério tem resultado que possa dar errado |

### Regras implícitas

O que a história não diz, mas alguém vai decidir — melhor que seja o PO, no
refinamento, e não o dev às 18h:

- **Permissão:** quem pode, quem não pode, outro cliente ou outro tenant.
- **Estados:** o que muda para registros em cada status existente.
- **Dados existentes:** registros antigos sem o campo novo, migração.
- **Limites:** tamanhos, quantidades, valores máximos, paginação.
- **Concorrência e repetição:** dois usuários ao mesmo tempo, duplo envio.
- **Falhas:** dependência fora do ar, timeout, retry que duplica.
- **Desfazer:** dá para cancelar, editar, excluir? Com que efeito?
- **Efeitos em volta:** relatórios, integrações, e-mails, exportações.
- **Canais:** a regra vale igual na web, no app e na API?

### Requisitos não funcionais esquecidos

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

### Perguntas que um QA faz no refinamento

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

## Critérios de aceite

| Formato | Use quando | Cuidado |
| --- | --- | --- |
| Regra + exemplo | padrão para quase tudo | todo exemplo com dados concretos |
| Gherkin (Dado/Quando/Então) | comportamento com contexto e o time automatiza BDD | declarativo, um comportamento por cenário |
| Checklist | verificações simples e independentes (campos, textos, layout) | cada item verificável sozinho |

| Ruim | Por quê | Bom |
| --- | --- | --- |
| "O cupom deve ser aplicado corretamente" | sem oráculo | "Cupom DEZ10 em carrinho de R$ 200,00 → desconto de R$ 20,00 e subtotal de R$ 180,00" |
| "A busca deve ser rápida" | sem número | "Busca por nome responde em até 1 s (p95) com 50 mil produtos" |
| "Validar o CPF" | quais regras? | "CPF com dígito verificador errado ou com 11 dígitos iguais é recusado com 'CPF inválido'; nada é gravado" |
| "Usuário pode exportar relatórios" | quais, em que formato, até quanto? | "Exporta as vendas do período filtrado em CSV (UTF-8, separador ;) até 100 mil linhas; acima disso, envia por e-mail" |
| "Clicar em Salvar e ver a mensagem" | descreve clique, não regra | "Endereço salvo passa a ser o padrão da próxima compra" |
| "Tratar erros do pagamento" | quais erros? | "Sem resposta do gateway em 10 s, o pedido fica 'aguardando pagamento' e o cliente vê 'Estamos confirmando seu pagamento'" |

Um bom critério tem um comportamento, dado concreto, resultado observável,
pelo menos um caminho negativo e nenhuma dependência do desenho da tela.

## Example Mapping passo a passo

Técnica de Matt Wynne (Cucumber) para descobrir regras com exemplos antes do
código. Cartões coloridos, físicos ou num quadro virtual:

| Cor | Significa |
| --- | --- |
| Amarelo | a história |
| Azul | uma regra (vira critério de aceite) |
| Verde | um exemplo concreto da regra (vira cenário ou caso de teste) |
| Vermelho | uma pergunta que ninguém na sala sabe responder |

1. Ponha a história (amarelo) no topo.
2. Liste as regras conhecidas (azul) lado a lado, abaixo dela.
3. Para cada regra, peça exemplos (verde): "um caso em que acontece" e "um em
   que não acontece". Frases curtas com dados ("Ana usa o link 29 min depois →
   troca a senha"), ainda não Gherkin. Exemplos costumam revelar regras novas:
   ganham um cartão azul.
4. Dúvida que trava a conversa vira cartão vermelho com dono, e a conversa
   segue. Não gaste 10 minutos discutindo o que só o jurídico responde.
5. Feche em 25 minutos com voto de polegar: está pronta para desenvolver?

Como ler o mapa:

- **Muitos vermelhos:** não está pronta; responda antes de começar.
- **Muitos azuis:** história grande; divida por regra.
- **Regra com muitos verdes:** regra complexa; considere tabela de decisão
  (`references/design-de-testes.md`) ou divisão.
- **Regra sem verde:** ninguém a entendeu de verdade.
- **Não fechou em 25 minutos:** grande ou incerta demais.

## Three amigos em 25 minutos

Negócio (PO ou analista), desenvolvimento e teste: são perspectivas, não
cargos. De 3 a 5 pessoas. Preparo: o PO traz objetivo e regras conhecidas; o
QA lê antes e chega com perguntas e riscos.

| Minutos | O quê | Quem puxa |
| --- | --- | --- |
| 0–3 | problema e valor para o usuário (não a solução) | PO |
| 3–18 | Example Mapping: regras, exemplos, perguntas | QA facilita |
| 18–22 | riscos e não funcionais: segurança, dados, performance, acessibilidade, o que quebra em volta | QA e dev |
| 22–25 | decisão: pronta, dividir ou voltar com respostas; dono de cada pergunta | todos |

Saída: regras e exemplos registrados na história, perguntas com dono, divisão
sugerida e notas de teste (o que automatizar e em que nível). Erros comuns:
virar reunião de solução técnica; QA só ouvindo; conversa sem exemplos
concretos; terminar sem decisão; convidar dez pessoas.

## Gherkin

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

`Given` descreve estado, não navegação. `When` é um evento. `Then` é algo que
o usuário ou um sistema externo observa. Tags (`@smoke`, `@wip`) selecionam
execuções. O mapeamento para português está em
[Gherkin em português](#gherkin-em-português).

### Declarativo vs imperativo

Imperativo (ruim): roteiro de cliques que quebra a cada redesenho e esconde a
regra.

```gherkin
Cenário: Aplicar cupom
  Dado que eu acesso "https://loja.exemplo.com/login"
  E preencho o campo "#email" com "ana@exemplo.com"
  E preencho o campo "#senha" com "Secreta123"
  E clico no botão "Entrar"
  E clico no menu "Carrinho"
  Quando digito "DEZ10" no campo "cupom"
  E clico em "Aplicar"
  Então vejo "R$ 180,00" no elemento ".total"
```

Declarativo (bom): diz o quê; o como fica nas step definitions.

```gherkin
Cenário: Cupom percentual reduz o subtotal
  Dado que existe o cupom "DEZ10" de 10% de desconto
  E que Ana tem R$ 200,00 em produtos no carrinho
  Quando Ana aplica o cupom "DEZ10"
  Então o subtotal com desconto é R$ 180,00
```

### Um comportamento por cenário

- Um único `Quando`. Se precisa de dois, são dois cenários, ou o primeiro é
  contexto e vira `Dado`.
- O título diz a regra ("Link expirado não troca a senha"), não "CT-042".
- Cenários independentes: nenhum depende de outro nem da ordem de execução.

### Contexto (Background) com parcimônia

Só passos `Dado` que **todos** os cenários do bloco precisam e que o leitor
precisa ver para entender; até três ou quatro linhas. Contexto longo esconde
dados relevantes e faz o leitor esquecer de onde veio o estado. Preparação
técnica (limpar banco, autenticar o cliente HTTP) vai em hooks, não no
Contexto. Se só parte dos cenários usa, o passo pertence a esses cenários.

### Esquema do cenário com exemplos nos limites

Cada linha da tabela deve representar uma partição ou um limite diferente;
trinta linhas da mesma classe só deixam a suíte lenta. Nomeie os blocos de
exemplos. Quando o resultado muda de natureza (sucesso vs. recusa), faça dois
esquemas: uma coluna "resultado: sucesso/erro" esconde dois comportamentos em
um.

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

`Rule` agrupa cenários sob uma regra de negócio e pode ter seu próprio
`Background`. Espelha o Example Mapping: cartão azul vira `Regra`, verdes
viram `Cenário`. Implementações antigas de algumas ferramentas não reconhecem
a palavra-chave; confirme o suporte na versão que o time usa.

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

Armadilhas: `Exemplo:` é sinônimo de **Cenário**, e `Cenários:` é sinônimo de
**Exemplos** — fácil de confundir. A palavra-chave não faz parte do texto
casado pela step definition: em "Dado que Ana tem…", o passo é "que Ana tem…".
Dado/Dada/Dados/Dadas só existem para concordância.

### Anti-padrões

| Anti-padrão | Exemplo | Correção |
| --- | --- | --- |
| Clique a clique | "E clico em 'Entrar'" | intenção: "Dado que Ana está autenticada" |
| `Então` que descreve implementação | "Então é inserida linha em tb_pedido com status 3" | resultado de negócio: "Então o pedido aparece como 'Pago' para Ana" |
| Dados mágicos | "Dado o usuário 4711" | dado com significado: "Dado um cliente VIP com 2 pedidos atrasados" |
| Vários `Quando` | Quando… Então… Quando… Então… | um cenário por comportamento |
| `Então` sem verificação | "Então o sistema processa a solicitação" | algo observável e que possa falhar |
| Esquema com coluna sucesso/erro | `\| resultado \|` com "ok" e "erro" | dois esquemas |
| Passo com conjunções | "Dado que Ana está logada e tem itens e um cupom" | passos separados |
| Contexto longo | dez passos antes de cada cenário | hooks ou passos no próprio cenário |
| Feature como roteiro de teste | "Cenário: CT-042 caminho feliz" | título que diz a regra |

## Step definitions e ferramentas

Princípios:

- **Passos finos.** O passo traduz a frase em uma chamada para a camada de
  automação (cliente de API, page object, construtor de dados). Lógica no passo
  se duplica entre passos parecidos.
- **Reuso pela linguagem do domínio.** "Ana tem R$ 200,00 no carrinho" pode
  montar o carrinho pela API em vez da tela: o mesmo passo serve a vários
  cenários e roda em segundos.
- **Estado pelo contexto do cenário** (o `World` do Cucumber, o `context` do
  Behave, fixtures do pytest-bdd), nunca por variáveis globais ou pela ordem.
- Passo não chama passo; extraia uma função.
- Organize por domínio (`carrinho.steps.js`, `pagamento.steps.js`), não por
  arquivo `.feature`, para não ter cinco versões de "clico em salvar".
- Mantenha um glossário: duas frases para a mesma coisa duplicam passos; dois
  passos que casam a mesma frase são erro de ambiguidade.

Exemplo em cucumber-js para o cenário declarativo acima. `this.api` é um
cliente HTTP criado no `World` do projeto (ilustrativo, não executado):

```javascript
// features/step_definitions/carrinho.steps.js
const { Given, When, Then, defineParameterType } = require('@cucumber/cucumber');
const assert = require('node:assert/strict');

// "1.234,56" -> 123456 centavos, sem ponto flutuante
defineParameterType({
  name: 'valor',
  regexp: /\d{1,3}(?:\.\d{3})*,\d{2}/,
  transformer: (texto) => Number(texto.replace(/\D/g, '')),
});

Given('que existe o cupom {string} de {int}% de desconto', async function (codigo, percentual) {
  await this.api.criarCupom({ codigo, percentual });
});

Given('que {word} tem R$ {valor} em produtos no carrinho', async function (nome, centavos) {
  this.cliente = await this.api.criarCliente({ nome });
  await this.api.adicionarItem(this.cliente.id, { precoCentavos: centavos });
});

When('{word} aplica o cupom {string}', async function (_nome, codigo) {
  this.carrinho = await this.api.aplicarCupom(this.cliente.id, codigo);
});

Then('o subtotal com desconto é R$ {valor}', function (centavos) {
  assert.equal(this.carrinho.subtotalComDescontoCentavos, centavos);
});
```

| Ferramenta | Linguagem | Observação |
| --- | --- | --- |
| Cucumber (cucumber-js, Cucumber-JVM, cucumber-ruby) | JS/TS, Java/Kotlin, Ruby | referência do ecossistema; Cucumber Expressions |
| Reqnroll | .NET | sucessor open source do SpecFlow, criado pelo autor original; o SpecFlow chegou ao fim de vida em 31/12/2024 |
| Behave | Python | estado compartilhado via `context` |
| pytest-bdd | Python | plugin do pytest; reaproveita fixtures |
| playwright-bdd | JS/TS | gera testes do Playwright Test a partir dos `.feature`, mantendo fixtures e paralelismo |
| Godog | Go | mantido na organização Cucumber |

## Quando não usar Gherkin

BDD é conversa (descoberta), formulação e automação; Gherkin é só a
formulação. Ele vale quando pessoas de negócio leem e discutem os cenários.
Não use quando:

- Ninguém de negócio lê os `.feature`: vira uma camada de tradução a mais para
  manter. Teste no código com nomes descritivos comunica o mesmo.
- O alvo é cálculo com muitas variações: teste parametrizado no nível unitário
  é mais direto e mais rápido.
- O teste é técnico: performance, segurança, contrato de API, infraestrutura,
  layout visual.
- O QA escreve sozinho, depois do código: é documentação de teste com sintaxe
  extra, não BDD.
- O trabalho é exploratório: charter e notas servem melhor.

Example Mapping e three amigos valem mesmo sem Gherkin.

## Exemplo completo: recuperação de senha

### História original

> Como usuário, quero recuperar minha senha para acessar o sistema caso eu a
> esqueça. Critérios: o usuário recebe um e-mail com um link; o link deve
> expirar; o processo deve ser seguro e fácil; tratar e-mails inválidos etc.

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

### Critérios reescritos (regra + exemplo)

1. A resposta não revela se o e-mail tem conta. Ex.: "ana@" (com conta) e
   "bia@" (sem conta) veem a mesma mensagem; só Ana recebe e-mail.
2. O link vale por até 30 minutos, inclusive, e uma única vez. Ex.: enviado às
   10:00:00, aceito às 10:30:00, recusado às 10:30:01.
3. Só o link mais recente vale. Ex.: links das 10:00 e das 10:05; o das 10:00
   é recusado.
4. Trocar a senha encerra todas as sessões e envia aviso ao titular.
5. No máximo 5 pedidos por e-mail por hora. Ex.: o 5º envia; o 6º não.

Ficam fora do Gherkin, como testes técnicos ou checklist: token fora de logs,
acessibilidade do fluxo, regras da nova senha (já cobertas no cadastro).

### Cenários

Os horários pressupõem relógio controlado pelo teste (relógio falso injetado),
nunca espera real.

```gherkin
# language: pt
Funcionalidade: Recuperação de senha
  Para voltar a acessar a conta quando esquece a senha,
  o titular redefine a senha por um link enviado ao e-mail cadastrado.

  Regra: A resposta não revela se o e-mail tem conta

    Cenário: Pedido para e-mail com conta envia o link
      Dado que existe uma conta com o e-mail "ana@exemplo.com"
      Quando a recuperação de senha é pedida para "ana@exemplo.com"
      Então a resposta é "Se houver uma conta com esse e-mail, enviaremos um link."
      E um link de redefinição é enviado para "ana@exemplo.com"

    Cenário: Pedido para e-mail sem conta não envia nada
      Dado que não existe conta com o e-mail "bia@exemplo.com"
      Quando a recuperação de senha é pedida para "bia@exemplo.com"
      Então a resposta é "Se houver uma conta com esse e-mail, enviaremos um link."
      Mas nenhum e-mail é enviado

  Regra: O link vale por até 30 minutos e uma única vez

    Contexto:
      Dado que Ana recebeu um link de redefinição às 10:00:00

    Esquema do Cenário: Link dentro do prazo troca a senha
      Quando Ana usa o link às <horário> para definir a senha "NovaSenha2026"
      Então Ana consegue entrar com a senha "NovaSenha2026"

      Exemplos: até o limite
        | horário  |
        | 10:29:59 |
        | 10:30:00 |

    Cenário: Link vencido não troca a senha
      Quando Ana usa o link às 10:30:01 para definir a senha "NovaSenha2026"
      Então a troca é recusada com "Este link expirou. Peça um novo."
      E a senha de Ana continua a mesma

    Cenário: Link já usado não troca a senha de novo
      Dado que Ana usou o link às 10:05:00 para definir a senha "NovaSenha2026"
      Quando Ana usa o mesmo link às 10:06:00 para definir a senha "OutraSenha2026"
      Então a troca é recusada com "Este link já foi usado."
      E Ana consegue entrar com a senha "NovaSenha2026"

  Regra: Só o link mais recente vale

    Cenário: Novo pedido invalida o link anterior
      Dado que Ana recebeu links de redefinição às 10:00:00 e às 10:05:00
      Quando Ana usa o link das 10:00:00 às 10:06:00
      Então a troca é recusada com "Este link expirou. Peça um novo."

  Regra: Trocar a senha encerra as sessões e avisa o titular

    Cenário: Sessões abertas são encerradas após a troca
      Dado que Ana está conectada no celular e no notebook
      Quando Ana redefine a senha pelo link
      Então as duas sessões são encerradas
      E Ana recebe um e-mail avisando que a senha foi trocada

  Regra: No máximo 5 pedidos por e-mail por hora

    Cenário: Quinto pedido na mesma hora ainda envia o link
      Dado que já foram feitos 4 pedidos para "ana@exemplo.com" na última hora
      Quando a recuperação de senha é pedida para "ana@exemplo.com"
      Então um link de redefinição é enviado para "ana@exemplo.com"

    Cenário: Sexto pedido na mesma hora não envia e-mail
      Dado que já foram feitos 5 pedidos para "ana@exemplo.com" na última hora
      Quando a recuperação de senha é pedida para "ana@exemplo.com"
      Então a resposta é "Muitas solicitações. Tente de novo mais tarde."
      E nenhum e-mail é enviado
```

O que a revisão rendeu: cinco regras explícitas onde havia quatro frases
vagas, uma pergunta aberta com dono e uma nova dúvida que só apareceu ao
escrever o último cenário — "na última hora" é janela deslizante ou hora
cheia? Volta para o PO antes do desenvolvimento.
