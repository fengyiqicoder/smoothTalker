# SmoothTalker backlog and iteration log

This file is the shared memory for the autonomous improvement loop. Each run reads it, picks the top unchecked items it can finish, does them, ticks them off, appends a log line, and pushes. Keep it short.

## Rules for every iteration
- Content quality beats count. One excellent playbook beats three thin ones.
- Every change passes `python3 scripts/lint.py` and `python3 scripts/build_index.py`; commit `data/` with the content.
- Keep counts and the all.json size in sync in `README.md`, `index.html`, `openapi.json`, `MUSE_PROMPT.md` and `skill/SKILL.md`. Never edit `SUBMISSION.md`'s submitted text; it records what was sent on 2026-09-25.
- Never change the shape of `data/*.json` fields or the OpenAPI paths (agents depend on them).
- No em-dashes anywhere in content. No manipulative or deceptive advice, ever.
- Push to the working branch only; a human merges to `main` (the live site).
- Size budget: agents load `all.json` whole, so every entry costs context for every user. `build_index.py` warns above 450 KB and fails above 600 KB. Near the budget, merge overlapping entries, trim padding and improve quality instead of adding. Growth past the budget needs the index-first retrieval item below first.
- Items marked "claimed" are being done by another session; skip them.

## Queue (top first)

### Scope: playbooks still missing
- [ ] (claimed 2026-09-27 loop) roommate-and-shared-living (chores, bills, guests, noise, moving out)
- [ ] co-parenting-and-ex-logistics (schedules, money, handovers, keeping it about the kids)
- [ ] wedding-and-event-host-messages (invites, plus-one no, registry, dress code, uninviting)
- [ ] neighbour-disputes (noise, parking, fence, shared wall; escalation to building or council)
- [ ] (claimed 2026-09-27 loop) ask-for-a-raise-or-promotion (separate from negotiating an offer: timing, evidence, the meeting request, the follow-up email)
- [ ] give-notice-to-a-landlord-or-tenant (move-out notice, ending a lease early, deposit expectations)
- [ ] respond-to-a-difficult-diagnosis-or-health-news (from friend or family; what to say, what not to ask)
- [ ] team-announcements-as-a-manager (reorg, someone leaving, a missed target, a new policy)
- [ ] customer-onboarding-and-welcome (first message after purchase, setting expectations, asking for the info you need)
- [ ] collect-a-debt-from-a-business-or-client-at-scale (dunning sequence: day 1, 7, 14, 30, final notice; when to stop)
- [ ] (claimed 2026-09-27 loop) thank-you-notes (gifts, hospitality, mentorship, after a favour; handwritten vs text)
- [ ] telling-someone-something-awkward-about-themselves (body odour, food in teeth, a mistake in their public post)
- [ ] responding-to-a-compliment-that-is-actually-a-hit-on (work context, keep it light and closed)
- [ ] mediating-between-two-people (friends fighting, two team members)

### Effectiveness: make existing entries land better
- [ ] (claimed 2026-09-27) Add a 3-line "Quick version" at the top of the 10 most-used entries (apologize, decline-request, follow-up-unanswered, negotiate-price-or-salary, respond-to-angry-customer, landlord-tenant, push-back-on-boss, decline-invitation, set-boundary, reply-to-customer-inquiry-dm) so an agent can answer a one-line request without reading the whole body.
- [ ] (claimed 2026-09-27) Audit every entry's `triggers` against how people actually type (short, lowercase, typos, "wtf do I say"). Add 2-3 colloquial triggers per entry where missing.
- [ ] Add a voice-note / phone-call variant to entries where the channel is often voice (cancel-or-reschedule, condolences, deliver-bad-news, apologize).
- [ ] (claimed 2026-09-27) Add non-English trigger phrases (zh, es, pt, de, fr, ja) to the 15 most-used entries so matching works for non-English users. Keep bodies in English.
- [ ] 02-tone-calibration: add a table of register markers per channel (WhatsApp, iMessage, Slack, LinkedIn, email, Instagram DM, Xiaohongshu/WeChat).
- [ ] 04-phrase-bank: add a "replace this with that" table for the 30 most common weak phrases.
- [ ] (claimed 2026-09-27) Write `scripts/eval_scenarios.json`: 40 scenarios with expected playbook ids, and `scripts/eval_match.py` that checks trigger/tag matching picks the expected entry with simple keyword overlap. Use it to tune triggers.

### Distribution
- [ ] Index-first retrieval: document and test a flow where the agent loads `index.json` (small), picks entries, then fetches `entries/{id}.json`, so the library can grow past the all.json budget. Update the OpenAPI descriptions, `skill/SKILL.md` and `MUSE_PROMPT.md` to recommend it once the library passes about 110 entries. Keep `all.json` published for existing installs.
- [ ] Add `skill/` folder to a zip release so it can be installed in Claude Code with one command; document in README.
- [ ] Add a "Try it without Muse" section to index.html: paste-a-playbook prompt for ChatGPT/Claude/Gemini users.
- [ ] Register with other agent connector directories when they open (record URLs and status here).

### Housekeeping
- [ ] TESTLOG.md: run a fourth round of live scenarios once the new entries are on `main`; record results.
- [ ] Re-check SUBMISSION.md status (Muse review reply?) and update.

## Log
- 2026-09-27: v1.3. Added lint (scripts/lint.py), CI, situation router (06), Agent Skill wrapper (skill/SKILL.md), llms.txt, 16 new playbooks, "If it goes badly" sections on 40 entries, Goal/Structure on the 7 that lacked them, this backlog.
