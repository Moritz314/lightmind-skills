# Dry run: "Booking page for a hair salon"

Simulated. The user's answers are invented to show how each next question follows from the last answer. Shows the first 5 questions plus the state file after them. The agent speaks the user's language; this sample is in English.

---

**User:** Plan the project: a booking page for a hair salon.

**Agent (before, silent):** Searched the project folder: empty. Looked at the web for common salon software (hosted systems with commission, calendar plugins, custom build). No tech questions at the start.

### Question 1 · Goal · The actual problem

As I understand it: a salon should get appointments online. I have no picture of the salon and of the why yet.

Tell me about last Monday in the salon: how did an appointment come about, and what went wrong?

*(open, because options would push you in one direction)*

**User:** Salon with 3 chairs, 2 employees. Appointments by phone and a paper book. The owner keeps answering the phone while cutting hair. Every 5th person does not show up or cancels too late.

### Question 2 · Approach · Build or not build

Two problems: the phone interrupts, and no-shows cost money. A booking page only solves the first by itself. Before anything else, check whether this must be a custom build. Found (web, prices still to verify): there are hosted salon systems, calendar plugins and pure booking services.

A) Rent a hosted salon system - Plus: reminders, till, calendar at once. Minus: monthly fee or commission, foreign design, data with a third party.
B) Embed a booking service or plugin in the existing site - Plus: fast, cheap. Minus: little customising, rules for duration and staff often limited.
C) Build our own page - Plus: exactly the owner's flow, full control of data. Minus: effort, someone must maintain it for good (you).
D) Unconventional: no page at all. An answering machine that points to a simple online sheet where clients enter themselves - Plus: live in a day, almost free. Minus: little comfort, hardly any protection against no-shows.

Recommendation: hinges on one fact. If the owner's own look and data ownership matter, C. If both are irrelevant, B.

**User:** C. The owner wants it to look like her site, and she is afraid of commission. Her site runs on a website builder.

*(Agent notes: the builder only allows embedding by iframe or link. Checks that on the web itself instead of asking.)*

### Question 3 · Feature · How long does an appointment take?

Found: the builder can only embed or link to other sites. A custom build then works as a sub-page or sub-domain, styled to match. Feasible.

Now the core of booking. You mentioned colouring and cutting. Colouring takes 1 to 4 hours depending on hair length and colour. If that is booked wrongly, the whole afternoon stalls.

A) Fixed duration per service - Plus: simple. Minus: often wrong for colouring.
B) Client picks hair length (short, medium, long), duration follows - Plus: usually fits. Minus: owner must maintain a table.
C) Long services only as a request, owner confirms by hand - Plus: no wrong bookings. Minus: slower, more work for the owner.
D) Unconventional: client uploads a photo, owner returns duration and price, only then is it booked - Plus: best advice. Minus: laborious, a photo is extra personal data.

Recommendation: B for cutting and washing, C for colouring. Cutting is most of the volume; colouring has too many variables.

**User:** Yes, but highlights by phone only.

*(Decision recorded: B for cutting, C for colouring, highlights by phone only. "By phone only" counts as deliberately not online and goes into "Out of scope".)*

### Question 4 · Data · Who is the truth, paper or system?

You say the appointment book is paper. As soon as people book online there are two calendars, and double bookings become risk number one.

A) The system becomes the only calendar, paper goes away - Plus: clean. Minus: owner must adapt, chaos at first.
B) System plus a view on the owner's phone, paper runs in parallel for 4 weeks, phone bookings are entered by the owner - Plus: soft transition. Minus: errors possible during the 4 weeks.
C) Online booking only in released time slots, the owner fills the rest by phone - Plus: no conflict with paper. Minus: wasted capacity.
D) Unconventional: paper stays, an employee copies the online bookings over every morning - Plus: zero change. Minus: permanent work, chaos again when she is out sick.

Recommendation: B, with a fixed date from which paper is dropped. Then there is no permanent state with two truths.

**User:** B, 4 weeks. The employees need their own calendar on the phone.

*(New open items created automatically: roles and rights (do employees see only their own calendar?), sign-in on the phone, staff absence.)*

### Question 5 · No-shows · How do we reduce them?

That was your biggest money problem and we have not touched it yet. It depends on reminders and on what a cancellation costs. Privacy is directly tied to it: a phone number or mail is required, so we collect personal data.

A) Reminder by mail with a cancel link - Plus: free, privacy is simple. Minus: mails get overlooked.
B) Reminder by SMS with a cancel link - Plus: gets read. Minus: a few cents per SMS, you need a number and a provider (data processing agreement).
C) Deposit or card guarantee for long appointments - Plus: strongest effect. Minus: payment provider needed, hurdle for clients, legal questions (cancellation terms).
D) Unconventional: waiting list: whoever cancels automatically releases the slot to the waiting list - Plus: early cancellations are no loss any more. Minus: only useful with full demand.

Recommendation: A plus a simple cancel link as the base, SMS only after 4 weeks if the rate does not fall. Mail is cheap and honest to measure. Record the rate beforehand (today: about 20 %).

**User:** A and D, no SMS.

*(State after question 5: see below. The next questions come from the answers, not from a list: roles and employees, payment on site, languages, legal pages and privacy notice, hosting and who maintains it later, budget.)*

---

## State file after Q5 (`inquisition-state.md`, excerpt)

| # | Domain | Status | Decision | Next |
|---|---|---|---|---|
| 1 | Purpose, success | decided | Less phone work, lower the no-show rate from ~20 %. Measure after 8 weeks | Ask for the target number |
| 2 | Users | open | Clients, owner, 2 employees | Roles and rights |
| 3 | Scope | partly | Cutting/washing online (hair length), colouring as request only, highlights by phone only | Prices, cancellation period |
| 4 | Design | assumed | Must match the owner's existing site | Reference and colours |
| 5 | Data | decided | System is the truth, 4 weeks in parallel with paper | Backup, export |
| 6 | Integrations | open | Mail sending, maybe a calendar feed for the phone | Provider |
| 7 | Tech | open | Custom build, sub-domain next to the existing site | Compare 3 approaches |
| 8 | Security/privacy | open | Name + mail, cancel link, waiting list | Legal basis, processing agreement, retention |
| 11 | Costs | open | No commission model wanted | Budget, running costs |
| 15 | Maintenance | open | The user maintains it | Who covers an outage? |

Decision log: D1 custom build (owner's look, avoid commission). D2 hair-length table plus request for colouring. D3 system as truth, 4 weeks parallel. D4 mail + waiting list, no SMS.
Out of scope: highlights online, SMS, till.

---

## Check: does it feel like a checklist?

- The order came from the answers, not from the domain list: Q2 "build or not" came from the word "commission" in the web finding, Q3 from the colouring example, Q4 from "paper appointment book" in Q1, Q5 from the number 20 % in Q1.
- Tech (stack) deliberately did not come up yet. It depends on approach, hosting and maintenance.
- Every option had plus and minus; every round had a real unconventional idea (online sheet, photo, paper copy, waiting list). Two of them (waiting list, photo) were even partly chosen or discussed.
- Q2 had a conditional recommendation ("if X, then C, else B") because a single fact decides the choice. No recommendation is forced.
- Not out of habit: no "Next.js + Postgres + Vercel" was proposed; the stack choice comes later as an approach comparison with at least one unconventional variant (for example a small static/PHP solution on the existing web space, or a form service plus a spreadsheet).
- Weakness found: Q2 was long. In practice, cut the first finding to 2 sentences and each option to one line.
