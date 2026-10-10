# Design de testes

Como derivar casos que encontram defeitos com poucas execuções: escolha da técnica, cada técnica, exploratório, dados de borda e critério de parada. Base: `design-de-testes.md` e `SKILL.md` do brain-of-agent (MIT, conteúdo próprio, condensado) com V-17 e V-22. Rótulo geral: conhecimento próprio Inferido; não reverificado em fonte externa. Validado em 2026-10-10.

## Sumário

- [Como escolher a técnica](#como-escolher-a-técnica)
- [Partição de equivalência](#partição-de-equivalência)
- [Valor-limite](#valor-limite)
- [Tabela de decisão](#tabela-de-decisão)
- [Transição de estados](#transição-de-estados)
- [Pairwise](#pairwise)
- [Cenários e caixa-branca](#cenários-e-caixa-branca)
- [Baseadas em experiência](#baseadas-em-experiência)
- [Teste exploratório](#teste-exploratório)
- [Catálogo de dados de borda e hostis](#catálogo-de-dados-de-borda-e-hostis)
- [Mini-exemplo e critério de parada](#mini-exemplo-e-critério-de-parada)

## Como escolher a técnica

A técnica vem da **forma da regra**, não da preferência de quem testa. No dia a dia, partição + valor-limite + suposição de erro rendem mais.

| Situação no requisito | Técnica principal | Complemento |
| --- | --- | --- |
| Campo com faixa, tamanho ou quantidade | Partição + valor-limite | dados hostis do catálogo |
| Lista fechada (tipo de conta, UF, plano) | Partição (uma classe por opção que muda o comportamento) | valor fora da lista via API |
| "Se A e B, mas não C, então…" | Tabela de decisão | valor-limite em cada condição numérica |
| Status, ciclo de vida, assistente em etapas | Transição de estados | concorrência entre transições |
| Muitas configurações independentes | Pairwise | combinações de risco conhecido, à mão |
| Fluxo ponta a ponta com várias telas ou serviços | Cenário / jornada | interrupções e retomada |
| Lógica crítica no código (preço, permissão, antifraude) | Caixa-branca (ramos, MC/DC) | mutação |
| Pouca especificação, funcionalidade nova, prazo curto | Exploratório com charter | suposição de erro |
| Área com histórico de defeitos | Suposição de erro + checklist | regressão dirigida |

**Oráculo primeiro.** Antes do passo, saiba como decidirá se está certo. "Funciona corretamente" não é esperado. Fontes: especificação, lei ou tabela oficial, cálculo independente, versão anterior, produto comparável, consistência interna, expectativa razoável do usuário. Copiar o valor que a tela mostra é oráculo circular. Esperado ambíguo vira **pergunta ao PO** (ex.: "a partir de R$ 199" inclui 199,00? antes ou depois do cupom?), não palpite.

## Partição de equivalência

Uma partição é uma **hipótese**: "o sistema trata todos estes valores do mesmo jeito". Se o código separa valores dentro da classe (frete por faixa de CEP), divida a classe. Fontes de classes: faixas, listas, formatos, tipos, presença e regras de negócio.

- **Combine classes válidas; isole as inválidas.** Se o caso tem idade 17 **e** e-mail sem `@`, a validação pode parar no e-mail, o teste passa ("recusou") e esconde que a idade 17 seria aceita. Cada classe inválida tem caso próprio, com o resto válido.
- **Particione a saída.** Análise de crédito com saídas "aprovado", "limite reduzido", "análise manual" e "recusado" exige um caso para cada. Cada mensagem de erro é uma classe de saída: sem caso que a dispare, pode estar errada ou inalcançável.
- Em JSON, campo **ausente**, `null` e `""` são três classes. A tela bloqueia a classe inválida e a API aceita: teste as importantes direto na API. O valor padrão e o zero ("sem limite", "gratuito", divisão) são classes especiais.

## Valor-limite

Defeitos se concentram nas fronteiras (`>` no lugar de `>=`, contagem que começa em 0 ou 1).

| Variante | Valores por limite | Faixa 18–65 |
| --- | --- | --- |
| 2 valores | o limite e o vizinho na partição adjacente | 17, 18, 65, 66 |
| 3 valores | o limite e os dois vizinhos | 17, 18, 19, 64, 65, 66 |

Use 3 valores onde o risco é alto (dinheiro, idade legal, prazo). Só o terceiro pega o defeito: na regra "a partir de 18 anos", se o código diz `idade == 18` em vez de `>=`, os testes 17 (recusa) e 18 (aceita) passam; o 19 revela. O **passo** do vizinho depende do tipo: 1 para inteiro, R$ 0,01 para moeda, 1 caractere, 1 dia, ou a precisão armazenada (segundo, milissegundo).

- **Textos:** o que a regra conta: caracteres visíveis, pontos de código, unidades UTF-16 (o `length` do JavaScript conta um emoji simples como 2) ou bytes ("ã" ocupa 2 em UTF-8)? Espaços nas pontas e máscara entram na conta?
- **Datas:** "até dia 10" é inclusivo? Até 23:59:59 de qual fuso? Último instante válido e primeiro inválido; viradas de mês (28, 29, 30, 31) e de ano; "maior de 18" no dia do 18º aniversário e na véspera.
- **Coleções:** 0, 1, máximo e máximo + 1. Paginação de 20: 0, 1, 19, 20, 21, 40, 41.
- **Moeda:** "frete grátis a partir de R$ 199,00" testa 198,99 e 199,00. R$ 100,00 em 3 parcelas: 33,33 + 33,33 + 33,34 precisa fechar o total; regra de arredondamento não escrita é pergunta ao PO.

**Limites ocultos** (ninguém escreveu, o sistema tem; procure no esquema do banco, na infra e no código):

| Limite | Valor conhecido | Teste |
| --- | --- | --- |
| Inteiro de 32 bits com sinal | 2.147.483.647 | quantidade, ID ou centavos no máximo e +1 (em centavos, trava em R$ 21.474.836,47) |
| Inteiro seguro em JavaScript | 2^53 − 1 = 9.007.199.254.740.991 | ID int64 lido por JS perde precisão: 9007199254740993 vira …992 |
| Coluna menor que a validação da tela | tela aceita 100, coluna `VARCHAR(80)` | 100 caracteres → erro 500 ou truncamento silencioso |
| Charset do banco | `utf8` do MySQL (utf8mb3) não guarda emoji | gravar 😀 e reler |
| Corpo da requisição no proxy ou framework | nginx `client_max_body_size` padrão 1 MB; `express.json()` padrão 100 kb (valores padrão a confirmar na sua versão) | payload logo acima → 413 |
| Gateway, balanceador, CDN | teto de payload e timeout próprios | requisição lenta logo acima do timeout |
| Nome de arquivo | 255 bytes na maioria dos sistemas de arquivos | 256 bytes, com acentos |
| Tempo Unix em 32 bits | 2038-01-19 03:14:07 UTC | vencimentos depois de 2038 |

## Tabela de decisão

Use quando o resultado depende da **combinação** de condições. Regra de exemplo: (1) frete grátis para subtotal ≥ R$ 199,00 (antes de descontos) ou cliente VIP; (2) cupom dá 10%; (3) VIP dá 5%; (4) cupom e VIP não acumulam, vale o cupom.

Completa (2³ = 8 colunas; S/N, X = executa):

| | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C1 Subtotal ≥ R$ 199,00 | S | S | S | S | N | N | N | N |
| C2 Cupom válido | S | S | N | N | S | S | N | N |
| C3 Cliente VIP | S | N | S | N | S | N | S | N |
| A1 Frete grátis | X | X | X | X | X | | X | |
| A2 Desconto do cupom (10%) | X | X | | | X | X | | |
| A3 Desconto VIP (5%) | | | X | | | | X | |

Colapsada (colunas com as mesmas ações que diferem em uma só condição se fundem; a condição vira "–"): R1+R5 (frete grátis + cupom), R3+R7 (frete grátis + VIP), R2, R4, R6, R8. Cada coluna vira um caso com dado concreto, por exemplo R1+R5: cliente VIP, cupom `DEZ10`, subtotal R$ 150,00 → frete R$ 0,00, desconto R$ 15,00, sem os 5%. Ponha C1 nos limites (198,99 e 199,00) para juntar técnicas. O colapso confia que o código segue a estrutura da regra; com 8 colunas a completa é barata. Combinação impossível vira "N/A", não é apagada. A tabela também acha lacunas de requisito: se o cupom leva R$ 200,00 a R$ 180,00, o frete segue grátis?

## Transição de estados

O defeito típico está nas transições que o sistema permite sem dever (enviar pedido não pago, reembolsar duas vezes). Monte a matriz estado × evento e marque "–" nas inválidas (recusar sem mudar o estado). Ciclo de pedido de exemplo: Criado →(pagar) Pago →(separar) Separado →(enviar) Enviado →(entregar) Entregue →(reembolsar, se arrependimento no prazo) Reembolsado; Criado/Pago/Separado →(cancelar) Cancelado →(reembolsar, se houve pagamento) Reembolsado.

| Critério de cobertura | Exige | Neste exemplo |
| --- | --- | --- |
| Todos os estados | visitar cada um | 7 |
| Transições válidas (0-switch) | cada transição válida | 9 |
| Todas as transições | válidas + tentar cada inválida | 9 + 33 células "–" |
| 1-switch | cada sequência de duas transições | 9 sequências, uma impossível |

Priorize as inválidas que dão prejuízo (pagar pedido já pago, enviar pedido Criado, cancelar Enviado, reembolsar duas vezes, entregar Cancelado) e **teste-as pela API**: a tela esconde o botão, o back-end esquece a regra. Por que 1-switch: a guarda "se houve pagamento" faz Cancelado → Reembolsado depender de **como** chegou a Cancelado; Criado → Cancelado → reembolsar deve ser recusada e o 0-switch não obriga esse teste. Guarda que depende do histórico indica subestados escondidos. Teste também concorrência: cancelar e enviar o mesmo pedido ao mesmo tempo deve terminar em estado coerente.

## Pairwise

Para vários parâmetros independentes com produto cartesiano grande: **todo par de valores** aparece em algum caso. Estudos do NIST com falhas reais indicam que a maioria é disparada por um ou dois parâmetros e praticamente todas por até seis (Inferido, do brain; fonte não relida); n-wise (3-wise) quando o risco justifica, com custo que cresce rápido. Exemplo: navegador (chrome, firefox, safari) × SO (windows, macos) × idioma (pt, en) = 12 combinações; restrição "Safari só no macOS"; 6 linhas cobrem todos os pares possíveis:

| # | Navegador | SO | Idioma |
| --- | --- | --- | --- |
| 1 | chrome | windows | pt |
| 2 | chrome | macos | en |
| 3 | firefox | windows | en |
| 4 | firefox | macos | pt |
| 5 | safari | macos | pt |
| 6 | safari | macos | en |

Restrições vão declaradas ao gerador (no PICT, `IF [so] = "windows" THEN [navegador] <> "safari";`); sem esse suporte, troque o valor proibido à mão e confira se nenhum par sumiu. Pairwise não sabe o que é arriscado: acrescente à mão as combinações de risco conhecido; não use quando os parâmetros interagem por regra de negócio (é tabela de decisão) nem quando o produto cartesiano cabe no tempo.

## Cenários e caixa-branca

**Cenários** verificam se as partes funcionam **juntas** para um objetivo ("cliente novo compra com PIX e acompanha a entrega") e acham defeitos de integração (o cupom some do carrinho depois do login). Cubra o fluxo principal, cada alternativo (pagamento recusado) e cada exceção (timeout do gateway); use personas com história (cartão vencido salvo) e interrompa no meio. São caros: reserve às jornadas de receita ou legais. Em BDD, escreva Gherkin **declarativo** (contexto, ação do usuário, resultado observável; sem seletores nem cliques); a página do Cucumber lida (V-17) descreve Discovery, Formulation e Automation e não traz a sintaxe Given/When/Then (Inferido para a forma). BDD vira custo quando cenários se tornam scripts de UI. Escrever a história é do plugin `product-discovery-specs`.

**Caixa-branca**, exemplo: `aprova = renda_ok and (score_alto or tem_garantia)`.

| Critério | Exige | Casos mínimos aqui |
| --- | --- | --- |
| Instruções | cada linha executada | 2 |
| Decisão / ramo | cada saída de cada decisão | 2 |
| Condição | cada condição atômica V e F | 2, sem garantir a decisão |
| MC/DC | cada condição muda sozinha o resultado | 4 (N + 1) |
| Múltiplas condições | todas as combinações | 8 (2^N) |

Conjunto MC/DC: T1 (renda S, score S, garantia N) aprova; T2 (N, S, N) recusa, prova `renda_ok` com T1; T3 (S, N, N) recusa, prova `score_alto` com T1; T4 (S, N, S) aprova, prova `tem_garantia` com T3. Condição não implica decisão: (S,N,N) e (N,S,S) põem cada condição V e F e a decisão é falsa nos dois. MC/DC é associado a normas de software crítico (DO-178C nível A; ISO 26262 para ASIL D; Inferido, confirme a norma do seu setor); fora disso, aplique à mão em decisões que movem dinheiro ou permissão. Curto-circuito muda o que as ferramentas medem. Cobertura mede execução, não verificação: a força das asserções se mede com mutação (`unitarios-e-integracao.md`).

## Baseadas em experiência

- **Suposição de erro:** liste erros comuns e defeitos que o sistema já teve e provoque-os (divisão por zero, lista vazia, opcional nulo, fuso, duplo envio, cache velho).
- **Ataques de falha:** escolha um modo (entrada enorme, recurso esgotado, dependência fora do ar) e force cada mensagem e estado de erro: "que erro existe no código e eu nunca vi na tela?".
- **Checklists** mantidos pelo time (formulário, upload, endpoint novo): inclua item quando um defeito escapar e corte o que nunca acha nada.

## Teste exploratório

Projetar, executar e aprender ao mesmo tempo, com missão, tempo e registro. **Charter:** *Explore* <alvo> *com* <recursos> *para descobrir* <informação>. Exemplos: "Explore o checkout com cupons expirados, esgotados e de outro cliente para descobrir se algum desconto indevido é aplicado"; "Explore a importação de planilha com arquivos de 0 byte, 50 MB e colunas trocadas para descobrir se linhas se perdem sem aviso". "Explore o sistema" não orienta; charter estreito demais vira roteiro. Template: `assets/templates/charter-exploratorio.md`.

**SBTM:** a unidade é a sessão: um charter, tempo fixo sem interrupção (curta ~60, normal ~90, longa ~120 min), notas com horário. Debrief de 10 a 15 min segue **PROOF**: Passado, Resultados, Obstáculos, Perspectiva (novos charters), Sentimentos. (A fonte de SBTM em PDF não foi lida; Inferido do brain.)

**Tours** (Whittaker): do dinheiro, dos marcos, FedEx (seguir um dado), do lixeiro (todas as telas), do bairro perigoso, do sabotador (cortar rede, disco, dependências), antissocial (o oposto do esperado), obsessivo (repetir a ação), do sedentário (aceitar padrões), da madrugada (deixar aberto por horas).

**SFDPOT** (o que explorar; Bach): Estrutura (config ausente, tabela vazia), Função (cada cálculo, mensagem de erro), Dados (tamanhos, acentos, dados antigos migrados), Interfaces (tela, API, CSV, webhook), Plataforma (navegador, SO, terceiro, versão do banco), Operações (celular com rede ruim, quem cola do Excel), Tempo (fuso, timeout, concorrência, virada de mês).

**FEW HICCUPPS** (como reconhecer problema sem especificação; Bach e Bolton): o produto é inconsistente com: Familiaridade (duplo clique cobra duas vezes), Explicabilidade (total muda ao trocar o CEP e voltar), Mundo (aceita 31/02), História (a versão anterior exportava "João", esta "Jo�o"), Imagem (erro mostra "NullPointerException" ao cliente), Produtos comparáveis (planilha financeira calcula outros juros), Promessas ("entrega em 24 h" e o sistema calcula 3 dias), Expectativa do usuário ("Cancelar" apaga o rascunho), Produto (coerência interna: "CPF" numa tela, "Documento" noutra), Propósito (relatório de fechamento omite o último dia), Padrões e leis (preço cobrado diferente do anunciado; dado pessoal em log).

**Heurísticas rápidas:** CRUD de cada entidade e o efeito nas relacionadas; Goldilocks (grande, pequeno, na medida); zero-um-muitos; seguir o dado ("Ação & Cia D'Ávila" na tela, e-mail, PDF, CSV, busca, relatório); interrupções (sair no meio, perder a rede, sessão expirada, voltar e reenviar).

## Catálogo de dados de borda e hostis

| Categoria | Valores | O que costuma quebrar |
| --- | --- | --- |
| Invisíveis | espaço de largura zero (U+200B), ZWJ (U+200D), BOM (U+FEFF) | "admin" e "admin"+U+200B: dois usuários idênticos na tela |
| Direção | árabe/hebraico; RTL override (U+202E) | layout invertido; "fdp.exe" exibido como "exe.pdf" |
| Emoji com ZWJ | 👨‍👩‍👧‍👦 | 1 caractere visível, 7 pontos de código, 11 unidades UTF-16, 25 bytes UTF-8 |
| Homóglifos | "pаypal" com "а" cirílico (U+0430) | usuário ou domínio que imita outro |
| Normalização | "José" em NFC e em NFD | unicidade e busca falham com o mesmo nome |
| Caixa e locale | "ß" maiúsculo vira "SS"; "İ" em turco | tamanho muda ao converter |
| Tamanho | 1, 255, 256, 65.535, 65.536 caracteres | `VARCHAR(255)`, campos de 16 bits |
| Controle | quebra de linha, tab, byte nulo (U+0000) | PostgreSQL recusa byte nulo em texto; CSV quebra |
| Números | -0, NaN, Infinity, 1e309 | `JSON.stringify(NaN)` vira `null`; 1e309 vira Infinity |
| Decimais | 0,1 + 0,2 = 0,30000000000000004 | moeda em float; -0,001 exibido "-0,00" |
| Bissextos | 2000-02-29 válido; 1900-02-29 e 2100-02-29 inválidos | regra "divisível por 4" sem a exceção de 100/400 |
| Datas especiais | 1970-01-01; 2038-01-19 03:14:07 UTC; 31/12 23:59:59 | época 0 lida como vazio; estouro de 32 bits |
| Fusos | `new Date("2026-03-10")` em JS é lida como UTC | no UTC−3 exibe 09/03 |
| Arquivos | 0 byte; no limite e +1; "foto.jpg" que é PDF; "nota.pdf.exe" | validação pela extensão, não pelo conteúdo |
| Nome de arquivo | `../../etc/passwd`; 256 bytes; `CON` e `NUL` no Windows | path traversal, erro ao salvar |
| Identidade | D'Ávila, O'Connor; nome único; Souza e Silva; sobrenome "Null"; nome social | apóstrofo quebra SQL ou escape; sobrenome obrigatório |
| Brasil | CPF/CNPJ com e sem máscara (CNPJ alfanumérico anunciado para 07/2026: Inferido, confirme), CEP, nono dígito, `R$ 1.234,56`, feriados municipais, fusos, sem horário de verão desde 2019 | máscara, parsing de vírgula/ponto, calendário |

Injeção (`' OR '1'='1`, `<script>`, `{{7*7}}`) vale em todo campo de texto; aprofundamento é do plugin `security-appsec`. Regra de segurança: teste de segurança só em sistema com autorização; para terceiros, ofereça casos de verificação, não exploração pronta. CPF/CNPJ com dígitos válidos só atendem à estrutura: não provam titularidade; use massa sintética.

## Mini-exemplo e critério de parada

Campo "idade", inteiro de 18 a 65:

| Classe / limite | Valores | Esperado |
| --- | --- | --- |
| Válidos (limites) | 18, 65 | aceita |
| Válido (interno) | 40 | aceita |
| Inválidos (fora do limite) | 17, 66 | recusa com mensagem que diz a faixa aceita |
| Inválidos (tipo) | vazio, " ", "abc", 18.5, -1 | recusa sem quebrar a tela |

Formulário completo com 25 casos (CAD-01..25) está em `${CLAUDE_PLUGIN_ROOT}/skills/test-design/references/exemplo-formulario-cadastro.md` (se ausente na instalação, reconstrua com as regras do PO e as técnicas acima).

**Quantos testes bastam** (o critério diz quando a técnica foi aplicada por inteiro, não quando o produto está bom):

| Técnica | Cobertura mínima | Suba o nível quando |
| --- | --- | --- |
| Partição | cada classe válida e inválida (inclusive de saída) | classe de alto risco: mais de um valor |
| Valor-limite | 2 valores por limite | dinheiro, idade legal, prazo: 3 valores |
| Tabela de decisão | cada coluna viável da colapsada | condições críticas: tabela completa |
| Transição de estados | cada transição válida | dinheiro ou guarda por histórico: inválidas + 1-switch |
| Pairwise | 100% dos pares | configuração crítica: 3-wise |
| Caixa-branca | 100% dos ramos | decisão de segurança ou regulada: MC/DC |
| Exploratório | cada charter, com debrief | o debrief gera charters de risco alto |

Pare quando valem juntos: (1) riscos altos com a cobertura acima e o que ficou de fora escrito com o risco que sobra; (2) testes novos pararam de trazer informação nova; (3) nenhum defeito crítico aberto sem decisão explícita de quem responde pelo produto. Se o prazo acabar antes, o critério vira transparência: o que foi testado, o que não foi e o que você testaria com mais um dia.
