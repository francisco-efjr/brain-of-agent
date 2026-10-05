#!/usr/bin/env python3
"""Roda um comando N vezes e mede a intermitência (diagnóstico de teste flaky).

Uso:
    python3 repetir_teste.py -n 30 -- npx playwright test tests/checkout.spec.ts --workers=1
    python3 repetir_teste.py -n 50 --paralelo 4 -- pytest tests/test_pedido.py -x -q
    python3 repetir_teste.py -n 20 --paralelo 4 --comparar -- npm test -- pedido
    python3 repetir_teste.py -n 100 --parar-na-falha --saida falhas/ -- go test ./... -run TestSaldo -count=1
    python3 repetir_teste.py --self-test

O que faz:
    - roda o comando N vezes (em série ou com --paralelo P execuções simultâneas);
    - cada execução recebe a variável de ambiente REPETICAO=1..N (útil para
      gerar dados únicos e para reproduzir uma execução específica);
    - mede taxa de falha e duração (mín, mediana, p95, máx);
    - salva stdout/stderr das execuções que falharam (pasta --saida; padrão
      ./repetir-teste-AAAAMMDD-HHMMSS, criada só se houver falha);
    - agrupa as falhas pela última linha de erro (números, UUIDs e horários
      normalizados para que "Timeout 5000ms" e "Timeout 5003ms" caiam juntos);
    - imprime um diagnóstico curto com as hipóteses mais prováveis.

--comparar roda N em série e depois N com --paralelo P e compara as taxas:
falhar só em paralelo sugere investigar estado compartilhado, saturação e
limites de recursos; a comparação sozinha não identifica a causa.

Pipes e redirecionamentos: passe por um shell, ex.: -- sh -c "npm test | tee log.txt".
Código de saída: 0 se nenhuma execução falhou, 1 se alguma falhou, 2 erro de uso.
"""
from __future__ import annotations

import argparse
import math
import os
import re
import shlex
import shutil
import signal
import statistics
import subprocess
import sys
import tempfile
import threading
import time
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Dict, List, Optional

PADRAO_ERRO = re.compile(
    r"error|erro|exception|exceção|fail|falh|assert|timeout|timed out|traceback|refused|recusad|panic|fatal",
    re.IGNORECASE)
# Linhas de resumo do runner ("1 failed, 3 passed in 2.1s") não identificam a causa.
PADRAO_RESUMO = re.compile(
    r"\b\d+\s+(failed|passed|skipped|errors?|tests?|falha(s|ram)?|passaram)\b|^=+.*=+$|^Tests?:|^Ran \d+ tests?",
    re.IGNORECASE)
NORMALIZACOES = [
    (re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I), "<uuid>"),
    (re.compile(r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:?\d{2})?"), "<data-hora>"),
    (re.compile(r"\b0x[0-9a-f]+\b", re.I), "<hex>"),
    (re.compile(r"\d+([.,]\d+)?"), "<n>"),
]


# ---------------------------------------------------------------- execução

def executar(idx: int, cmd: List[str], timeout: Optional[float], parar: threading.Event,
             parar_na_falha: bool) -> Optional[Dict]:
    if parar.is_set():
        return None
    env = dict(os.environ, REPETICAO=str(idx))
    posix = os.name == "posix"
    inicio = time.perf_counter()
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env,
                            start_new_session=posix)
    estourou = False
    try:
        out, err = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        estourou = True
        try:
            if posix:
                os.killpg(proc.pid, signal.SIGKILL)  # mata também os processos filhos (npm -> node)
            else:
                proc.kill()
        except ProcessLookupError:
            pass
        out, err = proc.communicate()
    duracao = time.perf_counter() - inicio
    r = {
        "idx": idx,
        "rc": proc.returncode,
        "timeout": estourou,
        "duracao": duracao,
        "stdout": out.decode("utf-8", errors="replace"),
        "stderr": err.decode("utf-8", errors="replace"),
    }
    r["falhou"] = estourou or proc.returncode != 0
    if r["falhou"] and parar_na_falha:
        parar.set()
    progresso = "T" if estourou else ("F" if r["falhou"] else ".")
    print(progresso, end="", file=sys.stderr, flush=True)
    return r


def rodar_lote(cmd: List[str], n: int, paralelo: int, timeout: Optional[float],
               parar_na_falha: bool) -> List[Dict]:
    if n < 1 or paralelo < 1:
        raise ValueError("n e paralelo precisam ser >= 1")
    if timeout is not None and (not math.isfinite(timeout) or timeout <= 0):
        raise ValueError("timeout precisa ser finito e positivo")
    parar = threading.Event()
    with ThreadPoolExecutor(max_workers=max(1, paralelo)) as pool:
        futuros = [pool.submit(executar, i, cmd, timeout, parar, parar_na_falha) for i in range(1, n + 1)]
        resultados = [f.result() for f in futuros]
    print(file=sys.stderr)
    return [r for r in resultados if r is not None]


# ---------------------------------------------------------------- análise

def percentil(valores: List[float], p: float) -> float:
    """Percentil pelo método do posto mais próximo (nearest-rank)."""
    ordenados = sorted(valores)
    k = max(1, math.ceil(p / 100 * len(ordenados)))
    return ordenados[k - 1]


def linha_de_erro(r: Dict, timeout: Optional[float]) -> str:
    if r["timeout"]:
        return f"TIMEOUT: passou de {timeout:g} s (processo encerrado)"
    for texto in (r["stderr"], r["stdout"]):
        linhas = [ln.strip() for ln in texto.splitlines() if ln.strip()]
        for ln in reversed(linhas):
            if PADRAO_ERRO.search(ln) and not PADRAO_RESUMO.search(ln):
                return ln[:300]
    for texto in (r["stderr"], r["stdout"]):
        linhas = [ln.strip() for ln in texto.splitlines() if ln.strip()]
        if linhas:
            return linhas[-1][:300]
    return f"(sem saída) código de saída {r['rc']}"


def normalizar(linha: str) -> str:
    for padrao, troca in NORMALIZACOES:
        linha = padrao.sub(troca, linha)
    return linha


def agrupar(falhas: List[Dict], timeout: Optional[float]) -> "OrderedDict[str, Dict]":
    grupos: "OrderedDict[str, Dict]" = OrderedDict()
    for r in sorted(falhas, key=lambda x: x["idx"]):
        linha = linha_de_erro(r, timeout)
        g = grupos.setdefault(normalizar(linha), {"exemplo": linha, "execucoes": [], "codigos": set()})
        g["execucoes"].append(r["idx"])
        g["codigos"].add("timeout" if r["timeout"] else str(r["rc"]))
    return OrderedDict(sorted(grupos.items(), key=lambda kv: -len(kv[1]["execucoes"])))


def fmt(x: float, casas: int = 2) -> str:
    return f"{x:.{casas}f}".replace(".", ",")


def pct(parte: int, total: int) -> str:
    return fmt(100 * parte / max(1, total), 1) + "%"


def diagnostico(res: List[Dict], paralelo: int, grupos, n_pedido: int, comparando: bool = False) -> List[str]:
    total = len(res)
    falhas = [r for r in res if r["falhou"]]
    oks = [r for r in res if not r["falhou"]]
    d: List[str] = []
    if not total:
        return ["Nenhuma execução: não há evidência para estimar a taxa de falha."]
    if not falhas:
        limite = 100 * -math.expm1(math.log(0.05) / total)
        d.append(f"Nenhuma falha em {total} execuções. Isso não prova estabilidade: com 0 de {total}, "
                 f"o limite superior binomial unilateral de 95% é {limite:.2f}% "
                 f"(aproximado pela regra do três). Só vale para repetições independentes, "
                 f"com probabilidade de falha constante; ~300 verdes sustentam limite abaixo de 1% "
                 f"sob essas hipóteses. Cache, retries e estado compartilhado podem invalidá-las.")
        return d
    if not oks:
        d.append("Falhou em todas as execuções observadas: compatível com falha determinística, "
                 "mas a amostra não exclui intermitência. Investigue defeito, ambiente e comando; "
                 "leia a saída salva da primeira execução.")
        return d
    d.append(f"Intermitente: {len(falhas)} de {total} ({pct(len(falhas), total)}).")
    if len(grupos) > 1:
        d.append(f"{len(grupos)} assinaturas de erro diferentes: provavelmente mais de uma causa; "
                 "ataque a mais frequente primeiro.")
    if any(r["timeout"] for r in falhas) or any("timeout" in k.lower() or "timed out" in k.lower() for k in grupos):
        d.append("Há falhas por timeout: suspeite de espera insuficiente, dependência lenta, fila "
                 "ou deadlock. Aumentar o timeout só esconde o sintoma se a lentidão for o defeito.")
    med_ok = statistics.median(r["duracao"] for r in oks)
    med_f = statistics.median(r["duracao"] for r in falhas)
    if med_f >= 1.5 * med_ok:
        d.append(f"Falhas são mais lentas (mediana {fmt(med_f)} s × {fmt(med_ok)} s nas verdes): "
                 "padrão de espera, timeout ou recurso disputado.")
    elif med_f <= 0.5 * med_ok:
        d.append(f"Falhas terminam mais rápido (mediana {fmt(med_f)} s × {fmt(med_ok)} s): o teste quebra "
                 "cedo — preparação, dado ausente, conexão recusada, porta ou arquivo ocupado.")
    idx_falhas = sorted(r["idx"] for r in falhas)
    if idx_falhas == [1]:
        d.append("Só a primeira execução falhou: investigue aquecimento (cache frio, compilação, migração, "
                 "container ainda subindo).")
    meio = n_pedido / 2
    primeira = sum(1 for i in idx_falhas if i <= meio)
    segunda = len(idx_falhas) - primeira
    if segunda >= 3 and segunda >= 2 * max(primeira, 1):
        d.append("As falhas se concentram nas últimas repetições: acúmulo de estado (dados residuais, "
                 "disco, conexões abertas, memória) ou rate limit de algum serviço.")
    if paralelo > 1 and not comparando:
        d.append(f"Rodou com --paralelo {paralelo}: repita com --paralelo 1 (ou use --comparar). "
                 "Se a taxa cair, investigue estado compartilhado entre execuções "
                 "(dado fixo, mesma conta, porta, arquivo, banco), saturação e rate limit.")
    elif paralelo == 1:
        d.append("Falha em série, sem concorrência entre execuções: suspeite de espera por tempo fixo, "
                 "relógio/fuso/data, ordem não garantida (consulta sem ORDER BY), aleatoriedade sem "
                 "semente, dependência da ordem dos testes ou serviço externo instável.")
    return d


def relatorio(titulo: str, res: List[Dict], paralelo: int, timeout: Optional[float],
              n_pedido: int, pasta: Optional[str], comparando: bool = False) -> str:
    falhas = [r for r in res if r["falhou"]]
    duracoes = [r["duracao"] for r in res]
    grupos = agrupar(falhas, timeout)
    puladas = n_pedido - len(res)
    out = [f"== {titulo} ==",
           f"Execuções: {len(res)} de {n_pedido} (paralelo {paralelo})"
           + (f", {puladas} puladas por --parar-na-falha" if puladas else "")
           + f" | falhas: {len(falhas)} ({pct(len(falhas), len(res))})"]
    if duracoes:
        out.append(f"Duração (s): mín {fmt(min(duracoes))} | mediana {fmt(statistics.median(duracoes))} | "
                   f"p95 {fmt(percentil(duracoes, 95))} | máx {fmt(max(duracoes))}")
    if grupos:
        out.append("Falhas agrupadas pela última linha de erro:")
        for g in grupos.values():
            ex = g["execucoes"]
            lista = ", ".join(map(str, ex[:10])) + (f" … (+{len(ex) - 10})" if len(ex) > 10 else "")
            out.append(f"  {len(ex)}x  {g['exemplo']}")
            out.append(f"       execuções: {lista}; código de saída: {', '.join(sorted(g['codigos']))}")
    if pasta and falhas:
        out.append(f"Saídas das falhas em: {pasta}")
    out.append("Diagnóstico:")
    out += [f"  - {linha}" for linha in diagnostico(res, paralelo, grupos, n_pedido, comparando)] if res else ["  - nada executado"]
    return "\n".join(out)


def salvar_falhas(res: List[Dict], pasta: str, prefixo: str = "") -> None:
    falhas = [r for r in res if r["falhou"]]
    if not falhas:
        return
    os.makedirs(pasta, exist_ok=True)
    for r in falhas:
        base = os.path.join(pasta, f"{prefixo}exec-{r['idx']:03d}")
        with open(base + ".stdout.txt", "w", encoding="utf-8") as f:
            f.write(r["stdout"])
        with open(base + ".stderr.txt", "w", encoding="utf-8") as f:
            f.write(r["stderr"])


def comparativo(serie: List[Dict], par: List[Dict], paralelo: int) -> str:
    def taxa(res):
        return sum(r["falhou"] for r in res) / max(1, len(res))
    ts, tp = taxa(serie), taxa(par)
    msg = f"Comparação: série {fmt(100 * ts, 1)}% × paralelo ({paralelo}) {fmt(100 * tp, 1)}% de falha. "
    if ts == 0 and tp == 0:
        return msg + "Sem falhas nos dois modos."
    if ts == 0:
        return msg + ("Falha só em paralelo: investigue estado compartilhado entre execuções "
                      "(dado fixo, mesma conta, porta, arquivo, banco), saturação e rate limit. "
                      "Isole os dados (REPETICAO mais um identificador do lote) e repita alternando "
                      "a ordem dos modos; deriva do ambiente também pode explicar a diferença.")
    if tp >= 2 * ts:
        return msg + ("Taxa observada maior em paralelo: investigue estado compartilhado e saturação; "
                      "amostra e mudança do ambiente podem explicar a diferença.")
    return msg + "Há falhas também em série; esta amostra não determina o peso da concorrência."


# ---------------------------------------------------------------- self-test

def self_test() -> int:
    erros: List[str] = []
    py = sys.executable
    tmp = tempfile.mkdtemp(prefix="repetir-selftest-")

    def script(nome: str, corpo: str) -> List[str]:
        caminho = os.path.join(tmp, nome)
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(corpo)
        return [py, caminho]

    ok = script("ok.py", "print('ok')\n")
    falha = script("falha.py", "import sys\nprint('AssertionError: esperado 3, obtido 4', file=sys.stderr)\nsys.exit(1)\n")
    intermitente = script("intermitente.py", (
        "import os, sys\n"
        "i = int(os.environ['REPETICAO'])\n"
        "if i % 3 == 0:\n"
        "    print('rodando...')\n"
        "    print(f'TimeoutError: Timeout {5000 + i}ms exceeded at 2026-10-05T10:00:0{i % 10}Z', file=sys.stderr)\n"
        "    print('1 failed, 2 passed in 0.10s', file=sys.stderr)\n"
        "    sys.exit(1)\n"))
    trava = os.path.join(tmp, "porta.lock")
    compartilhado = script("compartilhado.py", (
        "import os, sys, time\n"
        f"trava = {trava!r}\n"
        "try:\n"
        "    fd = os.open(trava, os.O_CREAT | os.O_EXCL)\n"
        "except FileExistsError:\n"
        "    print('OSError: porta 8080 já está em uso', file=sys.stderr)\n"
        "    sys.exit(1)\n"
        "time.sleep(0.25)\n"
        "os.close(fd)\n"
        "os.remove(trava)\n"))
    lento = script("lento.py", "import time\ntime.sleep(5)\n")

    # Funções puras
    if percentil(list(range(1, 21)), 95) != 19 or percentil([7.0], 95) != 7.0:
        erros.append("percentil nearest-rank incorreto")
    if normalizar("Timeout 5000ms at 2026-01-01T10:00:00Z id 3f2b1c9e-1a2b-4c3d-9e8f-0a1b2c3d4e5f") != \
            normalizar("Timeout 3000ms at 2025-12-31T23:59:59Z id 00000000-0000-4000-8000-000000000000"):
        erros.append("normalização não agrupou mensagens equivalentes")

    res = rodar_lote(ok, 5, 1, None, False)
    if len(res) != 5 or any(r["falhou"] for r in res):
        erros.append("comando ok: deveria ter 5 execuções verdes")
    if "regra do três" not in " ".join(diagnostico(res, 1, {}, 5)):
        erros.append("diagnóstico sem falhas deveria citar a regra do três")

    res = rodar_lote(falha, 4, 2, None, False)
    g = agrupar([r for r in res if r["falhou"]], None)
    if sum(r["falhou"] for r in res) != 4 or len(g) != 1:
        erros.append("comando que sempre falha: esperadas 4 falhas em 1 grupo")
    if "determinística" not in " ".join(diagnostico(res, 2, g, 4)):
        erros.append("falha em todas deveria ser diagnosticada como determinística")

    res = rodar_lote(intermitente, 9, 3, None, False)
    falhas = [r for r in res if r["falhou"]]
    g = agrupar(falhas, None)
    if sorted(r["idx"] for r in falhas) != [3, 6, 9]:
        erros.append(f"intermitente: esperadas falhas em 3, 6, 9; veio {[r['idx'] for r in falhas]}")
    if len(g) != 1 or "TimeoutError" not in next(iter(g.values()))["exemplo"]:
        erros.append(f"intermitente: agrupamento/linha de erro errados: {list(g.values())[:1]}")
    pasta = os.path.join(tmp, "saida")
    salvar_falhas(res, pasta)
    if len(os.listdir(pasta)) != 6:
        erros.append("deveria salvar stdout e stderr das 3 falhas (6 arquivos)")

    res = rodar_lote(falha, 10, 1, None, True)
    if len(res) != 1:
        erros.append(f"--parar-na-falha em série deveria parar após 1 execução; rodou {len(res)}")

    res = rodar_lote(lento, 2, 2, 0.5, False)
    if not all(r["timeout"] for r in res) or max(r["duracao"] for r in res) > 4:
        erros.append("timeout não encerrou o processo")
    if "TIMEOUT" not in next(iter(agrupar(res, 0.5).values()))["exemplo"]:
        erros.append("timeout deveria virar grupo TIMEOUT")

    serie = rodar_lote(compartilhado, 6, 1, None, False)
    par = rodar_lote(compartilhado, 6, 4, None, False)
    comp = comparativo(serie, par, 4)
    if any(r["falhou"] for r in serie) or not any(r["falhou"] for r in par) or "só em paralelo" not in comp:
        erros.append(f"estado compartilhado não detectado: {comp}")

    shutil.rmtree(tmp, ignore_errors=True)
    if erros:
        print(f"self-test: {len(erros)} falha(s)")
        for e in erros:
            print(" -", e)
        return 1
    print("self-test: OK (verde, falha fixa, intermitente 3/9, parar na falha, timeout, estado compartilhado)")
    return 0


# ---------------------------------------------------------------- CLI

def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Roda um comando N vezes e mede a taxa de falha (diagnóstico de teste intermitente).",
        usage="%(prog)s -n N [--paralelo P] [--comparar] [--parar-na-falha] [--timeout S] [--saida PASTA] "
              "-- comando [args...]")
    parser.add_argument("-n", type=int, default=20, help="número de execuções (padrão 20)")
    parser.add_argument("--paralelo", type=int, default=1, help="execuções simultâneas (padrão 1)")
    parser.add_argument("--comparar", action="store_true",
                        help="roda N em série e N com --paralelo P e compara as taxas")
    parser.add_argument("--parar-na-falha", action="store_true", help="não inicia novas execuções após a 1ª falha")
    parser.add_argument("--timeout", type=float, help="segundos por execução; estourar conta como falha")
    parser.add_argument("--saida", help="pasta para stdout/stderr das falhas")
    parser.add_argument("--self-test", action="store_true", help="roda as verificações internas e sai com 0 (ok) ou 1")
    parser.add_argument("comando", nargs=argparse.REMAINDER, help="comando a repetir, depois de --")
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()
    cmd = args.comando[1:] if args.comando[:1] == ["--"] else args.comando
    if not cmd:
        parser.error("informe o comando depois de --")
    if args.n < 1 or args.paralelo < 1:
        parser.error("-n e --paralelo precisam ser >= 1")
    if args.timeout is not None and (not math.isfinite(args.timeout) or args.timeout <= 0):
        parser.error("--timeout precisa ser finito e positivo")
    if args.comparar and args.paralelo < 2:
        parser.error("--comparar precisa de --paralelo 2 ou mais")
    if shutil.which(cmd[0]) is None and not os.path.exists(cmd[0]):
        print(f"erro: comando não encontrado: {cmd[0]}", file=sys.stderr)
        return 2

    pasta = args.saida or f"repetir-teste-{datetime.now():%Y%m%d-%H%M%S}"
    print(f"Comando: {shlex.join(cmd)}")
    blocos = []
    if args.comparar:
        serie = rodar_lote(cmd, args.n, 1, args.timeout, args.parar_na_falha)
        par = rodar_lote(cmd, args.n, args.paralelo, args.timeout, args.parar_na_falha)
        salvar_falhas(serie, pasta, "serie-")
        salvar_falhas(par, pasta, "paralelo-")
        blocos.append(relatorio("Em série", serie, 1, args.timeout, args.n, pasta))
        blocos.append(relatorio(f"Em paralelo ({args.paralelo})", par, args.paralelo, args.timeout, args.n,
                                pasta, comparando=True))
        blocos.append(comparativo(serie, par, args.paralelo))
        houve_falha = any(r["falhou"] for r in serie + par)
    else:
        res = rodar_lote(cmd, args.n, args.paralelo, args.timeout, args.parar_na_falha)
        salvar_falhas(res, pasta)
        blocos.append(relatorio("Resultado", res, args.paralelo, args.timeout, args.n, pasta))
        houve_falha = any(r["falhou"] for r in res)
    texto = "\n\n".join(blocos)
    print(texto)
    if houve_falha:
        with open(os.path.join(pasta, "resumo.txt"), "w", encoding="utf-8") as f:
            f.write(f"Comando: {shlex.join(cmd)}\n\n{texto}\n")
    return 1 if houve_falha else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError) as erro:
        print(f"erro: {erro}", file=sys.stderr)
        sys.exit(2)
