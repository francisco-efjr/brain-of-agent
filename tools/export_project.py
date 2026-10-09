#!/usr/bin/env python3
"""Exportar brains próprios e fontes gstack para um projeto, sem setup ou sobrescrita."""
from __future__ import annotations

import argparse
import json
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
    brains = sorted(path.parent for path in (root / 'brains').glob('*/SKILL.md'))
    if not brains or any(path.is_symlink() or not path.resolve().is_relative_to((root / 'brains').resolve()) for path in brains):
        raise ValueError('Brains próprios ausentes ou fora do diretório permitido')
    if any(path.name == 'gstack' for path in brains):
        raise ValueError('Nome de brain reservado: gstack')
    skill_dir = '.claude/skills' if host == 'claude' else '.agents/skills'
    sources = [(root / 'vendor/gstack', 'gstack'), *[(path, path.name) for path in brains]]
    destinations = [project / '.claude/skills/gstack',
                    *[project / skill_dir / path.name for path in brains]]
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
        for source, name in sources:
            ignore = None if name == 'gstack' else shutil.ignore_patterns('__pycache__', '*.pyc', '.pytest_cache')
            shutil.copytree(source, stage / name, symlinks=True, ignore=ignore)
            if name != 'gstack':
                # Material comum torna a leitura integral portável sem depender
                # de caminhos da raiz do repositório original.
                common = stage / name / 'assets/contexto'
                shared = {
                    'contexto-completo.md': root / 'docs/contexto/brain-of-agent-contexto-completo.md',
                    'integration.md': root / 'docs/integration.md',
                    'skills.json': root / 'registry/skills.json',
                }
                availability = {}
                for filename, origin in shared.items():
                    availability[filename] = origin.is_file()
                    if origin.is_file():
                        common.mkdir(parents=True, exist_ok=True)
                        if (common / filename).exists():
                            raise ValueError(f'Recurso comum já existe na skill: {name}/{filename}')
                        shutil.copyfile(origin, common / filename)
                common.mkdir(parents=True, exist_ok=True)
                metadata = common / 'availability.json'
                if metadata.exists():
                    raise ValueError(f'Manifest comum já existe: {name}')
                metadata.write_text(json.dumps({'resources': availability,
                    'complete': all(availability.values())}, indent=2) + '\n', encoding='utf-8')
        try:
            for (_, name), destination in zip(sources, destinations):
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
    for destination in destinations[1:]:
        metadata = json.loads((destination / 'assets/contexto/availability.json').read_text())
        missing = [name for name, exists in metadata['resources'].items() if not exists]
        if missing:
            print(f'Aviso: recursos comuns ausentes em {destination.name}: {", ".join(missing)}; leitura integral parcial.')
    print('Setup NÃO executado. Próxima etapa, com Bun >= 1.4.0 disponível:')
    print(f'cd {shlex.quote(str(destinations[0]))}')
    print(f'./setup --host {args.host} --prefix')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
