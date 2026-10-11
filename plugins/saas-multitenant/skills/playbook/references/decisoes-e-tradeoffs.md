# Decisões e trade-offs de SaaS multi-tenant e billing

Como usar: cada decisão traz as opções, o critério, o **padrão do plugin** (a escolha quando o usuário não decidiu) e o que registrar em ADR. O padrão é ponto de partida defensável, não verdade universal; quando a decisão é do produto ou do jurídico, o plugin pergunta ou marca Suposição. Fontes `V-nn` em `fontes.md`.

## Sumário

- [D1. Modelo de tenancy: silo, bridge, pool](#d1-modelo-de-tenancy-silo-bridge-pool)
- [D2. RLS, schema por tenant ou banco por tenant](#d2-rls-schema-por-tenant-ou-banco-por-tenant)
- [D3. Quando mudar de modelo](#d3-quando-mudar-de-modelo)
- [D4. Acesso em `past_due`](#d4-acesso-em-past_due)
- [D5. Metering: Metronome ou Billing Meters ou ledger interno](#d5-metering-metronome-ou-billing-meters-ou-ledger-interno)
- [D6. Customer por tenant](#d6-customer-por-tenant)
- [D7. RBAC, ABAC, ReBAC](#d7-rbac-abac-rebac)
- [D8. SSO por tenant: construir, biblioteca ou serviço](#d8-sso-por-tenant-construir-biblioteca-ou-serviço)
- [D9. 404 ou 403](#d9-404-ou-403)
- [D10. Sem contexto: erro ou zero linhas](#d10-sem-contexto-erro-ou-zero-linhas)
- [D11. Entitlement, flag e configuração](#d11-entitlement-flag-e-configuração)
- [D12. Backups e eliminação](#d12-backups-e-eliminação)
- [D13. Trial: gratuito ou pago](#d13-trial-gratuito-ou-pago)
- [D14. Cobrança por assento, por uso ou híbrida](#d14-cobrança-por-assento-por-uso-ou-híbrida)
- [D15. Hook, CLAUDE.md, permissão ou CI](#d15-hook-claudemd-permissão-ou-ci)
- [Registro dos conflitos C1 a C18](#registro-dos-conflitos-c1-a-c18)

## D1. Modelo de tenancy: silo, bridge, pool

Fontes: V-07 (Azure, `ms.date` 2025-06-11), V-33 (Azure `storage-data` e AWS Prescriptive Guidance), todos Verificados.

**Perguntas de entrada (V-07), uma por vez, só as materiais:**
1. Quem é o tenant? (B2B costuma ser a empresa; B2C pode ser família ou grupo; um cliente pode virar vários tenants.)
2. Há exigência regulatória ou contratual de separação física?
3. Quantos tenants em 3 anos e qual o maior?
4. Isolamento é vendido como plano (enterprise)?
5. O que pode ser compartilhado por camada (UI, aplicação, dados)?
6. Como mapear requisição → tenant → deployment (stamp)?

| Modelo | Escolha quando | Evite quando | Custo oculto |
| --- | --- | --- | --- |
| **Pool** (tabelas compartilhadas + RLS) | muitos tenants pequenos, equipe pequena, custo por tenant baixo | exigência de chave própria, residência de dados ou isolamento físico | impacto entre tenants (noisy neighbor), compliance mais difícil, disponibilidade tudo-ou-nada, complexidade do RLS (Azure: "muitas soluções não usam") |
| **Silo** (banco/instância por tenant) | poucos tenants grandes, contrato exige separação, customização forte | milhares de tenants sem automação | automação obrigatória; custo; migração por tenant |
| **Bridge** (híbrido) | maioria no pool, alguns clientes enterprise em silo | equipe sem capacidade de operar dois modelos | duas operações, mapa tenant → deployment |

**Padrão do plugin (V-33):** pool + RLS para planos comuns; silo para chave própria, residência de dados ou exigência de isolamento físico; **nunca** tabela ou coluna por tenant; alteração manual de schema e dependência de uma única versão de schema são antipadrões; migração de schema automatizada com versão por tenant e aplicação compatível com a versão anterior. Isolamento é espectro e pode variar por camada (V-07). Tenant e deployment são conceitos distintos: exija mapa tenant → deployment.

**Registrar em ADR:** definição de tenant, resposta às 6 perguntas, modelo por camada, riscos, critérios de mudança (D3), mapa tenant → deployment. Template: `assets/templates/adr-modelo-tenancy.md`.

## D2. RLS, schema por tenant ou banco por tenant

| Critério | Pool + RLS | Schema por tenant | Banco por tenant |
| --- | --- | --- | --- |
| Isolamento | lógico, segunda barreira em policy | lógico por schema/role | físico no nível do banco |
| Custo por tenant | menor | médio | maior |
| Migração de schema | uma vez, global | N vezes (código de migração) | N vezes |
| Backup/restore e GDPR por tenant | exige restauração em recurso separado e extração (V-49) | mais simples (apagar/restaurar o schema) | mais simples |
| Extensões, locks, memória | sem problema específico | relatos de limite de locks, memória e I/O, `pg_stat_statements` ruim | n/a |
| FK entre tenants | prevenida com FK composta | impossível entre schemas (uma equipe saiu de schema por tenant por isso) | impossível |
| Fonte | V-01, V-33 (Verificado) | V-44 (**relato de praticante**, HN) | V-33 (Verificado) |

Conflito C5: as vantagens e desvantagens do schema por tenant vêm de relatos (HN, 254 pontos, 22 comentários de topo lidos); a Azure lista tabela e coluna por tenant como antipadrão, não schema. Rotule "relato de praticante" no ADR. Não há comparação de schema-por-tenant em página oficial lida.

Padrão: pool + RLS; silo para exigência física. Schema por tenant só com razão escrita (por exemplo, restore por tenant frequente) e automação de migração.

## D3. Quando mudar de modelo

Critérios sugeridos (**Suposição**, calibrar com o produto): um tenant passa a exigir chave própria, residência ou isolamento físico; um tenant consome parcela anormal e degrada os demais mesmo com limites; contrato com RTO/RPO diferenciado; auditoria de cliente que exige separação demonstrável. Plano de migração entre modelos: copiar por tenant, reconciliar contagens e somas por partição, janela curta, reversão definida, mapa tenant → deployment atualizado de forma atômica, teste de dois tenants depois.

## D4. Acesso em `past_due`

Fontes: V-02 (Smart Retries "não garante"), V-38. Conflito C7.

| Opção | Efeito | Risco |
| --- | --- | --- |
| Liberar com aviso e prazo | menos churn involuntário; cliente percebe e regulariza | uso gratuito durante a janela |
| Liberar só leitura | meio-termo | complexidade de produto |
| Bloquear imediatamente | protege receita | churn por falha de cartão que seria recuperada |

**Padrão sugerido (Inferido):** liberar com aviso e prazo (alinhado às tentativas do Smart Retries, que na configuração recomendada somam 8 tentativas em 2 semanas), bloquear em `unpaid` e `canceled`. É decisão de produto: registre na tabela status → acesso do spec.

## D5. Metering: Metronome ou Billing Meters ou ledger interno

Fontes: V-06, V-39. Conflito C4.

- Stripe: Metronome recomendado para a maioria das integrações novas; Billing Meters para quem já cobra assim. "Billing Meters é legacy" é falso.
- Avalie: custo, lock-in, latência de visibilidade (eventos assíncronos), conflito de interesse (a recomendação é do fornecedor), granularidade (tenant, usuário, recurso), reconciliação.
- Ledger append-only interno: ideia classe C, não verificada (V-06); só com reconciliação contra o provedor.
- `compare-metronome` não foi relida: o plugin **não recomenda** Metronome, apenas registra o conflito e exige o ADR.

## D6. Customer por tenant

Fonte: V-39 ("usuário ou empresa" é o texto). Conflito C9. Padrão (**Inferido**): um tenant (organização) = um Customer, com `metadata.tenant_id`. Exceção em ADR: várias moedas por tenant exigem dois Customers (moeda única, imutável). Alternativa: objeto `Account` (Accounts v2; GA para Connect, prévia pública para os demais, V-39). Subconta de PSP para o tenant cobrar o cliente final é outro fluxo, fora do Customer do SaaS (V-53).

## D7. RBAC, ABAC, ReBAC

Fontes: V-11 (OWASP: RBAC inadequado para multi-tenant e acesso entre organizações; prefira ABAC/ReBAC), V-25 e V-31 (três papéis; papéis por aplicação). Conflito C6.

Padrão: papéis pequenos dentro do tenant **mais** checagem de objeto por tenant sempre. Migre para atributo/relação quando houver explosão de papéis (sinais: mais de uma exceção por cliente enterprise; papéis duplicados que diferem por um recurso; limiar é **Suposição**). Ferramentas de policy (Cedar, OpenFGA etc.) não foram pesquisadas: não recomende sem leitura.

## D8. SSO por tenant: construir, biblioteca ou serviço

Ver `identidade-sso-scim.md`, seção 1. Padrão: serviço ou biblioteca mantida; nunca parser SAML próprio. Critério de escolha: SSO/SCIM é requisito comercial imediato? equipe consegue operar o fluxo? limites do serviço (Auth0 sem domínio de login por organização, V-31).

## D9. 404 ou 403

Conflito C1. Padrão: **404** para objeto de outro tenant (evita enumeração); 403 só quando o objeto é do próprio tenant e falta papel. Prática, não norma (V-23 ressalva; V-11 e V-12 dizem "não encontrado"). Rótulo Inferido.

## D10. Sem contexto: erro ou zero linhas

Conflito C2. Padrão: `NULLIF(current_setting('app.tenant_id', true), '')::uuid` na policy (zero linhas; escrita rejeitada) **mais** guarda na aplicação que lança erro se o contexto faltar. O exemplo da AWS usa `current_setting` sem `missing_ok` (erro). Ambos fecham; escolha um, documente e teste (V-65).

## D11. Entitlement, flag e configuração

Conflito C10. Entitlement = direito pago (tabela local); flag = rollout/exceção; configuração = preferência do tenant. Ver `entitlements-limites-uso.md`, seção 1.

## D12. Backups e eliminação

Apagar linha não apaga backup (Inferido). Opções: (a) backups com expiração fixa e dita ao tenant (padrão); (b) criptografia por tenant com destruição de chave ("crypto-shredding"; ideia estável, **não pesquisada**: avalie custo e complexidade antes de propor); (c) re-gravar backup sem o tenant (custoso, raro). Backup compartilhado complica restauração por tenant: restaure em recurso separado (V-49).

## D13. Trial: gratuito ou pago

Fonte: V-38. Perguntas: o trial tem os mesmos requisitos de segurança e SLA? infraestrutura compartilhada? como evitar abuso? o que ocorre sem meio de pagamento (`missing_payment_method`: `create_invoice` padrão, `cancel` ou `pause`)? Trial offers exigem API `2026-09-30.endive`+ e modo `flexible`, não funcionam com Checkout (use `trial_end`). Conferir o changelog.

## D14. Cobrança por assento, por uso ou híbrida

Fontes: V-05, V-06, V-37. Assento: simples de entender, exige contagem idempotente e política de excedente no downgrade. Uso: exige metering com evento único, reconciliação e atraso declarado. Híbrida: assinatura base + uso; MRR da Stripe **não** inclui cobrança por uso (V-40), então defina a métrica própria. Decisão de produto.

## D15. Hook, CLAUDE.md, permissão ou CI

Fonte: V-14, V-15 (Anthropic). Conflitos C8 e C11. Árvore de decisão: o que deve valer **sempre** → hook mais regras `deny`; fato universal curto → CLAUDE.md; regra por caminho → regra com `paths`; conhecimento ocasional → skill; investigação ou revisão com contexto limpo → subagente. CLAUDE.md é contexto, não imposição; hook não é fronteira de segurança (regex não substitui scanner; hooks são guardrail). A afirmação "hooks são best-effort" **não foi encontrada** na documentação: não use. `@arquivo` não dispara `PreToolUse`: complementar com `permissions.deny` de `Read`. Garantia de isolamento = testes de dois tenants no CI, não frase em CLAUDE.md.

## Registro dos conflitos C1 a C18

| # | Conflito | Resolução adotada |
| --- | --- | --- |
| C1 | 404 x 403 para objeto de outro tenant | 404 por padrão (D9) |
| C2 | contexto ausente: erro (AWS) x vazio (`NULLIF`, V-01) | ambos fecham; policy vazia + guarda de aplicação (D10) |
| C3 | RLS "necessário no pool" (AWS) x "muitas soluções não usam" (Azure) | pool exige RLS como segunda barreira; custo aceito; exceções para silo |
| C4 | Metronome recomendado x Billing Meters | ADR com conflito de interesse (D5) |
| C5 | schema por tenant: prós e contras só em relatos | rotular "relato de praticante" (D2) |
| C6 | RBAC x ABAC/ReBAC | papéis pequenos + objeto por tenant (D7) |
| C7 | acesso em `past_due` | decisão de produto; padrão com aviso e prazo (D4) |
| C8 | "hooks best-effort" x documentação | hook + deny; não é fronteira de segurança (D15) |
| C9 | um Customer por tenant | padrão com exceção em ADR (D6) |
| C10 | entitlement x flag | separados (D11) |
| C11 | CLAUDE.md x garantia | testes, CI e hooks garantem (D15) |
| C12 | estudo Amplifying (modelos antigos) x modelos atuais | usar só como motivo para declarar a stack; sem percentuais |
| C13 | prazo de incidente LGPD "não aparece" | três dias úteis na página da ANPD; texto da Resolução não lido |
| C14 | LGPD art. 18 V como "acesso" (brain) | V é portabilidade; acesso é II |
| C15 | evento de cancelamento do Asaas | aberto: decidir no sandbox |
| C16 | webhook com token em header x assinatura do corpo | token do cofre + `id` UNIQUE + allowlist; replay mitigado, não impedido |
| C17 | prazo em dobro de incidente para pequeno porte | aberto: não citar como regra |
| C18 | datas de NFS-e/IBS/CBS para o Simples | vale a Res. CGSN 191/2026; datas como parâmetro |
