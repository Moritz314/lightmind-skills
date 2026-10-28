# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6.0"]
# ///
"""Install the cron triggers of triggers/*.md into the OS scheduler.

    uv run apply.py [--tree DIR] [--dry-run]     install (idempotent; replaces what it installed before)
    uv run apply.py --list                       triggers in the folder and what is installed
    uv run apply.py --remove [NAME]              remove all of them, or one

Linux: a block in the user crontab between `# lightmind triggers` and `# end lightmind triggers`.
Windows: scheduled tasks named `Lightmind <name>`.  Each trigger runs
in the tree root: `lm run --detach -a <agent> "<task>"` (`lm` must be on PATH, or give --lm).
Windows: a small wrapper file `triggers/.run/<name>.cmd` holds the command, so the task needs no quoting trick.
"""
import argparse
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

import yaml

BEGIN = "# lightmind triggers"
END = "# end lightmind triggers"
PREFIX = "Lightmind "
DAYS = {"0": "SUN", "1": "MON", "2": "TUE", "3": "WED", "4": "THU", "5": "FRI", "6": "SAT", "7": "SUN"}


def load_triggers(folder: Path) -> list[dict]:
    """Enabled-or-not triggers of the folder: name, schedule (5-field cron), agent, task, enabled, error."""
    out = []
    for f in sorted(folder.glob("*.md")):
        if f.name.startswith("_") or f.name.lower() == "readme.md":
            continue
        m = re.match(r"---\s*\n(.*?)\n---", f.read_text(encoding="utf-8"), re.S)
        try:
            fm = yaml.safe_load(m.group(1)) if m else None
        except yaml.YAMLError:
            fm = None
        t = {"name": f.stem, "schedule": "", "agent": "", "task": "", "enabled": False, "error": ""}
        if not isinstance(fm, dict):
            t["error"] = "no frontmatter"
            out.append(t)
            continue
        sched = str(fm.get("schedule") or "")
        when = str(fm.get("when") or "")
        if not sched and when.startswith("cron "):
            sched = when[5:]
        t.update(name=str(fm.get("name") or f.stem), schedule=sched.strip(), agent=str(fm.get("agent") or ""),
                 task=str(fm.get("task") or ""), enabled=fm.get("enabled", True) is not False)
        if not t["schedule"]:
            t["error"] = "no cron schedule (only cron triggers are installed here)"
        elif len(t["schedule"].split()) != 5:
            t["error"] = f"cron needs 5 fields: {t['schedule']!r}"
        elif not t["agent"] or not t["task"]:
            t["error"] = "agent and task are required"
        elif not re.fullmatch(r"[A-Za-z0-9._-]{1,64}", t["name"]) or not re.fullmatch(r"[A-Za-z0-9._-]{1,64}", t["agent"]):
            t["error"] = "name and agent may only hold letters, digits, . _ -"      # they end up in crontab / schtasks
        elif not all(re.fullmatch(r"[0-9*/,-]+", x) for x in t["schedule"].split()):
            t["error"] = f"cron fields may only hold digits * / , -: {t['schedule']!r}"
        elif any(c in t["task"] for c in "\r\n\x00%"):
            t["error"] = "task must be one line without % (crontab treats % and newlines specially)"
        out.append(t)
    return out


LM_BIN = "lm"        # overridden by --lm


def lm_command(tree: Path, t: dict, windows: bool = False) -> list[str]:
    """The `lm run` command line of one trigger (the caller changes into the tree root first)."""
    return [LM_BIN, "run", "--detach", "-a", t["agent"], t["task"]]


def render_block(tree: Path, triggers: list[dict]) -> str:
    lines = [BEGIN]
    for t in triggers:
        cmd = "cd " + shlex.quote(str(tree)) + " && " + " ".join(shlex.quote(a) for a in lm_command(tree, t))
        cmd = cmd.replace("%", "\\%")
        lines.append(f"# {t['name']}")
        lines.append(f"{t['schedule']} {cmd}")
    lines.append(END)
    return "\n".join(lines) + "\n"


def merge_crontab(existing: str, block: str | None) -> str:
    """Replace (or drop, block=None) the marked block; the rest of the crontab stays untouched."""
    pat = re.compile(rf"^{re.escape(BEGIN)}\n.*?^{re.escape(END)}\n?", re.S | re.M)
    rest = pat.sub("", existing).rstrip("\n")
    parts = [p for p in (rest, (block or "").rstrip("\n")) if p]
    return "\n".join(parts) + "\n" if parts else ""


def schtasks_args(tree: Path, t: dict, write: bool = True) -> list[str]:
    """schtasks /Create arguments for a cron schedule (daily, weekly, monthly, hourly, every N minutes)."""
    mi, h, dom, mon, dow = t["schedule"].split()
    wrapper = tree / "triggers" / ".run" / f"{t['name']}.cmd"
    line = subprocess.list2cmdline(lm_command(tree, {**t, "task": t["task"].replace('"', "'")}, True))
    if write:
        wrapper.parent.mkdir(parents=True, exist_ok=True)
        wrapper.write_text(f'@echo off\r\ncd /d "{tree}"\r\n{line}\r\n', encoding="utf-8")
    tr = f'"{wrapper}"'
    base = ["schtasks", "/Create", "/F", "/TN", PREFIX + t["name"], "/TR", tr]
    if mon != "*":
        raise ValueError("a month field is not supported on Windows")
    if mi.startswith("*/") and (h, dom, dow) == ("*", "*", "*") and mi[2:].isdigit():
        return base + ["/SC", "MINUTE", "/MO", mi[2:]]
    if not mi.isdigit() or not 0 <= int(mi) <= 59:
        raise ValueError(f"unsupported minute field {mi!r}")
    if h == "*" and (dom, dow) == ("*", "*"):
        return base + ["/SC", "HOURLY", "/ST", f"00:{int(mi):02d}"]
    if not h.isdigit() or not 0 <= int(h) <= 23:
        raise ValueError(f"unsupported hour field {h!r}")
    st = ["/ST", f"{int(h):02d}:{int(mi):02d}"]
    if (dom, dow) == ("*", "*"):
        return base + ["/SC", "DAILY"] + st
    if dom == "*":
        days = []
        for part in dow.split(","):
            a, _, b = part.partition("-")
            if not a.isdigit() or (b and not b.isdigit()) or int(b or a) > 7:
                raise ValueError(f"unsupported day-of-week {dow!r}")
            days += [DAYS[str(i)] for i in range(int(a), int(b or a) + 1)]
        return base + ["/SC", "WEEKLY", "/D", ",".join(dict.fromkeys(days))] + st
    if dow == "*" and dom.isdigit() and 1 <= int(dom) <= 31:
        return base + ["/SC", "MONTHLY", "/D", dom] + st
    raise ValueError(f"unsupported schedule {t['schedule']!r}")


def _run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def installed_windows() -> list[str]:
    r = _run(["schtasks", "/Query", "/FO", "CSV", "/NH"])
    names = [row.split('","')[0].strip('"\\ ') for row in r.stdout.splitlines()]
    return [n for n in names if n.startswith(PREFIX)]


def read_crontab() -> str:
    r = _run(["crontab", "-l"])
    return r.stdout if r.returncode == 0 else ""


def write_crontab(text: str) -> None:
    r = subprocess.run(["crontab", "-"], input=text, text=True, capture_output=True)
    if r.returncode:
        raise RuntimeError(r.stderr.strip() or "crontab failed")


def default_tree() -> Path:
    """The tree root: $LIGHTMIND_HOME, else the current folder."""
    return Path(os.environ.get("LIGHTMIND_HOME") or Path.cwd())


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--tree", type=Path, default=None, help="tree root (default $LIGHTMIND_HOME or the current folder)")
    ap.add_argument("--lm", default="lm", help="the lm command to put into the schedule (default: lm from PATH)")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--remove", nargs="?", const="*", metavar="NAME")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    global LM_BIN
    LM_BIN = a.lm
    tree = (a.tree or default_tree()).resolve()
    win = os.name == "nt"
    trig = load_triggers(tree / "triggers")
    if a.list:
        have = installed_windows() if win else [l[2:] for l in read_crontab().splitlines()
                                                if l.startswith("# ") and not l.startswith("# lightmind")
                                                and not l.startswith("# end lightmind")]
        for t in trig:
            on = (PREFIX + t["name"] in have) if win else (t["name"] in have)
            print(f"{t['name']:<20} {t['schedule'] or '-':<16} agent={t['agent'] or '-':<14} "
                  f"{'enabled' if t['enabled'] else 'disabled':<9} {'installed' if on else 'not installed'}"
                  f"{'  ERROR: ' + t['error'] if t['error'] else ''}")
        return 0
    if a.remove:
        if win:
            targets = installed_windows() if a.remove == "*" else [PREFIX + a.remove]
            for n in targets:
                print(f"{'would delete' if a.dry_run else 'delete'}: {n}")
                if not a.dry_run:
                    _run(["schtasks", "/Delete", "/F", "/TN", n])
        elif a.remove == "*":
            print("remove crontab block")
            if not a.dry_run:
                write_crontab(merge_crontab(read_crontab(), None))
        else:
            keep = [t for t in trig if t["enabled"] and not t["error"] and t["name"] != a.remove]
            print(f"reinstall block without {a.remove}")
            if not a.dry_run:
                write_crontab(merge_crontab(read_crontab(), render_block(tree, keep) if keep else None))
        return 0
    good = [t for t in trig if t["enabled"] and not t["error"]]
    for t in trig:
        if t["enabled"] and t["error"]:
            print(f"skip {t['name']}: {t['error']}", file=sys.stderr)
    if win:
        wanted = {PREFIX + t["name"] for t in good}
        for t in good:
            try:
                cmd = schtasks_args(tree, t, write=not a.dry_run)
            except ValueError as e:
                print(f"skip {t['name']}: {e}", file=sys.stderr)
                continue
            print(("would run: " if a.dry_run else "run: ") + subprocess.list2cmdline(cmd))
            if not a.dry_run:
                r = _run(cmd)
                if r.returncode:
                    print(f"failed {t['name']}: {r.stderr.strip()}", file=sys.stderr)
        for n in installed_windows():
            if n not in wanted:
                print(f"{'would delete' if a.dry_run else 'delete'} stale: {n}")
                if not a.dry_run:
                    _run(["schtasks", "/Delete", "/F", "/TN", n])
    else:
        new = merge_crontab(read_crontab(), render_block(tree, good) if good else None)
        print(new if a.dry_run else f"installed {len(good)} trigger(s) in the user crontab")
        if not a.dry_run:
            write_crontab(new)
    return 0


if __name__ == "__main__":
    sys.exit(main())
