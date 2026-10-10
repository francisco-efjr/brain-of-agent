# RPO/RTO, teste de restauração e registro

Base: brain `dados-e-migracoes.md` (MIT, Brain of Agent: "Definir RPO/RTO com responsável do produto, testar restauração em ambiente isolado e verificar consistência funcional. 'Backup existe' não prova que a restauração cabe no prazo. Nunca testar restaurando por cima de banco ativo"; atribuição mantida), V-14 e V-27. O restante é método de trabalho (Inferido). Fontes consultadas em 2026-10-09 (brain) e conferidas em 2026-10-10 contra `VALIDATED.md`. SQL conceitual: adaptar à engine do projeto.

Sumário
1. Questionário de RPO e RTO
2. Mapa objetivo -> técnica
3. Checklist de ensaio de restauração
4. Verificação funcional (exemplos)
5. Registro do teste
6. Resposta a incidente: ordem segura
7. Dados pessoais no ambiente de ensaio

## 1. Questionário de RPO e RTO

Perguntas ao responsável do produto (uma por vez; registre nome e data da resposta):

1. Se perdermos dados, qual o máximo aceitável em minutos de escrita (RPO) para cada banco/entidade? (pedidos e pagamentos costumam exigir muito menos que cache de sessão.)
2. Se o banco ficar indisponível, qual o tempo máximo até voltar (RTO)? E o custo por hora parada?
3. Há obrigações legais de retenção ou de exclusão (LGPD, contratos) que afetam o que o backup guarda e por quanto tempo?
4. Quem decide acionar a restauração e o corte? Quem executa?
5. Quais dados podem ser reconstruídos de outra fonte (reduzem o RPO efetivo)?

Sem RPO/RTO aprovados, o plano é rascunho (Suposição) e a pendência fica no topo de "O que falta para concluir".

## 2. Mapa objetivo -> técnica (PostgreSQL e Redis; demais engines em `outras-engines.md`)

| Objetivo | Técnica compatível | Não atende |
| --- | --- | --- |
| RPO de horas a 1 dia, banco pequeno/médio | `pg_dump` periódico (V-14) | Qualquer RPO em minutos |
| RPO de minutos, recuperar até um instante | PITR: backup base + WAL arquivado (V-14) | `pg_dump` (não serve para PITR, V-14) |
| Alta disponibilidade (failover) | Réplica em espera (fora do escopo de backup; não substitui backup: replica também o erro) | Proteção contra `DROP`/corrupção lógica |
| Redis cache puro | Sem persistência ou RDB | — |
| Redis como armazenamento | RDB + AOF e cópia externa (V-27) | AOF sozinho (desencorajado, V-27) |

Réplica não é backup: um `DELETE` errado é replicado em segundos (conhecimento estável; Inferido).

## 3. Checklist de ensaio de restauração

Ambiente **isolado** (servidor/container/instância temporária), sem rota para produção e sem credenciais de produção.

- [ ] Origem do backup escolhida (último dump, backup base + WAL, snapshot) e registrada.
- [ ] Hash/tamanho do arquivo conferidos contra o registro do momento do backup.
- [ ] Banco/instância de ensaio criado de forma limpa (PostgreSQL: de `template0`, V-14).
- [ ] Restauração executada com parada em erro (`ON_ERROR_STOP`/`--exit-on-error`/`--single-transaction`, V-14).
- [ ] Tempo medido do início ao "pronto para uso" (compare com o RTO).
- [ ] `ANALYZE` executado (PostgreSQL, V-14).
- [ ] Verificação funcional (seção 4) concluída.
- [ ] Aplicação (ambiente de teste) conectada à cópia e smoke test passou.
- [ ] Alvo de PITR validado (dados do instante esperado presentes; dados posteriores ausentes).
- [ ] Ambiente de ensaio destruído ou protegido conforme retenção; dados pessoais tratados (seção 7).
- [ ] Registro do teste preenchido (seção 5) e divergências abertas como pendências.

## 4. Verificação funcional (exemplos para o usuário adaptar)

Contagens e invariantes por tabela, comparadas com valores esperados (de monitoramento ou de um relatório gerado antes do backup):

```sql
SELECT 'orders' AS tabela, count(*) AS linhas, max(created_at) AS ultimo_registro FROM orders
UNION ALL SELECT 'customers', count(*), max(created_at) FROM customers;

-- integridade referencial lógica
SELECT count(*) AS orfaos FROM order_items oi LEFT JOIN orders o ON o.id = oi.order_id WHERE o.id IS NULL;

-- invariantes de negócio
SELECT count(*) AS negativos FROM items WHERE stock < 0;

-- índices inválidos após restauração (PostgreSQL)
SELECT indexrelid::regclass FROM pg_index WHERE NOT indisvalid;
```

- Confira `max(created_at)` contra o instante esperado do backup (ou do alvo de PITR).
- Compare tamanho aproximado por tabela com o de produção (queda grande = restauração parcial).
- Exercite três consultas de negócio críticas e um fluxo de escrita no ambiente de teste.
- Redis: `DBSIZE`, amostra de chaves por prefixo, `TTL` de chaves de cache, `INFO persistence` (V-27, Inferido para a lista exata).

## 5. Registro do teste

| Campo | Exemplo (formato; sem dado real) |
| --- | --- |
| Data / executor | AAAA-MM-DD / nome ou papel |
| Engine, versão (origem e ensaio) | PostgreSQL 16.x / 16.x |
| Origem do backup (tipo, data, hash) | dump custom, AAAA-MM-DD 02:00, sha256 ... |
| Alvo (instante PITR, se houver) | AAAA-MM-DD HH:MM -03 |
| Tempo total até pronto | medido, em minutos |
| RTO acordado | em minutos |
| Resultado | passou / falhou / parcial |
| Divergências | lista, com dono e prazo |
| Ações corretivas | ajuste de script, de agenda, de capacidade |
| Próximo teste | data |

Regra: teste que excede o RTO reprova o plano e abre ação corretiva (capacidade, método, paralelismo com `-j`, outra técnica).

## 6. Resposta a incidente: ordem segura

1. **Conter**: parar escritas ou isolar o banco; avisar responsáveis.
2. **Preservar**: snapshot/cópia do estado atual antes de qualquer restauração (pode conter dados que o backup não tem).
3. **Diagnosticar**: é perda lógica (DELETE/DROP/migração errada), corrupção física ou indisponibilidade? Qual o instante provável do problema?
4. **Escolher a técnica**: PITR até antes do incidente; restauração de dump para extrair apenas as linhas perdidas e reinserir; failover (se for indisponibilidade).
5. **Restaurar em isolado**, verificar (seção 4).
6. **Decidir o corte** com quem tem autoridade; planejar reapontamento e comunicação.
7. **Depois**: pós-incidente sem culpa, ação corretiva (privilégios, backups fora da conta, teste periódico).
Ações destrutivas e o corte de produção são sempre executados pelo usuário.

## 7. Dados pessoais no ambiente de ensaio

Cópia de produção em ambiente de ensaio é dado pessoal em outro lugar (brain: logs e snapshots de teste precisam de minimização e retenção): restrinja o acesso, mascare ou anonimize quando o objetivo não exigir os valores reais, defina prazo de descarte e registre quem acessou. Dado sintético não deve copiar identificador real.
