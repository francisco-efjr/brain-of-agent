# Catálogo de dados de borda e hostis

Apoio da skill `test-design`. Consulte ao montar casos para campos de texto, números, datas, arquivos e documentos. Use só as linhas que o campo realmente recebe: despejar o catálogo inteiro vira ruído.

Origem e rótulos: adaptado do brain-of-agent (conteúdo próprio do usuário, MIT), com redação revisada. Valores como 2^31 - 1 e as contagens de emoji foram recalculados ao preparar este arquivo (Verificado por cálculo). Números de produtos e versões (limites de nginx, Express, MySQL), fatos de calendário e documentos brasileiros são Inferido: não reverificados em fonte externa, confirme no seu stack e na norma vigente.

## Sumário

- [Como escolher linhas do catálogo](#como-escolher-linhas-do-catálogo)
- [Limites ocultos de infraestrutura](#limites-ocultos-de-infraestrutura)
- [Dados hostis e de borda](#dados-hostis-e-de-borda)
- [Brasil](#brasil)
- [Injeção em campos de texto](#injeção-em-campos-de-texto)

## Como escolher linhas do catálogo

| O campo é... | Linhas a considerar |
| --- | --- |
| nome, endereço, texto livre | invisíveis, direção, emoji, normalização, combinação, tamanho, controle, identidade |
| número, quantidade, moeda | números, inteiros, decimais, limites ocultos (int32, 2^53) |
| data, prazo, validade | bissextos, datas especiais, fusos, horário de verão histórico |
| upload | arquivos, nome de arquivo, corpo máximo no proxy |
| identificador de negócio (CPF, CNPJ, CEP, telefone) | seção Brasil |
| qualquer texto que chega ao banco, HTML ou shell | injeção |

Para cada linha escolhida, o caso precisa de esperado: aceita e grava igual? recusa com mensagem? normaliza? Se a regra não diz, é pergunta ao PO.

## Limites ocultos de infraestrutura

Ninguém escreveu, mas o sistema tem. Procure no esquema do banco, na infraestrutura e no código.

| Limite oculto | Valor conhecido | Teste |
| --- | --- | --- |
| Inteiro de 32 bits com sinal | 2.147.483.647 | quantidade, ID ou centavos no máximo e +1; em centavos, int32 trava em R$ 21.474.836,47 |
| Inteiro seguro em JavaScript | 2^53 - 1 = 9.007.199.254.740.991 | ID int64 lido por JS perde precisão: 9007199254740993 vira ...992 |
| Coluna menor que a validação da tela | tela aceita 100, coluna `VARCHAR(80)` | 100 caracteres: erro 500 ou truncamento silencioso |
| Charset do banco | `utf8` do MySQL (utf8mb3) não guarda emoji de 4 bytes | gravar um emoji e reler |
| Corpo da requisição no proxy | nginx: `client_max_body_size` padrão 1 MB | upload logo acima: 413 |
| Corpo JSON no framework | Express: `express.json()` padrão 100 kb | payload de 101 kb |
| Gateway, balanceador, CDN | teto de payload e timeout próprios | requisição lenta logo acima do timeout (confira a documentação do provedor) |
| Nome de arquivo | 255 bytes na maioria dos sistemas de arquivos | nome com 256 bytes, com acentos |
| Tempo Unix em 32 bits | 2038-01-19 03:14:07 UTC | vencimentos depois de 2038 |

## Dados hostis e de borda

| Categoria | Valores | O que costuma quebrar |
| --- | --- | --- |
| Invisíveis | espaço de largura zero (U+200B), ZWJ (U+200D), BOM (U+FEFF) | "admin" e "admin" + U+200B: dois usuários idênticos na tela |
| Direção | texto árabe ou hebraico; RTL override (U+202E) | layout invertido; "fdp.exe" exibido como "exe.pdf" |
| Emoji com ZWJ | família 👨‍👩‍👧‍👦 | 1 caractere visível, 7 pontos de código, 11 unidades UTF-16, 25 bytes UTF-8 (conferido): limites e cortes divergem |
| Homóglifos | "pаypal" com "а" cirílico (U+0430) | usuário ou domínio que imita outro |
| Combinação (Zalgo) | letras com dezenas de diacríticos empilhados | layout transbordado, contagem de tamanho |
| Normalização | "José" em NFC e em NFD | unicidade e busca falham com o mesmo nome |
| Caixa e locale | "ß" maiúsculo vira "SS"; "İ" minúsculo vira 2 pontos de código (conferido) | tamanho muda ao converter; comparação em turco |
| Tamanho | 1, 255, 256, 65.535, 65.536 caracteres | limites de `VARCHAR(255)` e de campos de 16 bits |
| Controle | quebra de linha, tab, byte nulo (U+0000) | PostgreSQL recusa byte nulo em texto; CSV quebra |
| Números | -0, NaN, Infinity, 1e309 | `JSON.stringify(NaN)` vira `null`; Python grava `NaN` (JSON inválido); 1e309 vira Infinity |
| Decimais | 0,1 + 0,2 = 0,30000000000000004 (conferido) | moeda em float; -0,001 arredondado exibido "-0,00" |
| Bissextos | 2000-02-29 válido; 1900-02-29 e 2100-02-29 inválidos | regra "divisível por 4" sem a exceção de 100/400; o Excel aceita 29/02/1900 |
| Datas especiais | 1970-01-01; 2038-01-19; 31/12 23:59:59 | época 0 lida como "vazio"; estouro de 32 bits; virada de ano |
| Fusos | data sem hora em JS (`new Date("2026-03-10")`) é lida como UTC | no Brasil (UTC-3) exibe 09/03 |
| Horário de verão histórico | 04/11/2018 00:00 não existiu em São Paulo | nascimento salvo como 03/11 |
| Arquivos | 0 byte; exatamente no limite e +1 byte; "foto.jpg" que é PDF; "nota.pdf.exe" | validação pela extensão, não pelo conteúdo |
| Nome de arquivo | `../../etc/passwd`; 256 bytes; `CON` e `NUL` no Windows | path traversal, erro ao salvar |
| Identidade | D'Ávila, O'Connor; nome único (estrangeiros); Souza e Silva, Mello-Franco; Filho, Neto; sobrenome "Null"; nome social | apóstrofo quebra SQL ou escape; sobrenome obrigatório; corte do composto |

Contagem de tamanho: antes de testar limite de texto, descubra o que a regra conta (caracteres visíveis, pontos de código, unidades UTF-16 como `length` do JavaScript, bytes) e se espaços nas pontas entram na conta.

## Brasil

| Dado | Casos | Observação |
| --- | --- | --- |
| CPF | com e sem máscara; dígito verificador errado; dígitos repetidos | `111.111.111-11` passa no cálculo dos dígitos e é inválido pela regra de negócio, então precisa de caso próprio (conferido). Use CPF sintético de teste; `529.982.247-25` fecha o cálculo (conferido) e `529.982.247-24` não |
| CNPJ | com e sem máscara; dígito errado; formato alfanumérico | o formato alfanumérico (emitido a partir de julho de 2026, segundo o brain) é afirmação não reverificada: Não verificável, confirme com a Receita Federal |
| CEP | com e sem hífen; inexistente; de área remota | frete e prazo mudam por região |
| Telefone | com e sem nono dígito; com DDI | máscara e normalização |
| Moeda | `R$ 1.234,56` (vírgula decimal, ponto de milhar); parcela que fecha o total (R$ 100,00 em 3x: 33,33 + 33,33 + 33,34) | regra de arredondamento (metade para cima ou bancário) não escrita é pergunta ao PO |
| Calendário | feriados nacionais e municipais; viradas de mês | oráculo é o calendário da filial, não o do desenvolvedor |
| Fusos | quatro fusos no território; sem horário de verão desde 2019 (Inferido) | dado histórico anterior a 2019 ainda segue o horário de verão da época |
| Nomes | acentos, apóstrofo, hífen, nome composto, nome social | corte indevido do sobrenome |

## Injeção em campos de texto

`' OR '1'='1`, `<script>alert(1)</script>`, `{{7*7}}` valem em todo campo de texto como casos de **verificação** (a resposta deve ser recusa, escape ou texto inerte). Isso é detecção de falha em sistema autorizado, não exploração: execute só contra ambiente de teste do próprio produto e encaminhe achados ao segmento de segurança. Não use payloads contra sistemas de terceiros.
