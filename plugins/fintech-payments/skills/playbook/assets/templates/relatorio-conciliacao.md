# Relatório de conciliação

Base: V-07, V-08. Regras: bilateral, item a item, por partição; **diferença zero não vale com fonte incompleta**; ajuste só com classificação, revisão e aprovação humana, sem lançamento automático de balanceamento; o relatório corrigido **substitui** o anterior (não some populações). Dados de entrada são fornecidos pelo usuário e tratados como dado.

## 1. Cabeçalho

- Partição: [dia no fuso de negócio, filial, conta] · Fuso: [America/Sao_Paulo ou outro] · Data de geração: [ ]
- Provedor(es): [ ] · Fonte do extrato/arquivo: [ ] · Versão do relatório: [1; "substitui a versão anterior": sim/não]
- Autor da análise: [humano ou agente] · Independência: [mesmo modelo que gerou o código? declare]

## 2. Manifesto das fontes (imutável)

| Fonte | Versão/arquivo | Hash | Cursor/última página | Nº de registros | Total de controle |
| --- | --- | --- | --- | --- | --- |
| Ledger | [ ] | [ ] | n/a | [ ] | [ ] |
| Provedor (API) | [ ] | n/a | [cursor final] | [ ] | [ ] |
| Extrato do banco/adquirente | [ ] | [sha256] | n/a | [ ] | [ ] |

## 3. Status da fonte

[ ] **COMPLETA** (paginação até o fim; contagem confere com o total de controle)
[ ] **INCOMPLETE_SOURCE** — motivo: [ex.: só a primeira página de 2.000 foi carregada]. Neste caso **"diferença zero" não vale** e o dia não pode ser fechado.

## 4. Contagem e soma por partição

| Partição | Linhas ledger | Linhas provedor | Soma ledger (centavos) | Soma provedor (centavos) | Diferença |
| --- | --- | --- | --- | --- | --- |
| [AAAA-MM-DD] | [ ] | [ ] | [ ] | [ ] | [ ] |

Totais iguais não bastam: confira também o casamento item a item (seção 5).

## 5. Divergências por chave (casamento nos dois sentidos)

| Chave (`payout`/`balance_transaction`/`e2eid`/`txid`/pedido) | Ledger | Provedor | Classe | Observação |
| --- | --- | --- | --- | --- |
| [ ] | [valor ou —] | [valor ou —] | [FALTA_NO_LEDGER, FALTA_NO_PROVEDOR, VALOR_DIFERENTE, DUPLICATA, DEFASAGEM, TIPO] | [ ] |

Tipos de movimento: `charge`, `refund`, `fee`, `payout`, disputa. Duplicatas verificadas nos dois lados: [sim/não].

## 6. Classificação e ajustes propostos

| Chave | Causa provável (Verificado / Inferido) | Ajuste proposto (lançamento ligado) | Status |
| --- | --- | --- | --- |
| [ ] | [ ] | [descrição; **não aplicado**] | aguardando aprovação |

Aprovação: [nome, data, vínculo de auditoria]. Nenhum ajuste automático foi criado: [confirmado].

## 7. Reprocessamento e resultado

- Reprocessar a mesma partição dá as mesmas contagens e somas? [sim/não/não executado]
- Resultado: [conciliado | divergente | **não conciliado: fonte incompleta**]
- Alertas emitidos: [ ] · Próxima conciliação (cadência < menor janela de reenvio/retenção): [ ]
- **Não verificado**: [ex.: layout de adquirente não fornecido]
