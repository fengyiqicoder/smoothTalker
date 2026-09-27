# SmoothTalker backlog and iteration log

This file is the shared memory for the autonomous improvement loop. Each run reads it, picks the top unchecked items it can finish, does them, ticks them off, appends a log line, and pushes. Keep it short.

## Rules for every iteration
- Content quality beats count. One excellent playbook beats three thin ones.
- Every change passes `python3 scripts/lint.py` and `python3 scripts/build_index.py`; commit `data/` with the content.
- `build_index.py` keeps the entry counts and the all.json size in `index.html`, `openapi.json`, `MUSE_PROMPT.md` and `skill/SKILL.md` in sync; commit what it changes. Never edit `SUBMISSION.md`'s submitted text; it records what was sent on 2026-09-25.
- Never change the shape of `data/*.json` fields or the OpenAPI paths (agents depend on them).
- No em-dashes anywhere in content. No manipulative or deceptive advice, ever.
- Push to the working branch only; a human merges to `main` (the live site).
- Size budget: agents load `all.json` whole, so every entry costs context for every user. `build_index.py` warns above 450 KB and fails above 600 KB. Near the budget, merge overlapping entries, trim padding and improve quality instead of adding. Growth past the budget needs the index-first retrieval item below first.
- Items marked "claimed" are being done by another session; skip them.
- Quality pass: every sixth loop run (count the "loop run" lines in the Log), add nothing. Instead pick 5 existing entries at random, compare each with the quality bar (examples specific and short, structure followed in order, no padding, recovery section useful) and tighten them. Log what changed.
- Routing: after adding an entry that overlaps an existing one, or changing titles, summaries or triggers, run the model routing check in `eval/README.md` and fix any confusion it finds (split the entries' scope in their summaries and triggers, and update `06-situation-router`). For every new entry, add 2 requests to `eval/routing_scenarios.json`, written the way a user would type them without reusing the entry's triggers; if the new entry takes over a situation an existing scenario covers, add its id as an acceptable second answer there. If a new entry overlaps an existing one, make each summary say where its scope ends and name the other entry.

## Queue (top first)

### Scope: playbooks still missing
- [x] roommate-and-shared-living (chores, bills, guests, noise, moving out)
- [ ] co-parenting-and-ex-logistics (schedules, money, handovers, keeping it about the kids)
- [x] wedding-and-event-host-messages (invites, plus-one no, registry, dress code, uninviting)
- [x] neighbour-disputes (noise, parking, fence, shared wall; escalation to building or council)
- [x] ask-for-a-raise-or-promotion (separate from negotiating an offer: timing, evidence, the meeting request, the follow-up email)
- [ ] give-notice-to-a-landlord-or-tenant (move-out notice, ending a lease early, deposit expectations)
- [x] respond-to-a-difficult-diagnosis-or-health-news (shipped as respond-to-difficult-health-news) (from friend or family; what to say, what not to ask)
- [ ] team-announcements-as-a-manager (reorg, someone leaving, a missed target, a new policy)
- [ ] customer-onboarding-and-welcome (first message after purchase, setting expectations, asking for the info you need)
- [ ] collect-a-debt-from-a-business-or-client-at-scale (dunning sequence: day 1, 7, 14, 30, final notice; when to stop)
- [x] thank-you-notes (gifts, hospitality, mentorship, after a favour; handwritten vs text)
- [ ] telling-someone-something-awkward-about-themselves (body odour, food in teeth, a mistake in their public post)
- [ ] responding-to-a-compliment-that-is-actually-a-hit-on (work context, keep it light and closed)
- [ ] mediating-between-two-people (friends fighting, two team members)

### Effectiveness: make existing entries land better
- [x] ~~Quick version at the top of the 10 most-used entries~~ Dropped 2026-09-27: it repeats each entry's Structure section and costs size budget for every user.
- [ ] (optional, low priority) Colloquial triggers. The model routing check scores 99.4% top-1 on 165 blind requests, so only add triggers for confusions it finds. The lexical eval (`scripts/eval_routing.py`) shows keyword gaps if you want to help weak keyword matchers, but do not stuff triggers to raise it.
- [ ] Add a voice-note / phone-call variant to entries where the channel is often voice (cancel-or-reschedule, condolences, deliver-bad-news, apologize).
- [ ] (optional, low priority) Non-English triggers. A model routes non-English requests correctly (33 of 34 in the check) without them; they only help keyword matching. If done, add 1 or 2 Chinese triggers per entry first, since Chinese is the second audience.
- [ ] 02-tone-calibration: add a table of register markers per channel (WhatsApp, iMessage, Slack, LinkedIn, email, Instagram DM, Xiaohongshu/WeChat).
- [ ] 04-phrase-bank: add a "replace this with that" table for the 30 most common weak phrases.
- [x] Routing evals: `eval/routing_scenarios.json` (165 blind requests, 34 non-English), `scripts/eval_routing.py` (lexical) and `scripts/model_routing.py` (model reads only the index). Results and prompts in `eval/README.md`.
- [ ] Re-run the end-to-end simulation in `eval/README.md` after every 6 to 8 new entries, with a few new scenarios aimed at them. Log the result in TESTLOG.md as a simulated round and fix the playbooks it exposes.

### Distribution
- [x] Index-first retrieval: recommended in skill/SKILL.md, openapi.json, llms.txt and README (index plus four core entries plus the chosen playbook, about a fifth of all.json). Tested by the model routing check (index only, 164 of 165) and the end-to-end simulation (index then entry, 20 of 20). MUSE_PROMPT.md keeps all.json on purpose: every fetch in Muse can need a permission prompt.
- [x] One-command install for Claude Code: a curl snippet in README and index.html fetches skill/SKILL.md and its reference file (works once the branch is on main). A GitHub release zip would need the owner to publish it.
- [x] "Use it with other agents" on index.html and README: the Claude Code install, and a project prompt for ChatGPT, Claude and Gemini with all.json as a file. Fixed the landing, support, privacy and terms pages overflowing sideways on phones (long URLs in the table and support card).
- [ ] Register with other agent connector directories when they open (record URLs and status here).

### Housekeeping
- [ ] TESTLOG.md: run a fourth round of live scenarios once the new entries are on `main`; record results.
- [ ] Re-check SUBMISSION.md status (Muse review reply?) and update.

## Log
- 2026-09-27: v1.3. Added lint (scripts/lint.py), CI, situation router (06), Agent Skill wrapper (skill/SKILL.md), llms.txt, 16 new playbooks, "If it goes badly" sections on 40 entries, Goal/Structure on the 7 that lacked them, this backlog.
- 2026-09-27: loop run. Added roommate-and-shared-living, ask-for-a-raise-or-promotion, thank-you-notes (78 entries, all.json 347 KB); router and README updated; moved the "ask for a raise" trigger from negotiate-price-or-salary to the new entry.
