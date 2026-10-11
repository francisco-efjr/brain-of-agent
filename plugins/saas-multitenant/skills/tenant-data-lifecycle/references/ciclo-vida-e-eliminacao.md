# Ciclo de vida do tenant, onboarding, exportação, eliminação, retenção e auditoria

Redação própria. Fontes: Azure tenant life cycle (V-30), LGPD (V-27), GDPR (V-28), checklist V-29, OWASP Logging (V-41), OWASP Multi-Tenant (V-49), V-38, V-59, V-60. Conferido em 2026-10-10. Não é orientação jurídica; prazos e cláusulas são decisão de produto e do jurídico. Rótulos: Verificado (lido na fonte), Inferido (nosso), Suposição, Não verificável.

## 1. Máquina de estados do tenant (design nosso, Inferido de V-30)

A página da Azure trata trial, onboarding, atualização, escala, movimentação, fusão e divisão, offboarding e desativação, e não traz prazos nem números. Desativação (por pedido ou por falta de pagamento) é temporária e pode virar offboarding.

| Estado | Entrada | Acesso | Dados | Dono | Evento de auditoria |
| --- | --- | --- | --- | --- | --- |
| `trial` | signup | completo, com limites do trial | mantidos | produto | `tenant.created` |
| `active` | conversão do trial ou pagamento confirmado | conforme plano | mantidos | produto | `tenant.activated` |
| `deactivated` | `unpaid` ou `paused`; pedido do tenant; abuso | bloqueado; admin vê aviso e pode regularizar | mantidos; nada é apagado | billing | `tenant.deactivated` com motivo |
| `offboarding` | cancelamento; prazo de graça esgotado | exportação disponível; sem uso do produto | mantidos até o fim da retenção | jurídico e produto | `tenant.offboarding_started` |
| `deleted` | fim da retenção e instrução do controlador | nenhum | eliminados (exceções legais anonimizadas ou retidas) | controlador (tenant) com execução do SaaS | `tenant.deleted` com evidência |

Transições permitidas: `trial` para `active`; `trial` para `deactivated` (expirou sem pagamento); `active` para `deactivated`; `deactivated` para `active` (regularização); `deactivated` para `offboarding`; `active` para `offboarding`; `offboarding` para `active` (reonboarding dentro da retenção; a Azure cita reonboarding); `offboarding` para `deleted`. Qualquer outra é rejeitada. Cada transição grava um evento com `actor_id` e motivo.

```sql
CREATE TABLE tenant_lifecycle (
  tenant_id   uuid PRIMARY KEY REFERENCES tenants (id),
  state       text NOT NULL CHECK (state IN ('trial', 'active', 'deactivated', 'offboarding', 'deleted')),
  state_since timestamptz NOT NULL DEFAULT now(),
  retention_until timestamptz,                 -- preenchido no offboarding conforme contrato (Suposição de prazo)
  reason      text
);
```

Perguntas de entrada do onboarding (V-30): residência de dados, compliance, RTO e RPO, plano de cobrança, ambiente de homologação. Trial: mesmos requisitos de segurança e SLA? Infraestrutura compartilhada? Como migra para tenant pago? Como evitar abuso? Quais limites?

## 2. Onboarding idempotente e retomável (acréscimo do crítico; ordem Inferida)

Sequência: (1) linha do tenant; (2) organização e membro dono; (3) Customer do provedor de billing com `metadata.tenant_id` (chave de idempotência `tenant-{id}-create-customer`, V-04, V-39); (4) `tenant_features` iniciais; (5) estado `trial` ou `active`; (6) evento de auditoria. Falha no meio não deixa tenant órfão nem Customer duplicado.

```sql
CREATE TABLE tenant_provisioning_steps (
  tenant_id       uuid NOT NULL,
  step            text NOT NULL,                          -- 'tenant_row', 'owner_membership', 'billing_customer', 'features', 'audit'
  status          text NOT NULL CHECK (status IN ('pending', 'done', 'failed')),
  idempotency_key text NOT NULL,
  attempts        integer NOT NULL DEFAULT 0,
  last_error      text,
  updated_at      timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (tenant_id, step)
);
```

Regra do runner: cada passo é idempotente (consulta antes, `INSERT ... ON CONFLICT DO NOTHING`, chamada externa com chave de idempotência derivada de `tenant + passo`); o runner retoma do primeiro passo `pending` ou `failed`; reexecutar o onboarding inteiro não cria duplicata. Teste: derrubar o processo depois de cada passo e reexecutar; contar tenants e Customers.

## 3. Exportação

| Requisito | Detalhe |
| --- | --- |
| Escopo | o `tenant_id` do token validado, nunca do corpo ou da query (V-29) |
| Formato | JSON ou CSV legível por máquina; esquema documentado |
| Conteúdo | dados do tenant e dos titulares; para portabilidade (GDPR art. 20), dados fornecidos pelo titular; dados derivados são decisão do jurídico (V-28) |
| Entrega | arquivo gerado em job, em storage com prefixo do tenant, URL assinada de vida curta, só após autorizar objeto e operação (V-49) |
| Auditoria | `export.requested`, `export.completed`, `export.downloaded` com `tenant_id` e `actor_id` |
| Base legal | LGPD art. 18, II (acesso) e V (portabilidade a outro fornecedor, mediante requisição expressa); GDPR art. 20 |
| Teste | exportação do tenant A não contém linha do B; export completo contra contagens por tabela |

## 4. Eliminação (job para revisão; não executa)

Entrada: instrução do controlador (o tenant), registrada, com o escopo (tenant inteiro ou titular específico). O SaaS operador executa a instrução (LGPD art. 39) sob as exceções do art. 16: obrigação legal ou regulatória, pesquisa com anonimização quando possível, transferência a terceiro dentro da lei, uso exclusivo do controlador anonimizado. GDPR art. 17(3) lista exceções próprias (V-27, V-28).

```sql
CREATE TABLE deletion_requests (
  id           uuid PRIMARY KEY,
  tenant_id    uuid NOT NULL,
  scope        text NOT NULL CHECK (scope IN ('tenant', 'data_subject')),
  subject_ref  text,                                -- identificador interno do titular, sem PII em claro
  requested_by uuid NOT NULL,                       -- instrução do controlador
  approved_by  uuid,                                -- autorização concreta antes de executar
  state        text NOT NULL CHECK (state IN ('requested', 'approved', 'running', 'completed', 'failed')),
  created_at   timestamptz NOT NULL DEFAULT now(),
  completed_at timestamptz
);

CREATE TABLE deletion_steps (
  request_id uuid NOT NULL REFERENCES deletion_requests (id),
  store      text NOT NULL,                         -- 'postgres', 'object_storage', 'cache', 'search_index', 'warehouse', 'processors'
  status     text NOT NULL CHECK (status IN ('pending', 'done', 'failed', 'not_applicable')),
  evidence   jsonb NOT NULL DEFAULT '{}',           -- contagens antes e depois, identificadores de lote; sem PII
  updated_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (request_id, store)
);
```

Ordem e cuidados por armazenamento:

| Armazenamento | Como | Verificação |
| --- | --- | --- |
| Banco | descobrir as tabelas com `tenant_id` pelo catálogo (consulta 5 de `tenant-rls-migration/references/sql-passo-a-passo.md`) e apagar em lotes, filhos antes dos pais, com contexto do tenant ou role de manutenção controlada (com RLS `FORCE`, a dona não enxerga linhas) | contagem por tabela antes e depois; zero linhas com o `tenant_id` |
| Storage de objetos | listar o prefixo `tenants/{tenant_id}/` e apagar; com versionamento ligado, apagar também versões e marcadores | listagem do prefixo vazia, incluindo versões |
| Cache | remover chaves com o prefixo do tenant usando iteração incremental, nunca varredura bloqueante | busca por prefixo vazia |
| Índice de busca | apagar por consulta `tenant_id` | contagem por filtro zero |
| Warehouse e BI | apagar ou anonimizar conforme a política; anotar o atraso de propagação | contagem por filtro |
| Réplicas | a eliminação replica; confirmar o atraso | consulta na réplica |
| Processadores (e-mail, suporte, analytics, billing) | notificar ou chamar a API de eliminação de cada um; manter lista com estado | tabela de processadores com estado e data |
| Backups | não se apaga linha em backup: definir expiração (prazo é decisão de produto), informar o tenant | política escrita e comunicada |
| Provedor de billing | registros financeiros e fiscais podem ter retenção legal (art. 16, I): retenha o mínimo e anonimize o que puder; decisão do jurídico (Suposição) | decisão registrada |

Registro de eliminações (tombstone) sem PII: `tenant_id` eliminado e data. Após restaurar um backup, reaplique a lista para que um tenant eliminado não reapareça (conhecimento estável; Inferido).

Evidência de conclusão: certificado interno com identificador do pedido, datas, contagens por loja, lista de processadores e o prazo de expiração dos backups; sem PII. O job exige `approved_by` antes de rodar e roda primeiro em homologação com dados sintéticos.

## 5. Retenção (tabela para o produto e o jurídico)

| Tipo de dado | Finalidade | Base | Prazo | Gatilho do prazo | Exceção legal | Dono | Rótulo |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Dados de conteúdo do tenant | prestar o serviço | contrato | [definir] | fim do contrato | LGPD art. 16 | produto e jurídico | Suposição |
| Dados de conta e usuários | autenticação | contrato | [definir] | fim do contrato | idem | produto | Suposição |
| Registros fiscais e de cobrança | obrigação legal | lei | [definir pelo jurídico] | emissão | art. 16, I | financeiro | Suposição |
| Trilha de auditoria | segurança | interesse legítimo ou lei | [definir] | evento | idem | segurança | Suposição |
| Registro de incidentes | obrigação regulatória | lei | no mínimo 5 anos segundo fonte secundária (V-61) | encerramento | idem | segurança | Verificado em fonte secundária |
| Backups | continuidade | interesse legítimo | [definir] | criação do backup | idem | infra | Suposição |

Prazos são decisão de produto e do jurídico (V-29, Suposição). O plugin não sugere números.

## 6. Trilha de auditoria por tenant (V-41; campos nossos, Suposição)

```sql
CREATE TABLE audit_events (
  id            bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  tenant_id     uuid NOT NULL,
  actor_id      uuid,                                  -- pessoa; ação do suporte usa o ator real
  actor_type    text NOT NULL CHECK (actor_type IN ('user', 'api_key', 'scim', 'system', 'support')),
  action        text NOT NULL,                         -- 'invite.created', 'member.deactivated', 'export.completed', ...
  resource_type text,
  resource_id   text,
  result        text NOT NULL CHECK (result IN ('success', 'denied', 'error')),
  occurred_at   timestamptz NOT NULL DEFAULT now(),    -- UTC
  origin        text,                                  -- origem truncada ou hash; IP completo pode ser dado pessoal
  details       jsonb NOT NULL DEFAULT '{}'            -- sem corpo de requisição, token, senha ou PII
);
CREATE INDEX audit_events_tenant_time_idx ON audit_events (tenant_id, occurred_at DESC);
-- Somente inserção para a aplicação (imutabilidade prática; detecção de adulteração é decisão adicional):
REVOKE UPDATE, DELETE, TRUNCATE ON audit_events FROM app_runtime;
```

Eventos obrigatórios por tenant (V-41): convite, mudança de papel, exportação, desativação, chave de API criada ou revogada, login SSO, ação do suporte do SaaS no tenant; mais mudanças de estado do tenant e pedidos de eliminação. Acesso a dado sensível, importação e exportação, upload, uso de chaves e mudanças de configuração entram também (OWASP Logging). Integridade segundo o OWASP: detecção de adulteração, mídia somente leitura, acesso aos logs monitorado e restrito, TLS no transporte, sanitizar CR e LF, falha de log não derruba a aplicação; separar logs de segurança, de operação e de auditoria.

Lacuna declarada: visibilidade da trilha ao administrador do cliente, retenção visível e imutabilidade não têm fonte; propostas ficam como Suposição. Proposta: tela ou API somente leitura, por tenant, com filtro por período, exportável, com retenção igual à do contrato.

Cuidado: a trilha contém `tenant_id` e `actor_id`; ela própria entra na eliminação do tenant (ou é anonimizada) conforme a política; registro de incidente tem retenção própria.

## 7. NFS-e e parâmetros regulatórios (Brasil, quando aplicável)

| Parâmetro | Valor | Fonte | Verificado em | Rótulo |
| --- | --- | --- | --- | --- |
| `nfse_nacional_obrigatoria_simples_efeitos_desde` | 2026-11-01 | Resolução CGSN nº 191/2026 (cópia no portal da SEEC-DF; não é o DOU) | 2026-10-10 | Verificado em cópia |
| `ibs_cbs_simples_efeitos_desde` | 2027-01-01 | fonte secundária (Fenacon, citando ato conjunto RFB/CGIBS) | 2026-10-10 | Não verificável em norma |
| Documentação técnica da NFS-e | https://www.gov.br/nfse/pt-br | portal oficial (estrutura lida) | 2026-10-10 | Verificado (estrutura) |

Esses valores moram em configuração com fonte e data de verificação; uma mudança de resolução não exige deploy de código. Checklist (V-59, Inferido): quem é o prestador (tenant ou SaaS); homologação ou produção restrita antes da produção; certificado do prestador no cofre, nunca em texto puro no banco; nota gravada com `tenant_id` e identificador de envio único (idempotência de emissão). Credenciamento de integrador e emissão por terceiro: Não verificáveis.

## 8. Esqueleto de DPA (somente estrutura; texto é jurídico)

GDPR art. 28(3) (V-28, Verificado na cópia): tratamento só por instruções documentadas do controlador; confidencialidade das pessoas autorizadas; medidas de segurança (art. 32); condições para subcontratação; auxílio ao controlador nos direitos do titular; auxílio nos arts. 32 a 36; eliminar ou devolver os dados ao fim, por escolha do controlador, e apagar as cópias salvo obrigação legal; disponibilizar informação para auditorias; avisar se uma instrução parecer violar a lei. Acrescente os prazos contratuais de aviso de incidente (SaaS para tenant) e o prazo de expiração de backups.
