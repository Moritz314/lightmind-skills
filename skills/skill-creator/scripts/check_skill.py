"""Check a skill folder against the skill format and print every problem.

    python check_skill.py skills/<name>          one skill
    python check_skill.py skills                 every skill below a skills folder

Exit code 0 when all checked skills are fine, 1 when there is a problem, 2 on bad usage.
Uses only the standard library.
"""
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")
MAX_NAME = 64
MAX_DESCRIPTION = 1024
MIN_DESCRIPTION = 40
SECTION_HINTS = ("when", "use", "step", "how", "example", "rule")


def read_frontmatter(text: str) -> tuple[dict, str] | None:
    """Split a SKILL.md into (frontmatter keys, body); None when there is no frontmatter block.

    Only simple `key: value` lines are understood, which is all the format needs."""
    m = re.match(r"---\r?\n(.*?)\r?\n---\r?\n?(.*)", text, re.S)
    if not m:
        return None
    keys = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            k, _, v = line.partition(":")
            keys[k.strip()] = v.strip().strip('"').strip("'")
    return keys, m.group(2)


def check_skill(folder: Path) -> list[str]:
    """Return the list of problems of one skill folder (empty list = fine)."""
    problems = []
    skill_file = folder / "SKILL.md"
    if not skill_file.is_file():
        return [f"{folder}: SKILL.md is missing"]
    parsed = read_frontmatter(skill_file.read_text(encoding="utf-8"))
    if parsed is None:
        return [f"{skill_file}: no frontmatter block (the file must start with --- and end the block with ---)"]
    keys, body = parsed
    name, description = keys.get("name", ""), keys.get("description", "")
    if not name:
        problems.append("frontmatter: `name` is missing")
    elif name != folder.name:
        problems.append(f"frontmatter: name `{name}` must equal the folder name `{folder.name}`")
    if name and (not NAME_RE.fullmatch(name) or len(name) > MAX_NAME):
        problems.append(f"frontmatter: name `{name}` must be lowercase letters, digits and single hyphens, at most {MAX_NAME} characters")
    if not description:
        problems.append("frontmatter: `description` is missing or not on a single line")
    else:
        if len(description) > MAX_DESCRIPTION:
            problems.append(f"frontmatter: description has {len(description)} characters, the limit is {MAX_DESCRIPTION}")
        if len(description) < MIN_DESCRIPTION:
            problems.append("frontmatter: description is too short to tell the AI when to use the skill")
        if not re.search(r"\buse\b|\bwhen\b", description, re.I):
            problems.append('frontmatter: description should say when to use the skill ("Use when ...", "Use for ...")')
    if len(body.strip()) < 200:
        problems.append("body: fewer than 200 characters, the skill has no real instructions")
    if not re.search(r"^# ", body, re.M):
        problems.append("body: no top-level heading (`# <name>`)")
    if not any(h in body.lower() for h in SECTION_HINTS):
        problems.append("body: no steps, rules or example found")
    for ref in re.findall(r"`((?:scripts|references|assets)/[^`\s]+)`", body):
        if not (folder / ref).exists():
            problems.append(f"body: mentions `{ref}` but the file does not exist")
    return [f"{folder.name}: {p}" for p in problems]


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2
    target = Path(argv[1])
    if not target.is_dir():
        print(f"error: {target} is not a folder")
        return 2
    folders = [target] if (target / "SKILL.md").exists() else sorted(p for p in target.iterdir() if p.is_dir())
    problems = [p for f in folders for p in check_skill(f)]
    for p in problems:
        print("PROBLEM", p)
    print(f"checked {len(folders)} skill(s): {'ok' if not problems else str(len(problems)) + ' problem(s)'}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
