# Design de testes

Como derivar casos que encontram defeitos com poucas execuções: escolha da
técnica, cada técnica a fundo, exploratório, dados de borda e critério de
parada. Leia para projetar casos, revisar cobertura ou planejar exploração.

## Sumário

- [Como escolher a técnica](#como-escolher-a-técnica)
- [Partição de equivalência](#partição-de-equivalência)
- [Valor-limite](#valor-limite)
- [Tabela de decisão](#tabela-de-decisão)
- [Transição de estados](#transição-de-estados)
- [Pairwise e combinatório](#pairwise-e-combinatório)
- [Cenários, jornadas e casos de uso](#cenários-jornadas-e-casos-de-uso)
- [Caixa-branca](#caixa-branca)
- [Técnicas baseadas em experiência](#técnicas-baseadas-em-experiência)
- [Teste exploratório](#teste-exploratório)
- [Catálogo de dados de borda e hostis](#catálogo-de-dados-de-borda-e-hostis)
- [Exemplo trabalhado: formulário de cadastro](#exemplo-trabalhado-formulário-de-cadastro)
- [Quantos testes bastam](#quantos-testes-bastam)

## Como escolher a técnica

A técnica vem da **forma da regra**, não da preferência de quem testa. As
técnicas se somam; no dia a dia, partição + valor-limite + suposição de erro
rendem mais.

| Situação no requisito | Técnica principal | Complemento |
| --- | --- | --- |
| Campo com faixa, tamanho ou quantidade | Partição + valor-limite | dados hostis do catálogo |
| Lista fechada de opções (tipo de conta, UF, plano) | Partição (uma classe por opção que muda o comportamento) | valor fora da lista via API |
| "Se A e B, mas não C, então…" | Tabela de decisão | valor-limite em cada condição numérica |
| Status, ciclo de vida, assistente em etapas | Transição de estados | concorrência entre transições |
| Muitas configurações independentes (navegador, SO, idioma) | Pairwise | combinações de risco conhecido, à mão |
| Fluxo de ponta a ponta com várias telas ou serviços | Cenário / jornada | interrupções e retomada |
| Lógica crítica no código (preço, permissão, antifraude) | Caixa-branca (ramos, MC/DC) | teste de mutação |
| Pouca especificação, funcionalidade nova, prazo curto | Exploratório com charter | suposição de erro |
| Área com histórico de defeitos | Suposição de erro + checklist | regressão dirigida |

## Partição de equivalência

Uma partição é uma **hipótese**: "o sistema trata todos estes valores do mesmo
jeito". Se o código separa valores dentro da classe (frete por faixa de CEP,
preço por faixa de quantidade), divida a classe. Fontes de classes: faixas,
listas de opções, formatos, tipos, presença e regras de negócio.

**Combine classes válidas; isole as inválidas.** Valores válidos podem dividir
um caso. Cada classe inválida tem caso próprio, com o resto válido. Motivo: se
o caso tem idade 17 **e** e-mail sem `@`, a validação pode parar no e-mail; o
teste passa ("recusou") e esconde que a idade 17 seria aceita.

**Particione também a saída.** Análise de crédito com saídas "aprovado",
"aprovado com limite reduzido", "análise manual" e "recusado" exige um caso que
produza cada uma, mesmo com as entradas cobertas. Cada mensagem de erro é uma
classe de saída: sem caso que a dispare, pode estar errada ou inalcançável.

Armadilhas: em JSON, campo **ausente**, `null` e `""` são três classes; a tela
bloqueia a classe inválida e a API aceita (teste as importantes direto na API);
o valor padrão e o zero ("sem limite", "gratuito", divisão) são classes
especiais.

## Valor-limite

Defeitos se concentram nas fronteiras (`>` no lugar de `>=`, contagem que
começa em 0 ou 1). O ISTQB CTFL 4.0 descreve duas variantes:

| Variante | Valores por limite | Faixa 18–65 |
| --- | --- | --- |
| 2 valores | o limite e o vizinho na partição adjacente | 17, 18, 65, 66 |
| 3 valores | o limite e os dois vizinhos | 17, 18, 19, 64, 65, 66 |

Use 3 valores onde o risco é alto. O que só ela pega: na regra "a partir de 18
anos", se o código diz `idade == 18` em vez de `idade >= 18`, os testes 17
(recusa) e 18 (aceita) passam; só o 19 revela o defeito.

O **passo** do vizinho depende do tipo: 1 para inteiros, R$ 0,01 para moeda,
1 caractere, 1 dia, ou a precisão armazenada (segundo, milissegundo) para
horários. Gere os valores com `python scripts/valores_limite.py numero --min 18 --max 65`
e `python scripts/valores_limite.py texto --min 3 --max 50`.

- **Textos.** O que a regra conta: caracteres visíveis, pontos de código,
  unidades UTF-16 (`length` do JavaScript conta um emoji simples como 2) ou
  bytes ("ã" ocupa 2 em UTF-8)? Espaços nas pontas e máscara entram na conta?
- **Datas.** "Até dia 10" é inclusivo? Até 23:59:59 de qual fuso? Teste o
  último instante válido e o primeiro inválido, viradas de mês (28, 29, 30, 31)
  e de ano. "Maior de 18" se testa no dia do 18º aniversário e na véspera.
- **Coleções.** 0, 1, máximo e máximo + 1 itens. Paginação de 20: 0, 1, 19, 20,
  21, 40 e 41 itens.
- **Moeda.** "Frete grátis a partir de R$ 199,00" testa R$ 198,99 e R$ 199,00.
  R$ 100,00 em 3 parcelas: 33,33 + 33,33 + 33,34 precisa fechar o total. Se a
  regra de arredondamento (metade para cima ou bancário) não está escrita, é
  pergunta para o PO.

### Limites ocultos

Ninguém escreveu, mas o sistema tem. Procure no esquema do banco, na infra e no código.

| Limite oculto | Valor conhecido | Teste |
| --- | --- | --- |
| Inteiro de 32 bits com sinal | 2.147.483.647 | quantidade, ID ou centavos no máximo e +1 (em centavos, int32 trava em R$ 21.474.836,47) |
| Inteiro seguro em JavaScript | 2^53 − 1 = 9.007.199.254.740.991 | ID int64 lido por JS perde precisão: 9007199254740993 vira …992 |
| Coluna menor que a validação da tela | ex.: tela aceita 100, coluna `VARCHAR(80)` | 100 caracteres → erro 500 ou truncamento silencioso |
| Charset do banco | `utf8` do MySQL (utf8mb3) não guarda emoji | gravar 😀 e reler |
| Corpo da requisição no proxy | nginx: `client_max_body_size` padrão 1 MB | upload logo acima → 413 |
| Corpo JSON no framework | Express: `express.json()` padrão 100 kb | payload de 101 kb |
| Gateway, balanceador, CDN | teto de payload e de timeout próprios (confira na documentação do provedor) | requisição lenta logo acima do timeout |
| Nome de arquivo | 255 bytes na maioria dos sistemas de arquivos | nome com 256 bytes, com acentos |
| Tempo Unix em 32 bits | 2038-01-19 03:14:07 UTC | vencimentos depois de 2038 |

## Tabela de decisão

Use quando o resultado depende da **combinação** de condições. Cada coluna é
uma regra. Exemplo: (1) frete grátis para subtotal a partir de R$ 199,00
(antes de descontos) ou para cliente VIP; (2) cupom dá 10%; (3) VIP dá 5%;
(4) cupom e desconto VIP não acumulam — vale o cupom.

**Tabela completa** (2³ = 8 colunas; S = sim, N = não, X = executa a ação):

| | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C1 Subtotal ≥ R$ 199,00 | S | S | S | S | N | N | N | N |
| C2 Cupom válido | S | S | N | N | S | S | N | N |
| C3 Cliente VIP | S | N | S | N | S | N | S | N |
| A1 Frete grátis | X | X | X | X | X | | X | |
| A2 Desconto do cupom (10%) | X | X | | | X | X | | |
| A3 Desconto VIP (5%) | | | X | | | | X | |

**Tabela colapsada.** Colunas com as mesmas ações que diferem em uma só
condição se fundem, e essa condição vira "–" (irrelevante):

| | R1+R5 | R3+R7 | R2 | R4 | R6 | R8 |
| --- | --- | --- | --- | --- | --- | --- |
| C1 Subtotal ≥ R$ 199,00 | – | – | S | S | N | N |
| C2 Cupom válido | S | N | S | N | S | N |
| C3 Cliente VIP | S | S | N | N | N | N |
| Ações | frete grátis + cupom | frete grátis + VIP | frete grátis + cupom | frete grátis | cupom | nenhuma |

Cada coluna vira um caso com dados concretos. R1+R5: cliente VIP, cupom
`DEZ10`, subtotal R$ 150,00 → frete R$ 0,00, desconto R$ 15,00, sem os 5%.
Ponha C1 nos limites (R$ 198,99 e R$ 199,00) para juntar as técnicas.

O colapso confia que o código segue a estrutura da regra; com 8 colunas, a
completa é barata. Marque combinações impossíveis como "N/A" em vez de apagar.
A tabela também acha lacunas: se o cupom leva o subtotal de R$ 200,00 a
R$ 180,00, o frete segue grátis? Sem o "antes de descontos", seria um defeito
de requisito achado antes do código.

## Transição de estados

O defeito típico está nas transições que o sistema permite sem dever (enviar
pedido não pago, reembolsar duas vezes). Exemplo de ciclo de vida de pedido;
"–" = transição inválida (recusar sem mudar o estado):

| Estado \ Evento | pagar | separar | enviar | entregar | cancelar | reembolsar |
| --- | --- | --- | --- | --- | --- | --- |
| Criado | Pago | – | – | – | Cancelado | – |
| Pago | – | Separado | – | – | Cancelado | – |
| Separado | – | – | Enviado | – | Cancelado | – |
| Enviado | – | – | – | Entregue | – | – |
| Entregue | – | – | – | – | – | Reembolsado [arrependimento em até 7 dias, CDC art. 49] |
| Cancelado | – | – | – | – | – | Reembolsado [se houve pagamento] |
| Reembolsado | – | – | – | – | – | – |

| Critério de cobertura | Exige | Neste exemplo |
| --- | --- | --- |
| Todos os estados | visitar cada estado | 7 estados |
| Transições válidas (0-switch) | executar cada transição válida | 9 transições |
| Todas as transições | válidas + tentar cada inválida | 9 válidas + 33 células "–" |
| 1-switch | cada sequência de duas transições seguidas | 9 sequências, uma impossível |

As 9 transições válidas cabem em 4 caminhos: Criado → Pago → Separado →
Enviado → Entregue → Reembolsado; Criado → Cancelado; Criado → Pago →
Cancelado → Reembolsado; Criado → Pago → Separado → Cancelado → Reembolsado.

Das 33 inválidas, priorize as que dão prejuízo: pagar pedido já pago, enviar
pedido Criado, cancelar Enviado, reembolsar duas vezes, entregar Cancelado.
Teste-as pela API: a tela esconde o botão, o back-end esquece a regra.

**Por que 1-switch importa aqui:** a guarda "se houve pagamento" faz
Cancelado → Reembolsado depender de **como** o pedido chegou a Cancelado. A
sequência Criado → Cancelado → reembolsar precisa ser recusada, e 0-switch não
obriga esse teste. Guarda que depende do histórico indica subestados
escondidos ("cancelado sem pagamento", "aguardando reembolso"); sugira
separá-los. E teste concorrência: cancelar e enviar o mesmo pedido ao mesmo
tempo precisa terminar em um estado coerente.

## Pairwise e combinatório

Para vários parâmetros independentes com produto cartesiano grande demais:
pairwise garante que **todo par de valores** aparece em algum caso. Estudos do
NIST com falhas reais indicam que a maioria é disparada por um ou dois
parâmetros e praticamente todas por até seis; n-wise (3-wise ou mais) aumenta
a força quando o risco justifica, com custo que cresce rápido.

Exemplo: navegador (chrome, firefox, safari) × SO (windows, macos) × idioma
(pt, en) = 12 combinações; restrição: Safari só no macOS. Gere com
`python scripts/pairwise.py navegador=chrome,firefox,safari so=windows,macos idioma=pt,en`.
Seis linhas cobrem todos os pares possíveis:

| # | Navegador | SO | Idioma |
| --- | --- | --- | --- |
| 1 | chrome | windows | pt |
| 2 | chrome | macos | en |
| 3 | firefox | windows | en |
| 4 | firefox | macos | pt |
| 5 | safari | macos | pt |
| 6 | safari | macos | en |

O ganho cresce com os parâmetros: 4 parâmetros de 3 valores somam 81
combinações, e 9 linhas cobrem todos os pares (arranjo ortogonal L9).

- **Restrições** vão declaradas ao gerador (no PICT, da Microsoft:
  `IF [so] = "windows" THEN [navegador] <> "safari";`); sem esse suporte,
  troque o valor proibido à mão e confira se nenhum par sumiu.
- Pairwise não sabe o que é arriscado: acrescente à mão as combinações de risco
  conhecido. Não use quando os parâmetros interagem por regra de negócio (é
  tabela de decisão) nem quando o produto cartesiano cabe no tempo.

## Cenários, jornadas e casos de uso

Cenários verificam se as partes funcionam **juntas** para um objetivo do
usuário ("cliente novo compra com PIX e acompanha a entrega") e acham defeitos
de integração (o cupom some do carrinho depois do login). De um caso de uso,
cubra o fluxo principal, cada alternativo (pagamento recusado) e cada exceção
(timeout do gateway). Use personas e dados com história (cartão vencido salvo)
e interrompa no meio. São caros: cubra as jornadas de receita ou legais.

## Caixa-branca

Casos derivados da estrutura do código:

```python
def aprova_credito(renda_ok: bool, score_alto: bool, tem_garantia: bool) -> bool:
    if renda_ok and (score_alto or tem_garantia):
        return True
    return False
```

| Critério | Exige | Casos mínimos aqui |
| --- | --- | --- |
| Instruções (statement) | cada linha executada | 2 |
| Decisão / ramo (branch) | cada saída de cada decisão | 2 |
| Condição | cada condição atômica verdadeira e falsa | 2, sem garantir a decisão |
| MC/DC | cada condição muda sozinha o resultado | 4 (N + 1) |
| Múltiplas condições | todas as combinações | 8 (2^N) |
| Caminhos | cada caminho do início ao fim | explode com laços |

Condição não implica decisão: (S, N, N) e (N, S, S) põem cada condição
verdadeira e falsa uma vez, e a decisão é falsa nos dois. Um conjunto MC/DC:

| Caso | renda_ok | score_alto | tem_garantia | Resultado | Prova a independência de |
| --- | --- | --- | --- | --- | --- |
| T1 | S | S | N | aprova | (base) |
| T2 | N | S | N | recusa | renda_ok, com T1 |
| T3 | S | N | N | recusa | score_alto, com T1 |
| T4 | S | N | S | aprova | tem_garantia, com T3 |

MC/DC é exigido pela DO-178C no software aeronáutico de nível A e fortemente
recomendado pela ISO 26262 para ASIL D. Fora disso, aplique-o à mão nas
decisões que movem dinheiro ou permissão. Curto-circuito (`and`, `&&`) muda o
que as ferramentas medem. Em caminhos, a complexidade ciclomática (decisões
binárias + 1) dá o número de caminhos independentes. Cobertura mede execução,
não verificação: a força das asserções se mede com mutação
(`references/unitarios-e-integracao.md`).

## Técnicas baseadas em experiência

- **Suposição de erro.** Liste erros que desenvolvedores cometem e defeitos que
  o sistema já teve, e provoque-os: divisão por zero, lista vazia, opcional
  nulo, fuso, duplo envio, cache velho. Parta do catálogo do `SKILL.md`.
- **Ataques de falha.** A versão sistemática: escolha um modo de falha (entrada
  enorme, recurso esgotado, dependência fora do ar) e force cada mensagem e
  estado de erro. Guia: "que erro existe no código e eu nunca vi na tela?".
- **Checklists.** Verificações mantidas pelo time (formulário, upload, endpoint
  novo). Para não virar ritual, inclua item quando um defeito escapar e corte o
  que nunca acha nada.

## Teste exploratório

Projetar, executar e aprender ao mesmo tempo, com missão, tempo e registro.
**Charter:** **Explore** <alvo> **com** <recursos> **para descobrir**
<informação>. Exemplos:

- Explore o checkout com cupons expirados, esgotados e de outro cliente para
  descobrir se algum desconto indevido é aplicado.
- Explore a importação de planilha com arquivos de 0 byte, 50 MB e colunas
  trocadas para descobrir se linhas se perdem sem aviso.

"Explore o sistema" não orienta; charter estreito demais vira roteiro. Template
em `assets/templates/charter-exploratorio.md`.

**SBTM (Session-Based Test Management).** A unidade é a sessão: um charter,
tempo fixo sem interrupção (curta ~60, normal ~90, longa ~120 minutos) e notas
com horário (o que testou, ideias, dúvidas, bugs). No fim, estime o tempo em
teste, em investigação de bugs e em preparação, e quanto foi no charter versus
oportunidade. O debrief de 10 a 15 minutos segue PROOF: Passado, Resultados,
Obstáculos, Perspectiva (novos charters) e Sentimentos (o que preocupa).

**Tours** (James Whittaker): do dinheiro (o que vende o produto), dos marcos
(funções principais em ordens diferentes), FedEx (seguir um dado), do lixeiro
(todas as telas, metodicamente), do bairro perigoso (áreas com mais bugs), do
sabotador (cortar rede, disco, dependências), antissocial (o oposto do
esperado), obsessivo (repetir a ação), do sedentário (o mínimo, aceitar os
padrões), da madrugada (deixar aberto por horas).

### SFDPOT: o que explorar

Elementos do produto (James Bach); versões novas somam **I** de Interfaces.

| Elemento | Pergunta | Exemplo |
| --- | --- | --- |
| Estrutura | do que é feito? | arquivo de configuração ausente, tabela vazia, fila parada |
| Função | o que faz? | cada cálculo, cada mensagem de erro, cada botão |
| Dados | o que processa? | tamanhos, tipos, acentos, dados antigos migrados |
| Interfaces | por onde se fala com ele? | tela, API, importação CSV, webhook |
| Plataforma | do que depende? | navegador, SO, serviço de terceiro, versão do banco |
| Operações | como é usado de verdade? | celular com rede ruim, usuário que cola dados do Excel |
| Tempo | o que muda com o tempo? | fuso, timeout, concorrência, virada de mês, ordem de eventos |

### FEW HICCUPPS: como reconhecer um problema

Heurísticas de oráculo (James Bach e Michael Bolton) para quando não há
especificação. Há problema quando o produto é **inconsistente com**:

| Oráculo | Exemplo de inconsistência |
| --- | --- |
| Familiaridade (problemas conhecidos) | "Pagar" aceita duplo clique — padrão clássico de cobrança dupla |
| Explicabilidade | ninguém explica por que o total mudou ao trocar o CEP e voltar ao original |
| Mundo | aceita 31/02, CEP inexistente ou frete negativo |
| História | a versão anterior exportava "João"; esta exporta "Jo�o" |
| Imagem | erro exibe "NullPointerException" ao cliente do banco |
| Produtos comparáveis | a planilha da área financeira calcula outros juros |
| Promessas (claims) | o site promete "entrega em 24 h" e o sistema calcula 3 dias |
| Expectativa do usuário | "Cancelar" apaga o rascunho que o usuário queria manter |
| Produto (coerência interna) | "CPF" em uma tela, "Documento" em outra; formatos de data diferentes |
| Propósito | relatório de fechamento do mês omite pedidos do último dia |
| Padrões e leis | preço cobrado diferente do anunciado (CDC); dado pessoal em log (LGPD) |

### Heurísticas rápidas

- **CRUD:** criar, ler, atualizar e excluir cada entidade e ver o efeito nas
  relacionadas (excluir cliente com pedidos, editar produto em carrinhos).
- **Goldilocks** (grande demais, pequeno demais, na medida); **zero, um,
  muitos**; **nenhum, alguns, todos**.
- **Seguir o dado:** cadastre "Ação & Cia D'Ávila" e veja como sai na tela, no
  e-mail, no PDF, no CSV, na busca e no relatório.
- **Interrupções:** sair no meio, perder a rede, fechar o app, receber
  ligação, deixar a sessão expirar, voltar e reenviar.

## Catálogo de dados de borda e hostis

| Categoria | Valores | O que costuma quebrar |
| --- | --- | --- |
| Invisíveis | espaço de largura zero (U+200B), ZWJ (U+200D), BOM (U+FEFF) | "admin" e "admin" + U+200B: dois usuários idênticos na tela |
| Direção | texto árabe ou hebraico; RTL override (U+202E) | layout invertido; "fdp.exe" exibido como "exe.pdf" |
| Emoji com ZWJ | 👨‍👩‍👧‍👦 | 1 caractere visível, 7 pontos de código, 11 unidades UTF-16, 25 bytes UTF-8: limites e cortes divergem |
| Homóglifos | "pаypal" com "а" cirílico (U+0430) | usuário ou domínio que imita outro |
| Combinação (Zalgo) | letras com dezenas de diacríticos empilhados | layout transbordado, contagem de tamanho |
| Normalização | "José" em NFC e em NFD | unicidade e busca falham com o mesmo nome |
| Caixa e locale | "ß" maiúsculo vira "SS"; "İ" minúsculo vira 2 pontos de código | tamanho muda ao converter; comparação em turco |
| Tamanho | 1, 255, 256, 65.535, 65.536 caracteres | limites de `VARCHAR(255)` e de campos de 16 bits |
| Controle | quebra de linha, tab, byte nulo (U+0000) | PostgreSQL recusa byte nulo em texto; CSV quebra |
| Números | -0, NaN, Infinity, 1e309 | `JSON.stringify(NaN)` vira `null`; Python grava `NaN` (JSON inválido); 1e309 vira Infinity |
| Inteiros | 2^31 − 1 = 2.147.483.647; 2^53 + 1 (ver limites ocultos) | estouro de int32; precisão perdida em JS |
| Decimais | 0,1 + 0,2 = 0,30000000000000004 em ponto flutuante | moeda em float; -0,001 arredondado exibido "-0,00" |
| Bissextos | 2000-02-29 válido; 1900-02-29 e 2100-02-29 inválidos | regra "divisível por 4" sem a exceção de 100/400; o Excel aceita 29/02/1900 |
| Datas especiais | 1970-01-01; 2038-01-19 03:14:07 UTC; 31/12 23:59:59 | época 0 lida como "vazio"; estouro de 32 bits; virada de ano |
| Fusos | data sem hora em JS (`new Date("2026-03-10")`) é lida como UTC | no Brasil (UTC−3) exibe 09/03 |
| Horário de verão histórico | 04/11/2018 00:00 não existiu em São Paulo | nascimento salvo como 03/11 |
| Arquivos | 0 byte; exatamente no limite e +1 byte; "foto.jpg" que é PDF; "nota.pdf.exe" | validação pela extensão, não pelo conteúdo |
| Nome de arquivo | `../../etc/passwd`; 256 bytes; `CON` e `NUL` no Windows | path traversal, erro ao salvar |
| Identidade | D'Ávila, O'Connor; nome único (estrangeiros); Souza e Silva, Mello-Franco; Filho, Neto; sobrenome "Null"; nome social | apóstrofo quebra SQL ou escape; sobrenome obrigatório; corte do composto |

Injeção (`' OR '1'='1`, `<script>`, `{{7*7}}`) vale em todo campo de texto;
aprofundamento em `references/seguranca.md`.

## Exemplo trabalhado: formulário de cadastro

Regras dadas pelo PO:

- **R1 Nome:** 3 a 100 caracteres após remover espaços nas pontas; letras
  (com acento), espaço, apóstrofo e hífen.
- **R2 E-mail:** formato válido; único, sem diferenciar maiúsculas.
- **R3 CPF:** com ou sem máscara; dígitos verificadores válidos; único.
- **R4 Nascimento:** 18 anos completos na data do cadastro.
- **R5 Senha:** 8 a 64 caracteres, com pelo menos uma letra e um número.
- **R6 Termos:** aceite obrigatório. Todos os campos são obrigatórios.
- **Saídas:** sucesso → conta "pendente de confirmação" + e-mail de
  confirmação; erro de validação ou duplicidade → mensagem, nada gravado.

Suposição: cadastro em 05/10/2026, com relógio controlado no teste. Cada caso
parte do CAD-01 e muda só o que está em "Dados" (uma classe inválida por caso).

| ID | Caso | Dados | Esperado | Técnica |
| --- | --- | --- | --- | --- |
| CAD-01 | Cadastra com todos os campos válidos | Maria Silva; maria.silva@exemplo.com; 529.982.247-25; 15/03/1990; senhaForte1; termos aceitos | conta "pendente de confirmação"; 1 e-mail enviado | EP válidas + saída sucesso |
| CAD-02 | Aceita nome no mínimo | "Ana" | aceita | BVA mín |
| CAD-03 | Recusa nome abaixo do mínimo | "Al" | "Informe de 3 a 100 caracteres"; nada gravado | BVA mín−1 |
| CAD-04 | Aceita nome no máximo | 100 caracteres, com acentos | aceita e grava sem truncar | BVA máx + limite oculto |
| CAD-05 | Recusa nome acima do máximo | 101 caracteres | mesma mensagem do CAD-03 | BVA máx+1 |
| CAD-06 | Remove espaços antes de contar | "␣␣Al␣␣" | recusa (conta 2) | BVA + suposição de erro |
| CAD-07 | Aceita apóstrofo, hífen e acento | "Joana D'Ávila-Gonçalves" | aceita; grava igual ao digitado | EP válida |
| CAD-08 | Recusa dígito no nome | "Jo3o Silva" | recusa | EP inválida |
| CAD-09 | Aceita e-mail com subendereço | maria+loja@exemplo.com | aceita | EP válida |
| CAD-10 | Recusa e-mail sem domínio | maria@ | recusa | EP inválida |
| CAD-11 | Recusa e-mail duplicado em outra caixa | existe maria.silva@exemplo.com; envia Maria.Silva@Exemplo.com | mensagem de duplicidade; nenhuma conta nova | EP de saída |
| CAD-12 | Aceita CPF sem máscara | 52998224725 | aceita; grava normalizado | EP válida |
| CAD-13 | Recusa CPF com dígito verificador errado | 529.982.247-24 | recusa | EP inválida |
| CAD-14 | Recusa CPF de dígitos repetidos | 111.111.111-11 | recusa (passa no cálculo, mas é inválido) | suposição de erro |
| CAD-15 | Aceita quem faz 18 hoje | 05/10/2008 | aceita | BVA limite |
| CAD-16 | Recusa quem faz 18 amanhã | 06/10/2008 | recusa | BVA limite+1 dia |
| CAD-17 | Nascido em 29/02, ano atual não bissexto | 29/02/2008, cadastro em 28/02/2026 | **pergunta ao PO**: 18 anos em 28/02 ou em 01/03? | suposição de erro |
| CAD-18 | Recusa senha abaixo do mínimo | "abcdef1" (7) | recusa | BVA mín−1 |
| CAD-19 | Aceita senha no mínimo | "abcdefg1" (8) | aceita | BVA mín |
| CAD-20 | Aceita senha no máximo | 63 letras + "1" (64) | aceita, sem truncar | BVA máx |
| CAD-21 | Recusa senha acima do máximo | 64 letras + "1" (65) | recusa | BVA máx+1 |
| CAD-22 | Recusa senha sem número | "senhasemnumero" | recusa | EP inválida |
| CAD-23 | Recusa sem aceite dos termos | termos desmarcados | recusa; nada gravado | EP inválida |
| CAD-24 | Duplo clique cria uma só conta | dois cliques rápidos em "Cadastrar" | 1 conta; 1 e-mail | suposição de erro |
| CAD-25 | API valida igual à tela | POST direto com nome "Al" | 400 ou 422 com erro no campo; nada gravado | suposição de erro |

Levado ao refinamento: a mensagem de duplicidade revela quais e-mails têm
conta (enumeração), decisão de produto e segurança; regras de composição de
senha são desaconselhadas pelas diretrizes do NIST (SP 800-63B); acessibilidade
das mensagens de erro fica para `references/acessibilidade.md`.

## Quantos testes bastam

O critério de cobertura diz quando a técnica foi aplicada por inteiro, não
quando o produto está bom.

| Técnica | Cobertura mínima | Suba o nível quando |
| --- | --- | --- |
| Partição | cada classe válida e inválida (inclusive de saída) | classe de alto risco: mais de um valor |
| Valor-limite | 2 valores por limite | dinheiro, idade legal, prazo: 3 valores |
| Tabela de decisão | cada coluna viável da tabela colapsada | condições críticas: tabela completa |
| Transição de estados | cada transição válida (0-switch) | dinheiro ou guarda por histórico: inválidas + 1-switch |
| Pairwise | 100% dos pares | configuração crítica: 3-wise |
| Caixa-branca | 100% dos ramos | decisão de segurança ou regulada: MC/DC |
| Exploratório | cada charter planejado, com debrief | o debrief gera charters de risco alto |

Pare quando os três valerem juntos: (1) os riscos altos têm a cobertura acima
e o que ficou de fora está escrito com o risco que sobra; (2) testes novos
pararam de trazer informação nova (a taxa de defeitos caiu e nenhuma área
mostra instabilidade); (3) nenhum defeito crítico está aberto sem decisão
explícita de quem responde pelo produto. Se o prazo acabar antes, o critério
vira transparência: o que foi testado, o que não foi e o que você testaria com
mais um dia.
