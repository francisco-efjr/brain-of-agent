# Backup e restore fora do PostgreSQL: modo genérico

**Status honesto:** esta base de conhecimento não tem fonte validada para backup de MySQL, SQL Server, MongoDB, DynamoDB e SQLite (lacunas L-06 e L-08 de `VALIDATED.md`). Redis tem fonte A (V-27) e está em `nosql-data-modeling/references/redis.md`. Tudo abaixo é conhecimento geral do domínio, rotulado **Inferido**, e serve para organizar perguntas e estrutura do runbook. Antes de recomendar um comando ao usuário, mande-o conferir na documentação oficial da versão instalada. Não cite números de retenção, limites ou preços.

Sumário
1. Como usar este arquivo
2. Tabela por engine
3. Perguntas por engine
4. Princípios que valem para todas
5. Escopo

## 1. Como usar este arquivo

1. Identifique a engine e se é autogerenciada ou serviço gerenciado (o provedor oferece backups próprios com recursos e limites próprios).
2. Preencha o runbook (`runbook-backup-restore.md`) com o **método** e as **perguntas pendentes**, rotulando "sem fonte validada".
3. Declare na saída: "Comandos e opções desta engine: Inferido. Conferir em <doc oficial> na versão <x>."

## 2. Tabela por engine (Inferido; conferir na doc oficial)

| Engine | Lógico | Físico / contínuo | Pontos de atenção |
| --- | --- | --- | --- |
| MySQL / MariaDB | `mysqldump` (para InnoDB, uma transação consistente costuma exigir `--single-transaction`; conferir) | Backup físico por ferramenta própria do ecossistema (ex.: MySQL Enterprise Backup, Percona XtraBackup: terceiros/produtos, não avaliados aqui) + **binlog** para recuperação até um instante | Binlog precisa estar ligado e arquivado antes do incidente; formato e retenção; sem DDL transacional (V-30) |
| SQL Server | Exportações lógicas (BACPAC) | `BACKUP DATABASE` completo/diferencial e `BACKUP LOG`; restauração em sequência (`RESTORE ... WITH NORECOVERY`) até o instante | Modelo de recuperação (FULL/SIMPLE) decide se há log; `RESTORE VERIFYONLY` não substitui restauração real |
| MongoDB | `mongodump`/`mongorestore` | Snapshots do volume; serviço gerenciado com backup contínuo | Consistência em cluster/replica set; oplog para instante; índices recriados na restauração |
| DynamoDB | Exportação para armazenamento de objetos | Backups sob demanda e recuperação contínua (PITR) do serviço | Restauração cria **nova** tabela; reconfigurar índices, políticas e alarmes; custos |
| SQLite | `.dump` (SQL texto) | Comando de backup online do shell/API (`.backup`), cópia do arquivo **só** com a garantia de que não há escrita ou usando a API | Copiar o arquivo de um banco em uso (especialmente em modo WAL) sem a API pode produzir cópia inconsistente (sem fonte lida, L-08) |
| Redis | RDB/AOF (ver `redis.md`) | — | Fonte A: V-27 |

## 3. Perguntas por engine (para o usuário responder)

Comuns: versão exata, serviço gerenciado ou não, tamanho, taxa de escrita, RPO/RTO, onde ficam os backups, quem tem acesso, último teste de restauração.

- MySQL: binlog ligado? formato (row/statement/mixed)? retenção do binlog? há réplica para backup sem carga na primária? versão (8.0/8.4/9.x)?
- SQL Server: modelo de recuperação? cadeia de log íntegra? backups verificados com restauração real? Always On?
- MongoDB: standalone, replica set ou sharded? Atlas ou autogerenciado? janela de oplog suficiente para o RPO?
- DynamoDB: PITR habilitado? quais tabelas? como são recriados índices secundários, TTL, streams e políticas após restaurar?
- SQLite: modo de journal (WAL?)? o app fecha conexões antes do backup? há API de backup disponível no driver?

## 4. Princípios que valem para todas (sem depender de engine)

1. Definir RPO/RTO com o responsável do produto antes de escolher método.
2. Backup fora do mesmo volume e da mesma conta/projeto do banco; credenciais escopadas por ambiente (V-37 como sinal de por que).
3. Restauração só em ambiente isolado; nunca sobre banco ativo; corte decidido pelo usuário.
4. Teste periódico com medição de tempo contra o RTO e registro (ver `teste-de-restauracao.md`).
5. Permissões restritas nos arquivos de backup; criptografia em repouso/trânsito; retenção e descarte definidos.
6. Réplica não é backup.
7. Distinguir reverter código, manter compatibilidade e restaurar dados (brain).

## 5. Escopo

Provisionar backups em banco gerenciado (configuração do provedor, IaC, redes) pertence ao segmento devops-cloud-infra; aqui fica o procedimento de dados e o critério de aceite. Backup de arquivos e volumes de infraestrutura, idem.
