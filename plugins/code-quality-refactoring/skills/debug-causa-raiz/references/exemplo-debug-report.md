# Exemplo: cache com chave incompleta, do sintoma ao relatório

O caso é pequeno de propósito para mostrar a ordem das etapas. Os trechos de saída foram executados em 2026-10-10 (Python 3.14.4, Windows, `unittest` da biblioteca padrão) e abreviados; o relatório é um molde, não um resultado do seu projeto.

## Pedido do usuário

"O relatório de ontem mostra a cotação de hoje, mas só quando gero os dois relatórios no mesmo processo. Comando: `python -m unittest -v test_cotacoes`."

## Passo 1: causa raiz

Código lido (`cotacoes.py`):

```python
_cache = {}

def cotacao(moeda, data):
    if moeda in _cache:
        return _cache[moeda]
    valor = TABELA[(moeda, data)]
    _cache[moeda] = valor
    return valor
```

Reprodução com o teste que descreve o sintoma (duas datas, mesma moeda, mesmo processo):

```text
FAIL: test_datas_diferentes_devolvem_valores_diferentes
    self.assertEqual(cotacoes.cotacao("USD", "2026-10-08"), 5.10)
AssertionError: 5.25 != 5.1
Ran 1 test in 0.001s
FAILED (failures=1)
```

Esperado 5.10 para 2026-10-08; observado 5.25 (o valor de 2026-10-09). Reproduz sempre (constante). `git log` do arquivo não mostra mudança recente: não é regressão por diff, o desenho já nascia assim.

## Passo 2: padrão

Padrão da tabela: cache obsoleto por chave incompleta. Contraste: `TABELA` usa `(moeda, data)` como chave; `_cache` usa só `moeda`.

## Passo 3: hipótese

"Acredito que `cotacao()` devolve o valor de outra data porque a chave de cache é só `moeda`; refuto chamando duas datas na mesma execução e comparando com `TABELA`." O comando é o próprio teste acima; a saída confirma. Hipóteses testadas: 1 (contador em 1 de 3).

## Passo 4: correção

O teste de regressão é o que falhou no passo 1 (foi visto falhar pelo motivo certo: o valor veio de outra data). Correção única, no menor diff:

```python
def cotacao(moeda, data):
    if (moeda, data) in _cache:
        return _cache[(moeda, data)]
    valor = TABELA[(moeda, data)]
    _cache[(moeda, data)] = valor
    return valor
```

```text
test_datas_diferentes_devolvem_valores_diferentes ... ok
Ran 1 test in 0.000s
OK
```

## Passo 5: revalidação

1. Reprodução original (o mesmo comando): passa.
2. Casos adjacentes: mesma moeda e mesma data duas vezes devolve o valor cacheado; moeda sem cotação na data continua levantando `KeyError` (comportamento anterior, não alterado).
3. Verificações afetadas: suíte do módulo verde; este projeto de exemplo não tem lint nem tipos.
4. Jornada real: não aplicável neste exemplo (função isolada).
5. Diff final conferido: só `cotacoes.py` e o teste.

## Relatório

| Campo | Conteúdo |
| --- | --- |
| Sintoma | Relatório de 2026-10-08 mostra 5.25 (cotação de 2026-10-09) quando os dois relatórios rodam no mesmo processo |
| Causa raiz | `cotacoes.py`, função `cotacao`: o cache usa só `moeda` como chave; a segunda data recebe o valor da primeira (Verificado) |
| Correção | Chave de cache passa a ser `(moeda, data)`; 3 linhas alteradas |
| Evidência | `python -m unittest -v test_cotacoes`: antes `FAILED (failures=1)`, depois `OK` (Verificado) |
| Teste de regressão | `test_cotacoes.py::TestCotacao::test_datas_diferentes_devolvem_valores_diferentes`; falhou sem a correção, passa com ela |
| Prevenção | O teste cobre duas datas na mesma execução; considerar `functools.lru_cache` com os dois argumentos para evitar chave manual |
| Relacionado | `_cache` nunca expira (sem TTL) e cresce sem limite: follow-up, não corrigido aqui (Inferido: sem medição de memória) |
| Status | DONE |

## O que este molde mostra

- A reprodução antes da hipótese e o teste visto falhar antes da correção.
- Uma correção, três linhas, sem refatorar a função.
- Bug vizinho (sem TTL) vai para "Relacionado", não para o diff.
- Cada afirmação traz rótulo e comando; o que não foi medido (memória) está marcado Inferido.
