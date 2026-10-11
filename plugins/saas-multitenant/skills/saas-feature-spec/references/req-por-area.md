# Biblioteca de requisitos testáveis por área

Redação própria, destilada de V-11, V-12, V-21, V-23, V-02, V-03, V-04, V-30, V-29, V-40, V-41, V-59, V-60 e do brain-of-agent (dominios.md, MIT, conteúdo próprio do usuário; normas e números a reconferir). Use como ponto de partida: copie só o que se aplica, troque os colchetes e mantenha uma verificação por requisito. Conferido em 2026-10-10. Cada linha traz a verificação e a fonte.

Formato de cada requisito: `REQ-NN` · enunciado verificável · verificação · fonte e rótulo.

## REQ-01 Isolamento por tenant

| Enunciado | Verificação | Fonte |
| --- | --- | --- |
| Todo recurso [X] pertence a exatamente um tenant e toda leitura ou escrita é escopada pelo tenant do contexto autenticado, inclusive para admin. | teste de integração com dois tenants | V-08, V-11. Verificado |
| O tenant do contexto vem do claim do token validado (ou de lookup pela identidade), nunca de corpo, query ou header livre. | teste que envia `tenantId` do outro tenant no corpo e na query e vê o pedido ignorado ou recusado | V-32. Verificado |
| Requisição a recurso de outro tenant responde 404 com o mesmo corpo de "não existe". | teste: A pede ID de B e compara com ID inexistente | V-11, V-12, V-23. Inferido (prática) |
| Tabelas novas com `tenant_id` têm RLS `ENABLE` e `FORCE`, policy com `USING` e `WITH CHECK`, e a aplicação conecta com role sem `BYPASSRLS`. | teste de banco com a role da aplicação e consulta de catálogo | V-01, V-49. Verificado |
| Sem contexto de tenant, o acesso falha fechado (zero linhas ou erro explícito, nunca linhas). | teste em pool de tamanho 1 | V-34, V-65. Verificado (pooler: Não verificável sem teste) |
| Busca, autocomplete, exportação, anexos, notificações, websockets e cache não expõem dado de outro tenant; chaves de cache contêm o tenant. | testes por canal | V-23, V-49. Verificado |
| Jobs processam um tenant por transação e levam o `tenant_id` na mensagem. | teste de job com dois tenants | V-34. Verificado |

## REQ-02 Autorização

| Enunciado | Verificação | Fonte |
| --- | --- | --- |
| Rota nova sem política explícita de autorização é negada (deny by default). | teste que chama rota sem política e espera negação | V-11, V-12 AZ1. Verificado |
| Campos aceitos em criação e atualização são uma lista explícita; `role`, `tenant_id` e `isAdmin` do corpo são ignorados. | teste de escalada no corpo | V-12 AZ4/AZ5. Verificado |
| A matriz papel × ação [tabela anexa] vale pela API, não só pela interface. | testes parametrizados | V-23. Verificado |
| Troca de e-mail, exclusão de conta e mudança de papel exigem reautenticação. | teste | V-12 AZ6. Verificado |
| Negações de acesso são registradas com `tenant_id` e `user_id`, sem PII. | teste de log | V-11, V-41. Verificado |

## REQ-03 Eventos de billing

| Enunciado | Verificação | Fonte |
| --- | --- | --- |
| Estado de billing do tenant só muda por webhook ou API verificados, nunca por redirect de checkout. | teste que visita a URL de sucesso sem evento e não ganha acesso | V-02. Verificado |
| O handler verifica a assinatura sobre o corpo bruto, grava `event.id` com UNIQUE, responde 2xx antes da lógica pesada e processa em worker. | testes: duplicado, assinatura inválida, corpo alterado | V-03. Verificado |
| Eventos fora de ordem convergem para o estado correto porque o worker lê o objeto atual. | teste: `invoice.paid` antes de `customer.subscription.created` | V-03. Verificado |
| Chamadas de saída com efeito usam chave de idempotência derivada da operação de negócio. | teste de retry com a mesma chave | V-04. Verificado |
| Política de acesso por status: `trialing` e `active` liberam; `past_due` [decisão]; `unpaid` e `canceled` revogam. | testes por status | V-02. Verificado; `past_due` é Inferido |

## REQ-04 Limites do plano e downgrade

| Enunciado | Verificação | Fonte |
| --- | --- | --- |
| O plano [Free, Pro, Business] permite [N] [assentos, projetos ou chamadas]; o limite vale sob concorrência. | teste com requisições simultâneas no limite | V-23 (plano e limites). Verificado |
| Limite excedido responde [código] com mensagem que oferece upgrade. | teste | V-09 (transparência com o cliente). Inferido |
| Downgrade com uso acima do novo limite [bloqueia ou desativa excedentes escolhidos pelo admin]; nunca apaga dados. | teste: 10 usuários para plano de 5 | V-23, V-38, V-30. Verificado/Inferido |
| Rate limit por tenant e por plano; resposta 429 com `Retry-After`; tarefas pesadas em fila. | teste de limite | V-09. Verificado; limiares: Suposição |
| O gate de feature lê só `tenant_features`, alimentada por webhook e reconciliação. | teste de gate | V-05. Verificado |

## REQ-05 Auditoria

| Enunciado | Verificação | Fonte |
| --- | --- | --- |
| Os eventos [convite, mudança de papel, exportação, desativação, chave de API criada ou revogada, login SSO, ação de suporte] geram registro por tenant com `tenant_id`, `actor_id`, ação, recurso, resultado, instante UTC e origem. | teste de auditoria | V-41. Verificado (campos: Suposição) |
| Registros não contêm corpo de requisição, token, senha nem PII. | revisão de log | V-41. Verificado |
| Quem consulta a trilha do tenant [admin do cliente ou só o suporte]. | decisão de produto | lacuna sem fonte: Suposição |

## REQ-06 Dados do titular e do tenant

| Enunciado | Verificação | Fonte |
| --- | --- | --- |
| Exportação devolve os dados do tenant ou do titular em formato legível por máquina, com escopo do `tenant_id` do token. | teste de exportação com dois tenants | V-29; LGPD art. 18 II (acesso) e V (portabilidade); GDPR art. 20. Verificado |
| Eliminação apaga banco, storage, caches, índices de busca e réplicas, e lista processadores notificados; backups expiram em [prazo] e o tenant é informado. | execução em homologação e checklist | V-29, LGPD arts. 15, 16; GDPR art. 17. Verificado/Inferido |
| Retenção por tipo de dado com prazo definido em contrato e exceções legais. | tabela anexa | V-29. Prazos: Suposição (produto e jurídico) |
| Incidente: o tenant é avisado em [prazo contratual] para cumprir o prazo legal. | runbook | V-27, V-61; não é orientação jurídica |

## REQ-07 Métricas

| Enunciado | Verificação | Fonte |
| --- | --- | --- |
| A feature altera [MRR, churn ou ativação] e o dicionário de métricas registra a nova fórmula, a fonte e o tratamento de desconto, moeda e trial. | revisão do dicionário | V-40. Verificado; ativação: Suposição |
| "Usuário ativo" é definido com evento e janela. | revisão | V-40 (a16z). Verificado |

## REQ-08 NFS-e (condicional: tenant brasileiro com serviço tributável)

| Enunciado | Verificação | Fonte |
| --- | --- | --- |
| Está definido quem é o prestador (tenant ou SaaS); a emissão usa homologação ou produção restrita antes da produção. | revisão e teste em homologação | V-59. Inferido (checklist) |
| O certificado do prestador não fica em texto puro no banco; a nota é gravada com `tenant_id` e identificador de envio único. | revisão e teste de duplicidade | V-59. Inferido |
| Datas de vigência (por exemplo, NFS-e Nacional para ME e EPP do Simples a partir de 01/11/2026 pela Res. CGSN 191/2026; IBS/CBS em 2027 só em fonte secundária) são parâmetros com fonte e data de verificação, nunca constantes. | revisão de configuração | V-60. Verificado em cópia do DF, não no DOU |

## Requisitos de onboarding de tenant brasileiro (opcional)

| Enunciado | Verificação | Fonte |
| --- | --- | --- |
| O campo de documento da empresa aceita CNPJ numérico e alfanumérico (as 12 primeiras posições com letras ou números, dígitos verificadores numéricos), não usa coluna inteira e normaliza caixa. | testes de validação | brain `dominios.md` (MIT, conteúdo próprio; regra a reconferir na fonte oficial). Inferido |
| Virada de período de cobrança e relatórios usam o fuso do cliente. | teste de borda de período | brain `dominios.md`. Inferido |

## Critérios de aceite: molde

```text
Dado dois tenants, A (Acme Ltda, plano Pro com 10 assentos) e B (Acme Ltd, plano Free com 3 assentos),
  cada um com dados próprios,
Quando [usuário do A faz a ação],
Então [resultado esperado para A] e nenhum dado de B é lido, alterado ou inferido (404 para recurso de B),
  e [evento de auditoria] é registrado com o tenant A.
```

Controle positivo em cada cenário: o tenant B continua enxergando e operando os próprios dados.
