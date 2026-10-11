#!/usr/bin/env python3
"""Gera e valida CPF e CNPJ (numérico e alfanumérico) para massa de teste.

Uso:
    python3 documentos_br.py gerar cpf [-n 5] [--mascara] [--semente 42]
    python3 documentos_br.py gerar cnpj [-n 5] [--mascara] [--filial]
    python3 documentos_br.py gerar cnpj-alfa [-n 5] [--mascara]
    python3 documentos_br.py validar 529.982.247-25 11222333000181 12.ABC.345/01DE-35
    cat lista.txt | python3 documentos_br.py validar -
    python3 documentos_br.py --self-test

Regras implementadas:
    CPF   11 dígitos; 2 DVs por módulo 11 (pesos 10..2 e 11..2); resto < 2 vira 0.
          Sequências de um só dígito (000.000.000-00 ... 999.999.999-99) passam
          no cálculo, mas são inválidas.
    CNPJ  14 posições: 8 de raiz + 4 de ordem (estabelecimento) + 2 DVs.
          Desde julho de 2026 a Receita emite inscrições novas com as 12
          primeiras posições alfanuméricas (A-Z, 0-9); os 2 DVs continuam
          numéricos. Valor de cada caractere = código ASCII - 48 (0..9 -> 0..9,
          A -> 17 ... Z -> 42). Pesos 5,4,3,2,9,8,7,6,5,4,3,2 (DV1) e
          6,5,4,3,2,9,8,7,6,5,4,3,2 (DV2); resto < 2 vira 0. Para CNPJ só com
          dígitos, o resultado é idêntico ao cálculo tradicional.

`validar` aceita valores com ou sem máscara (pontos, barra, hífen, espaços),
detecta o tipo pelo tamanho, diz o motivo de cada invalidez e sai com código 1
se algum valor for inválido.

Atenção: um CPF/CNPJ gerado com DV correto pode pertencer a uma pessoa ou
empresa real. Use apenas em ambientes de teste e nunca para consultar bases
externas (Receita, bureaus de crédito) ou cadastrar em sistemas de terceiros.
"""
from __future__ import annotations

import argparse
import random
import re
import string
import sys

PESOS_CNPJ_DV1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
PESOS_CNPJ_DV2 = [6] + PESOS_CNPJ_DV1
CARACTERES_ALFA = string.digits + string.ascii_uppercase
SEPARADORES = re.compile(r"[.\-/\s]")


def _dv_mod11(valores: list[int], pesos: list[int]) -> int:
    resto = sum(v * p for v, p in zip(valores, pesos)) % 11
    return 0 if resto < 2 else 11 - resto


def dv_cpf(base9: str) -> str:
    """Retorna os 2 DVs de um CPF a partir dos 9 primeiros dígitos."""
    if not re.fullmatch(r"[0-9]{9}", base9):
        raise ValueError("a base do CPF precisa ter exatamente 9 dígitos ASCII")
    valores = [int(c) for c in base9]
    d1 = _dv_mod11(valores, list(range(10, 1, -1)))
    d2 = _dv_mod11(valores + [d1], list(range(11, 1, -1)))
    return f"{d1}{d2}"


def dv_cnpj(base12: str) -> str:
    """Retorna os 2 DVs de um CNPJ (numérico ou alfanumérico) a partir das 12 primeiras posições."""
    if not re.fullmatch(r"[0-9A-Za-z]{12}", base12):
        raise ValueError("a base do CNPJ precisa ter exatamente 12 caracteres ASCII (0-9, A-Z)")
    valores = [ord(c) - 48 for c in base12.upper()]
    d1 = _dv_mod11(valores, PESOS_CNPJ_DV1)
    d2 = _dv_mod11(valores + [d1], PESOS_CNPJ_DV2)
    return f"{d1}{d2}"


def mascarar(valor: str) -> str:
    if len(valor) == 11:
        return f"{valor[:3]}.{valor[3:6]}.{valor[6:9]}-{valor[9:]}"
    if len(valor) == 14:
        return f"{valor[:2]}.{valor[2:5]}.{valor[5:8]}/{valor[8:12]}-{valor[12:]}"
    return valor


def gerar_cpf(rng: random.Random) -> str:
    while True:
        base = "".join(rng.choice(string.digits) for _ in range(9))
        if len(set(base)) > 1:
            return base + dv_cpf(base)


def gerar_cnpj(rng: random.Random, filial: bool = False) -> str:
    while True:
        raiz = "".join(rng.choice(string.digits) for _ in range(8))
        ordem = f"{rng.randint(2, 9999):04d}" if filial else "0001"
        base = raiz + ordem
        if len(set(raiz)) > 1:
            return base + dv_cnpj(base)


def gerar_cnpj_alfa(rng: random.Random) -> str:
    """Gera CNPJ com 12 posições alfanuméricas (garante ao menos uma letra) e DVs numéricos."""
    while True:
        base = "".join(rng.choice(CARACTERES_ALFA) for _ in range(12))
        if any(c.isalpha() for c in base):
            return base + dv_cnpj(base)


def validar(entrada: str) -> tuple[str, bool, str]:
    """Valida um valor. Retorna (tipo, válido, motivo/observação)."""
    bruto = entrada.strip()
    if not bruto:
        return ("?", False, "valor vazio")
    limpo = SEPARADORES.sub("", bruto)
    obs = []
    if not limpo.isascii():
        return ("?", False, "caractere(s) não permitido(s): apenas dígitos e letras ASCII")
    if limpo != limpo.upper():
        obs.append("letras minúsculas normalizadas para maiúsculas; confirme se o sistema deve aceitar")
        limpo = limpo.upper()
    invalidos = sorted({c for c in limpo if c not in CARACTERES_ALFA})
    if invalidos:
        return ("?", False, f"caractere(s) não permitido(s): {' '.join(invalidos)}")

    if len(limpo) == 11:
        tipo = "CPF"
        if not limpo.isdigit():
            return (tipo, False, "CPF só tem dígitos (letras não existem em CPF)")
        if len(set(limpo)) == 1:
            return (tipo, False, "sequência de um só dígito: passa no cálculo, mas é inválida")
        esperado = dv_cpf(limpo[:9])
        if limpo[9:] != esperado:
            return (tipo, False, f"dígito verificador esperado {esperado}, recebido {limpo[9:]}")
        return (tipo, True, "; ".join(obs))

    if len(limpo) == 14:
        alfa = not limpo.isdigit()
        tipo = "CNPJ alfanumérico" if alfa else "CNPJ"
        if not limpo[12:].isdigit():
            return (tipo, False, f"os 2 dígitos verificadores devem ser numéricos, recebido {limpo[12:]}")
        if len(set(limpo)) == 1:
            return (tipo, False, "sequência de um só caractere: passa no cálculo, mas é inválida")
        if limpo[:8] == "00000000" and limpo[8:12] == "0000":
            return (tipo, False, "raiz e ordem zeradas")
        esperado = dv_cnpj(limpo[:12])
        if limpo[12:] != esperado:
            return (tipo, False, f"dígito verificador esperado {esperado}, recebido {limpo[12:]}")
        if limpo[8:12] == "0000":
            obs.append("ordem 0000 não é usada pela Receita (matriz é 0001)")
        return (tipo, True, "; ".join(obs))

    return ("?", False, f"tamanho {len(limpo)} sem máscara; CPF tem 11 e CNPJ tem 14 posições")


# ---------------------------------------------------------------- self-test

def self_test() -> int:
    falhas = []

    def checar(cond: bool, msg: str) -> None:
        if not cond:
            falhas.append(msg)

    validos = {
        "529.982.247-25": "CPF",
        "52998224725": "CPF",
        "012.345.678-90": "CPF",  # zero à esquerda: quebra se guardado como inteiro
        "11.222.333/0001-81": "CNPJ",
        "11222333000181": "CNPJ",
        "00.000.000/0001-91": "CNPJ",
        "12.ABC.345/01DE-35": "CNPJ alfanumérico",  # exemplo da Receita/NT 2025.001
        "12ABC34501DE35": "CNPJ alfanumérico",
        "00.000.000/E08G-12": "CNPJ alfanumérico",  # 1º CNPJ alfanumérico emitido (31/07/2026)
    }
    for valor, tipo in validos.items():
        t, ok, motivo = validar(valor)
        checar(ok and t == tipo, f"deveria ser {tipo} válido: {valor} -> {t} {ok} {motivo}")

    invalidos = {
        "529.982.247-24": "dígito verificador esperado 25",
        "111.111.111-11": "sequência",
        "000.000.000-00": "sequência",
        "11.222.333/0001-80": "dígito verificador esperado 81",
        "00.000.000/0000-00": "sequência",
        "12.ABC.345/01DE-3A": "devem ser numéricos",
        "12.ABC.345/01DE-36": "esperado 35",
        "1234567890": "tamanho 10",
        "529.982.247-2#": "não permitido",
        "5299822472A": "só tem dígitos",
        "": "vazio",
    }
    for valor, trecho in invalidos.items():
        t, ok, motivo = validar(valor)
        checar(not ok and trecho in motivo, f"deveria ser inválido ({trecho}): {valor!r} -> {ok} {motivo}")

    t, ok, motivo = validar("12.abc.345/01de-35")
    checar(ok and "minúsculas" in motivo, f"minúsculas devem validar com aviso: {ok} {motivo}")

    # Tabela de valores de caracteres: A=17, Z=42.
    checar(ord("A") - 48 == 17 and ord("Z") - 48 == 42, "tabela ASCII-48")
    # Para CNPJ numérico, o cálculo alfanumérico deve coincidir com o tradicional.
    rng = random.Random(1)
    for _ in range(500):
        base = "".join(rng.choice(string.digits) for _ in range(12))
        v = [int(c) for c in base]
        r1 = sum(a * b for a, b in zip(v, PESOS_CNPJ_DV1)) % 11
        d1 = 0 if r1 < 2 else 11 - r1
        r2 = sum(a * b for a, b in zip(v + [d1], PESOS_CNPJ_DV2)) % 11
        d2 = 0 if r2 < 2 else 11 - r2
        checar(dv_cnpj(base) == f"{d1}{d2}", f"DV numérico divergente para {base}")

    # Ida e volta: tudo que é gerado precisa validar, com e sem máscara.
    rng = random.Random(42)
    geradores = [
        ("CPF", gerar_cpf, r"^\d{3}\.\d{3}\.\d{3}-\d{2}$"),
        ("CNPJ", gerar_cnpj, r"^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$"),
        ("CNPJ", lambda r: gerar_cnpj(r, filial=True), r"^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$"),
        ("CNPJ alfanumérico", gerar_cnpj_alfa, r"^[0-9A-Z]{2}\.[0-9A-Z]{3}\.[0-9A-Z]{3}/[0-9A-Z]{4}-\d{2}$"),
    ]
    for tipo, gerador, padrao in geradores:
        for _ in range(1000):
            valor = gerador(rng)
            t, ok, motivo = validar(valor)
            checar(ok and t == tipo, f"gerado inválido: {valor} -> {t} {motivo}")
            com_mascara = mascarar(valor)
            checar(re.match(padrao, com_mascara) is not None, f"máscara errada: {com_mascara}")
            checar(validar(com_mascara)[1], f"gerado com máscara inválido: {com_mascara}")

    # Mesma semente, mesma massa (reprodutibilidade).
    a = [gerar_cpf(random.Random(7)) for _ in range(3)]
    b = [gerar_cpf(random.Random(7)) for _ in range(3)]
    checar(a == b, "semente não reproduz a mesma massa")

    if falhas:
        print(f"self-test: {len(falhas)} falha(s)")
        for f in falhas[:20]:
            print(" -", f)
        return 1
    print("self-test: OK (casos conhecidos, inválidos, 4.000 gerados validados com e sem máscara)")
    return 0


# ---------------------------------------------------------------- CLI

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Gera e valida CPF e CNPJ (numérico e alfanumérico) para massa de teste.",
        epilog="Exemplos: gerar cnpj-alfa -n 3 --mascara | validar 529.982.247-25 12ABC34501DE35",
    )
    parser.add_argument("--self-test", action="store_true", help="roda as verificações internas e sai com 0 (ok) ou 1")
    sub = parser.add_subparsers(dest="comando")

    p_gerar = sub.add_parser("gerar", help="gera documentos válidos")
    p_gerar.add_argument("tipo", choices=["cpf", "cnpj", "cnpj-alfa"])
    p_gerar.add_argument("-n", type=int, default=1, help="quantidade (padrão 1)")
    p_gerar.add_argument("--mascara", action="store_true", help="formata com pontos, barra e hífen")
    p_gerar.add_argument("--filial", action="store_true", help="cnpj: ordem aleatória em vez de 0001 (matriz)")
    p_gerar.add_argument("--semente", type=int, help="semente para massa reproduzível")

    p_val = sub.add_parser("validar", help="valida um ou mais valores (use - para ler do stdin)")
    p_val.add_argument("valores", nargs="+")

    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    if args.comando is None:
        parser.print_help()
        return 2

    if args.comando == "gerar":
        if args.n < 1:
            parser.error("-n precisa ser >= 1")
        rng = random.Random(args.semente)
        for _ in range(args.n):
            if args.tipo == "cpf":
                valor = gerar_cpf(rng)
            elif args.tipo == "cnpj":
                valor = gerar_cnpj(rng, filial=args.filial)
            else:
                valor = gerar_cnpj_alfa(rng)
            print(mascarar(valor) if args.mascara else valor)
        return 0

    valores = []
    for v in args.valores:
        if v == "-":
            valores.extend(linha.rstrip("\n") for linha in sys.stdin if linha.strip())
        else:
            valores.append(v)
    if not valores:
        print("erro: nenhum documento informado no stdin", file=sys.stderr)
        return 2
    algum_invalido = False
    for v in valores:
        tipo, ok, motivo = validar(v)
        algum_invalido |= not ok
        status = "válido" if ok else "inválido"
        detalhe = f": {motivo}" if motivo else ""
        print(f"{v}\t{tipo}\t{status}{detalhe}")
    return 1 if algum_invalido else 0


if __name__ == "__main__":
    sys.exit(main())
