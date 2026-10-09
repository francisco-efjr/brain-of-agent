"""Regressões da cópia, catálogo e exportação; fixtures locais sem rede/runtime."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from catalog import build_catalog, serialize
from export_project import export_project
from import_gstack import import_snapshot
from verify import safe_path, verify_own, verify_snapshot


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='brain-integration-')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / 'repository'
        self.root.mkdir()
        self.vendor = self.root / 'vendor/gstack'
        self.vendor.mkdir(parents=True)
        self.write(self.root / 'SKILL.md', '---\nname: brain-of-agent\ndescription: router\n---\n')
        self.write(self.root / 'brains/qa/SKILL.md', '---\nname: qa\ndescription: QA\n---\n')
        self.write(self.root / 'brains/qa/references/risk.md', 'QA knowledge\n')
        files = {
            'LICENSE': 'MIT fixture\n', 'NOTICE.md': 'Credits fixture\n',
            'licenses/Apache-2.0.txt': 'License fixture\n',
            'setup': '#!/bin/sh\nprintf executed > "$PWD/EXECUTED"\n',
            'package.json': '{"version":"1.0.0"}\n',
            'SKILL.md': '---\nname: gstack\ndescription: router\n---\n',
            'qa/SKILL.md': '---\nname: qa\ndescription: QA workflow\n---\n',
            'browser-skills/example/SKILL.md': '---\nname: example\ndescription: nested\n---\n',
            'test/fixtures/not-a-workflow/SKILL.md': '---\nname: fake-test-skill\n---\n',
            'lib/diagram-render/dist/fixture.js': 'kept despite ignore\n',
            'test/fixtures/__pycache__/fixture.txt': 'tracked fixture, must export\n',
        }
        entries = []
        for name, content in files.items():
            path = self.vendor / name
            self.write(path, content)
            mode = '100755' if name == 'setup' else '100644'
            path.chmod(0o755 if mode == '100755' else 0o644)
            entries.append({'path': name, 'mode': mode, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
        (self.vendor / 'connect').symlink_to('qa')
        entries.append({'path': 'connect', 'mode': '120000', 'sha256': hashlib.sha256(b'qa').hexdigest()})
        self.manifest = {'repository': 'https://github.com/garrytan/gstack',
                         'revision': 'a' * 40, 'version': '1.0.0', 'directory': 'vendor/gstack',
                         'imported_on': '2026-10-05', 'files': sorted(entries, key=lambda e: e['path'])}
        self.save_manifest()
        self.write(self.root / 'registry/skills.json', serialize(build_catalog(self.root)))

    @staticmethod
    def write(path, content):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')

    def save_manifest(self):
        self.write(self.root / 'registry/gstack-upstream.json', json.dumps(self.manifest))

    def project(self):
        path = self.base / 'project'
        path.mkdir()
        return path

    def test_catalog_keeps_both_qa_and_nested_source_skills(self):
        catalog = build_catalog(self.root)
        ids = {entry['id'] for entry in catalog['skills']}
        self.assertIn('brain/qa', ids)
        self.assertIn('gstack/qa', ids)
        self.assertIn('gstack/browser-skills/example', ids)
        self.assertNotIn('gstack/test/fixtures/not-a-workflow', ids)
        self.assertEqual(verify_own(self.root), 5)

    def test_stale_catalog_is_rejected(self):
        self.write(self.root / 'registry/skills.json', '{}')
        with self.assertRaisesRegex(ValueError, 'desatualizado'):
            verify_own(self.root)

    def test_missing_announced_resource_is_rejected(self):
        self.write(self.root / 'brains/qa/SKILL.md', '---\nname: qa\n---\nLeia `references/missing.md`.\n')
        with self.assertRaisesRegex(ValueError, 'Recurso anunciado ausente'):
            verify_own(self.root)

    def test_hash_detects_tampering(self):
        (self.vendor / 'NOTICE.md').write_text('changed')
        with self.assertRaisesRegex(ValueError, 'Conteúdo alterado'):
            verify_snapshot(self.root)

    def test_extra_and_missing_files_do_not_pass(self):
        self.write(self.vendor / 'extra', 'not in snapshot')
        with self.assertRaisesRegex(ValueError, 'Inventário divergiu'):
            verify_snapshot(self.root)
        (self.vendor / 'extra').unlink()
        (self.vendor / 'LICENSE').unlink()
        with self.assertRaisesRegex(ValueError, 'Arquivo ausente'):
            verify_snapshot(self.root)

    def test_symlink_type_target_and_executable_modes_are_preserved(self):
        self.assertEqual(verify_snapshot(self.root), len(self.manifest['files']))
        (self.vendor / 'connect').unlink()
        (self.vendor / 'connect').symlink_to(self.base)
        with self.assertRaisesRegex(ValueError, 'Symlink inválido'):
            verify_snapshot(self.root)
        (self.vendor / 'connect').unlink()
        self.write(self.vendor / 'connect', 'qa')
        with self.assertRaisesRegex(ValueError, 'Symlink ausente'):
            verify_snapshot(self.root)

    @unittest.skipUnless(os.name == 'posix', 'POSIX executable modes')
    def test_loss_of_executable_bit_is_rejected(self):
        (self.vendor / 'setup').chmod(0o644)
        with self.assertRaisesRegex(ValueError, 'Executabilidade alterada'):
            verify_snapshot(self.root)

    def test_unsafe_manifest_paths_are_rejected(self):
        for path in ('../file', '/etc/passwd', 'a/../file', 'a\\file', './file', ''):
            with self.subTest(path=path), self.assertRaises(ValueError):
                safe_path(path)

    def test_export_for_each_host_preserves_source_without_executing_it(self):
        for host in ('claude', 'codex'):
            project = self.base / host
            project.mkdir()
            destinations = export_project(self.root, project, host)
            self.assertTrue((destinations[1] / 'references/risk.md').is_file())
            availability = json.loads((destinations[1] / 'assets/contexto/availability.json').read_text())
            self.assertFalse(availability['complete'])
            self.assertFalse(availability['resources']['contexto-completo.md'])
            for entry in self.manifest['files']:
                exported = destinations[0] / entry['path']
                data = os.readlink(exported).encode() if exported.is_symlink() else exported.read_bytes()
                self.assertEqual(hashlib.sha256(data).hexdigest(), entry['sha256'])
            self.assertFalse((destinations[0] / 'EXECUTED').exists())
            self.assertEqual(destinations[1].relative_to(project.resolve()).as_posix(),
                             '.claude/skills/qa' if host == 'claude' else '.agents/skills/qa')

    def test_fullstack_missing_reference_is_detected(self):
        self.write(self.root / 'brains/fullstack/SKILL.md', '---\nname: fullstack\ndescription: dev\n---\n[Contract](references/contract.md)\n')
        self.write(self.root / 'registry/skills.json', serialize(build_catalog(self.root)))
        with self.assertRaisesRegex(ValueError, 'Recurso anunciado ausente'):
            verify_own(self.root)
        self.write(self.root / 'brains/fullstack/references/contract.md', 'valid contract')
        self.assertEqual(verify_own(self.root), len(build_catalog(self.root)['skills']))

    def test_export_all_brains_and_shared_context(self):
        self.write(self.root / 'brains/fullstack/SKILL.md', '---\nname: fullstack\ndescription: dev\n---\n')
        self.write(self.root / 'docs/contexto/brain-of-agent-contexto-completo.md', 'shared knowledge')
        self.write(self.root / 'docs/integration.md', 'setup guide')
        self.write(self.root / 'registry/skills.json', serialize(build_catalog(self.root)))
        for host in ('claude', 'codex'):
            project = self.base / ('multi-' + host)
            project.mkdir()
            destinations = export_project(self.root, project, host)
            self.assertEqual([p.name for p in destinations], ['gstack', 'fullstack', 'qa'])
            for destination in destinations[1:]:
                self.assertEqual((destination / 'assets/contexto/contexto-completo.md').read_text(), 'shared knowledge')
                self.assertTrue((destination / 'assets/contexto/skills.json').is_file())
                self.assertTrue(json.loads((destination / 'assets/contexto/availability.json').read_text())['complete'])
            self.assertTrue((destinations[1].parent / 'qa/SKILL.md').exists())

    def test_fullstack_collision_prevents_all_writes(self):
        self.write(self.root / 'brains/fullstack/SKILL.md', '---\nname: fullstack\ndescription: dev\n---\n')
        project = self.project()
        existing = project / '.agents/skills/fullstack/SKILL.md'
        self.write(existing, 'preserved')
        with self.assertRaisesRegex(ValueError, 'Destino já existe'):
            export_project(self.root, project, 'codex')
        self.assertEqual(existing.read_text(), 'preserved')
        self.assertFalse((project / '.claude/skills/gstack').exists())
        self.assertFalse((project / '.agents/skills/qa').exists())

    def test_reserved_brain_name_rejected(self):
        self.write(self.root / 'brains/gstack/SKILL.md', '---\nname: gstack\ndescription: reserved\n---\n')
        project = self.project()
        with self.assertRaisesRegex(ValueError, 'reservado'):
            export_project(self.root, project, 'codex')
        self.assertEqual(list(project.iterdir()), [])

    def test_export_existing_skill_refuses_before_writing_other_destination(self):
        project = self.project()
        existing = project / '.agents/skills/qa/SKILL.md'
        self.write(existing, 'keep me')
        with self.assertRaisesRegex(ValueError, 'Destino já existe'):
            export_project(self.root, project, 'codex')
        self.assertEqual(existing.read_text(), 'keep me')
        self.assertFalse((project / '.claude/skills/gstack').exists())

    def test_export_cannot_escape_through_parent_symlink(self):
        project = self.project()
        external = self.base / 'external'
        external.mkdir()
        (project / '.claude').symlink_to(external)
        with self.assertRaisesRegex(ValueError, 'fora do projeto'):
            export_project(self.root, project, 'claude')
        self.assertEqual(list(external.iterdir()), [])

    def test_export_rejects_tampered_source_before_writing(self):
        project = self.project()
        (self.vendor / 'setup').write_text('bad')
        with self.assertRaisesRegex(ValueError, 'Conteúdo alterado'):
            export_project(self.root, project, 'claude')
        self.assertEqual(list(project.iterdir()), [])

    def test_import_clean_git_fixture_and_reject_dirty_revision(self):
        source = self.base / 'source'
        import shutil
        shutil.copytree(self.vendor, source, symlinks=True)

        def run(*args):
            return subprocess.check_output(['git', '-C', str(source), *args], stderr=subprocess.STDOUT, timeout=10)

        run('init', '--initial-branch=main')
        run('add', '.')
        run('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-m', 'fixture')
        run('remote', 'add', 'origin', 'https://github.com/garrytan/gstack.git')
        revision = run('rev-parse', 'HEAD').decode().strip()
        imported = self.base / 'imported'
        imported.mkdir()
        self.assertEqual(import_snapshot(imported, source, revision, '2026-10-05'), len(self.manifest['files']))
        self.assertEqual(verify_snapshot(imported), len(self.manifest['files']))
        manifest_before = (imported / 'registry/gstack-upstream.json').read_bytes()
        with self.assertRaisesRegex(ValueError, 'revisão solicitada'):
            import_snapshot(imported, source, 'b' * 40, '2026-10-05')
        self.assertEqual((imported / 'registry/gstack-upstream.json').read_bytes(), manifest_before)
        run('checkout', '--', 'NOTICE.md')
        (imported / 'vendor/gstack/LICENSE').write_text('local edit')
        with self.assertRaisesRegex(ValueError, 'Conteúdo alterado'):
            import_snapshot(imported, source, revision, '2026-10-05')
        self.assertEqual((imported / 'vendor/gstack/LICENSE').read_text(), 'local edit')
        (source / 'NOTICE.md').write_text('dirty')
        with self.assertRaisesRegex(ValueError, 'alterações versionadas'):
            import_snapshot(imported, source, revision, '2026-10-05')
        self.assertEqual((imported / 'registry/gstack-upstream.json').read_bytes(), manifest_before)


if __name__ == '__main__':
    unittest.main()
