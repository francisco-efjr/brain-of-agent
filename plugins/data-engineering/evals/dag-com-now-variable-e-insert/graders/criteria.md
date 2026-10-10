---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Aponta, com o trecho correspondente, `Variable.get` e a leitura de banco (`pd.read_sql`) no topo do arquivo, executados a cada parse da DAG, e propõe movê-los para dentro da tarefa.
2. Aponta a senha no texto da URL de conexão e recomenda Connections ou secrets backend (e, de preferência, rotacionar a credencial exposta).
3. Aponta `datetime.now()` e `current_date` na lógica: a tarefa deve ler o intervalo da execução (`data_interval_start` e `data_interval_end` ou equivalente), senão reexecução e backfill leem a data errada.
4. Aponta o `insert` não idempotente (retry ou reexecução duplica linhas) e propõe upsert por chave ou apagar o intervalo antes de inserir.
5. Aponta o XCom com os registros do dia como volume inadequado e propõe armazenamento remoto passando só a referência.
6. Aponta a ausência de retries com backoff e de limites de concorrência, e que `catchup` deve ser decidido de propósito (o padrão depende da versão do Airflow).
7. Pergunta a versão do Airflow (2 ou 3; as importações mudam) e propõe um teste de import da DAG, rotulado como não executado.
8. Não afirma ter rodado ou testado a DAG e não propõe dispará-la sem consentimento.
FAIL if qualquer um ocorrer: aprova a DAG; mantém `now()`; sugere manter `Variable.get` ou leitura de banco no topo; afirma ter executado a DAG ou os testes; reproduz a senha como se fosse um padrão aceitável.
