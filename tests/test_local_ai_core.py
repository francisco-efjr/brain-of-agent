"""Confere que o CORE.md da IA local está montado a partir da base e dos temas."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import pathlib
import unittest

RAIZ = pathlib.Path(__file__).resolve().parents[1] / "local-ai-core"


def carregar_montador():
    spec = importlib.util.spec_from_file_location("montar_core", RAIZ / "montar_core.py")
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


class LocalAiCoreTest(unittest.TestCase):
    def setUp(self):
        self.montador = carregar_montador()

    def test_fontes_dos_temas_existem(self):
        self.assertTrue(self.montador.BASE.is_file())
        for tema, caminho in self.montador.TEMAS.items():
            with self.subTest(tema=tema):
                self.assertTrue(caminho.is_file(), caminho)

    def test_core_md_em_dia(self):
        saida = io.StringIO()
        with contextlib.redirect_stdout(saida), contextlib.redirect_stderr(saida):
            codigo = self.montador.main(["--check"])
        self.assertEqual(codigo, 0, "CORE.md desatualizado: rode python local-ai-core/montar_core.py")

    def test_core_md_traz_base_e_temas(self):
        texto = (RAIZ / "CORE.md").read_text(encoding="utf-8")
        for marcador in ("<esteira>", "<invariantes>", "<windows-execucao>", "<pesquisa-metodo>"):
            with self.subTest(marcador=marcador):
                self.assertIn(marcador, texto)


if __name__ == "__main__":
    unittest.main()
