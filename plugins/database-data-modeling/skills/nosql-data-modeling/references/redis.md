# Redis: estrutura, chaves, persistência e backup

Conferido em 2026-10-10 contra V-28 (`redis/agent-skills`, skill `redis-core`, MIT, 166 estrelas na página consultada; classe B; prompt-score 67; versão 0.1.0; arquivos `references/` citados por ela não foram vistos) e V-27 (documentação oficial de persistência do Redis, classe A, lida inteira, com os três comportamentos de versão confirmados). Lacunas L-07: eviction (políticas `maxmemory`), cluster e ACL **sem fonte validada** (as skills `redis-security` e `redis-clustering` do mesmo repositório não foram lidas). Texto em redação própria.

Sumário
1. Escolha da estrutura pelo acesso
2. Nomes de chave
3. Padrões comuns
4. Persistência
5. Backup
6. Perguntas de revisão
7. Lacunas

## 1. Escolha da estrutura pelo acesso (V-28)

| Acesso | Estrutura | Observação |
| --- | --- | --- |
| Valor simples, contador, flag | String | `INCR` para contadores |
| Objeto com campos lidos/atualizados separadamente | Hash | Evita serializar o objeto inteiro em String (V-28) |
| Fila simples, pilha, últimos N | List | Para filas robustas considere Stream |
| Conjunto sem repetição, pertencimento | Set | Operações de união/interseção |
| Ranking, janelas por pontuação/tempo | Sorted Set | Leaderboards, agendamento por timestamp |
| Documento aninhado com consulta por caminho | JSON (módulo/Stack) | Depende de a instalação ter o recurso: conferir |
| Log de eventos com consumidores | Stream | Grupos de consumidores |
| Busca por similaridade | Vector Set | Fronteira com llm-ai-agents: escolha de vector DB é lá |

Regra: nunca guardar um objeto plano serializado em String se os campos são acessados individualmente (V-28).

## 2. Nomes de chave (V-28)

- Formato `entidade:id:atributo`, **minúsculas**, curtas, sem URL inteira, com **prefixo de tenant** quando multi-tenant.
- Exemplos: `tenant:42:user:1001:profile` (Hash), `tenant:42:lb:2026-10` (Sorted Set), `session:ab12...` (String com TTL).
- Padronize separador (`:`) e documente o catálogo de chaves (nome, tipo, TTL, dono, volume esperado).
- Evite chaves enormes e variáveis ilimitadas no nome (explode o keyspace).
- Não use dados pessoais crus em nomes de chave (aparecem em logs e dumps): use ids opacos (Inferido).

## 3. Padrões comuns

- **Cache**: String/Hash com **TTL sempre definido**; estratégia de invalidação escrita (por evento ou por expiração). Cache sem TTL é bug latente (Inferido).
- **Sessão**: String/Hash com TTL deslizante; dado sensível mínimo.
- **Contador / limite de taxa**: `INCR` por janela; a criação com TTL deve ser atômica (por exemplo `SET chave 1 EX 60 NX` seguido de `INCR`, ou script). Evite `INCR` e `EXPIRE` separados sem tratar falha entre eles (Inferido).
- **Ranking**: Sorted Set com `ZADD`/`ZREVRANGE` (ou comandos equivalentes da versão).
- **Fila**: List/Stream; garantias de entrega e reprocessamento são desenho de fila (backend-api).
- Operações em produção: `SCAN` em vez de `KEYS` (Inferido).

## 4. Persistência (V-27)

| Mecanismo | O que é | Perda | Observação |
| --- | --- | --- | --- |
| RDB | Snapshot periódico; compacto; usa `fork` | Os últimos minutos desde o snapshot | Bom para backups e restart rápido |
| AOF | Registro de comandos; `appendfsync everysec` é o padrão sugerido | Até 1 s | Arquivo maior; reescrita periódica |
| RDB + AOF | Ambos | Durabilidade comparável à do PostgreSQL (V-27) | Recomendado quando perda é cara |
| RDB sozinho | Só snapshot | Minutos | Aceitável se alguns minutos de perda são aceitos |
| AOF sozinho | Só log | ~1 s | Desencorajado pela doc (V-27) |

Decisão: pergunte "quanto dado o produto aceita perder?" (RPO) antes de escolher. Redis como cache puro pode dispensar persistência; Redis como armazenamento primário não (V-27).

Mudar RDB para AOF num servidor **em execução**: use `CONFIG SET` e **atualize o `redis.conf`**; apenas reiniciar não faz a troca correta (V-27). Comandos para o usuário rodar em ambiente permitido (leitura):

```text
CONFIG GET save
CONFIG GET appendonly
INFO persistence        # rdb_last_bgsave_status, aof_enabled, aof_rewrite_in_progress, ...
LASTSAVE
```

## 5. Backup (V-27)

1. **RDB**: copiar o arquivo `dump.rdb` é seguro com o servidor rodando (V-27). Mantenha cópias periódicas.
2. **AOF (Redis 7.0+)**: antes de copiar, **desligar a reescrita automática** (`CONFIG SET auto-aof-rewrite-percentage 0`) e conferir que `aof_rewrite_in_progress` é 0; religue depois (V-27).
3. **Fora da máquina**: enviar uma cópia para fora do servidor ao menos uma vez por dia; **verificar tamanho e SHA1** do arquivo copiado; ter alerta independente de falha de transferência (V-27).
4. **Restore**: sempre em instância isolada; conferir contagem de chaves (`DBSIZE`) e amostras antes de apontar a aplicação (Inferido, alinhado a `backup-restore-runbook`).
5. Família de comandos `BACKUP` em versões novas (a doc consultada menciona a partir do Redis 8.10.0): conferir na doc da versão antes de recomendar (V-27).
6. Permissão restrita nos arquivos de backup; backup no mesmo volume/conta do servidor não protege contra a falha mais comum (V-37, só como sinal).

## 6. Perguntas de revisão

1. Quais chaves existem, de que tipo, com que TTL e qual o crescimento do keyspace?
2. O que acontece se o Redis reiniciar vazio (cold cache)? A origem da verdade aguenta o pico?
3. Quanto dado se aceita perder (RPO) e quanto tempo para voltar (RTO)?
4. Quem escreve nas mesmas chaves (concorrência de aplicação)? Transações/scripts são necessários?
5. Há dados pessoais ou segredos guardados? Criptografia em trânsito/acesso por senha/ACL (lacuna L-07)?

## 7. Lacunas (declare na saída)

Eviction (`maxmemory-policy`), cluster/sharding, ACL e segurança, Sentinel/alta disponibilidade e latência: sem fonte validada nesta base (L-07). Responda com princípios gerais rotulados Inferido e peça que o usuário confira a documentação da versão instalada.
