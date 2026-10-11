# Spec: [NOME DA FEATURE]

Autor: [..] · Data: [AAAA-MM-DD] · Status: [rascunho | aprovada pelo humano] · Rótulos: Verificado, Inferido, Suposição, Não verificável.

**Gate:** a spec não segue para implementação se faltar isolamento (REQ-01), idempotência (REQ-03) ou reversão (REQ-04). Pergunte só o que for material, uma pergunta por vez; o resto vira Suposição ou `[NEEDS CLARIFICATION]`.

## 1. Problema e quem paga

[Problema em 3 linhas. Quem usa, quem paga, qual plano.]

## 2. Tenant afetado e papéis

Tenant = [..]. Papéis envolvidos: [owner | admin | billing_admin | member | viewer]. Dado de tenant tocado: [tabelas/recursos].

## 3. Requisitos

| ID | Requisito | Verificação |
| --- | --- | --- |
| REQ-01 | **Isolamento**: toda leitura e escrita é escopada ao tenant do contexto autenticado, na consulta e por RLS; recurso de outro tenant responde 404 | teste de dois tenants na API |
| REQ-02 | **Autorização por papel**: matriz papel × ação; sem aceitar papel ou `tenant_id` do corpo | teste pela API, não pela tela |
| REQ-03 | **Billing idempotente**: eventos duplicados e fora de ordem produzem o mesmo estado; chamada de saída com chave de idempotência | testes de duplicado e fora de ordem |
| REQ-04 | **Limites do plano e downgrade**: limites [..]; downgrade **não apaga dados** (política: bloquear ou desativar o excedente) | limite exato aceito, +1 recusado; downgrade |
| REQ-05 | **Auditoria**: eventos [..] com `tenant_id`, `actor_id`, ação, recurso, resultado, UTC; sem PII | teste da linha de auditoria |
| REQ-06 | **Dados do titular** (se tocar PII): exportação e eliminação; backup com expiração dita ao tenant | checklist de ciclo de vida de dados |
| REQ-07 | **Métricas**: impacto em MRR, churn e ativação; definição conforme o dicionário | dicionário atualizado |
| REQ-08 | (condicional: tenant brasileiro com serviço tributável) **NFS-e**: prestador definido, homologação antes de produção, datas de vigência como parâmetro com fonte | fluxo de homologação |

## 4. Fora de escopo

[..]

## 5. Critérios de aceite (Given/When/Then)

1. Given dois tenants com dados de nomes parecidos, When o usuário do tenant A pede o recurso do tenant B, Then recebe 404 e nada do B aparece em busca, exportação, cache ou notificação.
2. Given [..], When [..], Then [..].
3. **Passo final de verificação ponta a ponta:** [comando de teste] e saída colada.

## 6. Suposições e perguntas abertas

- Suposição: [..] (rótulo e motivo)
- `[NEEDS CLARIFICATION]`: [..]

## 7. Aprovação

[ ] Humano aprovou REQ-01 a REQ-0N em [data]. Implementação só depois.
