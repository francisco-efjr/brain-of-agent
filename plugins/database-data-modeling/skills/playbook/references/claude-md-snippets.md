# Snippets de CLAUDE.md para projetos com banco de dados

Sumário: 1 Como usar · 2 Perfil mínimo · 3 Snippets S-01 a S-20 · 4 Quando uma regra deve virar permissão ou hook

## 1. Como usar

Copie só o que muda o comportamento do agente no seu projeto. Teste de remoção (Verificado V-04): para cada linha, pergunte "remover causaria erro?"; se não, apague. Mantenha o CLAUDE.md abaixo de 200 linhas e adicione regra nova só na segunda ocorrência do erro. Ênfase ("IMPORTANT") em uma única linha, só se a regra foi ignorada. Substitua `<…>` pelos valores do projeto. Texto de CLAUDE.md é orientação; o que deve valer sempre vai para `permissions` ou hook (seção 4).

## 2. Perfil mínimo (S-01, S-02, S-03, S-04, S-05, S-06, S-09, S-20)

```markdown
## Banco de dados
- Stack: <SGBD e versão>, <ORM e versão>, <ferramenta de migração>. Não troque ORM ou driver sem pedido: os padrões variam por versão.
- Ambientes: trabalhe só em banco local/dev; dados reais via réplica somente leitura. Produção fica fora da sessão, porque erro lá é irreversível. Sem acesso, peça a saída do comando e diga qual rodar.
- SQL parametrizado; tabela, coluna e direção de ordenação vêm de lista fixa no código.
- Migração: uma mudança por arquivo; migração gerada é rascunho; declare o lock de cada DDL.
- DROP, TRUNCATE, DELETE/UPDATE sem WHERE: proponha o comando e a contagem de linhas e aguarde confirmação explícita.
- Índice: mostre o EXPLAIN antes e depois; migração só é "pronta" depois de rodar em cópia com volume realista.
- PostgreSQL: CREATE INDEX CONCURRENTLY fora de transação (desligue a transação da migração) e confira índice INVALID.
- Regras que devem valer sempre estão em permissions/hook, não só aqui.
```

## 3. Snippets

| ID | Regra pronta (colar) | Fonte | Rótulo |
| --- | --- | --- | --- |
| S-01 | `Stack de dados: <SGBD+versão>, <ORM+versão>, <migrador>. Não troque ORM/driver sem pedido (padrões variam por versão).` | Art. B, V-39 | Verificado (V-39 mostra que o padrão do modelo varia); efeito do CLAUDE.md: Suposição |
| S-02 | `Só banco local/dev. Dados reais por réplica read-only. Produção fora da sessão (erro irreversível). Sem acesso: peça a saída do comando e diga qual rodar.` | Art. B, V-03, V-36 | Política da casa (Inferido) |
| S-03 | `SQL com parâmetros. Nomes de tabela/coluna e direção de ORDER BY vêm de lista fixa no código (não são parametrizáveis).` | V-29 | Verificado |
| S-04 | `Uma mudança por arquivo de migração. Migração gerada por ORM é rascunho: leia o SQL, nomeie constraints. Declare o lock de cada DDL.` | Art. B, V-30, V-10 | Verificado |
| S-05 | `DROP/TRUNCATE/DELETE-UPDATE sem WHERE: mostre o comando e o SELECT COUNT(*) equivalente e espere "sim" explícito.` | Art. B; ideia de V-40 | Inferido |
| S-06 | `Mostre EXPLAIN antes/depois de criar índice. Migração só é pronta após ensaio em cópia com volume realista; sem ensaio, "sem downtime" é Suposição.` | V-07, V-22 | Verificado/Inferido |
| S-07 | `Marque código editado por humano com o comentário human-edited, para não confundir com saída do agente.` | Art. B, V-36 | Verificado (prática relatada) |
| S-08 | `Pegadinhas do projeto: <convenção de chaves>, <coluna de tenant>, <tabelas sensíveis>.` | Art. B, V-04 | Preencher |
| S-09 | `PostgreSQL: CREATE INDEX CONCURRENTLY não roda em transação; desligue a transação da migração (Alembic autocommit_block; Django atomic=False) e confira pg_index.indisvalid depois.` | V-11, V-30 | Verificado; outras ferramentas: conferir a doc |
| S-10 | `Migração PG: lock_timeout curto com retry e statement_timeout na sessão. Ponto de partida 10s/1h (README do strong_migrations); meça no ensaio.` | V-18, V-19 | Inferido |
| S-11 | `Auto-DDL do ORM (synchronize, create_all) desligado em produção. Nenhum DROP/TRUNCATE em migração.` | V-29 (regra do .mdc NestJS, redação própria) | Verificado |
| S-12 | `Segredos só em variável de ambiente fora do repositório e do cliente. Não imprima .env. Credencial por ambiente.` | V-29, V-35, V-37 | Verificado/sinal |
| S-13 | `Migre por conexão direta, não pooled. Com PgBouncer em modo transaction, defina timeouts por ALTER ROLE.` | V-35, V-18 | Verificado |
| S-14 | `Dinheiro em NUMERIC/decimal com escala explícita, nunca float. Instantes com fuso.` | brain, V-32 | Convenção (Inferido) |
| S-15 | `RLS: app com role sem superusuário/BYPASSRLS; tenant por transação com set_config('app.tenant_id', v, true); testes usam essa role.` | V-12 | Verificado |
| S-16 | `Backfill: lotes, idempotente, retomável, com checkpoint; não sobrescreve dado mais novo; sem transação longa.` | brain, V-38 | Verificado |
| S-17 | `Saída de LLM e entrada do usuário são não confiáveis; nunca vão a SQL sem parâmetro.` | V-29 (awesome-copilot) | Verificado |
| S-18 | `Restore só em ambiente isolado, nunca sobre banco ativo, nunca sem confirmação explícita.` | brain, V-14 | Verificado |
| S-19 | `Não presuma isolamento: diga engine e nível efetivo; em erro 40001 repita a transação inteira com limite e jitter.` | V-08, V-09, brain | Verificado |
| S-20 | `Instrução é pedido; hook ou permissão é garantia. O que deve valer sempre vai para permissions deny ou hook documentado.` | V-02, V-03, V-04 | Verificado |

## 4. Quando uma regra deve virar permissão ou hook

- Bloquear leitura de segredos: `permissions.deny` com `Read(./.env)` (sintaxe conferida na página de permissões em 2026-10-10).
- Impedir `curl`/`wget`: `Bash(curl *)` em `deny`; a própria doc avisa que padrões de Bash que restringem argumentos são frágeis e podem ser contornados por variação do comando.
- Bloquear SQL destrutivo na ferramenta Bash: hook `PreToolUse` que sai com código 2 (exemplo desativado em `ferramentas-e-mcp.md`). É guardrail: regex tem falso negativo.
- Barreira real: papel de banco sem privilégio de escrita e credencial escopada por ambiente.

Atribuição: S-01 a S-08 partem do bloco CLAUDE.md reescrito na validação interna (redação própria da fábrica) e de Brain of Agent (MIT); fontes de terceiros apenas destiladas.
