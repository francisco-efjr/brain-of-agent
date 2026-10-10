# Transformações de simplificação e como provar a equivalência

Sumário: 1 Retornos antecipados · 2 Remover duplicação · 3 Nomes · 4 Ternário aninhado · 5 Comentários · 6 Armadilhas verificadas · 7 Atribuição.

Rótulos: Verificado = executado em 2026-10-10 (Python 3.14.4 e Node v24.15.0 em Windows); Inferido = conhecimento estável. Em outra versão de linguagem, repita o teste de equivalência.

Cada transformação lista: antes, depois e o que checar para afirmar "mesmo comportamento".

## 1. Retornos antecipados (reduzir aninhamento)

Antes:

```python
def preco_final(pedido):
    if pedido is not None:
        if pedido.itens:
            total = 0
            for item in pedido.itens:
                total += item.preco * item.qtd
            if pedido.cupom:
                if total >= pedido.cupom.minimo:
                    total = total - total * pedido.cupom.percentual / 100
            return total
        else:
            return 0
    else:
        return 0
```

Depois (Verificado: devolveu o mesmo resultado em 6 entradas, incluindo `None`, lista vazia, sem cupom, cupom aplicado e cupom abaixo do mínimo):

```python
def preco_final(pedido):
    if pedido is None or not pedido.itens:
        return 0
    total = 0
    for item in pedido.itens:
        total += item.preco * item.qtd
    cupom = pedido.cupom
    if cupom and total >= cupom.minimo:
        total -= total * cupom.percentual / 100
    return total
```

Checar: a ordem das condições (curto-circuito) preservou o acesso a `pedido.itens` somente depois de `pedido is None`; o tipo de retorno (`0` inteiro) não mudou; o laço de soma foi mantido por causa da armadilha 6.1.

Em linguagens com limpeza no fim (`finally`, `defer`, `using`, `with`), um retorno antecipado antes da aquisição do recurso é seguro; depois dela, só se a limpeza estiver em construção que cobre todos os caminhos.

## 2. Remover duplicação

Antes:

```typescript
const a = items.filter(i => i.active && i.price > 0).map(i => i.price * 1.1);
const b = others.filter(o => o.active && o.price > 0).map(o => o.price * 1.1);
```

Depois, só porque há duas ocorrências reais e a mesma regra de negócio:

```typescript
const withMarkup = <T extends { active: boolean; price: number }>(xs: T[]) =>
  xs.filter(x => x.active && x.price > 0).map(x => x.price * 1.1);
const a = withMarkup(items);
const b = withMarkup(others);
```

Verificado em Node v24.15.0 (tipos removidos pelo próprio Node): mesmas saídas nas duas listas de exemplo. Checar: as duas cópias eram idênticas na regra (diferença sutil, como `>= 0`, significa que não eram duplicação); a função extraída ficou no mesmo módulo; nenhuma outra chamada foi tocada. Duplicação de aparência com regras que tendem a divergir não se extrai (extração prematura cria acoplamento). Duas ocorrências é o mínimo; três é o caso claro.

## 3. Nomes que dizem a intenção

Antes: `def f(d, n): return d * n / 100`. Depois: `def desconto_em_reais(preco, percentual): return preco * percentual / 100`.

Checar: renomear parâmetro posicional é seguro; renomear parâmetro **nomeado** muda a API para quem chama com `f(d=..., n=...)` (Python) ou com objetos de opções (JavaScript). Busque chamadas com `Grep` antes. Não renomeie símbolos exportados nesta skill (API pública: `refactor-seguro`).

## 4. Ternário aninhado vira if/else

Antes:

```typescript
const label = status === "paid" ? "Pago" : status === "pending" ? (late ? "Atrasado" : "Pendente") : "Cancelado";
```

Depois:

```typescript
function labelDe(status: string, late: boolean): string {
  if (status === "paid") return "Pago";
  if (status === "pending") return late ? "Atrasado" : "Pendente";
  return "Cancelado";
}
const label = labelDe(status, late);
```

Verificado em Node v24.15.0 com 5 valores de `status` (inclusive `undefined` e `""`) e os 2 valores de `late`: mesmo rótulo nas 10 combinações. Checar: o caso padrão (`"Cancelado"`) cobre exatamente o que o ternário cobria (qualquer outro valor, inclusive `undefined`); a função não captura variável de fora nem muda ordem de avaliação de expressões com efeito.

## 5. Comentários

Apague quando repete o código (`// incrementa i` ao lado de `i += 1`). Mantenha quando explica o porquê, uma restrição externa, uma decisão ou um bug conhecido (`// a API devolve 200 com corpo vazio quando não há resultado`). Em dúvida, mantenha e anote. Comentário que contradiz o código é achado: reporte, não decida sozinho qual dos dois está certo.

## 6. Armadilhas verificadas

### 6.1 `sum()` não é um laço `+=` com floats

Verificado em Python 3.14.4:

```python
t = 0
for _ in range(10):
    t += 0.1
print(repr(t), repr(sum([0.1] * 10)))   # 0.9999999999999999 1.0
```

Python 3.12 ou superior usa soma compensada em `sum()` de floats, então o resultado pode divergir do laço na última casa. Se o resultado entra em comparação de igualdade, arredondamento de dinheiro ou teste com valor fixado, mantenha o laço, ou use `decimal`/inteiros em centavos como mudança separada. Confirme a mudança de comportamento na versão que o projeto usa.

### 6.2 `||` não é `??`

Verificado em Node v24.15.0:

```javascript
const a = 0;
console.log(a || 5, a ?? 5);       // 5 0
console.log("" || "x", "" ?? "x"); // x  (string vazia)
```

`x || padrão` troca `0`, `""`, `false` e `NaN` pelo padrão; `x ?? padrão` só troca `null` e `undefined`. A simplificação que troca um pelo outro muda o comportamento nesses valores.

### 6.3 Truthiness em Python

`if x:` é falso para `0`, `""`, `[]`, `{}` e `None`; `if x is not None:` só para `None`. Trocar um pelo outro muda o tratamento de `0` e de lista vazia.

### 6.4 Guarda negada com `NaN`

`if not (a > 0 and b > 0)` e `if a <= 0 or b <= 0` diferem para `NaN` (Verificado em `refactor-seguro`, referência `caracterizacao-e-passos.md`, seção 3). Preserve a forma negada quando a entrada pode ser `NaN`.

### 6.5 Efeitos colaterais e ordem

Inline de variável que guarda uma chamada com efeito (log, I/O, contador) muda quantas vezes e em que ordem ela roda. Extrair função de dentro de um laço muda o escopo das variáveis capturadas.

## 7. Atribuição

Regras de escopo e de "mudar o como, nunca o quê": redação própria a partir do agente `code-simplifier` de `anthropics/claude-plugins-official` (Apache-2.0 na raiz do repositório; licença por plugin Inferida, V-12). Nenhum texto literal copiado. Exemplos de código: autoria deste plugin (MIT).
