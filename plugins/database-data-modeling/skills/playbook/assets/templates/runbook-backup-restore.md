# Runbook de backup e restore: [sistema/banco]

Versão: [N] · Responsável: [nome/time] · Última revisão: [AAAA-MM-DD] · Último teste de restauração: [data, duração, resultado]
Regra: este documento orienta pessoas. Restore em produção nunca é executado por automação sem confirmação explícita de quem responde pelo sistema.

## 1. Objetivos

| Métrica | Valor acordado | Com quem acordado | Medido no último teste |
| --- | --- | --- | --- |
| RPO | [ex.: 5 min] | [dono do produto] | |
| RTO | [ex.: 2 h] | [dono do produto] | |

## 2. Método e agenda

Engine e versão: [..]. Método: [PITR (base + WAL) | dump lógico | RDB+AOF | snapshot gerenciado]. Frequência: [base diária; WAL contínuo]. Retenção: [dias]. Lembrete: dump lógico não serve para PITR.

## 3. Armazenamento e segurança

Destino: [fora do volume e da conta do banco]. Permissões dos arquivos: [restritas]. Criptografia: [..]. Credenciais: [escopo por ambiente]. Configuração do servidor guardada à parte: [local] (recomendação).

## 4. Restauração em ambiente isolado

1. Preparar instância nova isolada da produção (rede, credenciais). Espaço e versão compatíveis: [..].
2. Obter o backup e conferir integridade (tamanho, checksum): [comando].
3. Restaurar: [comandos; ex. PG: banco criado de `template0`; `psql --set ON_ERROR_STOP=on --single-transaction`; ou `pg_restore -j N -d <banco_novo>`; PITR com `recovery.signal` e `restore_command`]. Nunca `--clean` sobre banco com dados que importam.
4. Executar `ANALYZE` (PG) e subir o banco em modo normal.
5. Verificar: contagens por tabela [lista], invariantes [lista], consulta crítica [..].
6. Registrar o tempo total e comparar com o RTO.
7. Decidir o corte para produção: [quem decide; critério]. Passos de corte são executados por pessoa autorizada, com confirmação por passo.

## 5. Teste periódico

Periodicidade: [..]. Registro: [data, quem, duração, resultado, falhas, ajustes].

## 6. Escalada

[Quem chamar, em que ordem; canal; critério para declarar desastre.]

## 7. Comandos não verificados

[Liste comandos de engines sem fonte validada (MySQL, SQL Server, MongoDB, DynamoDB) e confirme na documentação da versão.]
