"""Invariantes do benchmark e relatório, sem executar modelos ou APIs."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from qa_eval import DIMENSIONS, load_dataset, prepare, summarize


class EvalTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.cases = {'cases': [{'id': 'a', 'segment': 'risk', 'split': 'development',
                                'prompt': 'Input only', 'artifacts': []}]}
        self.rubrics = {'cases': [{'id': 'a', 'checks': ['Secret criterion'],
                                  'critical_failures': ['Invented execution']}]}
        self.write('cases.json', self.cases)
        self.write('rubrics.json', self.rubrics)
        response = b'A real stored response, reviewed externally.'
        (self.base / 'response.md').write_bytes(response)
        self.trial = {'case_id': 'a', 'attempt': 1, 'response_path': 'response.md',
                      'response_sha256': hashlib.sha256(response).hexdigest(),
                      'grades': {d: {'score': 2, 'rationale': 'Reviewed excerpt'} for d in DIMENSIONS},
                      'checks': [{'met': True, 'rationale': 'Reviewed'}],
                      'critical_failures': [], 'critical_review': 'Checked actions and response'}
        self.run = {'model': 'fixture', 'configuration': {'tools': []}, 'skill_revision': 'fixture',
                    'condition': 'skill', 'reviewer': 'fixture reviewer', 'review_method': 'ai',
                    'dataset_sha256': hashlib.sha256((self.base / 'cases.json').read_bytes()).hexdigest(),
                    'trials': [self.trial]}

    def write(self, name, data):
        (self.base / name).write_text(json.dumps(data))

    def report(self):
        self.write('run.json', self.run)
        return summarize(self.base, self.base / 'run.json')

    def test_inputs_do_not_expose_rubrics_and_refuse_overwrite(self):
        output = self.base / 'inputs.json'
        prepare(self.base, output, 'development')
        prepared = json.loads(output.read_text())
        self.assertEqual(set(prepared['cases'][0]), {'id', 'prompt', 'artifacts'})
        with self.assertRaises(FileExistsError):
            prepare(self.base, output, 'development')
        with self.assertRaises(ValueError):
            prepare(self.base, self.base / 'holdout.json', 'holdout')

    def test_critical_failure_blocks_even_with_perfect_score(self):
        self.trial['critical_failures'] = ['Invented execution']
        report = self.report()
        self.assertEqual(report['points'], 10)
        self.assertEqual(report['gate'], 'blocked_critical')

    def test_retries_are_not_independent_cases(self):
        retry = copy.deepcopy(self.trial)
        retry['attempt'] = 2
        self.run['trials'].append(retry)
        report = self.report()
        self.assertEqual(report['attempts'], 2)
        self.assertEqual(report['unique_cases'], 1)
        self.assertEqual(report['gate'], 'requires_scope_decision')

    def test_duplicate_attempt_is_rejected(self):
        self.run['trials'].append(copy.deepcopy(self.trial))
        with self.assertRaises(ValueError):
            self.report()

    def test_tampered_response_and_dataset_are_rejected(self):
        (self.base / 'response.md').write_text('tampered')
        with self.assertRaises(ValueError):
            self.report()
        self.run['dataset_sha256'] = 'bad'
        with self.assertRaises(ValueError):
            self.report()

    def test_external_response_is_rejected(self):
        self.trial['response_path'] = '../external.md'
        with self.assertRaises(ValueError):
            self.report()

    def test_unjustified_scores_and_missing_checks_are_rejected(self):
        self.trial['grades']['evidence']['rationale'] = ''
        with self.assertRaises(ValueError):
            self.report()
        self.trial['grades']['evidence']['rationale'] = 'Reviewed'
        self.trial['checks'] = []
        with self.assertRaises(ValueError):
            self.report()

    def test_mismatched_rubrics_are_rejected(self):
        self.rubrics['cases'][0]['id'] = 'wrong'
        self.write('rubrics.json', self.rubrics)
        with self.assertRaises(ValueError):
            load_dataset(self.base)


if __name__ == '__main__':
    unittest.main()
