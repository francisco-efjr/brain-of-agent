# Máquina de estados do tenant

Design nosso, **Inferido** de `V-30` (a Azure descreve fases, não estados). Prazos e gatilhos finais são decisão de produto e jurídico (Suposição até definir). Regra de ferro: desativar não apaga; downgrade não apaga; cobrança falha desativa; eliminação só após retenção e instrução do controlador, com autorização concreta.

Produto: [..] · Estados adicionais do produto: [..]

## Estados

| Estado | Significado | Acesso dos membros | Dados | Reversível? |
| --- | --- | --- | --- | --- |
| `trial` | período de teste | liberado com limites | preservados | sim |
| `active` | assinatura vigente | liberado | preservados | sim |
| `deactivated` | acesso suspenso (falta de pagamento, pedido do tenant, abuso) | bloqueado; admin vê tela de regularização | preservados | sim |
| `offboarding` | cancelamento definitivo, em período de retenção | bloqueado; exportação disponível | preservados até o fim da retenção | até o fim da retenção |
| `deleted` | eliminação concluída | n/a | eliminados (banco, storage, caches, índices, réplicas); backups expiram em [prazo] | não |

## Transições

| De → Para | Gatilho | Dono | Dado afetado | Evento de auditoria | Teste |
| --- | --- | --- | --- | --- | --- |
| `trial` → `active` | primeira cobrança paga (webhook) | billing | `tenant_billing`, `tenant_features` | `tenant.activated` | |
| `trial` → `deactivated` | trial expira sem meio de pagamento | billing | acesso | `tenant.deactivated` | |
| `active` → `deactivated` | `unpaid`/`paused`, pedido, abuso | billing ou suporte | acesso | `tenant.deactivated` (motivo) | |
| `deactivated` → `active` | regularização | billing | acesso | `tenant.reactivated` | |
| `deactivated` → `offboarding` | cancelamento definitivo ou fim da tolerância | produto e jurídico | início da retenção | `tenant.offboarding_started` | |
| `offboarding` → `deleted` | fim da retenção **e** instrução do controlador | operador, com autorização humana | eliminação completa | `tenant.deleted` (escopo e resultado) | |
| `offboarding` → `active` | reonboarding dentro da retenção | billing | restauração | `tenant.reactivated` | |

## Diagrama (texto)

```text
trial ──paga──▶ active ◀──regulariza── deactivated
  │                │                        │
  └─sem pagamento──┴──falha/pedido/abuso───▶│
                                            ▼
                        offboarding ──(retenção + instrução)──▶ deleted
                              │
                              └──reonboarding──▶ active
```

## Perguntas de entrada do onboarding (V-30)

Residência de dados · compliance · RTO/RPO · plano de cobrança · ambiente de homologação · informações necessárias · self-service ou manual · trial: mesmos requisitos de segurança e SLA? infraestrutura compartilhada? como evitar abuso?

## Onboarding idempotente

signup → organização (tenant) → membro dono → Customer com `metadata.tenant_id` → `tenant_features` iniciais → convites. Cada passo grava progresso e usa chave de idempotência por operação; falha no meio não deixa tenant órfão nem Customer duplicado.
