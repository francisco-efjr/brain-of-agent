# Notas e incertezas

Resposta feita só com conhecimento próprio, sem consultar skills nem a pasta evals/. Nenhuma requisição de rede. Arquivos gerados por `gerar_casos.py` (CSV e tabela.md); `resposta.md` é a mensagem final.

## Incertezas sobre a regra (viraram premissas e casos [CONFIRMAR])
- Fronteira de horário: "entre 6h e 20h" não diz se 06:00:00 e 20:00:00 são diurnos ou noturnos. Assumi 06:00:00 diurno e 20:00:00 noturno.
- Interpretação de "limite diário": assumi dois limites independentes, um por janela (interpretação I). A alternativa (teto único por dia calendário, com o valor do limite variando conforme o horário da transação) inverte JAN-01, JAN-02 e JAN-03 e pode mudar NOT-09.
- Período noturno cruzando a meia-noite tratado como um único período (NOT-09). Se o contador zera às 00:00, muda.
- Mensagem de erro quando estoura limite e saldo ao mesmo tempo (SAL-06): sem precedência definida.
- Mais de 2 casas decimais (VAL-05): rejeitar ou mascarar é suposição minha; a regra só diz mínimo R$ 0,01.
- Horário de referência = servidor/Brasília (HOR-09). Suposição.
- Regra avaliada na confirmação, não na abertura da tela (HOR-08). Suposição.

## Incertezas sobre o Xray
- Não validei a importação (sem acesso ao Xray). O formato segue o Test Case Importer (Summary, Description, Test Type, Priority, Labels, Action, Data, Expected Result), mas os nomes de colunas dependem do mapeamento feito no wizard e podem variar entre Xray Cloud e Server/DC.
- Uma linha por caso, com um único passo. Em Xray Cloud e Server o jeito de importar vários passos por teste difere, então optei por um passo só para reduzir risco. Se a equipe prefere passos separados, é preciso reformatar.
- Labels: usei um único label por caso (sem vírgula nem espaço) porque não tenho certeza de como o importador separa vários labels.
- Priority usa High/Medium/Low (padrão Jira). Instâncias em português podem ter nomes diferentes.
- Pré-condição foi para Description, não para Precondition do Xray.
- CSV com todos os campos entre aspas, UTF-8 sem BOM, separador vírgula. Excel em pt-BR pode abrir com separador ponto e vírgula; o wizard permite escolher o delimitador.
- Description tem quebras de linha dentro de campos entre aspas; o importador deve aceitar, mas não testei.

## Outras observações
- Prioridades: 26 High de 46 é muito alto para um conjunto desses; mantive porque quase tudo são fronteiras de regra de negócio e controle de risco financeiro. Pode ser rebaixado se o time quiser.
- Fora do escopo: PIX agendado, PIX Saque/Troco, devolução e restituição de limite, limite compartilhado entre canais, PJ, cheque especial, tarifas, modo de bloqueio por fraude, e se o limite é alterável pelo cliente. A regra dada não cobre; citei na resposta.
- Os casos de horário e de acumulado exigem relógio ajustável ou mock e massa pré-carregada; citei na resposta.
- Conferi à mão a aritmética dos saldos finais (saldo - valor) em cada caso; não há teste automatizado disso.
