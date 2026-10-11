# Matriz de casos de teste de pagamentos

Sumário: 1. Como usar · 2. Pagamentos e fintech (núcleo) · 3. Webhook e filas · 4. Pix · 5. Boleto · 6. Cartão, 3DS e PAN em log · 7. Vetores de arredondamento · 8. BR Code · 9. Documentos, datas, moeda e fusos · 10. Cobrança em SaaS e checkout

## 1. Como usar

Cada linha é um caso mínimo. Preencha dado, esperado, oráculo e fonte do número (`plano-testes-pagamentos.md`). Rótulos: **V** = item de VALIDATED lido na fonte; **Herdado** = brain-of-agent (V-33, **Inferido/herdado**, Não verificado contra norma); **Seed** = número regulatório a confirmar no regulamento vigente, nunca oráculo de aceitação.

Atribuição: as tabelas das seções 2, 4, 5, 6 (parte), 9 e 10 adaptam o conteúdo de `brains/qa/references/dominios.md` do repositório `francisco-efjr/brain-of-agent` (MIT, Copyright (c) 2026 Brain of Agent contributors), com a coluna "oráculo" e as fontes V acrescentadas pelo plugin. Regras e números regulatórios mudam; os herdados foram conferidos em 2026 pelo brain e não foram reconferidos contra a norma aqui.

## 2. Pagamentos e fintech (núcleo)

| Risco | Caso que não pode faltar | Esperado | Oráculo independente | Fonte |
| --- | --- | --- | --- | --- |
| Cobrança dupla | duplo clique em "Pagar"; mesma requisição com a mesma chave; timeout do gateway seguido de retry | uma cobrança só; a segunda chamada devolve o resultado da primeira | `SELECT count(*)` na tabela de cobranças e contagem de chamadas ao stub do provedor | V-01, Herdado |
| Chave mal escopada | mesma chave com corpo diferente (R$ 100,00 e depois R$ 150,00) | recusa explícita (conflito); nunca reaproveita em silêncio | linhas = 1 e nada chamado na segunda | V-01, V-58 |
| Arredondamento | R$ 100,00 em 3 parcelas; R$ 10,00 de desconto rateado entre 3 itens | 33,34 + 33,33 + 33,33 (ou a regra escrita); soma exatamente igual ao total | soma por consulta separada ou planilha | V-10, Herdado |
| Ponto flutuante | `0.1 + 0.2` em cálculo de valor | centavos inteiros ou decimal exato; nunca `float` | tipo da coluna e do DTO; teste do `Money` | V-10 (Inferido), Herdado |
| Regra de arredondamento | juros de 1% a.m. sobre R$ 333,33 por 17 dias | resultado conferido por planilha independente com a regra escrita (meio para cima × meio para o par) | planilha com a mesma regra | Herdado |
| Conciliação | pedido pago no sistema × liquidação no extrato | cada transação casa por ID; divergência gera alerta, não ajuste manual silencioso | extrato fornecido; relatório bilateral | V-08, Herdado |
| Fonte incompleta | extrato com menos linhas que o total de controle | `INCOMPLETE_SOURCE`; não declara conciliado | contagem versus total de controle | V-08 |
| Estorno | total, parcial, dois parciais somando mais que o original | parcial reduz o saldo estornável; soma acima do original é recusada | `original − soma(estornos)` calculado à parte | V-11, Herdado |
| Chargeback | contestação depois do repasse ao lojista | débito registrado, pedido marcado, disputa com prazo visível | lançamento de débito no ledger; prazo conferido na doc do provedor | V-09, Herdado |
| Limites | limite diário R$ 5.000,00: transferir 4.999,99 + 0,01; depois mais 0,01 | aceita até 5.000,00 exatos; recusa 5.000,01 com mensagem que diz o limite | soma das transações aceitas no dia | Herdado |
| Virada do limite | transação às 23:59:59 e às 00:00:00 no fuso do cliente | o contador zera no fuso definido pela regra (em geral `America/Sao_Paulo`), não em UTC | data local calculada com a base IANA | Herdado |
| Antifraude | 10 tentativas em 1 minuto com cartões diferentes no mesmo dispositivo | bloqueio ou desafio; cliente legítimo tem caminho de recuperação | contadores e log de decisão | V-40 (mapa), Herdado |
| Concorrência de saldo | dois débitos simultâneos de R$ 80,00 em conta com R$ 100,00 | um aprova, o outro recusa; saldo nunca negativo | saldo reconstruído do histórico, duas conexões reais | V-11, Herdado |
| Ledger imutável | tentativa de `UPDATE`/`DELETE` em lançamento | bloqueada | erro do banco; linhas intactas | V-46 |
| Transação desbalanceada | lançamentos que não somam zero por moeda | recusada, nada gravado | contagem de linhas inalterada | V-11 (Inferido) |
| Moedas misturadas | somar BRL com USD sem câmbio | erro explícito | exceção tipada | V-10 |

Armadilhas: testar o retry sem verificar o efeito no banco (conte as linhas, não a resposta); usar `float` no próprio teste e "acertar" o erro do sistema; esquecer que o webhook do gateway também chega duplicado e fora de ordem (`pagamento.aprovado` antes de `pagamento.criado`).

## 3. Webhook e filas

| Caso | Esperado | Fonte |
| --- | --- | --- |
| Assinatura válida | aceito; uma linha na inbox; um efeito | V-03, V-05 |
| Assinatura forjada, ou corpo alterado em um byte | 4xx; zero efeito | V-03, V-06 |
| Mesmo evento duas vezes (e concorrente) | um efeito | V-03 |
| Mesmo ID, conteúdo diferente | quarentena (não é duplicata) | V-05 |
| Fora de ordem (estorno antes da captura; falha antes da criação) | converge para o estado real relido; nada regride | V-03, Herdado |
| Crash após o efeito, antes de marcar processado | reprocessa sem duplicar efeito | V-05 |
| Evento envenenado | DLQ com motivo; a fila continua | V-05, Herdado |
| Replay fora da tolerância | 4xx; zero efeito | V-03 |
| Rotação de segredo | aceita a chave anterior só na janela | V-03, V-47 |
| Entrega pelo menos uma vez | publicar a mesma mensagem duas vezes aplica o efeito uma vez | Herdado |
| Timeouts em cascata | timeout de quem chama maior que o de quem é chamado somado aos retries, senão o retry duplica | Herdado |
| Outbox | banco grava, broker cai antes de publicar: evento sai depois; nunca grava sem publicar nem publica sem gravar | Herdado |
| Consistência eventual | asserção com polling até um prazo (por exemplo 10 s a cada 200 ms), nunca `sleep` fixo | Herdado |

Roteiro executável: `webhook-handler/references/roteiro-testes-hostis.md`. Chaos engineering (Toxiproxy, Chaos Mesh) só em teste, com hipótese escrita, raio de impacto pequeno e condição de aborto; em produção, só com autorização explícita.

## 4. Pix (V-43, V-44, V-48, V-65; números marcados Seed são Não verificados)

| Tema | O que testar | Dados e esperado | Rótulo |
| --- | --- | --- | --- |
| `txid` da cobrança | 25, 26, 35 e 36 caracteres; reuso após cancelamento | 26 a 35 alfanuméricos aceitos; 25 e 36 recusados; reuso recusado | V |
| Valor | `0.00`, `10.0`, `10.001`, `10.00` | só o último é válido para cobrança comum; zero é erro (exceto Pix Saque) | V |
| Conversão na borda | `10.00` ↔ 1000 centavos ↔ `10.00` | ida e volta sem perda; sem float | V + Inferido |
| Devolução | total, parcial, várias parciais, repetida com o mesmo `id`, após a janela | soma ≤ original; `id` repetido recusado; fora da janela recusado (90 dias na spec 2.10.0: conferir) | V |
| Timeout na criação | resposta não chega | consultar por `txid` antes de reenviar | V-48 (Inferido) |
| Timeout no pagamento | resposta não chega em 30 s | consultar o status pelo `EndToEndId` antes de reenviar; reenviar às cegas gera Pix em dobro | Herdado (30 s: Seed) |
| Webhook duplicado | mesmo `endToEndId` duas vezes | um crédito; releitura antes de creditar | V-54 (Inferido) |
| QR estático | mesmo QR pago duas vezes; QR sem valor | estático aceita vários pagamentos; sem valor o pagador digita | Herdado |
| QR dinâmico | pagar depois da expiração; pagar duas vezes | expirado recusado; unicidade é do `txid` da cobrança | V-65, Herdado |
| Cobrança com vencimento | pagar antes, no dia e depois; vencimento em feriado municipal | juros, multa e desconto calculados para a data de pagamento prevista | V-44 (Anexo III), Herdado |
| CNPJ alfanumérico | chave Pix de empresa `12ABC34501DE35` | aceita; parser só de dígitos é defeito | V-43 (schema), data: Herdado |
| Limite noturno | Pix de R$ 1.000,01 às 20h01 | comportamento deve vir de configuração; padrão R$ 1.000,00 entre 20h e 6h | Seed |
| Dispositivo novo | primeiro Pix em celular não cadastrado | limite por transação e por dia vem de configuração (R$ 200 e R$ 1.000 herdados) | Seed |
| Pix Automático | autorização, agendamento, cancelamento, saldo insuficiente | exige autorização prévia; agendamento 2 a 10 dias antes (herdado) | Seed; nenhum número como regra |
| MED | pagador contesta por golpe | dois prazos separados com `prazo_fonte` e `status`; 80 dias é Não verificável | V-64 |
| `EndToEndId` | parse de `E` + ISPB(8) + `AAAAMMDDHHmm` UTC + 11 | hora em UTC, não em Brasília; usar como chave de conciliação | Seed (só os 32 caracteres são V) |

Casos hostis: QR adulterado (CRC inválido), QR de outro recebedor colado na tela de checkout, valor alterado entre a leitura e a confirmação, app fechado no meio do pagamento e reaberto.

## 5. Boleto (Não verificados contra norma; ver `pix-boleto-br/references/boleto-checklist.md`)

Formatos (44 posições e linha digitável de 47 ou 48 dígitos); dígitos verificadores (módulo 10 por campo, módulo 11 geral); fator de vencimento com o reinício de 2025 (21/02/2025 fator 9999, 22/02/2025 fator 1000) e ambiguidade do fator 1000 (resolver para o ciclo mais próximo da data atual, nunca para 2000); valor (R$ 0,01 e R$ 99.999.999,99; sem valor pede digitação); vencimento em dia não útil (paga no próximo dia útil sem multa); linha digitável guardada como texto (zeros à esquerda); desconto com `limit_date` anterior ao `due_at` (V-36); boleto vencido há mais de 60 dias inacessível (Pagar.me, V-36).

## 6. Cartão, 3DS e PAN em log

| Caso | Esperado | Rótulo |
| --- | --- | --- |
| Luhn: número com dígito trocado (por exemplo `4242 4242 4242 4241`) | recusado no cliente, sem chamada ao gateway | Herdado |
| Cartões de teste do gateway | cada motivo de recusa tem mensagem própria; "erro desconhecido" para saldo insuficiente é defeito de UX | Herdado; use os cartões **do provedor em uso** |
| 3DS sem fricção, desafio aprovado, recusado, abandonado, timeout | pedido não fica "pago" sem autenticação concluída, nem preso para sempre em "aguardando" | Herdado, V-39 |
| 3DS: estados e dados | guarda resultado, ECI e fluxo por tentativa | V-49 |
| Texto de produto | nenhuma tela ou resposta promete transferência de responsabilidade | V-39, V-49 |
| Parcelamento | parcela mínima, loja × emissor, soma das parcelas = total, troca de parcelas após cupom, estorno parcelado | Herdado |
| Cartão salvo | expirado, removido, token de outro usuário (IDOR) | Herdado |
| PAN em log | nenhum número de cartão em log, URL, analytics ou print de erro | V-23, Herdado |

Detector de PAN em log (Python 3, stdlib; executado em 2026-10-10 sobre linhas sintéticas). Resultado observado: `card=4242 4242 4242 4242` detectado como `424242******4242`; `4242 4242 4242 4241` não detectado (falha no Luhn); `pedido 20261011123456` detectado por acaso (um ID numérico de 14 dígitos passou no Luhn, o que acontece em cerca de 1 em 10 sequências aleatórias): **trate cada achado como candidato e confira o contexto**; nunca grave o PAN inteiro no relatório.

```python
import re
CANDIDATO = re.compile(r"(?<!\d)(?:\d[ -]?){13,19}(?!\d)")

def luhn_ok(digitos: str) -> bool:
    soma, dobrar = 0, False
    for c in reversed(digitos):
        d = int(c)
        if dobrar:
            d *= 2
            if d > 9: d -= 9
        soma += d
        dobrar = not dobrar
    return soma % 10 == 0

def achar_pans(texto: str):
    achados = []
    for m in CANDIDATO.finditer(texto):
        d = re.sub(r"[ -]", "", m.group())
        if 13 <= len(d) <= 19 and luhn_ok(d):
            achados.append(d[:6] + "*" * (len(d) - 10) + d[-4:])   # mascarado
    return achados
```

PCI: o que vira caso de teste é nunca PAN completo em log, URL, analytics ou print de erro; exibição mascarada (no máximo BIN e quatro últimos); CVV nunca armazenado depois da autorização; ambiente de teste sem cartão real. Requisitos numerados do PCI DSS **não foram lidos**: não cite 6.4.3 ou 11.6.1 como fato (V-29, V-62).

## 7. Vetores de arredondamento (V-61; executados em Python 3.14.4; oráculo só para a política do projeto)

| Entrada | Casas | Modo | Esperado |
| --- | --- | --- | --- |
| `0.125` | 2 | HALF_EVEN | `0.12` |
| `0.125` | 2 | HALF_UP | `0.13` |
| `2.345` | 2 | HALF_UP | `2.35` |
| `2.345` | 2 | HALF_EVEN | `2.34` |
| `2.355` | 2 | HALF_EVEN | `2.36` |
| `2.355` | 2 | HALF_UP | `2.36` |
| `7.325` | 2 | ROUND_DOWN | `7.32` |
| `7.325` | 0 (`quantize(Decimal('1.'))`) | ROUND_UP | `8` |

Todas as entradas são strings (`Decimal('0.125')`). `Decimal('0.1') == Decimal(0.1)` dá `False` (construir de float). Rateio de 100,00 em 3 partes: 33,34 + 33,33 + 33,33. Vetores de Java (`setScale` e `RoundingMode.UNNECESSARY`) não foram executados. Reexecute os vetores no interpretador do projeto antes de promovê-los a oráculo.

## 8. BR Code (V-65; vetor sintético, ver `pix-boleto-br/references/pix-referencias.md`)

| Caso | Esperado |
| --- | --- |
| Payload estático do Manual (seção 2.6.3, CRC `1D3D`), obtido pelo usuário do PDF do BCB | CRC válido (vetor positivo oficial) |
| Payload sintético da referência (CRC `6BFD`) | válido |
| Mesmo payload com um caractere alterado (por exemplo `10.00` para `10.01`) mantendo o CRC | inválido; CRC calculado `D699` |
| QR dinâmico com valor e `txid` preenchidos | ignorados; vale o payload da URL |
| Mesmo QR dinâmico exibido duas vezes | dois pagamentos possíveis; unicidade é do `txid` |
| Copia e cola com chave de outro recebedor | CRC válido não prova a identidade; conferir chave e nome no DICT ou na API do PSP (Inferido) |

## 9. Documentos, datas, moeda e fusos (Herdados)

Gere e valide massa com `scripts/documentos_br.py` (autoteste: `--self-test`). Documento com DV correto pode pertencer a alguém real: só em teste.

| Documento | Regra | Casos que pegam defeito |
| --- | --- | --- |
| CPF | 11 dígitos; 2 DVs por módulo 11 | com e sem máscara; `529.982.247-25` válido; DV trocado; `111.111.111-11` (passa no cálculo, é inválido); zero à esquerda guardado como número |
| CNPJ numérico | 14 dígitos: raiz (8) + ordem (4) + 2 DVs | `11.222.333/0001-81` válido; filial com a mesma raiz; zeros à esquerda |
| CNPJ alfanumérico | 12 primeiras posições A-Z e 0-9; DVs numéricos; valor do caractere = ASCII − 48 (A = 17); pesos 5,4,3,2,9,8,7,6,5,4,3,2 e 6,5,4,3,2,9,8,7,6,5,4,3,2; resto < 2 vira 0 | `12.ABC.345/01DE-35` válido (validado pelo script em 2026-10-10); minúsculas (normaliza ou recusa, a regra decide); coluna `BIGINT`, máscara numérica e teclado numérico quebram. Data de julho de 2026: Herdado |

Datas e moeda: `DD/MM/AAAA` na tela e ISO `AAAA-MM-DD` na API; use dia ≤ 12 nos testes (`01/02/2026`) para pegar troca dia/mês; `R$ 1.234,56` com vírgula decimal; entrada `1.000` em campo pt-BR é mil. Feriados: nacionais fixos e móveis; Carnaval e Corpus Christi são ponto facultativo federal; estaduais e municipais variam (São Paulo 25/1, Rio de Janeiro 20/1); trate calendário como dado configurável. Fusos: quatro (UTC−2 a UTC−5), sem horário de verão desde 2019; use identificadores IANA e mantenha a base de fusos (tzdata) atualizada; teste usuário em Manaus (UTC−4) com servidor em São Paulo; em Windows o Python pode não ter tzdata e falha com `ZoneInfoNotFoundError`.

## 10. Cobrança em SaaS e checkout (linhas que tocam pagamento)

| Área | Caso | Esperado |
| --- | --- | --- |
| Cobrança recorrente | upgrade no meio do ciclo; falha de cartão; webhook duplicado | proporcional conferido por cálculo independente; retentativa conforme regra; um efeito por evento |
| Checkout | abandonar no pagamento e voltar; pagamento recusado | carrinho preservado; nova tentativa não duplica pedido |
| Pix expirado | Pix gerado e não pago até expirar | reserva de estoque liberada no fim do prazo |

Recorrência, planos e proration são do plugin `saas-multitenant`; checkout e estoque, de `ecommerce-marketplace`. Aqui só a mecânica financeira (idempotência, webhook, estorno).
