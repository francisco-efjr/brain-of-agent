# Inventário e padrões de busca para revisão de isolamento

Uso: passo 2 de `tenant-isolation-review`. Os padrões são ponto de partida para a ferramenta Grep (ripgrep); cada resultado é um candidato, não um achado. Confirme lendo o trecho. Ajuste extensões ao stack. Conferido em 2026-10-10; padrões são conhecimento estável de ORMs e frameworks, não vêm de V-nn, exceto onde indicado.

Exclusões comuns em toda busca: `node_modules`, `vendor`, `dist`, `build`, `.next`, `.venv`, `__pycache__`, `coverage`, arquivos de lock.

## 1. Onde existe o conceito de tenant

| Objetivo | Padrão (regex) | O que ler |
| --- | --- | --- |
| Tabelas e modelos com tenant | `tenant_id\|tenantId\|organization_id\|org_id\|account_id` | schema, migrations, models; liste as tabelas que NÃO aparecem e decida se são globais, de ponte ou esquecidas |
| Tabelas de tenant sem coluna | listar todas as tabelas do schema e subtrair as acima | tabela de tenant sem `tenant_id` é o primeiro suspeito |
| Origem do tenant em rota | `req\.(body\|query\|params)\.(tenant\|org)\|headers\[.?x-tenant\|request\.(json\|args\|form)\[.?(tenant\|org)` | qualquer ocorrência fora de rota pública é achado em potencial (V-32) |
| Origem correta | `req\.(user\|auth\|session)\.(tenant\|org)\|claims\[.?(tenant\|org)\|current_tenant\|get_tenant` | confirme que vem de credencial validada, não de decodificação sem verificação (`jwt.decode` sem `verify`) |
| Decodificação sem validar | `jwt\.decode\(\|decode\(.*verify\s*=\s*False\|ignoreExpiration\|algorithms\s*=\s*\[?.?none` | token usado para tenant sem validar assinatura é crítico |

## 2. Camada de dados

| Objetivo | Padrão | O que ler |
| --- | --- | --- |
| Prisma sem escopo | `\.(findUnique\|findFirst\|findMany\|update\|updateMany\|delete\|deleteMany\|count\|aggregate\|groupBy)\(` | o `where` tem tenant? Há extensão `$extends` ou middleware que injeta? |
| SQL cru | `\$queryRaw\|\$executeRaw\|\.query\(\|\.execute\(\|text\(\|raw\(\|sequelize\.query\|knex\.raw` | tenant em cada `WHERE` e `JOIN`; parâmetros ligados, não concatenados |
| SQLAlchemy / Django / Rails | `session\.get\(\|\.query\(\|select\(\|objects\.(get\|filter\|all)\|\.find\(\|find_by\|default_scope\|unscoped` | `unscoped`, `all`, `Model.objects` sem manager de tenant; `default_scope` com `unscoped` em jobs |
| Concatenação em SQL | `"\s*\+\s*(tenant\|req\.)\|f".*\{(tenant\|req)\|\$\{.*tenant` dentro de strings SQL | injeção e quebra de escopo |
| Contexto de sessão do banco | `SET\s+(LOCAL\s+)?app\.\|set_config\(\|current_setting\(` | `SET` sem `LOCAL` é de sessão: achado com pool; `set_config(..., false)` também (V-34) |
| Roles e bypass | `BYPASSRLS\|SUPERUSER\|service_role\|admin_bypass\|SET\s+ROLE\|row_security` | role da aplicação, jobs e migração devem ser distintas (V-01, V-57) |
| RLS nas migrations | `ENABLE ROW LEVEL SECURITY\|FORCE ROW LEVEL SECURITY\|CREATE POLICY\|WITH CHECK` | compare a lista de tabelas com `tenant_id` contra as que têm `ENABLE` e `FORCE` e `WITH CHECK` |
| Transação | `\.transaction\(\|\$transaction\|BEGIN\|begin\(\)\|atomic\(` | leituras ficam dentro da transação que define o contexto? |

Quando houver banco acessível em homologação (e o usuário permitir consultas), as consultas de catálogo que fecham a dúvida de roles e RLS estão em `${CLAUDE_PLUGIN_ROOT}/skills/tenant-rls-migration/references/sql-passo-a-passo.md`, seção "Catálogo". Esta skill não executa nada: peça ao usuário que rode e cole a saída, e rotule como Verificado só depois.

## 3. Autorização e corpo da requisição

| Objetivo | Padrão | O que ler |
| --- | --- | --- |
| Mass assignment | `\.\.\.req\.body\|Object\.assign\(.*req\.body\|update\(\{?\s*data:\s*req\.body\|\*\*request\.(json\|data)\|params\.permit!\|fields\s*=\s*['"]__all__` | lista explícita de campos aceitos (V-12 AZ4) |
| Papel vindo do corpo | `isAdmin\|is_admin\|role\s*[:=]\s*req\.\|"role"\s*:` em handlers de criação e atualização | AZ5 |
| Rotas sem guard | listar rotas (`app\.(get\|post\|put\|patch\|delete)\|@(Get\|Post)\|router\.`) e cruzar com o middleware de auth | rota nova sem política explícita falha (AZ1) |
| Autorização só no cliente | condicionais de UI sem equivalente no servidor | AZ2 |
| Reautenticação | `change.?email\|delete.?account\|change.?role\|update.?role` | AZ6 |

## 4. Jobs, filas, cache, arquivos, tempo real

| Objetivo | Padrão | O que ler |
| --- | --- | --- |
| Jobs e filas | `queue\.add\|enqueue\|perform_async\|\.delay\(\|cron\|schedule\|@Scheduled\|worker` | o payload leva `tenant_id`? O worker abre transação por tenant? |
| Cache | `cache\.(get\|set)\|redis\.(get\|set\|setex\|hget)\|@Cacheable\|lru_cache\|memoize\|cache_key\|CacheKey` | a chave contém tenant (e permissão, quando a resposta varia)? Há namespace global explícito? (V-49) |
| URL assinada, download | `getSignedUrl\|presign\|generate_presigned_url\|createPresignedPost\|signed_url\|sendFile\|send_from_directory` | objeto e operação autorizados antes de assinar; vida curta (V-49) |
| Armazenamento | `bucket\|putObject\|upload\|multer\|storage\.` | prefixo com tenant; nome de arquivo do cliente não vira caminho |
| Busca e exportação | `search\|autocomplete\|export\|csv\|report` em rotas | cada uma passa pelo escopo; índice de busca com campo `tenant_id` obrigatório no filtro |
| Tempo real | `socket\.io\|ws\.on\|subscribe\|channel\|room` | sala/canal derivado do tenant do token, não de parâmetro do cliente |

## 5. Billing, logs e suporte

| Objetivo | Padrão | O que ler |
| --- | --- | --- |
| Webhook Stripe | `stripe-signature\|constructEvent\|construct_event\|express\.json\(\)\|bodyParser\.json` | corpo bruto antes do parser; `event.id` UNIQUE (V-03) |
| Estado de billing | `plan\s*=\|subscription_status\|tenant_features\|entitlement` | só o módulo de billing grava o status (V-21); nada muda por redirect de checkout |
| Logs com PII | `console\.log\(.*(body\|token\|password\|authorization)\|logger\.\w+\(.*(body\|headers\|token)` | V-41 |
| Fixtures com dado real | `seed\|fixture\|factory` e e-mails/CPF/CNPJ reais | V-18, V-22 |
| Suporte e impersonation | `impersonat\|act_as\|sudo\|support_access\|admin_override\|login_as` | motivo, escopo, prazo, `actor_id` real na trilha |

## 6. Como declarar a cobertura

No relatório, para cada família acima, escreva `buscado`, `sem ocorrências` ou `não buscado (motivo)`. Um padrão sem ocorrência não prova ausência (nomes diferentes, código gerado, outro idioma de ORM): diga "sem ocorrências pelo padrão X", não "não existe".
