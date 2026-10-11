Montei 46 casos de teste por partição de equivalência e valor-limite sobre os eixos da regra: valor mínimo, limite diurno, limite noturno e saldo. Acrescentei fronteiras de horário, transição entre as janelas e concorrência, que costumam esconder os bugs de limite.

O arquivo para importar é o `casos-pix-limites-xray.csv` (UTF-8, vírgula como separador, uma linha por caso). Abaixo está o mesmo conteúdo em formato legível, para você revisar antes de importar.

## Premissas que usei

A regra não fecha estes pontos, então assumi o que segue. Os casos marcados com **[CONFIRMAR]** (10 de 46) dependem de uma dessas premissas.

1. **Limites inclusivos.** R$ 5.000,00 e R$ 1.000,00 passam; R$ 0,01 acima, não. Valor mínimo R$ 0,01 é aceito. Saldo igual ao valor é aceito.
2. **Janelas.** Diurna vai de 06:00:00 a 19:59:59 e noturna de 20:00:00 a 05:59:59. Quem decide o horário é o servidor (Brasília), no momento da confirmação.
3. **Limite acumulado.** O limite soma todos os PIX efetivados do cliente (qualquer destinatário), e cada janela tem o seu próprio saldo de limite. A noturna é um único período, mesmo cruzando a meia-noite.
4. **Saldo** é o saldo disponível, sem cheque especial. Transferência negada não debita nem consome limite.

## Casos

Saldo é o saldo no momento da tentativa e já desconta o que foi enviado antes. Em todos os casos a ação é a mesma: informar a chave do destinatário, informar o valor e confirmar. Os casos com mais de uma tentativa trazem os passos no CSV.

| ID | Cenário | Saldo (R$) | Já enviado no período (R$) | Horário | Valor (R$) | Resultado esperado | Prio |
|---|---|---|---|---|---|---|---|
| PIX-VAL-01 | Valor mínimo (R$ 0,01) é aceito | 20.000,00 | — | 10:00 | 0,01 | Aprovada. Débito de R$ 0,01 (saldo final 19.999,99) e comprovante gerado. | High |
| PIX-VAL-02 | Valor logo acima do mínimo (R$ 0,02) é aceito | 20.000,00 | — | 10:00 | 0,02 | Aprovada. Débito de R$ 0,02 (saldo final 19.999,98). | Medium |
| PIX-VAL-03 | Valor zero é rejeitado | 20.000,00 | — | 10:00 | 0,00 | Rejeitada na validação (valor mínimo R$ 0,01). Nenhuma transação criada; saldo inalterado em 20.000,00. | High |
| PIX-VAL-04 | Valor negativo é rejeitado | 20.000,00 | — | 10:00 | -0,01 | Rejeitada (app: campo não aceita o sinal; API: erro de validação). Nenhuma transação criada; saldo inalterado. | Medium |
| PIX-VAL-05 | **[CONFIRMAR]** Valor com mais de 2 casas decimais | 20.000,00 | — | 10:00 | 10,005 | Não aceita a 3ª casa (máscara bloqueia ou API devolve erro). Nunca debita valor arredondado ou truncado sem o cliente ver. | Medium |
| PIX-VAL-06 | Valor vazio ou não numérico | 20.000,00 | — | 10:00 | (vazio) e "abc" | Confirmar fica desabilitado ou há erro de validação de campo. Nenhuma transação criada. | Low |
| PIX-DIA-01 | Um centavo abaixo do limite diurno | 20.000,00 | — | 10:00 | 4.999,99 | Aprovada. Saldo final 15.000,01. | High |
| PIX-DIA-02 | Valor igual ao limite diurno | 20.000,00 | — | 10:00 | 5.000,00 | Aprovada. Saldo final 15.000,00. | High |
| PIX-DIA-03 | Um centavo acima do limite diurno | 20.000,00 | — | 10:00 | 5.000,01 | Negada por limite diário excedido (mensagem de limite, não de saldo). Sem débito; saldo 20.000,00; nenhuma transação efetivada. | High |
| PIX-DIA-04 | Acumulado do período diurno chega exatamente ao limite | 17.000,00 | 3.000,00 | 10:00 | 2.000,00 | Aprovada. Total do período = 5.000,00; saldo final 15.000,00. | High |
| PIX-DIA-05 | Acumulado do período diurno passa do limite em R$ 0,01 | 17.000,00 | 3.000,00 | 10:00 | 2.000,01 | Negada por limite (total seria 5.000,01). Sem débito; saldo 17.000,00. | High |
| PIX-DIA-06 | Limite diurno esgotado bloqueia até o valor mínimo | 15.000,00 | 5.000,00 | 10:00 | 0,01 | Negada por limite diário esgotado. Sem débito; saldo 15.000,00. | High |
| PIX-DIA-07 | Limite acumula entre destinatários diferentes | 17.000,00 | 3.000,00 (para o Cliente B) | 10:00 | 2.000,01 (para o Cliente C) | Negada por limite: o limite é do cliente pagador, não do par pagador/recebedor. Sem débito. | Medium |
| PIX-DIA-08 | Tentativa negada não consome limite | 16.000,00 | 4.000,00 | 10:00 | 1.500,00 e, em seguida, 1.000,00 | 1ª negada por limite (total seria 5.500,00), sem débito. 2ª aprovada (total 5.000,00); saldo final 15.000,00. | Medium |
| PIX-DIA-09 | Limite diurno renova no dia seguinte | 15.000,00 | 5.000,00 no dia anterior (15:00) | 10:00 do dia seguinte | 5.000,00 | Aprovada (novo dia, limite cheio). Saldo final 10.000,00. | Medium |
| PIX-NOT-01 | Um centavo abaixo do limite noturno | 20.000,00 | — | 22:00 | 999,99 | Aprovada. Saldo final 19.000,01. | High |
| PIX-NOT-02 | Valor igual ao limite noturno | 20.000,00 | — | 22:00 | 1.000,00 | Aprovada. Saldo final 19.000,00. | High |
| PIX-NOT-03 | Um centavo acima do limite noturno | 20.000,00 | — | 22:00 | 1.000,01 | Negada por limite noturno excedido. Sem débito; saldo 20.000,00. | High |
| PIX-NOT-04 | Limite diurno (R$ 5.000,00) não vale à noite | 20.000,00 | — | 22:00 | 5.000,00 | Negada por limite noturno. Sem débito; saldo 20.000,00. | High |
| PIX-NOT-05 | Madrugada: valor igual ao limite noturno | 20.000,00 | — | 03:00 | 1.000,00 | Aprovada. Saldo final 19.000,00. | High |
| PIX-NOT-06 | Madrugada: um centavo acima do limite noturno | 20.000,00 | — | 03:00 | 1.000,01 | Negada por limite noturno excedido. Sem débito; saldo 20.000,00. | High |
| PIX-NOT-07 | Acumulado noturno chega exatamente ao limite | 19.400,00 | 600,00 (às 21:00) | 23:30 | 400,00 | Aprovada. Total do período noturno = 1.000,00; saldo final 19.000,00. | Medium |
| PIX-NOT-08 | Acumulado noturno passa do limite em R$ 0,01 | 19.400,00 | 600,00 (às 21:00) | 23:30 | 400,01 | Negada por limite noturno (total seria 1.000,01). Sem débito; saldo 19.400,00. | High |
| PIX-NOT-09 | **[CONFIRMAR]** Acumulado noturno atravessa a meia-noite | 19.300,00 | 700,00 (às 23:50 do dia D) | 00:10 do dia D+1 e 01:00 do dia D+1 | 300,00 e, em seguida, 0,01 | 300,00 aprovada (total 1.000,00 no mesmo período noturno). 0,01 negada por limite noturno. Saldo final 19.000,00. | Medium |
| PIX-HOR-01 | 05:59:59 aplica o limite noturno | 20.000,00 | — | 05:59:59 | 1.500,00 | Negada por limite noturno (1.500,00 > 1.000,00). Sem débito. | High |
| PIX-HOR-02 | **[CONFIRMAR]** 06:00:00 aplica o limite diurno | 20.000,00 | — | 06:00:00 | 1.500,00 | Aprovada (limite diurno). Saldo final 18.500,00. | High |
| PIX-HOR-03 | 06:00:01 aplica o limite diurno | 20.000,00 | — | 06:00:01 | 1.500,00 | Aprovada. Saldo final 18.500,00. | Medium |
| PIX-HOR-04 | 19:59:59 aplica o limite diurno | 20.000,00 | — | 19:59:59 | 1.500,00 | Aprovada. Saldo final 18.500,00. | High |
| PIX-HOR-05 | **[CONFIRMAR]** 20:00:00 aplica o limite noturno | 20.000,00 | — | 20:00:00 | 1.500,00 | Negada por limite noturno. Sem débito. | High |
| PIX-HOR-06 | 20:00:01 aplica o limite noturno | 20.000,00 | — | 20:00:01 | 1.500,00 | Negada por limite noturno. Sem débito. | Medium |
| PIX-HOR-07 | Virada de data (00:00:00) mantém o limite noturno | 20.000,00 | — | 00:00:00 | 1.500,00 | Negada por limite noturno. Sem débito. | Medium |
| PIX-HOR-08 | **[CONFIRMAR]** Fluxo iniciado no diurno e confirmado no noturno | 20.000,00 | — | abre a tela 19:59:30; confirma 20:00:10 | 1.500,00 | Negada por limite noturno: a regra vale na hora da confirmação, não da abertura da tela. Sem débito. | Medium |
| PIX-HOR-09 | **[CONFIRMAR]** Relógio do aparelho diferente do horário oficial | 20.000,00 | — | servidor 22:00; aparelho ajustado para 10:00 | 1.500,00 | Negada por limite noturno: vale o horário do servidor (Brasília), não o do aparelho. Sem débito. | Medium |
| PIX-JAN-01 | **[CONFIRMAR]** Limite diurno esgotado não bloqueia o noturno | 15.000,00 | 5.000,00 (às 15:00) | 21:00 | 1.000,00 | Aprovada (o limite noturno tem saldo próprio). Saldo final 14.000,00. | High |
| PIX-JAN-02 | **[CONFIRMAR]** Limite noturno independe do uso diurno parcial | 17.000,00 | 3.000,00 (às 15:00) | 21:00 e 21:05 | 1.000,00 e, em seguida, 0,01 | 1.000,00 aprovada. 0,01 negada (limite noturno esgotado). Saldo final 16.000,00. | Medium |
| PIX-JAN-03 | **[CONFIRMAR]** Uso na madrugada não consome o limite diurno do mesmo dia | 19.000,00 | 1.000,00 (às 02:00; limite noturno esgotado) | 10:00 do mesmo dia | 5.000,00 | Aprovada (limite diurno cheio). Saldo final 14.000,00. | Medium |
| PIX-SAL-01 | Saldo exatamente igual ao valor | 100,00 | — | 10:00 | 100,00 | Aprovada. Saldo final 0,00. | High |
| PIX-SAL-02 | Saldo um centavo abaixo do valor | 99,99 | — | 10:00 | 100,00 | Negada por saldo insuficiente. Sem débito; saldo 99,99; nenhuma transação efetivada. | High |
| PIX-SAL-03 | Saldo zerado com valor mínimo | 0,00 | — | 10:00 | 0,01 | Negada por saldo insuficiente. Saldo permanece 0,00 (nunca negativo). | Medium |
| PIX-SAL-04 | Saldo cobre o valor, mas o limite diurno não | 10.000,00 | — | 10:00 | 5.000,01 | Negada por limite diário (não por saldo). Sem débito; saldo 10.000,00. | High |
| PIX-SAL-05 | Valor dentro do limite, mas saldo não cobre | 500,00 | — | 10:00 | 1.000,00 | Negada por saldo insuficiente (mensagem de saldo). Sem débito; saldo 500,00. | High |
| PIX-SAL-06 | **[CONFIRMAR]** Valor acima do limite e acima do saldo ao mesmo tempo | 100,00 | — | 10:00 | 6.000,00 | Negada. Sem débito; saldo 100,00. Mensagem exibida: confirmar qual tem precedência (limite ou saldo). | Low |
| PIX-SAL-07 | Tentativa negada por saldo não consome limite | 1.000,00 (depois 10.000,00) | — | 10:00 | 3.000,00; após creditar 9.000,00, 5.000,00 | 1ª negada por saldo insuficiente. 2ª aprovada (limite diurno intacto); saldo final 5.000,00. | Medium |
| PIX-SAL-08 | Saldo, valor e limite diurno coincidem | 5.000,00 | — | 10:00 | 5.000,00 | Aprovada. Saldo final 0,00. | Medium |
| PIX-CON-01 | Duas PIX simultâneas estouram o limite diurno | 20.000,00 | — | 10:00 | 2 x 3.000,00 em paralelo | Apenas uma aprovada; a outra negada por limite. Total efetivado 3.000,00; saldo final 17.000,00. | High |
| PIX-CON-02 | Duas PIX simultâneas estouram o saldo | 1.000,00 | — | 10:00 | 2 x 1.000,00 em paralelo | Apenas uma aprovada; a outra negada por saldo insuficiente. Saldo final 0,00, nunca negativo. | High |

Distribuição: Valor mínimo (6), Limite diurno (9), Limite noturno (9), Fronteiras de horário (9), Transição entre janelas (3), Saldo (8), Concorrência (2). Prioridade: 26 High, 18 Medium, 2 Low.

## Importação no Xray

- No Test Case Importer, mapeie `Summary`, `Description`, `Priority`, `Labels` e `Test Type`. Mapeie `Action`, `Data` e `Expected Result` como campos de passo (cada caso tem um passo só).
- A pré-condição está na `Description`, não em Precondition do Xray. Se você usa Precondition como issue própria, vale criar uma ("Cliente PF com saldo X e Y já enviado") e vincular depois.
- `Priority` usa os nomes padrão do Jira (High, Medium, Low). Se a sua instância usa outros nomes (Alta, Média, Baixa), ajuste na coluna ou no mapeamento.
- O ID do caso (PIX-DIA-03 etc.) está no início do `Summary`, porque o Xray gera a chave própria na criação. Para filtrar o que depende de definição, busque `[CONFIRMAR]` no Summary.

## Preciso que você confirme

1. **06:00:00 e 20:00:00 pertencem a qual janela?** Assumi 06:00:00 como diurna e 20:00:00 como noturna (HOR-02 e HOR-05).
2. **Limite por janela ou teto único por dia?** Assumi dois limites independentes: quem gastou R$ 5.000,00 de dia ainda pode enviar R$ 1.000,00 à noite. Se for um teto único, os casos JAN-01, JAN-02 e JAN-03 invertem o resultado.
3. **O período noturno é um só ao cruzar a meia-noite?** Assumi que sim (NOT-09). Se o contador zera às 00:00, o resultado de NOT-09 muda.
4. **Qual mensagem aparece quando o valor passa do limite e do saldo?** (SAL-06.) Defina a precedência.

Fora do escopo desta lista, por falta de informação na regra: PIX agendado (vale o horário do agendamento ou da execução?), PIX Saque/Troco, devolução (restitui limite?), limite compartilhado entre canais (app, internet banking, API) e conta de pessoa jurídica. Se algum desses entra na sua história, me avise e eu acrescento os casos.

Para os casos que dependem de horário e de PIX anterior, você vai precisar de um ambiente com relógio ajustável (ou mock de data/hora) e massa com acumulado pré-carregado. Sem isso, as fronteiras de horário não são testáveis de forma repetível.
