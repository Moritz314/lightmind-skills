# Domains and question banks

Inspiration, not a script. Pick the domains that matter for this project, add your own, skip the rest with a reason. The questions below are *seeds*: rewrite each into a specific question for this project, with options. Mark the typical risk level (H/M/L) only as a start; the real risk comes from this project.

Order is not fixed. Usually first: 1, 2, 3. Then whatever is riskiest. Dependencies: tech choices (7-9) come after scope and constraints (1-6, 17).

## 1. Purpose, goals, success (H)
- What is the real problem? What happens if we do nothing?
- Why now? What changed?
- Who benefits, who pays, who decides?
- How do we know in 3 / 12 months it worked? Number, date, observable event.
- What would make it a failure even if technically perfect (anti-goals)?
- Is software even the right answer? Cheaper non-software way? Buy, rent, reuse?
- What is the smallest version that proves the idea?

## 2. Users and stakeholders (H)
- Who exactly uses it (roles, count, tech skill, device, language, age, disabilities)?
- Who admins/operates it? Who supports users?
- Who else is affected without using it (staff, customers, regulators)?
- What do they do today instead? What do they love and hate about it?
- Conflicts between roles (owner vs. staff vs. customer)?
- Can the user talk to 2-3 real users first?

## 3. Scope and features (H)
- Core flows as scenes: start, steps, end, what can go wrong.
- Must / should / could / will-not for the first version.
- What is explicitly out of scope, now and ever?
- Which feature is the reason people come? Which are decoration?
- Manual first: what can be done by hand for the first 20 users?
- Edge cases: cancel, change, double entry, no-show, empty state, error, offline.
- Time dimension: seasons, deadlines, recurring things, time zones.

## 4. Design and UX (M)
- Look and feel: reference sites/apps loved or hated? Brand, logo, colors, tone, fonts?
- Mobile first or desktop first? Which device do users really hold?
- Information structure: pages/screens, navigation, the one primary action per screen.
- Accessibility level (WCAG AA?), languages, reading level, dark mode.
- Content: who writes texts and images? Real content or placeholders at launch?
- Emotion: what should the user feel in the first 10 seconds?
- Prototype or sketch before build? Which screens need one?
- Unconventional: conversation instead of forms, one-page, no-UI (mail/WhatsApp/phone), print.

## 5. Data (M-H)
- Entities, relations, ids, lifecycle, what is the source of truth?
- Volume now and in 3 years; growth shape (steady, spikes).
- Where does data come from (import, manual, sync) and who may change it?
- History/audit: what must be kept, what must be deletable?
- Migration from existing data (Excel, old system, paper)? Quality of that data?
- Backups, export, portability, ownership. Can the user or a client leave with the data?
- Analytics: which questions will be asked of the data?

## 6. Integrations and dependencies (M-H)
- Existing systems that must connect (calendar, accounting, CRM, payment, mail/SMS, maps, auth).
- For each: API quality, price, limits, failure mode, lock-in, alternative, "what if it disappears?".
- Build vs. buy vs. open source per component.
- Import/export formats, webhooks, who else consumes our data?
- Third-party scripts on the site (tracking, fonts, chat): needed?

## 7. Architecture and tech (M)
- Constraints first: team skills, existing infra, who maintains it, expected lifetime.
- Candidate approaches (at least 3, one unconventional): custom code, low-code/no-code, SaaS + glue, static site + small functions, existing CMS/plugin, spreadsheet + automation.
- Monolith or parts? Sync or async? Realtime needed?
- Language, framework, database: choose from needs, not habit. State the rejected ones and why.
- Dependency health: maintained, license, bus factor, size.
- Environments (dev, staging, prod), config, secrets handling.
- AI/LLM parts: really needed? Cost per use, privacy, fallbacks, evaluation.

## 8. Security and privacy, data protection law (H)
- Data classes: public, personal, special category (health!), payment, secrets.
- Legal basis per data type (Vertrag, Einwilligung, berechtigtes Interesse), purpose limitation, minimization.
- Auth: who logs in, how (password, magic link, SSO, passkey), roles and permissions, session handling.
- Threats: abuse (spam bookings, scraping, fake accounts), injection, takeover, insider, lost device.
- Processors (data processing agreement needed?), hosting country, transfers outside EU, sub-processors.
- Retention and deletion, right of access/erasure workflow, consent storage, cookie/tracking approach (none is an option).
- Logging without personal data; breach plan (72 h notice): who does what?
- Payment: PCI scope (use hosted checkout), refunds.
- Secrets and keys: where, rotation, who sees them.

## 9. Performance, scale, reliability (M)
- Real numbers: concurrent users, requests, data size, peak days.
- Targets: page load, response time, availability (is 99% fine? downtime cost per hour?).
- Degradation: what still works when part X is down? Offline?
- Capacity plan and cost at 1x / 10x. Where is the first bottleneck?
- Caching, CDN, images/video weight, SEO needs (Core Web Vitals).

## 10. Hosting and operations (M)
- Where does it run (own server, private network, managed, serverless, SaaS), why this and not others?
- Deploy: how, how often, rollback, zero-downtime needed?
- Monitoring, alerts, logs: who gets woken, when?
- Backups and restore test; disaster plan; RPO/RTO in words.
- Domain, DNS, mail deliverability (SPF/DKIM), certificates, renewals.
- Updates and patching; who owns it at 3 a.m.?

## 11. Costs and budget (H)
- Build budget (money and hours), run cost per month, per-use cost (SMS, AI, payment fees).
- Who pays, when does it pay back? Pricing model if it is a product.
- Where can cost explode (usage-based services)? Caps and alarms.
- Cheapest version that still reaches the goal? Cost of delay?
- Hidden: licenses, domains, design, content, support time, legal review.

## 12. Legal and compliance (H)
- Duties that apply where the product runs and where its users live: legal notice / imprint, privacy policy, terms and conditions, right of withdrawal, price display, cookie and tracking rules, accessibility law.
- Industry rules (health, finance, kids, alcohol, regulated trades).
- Contracts: with customer, freelancers, processors; IP and licenses of used assets, fonts, images, code.
- Liability: what if it fails or leaks? Insurance?
- Who checks legal? Needed before launch or after?

## 13. Testing and quality (M)
- What must never break (critical paths)? Test at which level (manual script, automated, load, security)?
- Test data and test accounts, real-user trial (pilot), acceptance by whom.
- Definition of done per feature.
- Browser/device matrix; accessibility check; content proofreading.

## 14. Rollout and change (M)
- Big bang, pilot group, parallel run, soft launch? Fallback to old way?
- Training, docs, announcement; who tells the users?
- Data cut-over date; freeze periods; support in the first weeks.
- Migration of existing users and links (redirects, SEO).

## 15. Maintenance, ownership, lifecycle (M)
- Who owns it after launch: fixes, content, updates, user support, budget? Handover docs.
- Expected lifetime; what is the exit plan (shut down, replace, export)?
- Dependency updates, security patches, expiring tokens/certificates.
- Documentation level; bus factor.
- Evolution: what comes in phase 2, which choices today keep it cheap?

## 16. Risks and unknowns (H)
- Pre-mortem: "In 6 months it failed. Why?" Collect 5, rank.
- Biggest technical unknown: can a spike answer it in a day?
- Biggest people risk (adoption, key person, stakeholder who says no later).
- External risk (API changes, law, platform rules, vendor price changes).
- Assumptions list: which one, if wrong, kills the plan?

## 17. Constraints and context (H)
- Deadline and why; fixed dates (event, season, law).
- Team and capacity: who builds, how many hours per week, what skills?
- Tools/platforms that are mandatory or forbidden. Existing brand/infra.
- Political/organisational: who must approve, who may block?
- The user's own preferences and taboos (state as preferences, not as laws; test them once).

## 18. Success measurement and feedback (M)
- Metrics and where they come from (without breaking privacy).
- Review date; what result means continue, change, stop?
- Feedback channel from users; how decisions come from it.

## Extra domains (add per project as needed)
- Marketing / acquisition / SEO / launch story
- Content and editorial workflow, translation
- Community / moderation / trust and safety
- Hardware, physical setting, printing, logistics
- Support processes, SLAs, escalation
- Sustainability, energy, device lifespan
- Accessibility beyond web (phone, in-person)
- Internationalisation, currencies, tax (VAT, OSS)
- AI governance (data sent to models, evaluation, human review)
- Partnerships, reseller, white-label
- Offline, kiosk, embedded constraints
- Ethics: dark patterns, addictive design, exclusion

## Unknown-unknown prompts (use at the end, pick 3-5)
- Who will be annoyed by this, and what will they do?
- What will we wish we had logged/recorded from day one?
- What is the first thing that will be abused?
- What breaks on the first public holiday, leap day, or time change?
- What if the main user is on a bad phone with bad network?
- What did a comparable project (name 2) regret?
- What happens to the data if this project stops tomorrow?
- Which decision here is hard to undo, and have we really decided it?

## Fresh-alternatives routine (before each option set)
1. List the *need*, not the solution.
2. Write 3 solutions without looking at what was used before.
3. Add one that removes the need, shrinks it, or hands it to someone else/something existing.
4. Only then compare with past solutions, and keep them only if they win on this project's facts.
