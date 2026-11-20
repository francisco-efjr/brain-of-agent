#!/usr/bin/env python3
"""Servidor MCP local da camada de SO (stdio). O OpenJarvis inicia este arquivo.

Uso:
  python servidor_so.py                      # servidor MCP por stdio (o OpenJarvis chama assim)
  python servidor_so.py --config C:/caminho/so-config.json
  python servidor_so.py --autoteste          # confere tudo neste PC e mostra um relatório
  python servidor_so.py --testar-janela      # abre a janela de aprovação R2 para você ver se aparece

Configuração: --config, ou a variável IA_OPERADOR_SO_CONFIG, ou %USERPROFILE%\\IA-Operador\\so-config.json
se existir; sem nada disso, valem os padrões de so_mcp/config.py.
"""
from __future__ import annotations

import argparse
import os
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from so_mcp import NOME, VERSAO  # noqa: E402
from so_mcp import config as configuracao  # noqa: E402
from so_mcp.estado import AREAS, VALIDADOR_PS  # noqa: E402
from so_mcp import politica  # noqa: E402


def achar_config(argumento: str | None) -> pathlib.Path | None:
    if argumento:
        return pathlib.Path(argumento)
    if os.environ.get("IA_OPERADOR_SO_CONFIG"):
        return pathlib.Path(os.environ["IA_OPERADOR_SO_CONFIG"])
    padrao = configuracao.caminho("%USERPROFILE%\\IA-Operador\\so-config.json")
    return padrao if padrao.is_file() else None


def autoteste(ferr) -> int:
    from so_mcp.estado import Leitor

    ok_total = True

    def linha(ok: bool, texto: str) -> None:
        nonlocal ok_total
        ok_total &= ok
        print(f"[{'OK' if ok else 'FALHOU'}] {texto}")

    print(f"{NOME} {VERSAO} — autoteste em {time.strftime('%Y-%m-%d %H:%M')}")
    linha(sys.version_info >= (3, 10), f"Python {sys.version.split()[0]} (precisa de 3.10+)")
    linha(ferr.executor.disponivel(), f"PowerShell: {ferr.cfg.powershell}")
    linha(True, f"pasta da IA: {ferr.cfg.pasta_operador}")
    linha(ferr.cfg.pasta_regras.is_dir(), f"regras em {ferr.cfg.pasta_regras} (temas: {', '.join(ferr.regras.temas())})")
    if not ferr.executor.disponivel():
        print("Sem PowerShell, o resto do autoteste não roda. Este servidor opera o Windows.")
        return 1

    leitor = Leitor(ferr.cfg, ferr.executor)
    for area in AREAS:
        texto, falhou = leitor.estado(area, None, 3)
        primeira = next((l for l in texto.splitlines() if l.strip()), "")[:90]
        linha(not falhou, f"so_estado {area}: {primeira}")

    casos = [("Get-Date", True), ("Get-Process | Select-Object -First 3 Name", True),
             ("Get-Process | Stop-Process -WhatIf", False), ("[IO.File]::Exists('C:\\x')", False),
             ("Get-ChildItem | ForEach-Object { $_.Delete() }", False), ("Invoke-Expression 'Get-Date'", False)]
    args = {"VERBOS": ",".join(sorted(politica.VERBOS_LEITURA)),
            "EXTERNOS": ",".join(sorted(e.removesuffix(".exe") for e in politica.EXTERNOS)),
            "METODOS": ",".join(sorted(politica.METODOS_OK)), "TIPOS": ",".join(sorted(politica.TIPOS_ESTATICOS_OK)),
            "NEGADOS": ",".join(sorted(politica.CMDLETS_NEGADOS)), "EXTRA": ",".join(sorted(politica.CMDLETS_EXTRA))}
    for comando, aceito in casos:
        r = ferr.executor.rodar(VALIDADOR_PS, {**args, "COMANDO": comando}, rotulo="autoteste")
        recusado = r.saida.strip().startswith("RECUSADO")
        linha(recusado != aceito, f"validador do PowerShell {'aceita' if aceito else 'recusa'}: {comando}")

    alvo = ferr.cfg.pasta_operador / f"autoteste-{time.strftime('%Y%m%d-%H%M%S')}"
    texto, falhou = ferr.planejador.planejar("pasta_criar", {"caminho": str(alvo)}, "autoteste")
    linha(not falhou and "[R1]" in texto, "plano R1 de pasta_criar")
    if not falhou:
        texto, falhou = ferr.planejador.executar()
        linha(not falhou and alvo.is_dir() and "STATUS: Verificado" in texto, "execução R1 sem janela e verificação")
        pid = ferr.planejador.registro.ultimos(1, "execucao")[0].get("plano", "")
        texto, falhou = ferr.planejador.desfazer(pid)
        if not falhou:
            texto, falhou = ferr.planejador.executar()
        linha(not falhou and not alvo.exists(), "desfazer (remove a pasta criada)")
    texto, _ = ferr.memoria.bastao_ler()
    linha(True, f"memória ({ferr.memoria.nome}): {texto.splitlines()[0][:80]}")
    print("Tudo certo." if ok_total else "Há falhas: veja as linhas FALHOU acima.")
    return 0 if ok_total else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Servidor MCP local da camada de SO da IA local.")
    parser.add_argument("--config", help="arquivo so-config.json")
    parser.add_argument("--autoteste", action="store_true", help="confere o servidor neste PC")
    parser.add_argument("--testar-janela", action="store_true", help="abre a janela de aprovação R2 para teste")
    args = parser.parse_args(argv)

    from so_mcp.ferramentas import Ferramentas
    from so_mcp.protocolo import ServidorMcp

    cfg = configuracao.carregar(achar_config(args.config))
    cfg.preparar_pastas()
    ferr = Ferramentas(cfg)
    if args.autoteste:
        return autoteste(ferr)
    if args.testar_janela:
        ok, detalhe = ferr.confirmador.pedir("R2", "Teste da IA local", "Isto é só um teste da janela de aprovação.\nClique Sim ou Não.")
        print(detalhe)
        return 0
    print(f"[so-mcp] {NOME} {VERSAO} pronto (pasta {cfg.pasta_operador})", file=sys.stderr)
    ServidorMcp(ferr).rodar()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
