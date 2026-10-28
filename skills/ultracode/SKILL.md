---
name: ultracode
description: Write and run workflow scripts with the built-in tool `workflow` - one Python script that orchestrates many sub-agents (agent, parallel, pipeline, phase, log, budget, nested workflows, schema answers, git worktrees, resume from the journal). Use for effort ultracode (every substantial task as a workflow), "ultracode", "use a workflow", "workflow script", fan-outs over many files or items, adversarial checks, judge panels, loop-until-dry searches.
---

# ultracode

The `workflow` tool runs a **Python script** in the core. The script holds the plan; each `agent()` is a sub-agent with the chat's rights. Its return value comes back to you as data. Your context sees only the result, not the hundreds of steps.

## When

- **Effort `ultracode`** (`/ultracode`, `/effort ultracode`, or the user writes the word `ultracode`): every substantial task goes through `workflow`. Big tasks: several workflows in a row (understand → design → build → verify); read each result, then write the next. Trivial requests and conversation: answer yourself.
- Otherwise: when a task has many similar parts (more than ~6 files, items, sources) or needs independent checking. For 2-6 parts `spawn` is enough (skill `delegation`).

## The tool

`workflow` with `script` (the code inline) or `path` (a `.py` file), `args` (JSON text, arrives as `args`), `budget` (`+500k`, `2m`: take it from the user's message, e.g. "+500k"), `resume_run_id` (`wf-3`), `background` (default true: returns at once, the result comes later as a message). Before it starts, the chat shows name, description and phases. In plan mode the tool is refused.

## Script format

```python
meta = {                                   # a pure literal: no names, no calls, no f-strings
    "name": "audit-routes",
    "description": "Check every route file for missing auth",
    "phases": [{"title": "Find", "detail": "list route files"}, {"title": "Check", "detail": "one agent per file"}],
}

async def main(args):
    phase("Find")
    found = await agent("List every route file under src/ as JSON.", label="finder", model="haiku",
                        schema={"type": "object", "properties": {"files": {"type": "array", "items": {"type": "string"}}},
                                "required": ["files"]})
    if found is None:
        return {"error": "finder failed"}
    phase("Check")
    reports = await pipeline(found["files"],
                             lambda f: agent(f"Check {f} for routes without auth. Answer: file, findings.", label=f, model="sonnet"))
    return [r for r in reports if r]
```

Rules the runtime checks before it runs (it names every line it refuses):
- `meta` at the top level, `async def main(args)`.
- **No clock, no chance**: no `time`, `datetime`, `random`, `uuid`, `calendar`, `zoneinfo`, nor the token-generating module of the standard library. Resume replays the script and must make the same calls.
- Imports only `json` (loads, dumps), `re`, `math`, `itertools`, `collections`, `functools`, `textwrap`, `string`. No `os`, no files, no shell: **agents do all work.**
- No names or attributes starting with `_`, no `.format` (use f-strings), no classes (use dicts), no `open`, `eval`, `getattr` ...
- The script's own loops are counted (1 million steps): it plans, it does not compute.

## Functions

| Call | Gives |
|---|---|
| `await agent(prompt, label=, phase=, schema=, model=, effort=, isolation=None, agent_type=)` | the agent's final text; with `schema` the checked object; `None` when it failed, was stopped or skipped |
| `await parallel([lambda: agent(...), ...])` | list of results; waits for all (a barrier); a failure is `None` |
| `await pipeline(items, stage1, stage2, ...)` | each item runs through all stages on its own, no waiting between stages; a stage gets `(value)` or `(value, item)` or `(value, item, index)`; `None` ends that item |
| `phase("title")` | groups the following agents in the display |
| `log("text")` | a line in the display and the journal |
| `await workflow("name-or-path.py", args)` | runs another script inside (one level); a name means `skills/ultracode/workflows/<name>.py` |
| `args`, `budget.total`, `budget.spent()`, `budget.remaining()` | input; token budget |

- **Prompts**: each agent sees nothing of the chat. Give a complete brief. Its final text is the value: ask for raw data or a file path, not prose.
- **schema**: the agent answers through the tool `StructuredOutput`; a wrong value is answered with the errors, then up to 3 fresh tries.
- **model**: haiku for collecting, sonnet for building and reviewing, the strong model only for judgment.
- **agent_type**: a name from `agents/`; needs the rule `spawn(<name>)` like `spawn` does. Rights stay the chat's, never the agent's own.
- **isolation="worktree"**: own git worktree on its own branch (for agents that write in parallel). The value becomes `{"value", "worktree", "branch"}`. After the run, unchanged worktrees are removed; changed ones stay: merge the branch, then `git worktree remove <path>` and `git branch -D <branch>`.

## Patterns (compose them)

```python
# adversarial verify: a finding survives only if most sceptics fail to refute it
async def verified(finding, n=3):
    votes = await parallel([lambda i=i: agent(f"Try to refute: {finding}. Answer only REFUTED or STANDS.", label=f"sceptic {i}", model="sonnet") for i in range(n)])
    return sum(1 for v in votes if v and "STANDS" in v) > n // 2

# judge panel: drafts from different directions, judged in parallel, synthesis of the winner and the best ideas
drafts = await parallel([lambda d=d: agent(f"Draft a solution for X, direction: {d}. Write it to a file, answer with the path.") for d in ("simple", "fast", "robust")])
scores = await parallel([lambda p=p: agent(f"Score the draft in {p} from 1-10 for correctness and clarity. Answer only the number.", model="sonnet") for p in drafts if p])
best = await agent(f"Drafts: {json.dumps(drafts)}. Scores: {json.dumps(scores)}. Merge the winner with the best ideas of the others into one file; answer with its path.")

# loop-until-dry: search until K rounds bring nothing new; compare against everything seen
seen, dry = set(), 0
while dry < 2:
    hits = await agent(f"Find bugs in src/ not in this list: {json.dumps(sorted(seen))}. JSON list of one-line findings.",
                       schema={"type": "array", "items": {"type": "string"}})
    new = [h for h in (hits or []) if h not in seen]
    seen.update(new)
    dry = dry + 1 if not new else 0
```

- **Perspectives**: reviewers for correctness, security, performance, reproducibility in `parallel`.
- **Multi-modal sweep**: the same question along different routes (code search, tests, logs, docs) in parallel.
- **Completeness critic**: a last agent asks "what is missing?"; its answer is the next round or the next workflow.
- **No silent caps**: whatever you leave out (too many items, a skipped part), say it with `log()`.

## Limits and machine protection

- At once: at most min(16, CPUs-2) agents. On a laptop the core allows fewer and a new agent waits while RAM is short (`workflow.*` in `config.md`). Heavy work belongs on a stronger machine.
- By default 1000 agents per run and 4096 items per `parallel`/`pipeline` (`workflow.max_agents`, `workflow.max_items`); the runtime logs every cut and gives `None` for the rest. The start note of a workflow (`limits: ...`) shows the values that apply.
- `budget` is a hard limit: past it, running agents are stopped and further ones give `None`. Without a `budget` in the call or the script, `workflow.budget` of `config.md` applies (none by default).

## Journal and resume

Each run writes `runs/<run>/workflow/<wf-id>/` with `journal.jsonl` (every agent call with its result), `script.py`, `args.json`, `result.json`. After a failure or a stop: call `workflow` again with `resume_run_id="wf-3"` (script and args may be left out: the old ones are used). Agents that ended well come from the journal until the first changed or failed call; from there everything runs live.

## `/ultracode` and the settings

- `/ultracode` (or `/ultracode on`) turns the level on for this chat, `/ultracode off` goes back to the effort the chat had before, `/ultracode status` lists the state and the settings that apply. `/effort ultracode` does the same as `on`. This skill is reachable as `/skill ultracode`; the command name belongs to the switch.
- Settings live in `/config` (page **Ultracode**) or in the `workflow:` section of `config.md`: `max_parallel`, `laptop_parallel`, `agent_memory_mb`, `free_memory_mb` (CPU and RAM); `max_agents` (1000), `max_items` (4096), `budget` (tokens per workflow, empty = none); `model` and `effort` of the workflow agents (empty = as `spawn` / the chat; an `agent()` call or an agent file with its own value wins); `schema_retries` (3); `skeptics` (3) and `dry_rounds` (2), which the patterns above state as N sceptics and K empty rounds: use exactly those numbers in your patterns; `tidy_worktrees` (yes: an unchanged worktree is removed at the end); `confirm`, `keyword`.
