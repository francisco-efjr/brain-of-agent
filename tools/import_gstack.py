#!/usr/bin/env python3
"""Importar arquivos versionados do gstack de um clone limpo e revisão explícita."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import tempfile
from datetime import date
from pathlib import Path

from catalog import ROOT
from verify import safe_path, verify_snapshot


def git(source: Path, *args: str) -> bytes:
    return subprocess.check_output(['git', '-C', str(source), *args], timeout=30)


def import_snapshot(root: Path, source: Path, revision: str, imported_on: str) -> int:
    source = source.resolve()
    target = root / 'vendor/gstack'
    if target.is_symlink() or source.is_relative_to(root.resolve()) or root.resolve().is_relative_to(source):
        raise ValueError('Use um clone independente fora do checkout')
    if not re.fullmatch(r'[0-9a-f]{40}', revision):
        raise ValueError('Informe um SHA completo de 40 caracteres minúsculos')
    if git(source, 'rev-parse', 'HEAD').decode().strip() != revision:
        raise ValueError('HEAD do clone não corresponde à revisão solicitada')
    origin = git(source, 'remote', 'get-url', 'origin').decode().strip().removesuffix('.git')
    if origin not in ('https://github.com/garrytan/gstack', 'git@github.com:garrytan/gstack'):
        raise ValueError('Origin não corresponde ao fornecedor oficial')
    if git(source, 'status', '--porcelain', '--untracked-files=no').strip():
        raise ValueError('Clone tem alterações versionadas; importação recusada')
    if target.exists():
        verify_snapshot(root)
    (root / 'vendor').mkdir(exist_ok=True)
    (root / 'registry').mkdir(exist_ok=True)
    entries = []
    with tempfile.TemporaryDirectory(prefix='.gstack-import-', dir=root / 'vendor') as work:
        stage = Path(work) / 'source'
        stage.mkdir()
        for raw in git(source, 'ls-files', '--stage', '-z').split(b'\0'):
            if not raw:
                continue
            metadata, path_bytes = raw.split(b'\t', 1)
            mode, blob, number = metadata.decode().split()
            name = path_bytes.decode()
            safe_path(name)
            if mode not in ('100644', '100755', '120000') or number != '0':
                raise ValueError(f'Entrada Git não suportada: {name}')
            src, dst = source / name, stage / name
            data = os.readlink(src).encode() if mode == '120000' else src.read_bytes()
            calculated = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
            if calculated != blob:
                raise ValueError(f'Blob diverge do index: {name}')
            dst.parent.mkdir(parents=True, exist_ok=True)
            if mode == '120000':
                dst.symlink_to(data.decode())
                if not dst.resolve().is_relative_to(stage.resolve()):
                    raise ValueError(f'Symlink escapa do snapshot: {name}')
            else:
                dst.write_bytes(data)
                dst.chmod(0o755 if mode == '100755' else 0o644)
            entries.append({'path': name, 'mode': mode, 'sha256': hashlib.sha256(data).hexdigest()})
        if not entries:
            raise ValueError('Snapshot vazio')
        for required in ('LICENSE', 'NOTICE.md', 'licenses/Apache-2.0.txt', 'setup', 'package.json'):
            if not (stage / required).is_file():
                raise ValueError(f'Arquivo essencial ausente; snapshot anterior preservado: {required}')
        for entry in entries:
            if entry['mode'] == '120000' and not (stage / entry['path']).exists():
                raise ValueError(f'Symlink quebrado: {entry["path"]}')
        version = json.loads((stage / 'package.json').read_text())['version']
        manifest = {'repository': 'https://github.com/garrytan/gstack', 'revision': revision,
                    'version': version, 'imported_on': imported_on, 'directory': 'vendor/gstack', 'files': entries}
        manifest_path = root / 'registry/gstack-upstream.json'
        pending = Path(work) / 'manifest.json'
        pending.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        previous = Path(work) / 'previous'
        existed = target.exists()
        if existed:
            target.rename(previous)
        try:
            stage.rename(target)
            pending.replace(manifest_path)
        except Exception:
            if target.exists():
                target.rename(stage)
            if existed:
                previous.rename(target)
            raise
    return len(entries)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True, type=Path)
    parser.add_argument('--revision', required=True)
    args = parser.parse_args()
    try:
        count = import_snapshot(ROOT, args.source, args.revision, date.today().isoformat())
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        parser.exit(1, f'Erro: {error}\n')
    print(f'Importados {count} arquivos. Gere o catálogo e revise as mudanças antes de publicar.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
