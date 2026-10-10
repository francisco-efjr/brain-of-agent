# Contraste WCAG: fórmula, limiares e script

Use este arquivo sempre que um par de cores precisar de um número. Estimar contraste pela imagem ou pela intuição é a falha mais comum de plano de design gerado por modelo. Calcule com os valores reais do estado (normal, hover, foco, desabilitado) e do fundo real.

Rótulo do conteúdo: fórmula e limiares são Verificado (WCAG 2.2, Recommendation de 2024-12-12, critérios 1.4.3 e 1.4.11; conferir em https://www.w3.org/TR/WCAG22/). Os números da tabela de exemplos foram calculados com o script abaixo em 2026-10-10.

## Sumário

- [Fórmula](#fórmula)
- [Limiares](#limiares)
- [Script (Python, só biblioteca padrão)](#script-python-só-biblioteca-padrão)
- [Exemplos calculados](#exemplos-calculados)
- [Casos em que o cálculo simples engana](#casos-em-que-o-cálculo-simples-engana)

## Fórmula

1. Converta cada canal sRGB de 0 a 255 para `c = valor / 255`.
2. Linearize: `c / 12.92` se `c <= 0.04045`; senão `((c + 0.055) / 1.055) ** 2.4`.
3. Luminância relativa: `L = 0.2126 * R + 0.7152 * G + 0.0722 * B`.
4. Razão: `(L_maior + 0.05) / (L_menor + 0.05)`, de 1:1 a 21:1.
5. Não arredonde para cima: 4,499:1 não atinge 4,5:1 (as páginas Understanding do W3C tratam o limiar como valor exato; conferir na versão vigente).

## Limiares

| O que | Critério | Nível | Mínimo |
| --- | --- | --- | --- |
| Texto normal | 1.4.3 | AA | 4,5:1 |
| Texto grande (a partir de 24 px, ou 18,66 px em negrito; equivale a 18 pt e 14 pt) | 1.4.3 | AA | 3:1 |
| Componente de interface e objeto gráfico necessário (borda de campo, ícone sem texto, indicador de foco, segmento de gráfico) | 1.4.11 | AA | 3:1 contra as cores adjacentes |
| Texto, nível aprimorado | 1.4.6 | AAA | 7:1 (4,5:1 se grande) |
| Texto puramente decorativo, logotipo, componente desabilitado | 1.4.3 / 1.4.11 | n/a | sem exigência (exceções do critério) |

## Script (Python, só biblioteca padrão)

Cole em um arquivo temporário do scratchpad e rode com `python`. Não precisa de instalação nem de rede.

```python
import sys

def _lin(c):
    c /= 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def luminancia(hex_):
    h = hex_.lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)

def razao(a, b):
    la, lb = sorted((luminancia(a), luminancia(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)

if __name__ == "__main__":
    # uso: python contraste.py "#14272B" "#F3F7F6" "#4A5D61" "#FFFFFF"
    cores = sys.argv[1:]
    for i in range(0, len(cores) - 1, 2):
        r = razao(cores[i], cores[i + 1])
        print(f"{cores[i]} sobre {cores[i+1]}: {r:.2f}:1  texto>=4.5 {'ok' if r >= 4.5 else 'falha'}  ui>=3 {'ok' if r >= 3 else 'falha'}")
```

## Exemplos calculados

| Par (texto/fundo) | Razão | Leitura |
| --- | --- | --- |
| `#999999` sobre `#FFFFFF` | 2,85:1 | falha em texto e em componente; o exemplo "≈ 2,5:1" que circula em guias é impreciso, calcule |
| `#767676` sobre `#FFFFFF` | 4,54:1 | passa por pouco em texto normal |
| `#FFFFFF` sobre `#1A1C1E` | 17,09:1 | a mensagem de 15,42:1 no exemplo de saída do linter do design.md é inconsistente com a fórmula; não use o linter como oráculo |
| `#14272B` sobre `#F3F7F6` | 14,35:1 | texto principal confortável |
| `#4A5D61` sobre `#F3F7F6` | 6,42:1 | texto secundário seguro |
| `#FFC53D` sobre `#F3F7F6` | 1,46:1 | amarelo só como preenchimento decorativo, nunca como texto nem como única borda |
| `#14272B` sobre `#FFC53D` | 9,82:1 | texto escuro sobre o amarelo funciona |

## Casos em que o cálculo simples engana

- **Transparência:** componha a cor com alfa sobre o fundo real antes de calcular (`resultado = alfa * cor + (1 - alfa) * fundo`, canal a canal).
- **Fundo com gradiente ou imagem:** meça no ponto de pior contraste sob o texto; se não der para medir, rotule Inferido e peça captura.
- **Estados:** hover, foco, selecionado, desabilitado e tema escuro têm pares próprios. Calcule o par de cada estado, nos dois temas.
- **Tamanho e peso reais:** a classe de texto grande depende do tamanho computado em pixels, não do nome da classe CSS.
- **Ferramentas automáticas** (axe, Lighthouse) deixam contraste sobre imagem em `incomplete`; trate essa fila como revisão manual.
