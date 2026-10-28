---
name: triggers
description: Schedule an agent to run by itself (daily, weekly, every N minutes) by writing a trigger file and installing it into cron (Linux, macOS) or the Windows Task Scheduler. Use for "run this every morning", "schedule", "remind me", "cron".
---

# triggers

A trigger is one Markdown file in `triggers/` that says when to start which agent with which task. The script `skills/triggers/scripts/apply.py` installs the cron-type triggers into the operating system's own scheduler: a block in your user crontab on Linux and macOS, scheduled tasks named `Lightmind <name>` on Windows. No extra service, no account.

Format of the trigger folder: `triggers/README.md` of your tree.

## Trigger file

```markdown
---
when: "cron 0 7 * * 1-5"     # 5-field cron: minute hour day-of-month month day-of-week
task: "Summarise yesterday's notes into out/summary.md"
agent: my-agent               # a folder in agents/
enabled: false                # start switched off
---
Why this trigger exists (free text).
```

`schedule: "0 7 * * 1-5"` works in place of `when: "cron ..."`. Only numbers, `*`, `/`, `,` and `-` are allowed in the fields.

## Steps

1. Copy `triggers/_example.md` to `triggers/<name>.md`; set `when`, `agent`, `task` and `enabled: false`. The agent must exist and work when started by hand first.
2. A scheduled run has nobody to talk to: it must not ask questions, and it has only the rights of its agent. Tell the user what will run, when, and with which rights, and get a yes before you install.
3. Preview: `uv run skills/triggers/scripts/apply.py --dry-run`. Then set `enabled: true`.
4. Install: `uv run skills/triggers/scripts/apply.py`. Check: `uv run skills/triggers/scripts/apply.py --list`.
5. Remove one with `apply.py --remove <name>`, all with `apply.py --remove`.

Options: `--tree DIR` (the tree root; default `$LIGHTMIND_HOME`, else the current folder), `--lm PATH` (the `lm` command to put into the schedule; default `lm` from PATH).

## What gets installed

- Linux/macOS: between the lines `# lightmind triggers` and `# end lightmind triggers` in your user crontab, one line per trigger: `cd <tree> && lm run --detach -a <agent> "<task>"`. The rest of the crontab stays untouched.
- Windows: one task per trigger (`schtasks`), started through a small wrapper `triggers/.run/<name>.cmd` that changes into the tree root and calls `lm run`. Windows supports: every N minutes, hourly, daily, weekly (days of week), monthly (one day). A month field or other mixes are skipped with a message.

## Limits

- The tree's computer must be on at the scheduled time; cron and the Task Scheduler do not catch up on missed runs.
- `task` must be one line without `%` (cron treats it specially). `name` and `agent` may only hold letters, digits, `.`, `_`, `-`.
- Re-running `apply.py` replaces what it installed before; triggers you removed from the folder are removed from the scheduler.
