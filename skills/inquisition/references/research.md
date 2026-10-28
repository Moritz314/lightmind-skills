# Research: comparable interview / planning skills

Checked 2026-10-22 on GitHub (raw files read, stars from the GitHub API that day). What I could not open is marked.

## Summary table

| Source | Stars | Style | Strong | Weak |
|---|---|---|---|---|
| mattpocock/skills `grilling` (`grill-me`, `grill-with-docs`) | ~300k | Design tree, rounds of the whole "frontier", each question with a recommended answer | Dependency-aware (ask only what is unblocked), "yes accepts the recommendation", facts are found by the agent not asked, stop = frontier empty and nothing silently assumed, docs (ADR, glossary) grow while grilling | No coverage map or domain list, so gaps are only found if the model thinks of them. Batches of numbered questions overwhelm. No persistent state file. No fixed output spec. No push for fresh alternatives. |
| RobMitt/grill-me-skill | ~1k | One question at a time via AskUserQuestion popup, 2-4 concrete options, "Other" always possible | Low load per turn, options are realistic answers, explore code instead of asking, summary at the end | No recommendation, no tradeoffs, no state, no taxonomy; ends with "concise summary" only. Needs a popup tool. |
| obra/superpowers `brainstorming` | ~300k | One question per message, open first, Socratic, specific to the project, plays back, recon offers | Excellent rules: "look before you ask", echo the request, say why you ask, ground to cover = territory not script, anti-goals, "lay out the approaches" (2-3 real alternatives, recommend one), size the work, written design + approval gate | Open questions only, no options per question; no coverage tracking; no explicit domain depth (security, ops, cost); lead-in text is long. |
| obra/superpowers `writing-plans` | (same repo) | Turns an approved spec into tasks | File structure first, task right-sizing (smallest unit with its own test cycle), scope check "split into sub-projects" | Starts after the spec; not an interview. We borrow: scope check and right-sized tasks for the hand-off. |
| github/spec-kit `/clarify` (+ `/specify`) | ~142k | Max 5 questions, strictly sequential, taxonomy scan with Clear/Partial/Missing, queue ranked by Impact x Uncertainty | The best coverage idea: a taxonomy (scope, data model, UX, non-functional, integration, edge cases, constraints, terminology, completion signals), recommendation on top with reasoning, table of options, "yes" shortcut, answers written back into the spec after each question, deferred list with reason | Hard cap of 5 questions is too small for a big project; only clarifies an existing spec (does not create from nothing); taxonomy is software-feature oriented (no budget, legal, rollout, maintenance); options only 2-5 "mutually exclusive", no creative option. |
| bmad-code-org/BMAD-METHOD (analyst, PM, `advanced-elicitation`, `brainstorming`) | ~54k | Persona agents, product brief -> PRD, elicitation method library (`methods.csv`: pre-mortem, first principles, red team, ...) | Method library to re-attack an answer from another angle; staged documents (brief, PRD, architecture); facilitation personas | Heavy ceremony, many files, document-first; easy to produce long PRDs nobody reads; methods chosen from a list rather than by need. |
| anthropics/skills (reference repo, ~183k) | - | Defines the skill format (lean SKILL.md, details in references) | Progressive disclosure, description with triggers | No interview skill of its own that I found. |
| Sorbh/interview-me, phong-baruby/ba-skills, senu-nk/project-manager, Ryan-Yongjoon-Lee/interview-with-ryan | 57 / 10 / 2 / 1 | "Interview like a senior architect", gated resumable interview adapting depth, "never invents requirements: unknowns become Open Questions", aggressive assumption challenge | Good ideas: resumable gates, unknowns tracked as open questions tied to the affected parts, adversarial mode | Small, untested; only skimmed descriptions (README text via GitHub search API), not read in full. |

## What to take, what to avoid

Take:
- Grilling: decision tree / dependencies, facts are the agent's job, "nothing silently assumed", yes = accept.
- Brainstorming: look before you ask, say why you ask, Socratic and specific, anti-goals, lay out approaches with a recommendation, scope check, approval before building.
- Spec-kit: coverage taxonomy with status, Impact x Uncertainty ranking, answers written back immediately, deferred list with reason.
- BMAD: re-attack technique library (pre-mortem etc.), kept short, chosen by need.
- Small skills: unknowns as tracked open questions; resumable state.

Avoid:
- Fixed question caps (5) and fixed batches of many questions.
- Open-only questions (slow) and options-without-tradeoffs (shallow).
- Checklist feel: question banks read out in order.
- Default stack / default design by habit. None of the sources forces fresh alternatives; this is our main addition.
- Ceremony: many documents. One state file, one final plan.

## Our additions (what none of them has)

1. Fresh-alternatives rule: every option set contains at least one unconventional approach, and a "pattern break check" against habit.
2. Persistent state file with open / decided / assumed / deferred per domain, survives resets.
3. Wide taxonomy including budget, legal, data protection, ops, rollout, maintenance, exit, risks, plus per-project extra domains.
4. Tight question format: options with tradeoffs, recommendation, letter answer, one question at a time.
5. Unknown-unknowns and out-of-scope questions as a required step, not a hope.
6. Hand-off to to-dos / delegation with right-sized tasks.

## Sources

- https://github.com/mattpocock/skills (skills/productivity/grill-me, skills/productivity/grilling, skills/engineering/grill-with-docs)
- https://github.com/RobMitt/grill-me-skill
- https://github.com/obra/superpowers (skills/brainstorming/SKILL.md, skills/writing-plans/SKILL.md)
- https://github.com/github/spec-kit (templates/commands/clarify.md, specify.md; specify.md only skimmed)
- https://github.com/bmad-code-org/BMAD-METHOD (skills/bmad-agent-analyst, bmad-advanced-elicitation, bmad-brainstorming; found by file tree, not read in full)
- https://github.com/anthropics/skills
- https://github.com/Sorbh/interview-me, https://github.com/phong-baruby/ba-skills, https://github.com/senu-nk/project-manager, https://github.com/Ryan-Yongjoon-Lee/interview-with-ryan (descriptions only)
