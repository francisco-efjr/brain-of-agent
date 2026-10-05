#!/usr/bin/env python3
"""Gera um conjunto de casos que cobre todos os pares de valores (pairwise).

Uso:
    python3 pairwise.py so=windows,macos,linux navegador=chrome,firefox,edge,safari idioma=pt,en
    python3 pairwise.py --arquivo params.json --csv > casos.csv
    python3 pairwise.py so=windows,macos navegador=edge,safari,chrome \\
        --excluir "so=macos&navegador=edge" --excluir "so=windows&navegador=safari"
    python3 pairwise.py --self-test

Entrada:
    param=v1,v2,v3      um argumento por parâmetro (valores separados por vírgula)
    --arquivo ARQ.json  {"param": ["v1", "v2"], ...}  (use para valores com vírgula)
    --excluir "a=x&b=y" combinação proibida (repetível). Um caso é descartado se
                        contiver TODAS as condições de alguma exclusão. Pode ter
                        1, 2 ou mais condições.

Saída: tabela markdown (padrão) ou CSV (--csv) no stdout. No stderr, um resumo:
casos gerados x produto cartesiano, pares cobertos e pares impossíveis (pares que
nenhuma combinação válida consegue conter por causa das exclusões).

Algoritmo: guloso no estilo AETG. A cada rodada gera vários candidatos; cada
candidato começa por um par ainda descoberto e completa os demais parâmetros
escolhendo o valor que cobre mais pares novos, sem violar exclusões e sem
entrar em beco sem saída (checagem por backtracking). Fica o melhor candidato.
É determinístico para a mesma entrada e a mesma --semente.

Limite do método: pairwise pega defeitos causados por interação de até dois
fatores. Interações de três fatores conhecidas por risco devem virar casos
explícitos, fora do pairwise.
"""
from __future__ import annotations

import argparse
import csv
import itertools
import json
import random
import sys
from typing import Dict, List, Optional, Sequence, Tuple

Parametros = List[Tuple[str, List[str]]]
Exclusao = Dict[int, str]  # índice do parâmetro -> valor
Caso = List[Optional[str]]


class ErroEntrada(Exception):
    pass


def _objeto_json(pares):
    dados = {}
    for nome, valor in pares:
        if nome in dados:
            raise ErroEntrada(f"parâmetro repetido no JSON: {nome!r}")
        dados[nome] = valor
    return dados


# ---------------------------------------------------------------- entrada

def ler_parametros(args_params: Sequence[str], arquivo: Optional[str]) -> Parametros:
    params: Parametros = []
    if arquivo:
        with open(arquivo, encoding="utf-8") as f:
            dados = json.load(f, object_pairs_hook=_objeto_json)
        if not isinstance(dados, dict):
            raise ErroEntrada("o JSON precisa ser um objeto {\"param\": [\"v1\", \"v2\"]}")
        for nome, valores in dados.items():
            if not nome.strip():
                raise ErroEntrada("o nome do parâmetro não pode ser vazio")
            if not isinstance(valores, list) or not valores:
                raise ErroEntrada(f"parâmetro {nome!r}: informe uma lista não vazia de valores")
            if not all(isinstance(v, str) for v in valores):
                raise ErroEntrada(f"parâmetro {nome!r}: cada valor deve ser uma string JSON")
            params.append((nome, valores))
    for item in args_params:
        if "=" not in item:
            raise ErroEntrada(f"argumento {item!r} não está no formato param=v1,v2")
        nome, _, resto = item.partition("=")
        valores = [v.strip() for v in resto.split(",")]
        if not nome.strip() or any(not v for v in valores):
            raise ErroEntrada(f"argumento {item!r} sem nome ou sem valores")
        params.append((nome.strip(), valores))
    nomes = [n for n, _ in params]
    repetidos = {n for n in nomes if nomes.count(n) > 1}
    if repetidos:
        raise ErroEntrada(f"parâmetro repetido: {', '.join(sorted(repetidos))}")
    limpos: Parametros = []
    for nome, valores in params:
        unicos = list(dict.fromkeys(valores))
        if len(unicos) != len(valores):
            print(f"aviso: valores repetidos removidos em {nome!r}", file=sys.stderr)
        limpos.append((nome, unicos))
    return limpos


def ler_exclusoes(textos: Sequence[str], params: Parametros) -> List[Exclusao]:
    """Converte "a=x&b=y" em {idx_a: "x", idx_b: "y"}. Nome ou valor desconhecido é erro:
    um erro de digitação aqui deixaria a combinação proibida passar em silêncio."""
    indice = {nome: i for i, (nome, _) in enumerate(params)}
    exclusoes: List[Exclusao] = []
    for texto in textos:
        exc: Exclusao = {}
        for cond in texto.split("&"):
            if "=" not in cond:
                raise ErroEntrada(f"exclusão {texto!r}: condição {cond!r} não está no formato param=valor")
            nome, _, valor = (s.strip() for s in cond.partition("="))
            if nome not in indice:
                raise ErroEntrada(f"exclusão {texto!r}: parâmetro desconhecido {nome!r}")
            if valor not in params[indice[nome]][1]:
                raise ErroEntrada(f"exclusão {texto!r}: valor {valor!r} não existe em {nome!r}")
            if indice[nome] in exc and exc[indice[nome]] != valor:
                raise ErroEntrada(f"exclusão {texto!r}: {nome!r} com dois valores nunca casa")
            exc[indice[nome]] = valor
        exclusoes.append(exc)
    return exclusoes


# ---------------------------------------------------------------- núcleo

def viola(caso: Caso, exclusoes: List[Exclusao]) -> bool:
    """True se todas as condições de alguma exclusão estão atribuídas e casam."""
    for exc in exclusoes:
        if all(caso[i] == v for i, v in exc.items()):
            return True
    return False


def completavel(caso: Caso, params: Parametros, exclusoes: List[Exclusao]) -> bool:
    """Backtracking: existe atribuição dos parâmetros vazios que não viola exclusões?"""
    if viola(caso, exclusoes):
        return False
    if not exclusoes:
        return True
    try:
        i = caso.index(None)
    except ValueError:
        return True
    for v in params[i][1]:
        caso[i] = v
        ok = completavel(caso, params, exclusoes)
        caso[i] = None
        if ok:
            return True
    return False


def todos_os_pares(params: Parametros) -> List[Tuple[int, str, int, str]]:
    pares = []
    for i, j in itertools.combinations(range(len(params)), 2):
        for vi in params[i][1]:
            for vj in params[j][1]:
                pares.append((i, vi, j, vj))
    return pares


def pares_do_caso(caso: Sequence[str]) -> set:
    return {(i, caso[i], j, caso[j]) for i, j in itertools.combinations(range(len(caso)), 2)}


def gerar(params: Parametros, exclusoes: List[Exclusao], semente: int = 2024,
          candidatos: int = 40) -> Tuple[List[List[str]], List[Tuple[int, str, int, str]]]:
    """Retorna (casos, pares_impossíveis)."""
    if not params or any(not valores for _, valores in params):
        raise ErroEntrada("informe pelo menos um parâmetro com valores não vazios")
    if candidatos < 1:
        raise ErroEntrada("candidatos precisa ser >= 1")
    n = len(params)
    rng = random.Random(semente)

    if n == 1:
        casos = [[v] for v in params[0][1] if not viola([v], exclusoes)]
        return casos, []

    impossiveis = []
    descobertos = set()
    for par in todos_os_pares(params):
        i, vi, j, vj = par
        caso: Caso = [None] * n
        caso[i], caso[j] = vi, vj
        if completavel(caso, params, exclusoes):
            descobertos.add(par)
        else:
            impossiveis.append(par)

    casos: List[List[str]] = []
    while descobertos:
        ordenados = sorted(descobertos, key=lambda p: (p[0], p[2], p[1], p[3]))
        melhor, melhor_ganho = None, -1
        for _ in range(candidatos):
            i, vi, j, vj = ordenados[rng.randrange(len(ordenados))]
            caso = [None] * n
            caso[i], caso[j] = vi, vj
            restantes = [k for k in range(n) if k not in (i, j)]
            rng.shuffle(restantes)
            for k in restantes:
                valores = list(params[k][1])
                rng.shuffle(valores)
                melhor_v, melhor_novos = None, -1
                for v in valores:
                    caso[k] = v
                    if not completavel(caso, params, exclusoes):
                        continue
                    novos = 0
                    for m in range(n):
                        if m != k and caso[m] is not None:
                            a, b = (m, k) if m < k else (k, m)
                            if (a, caso[a], b, caso[b]) in descobertos:
                                novos += 1
                    if novos > melhor_novos:
                        melhor_v, melhor_novos = v, novos
                caso[k] = melhor_v  # nunca None: o par semente é completável
            ganho = len(pares_do_caso(caso) & descobertos)
            if ganho > melhor_ganho:
                melhor, melhor_ganho = list(caso), ganho
        casos.append(melhor)
        descobertos -= pares_do_caso(melhor)
    return casos, impossiveis


# ---------------------------------------------------------------- saída

def escapar_md(texto: str) -> str:
    return texto.replace("\\", "\\\\").replace("|", "\\|").replace("\r", "\\r").replace("\n", "\\n")


def imprimir(params: Parametros, casos: List[List[str]], formato_csv: bool) -> None:
    nomes = [n for n, _ in params]
    if formato_csv:
        w = csv.writer(sys.stdout)
        w.writerow(["#"] + nomes)
        for k, caso in enumerate(casos, 1):
            w.writerow([k] + caso)
        return
    print("| # | " + " | ".join(escapar_md(n) for n in nomes) + " |")
    print("| --- " * (len(nomes) + 1) + "|")
    for k, caso in enumerate(casos, 1):
        print(f"| {k} | " + " | ".join(escapar_md(v) for v in caso) + " |")


def resumo(params: Parametros, casos, impossiveis, total_pares: int) -> str:
    cartesiano = 1
    for _, valores in params:
        cartesiano *= len(valores)
    cobertos = set().union(*(pares_do_caso(c) for c in casos))
    linhas = [f"pairwise: {len(casos)} casos (produto cartesiano: {cartesiano}); "
              f"pares cobertos: {len(cobertos)} de {total_pares - len(impossiveis)} possíveis"]
    if impossiveis:
        amostra = ", ".join(f"{params[i][0]}={vi} + {params[j][0]}={vj}" for i, vi, j, vj in impossiveis[:5])
        mais = f" (+{len(impossiveis) - 5})" if len(impossiveis) > 5 else ""
        linhas.append(f"pares impossíveis pelas exclusões: {len(impossiveis)}: {amostra}{mais}")
    for idx, (nome, valores) in enumerate(params):
        for v in valores:
            if not any(c[idx] == v for c in casos):
                linhas.append(f"aviso: {nome}={v} não aparece em nenhum caso (as exclusões o tornam impossível)")
    return "\n".join(linhas)


# ---------------------------------------------------------------- self-test

def verificar(params: Parametros, exclusoes: List[Exclusao], casos, impossiveis) -> List[str]:
    """Checagem independente do gerador: força bruta sobre o produto cartesiano."""
    erros = []
    validos = [list(c) for c in itertools.product(*[v for _, v in params]) if not viola(list(c), exclusoes)]
    possiveis = set()
    for c in validos:
        possiveis |= pares_do_caso(c)
    cobertos = set()
    for c in casos:
        if len(c) != len(params) or any(c[i] not in valores for i, (_, valores) in enumerate(params)):
            erros.append(f"caso fora dos domínios: {c}")
            continue
        if viola(c, exclusoes):
            erros.append(f"caso proibido gerado: {c}")
        if any(v is None for v in c):
            erros.append(f"caso incompleto: {c}")
        cobertos |= pares_do_caso(c)
    faltando = possiveis - cobertos
    if faltando:
        erros.append(f"{len(faltando)} pares possíveis sem cobertura, ex.: {sorted(faltando)[:3]}")
    if set(impossiveis) != set(todos_os_pares(params)) - possiveis:
        erros.append("lista de pares impossíveis difere do oráculo por força bruta")
    if len(params) == 1 and {tuple(c) for c in casos} != {tuple(c) for c in validos}:
        erros.append("um parâmetro: cobertura dos valores válidos incompleta")
    return erros


def self_test() -> int:
    erros: List[str] = []

    def rodar(nome, params, textos_exc=(), max_casos=None):
        exc = ler_exclusoes(list(textos_exc), params)
        casos, imp = gerar(params, exc)
        for e in verificar(params, exc, casos, imp):
            erros.append(f"[{nome}] {e}")
        if max_casos is not None and len(casos) > max_casos:
            erros.append(f"[{nome}] {len(casos)} casos, esperado no máximo {max_casos}")
        return casos, imp

    p3 = [("a", ["1", "2", "3"]), ("b", ["x", "y", "z"]), ("c", ["p", "q", "r"])]
    rodar("3x3x3 sem exclusões", p3, max_casos=12)  # ótimo teórico: 9; cartesiano: 27

    pn = [("so", ["windows", "macos", "linux"]), ("navegador", ["chrome", "firefox", "edge", "safari"]),
          ("idioma", ["pt", "en"]), ("tela", ["mobile", "desktop"])]
    rodar("com exclusões de 2 condições", pn,
          ["so=macos&navegador=edge", "so=windows&navegador=safari", "so=linux&navegador=safari"], max_casos=16)

    rodar("exclusão de 1 e de 3 condições", pn,
          ["navegador=firefox", "so=linux&idioma=en&tela=mobile"])

    # Exclusões que, juntas, tornam so=macos impossível: precisa detectar pares implícitos.
    pi = [("so", ["windows", "macos"]), ("navegador", ["chrome", "edge"]), ("idioma", ["pt", "en"])]
    casos, imp = rodar("impossibilidade implícita", pi, ["so=macos&navegador=chrome", "so=macos&navegador=edge"])
    if any(c[0] == "macos" for c in casos):
        erros.append("[impossibilidade implícita] macos apareceu apesar de impossível")
    if not any(p[1] == "macos" and p[2] == 2 for p in imp):
        erros.append("[impossibilidade implícita] par (so=macos, idioma) deveria ser impossível")

    grande = [(f"p{k}", ["0", "1", "2"]) for k in range(13)]
    casos, _ = gerar(grande, [])
    cobertos = set()
    for c in casos:
        cobertos |= pares_do_caso(c)
    if cobertos != set(todos_os_pares(grande)):
        erros.append("[3^13] cobertura incompleta")
    if len(casos) > 30:  # ótimo conhecido: 15; cartesiano: 1.594.323
        erros.append(f"[3^13] {len(casos)} casos, esperado no máximo 30")

    a, _ = gerar(pn, [], semente=7)
    b, _ = gerar(pn, [], semente=7)
    if a != b:
        erros.append("mesma semente gerou conjuntos diferentes")

    for ruim in (["so=macos&navegador=opera"], ["sistema=macos"], ["so"]):
        try:
            ler_exclusoes(ruim, pn)
            erros.append(f"exclusão inválida aceita: {ruim}")
        except ErroEntrada:
            pass

    if erros:
        print(f"self-test: {len(erros)} falha(s)")
        for e in erros:
            print(" -", e)
        return 1
    print(f"self-test: OK (cobertura por força bruta, exclusões explícitas e implícitas; 3^13 em {len(casos)} casos)")
    return 0


# ---------------------------------------------------------------- CLI

def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Gera casos que cobrem todos os pares de valores (pairwise), com exclusões opcionais.",
        epilog='Exemplo: pairwise.py so=windows,macos navegador=chrome,edge --excluir "so=macos&navegador=edge"',
    )
    parser.add_argument("parametros", nargs="*", help="param=v1,v2,v3 (um por parâmetro)")
    parser.add_argument("--arquivo", help='JSON {"param": ["v1", "v2"]}')
    parser.add_argument("--excluir", action="append", default=[], metavar='"a=x&b=y"',
                        help="combinação proibida; repetível")
    parser.add_argument("--csv", action="store_true", help="saída em CSV em vez de tabela markdown")
    parser.add_argument("--semente", type=int, default=2024, help="semente do desempate aleatório (padrão 2024)")
    parser.add_argument("--self-test", action="store_true", help="roda as verificações internas e sai com 0 (ok) ou 1")
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()
    try:
        params = ler_parametros(args.parametros, args.arquivo)
        if not params:
            parser.error("informe parâmetros (param=v1,v2) ou --arquivo")
        exclusoes = ler_exclusoes(args.excluir, params)
    except (ErroEntrada, OSError, json.JSONDecodeError) as e:
        print(f"erro: {e}", file=sys.stderr)
        return 2

    casos, impossiveis = gerar(params, exclusoes, semente=args.semente)
    if not casos:
        print("erro: as exclusões não deixam nenhuma combinação válida", file=sys.stderr)
        return 2
    imprimir(params, casos, args.csv)
    print(resumo(params, casos, impossiveis, len(todos_os_pares(params))), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
