"""Registro de auditoria em JSONL: uma linha por chamada de ferramenta, sem segredos."""
from __future__ import annotations

import datetime as dt
import json
import pathlib
import sys
from typing import Any

from .politica import mascarar_segredos


def agora() -> dt.datetime:
    return dt.datetime.now().astimezone()


def _curto(valor: Any, limite: int = 300) -> Any:
    if isinstance(valor, str):
        valor = mascarar_segredos(valor)
        return valor if len(valor) <= limite else valor[:limite] + "…"
    if isinstance(valor, dict):
        return {k: _curto(v, limite) for k, v in valor.items()}
    if isinstance(valor, list):
        return [_curto(v, limite) for v in valor[:20]]
    return valor


class Registro:
    def __init__(self, pasta: pathlib.Path):
        self.pasta = pasta

    def arquivo(self, quando: dt.datetime | None = None) -> pathlib.Path:
        return self.pasta / f"so-{(quando or agora()):%Y-%m}.jsonl"

    def anotar(self, **evento: Any) -> None:
        evento = {"quando": agora().isoformat(timespec="seconds"), **_curto(evento)}
        try:
            self.pasta.mkdir(parents=True, exist_ok=True)
            with self.arquivo().open("a", encoding="utf-8") as f:
                f.write(json.dumps(evento, ensure_ascii=False) + "\n")
        except OSError as exc:
            print(f"[so-mcp] não consegui gravar o registro: {exc}", file=sys.stderr)

    def ultimos(self, limite: int = 20, tipo: str | None = None) -> list[dict]:
        linhas: list[dict] = []
        for arq in sorted(self.pasta.glob("so-*.jsonl"), reverse=True):
            for linha in reversed(arq.read_text(encoding="utf-8", errors="replace").splitlines()):
                try:
                    evento = json.loads(linha)
                except ValueError:
                    continue
                if tipo is None or evento.get("tipo") == tipo:
                    linhas.append(evento)
                    if len(linhas) >= limite:
                        return linhas
        return linhas
