# Conciliação passo a passo, script executado e fluxo de estorno

Sumário: 1. Roteiro em 6 passos · 2. Script de exemplo (stdlib, executado) · 3. Fechamento diário por partição (SQL) · 4. Classificação das diferenças · 5. Fluxo de estorno ponta a ponta · 6. Conciliação Stripe por payout

Origem: V-07 (Stripe payouts), V-08 (bilateral, manifesto, `INCOMPLETE_SOURCE`, rmoff), V-67 (cadência), V-09 (disputa bloqueia estorno). A aplicação da metodologia de V-08 a pagamentos é **Inferido**. O bloco SQL da seção 3 é conteúdo próprio do usuário, reproduzido do brain-of-agent (`brains/qa/references/dominios.md`, seção "Dados, ETL e BI", MIT, Copyright (c) 2026 Brain of Agent contributors). O restante é redação própria. Conferido em 2026-10-10.

## 1. Roteiro em 6 passos

1. **Escolha a partição e o fuso** (dia em `America/Sao_Paulo`, filial, conta). Registre-os no relatório.
2. **Manifesto por fonte:** nome, contagem de linhas, soma em centavos, hash do arquivo, cursores de página, total de controle declarado pela fonte (se existir) e status. Um manifesto é imutável: se a fonte for recarregada, crie outro.
3. **Completude:** contagem recebida versus total de controle; paginação percorrida até o fim. Falhou: `INCOMPLETE_SOURCE`, o relatório diz "não conciliado" e a diferença zero não vale.
4. **Casamento nos dois sentidos** pela chave estável (nunca por posição ou só por valor).
5. **Classifique, proponha, aprove:** nada é aplicado sem aprovação; nenhuma linha de balanceamento automática.
6. **Reprocessamento:** rodar a mesma partição duas vezes deve dar as mesmas contagens e somas.

## 2. Script de exemplo (Python 3, stdlib; dados sintéticos; executado em 2026-10-10)

Mostra manifesto, `INCOMPLETE_SOURCE`, casamento bilateral e partição no fuso do negócio. No Windows o pacote `tzdata` pode faltar (`ZoneInfoNotFoundError` para `America/Sao_Paulo`); o esboço cai para UTC−3, válido só para datas sem horário de verão (o Brasil não tem desde 2019). Em produção, instale a base de fusos conforme a política do projeto.

```python
import csv, hashlib, io
from collections import defaultdict
from datetime import datetime, timedelta, timezone
try:
    from zoneinfo import ZoneInfo
    TZ = ZoneInfo("America/Sao_Paulo")       # partição = dia no fuso do negócio, nunca UTC por padrão
except Exception:
    TZ = timezone(timedelta(hours=-3))       # aproximação para datas sem horário de verão

def manifesto(nome, texto, total_esperado=None):
    linhas = list(csv.DictReader(io.StringIO(texto)))
    completo = total_esperado is None or len(linhas) == total_esperado
    return {"fonte": nome, "linhas": len(linhas), "soma": sum(int(l["valor_centavos"]) for l in linhas),
            "sha256": hashlib.sha256(texto.encode()).hexdigest()[:12],
            "status": "COMPLETA" if completo else "INCOMPLETE_SOURCE", "dados": linhas}

def particao(l):
    return datetime.fromisoformat(l["quando_utc"]).astimezone(TZ).date().isoformat()

def conciliar(a, b):
    """a = ledger, b = provedor/extrato; casa nos dois sentidos pela chave estável 'chave'."""
    idx = {}
    for nome, m in (("a", a), ("b", b)):
        d = defaultdict(list)
        for l in m["dados"]: d[l["chave"]].append(l)
        idx[nome] = d
    achados = []
    for k in sorted(set(idx["a"]) | set(idx["b"])):
        la, lb = idx["a"].get(k, []), idx["b"].get(k, [])
        if len(la) > 1 or len(lb) > 1: achados.append((k, "DUPLICATA", len(la), len(lb)))
        elif not lb: achados.append((k, "SO_NO_LEDGER", la[0]["valor_centavos"], None))
        elif not la: achados.append((k, "SO_NO_PROVEDOR", None, lb[0]["valor_centavos"]))
        elif la[0]["valor_centavos"] != lb[0]["valor_centavos"]:
            achados.append((k, "VALOR_DIFERENTE", la[0]["valor_centavos"], lb[0]["valor_centavos"]))
    return achados
```

Entrada sintética e saída observada: ledger com `tx1` (10000), `tx2` (2550), `tx3` (9990), `tx4` (500); provedor com `tx1` (10000), `tx2` (2500), `tx4` (500), `tx5` (700), com total de controle declarado de 5 e 4 linhas recebidas. Manifestos: ledger 4 linhas, soma 23040, `COMPLETA`; provedor 4 linhas, soma 13700, `INCOMPLETE_SOURCE`. Achados: `tx2 VALOR_DIFERENTE (2550 x 2500)`, `tx3 SO_NO_LEDGER`, `tx5 SO_NO_PROVEDOR`. Partições com `quando_utc` de `tx2` igual a `2026-10-01T02:10:00+00:00`: no fuso de São Paulo cai em 30/09, e não em 01/10. Resultado correto do relatório: "não conciliado (fonte incompleta)", mesmo que os achados acima tenham sido listados.

## 3. Fechamento diário por partição (SQL)

Fonte do bloco: brain-of-agent, MIT (ver cabeçalho). Rode na origem e no destino; o resultado precisa ser idêntico. Compare por partição (dia, filial), não só o total: totais iguais escondem erros que se compensam.

```sql
SELECT data_venda,
       COUNT(*)                    AS linhas,
       SUM(valor_centavos)         AS soma,
       COUNT(DISTINCT pedido_id)   AS pedidos,
       MIN(pedido_id), MAX(pedido_id)
FROM vendas
WHERE data_venda BETWEEN DATE '2026-09-01' AND DATE '2026-09-30'
GROUP BY data_venda
ORDER BY data_venda;
```

Adaptação do plugin: `data_venda` é a data no fuso do negócio (derivada de um instante UTC armazenado); acrescente a coluna `moeda` ao `GROUP BY` quando houver mais de uma moeda; para colunas transformadas, compare um hash por linha (por exemplo `md5` da concatenação das colunas normalizadas) e liste as chaves divergentes. Regras: divergência bloqueia a carga e gera alerta; reprocessar a partição dá as mesmas contagens (reprocessamento idempotente: apague a partição antes ou use `MERGE`, nunca `INSERT` cego); dado atrasado entra na partição de origem se estiver dentro da janela de reprocessamento definida. Para dbt, Great Expectations e SCD2, use o plugin `data-engineering`.

## 4. Classificação das diferenças

| Classe | Exemplo | Ação |
| --- | --- | --- |
| Só no ledger | pedido pago no sistema, sem linha no extrato | consultar o provedor; pode ser defasagem de liquidação; alerta se passar da janela |
| Só no provedor | liquidação sem pedido | procurar cobrança sem registro (webhook perdido, chave nova); registrar pendência |
| Valor diferente | 2550 contra 2500 | tarifa, câmbio, parcial ou erro de arredondamento; olhar a regra de alocação |
| Duplicata | mesma chave duas vezes de um lado | cobrança dupla possível: abrir caso com `payment-debugger` |
| Defasagem | D+1, D+30 | marcar `pendente_de_janela` com data limite |
| Tipo | tarifa, estorno, disputa, repasse | conciliar por tipo (Stripe: `charge`, `refund`, `stripe_fee`, `payout`) |

## 5. Fluxo de estorno ponta a ponta (pendência P1 do crítico; síntese de V-01, V-09, V-11, V-46, V-56)

1. **Autorizar e validar:** o chamador é dono do pedido (404 quando não é; reautenticação em estorno, **Inferido**); disputa aberta bloqueia estorno fora do processo; o valor é inteiro na menor unidade, não excede `original − estornos postados`. Efeito financeiro real exige confirmação humana com conta, modo, operação, valor e moeda; este plugin não executa.
2. **Reservar a intenção:** chave de idempotência do estorno persistida **antes** da chamada (Mercado Pago exige `X-Idempotency-Key` em Refunds, V-57); estado `refund_requested`.
3. **Chamar o provedor** fora de transação com lock. Timeout: estado desconhecido, consulta antes de repetir (`payment-idempotency`).
4. **Gravar o lançamento de estorno** (oposto, ligado ao original, `reverses_txn`) só com evidência: resposta, evento verificado e relido, ou consulta autenticada. Estorno parcial reduz o saldo estornável; soma acima do original é recusada.
5. **Webhook de estorno:** deduplique por ID, releia o recurso e converja para o estado real; o evento pode chegar antes da resposta síncrona (`webhook-handler`).
6. **Conciliar:** o estorno aparece no extrato do provedor como linha própria (Stripe: `refund`); casa com o lançamento nos dois sentidos; diferença vira caso classificado.
7. **Comunicação e trilha:** quem pediu, quem aprovou, motivo, horário, referência do provedor.

Não codifique prazos de estorno por bandeira ou por método sem conferir a documentação vigente (**Não verificado** neste plugin).

## 6. Conciliação Stripe por payout (V-07, Verificado)

1. Obtenha `po_...` pelo webhook `payout.reconciliation_completed`, pela listagem de payouts ou pelo extrato do banco. 2. Liste `balance_transactions` com `payout=po_...`, com paginação completa (padrão 10 por página; `limit` ou autopaginação). 3. Use `expand[]=data.source` para trazer o objeto de origem. 4. Classifique por tipo (`charge`, `refund`, `stripe_fee`, `payout`). 5. Compare com o ledger interno linha a linha. Só Stripe; sem fonte de adquirente brasileiro nem de arquivo de extrato bancário.
