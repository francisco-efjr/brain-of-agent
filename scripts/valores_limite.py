#!/usr/bin/env python3
"""Gera valores de partição de equivalência e de valor-limite.

Uso:
    python3 valores_limite.py numero --min 18 --max 65
    python3 valores_limite.py numero --min 0.01 --max 5000 --passo 0.01
    python3 valores_limite.py texto --min 3 --max 50 [--literal]
    python3 valores_limite.py data --min 2024-01-01 --max 2028-12-31
    python3 valores_limite.py --self-test

Saída: tabela markdown com as colunas Valor | Classe | Esperado.
    aceita   o sistema deve aceitar
    recusa   o sistema deve recusar com mensagem clara, sem erro 500 nem tela quebrada
    definir  a regra não diz; é uma pergunta para o PO antes de virar caso de teste

Os limites são inclusivos (mín e máx são válidos). Se a regra for "maior que"
ou "até, exclusive", desloque a faixa antes de rodar: "> 18" vira --min 19.

Valores de texto longos aparecem como 'a' × 51 para a tabela caber na tela;
use --literal para imprimir a string completa e copiar para o teste.
"""
from __future__ import annotations

import argparse
import ast
import calendar
import sys
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation, localcontext
from typing import List, Tuple

Linha = Tuple[str, str, str]


# ---------------------------------------------------------------- número

def _fmt(valor: Decimal, passo: Decimal) -> str:
    casas = max(0, -passo.normalize().as_tuple().exponent)
    return f"{valor:.{casas}f}"


def casos_numero(minimo: Decimal, maximo: Decimal, passo: Decimal) -> List[Linha]:
    valores = (minimo, maximo, passo)
    if not all(v.is_finite() for v in valores):
        raise ValueError("--min, --max e --passo precisam ser números finitos")
    # Evita arredondamento silencioso pelo contexto decimal padrão (28 dígitos).
    precisao = max(v.adjusted() for v in valores) - min(v.as_tuple().exponent for v in valores) + 16
    with localcontext() as contexto:
        contexto.prec = max(28, precisao)
        return _casos_numero(minimo, maximo, passo)


def _casos_numero(minimo: Decimal, maximo: Decimal, passo: Decimal) -> List[Linha]:
    if passo <= 0:
        raise ValueError("--passo precisa ser positivo")
    if minimo > maximo:
        raise ValueError("--min maior que --max")
    for nome, v in (("--min", minimo), ("--max", maximo)):
        if (v / passo) != (v / passo).to_integral_value():
            raise ValueError(f"{nome} {v} não é múltiplo do passo {passo}")

    f = lambda v: _fmt(v, passo)  # noqa: E731
    passos = int((maximo - minimo) / passo)
    nominal = minimo + passo * (passos // 2)
    linhas: List[Linha] = []
    vistos = set()

    def add(valor: Decimal, classe: str, esperado: str) -> None:
        if valor not in vistos:
            vistos.add(valor)
            linhas.append((f(valor), classe, esperado))

    add(minimo - passo, "inválida: abaixo do mínimo (mín − passo)", "recusa")
    add(minimo, "válida: limite inferior (mín)", "aceita")
    if minimo + passo <= maximo:
        add(minimo + passo, "válida: logo acima do mínimo (mín + passo)", "aceita")
    add(nominal, "válida: valor interno (nominal)", "aceita")
    if maximo - passo >= minimo:
        add(maximo - passo, "válida: logo abaixo do máximo (máx − passo)", "aceita")
    add(maximo, "válida: limite superior (máx)", "aceita")
    add(maximo + passo, "inválida: acima do máximo (máx + passo)", "recusa")
    if minimo <= 0 <= maximo:
        add(Decimal(0), "válida: zero dentro da faixa", "aceita")
    elif minimo > 0:
        add(Decimal(0), "inválida: zero", "recusa")
        add(-passo, "inválida: negativo", "recusa")

    fora_do_passo = nominal + passo / 2
    linhas.append((str(fora_do_passo), f"inválida: precisão maior que o passo {passo}",
                   "recusa (ou arredonda, se a regra disser como)"))
    if passo < 1:
        linhas.append((f(nominal).replace(".", ","), "formato: vírgula decimal (pt-BR)",
                       "definir: em tela pt-BR deve aceitar"))
    if maximo >= 1000:
        mil = Decimal(1000)
        if minimo <= mil <= maximo:
            linhas.append(("1.000", "formato: ponto de milhar (pt-BR)",
                           "definir: 1000 ou recusa — nunca interpretar como 1"))
    linhas += [
        ("(vazio)", "inválida: vazio", "recusa se obrigatório"),
        ("'   '", "inválida: só espaços", "recusa"),
        (f"' {f(nominal)} '", "formato: espaços nas pontas", "definir: aceita após trim"),
        ("abc", "inválida: texto", "recusa"),
        ("1e3", "formato: notação científica", "definir: aceitação e faixa após conversão"),
        ("9" * 30, "robustez: número enorme", "aceita se dentro da faixa e do passo; caso contrário recusa sem erro 500"),
        ("NaN", "inválida: valor especial", "recusa"),
    ]
    return linhas


# ---------------------------------------------------------------- texto

def _texto(n: int) -> str:
    return "a" * n


def casos_texto(minimo: int, maximo: int, literal: bool) -> List[Linha]:
    if minimo < 0 or minimo > maximo:
        raise ValueError("faixa de tamanho inválida")

    def mostra(s: str, rotulo: str = "") -> str:
        if literal or len(s) <= 12:
            return repr(s)
        return rotulo or f"'{s[0]}' × {len(s)}"

    linhas: List[Linha] = []
    tamanhos = []

    def add(n: int, classe: str, esperado: str) -> None:
        if n >= 0 and n not in tamanhos:
            tamanhos.append(n)
            linhas.append((mostra(_texto(n)) if n else "'' (vazio)", f"{classe} — {n} caractere(s)", esperado))

    add(0, "vazio", "aceita" if minimo == 0 else "recusa")
    if minimo - 1 > 0:
        add(minimo - 1, "inválida: abaixo do mínimo (mín − 1)", "recusa")
    add(minimo, "válida: tamanho mínimo", "aceita")
    if minimo + 1 <= maximo:
        add(minimo + 1, "válida: mín + 1", "aceita")
    add((minimo + maximo) // 2, "válida: tamanho nominal", "aceita")
    if maximo - 1 >= minimo:
        add(maximo - 1, "válida: máx − 1", "aceita")
    add(maximo, "válida: tamanho máximo", "aceita")
    add(maximo + 1, "inválida: acima do máximo (máx + 1)", "recusa (ou bloqueia a digitação)")
    if maximo * 10 > maximo + 1:
        add(maximo * 10, "inválida: muito acima do máximo (colar texto grande)", "recusa sem erro 500")

    n_esp = max(minimo, 1)
    linhas.append((mostra(" " * n_esp, f"' ' × {n_esp}"), f"inválida: só espaços — {n_esp} caractere(s)",
                   "recusa (conteúdo vazio após trim)" if minimo > 0 else "definir: grava vazio (trim) ou recusa"))
    if maximo >= 3:
        s = " " + "a" * (maximo - 1) + " "
        linhas.append((mostra(s, f"' ' + 'a' × {maximo - 1} + ' '"),
                       f"formato: espaços nas pontas — {len(s)} caractere(s)",
                       "definir: trim antes de contar (aceita) ou recusa"))
    especiais = [
        ("ç", "'ç'", "acentos (conta caracteres, não bytes)", "definir: aceita se permitido pelo domínio"),
        ("😀", "'😀'", "emoji (1 caractere, 2 unidades UTF-16, 4 bytes)", "definir: conta como 1"),
        ("e\u0301", "('e' + U+0301)", "acento combinado (é decomposto, NFD)", "definir: normaliza e conta 1"),
    ]
    if maximo >= 1:
        for unidade, nome, classe, esperado in especiais:
            s = unidade * maximo
            rotulo = repr(s) if literal else f"{nome} × {maximo}"
            linhas.append((rotulo, f"{classe} — no máximo", esperado))
    hostis = [
        ("<script>alert(1)</script>", "hostil: HTML/JS", "definir: aceita como texto ou recusa por regra; nunca executa"),
        ("' OR '1'='1", "hostil: aspas / injeção SQL", "definir: aceita como texto ou recusa por regra; nunca altera a consulta"),
        ("linha1\nlinha2", "formato: quebra de linha", "definir (campo de uma linha deve recusar)"),
        ("D'Ávila", "apóstrofo e acento em nome", "definir: aceita se permitido pelo domínio"),
    ]
    for s, classe, esperado in hostis:
        if minimo <= len(s) <= maximo:
            linhas.append((repr(s), classe, esperado))
    return linhas


# ---------------------------------------------------------------- data

def _br(d: date) -> str:
    return f"{d.isoformat()} ({d.day:02d}/{d.month:02d}/{d.year:04d})"


def casos_data(minimo: date, maximo: date) -> List[Linha]:
    if minimo > maximo:
        raise ValueError("--min posterior a --max")
    um = timedelta(days=1)
    linhas: List[Linha] = []
    vistas = set()

    def add(d: date, classe: str, esperado: str) -> None:
        if d not in vistas:
            vistas.add(d)
            linhas.append((_br(d), classe, esperado))

    if minimo > date.min:
        add(minimo - um, "inválida: um dia antes do mínimo", "recusa")
    else:
        linhas.append(("0000-12-31", "inválida: abaixo do domínio de datetime.date", "recusa"))
    add(minimo, "válida: limite inferior", "aceita")
    if minimo < maximo:
        add(minimo + um, "válida: um dia depois do mínimo", "aceita")
    add(minimo + timedelta(days=(maximo - minimo).days // 2), "válida: data interna (nominal)", "aceita")
    if maximo > minimo:
        add(maximo - um, "válida: um dia antes do máximo", "aceita")
    add(maximo, "válida: limite superior", "aceita")
    if maximo < date.max:
        add(maximo + um, "inválida: um dia depois do máximo", "recusa")
    else:
        linhas.append(("10000-01-01", "inválida: acima do domínio de datetime.date", "recusa"))

    bissextos = [date(a, 2, 29) for a in range(minimo.year, maximo.year + 1)
                 if calendar.isleap(a) and minimo <= date(a, 2, 29) <= maximo]
    for d in bissextos[:2] + ([bissextos[-1]] if len(bissextos) > 2 else []):
        add(d, "válida: 29/02 de ano bissexto", "aceita")
        if d + um <= maximo:
            add(d + um, "válida: dia seguinte ao 29/02", "aceita")

    nao_bissextos = [a for a in range(minimo.year, maximo.year + 1)
                     if not calendar.isleap(a) and minimo <= date(a, 2, 28) <= maximo]
    inexistentes = [(f"{a}-02-29", f"inválida: data inexistente ({a} não é bissexto)")
                    for a in [a for a in nao_bissextos if a % 100 != 0][:1]]
    inexistentes += [(f"{a}-02-29", f"inválida: data inexistente ({a} é divisível por 100 e não por 400)")
                     for a in nao_bissextos if a % 100 == 0]
    ref = minimo.year
    inexistentes += [(f"{ref}-04-31", "inválida: 31 em mês de 30 dias"),
                     (f"{ref}-02-30", "inválida: 30/02"),
                     (f"{ref}-13-01", "inválida: mês 13"),
                     (f"{ref}-00-10", "inválida: mês zero")]
    for valor, classe in inexistentes:
        linhas.append((valor, classe, "recusa (sem virar outra data por 'rolagem')"))

    for a in range(minimo.year, maximo.year):
        dez31, jan1 = date(a, 12, 31), date(a + 1, 1, 1)
        if minimo <= dez31 and jan1 <= maximo:
            add(dez31, "válida: último dia do ano", "aceita")
            add(jan1, "válida: virada de ano", "aceita")
            break

    for deslocamento in range(min((maximo - minimo).days, 31) + 1):
        d = minimo + timedelta(days=deslocamento)
        if d.day <= 12 and d.day != d.month and d not in vistas:
            add(d, "válida: dia ≤ 12 (detecta troca dd/mm × mm/dd)", "aceita e mantém dia e mês")
            break

    linhas += [
        ("(vazio)", "inválida: vazio", "recusa se obrigatório"),
        (f"{minimo:%d}/{minimo:%m}/{minimo:%y}", "formato: ano com 2 dígitos", "definir"),
        ("abc", "inválida: texto", "recusa"),
    ]
    return linhas


# ---------------------------------------------------------------- saída

def tabela(linhas: List[Linha]) -> str:
    out = ["| Valor | Classe | Esperado |", "| --- | --- | --- |"]
    for valor, classe, esperado in linhas:
        v = valor.replace("|", "\\|").replace("\n", "\\n")
        out.append(f"| {v} | {classe} | {esperado} |")
    return "\n".join(out)


# ---------------------------------------------------------------- self-test

def self_test() -> int:
    erros: List[str] = []

    def tem(linhas: List[Linha], valor: str, esperado_ini: str) -> None:
        for v, _, e in linhas:
            if v == valor:
                if not e.startswith(esperado_ini):
                    erros.append(f"{valor}: esperado {esperado_ini!r}, veio {e!r}")
                return
        erros.append(f"valor {valor!r} ausente")

    n = casos_numero(Decimal(18), Decimal(65), Decimal(1))
    for v, e in [("17", "recusa"), ("18", "aceita"), ("19", "aceita"), ("41", "aceita"),
                 ("64", "aceita"), ("65", "aceita"), ("66", "recusa"), ("0", "recusa"),
                 ("-1", "recusa"), ("41.5", "recusa")]:
        tem(n, v, e)

    m = casos_numero(Decimal("0.01"), Decimal("5000.00"), Decimal("0.01"))
    for v, e in [("0.00", "recusa"), ("0.01", "aceita"), ("0.02", "aceita"), ("4999.99", "aceita"),
                 ("5000.00", "aceita"), ("5000.01", "recusa"), ("1.000", "definir")]:
        tem(m, v, e)
    if not any("," in v for v, _, _ in m):
        erros.append("faltou caso de vírgula decimal")

    z = casos_numero(Decimal(-10), Decimal(10), Decimal(1))
    tem(z, "0", "aceita")
    tem(z, "-11", "recusa")
    tem(z, "11", "recusa")

    try:
        casos_numero(Decimal("0.015"), Decimal(1), Decimal("0.01"))
        erros.append("aceitou --min fora do passo")
    except ValueError:
        pass

    t = casos_texto(3, 50, literal=True)
    tamanhos = {int(c.split("— ")[1].split()[0]): e for v, c, e in t if v.startswith("'a")}
    for v, c, _ in t:
        if v.startswith("'a") and len(ast.literal_eval(v)) != int(c.split("— ")[1].split()[0]):
            erros.append(f"texto: tamanho declarado não confere em {c}")
    for tam, e in [(0, "recusa"), (2, "recusa"), (3, "aceita"), (4, "aceita"), (49, "aceita"),
                   (50, "aceita"), (51, "recusa")]:
        if tam == 0:
            e_vazio = next((e2 for v2, _, e2 in t if v2.startswith("''")), "")
            if not e_vazio.startswith(e):
                erros.append(f"texto vazio: esperado {e}, veio {e_vazio}")
            continue
        if not tamanhos.get(tam, "").startswith(e):
            erros.append(f"texto tamanho {tam}: esperado {e}, veio {tamanhos.get(tam)}")
    if not any("só espaços" in c for _, c, _ in t):
        erros.append("faltou caso só espaços")
    if not any(v.startswith("''") and e == "recusa" for v, _, e in casos_texto(1, 10, False)):
        erros.append("vazio deveria ser recusado com mínimo 1")

    d = casos_data(date(2023, 6, 1), date(2025, 3, 31))
    for v, e in [("2023-05-31 (31/05/2023)", "recusa"), ("2023-06-01 (01/06/2023)", "aceita"),
                 ("2025-03-31 (31/03/2025)", "aceita"), ("2025-04-01 (01/04/2025)", "recusa"),
                 ("2024-02-29 (29/02/2024)", "aceita"), ("2023-12-31 (31/12/2023)", "aceita"),
                 ("2024-01-01 (01/01/2024)", "aceita"), ("2025-02-29", "recusa")]:
        tem(d, v, e)
    if any(v.startswith("2023-02-29") for v, _, _ in d):
        erros.append("29/02/2023 fora da faixa não deveria aparecer")

    s = casos_data(date(1899, 1, 1), date(1901, 12, 31))
    tem(s, "1900-02-29", "recusa")
    if any(v.startswith("1900-02-29 (") for v, _, _ in s):
        erros.append("1900-02-29 tratado como válido")

    um_dia = casos_data(date(2024, 2, 29), date(2024, 2, 29))
    tem(um_dia, "2024-02-28 (28/02/2024)", "recusa")
    tem(um_dia, "2024-03-01 (01/03/2024)", "recusa")

    if erros:
        print(f"self-test: {len(erros)} falha(s)")
        for e in erros:
            print(" -", e)
        return 1
    print("self-test: OK (número inteiro e decimal, texto, datas com bissexto e 1900)")
    return 0


# ---------------------------------------------------------------- CLI

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Gera valores de partição e de limite em tabela markdown (Valor | Classe | Esperado).")
    parser.add_argument("--self-test", action="store_true", help="roda as verificações internas e sai com 0 (ok) ou 1")
    sub = parser.add_subparsers(dest="tipo")

    pn = sub.add_parser("numero", help="faixa numérica inclusiva")
    pn.add_argument("--min", required=True)
    pn.add_argument("--max", required=True)
    pn.add_argument("--passo", default="1", help="menor incremento aceito: 1, 0.01... (padrão 1)")

    pt = sub.add_parser("texto", help="tamanho de texto em caracteres")
    pt.add_argument("--min", required=True, type=int)
    pt.add_argument("--max", required=True, type=int)
    pt.add_argument("--literal", action="store_true", help="imprime as strings completas")

    pd = sub.add_parser("data", help="faixa de datas inclusiva (AAAA-MM-DD)")
    pd.add_argument("--min", required=True)
    pd.add_argument("--max", required=True)

    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    if args.tipo is None:
        parser.print_help()
        return 2
    try:
        if args.tipo == "numero":
            linhas = casos_numero(Decimal(args.min), Decimal(args.max), Decimal(args.passo))
        elif args.tipo == "texto":
            linhas = casos_texto(args.min, args.max, args.literal)
        else:
            linhas = casos_data(date.fromisoformat(args.min), date.fromisoformat(args.max))
    except (ValueError, InvalidOperation, OverflowError) as e:
        print(f"erro: {e}", file=sys.stderr)
        return 2
    print(tabela(linhas))
    return 0


if __name__ == "__main__":
    sys.exit(main())
