"""Configuração do servidor: um JSON simples com padrões seguros."""
from __future__ import annotations

import ipaddress
import json
import os
import pathlib
import re
import urllib.parse
from dataclasses import dataclass, field
from typing import Any

PASTA_SO = pathlib.Path(__file__).resolve().parent.parent
PASTA_CORE = PASTA_SO.parent

PADRAO: dict[str, Any] = {
    "pasta_operador": "%USERPROFILE%\\IA-Operador",
    "powershell": "powershell.exe",
    "timeout_comando_s": 60,
    "timeout_confirmacao_s": 120,
    "plano_validade_min": 30,
    "saida_max_caracteres": 6000,
    "pastas_permitidas": [
        "%USERPROFILE%\\Documents",
        "%USERPROFILE%\\Desktop",
        "%USERPROFILE%\\Downloads",
        "%USERPROFILE%\\IA-Operador",
    ],
    "pastas_sistema_extra": [],
    "pasta_regras": "",
    "memoria": {
        "backend": "local",
        "url": "http://127.0.0.1:49374/mcp",
        "workspace": "",
        "project": "",
        "token_env": "AI_MEMORY_TOKEN",
        "timeout_s": 10,
    },
}

_VAR = re.compile(r"%([A-Za-z0-9_()]+)%")


def expandir(texto: str, ambiente: dict[str, str] | None = None) -> str:
    """Expande %VAR% (estilo Windows) e ~. Sem USERPROFILE (fora do Windows), usa HOME."""
    amb = dict(os.environ if ambiente is None else ambiente)
    if "USERPROFILE" not in amb:
        amb["USERPROFILE"] = amb.get("HOME", str(pathlib.Path.home()))

    def troca(m: re.Match[str]) -> str:
        nome = m.group(1)
        for chave, valor in amb.items():
            if chave.upper() == nome.upper():
                return valor
        return m.group(0)

    texto = _VAR.sub(troca, texto)
    if texto.startswith("~"):
        texto = amb["USERPROFILE"] + texto[1:]
    return texto


def caminho(texto: str, ambiente: dict[str, str] | None = None) -> pathlib.Path:
    bruto = expandir(texto.strip().strip('"'), ambiente)
    if os.name != "nt":
        bruto = bruto.replace("\\", "/")
    return pathlib.Path(bruto)


def url_local(url: str) -> bool:
    """Só aceita endereço de loopback: a memória não pode sair da máquina."""
    try:
        host = urllib.parse.urlparse(url).hostname or ""
    except ValueError:
        return False
    if host == "localhost":
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


@dataclass
class Config:
    pasta_operador: pathlib.Path
    powershell: str
    timeout_comando_s: int
    timeout_confirmacao_s: int
    plano_validade_min: int
    saida_max_caracteres: int
    pastas_permitidas: list[pathlib.Path]
    pastas_sistema: list[pathlib.Path]
    perfil_usuario: pathlib.Path
    pasta_regras: pathlib.Path
    memoria: dict[str, Any] = field(default_factory=dict)

    @property
    def planos(self) -> pathlib.Path:
        return self.pasta_operador / "planos"

    @property
    def logs(self) -> pathlib.Path:
        return self.pasta_operador / "logs"

    @property
    def backups(self) -> pathlib.Path:
        return self.pasta_operador / "backups"

    @property
    def scripts(self) -> pathlib.Path:
        return self.pasta_operador / "scripts"

    @property
    def pasta_memoria(self) -> pathlib.Path:
        return self.pasta_operador / "memoria"

    @property
    def arquivo_parar(self) -> pathlib.Path:
        return self.pasta_operador / "PARAR"

    def preparar_pastas(self) -> None:
        for pasta in (self.planos, self.logs, self.backups, self.scripts, self.pasta_memoria):
            pasta.mkdir(parents=True, exist_ok=True)


def _pastas_sistema(ambiente: dict[str, str], extra: list[str]) -> list[pathlib.Path]:
    nomes = ("SystemRoot", "ProgramFiles", "ProgramFiles(x86)", "ProgramW6432", "ProgramData")
    pastas = []
    for nome in nomes:
        for chave, valor in ambiente.items():
            if chave.upper() == nome.upper() and valor:
                pastas.append(caminho(valor, ambiente))
    pastas += [caminho(p, ambiente) for p in extra]
    return pastas


def carregar(arquivo: pathlib.Path | None = None, ambiente: dict[str, str] | None = None) -> Config:
    amb = dict(os.environ if ambiente is None else ambiente)
    dados: dict[str, Any] = json.loads(json.dumps(PADRAO))
    if arquivo is not None:
        lido = json.loads(arquivo.read_text(encoding="utf-8-sig"))
        if not isinstance(lido, dict):
            raise ValueError("a configuração deve ser um objeto JSON")
        memoria = {**dados["memoria"], **lido.get("memoria", {})}
        dados.update(lido)
        dados["memoria"] = memoria

    if dados["memoria"]["backend"] not in ("local", "ai-memory"):
        raise ValueError("memoria.backend deve ser 'local' ou 'ai-memory'")
    if dados["memoria"]["backend"] == "ai-memory" and not url_local(dados["memoria"]["url"]):
        raise ValueError("memoria.url precisa ser local (127.0.0.1, ::1 ou localhost): nada sai da máquina")

    regras = dados["pasta_regras"]
    return Config(
        pasta_operador=caminho(dados["pasta_operador"], amb),
        powershell=dados["powershell"],
        timeout_comando_s=int(dados["timeout_comando_s"]),
        timeout_confirmacao_s=int(dados["timeout_confirmacao_s"]),
        plano_validade_min=int(dados["plano_validade_min"]),
        saida_max_caracteres=int(dados["saida_max_caracteres"]),
        pastas_permitidas=[caminho(p, amb) for p in dados["pastas_permitidas"]],
        pastas_sistema=_pastas_sistema(amb, list(dados["pastas_sistema_extra"])),
        perfil_usuario=caminho("%USERPROFILE%", amb),
        pasta_regras=caminho(regras, amb) if regras else PASTA_CORE,
        memoria=dados["memoria"],
    )
