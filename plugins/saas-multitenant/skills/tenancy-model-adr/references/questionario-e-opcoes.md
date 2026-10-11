# Questionário, opções por camada e regras de decisão

Redação própria, destilada de V-07, V-33, V-44, V-32, V-09, V-30, V-39, V-49. Conferido em 2026-10-10. Rótulos: Verificado (lido na fonte), Inferido (nosso), Suposição, Relato (praticante, V-44).

## 1. As seis perguntas de V-07 e como cada resposta pesa

| # | Pergunta | Por que perguntar | Como a resposta muda a decisão |
| --- | --- | --- | --- |
| 1 | Quem é o tenant? Um cliente pode ter vários? | Define a chave de isolamento e o modelo de cobrança | Vários tenants por cliente pedem entidade "conta" acima do tenant (cobrança e SSO no nível da conta) |
| 2 | Há exigência regulatória ou contratual de separação física? | Isolamento lógico (RLS) não atende cláusula de "dados em instância dedicada" | Sim para qualquer tenant: silo para ele; padrão continua pool para os demais (modelo híbrido) |
| 3 | Quantos tenants em 3 anos e qual o maior? | Escala e dispersão de tamanho | Poucos e grandes tendem a silo ou bridge; muitos e pequenos, pool. Limiares exatos: Suposição (medir) |
| 4 | Isolamento é vendido como plano (enterprise)? | Define se o produto precisa de dois modelos desde o início | Sim: projete o mapa tenant para deployment já, mesmo que todos comecem no pool |
| 5 | O que pode ser compartilhado por camada? | Isolamento é um espectro e pode variar por camada | Ex.: interface e aplicação compartilhadas, dados dedicados (particionamento horizontal) |
| 6 | Como mapear requisição para tenant e para deployment? | Sem isso, nenhum modelo funciona | Ver seção 5; tenant sai de credencial validada (V-32) |

Perguntas extras que mudam a decisão: equipe sabe operar muitos bancos? Há requisito de restaurar um único tenant? Há exclusão por tenant com prazo contratual (LGPD, GDPR)? O produto permite customização de schema por tenant? (customização por tenant favorece silo ou bridge; a Azure recomenda feature flags e configuração por tenant no lugar de infraestrutura customizada, V-33.)

## 2. Opções para a camada de dados

| Opção | Descrição | Prós | Contras | Fonte e rótulo |
| --- | --- | --- | --- | --- |
| A. Pool com RLS | Banco e schema compartilhados; `tenant_id` em toda tabela; filtro na aplicação mais RLS no banco | Densidade e custo menor; uma migração para todos; agilidade | Impacto entre tenants (vizinho barulhento); desafios de compliance; disponibilidade tudo-ou-nada; exige disciplina de contexto por transação e role correta | V-33 (AWS pool, Azure banco compartilhado), V-01. Verificado |
| B. Pool só com filtro na aplicação | Igual a A sem RLS | Mais simples | Um `WHERE` esquecido é falha total; sem segunda barreira | V-33 (AWS: RLS necessário no pool), V-08. Não recomendado |
| C. Schema por tenant (bridge) | Um banco, um schema por tenant | Apagar, fazer backup e restaurar por tenant; índices menores; caminho para sharding | Código de migração por schema; extensões; `pg_stat_statements` ruim; limite de locks; memória e I/O; sem FK entre schemas | V-44. Relato de praticante; não é a recomendação padrão |
| D. Banco por tenant (silo de dados) | Um banco (ou cluster) por tenant, aplicação compartilhada | Isolamento forte, ajuste por tenant, compliance | Custo; implantação complexa; automação obrigatória; roteamento de conexão | V-33 (AWS silo, Azure banco dedicado). Verificado |
| E. Deployment dedicado (stamp) | Pilha inteira dedicada (aplicação e dados) | Isolamento máximo, SLA próprio, residência | Operação multiplicada; releases por deployment | V-07 (stamps). Verificado |
| X. Tabela por tenant / coluna por tenant | Criar tabelas ou colunas por cliente | Nenhum | Antipadrão listado | V-33 (Azure). Nunca |

Regra de ADR (V-33): pool com RLS para planos comuns; silo para tenant com chave própria, residência de dados ou exigência de isolamento físico; nunca tabela por tenant; migração de schema automatizada com versão registrada por tenant.

## 3. Camadas além dos dados

| Camada | Opções | Notas |
| --- | --- | --- |
| Interface | compartilhada com tema por tenant; domínio próprio por tenant | Domínio próprio exige certificado e roteamento; Auth0 não oferece domínio de login por organização (V-31) |
| Aplicação | compartilhada; instância dedicada para tenants grandes | Dedicada resolve vizinho barulhento de CPU e memória; mantém o mesmo código |
| Dados | seção 2 | Pode divergir da aplicação |
| Armazenamento de arquivos | prefixo por tenant no bucket; bucket por tenant | Bucket por tenant simplifica chave própria e exclusão; custo de gestão |
| Cache e filas | chave com tenant; instância dedicada para silo | V-49: tenant na chave, namespace global explícito |
| Identidade | IdP compartilhado com organizações; conexão SSO por organização | V-31 |

## 4. Quando mudar de modelo (gatilhos, todos Suposição até haver medição)

Gatilhos a registrar no ADR, com dono e fonte de medição:

- Contrato exige isolamento físico, chave própria ou residência: tenant sai do pool para silo (cláusula, não métrica).
- Um tenant usa fração anormal da capacidade compartilhada de forma recorrente (métrica por tenant, V-09): mover para silo ou instância dedicada ou aplicar limite por plano antes.
- Custo de migração por tenant ou de operação do schema por tenant passa de um limite que o time define.
- Necessidade de restauração e exclusão individuais com SLA que o pool não cumpre (Inferido).

Plano de migração entre modelos (esqueleto): congelar escrita do tenant ou usar dupla escrita; copiar dados filtrando por `tenant_id`; validar contagens por tabela e checksums; trocar o roteamento no mapa tenant para deployment; manter o caminho de volta por uma janela; apagar do modelo antigo só depois da retenção; teste com dois tenants antes e depois. Cada passo com dono e evento de auditoria (V-30, V-41).

## 5. Mapa tenant para deployment e mapeamento da requisição

Tabela de roteamento mínima (nossa, Inferida de V-07 e V-32):

| Coluna | Uso |
| --- | --- |
| `tenant_id` | chave |
| `deployment_id` | stamp ou cluster onde o tenant vive |
| `data_region` | residência |
| `db_ref` | referência ao segredo/DSN no cofre (nunca o DSN em texto no banco) |
| `schema_version` | versão de schema aplicada ao tenant |
| `tier` | pool, bridge ou silo |
| `state` | trial, active, deactivated, offboarding, deleted (V-30) |

Como a requisição chega ao tenant (V-32, Verificado): domínio, caminho, query string, header customizado, claim de token, chave de API com lookup ou HMAC, certificado de cliente. Header customizado não serve em GET de navegador nem atrás de proxy que o altere; chave de API "não oferece nível alto de segurança" e a página prefere OAuth 2.0 ou OIDC com token de vida curta; usar frameworks de autenticação confiáveis, sem escrever validação de assinatura. Regra do plugin: o tenant sai do claim do token validado, ou de lookup pela identidade do token; nunca de query string, header livre ou corpo; subdomínio e claim divergentes recusam (Inferido). Cada rota confere audience e scope, porque mapear o tenant não autoriza a requisição.

## 6. Lista de consistência final do ADR

- Cada requisito mapeado a decisão; cada tier tem critério de entrada.
- Há dono e prazo para cada questão aberta.
- Os testes que provam a decisão estão nomeados (dois tenants, pool de tamanho 1 se houver RLS, roteamento por tenant).
- Os efeitos em billing (Customer por tenant), ciclo de vida (estados), vizinho barulhento (limites) e observabilidade (métrica por tenant) estão escritos.
