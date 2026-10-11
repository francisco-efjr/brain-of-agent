# Exemplo preenchido: ADR de modelo de tenancy híbrido

Exemplo ilustrativo (caso de eval `adr-schema-por-tenant`). Os números vêm do enunciado do caso, não de medição; os limiares são Suposição. Trate como molde de forma e de nível de detalhe, não como decisão para o seu produto.

---

# ADR 0003: modelo de tenancy

Status: proposto · Data: AAAA-MM-DD · Decisores: [nomes] · Rótulos: Verificado (lido em fonte ou contrato), Inferido, Suposição, Relato.

## Contexto e definição de tenant

Produto B2B de [domínio]. Tenant = a empresa cliente (uma assinatura, um domínio de SSO). Um cliente com várias empresas do grupo tem vários tenants ligados a uma conta de cobrança (Suposição: confirmar com o comercial).

## Requisitos

| Requisito | Origem | Rótulo |
| --- | --- | --- |
| 200 clientes hoje; 5.000 em 3 anos | enunciado | Suposição (projeção comercial) |
| 3 clientes exigem dados separados por contrato | enunciado | Verificado se o contrato foi lido; senão Suposição |
| 4 desenvolvedores, Postgres | enunciado | Verificado |
| Sem equipe de operação dedicada | inferido do tamanho do time | Suposição |
| Exclusão e restauração por tenant em prazo contratual | LGPD/GDPR (V-27, V-28) | Inferido |

## As seis respostas (V-07)

1. Tenant = empresa cliente. 2. Separação física: exigida por 3 contratos. 3. 200 para 5.000; maior tenant: desconhecido (pedir métrica). 4. Isolamento é vendido? Hoje por contrato sob medida; passará a plano enterprise (Suposição). 5. Compartilhável: interface e aplicação; dados dedicados só para os 3. 6. Mapeamento por claim do token validado e lookup em tabela tenant para deployment.

## Opções consideradas (camada de dados)

| Opção | Resultado | Motivo |
| --- | --- | --- |
| Pool com RLS para todos | Insuficiente sozinha | Não cumpre os 3 contratos de separação física |
| Banco por tenant para todos | Rejeitada | 5.000 bancos exigem automação e operação que 4 pessoas não sustentam (Suposição) |
| Schema por tenant para todos | Rejeitada como padrão | Custo de migração por schema e limites de locks e memória relatados por praticantes (Relato, V-44); equipe pequena |
| Tabela ou coluna por tenant | Rejeitada | Antipadrão (V-33) |
| Híbrido: pool com RLS como padrão e banco dedicado para os 3 | Escolhida | Atende contrato, mantém custo e operação no padrão |

## Decisão

- Dados: pool com RLS (Postgres) para todos os tenants comuns; `ENABLE` e `FORCE ROW LEVEL SECURITY`, `USING` e `WITH CHECK`, contexto por transação, role de runtime sem `BYPASSRLS` (V-01, V-34, V-49). Banco dedicado (silo de dados) para os 3 tenants com cláusula contratual, no mesmo cluster gerenciado ou em outro, conforme o contrato.
- Aplicação e interface: compartilhadas. A aplicação resolve o DSN pelo mapa tenant para deployment; o segredo mora no cofre.
- Migração de schema: automatizada, aplicada em todos os deployments pela mesma ferramenta, com `schema_version` por tenant; a aplicação aceita a versão anterior do schema durante a janela (V-33).
- Arquivos: prefixo `tenants/<tenant_id>/` no bucket compartilhado; bucket separado para os 3 se o contrato exigir.

## Mapa tenant para deployment

| tenant_id | deployment_id | tier | db_ref | schema_version |
| --- | --- | --- | --- | --- |
| (maioria) | pool-01 | pool | cofre://db/pool-01 | 2026.10.1 |
| T-A, T-B, T-C | silo-a, silo-b, silo-c | silo | cofre://db/silo-a ... | 2026.10.1 |

Roteamento: o tenant sai do claim do token validado; a aplicação consulta o mapa em cache com invalidação por mudança e abre a conexão do deployment correspondente. Subdomínio e claim divergentes recusam (Inferido, V-32). Cada rota confere audience e scope.

## Consequências

Positivas: contrato atendido; custo e operação do pool preservados. Negativas: dois caminhos de conexão para testar; mapa tenant para deployment passa a ser dependência crítica (disponibilidade e cache); migrações precisam rodar em N deployments com falha isolada e reexecução.

## Critérios de mudança de modelo (gatilhos; limiares são Suposição)

- Novo contrato com isolamento físico: promover o tenant a silo pelo plano de migração abaixo.
- Tenant do pool com consumo anormal e recorrente na métrica por tenant (V-09): aplicar limite do plano; se persistir, promover a silo.
- Mais de [N] tenants em silo (N definido pelo time): rever automação e custo; considerar bridge.

Plano de promoção pool para silo: provisionar banco; copiar dados filtrando por `tenant_id`; validar contagens por tabela; congelar escrita por janela curta; trocar a linha do mapa; testar com dois tenants; manter o caminho de volta por [prazo]; apagar do pool após retenção, com evento de auditoria.

## Riscos e questões abertas

| Item | Dono | Prazo | Rótulo |
| --- | --- | --- | --- |
| Maior tenant atual e seu consumo | [nome] | [data] | pendente |
| Contratos dos 3 clientes dizem "instância dedicada" ou "banco dedicado"? | jurídico/comercial | [data] | pendente |
| Backup e exclusão por tenant no pool (backups não somem ao apagar linha; declarar expiração) | [nome] | [data] | Inferido |
| Teste do contexto por transação com o pooler real (pool de tamanho 1) | [nome] | antes do go-live | Não verificável sem teste (V-47) |

## Ligações

Vizinho barulhento: limites por tenant e plano (V-09). Ciclo de vida: estados em `tenant_deployments.state` (V-30). Billing: Customer Stripe por tenant com `metadata.tenant_id`, Inferido de V-39. Testes: matriz de dois tenants, inclusive um tenant do silo e um do pool.

Esta decisão é uma proposta de arquitetura; não substitui revisão por pessoa responsável nem avaliação jurídica dos contratos.
