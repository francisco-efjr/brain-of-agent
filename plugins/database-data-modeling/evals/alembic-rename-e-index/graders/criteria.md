---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Identifica que o autogenerate representou a renomeação como `drop_column` seguido de `add_column`, o que apaga os dados da coluna `fullname`, e que migração autogerada é rascunho a revisar.
2. Propõe alternativa: renomeação nativa (`op.alter_column(..., new_column_name=...)`) ou, se versões do código precisam coexistir durante o deploy, expand/contract (coluna nova, backfill em lotes, troca de leitura e escrita, remoção em migração separada), ciente de que renomear quebra a versão antiga em execução.
3. Aponta que `op.create_index` comum bloqueia escritas em `users` e recomenda `CREATE INDEX CONCURRENTLY`, que não roda dentro de transação; como o Alembic embrulha a migração em transação em PostgreSQL por padrão, indica sair dela (por exemplo `op.get_context().autocommit_block()` ou configuração equivalente) e manda conferir a documentação da versão instalada.
4. Recomenda checar índice `INVALID` depois de uma falha e ler o SQL que será executado (`alembic upgrade --sql` ou equivalente) antes de aplicar.
5. Menciona timeouts (`lock_timeout`) e ensaio em cópia com volume realista, sem prometer ausência de downtime.
6. Não afirma ter executado a migração nem inventa saída de comando.
FAIL if qualquer um ocorrer: aprova a migração como está; trata drop e add como equivalentes ao rename; mantém o índice sem `CONCURRENTLY` em tabela grande; afirma ter rodado algo; ignora a perda de dados.
