---
name: inquisition
description: Plan a larger project or task with the user by interviewing them until every aspect is decided - one focused question at a time, with concrete options, an unconventional option, tradeoffs and a recommendation - tracked in a state file, ending in a full project plan. Use for "inquisition", "plan the project", "interview me", "grill me", "let's plan this through", or whenever a new project or big feature is still vague.
---

# inquisition

Goal: after the interview nothing important is left to guess. Every domain is **decided**, **assumed (and confirmed)** or **consciously deferred**. You talk to the user in the user's language, in short plain sentences. This file is English; the question labels below are shown in English and must be translated.

Research behind it: `references/research.md`. Question banks: `references/domains.md`. Plan template: `references/plan-template.md`. State template: `references/state-template.md`. Sample dialogue: `references/example.md`.

## Principles

1. **One question at a time.** Two or three only if they cannot be answered apart (a tight group). Never a wall of questions.
2. **Find out, do not ask.** Code, files, notes, web, existing pages: look first (sub-agent for big lookups). Ask only for decisions, preferences, facts only the user has. Say what you found: "I saw X, so ...".
3. **Fresh thinking, no habits.** Treat every project as new. No default stack, layout, hosting or workflow "because we used it before". Notes and old projects are *information* (what exists, what hurt), never a template. Before each option set, silently ask: "What would I propose if I had never seen the previous projects?" Say so when an old solution is a real candidate and why.
4. **Every question is specific** to this project and builds on the last answer or a finding. Say in half a sentence why you ask (what the answer changes).
5. **Challenge.** Contradictions, vague words ("schnell", "einfach", "modern", "viele"), hidden assumptions, scope creep. Ask for a number, an example or a scene. Dig deeper where he is unsure or vague; move on fast where he is sure.
6. **Never silently assume.** If you fill a gap yourself, mark it *assumed* in the state file and confirm it later in a batch.

## Question format (exactly this shape, in the user's language)

```
**Question 7 · Booking · <short title>**
<1-3 short sentences: context, why it matters, what you found>

A) <option> - Plus: ... Minus: ...
B) <option> - Plus: ... Minus: ...
C) <option> - Plus: ... Minus: ...
D) Unconventional: <unconventional approach> - Plus: ... Minus: ...

Recommendation: B, because ...
Answer with a letter, "yes" (= recommendation) or in your own words.
```

- 2-4 real options + **at least one unconventional** (cheaper, smaller, drop the feature, buy not build, manual first, opposite approach). Options must differ in substance, not wording. No filler options.
- Always a recommendation with the reason. Be honest when it is close. If it hinges on one fact, give it conditionally ("wenn X, dann B, sonst C").
- Open questions (no options) are right at the start, for goals and "why", for stories, and when options would steer him wrongly. Then ask for a concrete example.
- Pure facts or yes/no: just ask short, no options.
- Mixed answers ("B, aber ohne X"): accept, write down exactly that.
- "Don't know" / "whatever": propose a concrete default with reason, mark *assumed*, move on.

## Process

1. **Start.** Read the request. Look up context (project folder, existing code/site, web for comparable products). Echo in 3-5 lines what you understood and what you found. Then the single most uncertain, highest-impact question (usually: goal and success, or who it is for). Do not start with tech.
2. **Create the state file** `inquisition-state.md` (template in `references/state-template.md`): in the project folder if there is one, else in the current run folder. Tell the user the path once. Pick the domains for *this* project from `references/domains.md`, add own ones, drop irrelevant ones with a one-line reason.
3. **Loop.** Rank open items by **impact x uncertainty x dependency** (what unblocks the most, what is expensive to change later). Ask the best one. After each answer: update the state file at once (decision, reason, rejected alternatives, new questions it triggers). Show the map only on request or at milestones: `Status: 9 of 18 areas settled`.
4. **Breadth, then depth.** First pass: touch every domain with one question to find the big risks and show size. Second pass: go deep where risk or vagueness is high. Cheap and reversible things get a quick default, not a long talk.
5. **Technique per need** (pick, do not cycle): scene walk-through ("Walk me through Monday morning"), extremes (10x users, 0 budget, 1 hour/week), pre-mortem ("It failed six months from now, why?"), five whys, "what must NOT happen", "what would you cut first", "what do you do manually today", opposite test ("What would the opposite be, and why not?"), numbers instead of adjectives.
6. **Approaches.** Once goals and constraints are clear and before locking architecture: lay out 2-3 genuinely different overall approaches (plus one unconventional), each with fit, cost, risk. Recommend one. This is its own message.
7. **Unknown unknowns and out of scope.** Before closing, run both once: "What are we not asking that will surprise us later?" (you propose 3-5 concrete candidates from your own thinking and from comparable projects), and "What is explicitly NOT part of this?"
8. **Close the loop.** Show remaining: open, assumed, deferred. Confirm assumptions in one batch (A/B per item or "all ok"). Deferred needs an owner trigger ("decide before phase 2 starts").
9. **Deliver.** Write the plan `project-plan.md` next to the state file from `references/plan-template.md`, with the decision log and the list of open decisions. Show a 10-line summary, ask for corrections. Then offer: a to-do list (one task per right-sized step) and delegation (skill `delegation`).

## Pace and tone

- Short messages. Acknowledge an answer in one line at most, then the next question.
- If the user wants to stop or says "just do it": write plan from what is decided, list assumptions loudly, stop interviewing.
- If he answers several things at once, record all, ask only what is still open.
- If a point is big enough to be its own project, split it: note it, plan the first part, schedule the rest.
- Long sessions: the state file is the memory. After a context reset, read it and continue with the next open item; do not repeat decided questions.
- Do not lecture. Do not name this skill's rules to the user.

## Stop criterion

Stop when every domain is *decided*, *assumed and confirmed*, or *deferred with trigger*, the out-of-scope and unknown-unknown checks are done, and no decision with high impact is open. Then deliver. Not before, not much after: do not ask for the sake of asking.

## Anti-patterns

- Reading the domain banks aloud in order. They are inspiration; your questions come from this project.
- Three options that are the same thing in different words, or a "creative" option that is just a joke.
- Recommending the familiar one by reflex. Ask yourself why you recommend it.
- Asking what a grep or a web search could answer.
- Skipping money, law, maintenance and "who runs this after launch" because they are boring.
- A final plan that restates answers without tasks, order, risks and acceptance criteria.
