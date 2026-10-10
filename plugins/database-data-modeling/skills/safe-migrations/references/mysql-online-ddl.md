# Migração segura em MySQL/InnoDB (online DDL)

Conferido em 2026-10-10 contra V-16 (MySQL 8.4, `innodb-online-ddl-operations`, Verificado pelo validador), V-17 (gh-ost, B7, MIT, conceito), V-30 (MySQL sem DDL transacional) e V-09. **Válido para MySQL 8.4**; MySQL 8.0 e 9.x diferem em algoritmos padrão e operações INSTANT: sempre conferir a página da versão instalada. Cobertura desta base para MySQL é rasa (sem EXPLAIN, deadlocks, backup: L-03, L-06): onde faltar fonte, escreva "sem fonte validada".

Sumário
1. Algoritmos e o que declarar
2. Tabela operação -> algoritmo (8.4)
3. Checklist de migração MySQL
4. Receitas
5. Ferramentas triggerless (conceito)
6. Armadilhas

## 1. Algoritmos e o que declarar

- `INSTANT`: só altera metadados; é o padrão no 8.4 quando suportado (V-16).
- `INPLACE`: reconstrói/ajusta no próprio motor, geralmente permitindo DML concorrente.
- `COPY`: cria tabela nova e copia; sem DML concorrente.
- **Declare `ALGORITHM` e `LOCK` explicitamente** no comando: se a operação não suporta o pedido, o comando **falha** em vez de cair em outro algoritmo em silêncio (visto nos exemplos da doc; a página não enuncia como regra universal, V-16). Isso transforma "bloqueou produção" em "erro imediato".

```sql
ALTER TABLE orders ADD COLUMN channel VARCHAR(20) NOT NULL DEFAULT 'web', ALGORITHM=INSTANT;
ALTER TABLE orders ADD INDEX idx_orders_customer_created (customer_id, created_at), ALGORITHM=INPLACE, LOCK=NONE;
```

## 2. Tabela operação -> algoritmo (8.4)

Apenas o que V-16 verificou; para o resto, abra a tabela da página oficial na versão em uso.

| Operação | Algoritmo | DML concorrente | Observação | Rótulo |
| --- | --- | --- | --- | --- |
| `ADD COLUMN` | `INSTANT` (padrão 8.4) | sim (metadado) | não em tabela `ROW_FORMAT=COMPRESSED` nem com índice FULLTEXT | V-16 |
| `DROP COLUMN` | `INSTANT` (padrão 8.4) | sim | mesmas exceções | V-16 |
| Criar índice secundário | `INPLACE` | sim | custo de I/O e espaço; espere lag de réplica | V-16 |
| Mudar tipo de coluna | só `COPY` | **não** (a doc diz que DML concorrente não é permitido) | reduzir `VARCHAR` também exige `COPY` | V-16 |
| Adicionar PK | reconstrói a tabela | conferir na página | custo alto | V-16 |
| Remover PK sem adicionar outra | só `COPY` | não | evitar | V-16 |
| `ADD COLUMN` auto-incremento | no mínimo `INPLACE, LOCK=SHARED` | **não** (leitura sim, escrita não) | não é online para escrita | V-16 |

Operações fora da tabela (renomear coluna, mudar default, adicionar FK, particionamento): não estão no recorte verificado; consulte a página oficial e rotule "sem fonte validada".

## 3. Checklist de migração MySQL

- [ ] **ALGORITHM e LOCK declarados** (falha em vez de fallback silencioso).
- [ ] Operação classificada como INSTANT, INPLACE ou COPY **na versão em uso**; anotada a versão consultada.
- [ ] Operação `COPY` (mudança de tipo, PK) em tabela grande: tratada como indisponibilidade de escrita ou migrada por ferramenta online (seção 5) após teste em réplica.
- [ ] Limite de ritmo (throttle) e janela da troca final definidos; procedimento de pausa.
- [ ] Confirmado que DML concorrente é permitido para a operação (coluna acima).
- [ ] Backup recente antes e contagem/checksum de comparação depois.
- [ ] Sem DDL transacional: se o arquivo tem vários comandos e o terceiro falha, o estado fica parcial. Uma mudança por arquivo (V-30). Plano de desfazer à mão escrito.
- [ ] Réplicas: DDL e backfill aumentam lag; limite definido.
- [ ] Ensaiado em cópia com volume real, incluindo distribuição (duplicatas, NULLs).

## 4. Receitas

### 4.1 Adicionar coluna (8.4, INSTANT)

```sql
ALTER TABLE orders ADD COLUMN channel VARCHAR(20) NOT NULL DEFAULT 'web', ALGORITHM=INSTANT;
```
Se falhar por exceção (tabela comprimida, FULLTEXT), declare `ALGORITHM=INPLACE` se suportado ou use a ferramenta da seção 5.

### 4.2 Novo índice

```sql
ALTER TABLE orders ADD INDEX idx_orders_customer_created (customer_id, created_at), ALGORITHM=INPLACE, LOCK=NONE;
```
Acompanhe `SHOW PROCESSLIST` (ou `performance_schema`) por esperas de metadata lock; transação longa aberta pode segurar o metadata lock e travar o DDL e quem chega depois (Inferido: mecanismo geral de MDL; conferir a doc da versão).

### 4.3 Mudar tipo (ex.: `INT` -> `BIGINT`)

Só `COPY` sem DML concorrente (V-16). Use expand/contract em [expand-contract-e-backfill.md](expand-contract-e-backfill.md): coluna nova `BIGINT`, escrita dupla, backfill em lotes por PK, troca de leitura, remoção. Alternativa: ferramenta online (seção 5) validada em réplica.

## 5. Ferramentas triggerless (conceito, não instalar por esta skill)

- **gh-ost** (GitHub, MIT, 13,6k estrelas na página consultada, V-17): migração online sem triggers, lendo o binlog; recomenda `--test-on-replica` antes de produção; permite pausar, limitar ritmo e adiar a troca final. Exige binlog em formato adequado e réplica para teste. O que a página diz sobre releases: use releases estáveis, não a `master` (V-17). Data do último commit: **Não verificado** nesta base.
- Outras (por exemplo, `pt-online-schema-change` do Percona, baseada em triggers): **não avaliadas** nesta base (Não verificável).
- Postura do plugin: documentar o conceito e o critério de escolha; **o usuário revisa e decide** instalar ou executar código de terceiros. Nunca instrua `curl | bash`.

## 6. Armadilhas

- Assumir que PostgreSQL e MySQL se comportam igual: aqui não há `CONCURRENTLY`; o análogo é `ALGORITHM/LOCK` explícitos e ferramentas online.
- Esperar atomicidade de DDL em migração com vários comandos: não existe (V-30).
- Executar mudança de tipo "porque é rápido em dev": COPY em tabela grande bloqueia escritas pela duração da cópia.
- Replicação: DDL pesado atrasa réplicas; lag alto invalida leitura em réplica durante a janela.
- Triggers/CDC e foreign keys ao usar ferramentas online: confira compatibilidade na doc da ferramenta (Não verificado aqui).
- Isolamento e deadlock no MySQL têm comportamento próprio (REPEATABLE READ, gap locks): ver `transactions-and-isolation`.
