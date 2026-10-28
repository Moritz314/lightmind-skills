---
name: skill-creator
description: Build a new skill from a plain description - ask what it should do, write the SKILL.md in the correct format (frontmatter, triggers, steps, example), check it with a script and save it under skills/. Use when the user says "make a skill for ...", "create a skill", "turn this into a skill", "teach yourself to ...", or wants to save a repeatable way of working.
---

# skill-creator

A skill is a folder `skills/<name>/` with a `SKILL.md` that the AI reads when a task needs it. This skill turns a description of the user into such a folder, checks it, and puts it in place.

## Format (short)

```text
skills/<name>/
├─ SKILL.md        required: frontmatter and instructions
├─ scripts/        optional: scripts the skill tells the AI to run
└─ references/     optional: long material, read only when needed
```

`SKILL.md` starts with a frontmatter block, then the instructions:

```markdown
---
name: <name>            # equals the folder name; lowercase letters, digits, single hyphens
description: <what it does>. Use when <situations>, or when the user says "<phrases>".
---

# <name>
...
```

The `description` is the only text the AI sees before it decides to open the skill. It must say **what** the skill does and **when** to use it, with the words the user would really use. One line, at most 1024 characters. A template is in `references/skill-template.md`.

## Steps

1. **Understand.** From the user's description, find out: what is the task, what triggers it (which phrases, which situations), what is the result, what must never happen. Ask only what you cannot find out yourself; one short question at a time, at most three in total. If the user gave a finished example (a file, a past chat), read it instead of asking.
2. **Check for overlap.** List `skills/`. If a skill already covers the task, say so and offer to extend it instead of creating a second one.
3. **Pick the name.** Short, lowercase, hyphens, named after the task (`weekly-report`, `release-notes`), not after the user.
4. **Write `skills/<name>/SKILL.md`** from `references/skill-template.md`:
   - `description`: what + "Use when ..." + 2 to 4 real trigger phrases.
   - Body: goal in one or two sentences; when to use (and when not); numbered steps with exact files, commands and checks; rules for what the AI would otherwise get wrong; one worked example.
   - Write instructions to the AI in the imperative, in plain sentences. Explain the why of a rule in half a sentence; do not shout in capitals.
   - Keep `SKILL.md` under about 300 lines. Put long tables, templates and background into `references/` and name them in the steps ("read the reference file when ...").
   - Put code the AI should run into `scripts/` and call it from a step; do not paste long code into the body. Scripts need to run without paid services or accounts unless the user wants them.
   - No secrets, tokens, personal data or absolute paths of one machine in the skill. Use relative paths and environment variables.
5. **Check.** Run `python skills/skill-creator/scripts/check_skill.py skills/<name>` and fix every problem it prints. Then read the skill once as if you had never seen the task: could you do it from this text alone?
6. **Test it.** Run the skill's main steps once on a small real or sample case (do not skip this). Fix unclear steps.
7. **Report.** Tell the user the path, the trigger phrases, and one sentence on how to change the skill later (edit the file; the next session picks it up).

## Rules

- One skill, one job. If the description needs "and" for two unrelated jobs, make two skills.
- Do not copy another skill's text unchanged. Link to it by name ("see skill `delegation`").
- A skill never grants rights. Say in the skill when to ask the user first (sending, buying, deleting).
- Never overwrite an existing `skills/<name>/` without the user's yes; make a backup copy first.

## Example

User: "Make a skill that writes my weekly status report from the git log."

1. Questions: which repositories, which format (bullet list or prose), where the report goes. The user answers: one repo, five bullets, `out/status.md`.
2. `skills/` has no similar skill. Name: `weekly-status`.
3. Write `skills/weekly-status/SKILL.md`:

```markdown
---
name: weekly-status
description: Write the weekly status report from the git log of the current repository into out/status.md. Use when the user says "weekly status", "what did I do this week", "status report".
---

# weekly-status

Turn the commits of the last seven days into five bullet points in `out/status.md`.

## Steps

1. Run `git log --since="7 days ago" --no-merges --pretty="%h %s"`.
2. Group the commits by topic and write at most five bullets, each one sentence, result first.
3. Write the bullets to `out/status.md`; answer with the path and the bullets.

## Rules

- Do not invent work that is not in the log.
- If the log is empty, say so instead of writing a report.
```

4. `python skills/skill-creator/scripts/check_skill.py skills/weekly-status` prints `checked 1 skill(s): ok`.
5. Answer: "Skill created: skills/weekly-status/SKILL.md. Say 'weekly status' to use it."
