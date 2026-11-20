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

    def test_fontes_dos_temas_existem_e_tem_cartao(self):
        self.assertTrue(self.montador.BASE.is_file())
        for tema, caminho in self.montador.TEMAS.items():
            with self.subTest(tema=tema):
                self.assertTrue(caminho.is_file(), caminho)
                texto = caminho.read_text(encoding="utf-8")
                self.assertIn(self.montador.INICIO, texto)
                self.assertIn(self.montador.FIM, texto)

    def test_perfis_cobrem_temas_validos(self):
        for perfil, escolha in self.montador.PERFIS.items():
            with self.subTest(perfil=perfil):
                self.assertTrue(set(escolha) <= set(self.montador.TEMAS))
                self.assertTrue(set(escolha.values()) <= set(self.montador.MODOS))

    def test_core_md_em_dia(self):
        saida = io.StringIO()
        with contextlib.redirect_stdout(saida), contextlib.redirect_stderr(saida):
            codigo = self.montador.main(["--check"])
        self.assertEqual(codigo, 0, "CORE.md desatualizado: rode python local-ai-core/montar_core.py")

    def test_core_md_segue_o_perfil_padrao(self):
        texto = (RAIZ / "CORE.md").read_text(encoding="utf-8")
        self.assertNotIn(self.montador.INICIO, texto)
        for tema, modo in self.montador.PERFIS["padrao"].items():
            _, cartao, completo = self.montador.partes_do_tema(
                self.montador.TEMAS[tema].read_text(encoding="utf-8"), tema
            )
            with self.subTest(tema=tema, modo=modo):
                if modo == "completo":
                    self.assertIn(completo, texto)
                    self.assertNotIn(cartao, texto)
                else:
                    self.assertIn(cartao, texto)
                    self.assertNotIn(completo, texto)


if __name__ == "__main__":
    unittest.main()
