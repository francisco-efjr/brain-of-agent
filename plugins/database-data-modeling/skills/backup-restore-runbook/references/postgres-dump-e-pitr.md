# PostgreSQL: dump lógico e PITR (comandos e notas de versão)

Conferido em 2026-10-10 contra V-14 (`continuous-archiving` e `backup-dump`, PostgreSQL 18.6; Verificado: PITR = backup base + arquivo contínuo de WAL; `pg_dump` não serve para PITR; `wal_level` replica ou superior e `archive_mode` on; `archive_command` retorna zero só se teve sucesso e deve recusar sobrescrever; PANIC se o filesystem do `pg_wal/` encher; restore usa `recovery.signal` e `restore_command`; `pg_dump` em plain, custom e directory, e `-F d` obrigatório com `-j`; `pg_restore -j` vale para custom e directory; restore de texto: banco criado de `template0`, `ON_ERROR_STOP` ou `--single-transaction`, depois `ANALYZE`; backup completo quase sempre exige superusuário) e V-15. Itens sem V-nn são conhecimento estável (Inferido): conferir na doc da versão instalada. **Estes comandos são para o usuário executar em ambiente apropriado; a skill não executa nada.** Comandos de restauração visam sempre um servidor/banco **isolado**.

Sumário
1. Credenciais sem expor senha
2. Dump lógico
3. Restauração de dump em ambiente isolado
4. PITR: configuração
5. PITR: base backup
6. PITR: recuperação até um instante
7. Verificações e armadilhas
8. Windows

## 1. Credenciais sem expor senha

Não coloque senha na linha de comando nem em URL salva em histórico. Use arquivo de senha (`.pgpass` no Linux/macOS; `%APPDATA%\postgresql\pgpass.conf` no Windows), variáveis de ambiente de sessão restritas ou arquivo de serviço (Inferido; conferir na doc de libpq). O papel de backup precisa de leitura do banco; backup completo quase sempre exige superusuário (V-14).

## 2. Dump lógico

```bash
# formato custom: compacto, restaura seletivamente com pg_restore
pg_dump -Fc -f app_2026-10-10.dump -h <host> -U <papel_de_backup> app

# formato directory: permite paralelismo na geração (-j) e no restore
pg_dump -F d -j 4 -f app_2026-10-10.dir -h <host> -U <papel_de_backup> app

# papéis e tablespaces não entram no pg_dump: exporte à parte (Inferido)
pg_dumpall --globals-only -h <host> -U <superusuario> > globals_2026-10-10.sql
```

Pontos (V-14): `-F d` é obrigatório para usar `-j` no `pg_dump`; `pg_restore -j` vale para custom e directory; `pg_dump` **não** serve para PITR. Dumps são fotografia consistente do instante em que a leitura começou (Inferido); não incluem arquivos de configuração do servidor.

Armazenamento: gravar fora do volume do banco, em conta/projeto diferente, com permissões restritas (o arquivo contém o banco inteiro), e registrar tamanho e hash (`sha256sum`/`Get-FileHash`) para conferência (Inferido).

## 3. Restauração de dump em ambiente isolado

Alvo: servidor de ensaio (container, VM, instância temporária), **nunca** o banco ativo de produção.

```bash
# 3.1 criar o banco vazio a partir de template0 (V-14)
createdb -h <host_ensaio> -U <superusuario> -T template0 app_restore

# 3.2 papéis globais primeiro, se necessário (arquivo gerado por pg_dumpall --globals-only)
psql -h <host_ensaio> -U <superusuario> -v ON_ERROR_STOP=1 -f globals_2026-10-10.sql

# 3.3 restaurar dump custom/directory
pg_restore -h <host_ensaio> -U <superusuario> -d app_restore --exit-on-error -j 4 app_2026-10-10.dump
#   alternativa em transação única (não combina com -j; conferir pg_restore --help da versão):
pg_restore -h <host_ensaio> -U <superusuario> -d app_restore --single-transaction app_2026-10-10.dump

# 3.4 se o dump for texto plano
psql -h <host_ensaio> -U <superusuario> -d app_restore -v ON_ERROR_STOP=1 --single-transaction -f app_2026-10-10.sql

# 3.5 estatísticas (V-14)
psql -h <host_ensaio> -U <superusuario> -d app_restore -c "ANALYZE;"
```

Sobre `--clean`/`-c` do `pg_restore`: remove objetos do banco alvo antes de recriá-los (Inferido; conferir). **Não use com alvo que tenha dados que importam.** Em ambiente isolado recém-criado é desnecessário. O comando `pg_restore -d prod --clean ...` do pedido urgente sobrescreve o que ainda existe em produção: não executar; restaurar em isolado e decidir o corte depois da verificação.

Depois: verificação funcional (`teste-de-restauracao.md`).

## 4. PITR: configuração

Pré-requisitos no servidor de origem (V-14): `wal_level` = `replica` (ou superior), `archive_mode` = `on`, `archive_command` que retorna zero somente se a cópia deu certo e que **recusa sobrescrever** arquivo existente.

```ini
# postgresql.conf (exemplo Linux; adaptar; reiniciar quando exigido pela versão)
wal_level = replica
archive_mode = on
archive_command = 'test ! -f /mnt/wal_archive/%f && cp %p /mnt/wal_archive/%f'
```

- Teste o `archive_command` isoladamente antes de confiar nele (copiar um arquivo de teste duas vezes: a segunda deve falhar).
- Destino de arquivamento **fora** do volume do banco e fora da conta; permissões restritas.
- Monitore: se o arquivamento falhar, o `pg_wal/` acumula e, se o filesystem encher, o servidor dá PANIC (V-14: ocorre quando o disco lota, não quando o diretório apenas cresce). Alerta de espaço e de falha de `archive_command` (por exemplo `pg_stat_archiver`, Inferido).
- Em Windows, o `archive_command` deve ser um script que verifique existência, copie e devolva código de saída diferente de zero em qualquer falha (a doc oficial traz um exemplo simples com `copy`; não verifica sobrescrita).

## 5. PITR: base backup

```bash
pg_basebackup -h <host> -U <papel_de_replicacao> -D /backups/base_2026-10-10 -Ft -z -Xs -P
```

- Gera o backup base (formato tar comprimido aqui; `-Fp` para plain). Opções exatas variam por versão (Inferido): conferir `pg_basebackup --help`.
- Verificação de integridade de backups em formato plain com `pg_verifybackup` (PostgreSQL 13+; suporte a outros formatos depende da versão; Inferido).
- Registre: instante de início/fim, versão do servidor, tamanho, hash, localização, quem executou.
- A cadeia é **base + todos os WAL desde o início do backup** até o alvo: perder um segmento intermediário interrompe a recuperação.

## 6. PITR: recuperação até um instante

Em um servidor **isolado** (nunca sobre o diretório de dados em uso):

1. Parar o servidor de ensaio; esvaziar o diretório de dados de ensaio; restaurar o backup base nele (extrair o tar).
2. Configurar no `postgresql.conf` do ensaio (V-14 para `restore_command`/`recovery.signal`):
```ini
restore_command = 'cp /mnt/wal_archive/%f %p'
recovery_target_time = '2026-10-10 14:29:00-03'      # instante imediatamente antes do incidente; fuso explícito
recovery_target_action = 'pause'                     # pausa no alvo para inspeção (Inferido; conferir)
```
3. Criar o arquivo vazio `recovery.signal` no diretório de dados (V-14) e iniciar o servidor. Ele reproduz os WAL até o alvo.
4. Conectar (somente leitura) e verificar o estado: contagens, linhas do período, invariantes. Se o instante estiver errado, repetir com outro alvo a partir de uma nova restauração do base (não é possível "voltar" depois de promover; Inferido).
5. Promover só depois da verificação (por exemplo `SELECT pg_wal_replay_resume();` quando em pausa; Inferido; conferir na versão).
6. Qualquer corte de produção para o servidor recuperado é decisão do usuário, planejada (DNS/strings de conexão, réplicas a refazer), fora desta skill.

Como escolher o alvo: horário do último estado conhecido bom (logs de aplicação, hora do deploy/migração/comando incorreto) com margem; preferir recuperar duas vezes a recuperar tarde demais. Cada tentativa parte do base backup original.

## 7. Verificações e armadilhas

- Último `pg_dump` bem-sucedido e seu tamanho (queda brusca de tamanho é alerta).
- `archive_command` falhando em silêncio: consulte as estatísticas do arquivador e o log do servidor.
- Versão: o backup base só restaura em servidor da **mesma versão maior**; dump lógico pode ser restaurado em versão maior mais nova (Inferido; conferir).
- Extensões e locale do alvo devem existir (a restauração falha ou muda ordenação se faltarem; Inferido).
- Permissões de objetos grandes, `search_path` e papéis: ver `globals` (seção 2).
- Dados sensíveis em dumps: tratar como produção (acesso, criptografia, retenção, descarte).
- Teste periódico: sem ele a cadeia pode estar quebrada há meses sem ninguém saber.

## 8. Windows

- Prefira PowerShell ou Git Bash conforme o ambiente; caminhos com espaço entre aspas.
- `Get-FileHash -Algorithm SHA256 arquivo` para hash.
- `archive_command` e `restore_command`: use script `.cmd`/PowerShell com verificação de existência e de código de saída; barras invertidas precisam de escape no `postgresql.conf`.
- Agendamento: Task Scheduler ou o agendador do serviço gerenciado; registre exit codes.
