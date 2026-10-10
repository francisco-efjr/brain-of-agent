# Multi-tenant e Row-Level Security

Sumário: 1 Ordem de decisão · 2 Matriz de tenancy · 3 Antipadrões · 4 Banco compartilhado: regras de schema · 5 RLS no PostgreSQL · 6 SQL de referência · 7 Teste de dois tenants · 8 Vazamentos fora da consulta · 9 Fronteiras · 10 Lacunas

Escolha o modelo de tenancy primeiro e trate RLS como defesa em profundidade com custo, não como o modelo (V-33: "muitas soluções multi-tenant não usam RLS" pela complexidade de propagar identidade). Registre a decisão em `adr-de-dados.md`.

## 1. Ordem de decisão

1. Requisitos: número de tenants, tamanho, variação de carga (noisy neighbor), isolamento exigido (chaves próprias, backup e região por tenant), custo, compliance.
2. Escolha na matriz (seção 2).
3. Se banco compartilhado no PostgreSQL: decida se RLS entra e quem o configura (pool, ORM, transação).
4. Teste de dois tenants antes de chamar de seguro (seção 7).

## 2. Matriz de tenancy (V-33, redação própria; fonte orientada a Azure)

| Modelo | Escala | Isolamento | Ruído entre tenants | Complexidade operacional | Custo por tenant |
| --- | --- | --- | --- | --- | --- |
| Banco/schema compartilhado com `tenant_id` | muito alta | lógico (código e/ou RLS) | alto risco | baixa a média | mais baixo |
| Sharding (grupos de tenants por banco) | alta | lógico + físico por grupo | médio | alta (roteamento, rebalanceamento) | médio |
| Banco por tenant | limitada pelo número de bancos | forte (chaves, backup, região próprios) | baixo | alta (migrar N bancos) | alto |
| Stamps (implantações completas) | muito alta | forte | baixo | muito alta | alto |

Compare por: escala, previsibilidade de desempenho, isolamento, complexidade e custo.

## 3. Antipadrões relacionais (V-33)

Tabela por tenant; coluna por tenant; mudança manual de schema por tenant; depender de uma única versão do schema (mantenha compatibilidade com pelo menos uma versão anterior durante migrações). Banco por tenant exige automação de migração e inventário de versões (Inferido).

## 4. Banco compartilhado: regras de schema (Inferido, convenções estáveis)

- `tenant_id NOT NULL` em toda tabela com dado de tenant, com FK para `tenants`.
- Índices compostos começando por `tenant_id`; UNIQUE que inclui `tenant_id` quando a unicidade é por tenant.
- Chaves estrangeiras entre tabelas de tenant devem incluir `tenant_id` para impedir referência cruzada: `FOREIGN KEY (tenant_id, order_id) REFERENCES orders (tenant_id, id)` com UNIQUE `(tenant_id, id)` no pai.
- Índices nas colunas usadas pelas políticas (V-12).
- Backups, exportações, materialized views e relatórios não podem misturar tenants.

## 5. RLS no PostgreSQL (V-12, Verificado na doc)

- RLS ligado sem política nega tudo. `USING` filtra linhas existentes; `WITH CHECK` valida linhas escritas; `USING` sozinho vale como `WITH CHECK`.
- Políticas permissivas combinam por OR; restritivas por AND.
- Superusuário e `BYPASSRLS` ignoram sempre. O dono da tabela ignora salvo `FORCE ROW LEVEL SECURITY`.
- Unicidade e FK ignoram RLS: canal de vazamento de existência.
- `row_security = off` gera erro quando a consulta seria filtrada.
- Subconsulta em política pode ter condição de corrida em READ COMMITTED (mitigar com `FOR SHARE`, função `SECURITY DEFINER` ou lock).
- `TRUNCATE` e `REFERENCES` não são cobertos por RLS.
- Do checklist de apoio (classe C, redação própria): aplicação com role sem superusuário nem BYPASSRLS; testes com essa role; contexto de tenant por transação; views com `security_invoker` (PG ≥ 15); `SECURITY DEFINER` com `search_path` fixo.

## 6. SQL de referência (PostgreSQL ≥ 15; adapte e teste)

```sql
-- role da aplicação: sem superusuário e sem BYPASSRLS (NOBYPASSRLS é o padrão)
CREATE ROLE app_user LOGIN NOSUPERUSER NOBYPASSRLS;   -- defina a senha fora do repositório

ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;
ALTER TABLE invoices FORCE ROW LEVEL SECURITY;        -- dono também é filtrado

CREATE POLICY tenant_isolation ON invoices
  USING      (tenant_id = current_setting('app.tenant_id', true)::bigint)
  WITH CHECK (tenant_id = current_setting('app.tenant_id', true)::bigint);
-- current_setting(..., true) devolve NULL se ausente: nenhuma linha passa (falha segura)

-- uso por transação (aceita parâmetro; equivale a SET LOCAL)
BEGIN;
SELECT set_config('app.tenant_id', $1, true);         -- true = vale só nesta transação
-- consultas da requisição
COMMIT;

CREATE VIEW invoice_summary WITH (security_invoker = true) AS
  SELECT tenant_id, count(*) AS n FROM invoices GROUP BY tenant_id;
```

`SET app.tenant_id = $1` e `SET LOCAL x = ?` não aceitam parâmetro; `SET` simples em conexão de pool no modo transaction vaza o tenant para outro cliente (Verificado V-18, V-35 para o problema do pool; Artefato G para `set_config`). Funções `SECURITY DEFINER`: `SET search_path = pg_catalog, public` na definição e sem receber o id do usuário como parâmetro livre.

## 7. Teste de dois tenants (entregue ao usuário para rodar com a role real)

```sql
-- como app_user
BEGIN; SELECT set_config('app.tenant_id','1',true);
  INSERT INTO invoices(tenant_id, total) VALUES (1, 10);        -- deve passar
  INSERT INTO invoices(tenant_id, total) VALUES (2, 10);        -- deve FALHAR (WITH CHECK)
  SELECT count(*) FROM invoices WHERE tenant_id = 2;            -- deve ser 0
  UPDATE invoices SET tenant_id = 2 WHERE tenant_id = 1;        -- deve FALHAR (não move linha)
ROLLBACK;
-- sem set_config: SELECT count(*) FROM invoices;               -- deve ser 0
```

Critério: cada linha tem resultado esperado escrito; "seguro" só após rodar com a role de produção da aplicação. Cobrir também leitura cruzada via JOIN, via view e via função.

## 8. Vazamentos fora da consulta

UNIQUE e FK revelam existência; mensagens de erro com valores; índices parciais e estatísticas; materialized views e exportações; logs e backups; cache compartilhado sem prefixo de tenant (Redis: prefixo de tenant na chave, V-28); filas e jobs sem contexto de tenant.

## 9. Fronteiras

Billing, entitlements, SSO/RBAC e ciclo de vida do tenant (exclusão, LGPD) → `/saas-multitenant:playbook`. Autorização por objeto na aplicação → `/security-appsec:playbook`. Aqui fica o isolamento no dado.

## 10. Lacunas

RLS em outras engines (SQL Server tem recurso próprio; sem fonte), sharding fora do PG (L-09), desempenho de RLS em escala (Suposição: meça).
