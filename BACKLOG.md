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
- [x] co-parenting-and-ex-logistics (schedules, money, handovers, keeping it about the kids)
- [x] wedding-and-event-host-messages (invites, plus-one no, registry, dress code, uninviting)
- [x] neighbour-disputes (noise, parking, fence, shared wall; escalation to building or council)
- [x] ask-for-a-raise-or-promotion (separate from negotiating an offer: timing, evidence, the meeting request, the follow-up email)
- [x] give-notice-to-a-landlord-or-tenant (move-out notice, ending a lease early, deposit expectations)
- [x] respond-to-a-difficult-diagnosis-or-health-news (shipped as respond-to-difficult-health-news) (from friend or family; what to say, what not to ask)
- [x] team-announcements-as-a-manager (reorg, someone leaving, a missed target, a new policy)
- [x] customer-onboarding-and-welcome (first message after purchase, setting expectations, asking for the info you need)
- [x] ~~collect-a-debt-from-a-business-or-client-at-scale~~ Folded into chase-late-payment 2026-09-28: it already had the staged sequence; added an automated-reminders variation instead of a near-duplicate entry.
- [x] thank-you-notes (gifts, hospitality, mentorship, after a favour; handwritten vs text)
- [x] telling-someone-something-awkward-about-themselves (shipped as tell-someone-something-awkward) (body odour, food in teeth, a mistake in their public post)
- [ ] responding-to-a-compliment-that-is-actually-a-hit-on (work context, keep it light and closed)
- [x] write-a-recommendation-or-reference-for-someone (shipped as write-a-recommendation-or-reference) (LinkedIn recommendation, reference letter, a reference call when you have reservations; honest without sinking them)
- [x] messages-to-teachers-and-schools (a concern about your child, asking for a meeting, absence notes, disagreeing with a grade or a decision)
- [ ] apologise-for-a-slow-reply (the days-or-weeks-late reply: one line of ownership, then the answer; personal and work)
- [x] mediating-between-two-people (friends fighting, two team members)

### Effectiveness: make existing entries land better
- [x] ~~Quick version at the top of the 10 most-used entries~~ Dropped 2026-09-27: it repeats each entry's Structure section and costs size budget for every user.
- [ ] (optional, low priority) Colloquial triggers. The model routing check scores 99.4% top-1 on 165 blind requests, so only add triggers for confusions it finds. The lexical eval (`scripts/eval_routing.py`) shows keyword gaps if you want to help weak keyword matchers, but do not stuff triggers to raise it.
- [ ] Add a voice-note / phone-call variant to entries where the channel is often voice (cancel-or-reschedule, condolences, deliver-bad-news, apologize).
- [ ] (optional, low priority) Non-English triggers. A model routes non-English requests correctly (33 of 34 in the check) without them; they only help keyword matching. If done, add 1 or 2 Chinese triggers per entry first, since Chinese is the second audience.
- [x] 02-tone-calibration: add a table of register markers per channel (WhatsApp, iMessage, Slack, LinkedIn, email, Instagram DM, Xiaohongshu/WeChat).
- [x] 04-phrase-bank: add a "replace this with that" table for the 30 most common weak phrases.
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
- 2026-09-27: loop run. Added neighbour-disputes, wedding-and-event-host-messages, respond-to-difficult-health-news (81 entries, all.json 348 KB); scoped ask-to-change-behavior and condolences-and-support against them; 6 new routing scenarios. Model routing check (176 requests): top-1 98.3% after scenario #134 (upstairs noise) accepts neighbour-disputes, top-2 100%; dropped "colleague" from ask-to-change-behavior's title after it pulled a peer-feedback request (#98). Two remaining misses (#76 family pressure, #139 ghosting client) are older overlaps, second choice correct.
- 2026-09-27: loop run. Added team-announcements-as-a-manager, customer-onboarding-and-welcome, tell-someone-something-awkward (84 entries, all.json 364 KB); deliver-bad-news summary points team news to the new entry; 6 new routing scenarios. Model routing check (182 requests): top-1 100%, top-2 100%. Nine entries added since the last end-to-end simulation, so that re-run is due next.
- 2026-09-27: loop run. Simulated round 5 (S21-S30, aimed at the nine entries added since round 4): 10/10 passed, including a refused "from all of us" letter; neighbour-disputes gained two principles it exposed (ask for what they can do; speak only for neighbours who agreed). Added co-parenting-and-ex-logistics and give-notice-to-a-landlord-or-tenant (86 entries, all.json 375 KB); 4 routing scenarios. Model routing check (186 requests): top-1 99.5%, top-2 100%; the one miss (#139, a client stalled on files, routed to follow-up-unanswered in 2 of 3 runs today) fixed by scoping the two summaries, confirmed on a targeted re-check. Next e2e round due after 6 to 8 more entries.
- 2026-09-28: loop run. Added mediating-between-two-people (87 entries, all.json 384 KB); 04-phrase-bank gained a 30-row "Replace this with that" table; chase-late-payment gained automated reminders and absorbed the dunning item. lint.py now fails on banned phrases inside example blockquotes, which caught three (chase-late-payment, decline-invitation, decline-offer-or-candidate), now fixed. Model routing check (188 requests): top-1 98.4%, top-2 100%; the new confusion (#123, feedback on a husband's cooking routed to tell-someone-something-awkward) fixed by scoping both summaries, 8 of 8 on a targeted re-check; #76 and #95 are older overlaps, second choice correct. Added three scope items (recommendations for someone, messages to schools, apologising for a slow reply). Next run is the quality pass.
- 2026-09-28: loop run (quality pass, nothing added). Random five: disagree-without-conflict (placeholder examples replaced with concrete ones; recovery section expanded from one line), cancel-or-reschedule (same-day example now leads with the change as its own structure says; cover costs they already paid), give-feedback-kindly (cooking example, clearer principle on what they cannot change), set-boundary (what to do about guilt trips and going cold), ask-for-a-raise-or-promotion (trimmed 33 words of padding). 87 entries, all.json 385 KB.
- 2026-09-28: loop run. Added write-a-recommendation-or-reference and messages-to-teachers-and-schools (89 entries, all.json 398 KB, budget warning at 450); 02-tone-calibration gained register markers per app (WhatsApp, iMessage, Slack, LinkedIn, email, Instagram, WeChat, Xiaohongshu); ask-for-reference-or-recommendation points to the new writing entry; 4 routing scenarios. Model routing check (192 requests): top-1 98.4% (99.0% after scenario #132, a school follow-up, accepts messages-to-teachers-and-schools), top-2 100%. The eval prompt now says not to renumber (a batch starting at 170 was renumbered from 1 twice). Four entries since the last e2e round; the size budget is getting close, so favour merging and trimming over new entries soon.
