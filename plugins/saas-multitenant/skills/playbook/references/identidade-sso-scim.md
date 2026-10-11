# Identidade enterprise: organizações, SSO (SAML e OIDC), SCIM e domínio verificado

Escopo: login corporativo e provisionamento em SaaS multi-tenant. Itens `V-nn` em `fontes.md`. Princípio: **não implementar parser SAML, validação de token ou provisionamento do zero**; usar biblioteca mantida ou serviço, e testar o comportamento. Lacunas declaradas: do OIDC só a validação do ID Token (§ 3.1.3.7) foi lida (100 mil de 285 mil caracteres); discovery, rotação de JWKS e § 5.5 são Não verificáveis; JIT em Okta e Entra e reativação no Entra não foram pesquisados.

## Sumário

- [1. Decisão: construir, biblioteca ou serviço](#1-decisão-construir-biblioteca-ou-serviço)
- [2. Organizações, convites e estados de membro](#2-organizações-convites-e-estados-de-membro)
- [3. Domínio verificado](#3-domínio-verificado)
- [4. SAML: checagens obrigatórias](#4-saml-checagens-obrigatórias)
- [5. OIDC: validação do ID Token](#5-oidc-validação-do-id-token)
- [6. SCIM](#6-scim)
- [7. Requisitos de endpoint SCIM do Entra](#7-requisitos-de-endpoint-scim-do-entra)
- [8. JIT provisioning](#8-jit-provisioning)
- [9. Auditoria de identidade](#9-auditoria-de-identidade)
- [10. Testes de integração](#10-testes-de-integração)

## 1. Decisão: construir, biblioteca ou serviço

| Opção | Quando | Cuidado |
| --- | --- | --- |
| Serviço de identidade (Clerk, Auth0, WorkOS e similares) | time pequeno, SSO/SCIM como requisito comercial | viés de fornecedor nas fontes (V-31); conferir limites (o Auth0 não tem domínio de login próprio por organização: quem exige isso pede tenant Auth0 separado) |
| Biblioteca mantida de SAML/OIDC no seu backend | controle total, custo operacional aceito | a lista de bibliotecas recomendadas não foi obtida (V-35); escolha pela manutenção ativa e CVEs recentes, conferidos por você |
| Parser SAML próprio | **não** | validação de assinatura XML tem classes de ataque conhecidas (XML Signature Wrapping); decisão fora do padrão exige aprovação explícita |

Snippet 12 do CLAUDE.md fixa a stack aceita (`auth = [BIBLIOTECA]`). Claude Code tende a escrever autenticação própria (V-19); a regra é declarar e proibir sem aprovação.

## 2. Organizações, convites e estados de membro

Fonte: V-31 (Clerk, Auth0, WorkOS: páginas de fornecedor, Verificado, usar como comparação de padrões).

- Organização = cliente/parceiro B2B; usuário pode pertencer a várias. Conexão enterprise é habilitada **por organização**. Papéis definidos uma vez por aplicação.
- Convites carregam papel; convite independe do domínio do e-mail (WorkOS). Convite expirado ou reutilizado é recusado; e-mail com caixa diferente casa com o mesmo convite; convidado já membro de outro tenant entra no segundo com troca de contexto clara (brain, V-23).
- Estados do membro (WorkOS: `pending`, `active`, `inactive`): `invited` → `active` → `inactive` → `deleted`. Desativar **revoga todas as sessões e preserva o papel**; membro `pending` só pode ser excluído; exclua quando o app não precisa manter o registro e desative quando dados históricos o referenciam.
- Organização ativa resolvida **por requisição** a partir de credencial validada (`autorizacao-e-tenant-context.md`, seção 8).
- Campo CNPJ do cadastro do tenant: não pode ser `BIGINT` nem aceitar só dígitos, porque o CNPJ alfanumérico é aceito desde julho de 2026 para inscrições novas (brain, "Documentos brasileiros"; reconferir a norma vigente).

## 3. Domínio verificado

Fonte: V-36 (Entra, Verificado, `ms.date` 2026-06-18).

- SSO por tenant só é habilitado **depois** de o tenant provar o domínio de e-mail. Padrão do Entra: registro TXT ou MX; TTL de 3600 s; propagação de "instantânea a dias" (não "horas"); um domínio só verifica em um diretório.
- Domínio não verificado não entra (teste obrigatório).
- Auto-join ou sugestão com aprovação em domínio verificado (Clerk, V-31). Não conceda papel elevado por domínio.

## 4. SAML: checagens obrigatórias

Fonte: OWASP SAML Security Cheat Sheet (V-35, classe A, Verificado); a visão geral da OASIS é um **Committee Draft de 2008, não normativo** (contexto de papéis IdP/SP e bindings, não norma).

Rejeite a resposta se faltar qualquer item:

1. Confiar **só** na chave obtida do IdP (metadado) e guardada localmente; **ignorar `KeyInfo` do documento**.
2. Rejeitar SHA-1.
3. `Audience` igual ao EntityID do SP.
4. `Destination` igual à URL do ACS.
5. `InResponseTo` correspondente à requisição emitida (e detecção de replay em respostas não solicitadas).
6. `Recipient` correto.
7. `NotBefore` e `NotOnOrAfter` válidos.
8. Defesa contra XML Signature Wrapping: schema local, XPath absoluto, sem `getElementsByTagName` antes da validação, assinatura cobrindo a asserção efetivamente usada.

Regra de CLAUDE.md (snippet): "Não implementar parser SAML próprio. Validar assinatura com chave do metadado do IdP, Audience, Destination, InResponseTo e validade; rejeitar a resposta sem todas as checagens. SSO ativa por tenant só depois de o tenant provar o domínio."

## 5. OIDC: validação do ID Token

Fonte: OpenID Connect Core 1.0, § 3.1.3.7 (V-46, classe A, Verificado). Licença da especificação não verificada: redação própria.

| Item | Requisito |
| --- | --- |
| `iss` | exatamente igual ao Issuer (MUST) |
| `aud` | contém o `client_id`; rejeitar se o cliente não for audiência válida (MUST) |
| `azp` | se presente, igual ao `client_id` (SHOULD) |
| assinatura | validar com o `alg` do cabeçalho e as chaves do Issuer (MUST); RS256 por padrão ou o registrado (SHOULD); HS256/384/512 usam o `client_secret` |
| `alg` | lista de aceitos definida pelo projeto, **sem `none`** |
| `exp` | no futuro (MUST) |
| `nonce` | se enviado na requisição, presente e igual (MUST) e checado contra replay (SHOULD) |
| `iat` | **não é MUST**: a janela aceitável é do cliente; registre o valor no spec e rejeite fora dela |
| `acr`, `auth_time` | SHOULD quando solicitados ou com `max_age` |

A validação TLS pode (MAY) substituir a checagem de assinatura quando o token vem direto do Token Endpoint. **O tenant sai do `iss` validado e do vínculo cadastrado de SSO** (Inferido, liga OIDC à regra de mapeamento de V-32). Discovery, rotação de JWKS e § 5.5: Não verificáveis; leia a especificação e a documentação do IdP antes de implementar.

## 6. SCIM

Fontes: RFC 7643 (lida até a seção 4.2), RFC 7644 (§ 7 lida na rodada 2), RFC 9865, RFC 9967 (V-10, V-36, classe A); Okta (V-55).

Regras de implementação:

1. Endpoints `/Users` e `/Groups`; busca por e-mail via `POST /.search` (filtro com dado pessoal não vai em URL de GET; o servidor pode responder 403 com `scimType` "sensitive").
2. **Token escopado a um único tenant**, com entropia e vida limitada; TLS 1.2 no mínimo; Basic deve ser evitado; credencial nunca em texto claro.
3. `userName`: obrigatório, sem diferenciar maiúsculas, único no provedor. `id` e `meta` atribuídos pelo servidor (readOnly). `externalId` opcional, definido pelo cliente: guarde para correlação com o IdP (**Inferido**: não é exigência da RFC para idempotência de POST). `groups` no User é readOnly e muda pelo recurso Group; Group exige `displayName`.
4. POST create devolve 201 com `Location`; PUT substitui e não cria; conflito de unicidade responde 409 (**Inferido**; confirme na RFC).
5. PATCH com `add`, `remove` e `replace`; **idempotente**: `add` de valor existente e `remove` de membro inexistente não alteram nada e devolvem sucesso (RFC 7644).
6. **Desprovisionar é `active=false`, nunca DELETE.** `active=false` revoga sessões e tokens **na hora** (não no próximo login) e **mantém os vínculos de grupo**; exclusão definitiva segue a política de retenção. O Okta diz que não envia DELETE de usuário ao app SCIM e envia `active=false` (PATCH em integrações novas do OIN, PUT em customizadas); usuário só suspenso no Okta não dispara desprovisionamento (V-55).
7. Paginação por cursor (RFC 9865): `cursor`, `nextCursor`, erros `invalidCursor`, `expiredCursor`, `invalidCount` (HTTP 400); trate `expiredCursor` reiniciando a listagem. Paginação clássica: `startIndex` (padrão 1) e `count`.
8. Limite de taxa: responder 429 com `Retry-After`. O comportamento do Okta (inteiro em `Retry-After`, senão cinco minutos, backoff dobrando, até 10 tentativas) é do Okta, não do padrão.
9. RFC 9967: eventos SCIM como SETs, `Prefer: respond-async` com 202, cabeçalho `Set-Txn`; implemente só se o cliente exigir.
10. Criação anônima, se existir, com limite de taxa e usuário inativo até confirmação (RFC 7644 § 7).

Ressalvas: ler as RFCs 7643 (além da 4.2), 9865 e 9967 antes de implementar. Detalhes de IdP específicos são Suposição até teste.

## 7. Requisitos de endpoint SCIM do Entra

Fonte: V-54 (`ms.date` 2026-09-15, Verificado). Checklist de aceite:

- [ ] usuário desativado volta nas leituras com `active=false` (soft delete: o objeto "should be returned" ativo ou não; só deixa de ser devolvido no hard delete);
- [ ] PATCH aceita `op` Add, Replace e Remove **em qualquer capitalização**;
- [ ] `excludedAttributes=members` em Group (RFC 7644 § 3.4.2.2), listagem e paginação (§ 3.4.2.4);
- [ ] `/Schemas` exposto (RFC 7643 § 7);
- [ ] um único bearer token para o Entra, escopado a um tenant;
- [ ] **Test Connection** passa sem dado real de cliente (o Entra busca um usuário e um grupo aleatórios); as chamadas DELETE de teste só ocorrem se o hard delete for suportado;
- [ ] reativação de usuário e restauração de grupos testadas (comportamento do Entra ao reativar: Não verificável).

## 8. JIT provisioning

Fonte: V-56 (Braze, classe B, regras de fornecedor, não padrão de IdP).

Regras do fornecedor: o domínio de e-mail precisa já existir na empresa, com ao menos um desenvolvedor confirmado; vale só para login iniciado pelo IdP; a asserção precisa de atributo `email` válido, igual ao do login; todos os criados recebem o mesmo workspace e permission set padrão; não atualiza permissões de usuário existente; desligar exige o suporte do fornecedor.

Regras derivadas do plugin (**Inferido**): JIT só para **domínio verificado**; criar com o **papel mínimo**, nunca elevar por atributo do IdP sem aprovação; não ligar JIT junto com SCIM ativo para o mesmo tenant (resumos de Harness e Workato não lidos). JIT em Okta e Entra: lacuna.

## 9. Auditoria de identidade

Eventos obrigatórios por tenant (V-41): login SSO (sucesso e falha), convite, mudança de papel, desativação, chave de API criada ou revogada, ação do suporte. Campos: `tenant_id`, `actor_id`, ação, recurso, resultado, instante UTC, origem; sem token, senha ou corpo. Detalhes em `lifecycle-compliance-auditoria.md`.

## 10. Testes de integração

| # | Teste | Esperado |
| --- | --- | --- |
| 1 | usuário removido ou desativado no IdP | perde acesso; sessões e tokens revogados na hora |
| 2 | domínio não verificado tenta SSO | recusado |
| 3 | primeiro login por SSO | cria membro com papel padrão mínimo |
| 4 | token SCIM do tenant A chama `/Users` do tenant B | 404/401, nada alterado |
| 5 | desprovisionar | `active=false`, grupos preservados; reativar restaura |
| 6 | PATCH com `op` em maiúsculas, minúsculas e misto | aceito nos três |
| 7 | resposta SAML com Audience, Destination ou InResponseTo errados; assinatura por chave do `KeyInfo`; SHA-1 | todas recusadas |
| 8 | ID Token com `iss` diferente, `aud` sem o `client_id`, `exp` vencido, `nonce` errado, `alg: none` | todos recusados |
| 9 | paginação por cursor expirado | tratado por reinício |
| 10 | 429 do SCIM | cliente respeita `Retry-After` |

Revisão somente leitura do login SSO: prompt PR-31 da biblioteca (V-64, sem eval) ou o agente `tenant-isolation-reviewer` para o mapeamento tenant.
