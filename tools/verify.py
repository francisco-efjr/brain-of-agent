#!/usr/bin/env python3
"""Verificar fidelidade do snapshot e estrutura própria, sem executar gstack."""
from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path, PurePosixPath

from catalog import ROOT, build_catalog, serialize, skill_name


def safe_path(raw: str) -> PurePosixPath:
    path = PurePosixPath(raw)
    if not raw or path.is_absolute() or '..' in path.parts or '\\' in raw or str(path) != raw:
        raise ValueError(f'Caminho de origem inválido: {raw!r}')
    return path


def verify_snapshot(root: Path) -> int:
    manifest = json.loads((root / 'registry/gstack-upstream.json').read_text())
    if manifest['repository'] != 'https://github.com/garrytan/gstack' or manifest['directory'] != 'vendor/gstack':
        raise ValueError('Origem/diretório do snapshot inesperados')
    if not re.fullmatch(r'[0-9a-f]{40}', manifest['revision']):
        raise ValueError('Revisão upstream inválida')
    vendor = root / 'vendor/gstack'
    if vendor.is_symlink() or not vendor.is_dir():
        raise ValueError('Snapshot deve ser um diretório real')
    expected = set()
    for item in manifest['files']:
        rel = safe_path(item['path'])
        if item['path'] in expected:
            raise ValueError(f'Entrada duplicada: {rel}')
        expected.add(item['path'])
        path = vendor / rel
        if not path.parent.resolve().is_relative_to(vendor.resolve()):
            raise ValueError(f'Pai fora do snapshot: {rel}')
        if item['mode'] == '120000':
            if not path.is_symlink():
                raise ValueError(f'Symlink ausente: {rel}')
            data = os.readlink(path).encode()
            if not path.resolve().is_relative_to(vendor.resolve()) or not path.exists():
                raise ValueError(f'Symlink inválido: {rel}')
        elif item['mode'] in ('100644', '100755'):
            if path.is_symlink() or not path.is_file():
                raise ValueError(f'Arquivo ausente/tipo alterado: {rel}')
            data = path.read_bytes()
            if os.name == 'posix' and bool(path.stat().st_mode & 0o111) != (item['mode'] == '100755'):
                raise ValueError(f'Executabilidade alterada: {rel}')
        else:
            raise ValueError(f'Modo Git não suportado: {rel}')
        if hashlib.sha256(data).hexdigest() != item['sha256']:
            raise ValueError(f'Conteúdo alterado: {rel}')
    actual = {p.relative_to(vendor).as_posix() for p in vendor.rglob('*') if p.is_file() or p.is_symlink()}
    if actual != expected:
        raise ValueError(f'Inventário divergiu: extras={sorted(actual-expected)[:5]}, ausentes={sorted(expected-actual)[:5]}')
    for name in ('LICENSE', 'NOTICE.md', 'licenses/Apache-2.0.txt', 'setup', 'package.json'):
        if name not in expected:
            raise ValueError(f'Arquivo essencial do fornecedor ausente: {name}')
    return len(expected)


def verify_own(root: Path) -> int:
    catalog = build_catalog(root)
    if (root / 'registry/skills.json').read_text() != serialize(catalog):
        raise ValueError('Catálogo desatualizado; execute python3 tools/catalog.py')
    ids = [entry['id'] for entry in catalog['skills']]
    if len(ids) != len(set(ids)):
        raise ValueError('IDs de skills duplicados')
    own = [root / 'SKILL.md', *sorted((root / 'brains').glob('*/SKILL.md'))]
    for entry in own:
        skill_name(entry)
        text = entry.read_text()
        # Recursos concretos anunciados em código inline e links Markdown.
        paths = re.findall(r'`((?:references|assets/templates|scripts|evals|vendor/gstack)/[^`\s]+\.(?:md|py|json))`', text)
        paths += re.findall(r'\]\(([^\s()]+\.(?:md|py|json))\)', text)
        for raw in paths:
            if '://' not in raw and not raw.startswith('#') and not (entry.parent / raw).is_file():
                raise ValueError(f'Recurso anunciado ausente: {entry.relative_to(root)} → {raw}')
        if entry.parent.name == 'qa':
            table_lines = '\n'.join(line for line in text.splitlines() if line.startswith('|'))
            templates = re.findall(r'`([a-z][a-z-]*\.md)`', table_lines)
            for template in templates:
                if not (entry.parent / 'assets/templates' / template).is_file():
                    raise ValueError(f'Template anunciado ausente: {template}')
    return len(catalog['skills'])


def main() -> int:
    try:
        count = verify_snapshot(ROOT)
        skills = verify_own(ROOT)
        print(f'OK: {count} arquivos upstream íntegros; {skills} skills no catálogo; recursos próprios presentes.')
        print('Escopo: integridade e estrutura. Runtime/testes upstream não executados.')
        return 0
    except (OSError, ValueError, KeyError) as error:
        print(f'ERRO: {error}')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
