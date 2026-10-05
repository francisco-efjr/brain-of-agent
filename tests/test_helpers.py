"""Regressões com oráculos independentes; apenas processos/arquivos locais temporários.

python3 -m unittest discover -s tests -p 'test_helpers*.py' -v
"""
from __future__ import annotations

import ast
import contextlib
import importlib.util
import io
import itertools
import random
import re
import subprocess
import sys
import tempfile
import types
import unittest
from datetime import date
from decimal import Decimal
from pathlib import Path
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parents[1]


def carregar(nome):
    spec = importlib.util.spec_from_file_location(nome, ROOT / 'scripts' / f'{nome}.py')
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


limites = carregar('valores_limite')
documentos = carregar('documentos_br')
pairwise = carregar('pairwise')
repetir = carregar('repetir_teste')
axe = carregar('auditoria_axe')


class LimitesTests(unittest.TestCase):
    def test_numeric_singleton_never_accepts_outside_range(self):
        rows = limites.casos_numero(Decimal(1), Decimal(1), Decimal(1))
        by_value = {v: expected for v, _, expected in rows}
        self.assertEqual(by_value['0'], 'recusa')
        self.assertEqual(by_value['1'], 'aceita')
        self.assertEqual(by_value['2'], 'recusa')

    def test_numeric_boundary_invariants_for_narrow_ranges(self):
        for step in map(Decimal, ('1', '0.1', '0.01', '2.5')):
            for low in range(-3, 4):
                for width in range(4):
                    minimum, maximum = low * step, (low + width) * step
                    rows = limites.casos_numero(minimum, maximum, step)
                    for value, category, expected in rows:
                        if category.startswith('válida:'):
                            self.assertTrue(minimum <= Decimal(value) <= maximum, (rows, value))
                        if category.startswith('inválida:') and expected == 'recusa' and re.fullmatch(r'-?\d+(?:\.\d+)?', value):
                            self.assertFalse(minimum <= Decimal(value) <= maximum, (rows, value))

    def test_nonfinite_numbers_are_rejected(self):
        for value in ('NaN', 'sNaN', 'Infinity', '-Infinity'):
            for position in range(3):
                args = [Decimal(0), Decimal(10), Decimal(1)]
                args[position] = Decimal(value)
                with self.subTest(value=value, position=position), self.assertRaises(ValueError):
                    limites.casos_numero(*args)

    def test_decimal_default_precision_does_not_round_large_limits(self):
        number = Decimal('123456789012345678901234567890.12')
        rows = limites.casos_numero(number, number, Decimal('0.01'))
        values = {v: e for v, _, e in rows}
        self.assertEqual(values['123456789012345678901234567890.11'], 'recusa')
        self.assertEqual(values['123456789012345678901234567890.12'], 'aceita')
        self.assertEqual(values['123456789012345678901234567890.13'], 'recusa')

    def test_text_singletons_and_small_ranges(self):
        for minimum in range(6):
            for maximum in range(minimum, minimum + 4):
                rows = limites.casos_texto(minimum, maximum, True)
                lengths = {}
                for value, category, expected in rows:
                    if value.startswith("'' (vazio)"):
                        lengths[0] = expected
                    elif re.fullmatch(r"'a*'", value) and 'caractere(s)' in category:
                        lengths[len(ast.literal_eval(value))] = expected
                for length, expected in lengths.items():
                    self.assertEqual(expected.startswith('aceita'), minimum <= length <= maximum,
                                     (minimum, maximum, length, expected))
                self.assertTrue(lengths[maximum].startswith('aceita'))
                self.assertTrue(lengths[maximum + 1].startswith('recusa'))

    def test_date_representation_extremes_and_singletons(self):
        for value in (date.min, date.max, date(2000, 2, 29), date(1900, 2, 28)):
            rows = limites.casos_data(value, value)
            accepted = [v.split()[0] for v, _, expected in rows if expected.startswith('aceita')]
            self.assertEqual(accepted, [value.isoformat()])
        self.assertIn('0000-12-31', [r[0] for r in limites.casos_data(date.min, date.min)])
        self.assertIn('10000-01-01', [r[0] for r in limites.casos_data(date.max, date.max)])

    def test_unstated_format_and_domain_rules_remain_questions(self):
        rows = limites.casos_numero(Decimal(0), Decimal(1000), Decimal(1))
        self.assertTrue(next(e for v, _, e in rows if v == '1e3').startswith('definir'))
        for _, category, expected in limites.casos_texto(0, 50, False):
            if category.startswith('hostil:'):
                self.assertTrue(expected.startswith('definir'))


class DocumentosTests(unittest.TestCase):
    def test_official_cnpj_vector(self):
        # Receita/SERPRO: manual-dv-cnpj.pdf, worked ASCII-48 example.
        self.assertEqual(documentos.dv_cnpj('12ABC34501DE'), '35')
        self.assertTrue(documentos.validar('12.ABC.345/01DE-35')[1])
        self.assertTrue(documentos.validar('12.abc.345/01de-35')[1])

    def test_dv_rejects_wrong_length_or_nonascii(self):
        for base in ('', '123', '1234567890', '１２３４５６７８９', '12345678A'):
            with self.subTest(base=base), self.assertRaises(ValueError):
                documentos.dv_cpf(base)
        for base in ('', '123', '1234567890123', '12ßC34501DE', '12345678901_'):
            with self.subTest(base=base), self.assertRaises(ValueError):
                documentos.dv_cnpj(base)

    def test_unicode_uppercase_expansion_is_not_a_document(self):
        self.assertFalse(documentos.validar('12ßC34501DE33')[1])
        self.assertFalse(documentos.validar('１２ABC34501DE35')[1])

    def test_generated_documents_and_corrupted_check_digits(self):
        rng = random.Random(712)
        for generator in (documentos.gerar_cpf, documentos.gerar_cnpj, documentos.gerar_cnpj_alfa):
            for _ in range(100):
                value = generator(rng)
                self.assertTrue(documentos.validar(value)[1])
                self.assertTrue(documentos.validar(documentos.mascarar(value))[1])
                for digit in '0123456789':
                    if digit != value[-1]:
                        self.assertFalse(documentos.validar(value[:-1] + digit)[1])

    def test_empty_stdin_is_not_successful_validation(self):
        with patch('sys.stdin', io.StringIO('\n \n')), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(documentos.main(['validar', '-']), 2)


class PairwiseTests(unittest.TestCase):
    def test_random_models_against_independent_exhaustive_oracle(self):
        rng = random.Random(8304)
        for scenario in range(60):
            parameters = [(f'p{i}', [str(v) for v in range(rng.randint(1, 3))])
                          for i in range(rng.randint(1, 5))]
            exclusions = []
            for _ in range(rng.randint(0, 6)):
                indices = rng.sample(range(len(parameters)), rng.randint(1, len(parameters)))
                exclusions.append({i: rng.choice(parameters[i][1]) for i in indices})
            valid = [row for row in itertools.product(*(v for _, v in parameters))
                     if not any(all(row[i] == value for i, value in exclusion.items())
                                for exclusion in exclusions)]
            rows, impossible = pairwise.gerar(parameters, exclusions, candidatos=8)
            self.assertTrue(all(tuple(row) in valid for row in rows), scenario)
            possible = {(i, row[i], j, row[j]) for row in valid
                        for i in range(len(parameters)) for j in range(i + 1, len(parameters))}
            actual = {(i, row[i], j, row[j]) for row in rows
                      for i in range(len(parameters)) for j in range(i + 1, len(parameters))}
            all_pairs = {(i, v, j, w) for i in range(len(parameters))
                         for j in range(i + 1, len(parameters))
                         for v in parameters[i][1] for w in parameters[j][1]}
            self.assertEqual(actual, possible, scenario)
            self.assertEqual(set(impossible), all_pairs - possible, scenario)
            if len(parameters) == 1:
                self.assertEqual({tuple(row) for row in rows}, set(valid))

    def test_seed_reproducibility(self):
        params = [(str(i), ['a', 'b', 'c']) for i in range(5)]
        self.assertEqual(pairwise.gerar(params, [], semente=3), pairwise.gerar(params, [], semente=3))

    def test_malformed_input_rejected_instead_of_silent_coercion(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'params.json'
            for content in ('{"a":["x"],"a":["y"]}', '{" ":["x"]}', '{"a":[null]}', '{"a":[{}]}'):
                path.write_text(content)
                with self.subTest(content=content), self.assertRaises(pairwise.ErroEntrada):
                    pairwise.ler_parametros([], str(path))
        with self.assertRaises(pairwise.ErroEntrada):
            pairwise.ler_parametros(['a=x,,y'], None)

    def test_explicit_empty_string_json_value_supported(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'params.json'
            path.write_text('{"a":["", "x"]}')
            self.assertEqual(pairwise.ler_parametros([], str(path)), [('a', ['', 'x'])])

    def test_generator_rejects_empty_domain_or_no_candidates(self):
        for parameters in ([], [('a', [])]):
            with self.assertRaises(pairwise.ErroEntrada):
                pairwise.gerar(parameters, [])
        with self.assertRaises(pairwise.ErroEntrada):
            pairwise.gerar([('a', ['x']), ('b', ['y'])], [], candidatos=0)

    def test_unsatisfiable_cli_is_nonzero(self):
        with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(pairwise.main(['a=x', '--excluir', 'a=x']), 2)

    def test_summary_counts_actual_pairs(self):
        params = [('a', ['x', 'y']), ('b', ['1', '2'])]
        self.assertIn('pares cobertos: 1 de 4', pairwise.resumo(params, [['x', '1']], [], 4))

    def test_markdown_escapes_line_breaks(self):
        self.assertNotIn('\n', pairwise.escapar_md('a\nb|c'))


class RepetirTests(unittest.TestCase):
    def test_observational_diagnostics_do_not_claim_causality(self):
        failure = {'idx': 1, 'falhou': True, 'timeout': False, 'duracao': 1}
        diagnosis = ' '.join(repetir.diagnostico([failure], 1, {}, 1))
        self.assertIn('amostra não exclui intermitência', diagnosis)
        comparison = repetir.comparativo([dict(failure, falhou=False)], [failure], 4)
        self.assertIn('saturação', comparison)
        self.assertIn('deriva do ambiente', comparison)

    def test_zero_failures_bound_states_assumptions(self):
        diagnosis = ' '.join(repetir.diagnostico([{'falhou': False}], 1, {}, 1))
        self.assertIn('95.00%', diagnosis)
        self.assertIn('independentes', diagnosis)
        self.assertIn('probabilidade de falha constante', diagnosis)
        self.assertIn('Nenhuma execução', repetir.diagnostico([], 1, {}, 0)[0])

    def test_local_command_repetitions_and_failure_logs(self):
        command = [sys.executable, '-c', "import os,sys; print(os.environ['REPETICAO']); sys.exit(int(os.environ['REPETICAO']) % 2)"]
        with contextlib.redirect_stderr(io.StringIO()):
            results = repetir.rodar_lote(command, 4, 2, 5, False)
        self.assertEqual([r['idx'] for r in results if r['falhou']], [1, 3])
        self.assertEqual([r['stdout'].strip() for r in results], ['1', '2', '3', '4'])
        with tempfile.TemporaryDirectory() as folder:
            repetir.salvar_falhas(results, folder)
            self.assertEqual(len(list(Path(folder).glob('*.txt'))), 4)
            self.assertEqual((Path(folder) / 'exec-001.stdout.txt').read_text().strip(), '1')

    def test_timeout_and_stop_on_first_failure(self):
        with contextlib.redirect_stderr(io.StringIO()):
            timeout = repetir.rodar_lote([sys.executable, '-c', 'import time; time.sleep(20)'], 1, 1, 0.15, False)
            stopped = repetir.rodar_lote([sys.executable, '-c', 'raise SystemExit(1)'], 5, 1, 5, True)
        self.assertTrue(timeout[0]['timeout'])
        self.assertLess(timeout[0]['duracao'], 5)
        self.assertEqual(len(stopped), 1)

    def test_invalid_timeout_rejected_before_execution(self):
        for timeout in (-1, 0, float('nan'), float('inf')):
            with self.assertRaises(ValueError):
                repetir.rodar_lote(['nonexistent-command'], 1, 1, timeout, False)

    def test_launch_error_cli_returns_usage_error_without_traceback(self):
        with tempfile.TemporaryDirectory() as folder:
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/repetir_teste.py'), '-n', '1', '--', folder],
                                    capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn('Traceback', result.stderr)


class AxeTests(unittest.TestCase):
    def fixture(self, violations=None, incomplete=None, status=200, page_url='https://example.test/'):
        page = MagicMock()
        page.url = page_url
        page.goto.return_value.status = status
        page.evaluate.side_effect = [None, {'violations': violations or [], 'incomplete': incomplete or []}]
        browser = MagicMock()
        browser.new_context.return_value.new_page.return_value = page
        playwright = MagicMock()
        playwright.chromium.launch.return_value = browser
        context = MagicMock()
        context.__enter__.return_value = playwright
        module = types.ModuleType('playwright.sync_api')
        module.sync_playwright = lambda: context
        return page, browser, {'playwright': types.ModuleType('playwright'), 'playwright.sync_api': module}

    def run_fake(self, argv, **kwargs):
        page, browser, modules = self.fixture(**kwargs)
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch.dict(sys.modules, modules), patch.object(axe, 'obter_axe', return_value='axe-source'), \
                contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = axe.main(argv)
        return code, stdout.getvalue(), stderr.getvalue(), page, browser

    def test_incomplete_is_reported_without_claiming_conformance(self):
        item = {'id': 'contrast', 'help': 'review contrast', 'nodes': [{'target': [['frame', 'button']]}], 'helpUrl': 'https://example.test/rule'}
        code, output, _, page, browser = self.run_fake(['https://example.test'], incomplete=[item])
        self.assertEqual(code, 0)
        self.assertIn('revisão manual pendente: 1', output)
        self.assertIn('não comprova conformidade', output)
        self.assertIn("'incomplete'", page.evaluate.call_args_list[-1].args[0])
        browser.close.assert_called_once()

    def test_violation_nonzero(self):
        item = {'id': 'button-name', 'help': 'button needs name', 'nodes': [], 'helpUrl': 'https://example.test/rule'}
        self.assertEqual(self.run_fake(['https://example.test'], violations=[item])[0], 1)

    def test_http_error_or_cross_host_redirect_is_not_a_pass(self):
        for kwargs in ({'status': 404}, {'page_url': 'https://login.example.test/'}):
            code, _, stderr, page, browser = self.run_fake(['https://example.test'], **kwargs)
            self.assertEqual(code, 2)
            self.assertIn('auditoria não concluída', stderr)
            page.evaluate.assert_not_called()
            browser.close.assert_called_once()

    def test_documented_route_file_option_and_readiness_selector(self):
        with tempfile.TemporaryDirectory() as folder:
            routes = Path(folder) / 'rotas.txt'
            routes.write_text('# Routes\n/login\n\n', encoding='utf-8')
            code, _, _, page, _ = self.run_fake(['https://example.test', '--todas-as-rotas', str(routes), '--esperar-seletor', 'h1'])
        self.assertEqual(code, 0)
        page.goto.assert_called_once_with('https://example.test/login', wait_until='domcontentloaded')
        page.locator.assert_called_with('h1')

    def test_empty_routes_file_rejected_before_browser_import(self):
        with tempfile.TemporaryDirectory() as folder:
            routes = Path(folder) / 'routes.txt'
            routes.write_text('# no route\n')
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(axe.main(['https://example.test', '--todas-as-rotas', str(routes)]), 2)

    def test_legacy_analysis_api_still_returns_only_violations(self):
        page, _, _ = self.fixture(violations=[{'id': 'x'}])
        self.assertEqual(axe.analisar(page, 'source'), [{'id': 'x'}])

    def test_invalid_or_external_route_rejected(self):
        for base, route in [('file:///tmp/test', '/'), ('https://example.test', '//evil.test'),
                            ('https://example.test', 'https://evil.test'), ('https://example.test?x=1', '/')]:
            with self.subTest(base=base, route=route), self.assertRaises(ValueError):
                axe.montar_url(base, route)

    def test_existing_cache_never_uses_network(self):
        with tempfile.TemporaryDirectory() as folder:
            cached = Path(folder) / 'axe.min.js'
            cached.write_text('cached engine')
            with patch.object(axe, 'AXE_LOCAL', cached), patch.object(axe.urllib.request, 'urlopen') as request:
                self.assertEqual(axe.obter_axe(), 'cached engine')
                request.assert_not_called()


if __name__ == '__main__':
    unittest.main()
