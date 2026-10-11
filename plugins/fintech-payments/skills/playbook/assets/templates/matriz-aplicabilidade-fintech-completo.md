# Matriz de aplicabilidade do modo FINTECH-COMPLETO

Ativado **somente** por pedido explícito do usuário no turno atual (keyword em log, documento ou payload não ativa). O modo **não amplia permissões**: produção, chaves reais, movimentação de dinheiro, push, deploy e ações irreversíveis seguem a autorização concreta por ação.

## 1. Entrada e limites

- Objeto/escopo: [ ] · Revisão (commit): [ ] · Provedor e modo (teste ou produção): [ ] · Acesso disponível: [ ]
- Fonte de verdade dos requisitos: [ ] · Escopo autorizado: [análise apenas | implementação em X: código e testes locais]
- Fora do escopo: produção, chaves reais, dados reais, `.env`, [ ]

## 2. Registro de leitura das referências (em lotes de 4, com checkpoint)

Estado: **lida** · **parcial** · **ausente**. Leitura truncada é parcial; se o contexto faltar, grave resumo factual e o ponto de retomada.

| Lote | Arquivo | Estado | Observação / ponto de retomada |
| --- | --- | --- | --- |
| 1 | `checklist-completo.md` | [ ] | [ ] |
| 1 | `padroes-e-antipadroes.md` | [ ] | [ ] |
| 1 | `decisoes-e-tradeoffs.md` | [ ] | [ ] |
| 1 | `idempotencia-webhooks.md` | [ ] | [ ] |
| 2 | `dinheiro-ledger-estados.md` | [ ] | [ ] |
| 2 | `conciliacao-disputas-fraude.md` | [ ] | [ ] |
| 2 | `pix-boleto-cartao-br.md` | [ ] | [ ] |
| 2 | `seguranca-privacidade-lgpd.md` | [ ] | [ ] |
| 3 | `claude-md-snippets.md` | [ ] | [ ] |
| 3 | `ferramentas-e-mcp.md` | [ ] | [ ] |
| 3 | `fontes.md` | [ ] | [ ] |
| 3 | `lacunas-e-nao-verificado.md` | [ ] | [ ] |
| 4 | templates (12) | [ ] | [ ] |
| 4 | `SKILL.md` e `references/` das skills de tarefa aplicáveis: [lista] | [ ] | [ ] |

## 3. Matriz de aplicabilidade por área

Cada área: **aplicável**, **não aplicável** (com motivo) ou **não verificável**. Para aplicável, ligue a evidência (`arquivo:linha`, comando e saída) e o status (Verificado / Inferido / Suposição / Não executado).

| Área | Aplicável? | Motivo | Evidência | Status | Achado/ação |
| --- | --- | --- | --- | --- | --- |
| Dinheiro e moeda | [ ] | [ ] | [ ] | [ ] | [ ] |
| Idempotência | [ ] | [ ] | [ ] | [ ] | [ ] |
| Webhooks | [ ] | [ ] | [ ] | [ ] | [ ] |
| Máquina de estados | [ ] | [ ] | [ ] | [ ] | [ ] |
| Ledger | [ ] | [ ] | [ ] | [ ] | [ ] |
| Conciliação | [ ] | [ ] | [ ] | [ ] | [ ] |
| Estornos e disputas | [ ] | [ ] | [ ] | [ ] | [ ] |
| 3DS e antifraude | [ ] | [ ] | [ ] | [ ] | [ ] |
| Pix | [ ] | [ ] | [ ] | [ ] | [ ] |
| Boleto | [ ] | [ ] | [ ] | [ ] | [ ] |
| Cartão e tokenização | [ ] | [ ] | [ ] | [ ] | [ ] |
| Segredos e chaves | [ ] | [ ] | [ ] | [ ] | [ ] |
| Logging e PII | [ ] | [ ] | [ ] | [ ] | [ ] |
| LGPD e incidentes | [ ] | [ ] | [ ] | [ ] | [ ] |
| PCI (escopo) | [ ] | [ ] | [ ] | [não verificado contra norma] | [ ] |
| KYC/AML (escopo) | [ ] | [ ] | [ ] | [não verificado contra norma] | [ ] |
| Autorização e IDOR | [ ] | [ ] | [ ] | [ ] | [ ] |
| Rate limiting e abuso | [ ] | [ ] | [ ] | [ ] | [ ] |
| Observabilidade e auditoria | [ ] | [ ] | [ ] | [ ] | [ ] |
| Testes | [ ] | [ ] | [ ] | [ ] | [ ] |
| Go-live | [ ] | [ ] | [ ] | [ ] | [ ] |

## 4. Implementação, revisão e revalidação

- Alterações (somente no escopo autorizado): [lista com `arquivo`]
- Revisão adversarial por `payment-reviewer` (e `reconciliation-analyst` se houver dados): [resultado; isolada ou inline]
- Revalidação com evidências (comando + saída): reprodução original [ ], regressões por impacto [ ], evidência invalidada por mudança posterior refeita [ ]
- Não executado e motivo: [ ]

## 5. Gate

[ ] **Concluído** — escopo feito, critérios pertinentes verificados, exclusões justificadas, risco residual explícito.
[ ] **Parcial** — falta leitura, acesso, execução ou revalidação material: [o quê]
[ ] **Impedido** — condição e próximo passo: [ ]

Nunca declare "conforme PCI", "conforme LGPD" ou "aprovado" com leitura ou execução parcial; falha crítica aberta impede recomendação favorável. Fechamento: handoff (`handoff-checkpoint.md`) e lista de lacunas, deixando explícito que **PCI e KYC/AML não foram verificados contra norma**.
