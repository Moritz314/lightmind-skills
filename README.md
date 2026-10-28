# lightmind-skills

Ready-made skills for [Lightmind](https://github.com/Moritz314/lightmind), the file-based agent harness. A skill is a folder with a `SKILL.md` that the AI reads when a task needs it. Everything here runs on your machine, without paid services and without extra accounts.

Licensed under the [Apache License 2.0](LICENSE). Provided "as is", without warranty.

## Skills

| Skill | What it does |
|---|---|
| [`programming`](skills/programming/SKILL.md) | House rules and a workflow for writing, changing, checking and finishing code. |
| [`delegation`](skills/delegation/SKILL.md) | Splits a big task into independent parts and hands them to parallel sub-agents, then checks and merges the results. |
| [`inquisition`](skills/inquisition/SKILL.md) | Plans a project by interviewing you one question at a time, with options and a recommendation, and ends in a full plan. |
| [`browser`](skills/browser/SKILL.md) | Reads web pages, takes screenshots, logs in and fills forms with a local Playwright browser. |
| [`triggers`](skills/triggers/SKILL.md) | Runs an agent on a schedule through cron (Linux, macOS) or the Windows Task Scheduler. |
| [`ultracode`](skills/ultracode/SKILL.md) | Writes workflow scripts for the built-in `workflow` tool: fan-outs, adversarial checks, judge panels, resumable runs. |
| [`skill-creator`](skills/skill-creator/SKILL.md) | Builds a new skill from your description, checks it and saves it under `skills/`. |

## Install

```bash
lm skill list                 # show the skills in this repository
lm skill add programming      # copy skills/programming into your tree's skills/ folder
lm skill add delegation inquisition
```

Without the command: copy the folder `skills/<name>/` into the `skills/` folder of your Lightmind tree. The AI finds it by itself in the next session.

Some skills need a little more on your machine:

- `browser`: Python 3.11+ and [`uv`](https://docs.astral.sh/uv/); Playwright and Chromium are installed on the first run.
- `triggers`: `uv`, and `lm` on your PATH.
- `delegation`, `ultracode`: the `spawn` and `workflow` tools of the Lightmind core.

## Format of this repository

```text
lightmind-skills/
├─ index.json            list of all skills (read by `lm skill list` / `lm skill add`)
├─ skills/
│  └─ <name>/
│     ├─ SKILL.md        required: frontmatter and instructions
│     ├─ scripts/        optional: scripts the skill tells the AI to run
│     └─ references/     optional: long material, read only when needed
├─ scripts/build_index.py
├─ LICENSE
└─ README.md
```

`SKILL.md` begins with a frontmatter block:

```markdown
---
name: programming            # equals the folder name; lowercase letters, digits, hyphens
description: <what it does>. Use when <situations and phrases>.   # one line, at most 1024 characters
---
```

`index.json`:

```json
{
  "format": 1,
  "name": "lightmind-skills",
  "skills": [
    {
      "name": "programming",
      "description": "Master rules for writing, changing, fixing ...",
      "path": "skills/programming",
      "files": ["SKILL.md"]
    }
  ]
}
```

- `format`: version of this index layout (now `1`).
- `name`, `description`: from the frontmatter of the skill.
- `path`: folder of the skill, relative to the repository root.
- `files`: every file of the skill, relative to its folder; `lm skill add` copies exactly these.

`scripts/build_index.py` writes the file from the skills folder; do not edit `index.json` by hand.

## Contribute

1. Fork the repository and create a folder `skills/<name>/` (the skill `skill-creator` does this for you).
2. Write the `SKILL.md`: one skill, one job; English; a `description` that says what it does and when to use it; no secrets, no personal data, no absolute paths of your machine; no paid services or accounts as a requirement.
3. Check it: `python skills/skill-creator/scripts/check_skill.py skills/<name>`.
4. Rebuild the list: `python scripts/build_index.py`.
5. Open a pull request. Describe what the skill is for and how you tested it. Contributions are licensed under Apache 2.0.

Bugs and questions: GitHub Issues and Discussions of the Lightmind repository.
