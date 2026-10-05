#!/usr/bin/env python3
"""Catálogo determinístico das skills próprias e do snapshot gstack."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def skill_name(path: Path) -> str:
    text = path.read_text(encoding='utf-8')
    header = re.match(r'^---\n(.*?)\n---(?:\n|$)', text, re.S)
    if not header:
        raise ValueError(f'SKILL.md sem frontmatter: {path}')
    name = re.search(r'^name:\s*([^\n]+)', header.group(1), re.M)
    if not name:
        raise ValueError(f'SKILL.md sem name: {path}')
    return name.group(1).strip().strip('\"\'')


def build_catalog(root: Path) -> dict:
    manifest = json.loads((root / 'registry/gstack-upstream.json').read_text())
    entries = [{'id': 'brain-of-agent', 'name': skill_name(root / 'SKILL.md'),
                'source': 'own', 'path': 'SKILL.md'}]
    for path in sorted((root / 'brains').glob('*/SKILL.md')):
        entries.append({'id': f'brain/{path.parent.name}', 'name': skill_name(path),
                        'source': 'own', 'path': path.relative_to(root).as_posix()})
    vendor = root / 'vendor/gstack'
    # Enumerar o manifest impede que outputs locais virem skills de origem.
    for item in manifest['files']:
        if Path(item['path']).name != 'SKILL.md' or item['path'].startswith('test/'):
            continue
        path = vendor / item['path']
        parent = Path(item['path']).parent.as_posix()
        entries.append({'id': f'gstack/{parent if parent != "." else "router"}',
                        'name': skill_name(path), 'source': 'gstack',
                        'path': path.relative_to(root).as_posix()})
    entries.sort(key=lambda e: e['id'])
    return {'schema_version': 1, 'upstream_revision': manifest['revision'], 'skills': entries}


def serialize(catalog: dict) -> str:
    return json.dumps(catalog, ensure_ascii=False, indent=2) + '\n'


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--list', action='store_true', help='Listar sem gravar')
    parser.add_argument('--check', action='store_true', help='Verificar catálogo sem gravar')
    args = parser.parse_args()
    try:
        catalog = build_catalog(ROOT)
        if args.list:
            for entry in catalog['skills']:
                print(f"{entry['id']:<46} {entry['path']}")
        elif args.check:
            if (ROOT / 'registry/skills.json').read_text() != serialize(catalog):
                raise ValueError('Catálogo desatualizado; execute python3 tools/catalog.py')
            print(f"Catálogo atualizado: {len(catalog['skills'])} skills")
        else:
            (ROOT / 'registry/skills.json').write_text(serialize(catalog), encoding='utf-8')
            print(f"Catálogo gerado: {len(catalog['skills'])} skills")
    except (OSError, ValueError, KeyError) as error:
        parser.exit(1, f'Erro: {error}\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
