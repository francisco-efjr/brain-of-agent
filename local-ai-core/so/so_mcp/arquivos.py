"""Leitura de pastas e arquivos (R0), em Python puro: funciona igual em qualquer sistema."""
from __future__ import annotations

import datetime as dt
import fnmatch
import pathlib

from . import politica
from .config import caminho as expandir_caminho
from .executor import cortar

LIMITE_LEITURA = 2 * 1024 * 1024


def _tamanho(n: int) -> str:
    for unidade in ("B", "KB", "MB", "GB"):
        if n < 1024 or unidade == "GB":
            return f"{n:.0f} {unidade}" if unidade == "B" else f"{n:.1f} {unidade}"
        n /= 1024
    return str(n)


def _caminho(texto: str) -> pathlib.Path | None:
    cam = expandir_caminho(texto or "")
    return cam if cam.is_absolute() else None


def listar(pasta: str, filtro: str | None = None, limite: int | None = None) -> tuple[str, bool]:
    cam = _caminho(pasta)
    if cam is None:
        return "Use um caminho completo, como C:\\Users\\voce\\Documents (veja so_estado area=usuario).", True
    if not cam.is_dir():
        return f"A pasta não existe: {cam}", True
    limite = max(1, min(int(limite or 50), 200))
    padrao = (filtro or "*").lower()
    try:
        entradas = [e for e in cam.iterdir() if fnmatch.fnmatch(e.name.lower(), padrao)]
    except PermissionError:
        return f"Sem permissão para listar {cam}.", True
    entradas.sort(key=lambda e: (not e.is_dir(), e.name.lower()))
    linhas = [f"{cam} — {len(entradas)} item(ns){' com o filtro ' + filtro if filtro else ''}:"]
    for e in entradas[:limite]:
        try:
            if e.is_dir():
                linhas.append(f"[pasta] {e.name}")
            else:
                info = e.stat()
                quando = dt.datetime.fromtimestamp(info.st_mtime).strftime("%Y-%m-%d %H:%M")
                linhas.append(f"{e.name}  {_tamanho(info.st_size)}  {quando}")
        except OSError:
            linhas.append(f"{e.name}  (sem acesso)")
    if len(entradas) > limite:
        linhas.append(f"... e mais {len(entradas) - limite}. Use filtro (ex.: *.pdf) ou aumente o limite.")
    return "\n".join(linhas), False


def ler(arquivo: str, inicio: int | None = None, linhas: int | None = None, limite_saida: int = 6000) -> tuple[str, bool]:
    cam = _caminho(arquivo)
    if cam is None:
        return "Use um caminho completo do arquivo.", True
    if not cam.is_file():
        return f"O arquivo não existe: {cam}", True
    if politica.arquivo_de_segredo(cam):
        return (f"BLOQUEADO: {cam.name} guarda senhas, chaves ou cookies. Segredos ficam onde estão; "
                "se o usuário precisar, ele abre o arquivo."), True
    with cam.open("rb") as f:
        bruto = f.read(LIMITE_LEITURA + 1)
    if b"\x00" in bruto[:8192]:
        return f"{cam.name} é binário. Para abrir no app padrão, use so_planejar com arquivo_abrir.", True
    cortado = len(bruto) > LIMITE_LEITURA
    for codificacao in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            texto = bruto[:LIMITE_LEITURA].decode(codificacao)
            break
        except UnicodeDecodeError:
            continue
    todas = texto.splitlines()
    inicio = max(1, int(inicio or 1))
    quantas = max(1, min(int(linhas or 200), 1000))
    trecho = todas[inicio - 1: inicio - 1 + quantas]
    fim = inicio + len(trecho) - 1
    cabecalho = f"{cam} — linhas {inicio} a {fim} de {len(todas)}{' (arquivo grande: só os primeiros 2 MB)' if cortado else ''}"
    corpo = "\n".join(f"{inicio + i:>5}  {linha}" for i, linha in enumerate(trecho))
    rodape = f"\n[Continua: peça inicio={fim + 1}.]" if fim < len(todas) else ""
    return cortar(cabecalho + "\n" + politica.mascarar_segredos(corpo) + rodape, limite_saida), False
