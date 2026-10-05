#!/usr/bin/env python3
"""Exportar fontes QA/gstack para um projeto, sem setup ou sobrescrita."""
from __future__ import annotations

import argparse
import shlex
import shutil
import tempfile
from pathlib import Path

from catalog import ROOT
from verify import verify_snapshot


def export_project(root: Path, target: Path, host: str) -> list[Path]:
    if host not in ('claude', 'codex'):
        raise ValueError(f'Host não suportado: {host}')
    if not target.is_dir():
        raise ValueError('O diretório do projeto precisa existir')
    project = target.resolve()
    if project == root.resolve() or project.is_relative_to((root / 'vendor').resolve()):
        raise ValueError('Escolha outro projeto; preserve o checkout e o snapshot')
    verify_snapshot(root)
    destinations = [project / '.claude/skills/gstack',
                    project / ('.claude/skills/qa' if host == 'claude' else '.agents/skills/qa')]
    for destination in destinations:
        if destination.exists() or destination.is_symlink():
            raise ValueError(f'Destino já existe; nada exportado: {destination}')
        if not destination.parent.resolve().is_relative_to(project):
            raise ValueError(f'Destino aponta para fora do projeto: {destination}')
        for parent in destination.parents:
            if parent == project:
                break
            if parent.exists() and not parent.is_dir():
                raise ValueError(f'Pai do destino não é diretório: {parent}')
            if parent.is_symlink() and not parent.exists():
                raise ValueError(f'Symlink de destino quebrado: {parent}')
    created = []
    with tempfile.TemporaryDirectory(prefix='.brain-export-', dir=project) as work:
        stage = Path(work)
        for source, name in ((root / 'vendor/gstack', 'gstack'), (root / 'brains/qa', 'qa')):
            ignore = None if name == 'gstack' else shutil.ignore_patterns('__pycache__', '*.pyc', '.pytest_cache')
            shutil.copytree(source, stage / name, symlinks=True, ignore=ignore)
        try:
            for name, destination in zip(('gstack', 'qa'), destinations):
                destination.parent.mkdir(parents=True, exist_ok=True)
                if destination.exists() or destination.is_symlink():
                    raise ValueError(f'Destino apareceu durante exportação: {destination}')
                (stage / name).rename(destination)
                created.append(destination)
        except Exception:
            # Só desfaz destinos novos criados por esta operação.
            for destination in reversed(created):
                destination.rename(stage / destination.name)
            raise
    return destinations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', required=True, choices=('claude', 'codex'))
    parser.add_argument('--target', required=True, type=Path)
    args = parser.parse_args()
    try:
        destinations = export_project(ROOT, args.target, args.host)
    except (OSError, ValueError, KeyError) as error:
        parser.exit(1, f'Erro: {error}\n')
    for destination in destinations:
        print(f'Fontes exportados: {destination}')
    print('Setup NÃO executado. Próxima etapa, com Bun >= 1.4.0 disponível:')
    print(f'cd {shlex.quote(str(destinations[0]))}')
    print(f'./setup --host {args.host} --prefix')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
