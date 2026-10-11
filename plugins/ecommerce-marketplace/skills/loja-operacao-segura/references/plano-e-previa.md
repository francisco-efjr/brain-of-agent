# Plano, prévia e releitura de mudança em lote

Modelo-alvo e data de validação: Claude 4.x/5.x, 2026-10-10. O gate de 7 passos é **redação própria do plugin** (V-18, V-44): `dry_run` com esse nome não existe no SKILL.md raiz de `shopify-admin-skills` (score 42 em V-44); o modelo somente leitura vem de `shopify-catalog-audit` (escopo `read_products`, "nunca mutar", verificação pela Admin API). O padrão de ledger com estado por item, checagem de frescor e reversão vem de um projeto minúsculo (V-20, Classe C, 1 estrela): **padrão, não evidência**. Os scripts abaixo foram **executados em 2026-10-10** (Python 3.14) sobre CSVs sintéticos; não tocam em nenhuma loja. Adapte colunas ao export real da plataforma e confira a doc da versão da API.

## 1. Plano preenchido (exemplo sintético)

```markdown
# Plano de mudança em lote: +10% nos preços da coleção "Verão"
Ambiente: loja de DESENVOLVIMENTO (live bloqueado por padrão)   Plataforma: Shopify, Admin API <aaaa-mm registrada>
Credencial: variável SHOP_ADMIN_TOKEN_RO (somente leitura nos passos 1-3); a de escrita só no passo 5, fornecida pelo usuário
Escopo exato: produtos da coleção "Verão" (ID <a confirmar>), todas as variantes; regra: +10%, meio para cima, em centavos inteiros; teto de variação por item 20%
Critério de aceite: releitura pela API mostra preço novo = preço do diff em 100% dos itens; zero faltando/extras
Janela: terça 02h-04h (menor tráfego); responsável acompanhando: <nome>
Efeitos colaterais: webhooks de produto atualizado, feed do Merchant Center, sincronização do ERP (pausar? decisão: <...>)

1 Escopo mínimo: token RO; coleção Verão; dev store                      -> OK / Pendente
2 Contagem: esperado 142 variantes · encontrado <N>                      -> parar se divergir
3 Prévia: dry_run_preco.py -> diff.csv (itens, soma antes/depois)        -> anexar resumo
4 Confirmação: "Confirma aplicar +10% a 142 variantes (soma R$ X -> R$ Y)? Backup: export-2026-10-10.csv" -> aguardar "sim"
5 Execução: canário de 5 -> releitura -> lotes de 25; chave: <mudanca_id>-<variant_id>
6 Releitura: comparar_releitura.py diff.csv relido.csv
7 Desfazer: reaplicar "antes" do ledger/backup nos itens com estado aplicado/verificado; testado em 5 itens
Não verificado: <lista>
```

## 2. Prévia (dry run) de preço: script executado

Lê o CSV exportado (colunas `id`, `sku`, `preco`), aplica o reajuste em pontos-base, valida e grava o diff. Não escreve na loja. Aborta (código de saída 1, nada gravado) em: contagem divergente do esperado, preço vazio, ilegível, zero ou negativo, e variação acima do teto.

```python
#!/usr/bin/env python3
"""Prévia (dry run) de reajuste de preço a partir de uma exportação CSV. Não toca em loja nenhuma."""
import argparse, csv, sys
from decimal import Decimal, InvalidOperation

def para_centavos(texto):
    try:
        return int((Decimal(texto.strip().replace(",", ".")) * 100).to_integral_value())
    except (InvalidOperation, AttributeError):
        raise ValueError(f"preço ilegível: {texto!r}")

def reajustar(centavos, bps):            # bps = pontos-base; 1000 = +10%; meio para cima
    return (centavos * (10000 + bps) + 5000) // 10000

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--entrada", required=True); p.add_argument("--saida", required=True)
    p.add_argument("--bps", type=int, required=True); p.add_argument("--esperado", type=int, required=True)
    p.add_argument("--teto-bps", type=int, default=2000, help="aborta se algum item variar mais que isso")
    a = p.parse_args()
    with open(a.entrada, newline="", encoding="utf-8") as f:
        linhas = list(csv.DictReader(f))
    erros = []
    if len(linhas) != a.esperado:
        erros.append(f"contagem divergente: exportação={len(linhas)} esperado={a.esperado}")
    saida = []
    for i, l in enumerate(linhas, start=2):
        try:
            antes = para_centavos(l["preco"])
            if antes <= 0:
                raise ValueError("preço zero ou negativo")
            depois = reajustar(antes, a.bps)
            if abs(depois - antes) * 10000 > antes * a.teto_bps:
                raise ValueError("variação acima do teto")
            saida.append({"id": l["id"], "sku": l["sku"], "antes": antes, "depois": depois})
        except (ValueError, KeyError) as e:
            erros.append(f"linha {i} (sku={l.get('sku')}): {e}")
    if erros:
        print("ABORTADO, nada gravado:", *erros[:20], sep="\n  "); sys.exit(1)
    with open(a.saida, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id", "sku", "antes", "depois"]); w.writeheader(); w.writerows(saida)
    print(f"itens={len(saida)} soma_antes={sum(r['antes'] for r in saida)} soma_depois={sum(r['depois'] for r in saida)}")

main()
```

Uso e saída observada (entrada com `129,90`, `59.90` e `10`):

```bash
python dry_run_preco.py --entrada produtos.csv --saida diff.csv --bps 1000 --esperado 3
# itens=3 soma_antes=19980 soma_depois=21978     (129,90 -> 142,89; 59,90 -> 65,89; 10,00 -> 11,00)
python dry_run_preco.py --entrada produtos.csv --saida diff.csv --bps 1000 --esperado 4
# ABORTADO, nada gravado:  contagem divergente: exportação=3 esperado=4        (código de saída 1)
```

Observações: preço em centavos inteiros, sem `float`; `129,90` e `129.90` são aceitos; a regra "terminar em ,90" ou outra psicologia de preço precisa ser escrita no plano e implementada à parte. Arredondamento meio para cima é decisão do projeto.

## 3. Comparador da releitura: script executado

Compara o diff esperado com a releitura da API (exportada de volta para CSV com colunas `id`, `preco`). Saída 0 só se não houver faltando, extras nem divergentes.

```python
#!/usr/bin/env python3
"""Compara o esperado (saída do dry run) com a releitura pela API-fonte da verdade. Somente leitura."""
import csv, sys
from decimal import Decimal

def centavos(t): return int((Decimal(t.strip().replace(",", ".")) * 100).to_integral_value())

esperado = {r["id"]: int(r["depois"]) for r in csv.DictReader(open(sys.argv[1], newline="", encoding="utf-8"))}
relido = {r["id"]: centavos(r["preco"]) for r in csv.DictReader(open(sys.argv[2], newline="", encoding="utf-8"))}
faltando = sorted(set(esperado) - set(relido)); extras = sorted(set(relido) - set(esperado))
diverge = sorted(i for i in esperado.keys() & relido.keys() if esperado[i] != relido[i])
print(f"esperado={len(esperado)} relido={len(relido)} faltando={len(faltando)} extras={len(extras)} divergentes={len(diverge)}")
for i in diverge[:20]: print(f"  id={i} esperado={esperado[i]} relido={relido[i]}")
sys.exit(1 if (faltando or extras or diverge) else 0)
```

Saída observada: caso correto `esperado=3 relido=3 faltando=0 extras=0 divergentes=0` (saída 0); caso com item faltando e preço divergente `faltando=1 ... divergentes=1` (saída 1).

## 4. Ledger por item (padrão de V-20; padrão, não evidência)

```sql
CREATE TABLE ledger (
  mudanca_id        text    NOT NULL,
  item_id           text    NOT NULL,
  antes             bigint  NOT NULL,           -- centavos lidos na prévia
  depois            bigint  NOT NULL,           -- centavos planejados
  estado            text    NOT NULL CHECK (estado IN ('planejado','aplicado','verificado','pulado_frescor','revertido','erro')),
  lote              integer,
  chave_idempotencia text   NOT NULL UNIQUE,    -- <mudanca_id>-<item_id>
  atualizado_em     timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (mudanca_id, item_id)
);
```

Regras: aplicar só itens `planejado`; **frescor** (reler o valor atual antes de gravar; se diferir de `antes`, estado `pulado_frescor` e reporte); transição `planejado -> aplicado` condicionada ao estado (repetição não reaplica); `aplicado -> verificado` só depois da releitura; reversão usa `antes` e muda para `revertido`. Lógica verificada em SQLite em 2026-10-10: item 1 aplicado, item 2 pulado por frescor (alguém alterou o preço), repetição do item 1 sem efeito.

## 5. Texto da confirmação do passo 4 (modelo)

```text
Vou pedir permissão para aplicar a mudança abaixo na loja <ambiente>:
- O que: reajuste de +10% no preço de 142 variantes da coleção "Verão"
- Valores: soma R$ X -> R$ Y; maior variação +10,0%; nenhum preço vazio/zero; prévia em diff.csv
- Backup: export-2026-10-10.csv verificado (142 linhas)
- Como desfazer: reaplicar "antes" do ledger/backup
- Efeitos colaterais: webhooks de produto, feed do Merchant Center, ERP
Confirma aplicar nessas condições? Responda "sim, aplicar 142 itens" para eu preparar o comando da etapa 5.
```

A confirmação vale para esta ação, neste ambiente, com estes números. Outra ação (por exemplo, publicar o tema) pede outra confirmação.
