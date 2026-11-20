"""Roda PowerShell sem shell intermediário.

Os parâmetros nunca entram no texto do script: vão por variáveis de ambiente SO_P_<NOME> e o
script lê com (P 'NOME'). Assim, um nome de serviço ou caminho vindo do modelo é sempre dado,
nunca código. O script vai por -EncodedCommand (UTF-16LE em base64), sem arquivo .ps1.
"""
from __future__ import annotations

import base64
import json
import os
import pathlib
import shutil
import subprocess
import time
import uuid
from dataclasses import dataclass
from typing import Any

PRELUDIO = r"""
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}
$OutputEncoding = [System.Text.Encoding]::UTF8
function P([string]$n) { [Environment]::GetEnvironmentVariable('SO_P_' + $n) }
"""

# Roda o script interno elevado. O UAC é a trava: o usuário vê a janela segura do Windows e decide.
_LANCADOR_ELEVADO = r"""
try {
    $p = Start-Process -FilePath (P 'EXE') -ArgumentList '-NoProfile','-NonInteractive','-WindowStyle','Hidden','-EncodedCommand',(P 'INTERNO') -Verb RunAs -Wait -PassThru -WindowStyle Hidden
    exit $p.ExitCode
} catch {
    Write-Output ('UAC: ' + $_.Exception.Message)
    exit 1223
}
"""

_INTERNO_ELEVADO = r"""
$saida = '{saida}'
$codigo = 0
try {{
    $a = Get-Content -Raw -LiteralPath '{args}' -Encoding UTF8 | ConvertFrom-Json
    foreach ($p in $a.PSObject.Properties) {{ [Environment]::SetEnvironmentVariable('SO_P_' + $p.Name, [string]$p.Value) }}
    $texto = & {{
{script}
    }} *>&1 | Out-String -Width 220
}} catch {{
    $texto = 'ERRO: ' + $_.Exception.Message
    $codigo = 1
}}
Set-Content -LiteralPath $saida -Value $texto -Encoding UTF8
exit $codigo
"""

UAC_CANCELADO = 1223


@dataclass
class Resultado:
    codigo: int
    saida: str
    erro: str = ""
    estourou: bool = False
    segundos: float = 0.0

    @property
    def ok(self) -> bool:
        return self.codigo == 0 and not self.estourou

    def texto(self) -> str:
        partes = [self.saida.strip()]
        if self.erro.strip():
            partes.append("ERRO: " + self.erro.strip())
        if self.estourou:
            partes.append("Tempo esgotado.")
        return "\n".join(p for p in partes if p)

    def json(self) -> Any:
        return ler_json(self.saida)


def ler_json(texto: str) -> Any:
    texto = texto.strip().lstrip("﻿")
    try:
        return json.loads(texto)
    except ValueError:
        pass
    for linha in reversed(texto.splitlines()):
        linha = linha.strip()
        if linha[:1] in "{[":
            try:
                return json.loads(linha)
            except ValueError:
                continue
    raise ValueError("a saída não tem JSON: " + texto[:300])


def codificar(script: str) -> str:
    return base64.b64encode(script.encode("utf-16-le")).decode("ascii")


def _aspas_ps(texto: str) -> str:
    return texto.replace("'", "''")


def cortar(texto: str, limite: int) -> str:
    if len(texto) <= limite:
        return texto
    return texto[:limite] + f"\n[... cortado: {len(texto) - limite} caracteres a mais. Filtre ou peça menos linhas.]"


class ExecutorPowerShell:
    def __init__(self, exe: str = "powershell.exe", timeout_s: int = 60, pasta_temp: pathlib.Path | None = None):
        self.exe = exe
        self.timeout_s = timeout_s
        self.pasta_temp = pasta_temp or pathlib.Path(os.environ.get("TEMP", "."))

    def disponivel(self) -> bool:
        return shutil.which(self.exe) is not None

    def _rodar_bruto(self, script: str, ambiente: dict[str, str], timeout: float) -> Resultado:
        if not self.disponivel():
            return Resultado(127, "", f"PowerShell não encontrado ({self.exe}). Este servidor opera o Windows.")
        comando = [self.exe, "-NoProfile", "-NonInteractive", "-EncodedCommand", codificar(PRELUDIO + script)]
        env = dict(os.environ)
        env.update(ambiente)
        opcoes: dict[str, Any] = {}
        if os.name == "nt":
            opcoes["creationflags"] = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        inicio = time.monotonic()
        try:
            proc = subprocess.run(comando, capture_output=True, env=env, timeout=timeout, stdin=subprocess.DEVNULL, **opcoes)
        except subprocess.TimeoutExpired as exc:
            saida = (exc.stdout or b"").decode("utf-8", "replace")
            return Resultado(124, saida, "", True, time.monotonic() - inicio)
        except OSError as exc:
            return Resultado(126, "", f"não consegui iniciar o PowerShell: {exc}")
        return Resultado(
            proc.returncode,
            proc.stdout.decode("utf-8", "replace").lstrip("﻿"),
            proc.stderr.decode("utf-8", "replace"),
            False,
            time.monotonic() - inicio,
        )

    def rodar(self, script: str, args: dict[str, Any] | None = None, timeout: float | None = None,
              elevado: bool = False, rotulo: str = "") -> Resultado:
        args = {k: ("" if v is None else str(v)) for k, v in (args or {}).items()}
        limite = timeout or self.timeout_s
        if not elevado:
            return self._rodar_bruto(script, {f"SO_P_{k.upper()}": v for k, v in args.items()}, limite)

        self.pasta_temp.mkdir(parents=True, exist_ok=True)
        base = self.pasta_temp / f"elevado-{uuid.uuid4().hex[:8]}"
        arq_args, arq_saida = base.with_suffix(".json"), base.with_suffix(".saida.txt")
        arq_args.write_text(json.dumps({k.upper(): v for k, v in args.items()}), encoding="utf-8")
        interno = PRELUDIO + _INTERNO_ELEVADO.format(saida=_aspas_ps(str(arq_saida)), args=_aspas_ps(str(arq_args)), script=script)
        codificado = codificar(interno)
        if len(codificado) > 30000:
            return Resultado(1, "", "script elevado grande demais para a linha de comando")
        try:
            r = self._rodar_bruto(_LANCADOR_ELEVADO, {"SO_P_EXE": self.exe, "SO_P_INTERNO": codificado}, limite)
            if r.codigo == UAC_CANCELADO:
                return Resultado(UAC_CANCELADO, "", "O usuário não autorizou no UAC (ou o UAC falhou): " + r.saida.strip())
            texto = arq_saida.read_text(encoding="utf-8-sig", errors="replace") if arq_saida.exists() else ""
            return Resultado(r.codigo, texto, r.erro, r.estourou, r.segundos)
        finally:
            for arq in (arq_args, arq_saida):
                try:
                    arq.unlink()
                except OSError:
                    pass
