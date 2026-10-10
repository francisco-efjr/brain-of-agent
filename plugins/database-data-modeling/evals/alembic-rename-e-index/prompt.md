---
name: alembic-rename-e-index
description: "Mede se o plugin trata migração autogerada pelo Alembic como rascunho, detecta rename virado em drop e add com perda de dados e exige CREATE INDEX CONCURRENTLY fora da transação no PostgreSQL 14."
tags: [database-data-modeling, safe-migrations, alembic, orm]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Identifica que o autogenerate transformou o rename em drop_column mais add_column (perda de dado), recomenda rename nativo ou expand/contract com compatibilidade de versões, indica CREATE INDEX CONCURRENTLY fora da transação com checagem de índice INVALID e manda ler o SQL gerado."
model: sonnet
---
Renomeei o atributo `fullname` para `full_name` no modelo SQLAlchemy da tabela `users` (Postgres 14, uns 30 milhões de linhas, API no ar o dia todo) e também adicionei `index=True` em `email`. Rodei `alembic revision --autogenerate` e saiu isto:

```python
def upgrade():
    op.drop_column('users', 'fullname')
    op.add_column('users', sa.Column('full_name', sa.String(), nullable=True))
    op.create_index('ix_users_email', 'users', ['email'])


def downgrade():
    op.drop_index('ix_users_email', table_name='users')
    op.drop_column('users', 'full_name')
    op.add_column('users', sa.Column('fullname', sa.VARCHAR(), nullable=True))
```

Posso rodar `alembic upgrade head` no deploy de amanhã? O env.py está com a configuração padrão.
