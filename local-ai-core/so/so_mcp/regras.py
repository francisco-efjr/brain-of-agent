"""Consulta às regras do core: o modelo busca a seção certa em vez de carregar tudo no prompt."""
from __future__ import annotations

import pathlib
import re
from dataclasses import dataclass

from .executor import cortar
from .memoria import normalizar, termos

_INICIO_SECAO = re.compile(r"^(?:##\s+(?P<titulo>.+?)\s*$|<(?P<tag>[a-z][\w-]*)>\s*$)")


@dataclass
class Secao:
    tema: str
    arquivo: str
    titulo: str
    texto: str


class Regras:
    def __init__(self, pasta: pathlib.Path):
        self.pasta = pasta
        self._cache: tuple[float, list[Secao]] | None = None

    def _arquivos(self) -> list[pathlib.Path]:
        if not self.pasta.is_dir():
            return []
        achados = list(self.pasta.glob("CORE-BASE.md"))
        for padrao in ("*/CORE-*.md", "*/REFERENCIA-*.md"):
            achados += self.pasta.glob(padrao)
        return sorted(achados)

    def temas(self) -> list[str]:
        return sorted({"base" if a.parent == self.pasta else a.parent.name for a in self._arquivos()})

    def _secoes(self) -> list[Secao]:
        arquivos = self._arquivos()
        marca = max((a.stat().st_mtime for a in arquivos), default=0.0)
        if self._cache and self._cache[0] == marca:
            return self._cache[1]
        secoes: list[Secao] = []
        for arq in arquivos:
            tema = "base" if arq.parent == self.pasta else arq.parent.name
            rel = arq.relative_to(self.pasta).as_posix()
            titulo, linhas = arq.stem, []
            for linha in arq.read_text(encoding="utf-8").splitlines():
                m = _INICIO_SECAO.match(linha)
                if m:
                    if "".join(linhas).strip():
                        secoes.append(Secao(tema, rel, titulo, "\n".join(linhas).strip()))
                    titulo, linhas = m.group("titulo") or m.group("tag"), []
                    continue
                linhas.append(linha)
            if "".join(linhas).strip():
                secoes.append(Secao(tema, rel, titulo, "\n".join(linhas).strip()))
        self._cache = (marca, secoes)
        return secoes

    def consultar(self, consulta: str, tema: str | None = None, quantas: int = 2) -> tuple[str, bool]:
        alvo = termos(consulta)
        if not alvo:
            return "Consulta vazia: use palavras do assunto, como 'instalar programa winget' ou 'backup antes de mudar'.", True
        secoes = [s for s in self._secoes() if not tema or s.tema == tema]
        if not secoes:
            return f"Nenhuma regra encontrada{' no tema ' + tema if tema else ''}. Temas: {', '.join(self.temas())}", True
        notas = []
        for s in secoes:
            titulo, texto = normalizar(s.titulo), normalizar(s.texto)
            pontos = sum(4 * titulo.count(t) + min(texto.count(t), 5) for t in alvo)
            if pontos:
                notas.append((pontos, len(s.texto), s))
        if not notas:
            return f"Nenhuma seção fala de '{consulta}'. Tente outras palavras ou outro tema ({', '.join(self.temas())}).", False
        notas.sort(key=lambda x: (-x[0], x[1]))
        partes = [f"Fonte: {s.arquivo} › {s.titulo}\n{cortar(s.texto, 1800)}" for _, _, s in notas[:quantas]]
        return "\n\n".join(partes) + "\n\nIsto é regra do seu core: siga.", False
