#!/usr/bin/env python3
"""Monta o CORE.md, o prompt de sistema único da IA local, a partir da base e dos temas.

O OpenJarvis aceita um só arquivo em system_prompt_path, então a base comum e os temas
são concatenados aqui. Cada tema entra de um de dois modos:
  - completo: todas as regras do tema;
  - cartao:   só o bloco curto entre <!-- cartao:inicio --> e <!-- cartao:fim -->, que manda
              buscar as regras completas na memória (o CORE-<TEMA>.md também é indexado).
Perfis prontos definem o modo de cada tema. Só biblioteca padrão (Python 3.10+).

Uso:
  python montar_core.py                               # perfil padrao -> CORE.md
  python montar_core.py --perfil leve --saida C:/caminho/CORE-leve.md
  python montar_core.py --temas windows,memoria:cartao --saida C:/caminho/CORE-x.md
  python montar_core.py --check                       # falha se o CORE.md estiver desatualizado
"""
from __future__ import annotations

import argparse
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parent
BASE = RAIZ / "CORE-BASE.md"
# Ordem de montagem. Tema novo: crie <tema>/CORE-<TEMA>.md com um bloco de cartão e acrescente aqui e nos perfis.
TEMAS = {
    "windows": RAIZ / "windows" / "CORE-WINDOWS.md",
    "conhecimento": RAIZ / "conhecimento" / "CORE-CONHECIMENTO.md",
    "memoria": RAIZ / "memoria" / "CORE-MEMORIA.md",
}
PERFIS = {
    # O que o dono usa todo dia entra completo; o resto entra como cartão.
    "padrao": {"windows": "completo", "conhecimento": "completo", "memoria": "cartao"},
    "completo": {tema: "completo" for tema in TEMAS},
    "leve": {tema: "cartao" for tema in TEMAS},
}
MODOS = ("completo", "cartao")
INICIO = "<!-- cartao:inicio -->"
FIM = "<!-- cartao:fim -->"
SAIDA_PADRAO = RAIZ / "CORE.md"
CABECALHO = (
    "<!-- Gerado por local-ai-core/montar_core.py ({origem}): {temas}. "
    "Não edite à mão: edite as fontes e rode o script de novo. -->\n\n"
)


def partes_do_tema(texto: str, tema: str) -> tuple[str, str, str]:
    """Devolve (título, cartão, texto completo sem o cartão)."""
    if INICIO not in texto or FIM not in texto:
        raise ValueError(f"tema {tema} sem bloco de cartão ({INICIO} ... {FIM})")
    antes, resto = texto.split(INICIO, 1)
    cartao, depois = resto.split(FIM, 1)
    titulo = antes.strip().splitlines()[0]
    completo = (antes.rstrip() + "\n\n" + depois.lstrip()).strip()
    return titulo, cartao.strip(), completo


def bloco(tema: str, modo: str) -> str:
    titulo, cartao, completo = partes_do_tema(TEMAS[tema].read_text(encoding="utf-8"), tema)
    if modo == "completo":
        return completo
    return f"{titulo} (cartão)\n\n{cartao}"


def montar(escolha: dict[str, str], origem: str) -> str:
    partes = [BASE.read_text(encoding="utf-8").strip()]
    partes += [bloco(tema, modo) for tema, modo in escolha.items()]
    descricao = ", ".join(f"{tema} ({modo})" for tema, modo in escolha.items())
    return CABECALHO.format(origem=origem, temas=descricao) + "\n\n".join(partes) + "\n"


def estimar_tokens(texto: str) -> int:
    # Aproximação para português em tokenizadores comuns; meça no seu modelo.
    return round(len(texto) / 3.2)


def ler_temas(valor: str, parser: argparse.ArgumentParser) -> dict[str, str]:
    escolha: dict[str, str] = {}
    for item in (parte.strip() for parte in valor.split(",") if parte.strip()):
        tema, _, modo = item.partition(":")
        modo = modo or "completo"
        if tema not in TEMAS:
            parser.error(f"tema desconhecido: {tema}. Disponíveis: {', '.join(TEMAS)}")
        if modo not in MODOS:
            parser.error(f"modo desconhecido: {modo}. Use {' ou '.join(MODOS)}")
        escolha[tema] = modo
    return escolha


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Monta o CORE.md da IA local.")
    parser.add_argument("--perfil", choices=sorted(PERFIS), default="padrao", help="perfil pronto (padrão: padrao)")
    parser.add_argument("--temas", help="lista tema[:modo] separada por vírgula; substitui o perfil")
    parser.add_argument("--saida", type=pathlib.Path, default=SAIDA_PADRAO, help="arquivo de saída")
    parser.add_argument("--check", action="store_true", help="só confere se a saída está em dia")
    args = parser.parse_args(argv)

    if args.temas:
        escolha, origem = ler_temas(args.temas, parser), "temas escolhidos"
    else:
        escolha, origem = dict(PERFIS[args.perfil]), f"perfil {args.perfil}"

    texto = montar(escolha, origem)
    resumo = f"{len(texto)} caracteres, cerca de {estimar_tokens(texto)} tokens"

    if args.check:
        atual = args.saida.read_text(encoding="utf-8") if args.saida.exists() else ""
        if atual != texto:
            print(f"{args.saida.name} desatualizado: rode python local-ai-core/montar_core.py", file=sys.stderr)
            return 1
        print(f"{args.saida.name} em dia ({resumo})")
        return 0

    args.saida.write_text(texto, encoding="utf-8", newline="\n")
    print(f"{args.saida} gerado ({origem}: {', '.join(f'{t} {m}' for t, m in escolha.items())}; {resumo})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
