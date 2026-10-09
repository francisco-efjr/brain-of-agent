# Dados, transações, migrações e recuperação

## Descobrir a verdade persistida

Inventariar engine/versão, tabelas, índices, constraints, cardinalidade, volume, retenção, proprietários, backups e consumidores. Observar consultas e planos antes de sugerir índice. Um banco local vazio não reproduz lock, duração ou distribuição de produção.

Definir invariantes no local apropriado. Unicidade de operação, chave estrangeira e restrição de domínio podem proteger além do ORM. Não deduzir isolamento pelo nome “transação”: engine e nível alteram garantias.

A documentação PostgreSQL explica anomalias e diferença entre níveis; SERIALIZABLE pode abortar operações e requer tratamento de retry. Estas propriedades não devem ser extrapoladas para outra engine. [Fonte: PostgreSQL Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html).

## Concorrência com exemplo

Antes: ler estoque=1; duas requisições passam na validação; ambas vendem uma unidade. Depois proposto: atualizar condicionalmente `estoque = estoque - quantidade` apenas quando há saldo suficiente, dentro da mesma unidade transacional da reserva; verificar quantidade de linhas afetadas. Outra opção é lock apropriado ou controle otimista por versão. Escolher com base em contenção e regras.

Teste: iniciar duas vendas coordenadas, confirmar no máximo uma aceitação, estoque não negativo, reserva consistente e erro tratável. Não usar apenas duas chamadas sequenciais para afirmar concorrência.

## Expandir, migrar, contrair

Para trocar `nome` por `nome_completo`: adicionar estrutura compatível; implantar leitura/escrita compatível com versões coexistentes; preencher dados em lotes observáveis e reiniciáveis; verificar contagens e valores; mudar leitores; remover campo antigo apenas após janela e consumidores confirmados. Dual-write sem atomicidade precisa de reconciliação.

Consultar locks e reescritas da operação na engine/versão. ALTER TABLE não tem custo uniforme. [Fonte: PostgreSQL ALTER TABLE](https://www.postgresql.org/docs/current/sql-altertable.html).

Definir interrupção: duração/lock acima de orçamento, crescimento inesperado de erro, divergência entre campos ou esgotamento de capacidade. Backfill deve ter checkpoint e operação idempotente; não recomeçar milhões de registros sem necessidade.

## Rollback e recuperação

Rollback de aplicação não desfaz automaticamente schema ou dado transformado. Distinguir reversão de código, compatibilidade de versões e restauração de dados. Remoção de coluna ou conversão com perda pode exigir backup e plano de restauração, não simples migration down.

Definir RPO/RTO com responsável do produto, testar restauração em ambiente isolado e verificar consistência funcional. “Backup existe” não prova que a restauração cabe no prazo. Nunca testar restaurando por cima de banco ativo.

## Qualidade e privacidade

Para importação: validar encoding, separador, tamanho, duplicatas, formato e erros por linha; não aceitar parcialmente sem contrato explícito. Dado sintético não deve copiar identificador real. Logs e snapshots de teste precisam de minimização e retenção.

## Checklist

- [ ] Schema, consumidores, volume e versão observados.
- [ ] Constraints e precisão refletem invariantes de negócio.
- [ ] Concorrência testada com coordenação e transação efetiva.
- [ ] Plano/query analisado em dados representativos, sem exposição.
- [ ] Migração suporta versões coexistentes e lote retomável.
- [ ] Locks, espaço, duração e interrupção possuem critério definido.
- [ ] Backup e restauração validados em ambiente permitido.
- [ ] Rollback documenta perda potencial e compatibilidade.
- [ ] Dados pós-migração comparados por contagem e invariantes.

Falhas comuns: índice por intuição; migração apenas no startup de todas as réplicas; transação longa de backfill; dinheiro em ponto flutuante sem regra; horário local sem contexto; declarar “sem downtime” por execução local rápida.

Fontes consultadas em 2026-10-09. SQL conceitual deve ser adaptado e testado na engine do projeto.
