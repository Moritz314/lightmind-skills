"""Rebuild index.json from the skills/ folder, so `lm skill list` and `lm skill add` can read it.

    python scripts/build_index.py            write index.json
    python scripts/build_index.py --check    exit 1 when index.json is out of date (for CI)

Name and description come from the frontmatter of each SKILL.md. Uses only the standard library.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORMAT_VERSION = 1


def frontmatter(skill_file: Path) -> dict:
    """The `key: value` pairs of the frontmatter block of one SKILL.md."""
    m = re.match(r"---\r?\n(.*?)\r?\n---", skill_file.read_text(encoding="utf-8"), re.S)
    if not m:
        raise SystemExit(f"{skill_file}: no frontmatter")
    keys = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            k, _, v = line.partition(":")
            keys[k.strip()] = v.strip().strip('"').strip("'")
    return keys


def build() -> dict:
    """The index as a dict: one entry per skill folder, files listed relative to the skill folder."""
    skills = []
    for folder in sorted((ROOT / "skills").iterdir()):
        skill_file = folder / "SKILL.md"
        if not skill_file.is_file():
            continue
        keys = frontmatter(skill_file)
        if keys.get("name") != folder.name or not keys.get("description"):
            raise SystemExit(f"{skill_file}: name must equal the folder name and description must be set")
        files = sorted(p.relative_to(folder).as_posix() for p in folder.rglob("*")
                       if p.is_file() and "__pycache__" not in p.parts)
        skills.append({"name": folder.name, "description": keys["description"],
                       "path": f"skills/{folder.name}", "files": files})
    return {"format": FORMAT_VERSION, "name": "lightmind-skills", "skills": skills}


def main(argv: list[str]) -> int:
    text = json.dumps(build(), indent=2, ensure_ascii=False) + "\n"
    target = ROOT / "index.json"
    if "--check" in argv:
        current = target.read_text(encoding="utf-8") if target.exists() else ""
        if current != text:
            print("index.json is out of date: run python scripts/build_index.py")
            return 1
        print("index.json is up to date")
        return 0
    target.write_text(text, encoding="utf-8")
    print(f"wrote index.json with {len(json.loads(text)['skills'])} skills")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
