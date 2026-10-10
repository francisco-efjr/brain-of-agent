# NoSQL: MongoDB, DynamoDB e Redis

Sumário: 1 Regra de entrada · 2 MongoDB · 3 DynamoDB · 4 Redis · 5 Escolher a engine · 6 Gotchas · 7 Lacunas

## 1. Regra de entrada: perguntas antes do schema

"Não desenhe o schema antes de saber as perguntas" (DynamoDB, V-26) vale para os três. Preencha `ficha-de-padroes-de-acesso.md` (consulta, frequência, latência-alvo, cardinalidade, crescimento, consistência, retenção). Sem a ficha, pare e pergunte, uma pergunta por vez. Modelo NoSQL desenhado como se fosse relacional tende a reproduzir joins caros ou documentos ilimitados.

## 2. MongoDB (V-25)

Embutir ou referenciar:

| Critério | Embutir | Referenciar |
| --- | --- | --- |
| Relação | "contém" (endereços dentro do cliente) | existe sozinho (produto, usuário) |
| Leitura | consultado junto | consultado separado ou por vários pais |
| Cardinalidade | baixa, limitada | alta |
| Crescimento | limitado | sem limite (comentários de um post) |
| Duplicação | classifique pela sensibilidade a obsolescência: imutável, temporal, sensível, tolerante | evita duplicar dado sensível a obsolescência |

- Documentos maiores usam mais RAM no conjunto de trabalho. Limite de 16 MB por documento como "hard limit" (fonte: SKILL.md `mongodb-schema-design`; a página de embed vs reference não o cita).
- Antipadrões (SKILL.md, Apache-2.0, redação própria aqui): coleções demais, `$lookup` excessivo, índices desnecessários.
- Fluxo seguro com agente: descobrir ambiente, tipo de carga (`db.serverStatus().opcounters`), fontes, só então analisar; sem escrita sem "yes" explícito do usuário; cliente em modo somente leitura (`--readOnly` citado pelo SKILL.md; nome do pacote do servidor MCP: Não verificado).
- Exemplo: post com comentários. Comentários ilimitados dentro do post ultrapassam 16 MB e inflam toda leitura do post. Coleção `comments { post_id, created_at, ... }` com índice `(post_id, created_at)` e, se a tela mostra os 3 últimos, duplique-os no post (dado tolerante a obsolescência).
- Lacunas (L-07): índices e regra ESR, agregação, transações, sharding, backup. Diga "sem fonte validada".

## 3. DynamoDB (V-26)

- Levantar tamanho, forma e velocidade dos dados; usar "o menor número possível de tabelas" (exceções: séries temporais de alto volume e acessos muito diferentes); manter dados relacionados juntos; usar a ordenação da sort key; distribuir tráfego com chaves de alta cardinalidade; GSIs para consultas extras; NoSQL Workbench para modelar.
- Exemplo (Inferido, ilustrativo): pedidos de e-commerce. Perguntas: pedidos de um cliente por data; pedido por id; pedidos por status na última hora. Modelo: `PK = CUSTOMER#<id>`, `SK = ORDER#<timestamp>#<orderId>` atende a primeira; `GSI1PK = ORDER#<orderId>` a segunda; a terceira com `status` como chave tem baixa cardinalidade (hot partition): prefixe com um fragmento (`STATUS#open#<0..N>`) e consulte os N fragmentos. Cada escolha ligada a uma pergunta; sem pergunta, sem chave.
- Lacuna L-07 (Não verificado): capacidade e throughput, GSI/LSI em detalhe, transações, single-table design em detalhe. Não invente números de capacidade.

## 4. Redis (V-27, V-28)

Estrutura pelo padrão de acesso: String, Hash, List, Set, Sorted Set, JSON, Stream, Vector Set. Evitar objeto plano serializado numa String quando se lê campo a campo (Hash). Chave `entidade:id:atributo` em minúsculas, curta, sem URL inteira, com prefixo de tenant. Defina TTL conscientemente: chave de cache sem TTL vira vazamento de memória (Inferido).

Persistência (Verificado V-27):

| Opção | Perda possível | Observação |
| --- | --- | --- |
| RDB (snapshot) | últimos minutos | compacto, `fork`; copiar o RDB é seguro com o servidor rodando |
| AOF `appendfsync everysec` | até ~1 s | AOF sozinho é desencorajado |
| RDB + AOF | mínima | durabilidade comparável ao PostgreSQL, segundo a doc |

- Copiar AOF no Redis 7.0 ou superior: desligar a reescrita automática antes (`auto-aof-rewrite-percentage 0`) e conferir `aof_rewrite_in_progress`.
- Trocar RDB por AOF em servidor vivo: `CONFIG SET` e atualizar o `redis.conf`; apenas reiniciar não basta.
- Enviar cópia para fora da máquina ao menos uma vez por dia, verificar tamanho e SHA1, ter alerta independente. A família de comandos `BACKUP` existe a partir do Redis 8.10.0 (conforme a página; confira a versão).
- Cache x fonte de verdade: se perder o Redis é aceitável, RDB basta; se não, o dado precisa estar também num banco durável. Eviction, cluster e ACL: sem fonte lida (L-07).

## 5. Escolher a engine (resumo; árvore completa em `decisoes-e-tradeoffs.md`)

Relacional quando há invariantes entre entidades, consultas ad hoc e transações multi-linha. Documento quando o agregado é lido e escrito inteiro e o schema varia. Chave-valor/DynamoDB quando os padrões de acesso são poucos, conhecidos e de altíssima escala. Redis como cache, fila leve, contadores, ranking. Bancos vetoriais para RAG: `/llm-ai-agents:playbook`.

## 6. Gotchas

- Replicar o schema relacional em várias tabelas DynamoDB sem justificativa.
- Documento que cresce sem limite; `$lookup` em todo request.
- Sorted Set com milhões de membros lidos inteiros; chaves sem prefixo de tenant.
- Redis como "banco principal" sem política de persistência e backup.
- Escrever em Mongo/Redis em nome do usuário sem confirmação explícita.

## 7. Lacunas

MongoDB: índices, agregação, sharding, backup. DynamoDB: capacidade, transações, GSI/LSI. Redis: eviction, cluster, ACL (`redis/agent-skills` tem `redis-security` e `redis-clustering` não lidos). Declare "sem fonte validada" nessas áreas.
