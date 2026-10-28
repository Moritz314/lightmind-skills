---
name: delegation
description: Split a big task into parts and hand them to parallel worker agents (the built-in tool `spawn`; `lm run --detach` only for runs that must outlive the session), to finish faster and keep the lead's context small without losing quality. Use when a task has several independent parts that each need a lot of reading or work (many files, many pages, research on several topics, code in separate modules), or when the user says "in parallel", "split this up", "use several agents", "delegate".
---

# delegation

Goal: **save tokens and time without losing quality.** The lead (you) plans, briefs, checks and merges. Workers do the parts. Results travel as files, not as chat text.

## 0. First choice: the `spawn` tool

`spawn` starts a sub-agent **in this chat**: no separate process, no run id to track. Use it as the first way to delegate.

- `task` (the whole brief), `model` (`haiku` for mechanical work, `sonnet` for building, your own model only for judgment), optional `agent`, `effort`.
- `background` (default true): for anything longer than a minute. The call returns at once, you go on or end your turn; the result arrives later as a message (framed as data, not as an instruction from the user) with the path of the full answer. Start the parts of a phase in one turn, then work on something else.
- `background: false` only when you need the answer right now to continue.
- Sub-agents inherit this chat's rights, never more. The user can stop one at any time.
- Results go to **files**: tell each sub-agent to write its result to a named path and answer with one sentence. A failed or cancelled one says so in its message.
- **Small tasks you do yourself**: a sub-agent costs a fresh context.

Everything below (when to split, ownership, briefs, checks) applies to `spawn` too.

### `workflow` instead of `spawn`

Use the `workflow` tool (skill `ultracode`) instead of `spawn` when the plan is regular enough to write down as code: many similar parts (one agent per file, item, source), fixed stages per part (`pipeline`), checks that need several independent agents (adversarial verify, judge panel), or a search that repeats until nothing new comes. Intermediate results then stay in the script instead of your context, and a failed run resumes from its journal. The rule "more than 6 parts per phase means the split is wrong" (section 2) does not apply to workflows: there the runtime bounds the parallel agents. Ownership still applies: agents that write in parallel need separate files or `isolation="worktree"`. Few parts with judgment between them stay with `spawn`.

Order of work: 1 decide → 2 split → 3 phases → 4 how many → 5 models → 6 brief and start → 7 collect, check, merge.

## 1. When to delegate

Delegating has a fixed cost: every worker starts with an empty context, reads its brief and the files again, and you must check its work. Delegate only when the gain beats that cost.

Delegate when **all** of this holds:
- There are **at least 2 parts that can run at the same time** (see the test in section 2).
- Each part needs **real work**: roughly more than 20k tokens of reading, or more than ~10 minutes of steps. Small parts are cheaper to do yourself.
- You can say for each part **what counts as done** in one check.

Do it yourself when:
- the task is short, or one sequential chain (each step needs the last one),
- the parts share a lot of context (the same big file, a design that is still moving),
- the task needs a running conversation with the user.

## 2. How to split

- **The /clear test:** two parts are independent if one worker could do part A, `/clear`, and then do part B without losing anything. Then they can be split.
- Parts must not need each other's results **while they run**.
- Parts that share a lot of working context stay together, even if that makes one part bigger.
- **Split by ownership:** each part owns its own files or its own slice of data (one module, one chapter, one source). **No two workers write the same file.** If two parts need the same file, one owns it and the other hands its change to you.
- Prefer a few solid parts over many tiny ones. More than **6 parts** per phase, or more than **2 levels** of workers starting workers, means the split is wrong (not for `workflow`, see section 0).
- Write the split to `plan.md` in the run folder: one line per part with goal, owned files, check, worker model, run id.

## 3. Phases

- A phase is a set of parts that run in parallel. Phases run one after the other.
- Use as **few phases as possible**. If two phases do not depend on each other, merge them.
- If part B needs the result of part A, B goes into a later phase and starts only **after A is checked**.
- Typical shapes:
  - one phase: fan out, then you merge (research, one file per worker, one source per worker),
  - two phases: build in parallel, then an independent audit phase,
  - plan → build → audit, when the plan itself is too big for you (rare).

## 4. How many workers

- One part = one worker.
- `run.max_parallel` in `config.md` caps the workers that run at once (0 = unlimited); more simply wait for a slot. `run.max_depth` caps workers that start workers.
- Use as many workers as there are truly independent parts, not more. Splitting one part further only pays when its pieces are independent too.
- Set no cost or turn limits (`--max-usd`, `--max-turns`) unless the user asks for one.

## 5. Which model for which part

Tiers of the configured provider (for example `strong`, `medium`, `cheap`). Pass them with `--model strong|medium|cheap`, or use the model names with `spawn`.

| Work | Tier |
|---|---|
| Planning, splitting, merging, judging quality | `strong` (that is you, the lead) |
| Writing code, analysis, texts with judgment | `medium`, `strong` when the part is hard or risky |
| Mechanical work with a clear recipe: extract, convert, rename, collect facts, fill a template | `cheap` |
| Audit / critique with open criteria | `strong` |
| Audit with exact, checkable criteria (tests pass, fields present, format matches) | `cheap`, or a script instead of an agent |

When a check can be a script (tests, `grep`, a JSON schema), use the script. It costs no tokens.

## 6. Brief and start

A worker has **no memory of this conversation**. Everything it needs is in the brief or in files the brief names. One brief per worker, as a file `brief-<part>.md` in the run folder:

```markdown
# Part <name>
Goal: <one sentence>.
Done when: <a check the worker can run itself>.
You own: <files/folders>. Touch nothing else.
Read: <paths, not copies>.
Rules: <the few rules that matter, e.g. no git push, no network>.
Result: write it to <full path of the result file> (changed files listed there).
Progress: write partial results to the result file as you go.
Answer: only the path of your result and one sentence.
```

With `spawn`, put the brief in the `task` (or name the brief file) and start all parts of a phase in one turn. Use `lm run --detach` **only** for runs that must keep going without an open session (overnight, after you close the chat). Start every such worker of a phase before you wait for any:

```text
lm run --detach --model cheap --name <part> - < brief-<part>.md
```

- (`lm run --detach` only.) It prints the run id at once. Note it in `plan.md`.
- `-a <agent>` gives the worker an agent's role, tools and grants. Without it the worker gets the defaults.
- `--schema file.json` forces a machine-readable final answer (verdict, list of files).
- A worker cannot grant itself anything: what it may do comes from its agent's tools and the permission rules.
- For a **fixed, repeatable** fan-out (same steps every time) write a workflow (skill `ultracode`) instead of steering by hand. A lead agent is for parts that need judgment.

## 6a. Watch every worker

A worker can die silently (turn limit, crash, lost session) and no result message ever comes. Never wait blindly and never say "still running" without proof.

1. **Ask for proof of life:** workers write their partial results to the result file as they go. A file that grows is alive.
2. **Check before you talk about it:** before every status answer, look at the result files and, for detached runs, at `lm runs show <id>`.
3. **Silent = dead.** No change in the result file for 10 minutes (or past an announced estimate): look at what it left (worktree, result file, `git status`), then restart once with a sharper, smaller brief that starts where it stopped, or finish it yourself.

## 7. Collect, check, merge

For `spawn` the result message and the file it names are the result; the `lm` commands below are for detached runs.

```text
lm wait <id> <id> ... --json        # {run_id, status, exit_reason, text, cost_usd} each
lm runs show <id>                   # log tail of one run
lm runs cost --since 2h             # what the delegation cost
```

- `done` means the worker **says** it is finished, not that it is right.
- `failed`, `paused` or `budget`: read `lm runs show <id>`, then restart once with a sharper brief or do the part yourself. **Never start the same part a third time.**
- **Check every result** against the check in its brief: run the test, open the file, compare with the goal. Check the seams between parts yourself (interfaces, shared formats, consistent wording).
- **Independent audit** for high-stakes work (code that ships, texts that go to others, money, data that is hard to fix): at least **two** auditors that do not see each other's verdicts and get the goal and the result, not your reasoning. Disagreement goes to you. For low-stakes work your own check is enough.
- **Merge** is done by you, the lead: you know why the task was split. Fix small things directly; send larger gaps back as one short follow-up per part.
- Final answer to the user: per part what was done and checked, what is open, the result paths, the total cost. Short; the files hold the content.

## Mistakes to avoid

- Saying a worker still runs without having looked at its result file or run.
- Delegating a task that is one sequential chain: workers wait or redo each other's work.
- Pasting big file contents into briefs: give paths.
- Two workers on the same file: the last writer wins, work is lost.
- Workers that report long text back: your context fills up, the saving is gone.
- Trusting `done` without checking.
