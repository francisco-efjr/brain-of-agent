# Checklists completos

Sumário: 1 Como usar · 2 Migração PostgreSQL · 3 Migração MySQL · 4 Plano de consulta · 5 Índices e paginação · 6 Transações e retry · 7 RLS multi-tenant · 8 Modelagem relacional · 9 Modelagem por acesso (NoSQL) · 10 Backup e restore · 11 Configuração segura · 12 Tools de MCP de banco · 13 Entrega

## 1. Como usar

Marque cada item como Verificado (evidência colada: código lido, saída de comando fornecida pelo usuário, teste rodado), Inferido, Suposição, Não verificável ou Não aplicável. Item violado vira achado: item, risco, alternativa. Os "porquês" explicam a regra para que o julgamento se adapte ao caso. Fontes `V-nn` estão em `fontes.md`.

## 2. Migração PostgreSQL (Art. C; V-10, V-11, V-18, V-19, V-30)

Confira primeiro a versão do servidor: PG 18 documenta `NOT VALID` para not-null; versões anteriores usam CHECK.

- [ ] Lock declarado para cada DDL? `ALTER TABLE` usa `ACCESS EXCLUSIVE` salvo exceção; subcomandos combinados usam o mais forte. Porquê: esse lock bloqueia até `SELECT`.
- [ ] Índice novo com `CREATE INDEX CONCURRENTLY`, fora de transação, e checagem de `INVALID` depois? Porquê: o build comum bloqueia escrita; o concorrente pode falhar deixando lixo.
- [ ] FK, CHECK e NOT NULL em duas etapas (`NOT VALID`, depois `VALIDATE CONSTRAINT`)? Porquê: a validação usa lock mais leve; para NOT NULL, um CHECK válido evita o scan.
- [ ] Coluna nova sem default volátil? Default fixo é metadado; volátil reescreve a tabela. Backfill em lotes, fora de transação longa.
- [ ] Mudança de tipo ou renome em expand/contract, nunca DDL direto?
- [ ] `lock_timeout` curto e `statement_timeout` na sessão da migração, com retry para falha de lock? (Valores de partida em V-18, Inferido.)
- [ ] Uma tabela por transação, salvo necessidade de atomicidade? Transações da aplicação não ficam abertas em espera?
- [ ] Migração por conexão direta, não pooled; timeouts por `ALTER ROLE` se há PgBouncer em modo transaction?
- [ ] Testada em cópia com volume realista, incluindo duplicatas e NULLs?
- [ ] Rollback escrito e ensaiado; "reverter schema" diferente de "reverter dados"?
- [ ] Migração gerada por ferramenta revisada à mão; `sqlmigrate`/dry-run lido?
- [ ] Constraints com nome explícito?

Saída: lista de achados com item violado, risco e alternativa; rótulos.

## 3. Migração MySQL (Art. D corrigido; V-16, V-17; válido para 8.4, confira a versão)

- [ ] Operação classificada: `INSTANT` (add/drop column; não com `ROW_FORMAT=COMPRESSED` nem FULLTEXT), `INPLACE` (índice secundário com DML concorrente), `COPY` (mudar tipo; sem DML concorrente)?
- [ ] `ALGORITHM=` e `LOCK=` explícitos para falhar em vez de degradar?
- [ ] `ADD COLUMN AUTO_INCREMENT` tratado (mínimo `INPLACE, LOCK=SHARED`, sem DML concorrente); PK adicionada reconstrói a tabela?
- [ ] Sem DDL transacional: uma mudança por arquivo e plano de desfazimento manual?
- [ ] Tabela grande + mudança de tipo: ferramenta de migração online (gh-ost como conceito: binlog, `--test-on-replica`) avaliada pelo usuário?
- [ ] Lag de réplica monitorado durante o `INPLACE`?

## 4. Plano de consulta (Art. E; V-07)

- [ ] `EXPLAIN` primeiro; `EXPLAIN ANALYZE` executa: DML só em `BEGIN…ROLLBACK`, réplica/dev, nunca produção.
- [ ] Estimado × real por nó; divergência grande → `ANALYZE` e comparar.
- [ ] `Seq Scan` em tabela grande com índice de suporte avaliado (ordem das colunas).
- [ ] Tempo e linhas × `loops`; `BUFFERS` para I/O.
- [ ] Tempo não inclui rede (`SERIALIZE` mede conversão de saída).
- [ ] Mesma massa de dados antes e depois; resultado registrado em `relatorio-explain.md`.

## 5. Índices e paginação (V-23, V-24)

- [ ] Colunas de igualdade antes da de faixa/ordenação; ≤ 3 colunas salvo evidência.
- [ ] Função aplicada à coluna? Índice de expressão (PG) ou coluna gerada/collation (MySQL, SQL Server).
- [ ] FK com índice no lado filho.
- [ ] `OFFSET` grande → seek com PK de desempate (Inferido).
- [ ] Custo de escrita e espaço do índice declarado; sem índice prefixo de outro.
- [ ] Criado online; `indisvalid` conferido.
- [ ] N+1 descartado antes de culpar o índice.

## 6. Transações, isolamento e retry (V-08, V-09, brain)

- [ ] Engine e nível efetivo declarados (PG RC, MySQL RR, SQL Server RCSI se ligado).
- [ ] Anomalia descrita em antes/depois; correção atômica (UPDATE condicional, lock, versão) ou SERIALIZABLE com retry.
- [ ] Retry repete a transação inteira em `40001` (e deadlock), com limite e jitter.
- [ ] Rede de segurança no banco (CHECK, UNIQUE).
- [ ] Teste com duas sessões coordenadas por barreira; no máximo uma aceitação; estoque ≥ 0.
- [ ] Transações curtas; ordem consistente de locks; sem `idle in transaction`.
- [ ] Nenhuma extrapolação entre engines.

## 7. RLS multi-tenant (Art. G; V-12, V-33)

- [ ] Modelo de tenancy escolhido e registrado antes de RLS.
- [ ] RLS ligado e política presente em toda tabela com dado de tenant (sem política = nega tudo).
- [ ] `USING` e `WITH CHECK` revisados: INSERT/UPDATE não movem linha para outro tenant.
- [ ] Aplicação conecta com role sem superusuário e sem `BYPASSRLS`; testes usam essa role.
- [ ] `FORCE ROW LEVEL SECURITY` quando o dono também executa consultas da aplicação.
- [ ] Tenant por transação com `set_config('app.tenant_id', valor, true)`; nunca `SET` simples em conexão de pool.
- [ ] Views com `security_invoker` (PG ≥ 15); materialized views e exportações não vazam tenants.
- [ ] `SECURITY DEFINER` com `search_path` fixo e sem id de usuário como parâmetro livre.
- [ ] Políticas sem subconsulta em outras tabelas, ou com `FOR SHARE`/função definer documentada.
- [ ] Unicidade e FK podem vazar existência: avaliado.
- [ ] `TRUNCATE` e `REFERENCES` fora da cobertura: permissões restritas.
- [ ] Índices nas colunas das políticas; teste de dois tenants (leitura, escrita, acesso cruzado) rodado.

## 8. Modelagem relacional (Art. N corrigido; V-32 classe B, convenções = Inferido; L-01)

- [ ] Entidades, invariantes e consultas críticas na ficha de acesso.
- [ ] Normalizado até 3FN; desnormalização só com medição (Inferido).
- [ ] PK `BIGINT GENERATED ALWAYS AS IDENTITY` por padrão; UUID com motivo (Inferido).
- [ ] Dinheiro em `NUMERIC`/decimal com escala explícita, nunca float; instantes com fuso (`timestamptz`) (convenção).
- [ ] CHECK, UNIQUE, NOT NULL e FK refletem as invariantes (o ORM não protege outros escritores).
- [ ] `NULLS NOT DISTINCT` apenas PG ≥ 15; `JSONB` só para atributos opcionais.
- [ ] Tipos evitados por convenção, não norma: `char(n)`, `money`, `timetz`, `serial` (preferir identity).
- [ ] Índices de suporte para FKs e filtros críticos.
- [ ] Retenção e dados pessoais identificados.

## 9. Modelagem por acesso (Art. H corrigido; V-25, V-26, V-28)

- [ ] Ficha de padrões de acesso preenchida; sem ela, perguntas (uma por vez).
- [ ] Cardinalidade e crescimento do filho respondidos (MongoDB: embutir ou referenciar).
- [ ] Limite de 16 MB considerado (fonte: SKILL.md do MongoDB).
- [ ] DynamoDB: menor número de tabelas com exceções justificadas; chaves de alta cardinalidade; GSI por consulta extra.
- [ ] Redis: estrutura por acesso; chave com prefixo de tenant; TTL; persistência RDB+AOF ou decisão documentada.
- [ ] Nenhuma escrita sem "yes" explícito.

## 10. Backup e restore (Art. I corrigido; V-14, V-27)

- [ ] RPO/RTO definidos com o responsável do produto.
- [ ] Método coerente (PITR base + WAL; dump não serve para PITR; Redis RDB+AOF).
- [ ] `archive_command` retorna 0 só com sucesso e não sobrescreve; monitorar espaço de `pg_wal/`.
- [ ] Backups com permissão restrita, fora do mesmo volume e conta; configuração guardada à parte (recomendação).
- [ ] Restore apenas em ambiente isolado, banco criado de `template0`, `ON_ERROR_STOP`/`--single-transaction`, `ANALYZE` depois.
- [ ] Nenhum restore executado sem confirmação explícita do usuário.
- [ ] Tempo real de restauração medido contra o RTO; teste periódico registrado.

## 11. Configuração segura (Art. M corrigido; V-15, V-29)

- [ ] Senhas com SCRAM; `hostssl` exige TLS.
- [ ] Criptografia em repouso por filesystem/bloco ou serviço gerenciado; TDE nativo = Não verificado.
- [ ] App sem papel DBA; papel somente leitura para análise.
- [ ] Segredos fora do repositório e do cliente; auto-DDL desligado em produção.
- [ ] Erros sem SQL nem stack trace; logs sem dado pessoal.

## 12. Tools de MCP de banco (Art. O; V-05, V-34)

- [ ] Poucas tools consolidadas, com namespace por serviço/recurso (`db_`, `pg_`).
- [ ] Nomes legíveis em vez de UUIDs; `user_id` em vez de `user`.
- [ ] `response_format` concise/detailed; paginação, filtro e truncamento com padrão sensato (Claude Code limita respostas de tool a 25 mil tokens por padrão).
- [ ] Erros acionáveis (o que tentar a seguir).
- [ ] Modo somente leitura/`restricted` por padrão; limites de linhas e de tempo (valores específicos: Inferido).
- [ ] Descrição "como para um novo membro do time".
- [ ] Avaliada com tarefas realistas antes de ligar; instalada pelo usuário, em réplica ou dev.

## 13. Entrega (Brain of Agent, adaptado; MIT)

- [ ] Schema, consumidores, volume e versão observados.
- [ ] Constraints e precisão refletem invariantes de negócio.
- [ ] Concorrência testada com coordenação e transação efetiva.
- [ ] Plano/query analisado em dados representativos, sem exposição.
- [ ] Migração suporta versões coexistentes e lote retomável.
- [ ] Locks, espaço, duração e interrupção têm critério definido.
- [ ] Backup e restauração validados em ambiente permitido.
- [ ] Rollback documenta perda potencial e compatibilidade.
- [ ] Dados pós-migração comparados por contagem e invariantes.
- [ ] "O que falta para concluir" preenchido.
