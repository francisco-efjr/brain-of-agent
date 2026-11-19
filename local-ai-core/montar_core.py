#!/usr/bin/env python3
"""Monta o CORE.md, o prompt de sistema único da IA local, a partir da base e dos temas.

O OpenJarvis aceita um só arquivo em system_prompt_path, então a base comum e os temas
são concatenados aqui, nesta ordem. Só biblioteca padrão (Python 3.10+).

Uso:
  python montar_core.py                          # base + todos os temas -> CORE.md
  python montar_core.py --temas windows          # base + só os temas escolhidos
  python montar_core.py --temas conhecimento --saida C:/caminho/CORE-pesquisa.md
  python montar_core.py --check                  # falha se o CORE.md estiver desatualizado
"""
from __future__ import annotations

import argparse
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parent
BASE = RAIZ / "CORE-BASE.md"
# Ordem de montagem. Tema novo: crie <tema>/CORE-<TEMA>.md e acrescente aqui.
TEMAS = {
    "windows": RAIZ / "windows" / "CORE-WINDOWS.md",
    "conhecimento": RAIZ / "conhecimento" / "CORE-CONHECIMENTO.md",
}
SAIDA_PADRAO = RAIZ / "CORE.md"
CABECALHO = (
    "<!-- Gerado por local-ai-core/montar_core.py a partir de CORE-BASE.md e dos temas: {temas}. "
    "Não edite à mão: edite as fontes e rode o script de novo. -->\n\n"
)


def montar(temas: list[str]) -> str:
    partes = [BASE.read_text(encoding="utf-8").strip()]
    partes += [TEMAS[t].read_text(encoding="utf-8").strip() for t in temas]
    return CABECALHO.format(temas=", ".join(temas)) + "\n\n".join(partes) + "\n"


def estimar_tokens(texto: str) -> int:
    # Aproximação para português em tokenizadores comuns; meça no seu modelo.
    return round(len(texto) / 3.2)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Monta o CORE.md da IA local.")
    parser.add_argument("--temas", default=",".join(TEMAS), help="temas separados por vírgula, na ordem desejada")
    parser.add_argument("--saida", type=pathlib.Path, default=SAIDA_PADRAO, help="arquivo de saída")
    parser.add_argument("--check", action="store_true", help="só confere se a saída está em dia")
    args = parser.parse_args(argv)

    temas = [t.strip() for t in args.temas.split(",") if t.strip()]
    desconhecidos = [t for t in temas if t not in TEMAS]
    if desconhecidos:
        parser.error(f"tema desconhecido: {', '.join(desconhecidos)}. Disponíveis: {', '.join(TEMAS)}")

    texto = montar(temas)
    resumo = f"{len(texto)} caracteres, cerca de {estimar_tokens(texto)} tokens"

    if args.check:
        atual = args.saida.read_text(encoding="utf-8") if args.saida.exists() else ""
        if atual != texto:
            print(f"{args.saida.name} desatualizado: rode python local-ai-core/montar_core.py", file=sys.stderr)
            return 1
        print(f"{args.saida.name} em dia ({resumo})")
        return 0

    args.saida.write_text(texto, encoding="utf-8", newline="\n")
    print(f"{args.saida} gerado com base + {', '.join(temas)} ({resumo})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
