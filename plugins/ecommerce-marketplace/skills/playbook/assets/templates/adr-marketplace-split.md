# ADR: modelo de cobrança e split do marketplace

Uso: decisão material de marketplace multi-seller. **Somente decisão**: nenhuma cobrança, conta conectada, transferência ou estorno real é criada. Base: V-11, V-29, V-47, V-36. Provedores sem leitura da documentação ficam "Não verificado". A decisão final é humana (responsável pelo produto, jurídico e financeiro).

- Status: [proposto | aprovado | substituído] · Data: [AAAA-MM-DD] · Decisores: [NOMES] · País do vendedor/comprador: [BR/…]

## 1. Contexto
- Modelo de negócio: [DESCRIÇÃO] · Volume esperado: [X] · Meios de pagamento: [Pix, boleto, cartão] · PSP candidato(s): [LISTA]

## 2. As 4 perguntas
| # | Pergunta | Resposta | Consequência |
| --- | --- | --- | --- |
| 1 | O comprador sabe que compra do vendedor ou da plataforma? | [X] | direct × destination/indireta |
| 2 | Um pagamento é dividido entre vários vendedores (carrinho multi-seller)? | [SIM/NÃO] | sim ⇒ cobranças e transferências separadas |
| 3 | A transferência pode ocorrer antes da liquidação ou antes de saber o vendedor? | [SIM/NÃO] | sim ⇒ separadas |
| 4 | Quem arca com reembolso, contestação e tarifas? | [PLATAFORMA/VENDEDOR] | define quem é debitado |

## 3. Alternativas
| Opção | Prós | Contras | Rótulo da evidência |
| --- | --- | --- | --- |
| [Direct] | | | [Verificado V-11 / Não verificado no Brasil] |
| [Destination] | | | |
| [Separadas] | | | |
| [Mercado Pago Split 1:1] | Lista Brasil (V-36) | Só 1:1; saldo negativo do vendedor a definir (V-47) | Verificado |
| Alternativa mais simples: [EX.: vender como loja única, sem marketplace] | | | |

## 4. Decisão
- Escolha: [OPÇÃO] · Motivo: [UMA FRASE] · Não escolhidas porque: [UMA FRASE POR OPÇÃO]

## 5. Fluxo de fundos
```text
[DIAGRAMA EM TEXTO: comprador → PSP → plataforma → vendedor; comissão; momento da transferência]
```

## 6. Quem é debitado, por evento
| Evento | Debitado | Observação |
| --- | --- | --- |
| Reembolso total | [X] | |
| Reembolso parcial | [X] | soma ≤ capturado |
| Contestação (chargeback) | [X] | prazo e disputa |
| Tarifa do PSP | [X] | |
| Saldo negativo do vendedor | [X] | **definir antes do go-live** |

## 7. Onboarding e KYC
- Tipo: [hospedado | embutido | API (revisão de requisitos ≥ semestral)] · Coleta: [antecipada `eventually_due` | incremental `currently_due`]
- Regra: ler o estado de requisitos antes de liberar repasse; bloquear venda com pendência vencida. KYC do provedor não substitui LGPD, fiscal e antifraude.

## 8. Fiscal e frete
- Papel fiscal da plataforma: ver [adr-papel-fiscal-plataforma.md](adr-papel-fiscal-plataforma.md) · Frete por vendedor: [COMO COTA E QUEM CONTRATA]

## 9. Não verificado
- [Ex.: disponibilidade do Stripe Connect no Brasil; Pagar.me split; Mirakl API; reentrega do canal X]

## 10. Riscos e próximos passos
- Efeitos reais (estorno, repasse) só com aprovação humana · Revisão jurídica/fiscal: [PENDENTE/FEITA] · Próximo passo: [AÇÃO]
