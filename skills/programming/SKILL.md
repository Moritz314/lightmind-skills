---
name: programming
description: Master rules for writing, changing, fixing and reviewing code - scripts, tools, apps, extensions, bug fixes, refactors, tests. Use for every programming task, also when you delegate one ("build", "write a script", "fix the bug", "refactor", "code review"). Contains the house rules (comments, style, tests, finishing); pass them on to sub-agents that write code.
---

# programming

This skill is the master prompt for programming. Section 1 holds the house rules; they come before everything else, and you can edit them to your taste. Sections 2-5 are the workflow.
When you hand code work to a sub-agent, write into the brief: "Read skills/programming/SKILL.md first and follow it."

## 1. House rules (edit to your taste)

### Comments
- Comments explain the **why**, not the what. Every file starts with one sentence (two at most) about its purpose.
- Called functions: 1 to 2 sentences on what the function does, plus a few words to one sentence per argument.
- No commented-out code, no history comments, no `TODO` without an issue number or an owner. One fact lives in one place; config files: at most one short line per key.
- Language of code, identifiers and comments: English. Texts for users: in the language of the product.

### Style
- Adopt the style of the existing file, unless the project's formatter configuration says otherwise. For new files follow the project's conventions (naming, layout, formatter); if there are none, pick the usual ones of the language and stay consistent.
- Small functions, speaking names, no abbreviations except the common ones (`id`, `url`, `api` ...; not `cfg`).
- Python: dependencies inline (PEP 723) and start with `uv run` when the project uses uv. Standard library before new packages.
- No new dependency and no new framework without a reason that you name in the report.

### Tests and checks
- Every change is executed before it counts as "done": syntax check, tests, or a real run.
- Every test that is meant to prove a promise needs its counter-test: it must turn red when the promise is broken.
- Security checks go where the attacker passes by, not in the convenient preparation step.

### Report
- Short: what changed, where (paths), what was checked, what could not be checked.

## 2. Understand

1. Have the goal in one sentence. If it is ambiguous and expensive to guess wrong: ask once; otherwise take the obvious reading and state it in the report.
2. Read first, then write: the affected files, their callers, existing tests, the README of the folder. Read big files in parts (grep, sections) rather than whole.
3. Find the cause, do not patch the symptom. For a bug: reproduce it, then fix it.

## 3. Change

- Smallest diff that reaches the goal. Do not rebuild things on the side that nobody asked for; name findings instead of touching them.
- Before overwriting a file that is not under version control: make a backup `<file>.bak-<date>`.
- Long or delicate replacements run as a script file, not as a long one-liner with many escapes.
- No secrets in code, logs, command lines or tests. Values come from the environment.
- Working in parallel: `git pull` before you commit, stage only your own files, never revert other people's work.

## 4. Check

1. Run: the project's formatter and linter, syntax checks (`node --check`, `python -m py_compile`, type check), then tests, then a real call with sample data. Keep one test or screenshot per requirement ready so a reviewer can verify it.
2. Check the failure case too: wrong input, empty input, missing file.
3. For larger or security-relevant changes: put a second agent on the diff as a critic.

## 5. Finish

- Done means: goal reached, checked by yourself, documented (README / header comment up to date).
- Say openly what does not work or was blocked. Report nothing as done that was not executed.
