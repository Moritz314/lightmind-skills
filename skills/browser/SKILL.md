---
name: browser
description: Read a web page, take a screenshot of it, or log in, click and fill forms in a real local browser (Playwright). Use for any task on a website, when plain fetching is not enough (JavaScript, logins), or when the user says "look at this page", "open the site", "screenshot the page".
---

# browser

Script: `skills/browser/scripts/browser.py`. It drives a local Chromium (or your installed Chrome) with [Playwright](https://playwright.dev/). Nothing leaves your machine except the page requests themselves; no account and no paid service is needed.

## Requirements

- Python 3.11+ and [`uv`](https://docs.astral.sh/uv/), which installs the `playwright` package on the first run (the script declares it inline).
- A browser: if Chrome is installed it is used, otherwise the script runs `python -m playwright install chromium` once on first use (needs network and about a minute).

## Calls

```bash
uv run skills/browser/scripts/browser.py open https://example.com
uv run skills/browser/scripts/browser.py open URL --format text --profile shop --headed
uv run skills/browser/scripts/browser.py screenshot URL --full --out shot.png
uv run skills/browser/scripts/browser.py open URL --steps '[{"fill":["#user","name"]},{"click":"button[type=submit]"},{"wait":1000}]'
```

- `open` prints `# <title>`, the final URL and the page as markdown (`--format md`, default) or plain text (`--format text`).
- `screenshot` prints the path of the PNG (default `shot-<time>.png` in `$LIGHTMIND_RUN_DIR`, else `out/`). Then look at the picture.
- `--steps` is a JSON list (or `@file.json`), run in order after the page loaded. One action per step: `{"goto": url}`, `{"click": selector}`, `{"fill": [selector, text]}`, `{"press": "Enter"}`, `{"wait": ms-or-selector}`, `{"scroll": pixels}`. A bad list exits with code `2` before a browser starts.
- Headless by default; `--headed` shows the window.
- Exit code `0` on success, `1` on a browser or page error.

## How to work

1. Read a page: `open <url>`. Start here; most tasks need nothing more.
2. See a page: `screenshot <url> --full`, then open the PNG.
3. Click through or log in: inspect with `open` first to find the selectors, then add `--steps`.
4. Keep a login: use the same `--profile <name>` every time (one profile per site or account). Profiles are stored in `~/.lightmind-browsers/profiles/<name>` (change the base with `LIGHTMIND_BROWSER_PROFILES`). For a first login that needs a human (captcha, 2FA) run with `--headed` and let the user log in by hand.
5. Never put a password or token into a command in plain text; take it from an environment variable and build the JSON in the shell.
6. Ask the user before anything that sends, buys or deletes on a site.
7. Respect the site: no mass scraping, no bypassing of paywalls or logins you have no right to.
