#!/usr/bin/env python3
"""Deterministic structural checks for a dev-segments plugin (stdlib only).

Usage: python tools/verify_plugin.py plugins/<slug> [--json]
Exit code 0 = no errors (warnings allowed), 1 = errors found.
"""
import json
import re
import sys
from pathlib import Path

RESERVED_PREFIXES = ("claude-", "anthropic-", "anthropics-", "cc-plugin-")
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
FORBIDDEN_FILES = ("hooks/hooks.json", ".mcp.json", ".lsp.json")
SKILL_FIELDS = {
    "name", "description", "when_to_use", "argument-hint", "arguments",
    "disable-model-invocation", "user-invocable", "allowed-tools",
    "disallowed-tools", "model", "effort", "context", "agent", "background",
    "hooks", "paths", "shell", "metadata", "license", "compatibility",
}
AGENT_FIELDS = {
    "name", "description", "tools", "disallowedTools", "model", "permissionMode",
    "skills", "hooks", "mcpServers", "memory", "color", "effort", "maxTurns",
    "isolation", "background", "initialPrompt",
}
EVAL_PROMPT_FIELDS = {
    "schema_version", "name", "description", "tags", "plugins", "runs",
    "expected_outcome", "model", "max_turns", "timeout_seconds",
    "allowed_tools", "append_system_prompt", "env",
}
GRADER_TYPES = {"regex", "tool_used", "tool_order", "file_exists", "llm", "baseline"}
LINK = re.compile(r"\]\(([^)#\s]+\.md)(?:#[^)]*)?\)")


def parse_frontmatter(text):
    """Minimal YAML frontmatter reader: top-level keys only."""
    if not text.startswith("---"):
        return None, "missing frontmatter (file must start with ---)"
    end = text.find("\n---", 3)
    if end == -1:
        return None, "unterminated frontmatter"
    block = text[3:end].strip("\n")
    keys = {}
    for line in block.splitlines():
        if not line.strip() or line.lstrip().startswith("#") or line.startswith((" ", "\t", "-")):
            continue
        m = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$", line)
        if not m:
            return None, f"unparseable frontmatter line: {line[:60]!r}"
        keys[m.group(1)] = m.group(2).strip().strip("'\"")
    return keys, None


def check(root: Path):
    errors, warnings, stats = [], [], {"skills": 0, "agents": 0, "commands": 0, "evals": 0, "files": 0}
    manifest = root / ".claude-plugin" / "plugin.json"
    if not manifest.is_file():
        errors.append("missing .claude-plugin/plugin.json")
        name = root.name
    else:
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"plugin.json invalid JSON: {exc}")
            data = {}
        name = data.get("name", "")
        if not name:
            errors.append("plugin.json: name missing")
        elif not KEBAB.match(name):
            errors.append(f"plugin.json: name not kebab-case: {name}")
        if name.startswith(RESERVED_PREFIXES) or re.search(r"\b(claude|anthropic)\b", name.replace("-", " ")):
            errors.append(f"plugin.json: reserved-looking name: {name}")
        if name and name != root.name:
            warnings.append(f"plugin name {name!r} differs from directory {root.name!r}")
        for field in ("version", "description", "author"):
            if field not in data:
                warnings.append(f"plugin.json: {field} missing")
        for key in ("skills", "commands", "agents"):
            if key in data:
                warnings.append(f"plugin.json declares {key!r}; default directories are preferred")
    for rel in FORBIDDEN_FILES:
        if (root / rel).exists():
            errors.append(f"forbidden active component present: {rel} (project policy: document, do not activate)")
    if (root / "bin").exists():
        errors.append("forbidden bin/ directory present")
    if (root / "CLAUDE.md").exists():
        warnings.append("CLAUDE.md at plugin root is not loaded; move content into a skill")
    if not (root / "README.md").is_file():
        errors.append("README.md missing")

    skills_dir = root / "skills"
    for skill_md in sorted(skills_dir.glob("*/SKILL.md")) if skills_dir.is_dir() else []:
        stats["skills"] += 1
        text = skill_md.read_text(encoding="utf-8")
        fm, err = parse_frontmatter(text)
        rel = skill_md.relative_to(root).as_posix()
        if err:
            errors.append(f"{rel}: {err}")
            continue
        folder = skill_md.parent.name
        if fm.get("name") and fm["name"] != folder:
            errors.append(f"{rel}: name {fm['name']!r} != folder {folder!r}")
        if not KEBAB.match(folder):
            errors.append(f"{rel}: skill folder not kebab-case")
        desc = fm.get("description", "")
        if not desc:
            errors.append(f"{rel}: description missing")
        elif len(desc) > 1024:
            warnings.append(f"{rel}: description {len(desc)} chars (>1024; listing truncates at 1536 incl. when_to_use)")
        unknown = set(fm) - SKILL_FIELDS
        if unknown:
            warnings.append(f"{rel}: unknown frontmatter fields {sorted(unknown)}")
        lines = text.count("\n") + 1
        if lines > 500:
            warnings.append(f"{rel}: {lines} lines (>500); move detail into references/")
    if stats["skills"] == 0:
        errors.append("no skills found under skills/<name>/SKILL.md")
    for required in ("playbook", "prompts"):
        if not (skills_dir / required / "SKILL.md").is_file():
            errors.append(f"required skill missing: skills/{required}/SKILL.md")

    agents_dir = root / "agents"
    for agent_md in sorted(agents_dir.glob("**/*.md")) if agents_dir.is_dir() else []:
        stats["agents"] += 1
        rel = agent_md.relative_to(root).as_posix()
        fm, err = parse_frontmatter(agent_md.read_text(encoding="utf-8"))
        if err:
            errors.append(f"{rel}: {err}")
            continue
        for field in ("name", "description"):
            if not fm.get(field):
                errors.append(f"{rel}: {field} missing")
        unknown = set(fm) - AGENT_FIELDS
        if unknown:
            warnings.append(f"{rel}: unknown frontmatter fields {sorted(unknown)}")

    commands_dir = root / "commands"
    for cmd in sorted(commands_dir.glob("*.md")) if commands_dir.is_dir() else []:
        stats["commands"] += 1
        fm, err = parse_frontmatter(cmd.read_text(encoding="utf-8"))
        if err:
            errors.append(f"{cmd.relative_to(root).as_posix()}: {err}")

    evals_dir = root / "evals"
    for prompt in sorted(evals_dir.glob("**/prompt.md")) if evals_dir.is_dir() else []:
        if "results" in prompt.parts:
            continue
        stats["evals"] += 1
        case = prompt.parent
        rel = case.relative_to(root).as_posix()
        fm, err = parse_frontmatter(prompt.read_text(encoding="utf-8"))
        if err:
            errors.append(f"{rel}/prompt.md: {err}")
        else:
            unknown = set(fm) - EVAL_PROMPT_FIELDS
            if unknown:
                errors.append(f"{rel}/prompt.md: unknown keys {sorted(unknown)} (eval loader rejects unknown keys)")
        graders = sorted((case / "graders").glob("*.md"))
        if not graders and not (case / "case.yaml").exists():
            errors.append(f"{rel}: no graders (case fails to load)")
        for grader in graders:
            gfm, gerr = parse_frontmatter(grader.read_text(encoding="utf-8"))
            if gerr:
                errors.append(f"{rel}/graders/{grader.name}: {gerr}")
            elif gfm.get("type") not in GRADER_TYPES:
                errors.append(f"{rel}/graders/{grader.name}: invalid type {gfm.get('type')!r}")
    if stats["evals"] == 0:
        warnings.append("no eval cases under evals/<case>/prompt.md")

    for md in root.rglob("*.md"):
        stats["files"] += 1
        text = md.read_text(encoding="utf-8", errors="replace")
        for target in LINK.findall(text):
            if target.startswith(("http://", "https://", "mailto:")) or "${" in target:
                continue
            if not (md.parent / target).resolve().exists():
                warnings.append(f"{md.relative_to(root).as_posix()}: broken relative link -> {target}")
        if len(str(md.resolve())) > 240:
            warnings.append(f"long path ({len(str(md.resolve()))} chars): {md.relative_to(root).as_posix()}")
        if re.search(r"(sk-ant-[A-Za-z0-9]|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16})", text):
            errors.append(f"{md.relative_to(root).as_posix()}: looks like a credential")
    return errors, warnings, stats


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    root = Path(argv[1]).resolve()
    errors, warnings, stats = check(root)
    if "--json" in argv:
        print(json.dumps({"plugin": root.name, "errors": errors, "warnings": warnings, "stats": stats}, ensure_ascii=False, indent=2))
    else:
        print(f"Plugin: {root.name}  {stats}")
        for e in errors:
            print(f"ERROR   {e}")
        for w in warnings:
            print(f"WARNING {w}")
        print("RESULT: " + ("FAIL" if errors else ("PASS with warnings" if warnings else "PASS")))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
