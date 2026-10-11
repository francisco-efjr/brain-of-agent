#!/usr/bin/env python3
"""Calcula razão de contraste WCAG (fórmula de luminância relativa) para as cores
do cadastro original e do cadastro corrigido. Só biblioteca padrão.

Uso: python3 contraste.py
Limiares (WCAG 2.2 AA): texto 4,5:1 (1.4.3); texto grande 3:1; componente de
interface e borda de campo 3:1 (1.4.11). Texto grande = >= 24 px, ou >= 18,66 px em negrito.
"""


def luminancia(hex_: str) -> float:
    h = hex_.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))

    def canal(c: float) -> float:
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * canal(r) + 0.7152 * canal(g) + 0.0722 * canal(b)


def razao(a: str, b: str) -> float:
    la, lb = sorted((luminancia(a), luminancia(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


# (descrição, primeiro plano, fundo, mínimo exigido, critério)
ORIGINAL = [
    ("texto do corpo e do título (13 px) #999 / #fff", "#999999", "#ffffff", 4.5, "1.4.3"),
    ("texto de ajuda da senha (11 px) #bbb / #fff", "#bbbbbb", "#ffffff", 4.5, "1.4.3"),
    ("texto do botão Enviar #fff / #6cf", "#ffffff", "#66ccff", 4.5, "1.4.3"),
    ("borda dos campos #ddd / #fff", "#dddddd", "#ffffff", 3.0, "1.4.11"),
    ("borda de campo em erro (red) / #fff", "#ff0000", "#ffffff", 3.0, "1.4.11"),
    ("mensagem de sucesso (green) / #fff", "#008000", "#ffffff", 4.5, "1.4.3"),
    ("placeholder (cor padrão do Chrome, #757575) / #fff", "#757575", "#ffffff", 4.5, "1.4.3"),
]

CORRIGIDO = [
    ("texto do corpo #1f1f1f / #fff", "#1f1f1f", "#ffffff", 4.5, "1.4.3"),
    ("texto de dica #595959 / #fff", "#595959", "#ffffff", 4.5, "1.4.3"),
    ("texto do botão #fff / #00539b", "#ffffff", "#00539b", 4.5, "1.4.3"),
    ("borda dos campos #767676 / #fff", "#767676", "#ffffff", 3.0, "1.4.11"),
    ("borda e texto de erro #b00020 / #fff", "#b00020", "#ffffff", 4.5, "1.4.3"),
    ("contorno de foco #005fcc / #fff", "#005fcc", "#ffffff", 3.0, "1.4.11"),
    ("borda da mensagem de sucesso #1b5e20 / #fff", "#1b5e20", "#ffffff", 3.0, "1.4.11"),
    ("link #0b3d91 / #fff", "#0b3d91", "#ffffff", 4.5, "1.4.3"),
]


def imprimir(titulo: str, linhas: list) -> int:
    falhas = 0
    print(f"\n== {titulo} ==")
    for desc, fg, bg, minimo, criterio in linhas:
        r = razao(fg, bg)
        ok = r >= minimo
        falhas += not ok
        print(f"{'OK   ' if ok else 'FALHA'}  {r:5.2f}:1 (mín. {minimo}:1, {criterio})  {desc}")
    return falhas


if __name__ == "__main__":
    f1 = imprimir("Original (cadastro.html)", ORIGINAL)
    f2 = imprimir("Corrigido (cadastro-corrigido.html)", CORRIGIDO)
    print(f"\nfalhas no original: {f1}; falhas no corrigido: {f2}")
    raise SystemExit(1 if f2 else 0)
