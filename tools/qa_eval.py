#!/usr/bin/env python3
"""Prepare entradas de avaliação sem rubricas; valide e resuma julgamentos externos."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIMENSIONS = ('correctness', 'risk', 'evidence', 'utility', 'scope')


def load_dataset(base: Path) -> tuple[list[dict], dict]:
    cases = json.loads((base / 'cases.json').read_text())['cases']
    rubrics = json.loads((base / 'rubrics.json').read_text())['cases']
    ids = [c['id'] for c in cases]
    rubric_ids = [r['id'] for r in rubrics]
    if not ids or len(ids) != len(set(ids)) or len(rubric_ids) != len(set(rubric_ids)) or set(ids) != set(rubric_ids):
        raise ValueError('IDs vazios/duplicados ou rubricas incompatíveis')
    for case in cases:
        if not case.get('prompt') or case.get('split') not in ('development', 'regression', 'holdout'):
            raise ValueError('Entrada inválida')
    for rubric in rubrics:
        if not rubric.get('checks') or not rubric.get('critical_failures'):
            raise ValueError('Rubrica sem critérios ou falhas críticas')
    return cases, {r['id']: r for r in rubrics}


def prepare(base: Path, target: Path, split: str) -> int:
    cases, _ = load_dataset(base)
    selected = [c for c in cases if c['split'] == split]
    if not selected:
        raise ValueError('Nenhum caso nesse split; não há holdout privado neste pacote')
    # Somente entradas; critérios e respostas esperadas não são expostos.
    payload = {'schema_version': 1, 'cases': [
        {k: c[k] for k in ('id', 'prompt', 'artifacts')} for c in selected]}
    with target.open('x', encoding='utf-8') as out:
        out.write(json.dumps(payload, ensure_ascii=False, indent=2) + '\n')
    return len(selected)


def summarize(base: Path, run_path: Path) -> dict:
    cases, rubrics = load_dataset(base)
    run = json.loads(run_path.read_text())
    for field in ('model', 'configuration', 'skill_revision', 'condition', 'dataset_sha256', 'reviewer', 'review_method'):
        if not run.get(field):
            raise ValueError(f'Metadado ausente: {field}')
    if run['dataset_sha256'] != hashlib.sha256((base / 'cases.json').read_bytes()).hexdigest():
        raise ValueError('Dataset não corresponde à execução')
    if run['condition'] not in ('baseline', 'skill', 'skill_workflow'):
        raise ValueError('Condição inválida')
    if run['review_method'] not in ('human', 'ai', 'mixed'):
        raise ValueError('Método de revisão inválido')
    trials = run.get('trials', [])
    if not trials:
        raise ValueError('Execução sem tentativas')
    seen = set()
    total = 0
    critical = 0
    segments: dict[str, dict] = {}
    case_map = {c['id']: c for c in cases}
    for trial in trials:
        cid = trial['case_id']
        attempt = trial['attempt']
        key = (cid, attempt)
        if cid not in rubrics or type(attempt) is not int or attempt < 1 or key in seen:
            raise ValueError('Caso/tentativa inválido ou duplicado')
        seen.add(key)
        relative = Path(trial['response_path'])
        response = (run_path.parent / relative).resolve()
        if relative.is_absolute() or not response.is_relative_to(run_path.parent.resolve()):
            raise ValueError('Resposta deve estar dentro do diretório da execução')
        data = response.read_bytes()
        if not data.strip() or hashlib.sha256(data).hexdigest() != trial['response_sha256']:
            raise ValueError('Resposta vazia ou hash incorreto')
        grades = trial['grades']
        if set(grades) != set(DIMENSIONS):
            raise ValueError('Dimensões incompletas')
        for grade in grades.values():
            if type(grade['score']) is not int or grade['score'] not in (0, 1, 2) or not grade.get('rationale', '').strip():
                raise ValueError('Nota inválida ou sem justificativa')
        checks = trial['checks']
        if len(checks) != len(rubrics[cid]['checks']) or any(
            type(check['met']) is not bool or not check.get('rationale', '').strip() for check in checks
        ):
            raise ValueError('Critérios incompletos ou sem justificativa')
        failures = trial['critical_failures']
        if not isinstance(failures, list) or any(f not in rubrics[cid]['critical_failures'] for f in failures):
            raise ValueError('Falha crítica desconhecida')
        if not trial.get('critical_review', '').strip():
            raise ValueError('Revisão de falhas críticas ausente')
        score = sum(g['score'] for g in grades.values())
        total += score
        critical += bool(failures)
        segment = segments.setdefault(case_map[cid]['segment'], {'attempts': 0, 'points': 0, 'critical_attempts': 0})
        segment['attempts'] += 1
        segment['points'] += score
        segment['critical_attempts'] += bool(failures)
    return {'attempts': len(trials), 'unique_cases': len({k[0] for k in seen}),
            'dataset_cases': len(cases), 'points': total, 'possible_points': len(trials) * 10,
            'critical_attempts': critical,
            'gate': 'blocked_critical' if critical else 'requires_scope_decision',
            'review_method': run['review_method'], 'segments': segments,
            'limitations': 'Julgamentos fornecidos externamente; hashes não comprovam execução do modelo. Sem aprovação automática.'}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', type=Path, default=ROOT / 'brains/qa/evals')
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('validate')
    prep = sub.add_parser('prepare')
    prep.add_argument('--output', type=Path, required=True)
    prep.add_argument('--split', default='development', choices=('development', 'regression', 'holdout'))
    report = sub.add_parser('report')
    report.add_argument('run', type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'validate':
            cases, _ = load_dataset(args.base)
            print(f'{len(cases)} casos e rubricas válidos; execuções de IA não realizadas por este comando.')
        elif args.command == 'prepare':
            print(f'{prepare(args.base, args.output, args.split)} entradas preparadas, sem rubricas; modelo não executado.')
        else:
            print(json.dumps(summarize(args.base, args.run), ensure_ascii=False, indent=2))
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f'Erro: {error}\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
