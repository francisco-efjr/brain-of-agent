# Organizações, domínio verificado, convites, estados de membro e JIT

Redação própria. Fontes: Clerk, Auth0 e WorkOS (V-31, fornecedores comerciais, viés), Entra e Okta (V-36), Braze (V-56, regras de fornecedor), OWASP Multi-Tenant (V-49). Conferido em 2026-10-10. Rótulos: Verificado (lido na página), Inferido (nosso), Não verificável.

## 1. Modelo de dados mínimo (Inferido)

```sql
CREATE TABLE verified_domains (
  domain       text PRIMARY KEY,                     -- um domínio verificado pertence a um único tenant
  tenant_id    uuid NOT NULL REFERENCES tenants (id),
  token_hash   text NOT NULL,                        -- hash do valor publicado no TXT
  verified_at  timestamptz,
  last_checked_at timestamptz
);

CREATE TABLE sso_connections (
  id           uuid PRIMARY KEY,
  tenant_id    uuid NOT NULL REFERENCES tenants (id),
  protocol     text NOT NULL CHECK (protocol IN ('saml', 'oidc')),
  issuer       text NOT NULL,                        -- EntityID do IdP ou iss do OIDC
  client_id    text,                                 -- OIDC
  status       text NOT NULL CHECK (status IN ('draft', 'active', 'disabled')),
  UNIQUE (issuer, client_id)
);

CREATE TABLE memberships (
  tenant_id    uuid NOT NULL REFERENCES tenants (id),
  user_id      uuid NOT NULL,
  role         text NOT NULL,
  status       text NOT NULL CHECK (status IN ('invited', 'active', 'inactive', 'deleted')),
  source       text NOT NULL CHECK (source IN ('invite', 'sso_jit', 'scim', 'manual')),
  PRIMARY KEY (tenant_id, user_id)
);

CREATE TABLE external_identities (
  tenant_id    uuid NOT NULL,
  connection_id uuid NOT NULL REFERENCES sso_connections (id),
  subject      text NOT NULL,                        -- sub do OIDC ou NameID persistente
  user_id      uuid NOT NULL,
  PRIMARY KEY (connection_id, subject)
);

CREATE TABLE invites (
  id           uuid PRIMARY KEY,
  tenant_id    uuid NOT NULL REFERENCES tenants (id),
  email_lower  text NOT NULL,
  role         text NOT NULL,
  token_hash   text NOT NULL UNIQUE,                 -- o token vai por e-mail; só o hash fica no banco
  expires_at   timestamptz NOT NULL,
  used_at      timestamptz,
  created_by   uuid NOT NULL
);
```

Tabelas de resolução de identidade (domínio, conexão, convite por token) são lidas antes de existir contexto de tenant: classifique-as como "ponte" na migração de RLS (skill `tenant-rls-migration`).

## 2. Verificação de domínio

Fonte da prática: a Entra prova domínio com registro TXT ou MX; TTL de 3600 s; propagação de instantânea a dias (não "horas"); um domínio só verifica em um diretório (V-36, Verificado). O desenho abaixo é nosso (Inferido):

1. O admin do tenant informa o domínio. O sistema gera um valor aleatório e mostra o registro `TXT` a publicar; guarda só o hash.
2. Verificação por consulta DNS ao pedido do admin e por tentativas espaçadas; a propagação pode levar de instantes a dias, então o estado "pendente" é normal.
3. Ao verificar, o sistema grava `verified_at`. A restrição `PRIMARY KEY (domain)` impede que dois tenants verifiquem o mesmo domínio; conflito vai para o suporte com prova.
4. Reverificação periódica; se o registro sumir, o domínio vira `verified_at = NULL` e SSO e JIT desse domínio param até nova prova (domínio abandonado e revendido é risco de tomada de conta).
5. SSO e JIT só valem para e-mails em domínio verificado do próprio tenant. Convite independe do domínio (WorkOS, V-31).

## 3. Estados de membro (V-31)

```text
invited -> active -> inactive -> deleted
              ^----------|   (reativar)
```

| Transição | Efeito |
| --- | --- |
| convite aceito | `invited` para `active`; papel do convite |
| desativar (SCIM `active=false` ou admin) | `active` para `inactive`: sessões revogadas, papel mantido, reativável (WorkOS) |
| reativar | `inactive` para `active` com o papel anterior |
| excluir | só quando o registro não é mais necessário; membro `pending` (convite não aceito) só pode ser excluído; havendo dados históricos referenciando o membro, prefira desativar (WorkOS) |

Cada transição tem dono e evento de auditoria (V-30, V-41).

## 4. Organização ativa por requisição (V-31, Verificado em Clerk; regra do plugin Inferida)

O Clerk mantém a organização ativa por aba do navegador e o cookie de sessão reflete só a aba mais recente, então requisições de fundo devem enviar o token no cabeçalho `Authorization`. Regra do plugin: o servidor resolve a organização ativa a cada requisição a partir de credencial validada (token com claim de organização conferido contra os vínculos ao vivo) e nunca confia só em cookie nem em seletor de organização vindo do cliente. Vínculos são verificados ao vivo, não por token antigo (V-25). Teste: usuário em dois tenants abre duas abas com tenants diferentes e faz operações em fundo; cada operação vai para o tenant da aba que a originou.

## 5. Convites

- Token aleatório de uso único, enviado por e-mail, hash no banco, expiração curta, vinculado ao e-mail (sem diferenciar caixa) e ao tenant.
- Convite expirado ou já usado: recusado; mensagem não revela se o e-mail existe em outro tenant.
- Convidado já pertence a outro tenant: cria vínculo adicional, com troca de contexto clara (V-23).
- Convite conta como assento conforme a decisão do spec (skill `saas-feature-spec`).
- Papel do convite vem do admin que convida, limitado ao próprio papel (ninguém convida para papel acima do seu); papel do corpo do aceite é ignorado (V-12 AZ5).

## 6. JIT (V-56: regras de fornecedor; derivadas Inferidas)

Verificado no Braze: o domínio de e-mail precisa já existir na empresa com ao menos um desenvolvedor confirmado; só vale para login iniciado pelo IdP; a asserção precisa de atributo `email` válido e igual ao do login; todos os criados recebem o mesmo workspace e permission set padrão; não atualiza permissões de usuário existente; desligar exige o suporte do fornecedor; incompatível com login Google. Isso é comportamento de um fornecedor, não padrão de IdP.

Regras do plugin (Inferido):
1. JIT só para e-mail em domínio verificado (V-31 WorkOS) e só se o admin do tenant ativou.
2. Cria com o papel mínimo, nunca elevado por atributo do IdP sem aprovação.
3. Não ligar JIT junto com SCIM ativo para o mesmo tenant (resumos de Harness e Workato não foram lidos).
4. Auditar `member.created` com `source = 'sso_jit'`.
5. JIT em Okta e Entra: lacuna, Não verificável.

## 7. Testes

| Teste | Esperado |
| --- | --- |
| domínio não verificado tenta SSO | recusado |
| dois tenants tentam verificar o mesmo domínio | o segundo é recusado |
| registro TXT removido | SSO e JIT do domínio suspensos após reverificação |
| primeiro login SSO | cria membro com papel padrão e auditoria |
| usuário removido no IdP | perde acesso (SCIM `active=false` ou fim do login) |
| convite reutilizado ou expirado | recusado |
| convite com papel acima do convidante | recusado |
| usuário em dois tenants, duas abas | cada requisição no tenant correto |
| membro desativado | sessões revogadas; papel mantido; reativar restaura |
