# Autorização por tenant e contexto de tenant na aplicação

Escopo: como a requisição vira tenant, como o objeto é autorizado, onde o contexto vive (middleware, repositório, jobs, cache, arquivos, websockets), acesso de suporte e restauração. Itens `V-nn` em `fontes.md`. Rótulos: Verificado = lido na fonte pelo validador do segmento; Inferido = conhecimento estável ou derivação nossa; Suposição = hipótese a confirmar.

## Sumário

- [1. Mapear requisição para tenant](#1-mapear-requisição-para-tenant)
- [2. Autorização do objeto](#2-autorização-do-objeto)
- [3. 404 ou 403](#3-404-ou-403)
- [4. Esqueleto de contexto em mecanismo compartilhado](#4-esqueleto-de-contexto-em-mecanismo-compartilhado)
- [5. Jobs, workers e filas](#5-jobs-workers-e-filas)
- [6. Cache, busca, arquivos e websockets](#6-cache-busca-arquivos-e-websockets)
- [7. Papéis: RBAC, ABAC, ReBAC](#7-papéis-rbac-abac-rebac)
- [8. Organização ativa e multi-aba](#8-organização-ativa-e-multi-aba)
- [9. Acesso de suporte e impersonation](#9-acesso-de-suporte-e-impersonation)
- [10. Restauração de um tenant e alerta cruzado](#10-restauração-de-um-tenant-e-alerta-cruzado)
- [11. Limites por tenant em toda dimensão](#11-limites-por-tenant-em-toda-dimensão)
- [12. Checklist de PR](#12-checklist-de-pr)

## 1. Mapear requisição para tenant

Mapear o tenant **não é** autorizar a requisição (V-32, Azure, Verificado). Duas etapas: (a) identificar o tenant; (b) provar que a identidade autenticada pode agir nele (audience e scope em OAuth 2.0).

| Forma de identificar | Quando serve | Cuidados |
| --- | --- | --- |
| Claim do token validado (ou lookup pela identidade do token) | padrão para APIs | validar assinatura com biblioteca confiável; o plugin não escreve validação de assinatura |
| Subdomínio (`acme.app.com`) | UX e roteamento | confirmar contra o claim; divergência recusa (regra nossa, **Inferido** de V-32) |
| Caminho (`/t/acme/...`) | APIs públicas | idem; nunca confiar só no caminho |
| Header customizado | APIs internas | não serve em GET de navegador nem atrás de proxy que o altere (V-32) |
| Query string, corpo | **nunca** como fonte do tenant | o cliente controla |
| Chave de API com lookup ou HMAC | integrações máquina a máquina | a página da Azure diz que API key "não oferece nível alto de segurança" e prefere OAuth 2.0/OIDC com token de vida curta (V-32) |
| Certificado de cliente | mTLS | mapear fingerprint para tenant em tabela própria |

Regra para o CLAUDE.md (snippets 2 e 22): `tenant_id` sai do claim validado ou do cadastro vinculado ao `iss` de SSO; subdomínio e claim divergentes recusam; a rota confere audience e scope; token de usuário que pertence a vários tenants carrega a organização **ativa** e o servidor confere a associação a cada requisição (seção 8).

## 2. Autorização do objeto

Base: OWASP Authorization Cheat Sheet (V-11) e a instrução de segurança do awesome-copilot (V-12, MIT, classe B). "Autenticado não é isolado" (V-08).

1. **Deny by default**: rota nova sem policy explícita falha (V-11, AZ1 de V-12).
2. **Dono do objeto**: toda leitura e escrita confere `objeto.tenant_id == contexto.tenant_id` na própria consulta (`WHERE id = $1 AND tenant_id = $2`), não em `if` depois de carregar (V-11).
3. **IDOR/BOLA**: IDs de lookup não são acessíveis nem adulteráveis sem checagem; UUID aleatório não é controle de acesso (V-11; correção de V-57).
4. **Mass assignment**: nunca aceitar `role`, `tenant_id` ou `isAdmin` do corpo; lista explícita de campos aceitos (AZ4, AZ5 de V-12).
5. **Autorização no servidor**: esconder o botão na tela não é controle (AZ2); arquivos estáticos e anexos também passam pela checagem (V-11).
6. **Reautenticação** em troca de e-mail, exclusão de conta, mudança de papel e exportação completa (AZ6 de V-12).
7. **Falha segura**: se a checagem falha ou não consegue executar, negar (V-11).
8. **Log de negação** com `tenant_id` e `user_id`, sem PII (V-11, V-41).
9. **Teste negativo**: usuário do tenant A tenta objeto do tenant B em cada rota (matriz em `assets/templates/matriz-dois-tenants.md`).

Severidade de três níveis no relatório: crítico (antes do merge), importante (no sprint), sugestão (depois) (V-12). A ferramenta oficial `claude-code-security-review` filtra por padrão DoS e rate limiting, e declara que não é endurecida contra prompt injection (V-13).

## 3. 404 ou 403

Conflito C1: V-23 (brain) manda 404 para objeto de outro tenant ("403 confirma a existência"); V-11 e V-12 recomendam "não encontrado". Padrão do plugin: **404 para objeto de outro tenant**; 403 só quando o objeto é do próprio tenant e falta papel. É prática, não norma (**Inferido**). Evite diferenças observáveis entre "não existe" e "é de outro tenant": mesmo corpo, mesmo tempo aproximado, mesma forma de erro.

## 4. Esqueleto de contexto em mecanismo compartilhado

O isolamento mora num ponto único (V-63, V-48): helper de transação, repositório base e policy de banco. Esqueleto em TypeScript com `node-postgres`; **não executado** e a assinatura da API deve ser conferida na versão instalada (PAD-13).

```ts
import type { Pool, PoolClient } from "pg";

const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

export async function withTenant<T>(
  pool: Pool,
  tenantId: string,                       // vem do contexto autenticado, nunca do corpo
  fn: (db: PoolClient) => Promise<T>,
): Promise<T> {
  if (!UUID.test(tenantId)) throw new Error("tenant context ausente ou inválido");  // falha audível
  const db = await pool.connect();
  try {
    await db.query("BEGIN");
    await db.query("SELECT set_config('app.tenant_id', $1, true)", [tenantId]);     // escopo de transação
    const result = await fn(db);
    await db.query("COMMIT");                                                       // antes de responder
    return result;
  } catch (err) {
    await db.query("ROLLBACK");
    throw err;
  } finally {
    db.release();
  }
}

// Repositório: única camada com acesso ao banco; toda função recebe o tenant (snippet 5)
export const invoices = {
  byId: (pool: Pool, tenantId: string, id: string) =>
    withTenant(pool, tenantId, (db) =>
      db.query("SELECT * FROM invoices WHERE id = $1 AND tenant_id = $2", [id, tenantId])
        .then((r) => r.rows[0] ?? null),                                            // null -> 404
    ),
};
```

Observe o duplo filtro: `tenant_id = $2` na consulta (barreira 1) e RLS (barreira 2). Mesma ideia em outras stacks: `AsyncLocalStorage` (Node), `contextvars` (Python), `context.Context` (Go), `ThreadLocal`/`@RequestScope` (Java), `AsyncLocal` (.NET); a regra é que **nenhuma função de domínio escolha o tenant**.

## 5. Jobs, workers e filas

- A **mensagem carrega `tenant_id`** (e a versão do schema da mensagem). O worker não herda contexto global (caso clássico: contexto de tenant perdido em worker, brain).
- Uma transação por tenant em jobs em lote; falha em um tenant não impede os demais e é reexecutável (V-23).
- Entrega "pelo menos uma vez": tabela de mensagens processadas com `UNIQUE (tenant_id, message_id)`; efeito aplicado uma vez (brain, "Microsserviços e eventos").
- Retry com backoff exponencial e jitter, só em operação idempotente; mensagem venenosa vai para DLQ com o motivo e há reprocessamento (brain).
- Escrita em lote e operações de otimização (reindexação, compactação, ingestão) também rodam sob o isolamento (**Inferido**; ver princípio de S4; a fonte original R-gap2-14 foi rejeitada como regra).
- Fila compartilhada: limite de concorrência por tenant para evitar noisy neighbor (V-09, V-49).

## 6. Cache, busca, arquivos e websockets

| Superfície | Regra | Fonte |
| --- | --- | --- |
| Cache | tenant na chave de **todo** valor que varia por tenant; namespace global explícito para o que é realmente compartilhado; autorizar antes de ler valor protegido; chave só com o ID do recurso vaza entre tenants e permissões (brain `cache-permissao`: cache key = `report_id` com TTL de 10 min, e o usuário pode perder a permissão antes do TTL) | V-49, brain |
| Busca e autocomplete | filtro por tenant na consulta ao índice, não pós-filtro no cliente; índice por tenant ou campo filtrável obrigatório | V-23, Inferido |
| Exportação CSV e relatórios | escopo do `tenant_id` do token; job de exportação grava arquivo em prefixo do tenant e a URL expira | V-23, V-29 |
| Arquivos e anexos | caminho de storage com prefixo do tenant; URL assinada **só depois** de autorizar objeto e operação, limitada a objeto e método, vida curta | V-49 |
| Websockets e SSE | sala/canal por tenant; autorização no handshake **e** em cada assinatura de canal | V-23, Inferido |
| Notificações e e-mails | resolver destinatários dentro do tenant; template sem dado de outro tenant | V-23 |
| Logs | `tenant_id` em todo log; sem corpo de requisição, token, senha ou PII | V-41 |

## 7. Papéis: RBAC, ABAC, ReBAC

Conflito C6: o OWASP diz que RBAC é inadequado para multi-tenant e acesso entre organizações e prefere ABAC/ReBAC (V-11); starters e fornecedores usam 3 papéis (Member, Manager, Admin) checados contra a associação atual (V-25, B) e papéis definidos uma vez por aplicação (V-31).

Padrão do plugin: papéis pequenos **dentro** do tenant (por exemplo `owner`, `admin`, `billing_admin`, `member`, `viewer`) **mais** checagem de objeto por tenant sempre. Migre para atributo/relação quando houver explosão de papéis; o limiar é Suposição (sem fonte), meça com contagem de papéis e de exceções por cliente. Desenho de papéis, por pergunta: quem paga e gerencia assinatura (`billing_admin`)? quem convida e remove? quem exporta dados? quem vê auditoria? A matriz papel x ação é testada **pela API**, não pela tela (V-23).

## 8. Organização ativa e multi-aba

Usuário pode pertencer a várias organizações (Auth0, V-31). O Clerk documenta organização ativa **por aba** e que o cookie de sessão reflete só a aba mais recente, de modo que requisições de fundo devem enviar o token no cabeçalho `Authorization` (V-31, Verificado). Regra do plugin (**Inferido** desse caso): o servidor resolve a organização ativa a **cada requisição** a partir de credencial validada e confere a associação ao vivo (não um token antigo, V-25); nunca confia só no cookie nem em seletor de organização vindo do cliente. Contrato para o front (`/web-frontend:playbook`) e o mobile (`/mobile-apps:playbook`): enviar a organização ativa de forma explícita e tratar 404/403 como troca de contexto.

Estados de membro: `invited` → `active` → `inactive` (sessões revogadas, papel mantido, reativável) → `deleted`. O WorkOS documenta `pending`, `active`, `inactive`, e que desativar revoga todas as sessões e preserva o papel (V-31). Excluir quando o app não precisa manter o registro; desativar quando dados históricos referenciam o membro.

## 9. Acesso de suporte e impersonation

Sem fonte dedicada: **Inferido** de V-08 ("inclusive para admin") e V-41 (eventos de auditoria incluem ação do suporte do SaaS no tenant). Fonte comum de vazamento real; trate como funcionalidade de segurança.

1. Acesso por **motivo, escopo e prazo**: ticket vinculado, tenant específico, expiração automática.
2. Papel de suporte **não** contorna RLS com role privilegiada; a sessão de suporte é uma sessão do tenant, com contexto de tenant, e papel limitado (somente leitura por padrão).
3. Trilha com `actor_id` real do funcionário e `on_behalf_of` do usuário/tenant; evento visível ao admin do tenant (visibilidade ao cliente: lacuna sem fonte, **Suposição**).
4. Aprovação do tenant para ações de escrita; reautenticação do funcionário.
5. Sem copiar produção para ambiente de desenvolvimento (V-22).
6. Teste: sessão de suporte do tenant A não lê tenant B; encerra no prazo; gera evento.

## 10. Restauração de um tenant e alerta cruzado

V-49 (OWASP Multi-Tenant, CC BY-SA 4.0: só redação própria):

- Restaurar um tenant a partir de backup compartilhado em **recurso separado**, recuperar só o alvo e nunca restaurar sobre dado vivo; registrar origem, destino, motivo e resultado; testar que os outros tenants estão ausentes no recurso restaurado.
- Tentativa cruzada **negada** vira evento de segurança com alerta por limiar (por exemplo, N negações de um ator em T minutos: limiar é Suposição). Uma negação isolada é ruído; um padrão de enumeração de IDs é sinal.

## 11. Limites por tenant em toda dimensão

Rate limit com tenant como dimensão, também em filas, concorrência e conexões (V-49); teto de página e timeout de query; exportações em fila; métricas e custo por tenant; resposta de throttling documentada com código e `Retry-After` (V-09). Detalhes em `entitlements-limites-uso.md`.

## 12. Checklist de PR

Versão colável em `assets/templates/checklist-pr-tenant.md`. Resumo: tenant do contexto; consulta escopada; policy explícita; 404 para outro tenant; campos aceitos em lista; sem `SET` de sessão; job com contexto; cache com tenant na chave; teste com dois tenants; log sem PII.
