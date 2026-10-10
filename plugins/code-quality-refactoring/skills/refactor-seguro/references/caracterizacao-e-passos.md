# Caracterização, catálogo de passos e Parallel Change

Sumário: 1 Exemplo executável · 2 Os passos do exemplo · 3 Armadilhas de equivalência · 4 Catálogo de refatorações como vocabulário · 5 Parallel Change · 6 Dividir a mudança · 7 Atribuições.

Rótulos: Verificado = executado em 2026-10-10 (Python 3.14.4, `unittest` da biblioteca padrão, Windows); Inferido = conhecimento estável ou leitura de fonte. Confira o runner e as versões do seu projeto.

## 1. Exemplo executável

Função legada, sem testes (`frete.py`). Pedido: "refatore para ficar legível, sem mudar o comportamento".

```python
def calcular_frete(peso_kg, distancia_km, expresso):
    if peso_kg > 0:
        if distancia_km > 0:
            if expresso:
                valor = 8 + peso_kg * 1.5 + distancia_km * 0.05
                if peso_kg > 30:
                    valor = valor * 1.2
            else:
                valor = 5 + peso_kg * 1.0 + distancia_km * 0.03
                if peso_kg > 30:
                    valor = valor * 1.1
            return int(valor * 100) / 100
        else:
            return -1
    else:
        return -1
```

Passo 1: caracterizar. Entradas: caso comum, cada ramo, limite exato (30 kg), entradas inválidas. As expectativas abaixo foram fixadas a partir da execução real do código original (passo 2 do procedimento):

```python
import unittest
from frete import calcular_frete

CASOS = [
    # (peso_kg, distancia_km, expresso, esperado_atual, nome)
    (1, 10, False, 6.3, "padrao_leve"),
    (10, 100, True, 28.0, "expresso_medio"),
    (31, 100, False, 42.9, "padrao_pesado_acrescimo_10pct"),
    (30, 100, False, 38.0, "padrao_limite_30kg_sem_acrescimo"),
    (0, 10, False, -1, "peso_zero_devolve_sentinela"),
    (5, 0, True, -1, "distancia_zero_devolve_sentinela"),
    (-1, 10, True, -1, "peso_negativo_devolve_sentinela"),
    # comportamento atual, possível defeito: trunca em vez de arredondar.
    # 59.5 * 1.2 = 71.4 em aritmética exata; o código devolve 71.39.
    (31, 100, True, 71.39, "expresso_pesado_trunca_centavo_POSSIVEL_DEFEITO"),
]

class TestCalcularFreteCaracterizacao(unittest.TestCase):
    def test_comportamento_atual(self):
        for peso, dist, expresso, esperado, nome in CASOS:
            with self.subTest(nome):
                self.assertEqual(calcular_frete(peso, dist, expresso), esperado)
```

`python -m unittest test_frete_caracterizacao` contra o original: `OK` (Verificado). O último caso fixa `71.39`: o valor exato seria `71.4`, mas `int(valor * 100)` trunca e o erro de ponto flutuante (`71.39999999999999`) derruba o centavo. Isso é **possível defeito**: fica no relatório como follow-up, e o teste continua afirmando `71.39` até alguém decidir a regra de negócio em outra mudança.

Equivalente em pytest: `@pytest.mark.parametrize("peso,dist,expresso,esperado", CASOS)`. Em Jest: `test.each(CASOS)("%s", ...)`. Em saídas complexas (HTML, JSON grande) use teste de snapshot como caracterização, com revisão humana do snapshot gerado (Inferido).

## 2. Os passos do exemplo

Resultado final do exemplo (Verificado: os mesmos testes passam contra ele, e os 12 casos comparados com o original deram o mesmo resultado, inclusive o limite de 30 kg):

```python
def _valor_expresso(peso_kg, distancia_km):
    valor = 8 + peso_kg * 1.5 + distancia_km * 0.05
    return valor * 1.2 if peso_kg > 30 else valor

def _valor_padrao(peso_kg, distancia_km):
    valor = 5 + peso_kg * 1.0 + distancia_km * 0.03
    return valor * 1.1 if peso_kg > 30 else valor

def calcular_frete(peso_kg, distancia_km, expresso):
    if not (peso_kg > 0 and distancia_km > 0):
        return -1
    calcular = _valor_expresso if expresso else _valor_padrao
    return int(calcular(peso_kg, distancia_km) * 100) / 100
```

| Passo | Refatoração (catálogo) | Escopo | Teste |
| --- | --- | --- | --- |
| 1 | Replace Nested Conditional with Guard Clauses | Os dois `if` de validação viram uma cláusula de guarda | `unittest` verde |
| 2 | Extract Function | Cálculo expresso vira `_valor_expresso` | `unittest` verde |
| 3 | Extract Function | Cálculo padrão vira `_valor_padrao` | `unittest` verde |
| 4 | Decompose Conditional | Escolha entre as duas funções em uma variável | `unittest` verde |

Um passo por vez, teste após cada passo. O truncamento, o `-1` como sentinela de erro e os números mágicos (8, 1.5, 0.05) continuam: são follow-ups, não parte desta mudança.

## 3. Armadilhas de equivalência

A guarda do passo 1 poderia ter sido escrita `if peso_kg <= 0 or distancia_km <= 0: return -1`, que parece idêntica. Não é (Verificado): com `peso_kg = float("nan")`, o original devolve `-1` (porque `nan > 0` é falso), a versão com `<=` segue adiante e levanta `ValueError: cannot convert float NaN to integer`. O teste de caracterização só pegaria isso se a entrada `NaN` estivesse na tabela. Regras:

- Negar condição composta exige De Morgan com cuidado e, para números, atenção a `NaN` e a `None`.
- Trocar `a or b` por `a if a else b`, ou `||` por `??` em JavaScript, muda o resultado para `0`, `""` e `false`.
- Reordenar condições muda curto-circuito e efeitos colaterais (log, I/O, contador).
- Extrair função pode mudar o escopo de variáveis fechadas (closures) e a captura em laços.
- Mover código para dentro ou fora de `try`/`finally` muda quando a limpeza roda.
- Inline de variável com chamada cara ou com efeito colateral muda quantas vezes ela roda.

Adicione ao teste uma entrada para cada risco que o trecho tem; o custo é uma linha na tabela.

## 4. Catálogo de refatorações como vocabulário

Nomes verificados no catálogo de refatorações de Martin Fowler (https://refactoring.com/catalog/, 2026-10-10); a mecânica passo a passo vem da prática e do livro, não da página (Inferido). Cite o nome no plano para que o revisor reconheça o passo.

| Refatoração | Quando usar |
| --- | --- |
| Extract Function / Inline Function | Bloco com um propósito nomeável / função que não diz mais que o corpo |
| Extract Variable | Expressão longa ou repetida |
| Split Loop | Laço fazendo duas coisas independentes |
| Remove Dead Code | Código sem uso confirmado por busca e testes |
| Move Function | A função usa mais dados de outro módulo |
| Extract Class | Classe com duas responsabilidades |
| Hide Delegate | Cliente atravessa uma cadeia de objetos |
| Encapsulate Variable | Dado mutável acessado de muitos lugares |
| Replace Primitive with Object | `str`/`int` carregando regra (CPF, dinheiro) |
| Decompose Conditional | Condição complexa com ramos grandes |
| Replace Nested Conditional with Guard Clauses | Casos excepcionais empilhados em `if` aninhado |
| Replace Conditional with Polymorphism | `switch` repetido sobre tipo |
| Remove Flag Argument | Parâmetro booleano que escolhe o comportamento |
| Change Function Declaration | Renomear função ou mudar parâmetros (pode ser Parallel Change) |
| Introduce Parameter Object | Grupo de parâmetros que sempre viaja junto |

## 5. Parallel Change (V-37)

Para trocar função pública, esquema ou dependência com API quebrada: expandir, migrar, contrair (Martin Fowler, Danilo Sato, 2014-05-13). Exemplo, renomear `calcular_frete` para `calcular_frete_brl` quando há chamadores em outros pacotes:

1. **Expandir.** Crie `calcular_frete_brl` com o corpo; deixe `calcular_frete` chamando a nova. Testes verdes. Commit próprio.
2. **Migrar.** Troque os chamadores em lotes pequenos (um módulo por commit), testes a cada lote.
3. **Contrair.** Quando `Grep` por `calcular_frete(` só achar a definição e a suíte passar, remova a antiga. Anote a data prevista da contração no registro de dívida para a transição não virar permanente.

Banco de dados e API remota seguem a mesma forma, com mais cuidado de implantação: o conceito é daqui, a migração de dados é de `database-data-modeling`.

## 6. Dividir a mudança

| Sinal | Ação |
| --- | --- |
| Refatoração e correção no mesmo diff | Separar em dois commits ou PRs; refatoração primeiro |
| Diff acima de ~400 linhas ou 10 arquivos (Suposição) | Propor divisão por pasta ou por passo |
| Testes novos de caracterização | No mesmo PR da refatoração, em commit anterior ao primeiro passo |
| Renomeações em massa | Commit só de renomeação, sem outra mudança, para o revisor poder ignorar |

Para PRs empilhados e branches, o fluxo de git é de `git-workflow-release`.

## 7. Atribuições

- Feathers, "Characterization Testing" (2016-08-08) e Fowler, "Self-Testing Code" (2014-05-01): procedimento e justificativa; redação própria (V-36).
- Catálogo de refatorações (refactoring.com): somente nomes; sem texto copiado.
- Parallel Change (martinfowler.com): redação própria (V-37).
- Google Engineering Practices, CLs pequenos (V-18): redação própria; os números são orientação da fonte.
