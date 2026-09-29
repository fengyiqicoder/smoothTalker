# SmoothTalker

**A static, read-only Muse connector that makes every conversation smoother.**

SmoothTalker is a library of conversation playbooks. When a Muse user asks their agent to write, reply to, soften or improve any message, the agent consults the matching playbook and produces something clearer, kinder and more effective. It covers declining, apologising, negotiating, following up, delivering bad news, setting boundaries, handling angry customers, DM replies for small businesses, brand-deal replies for creators, and more.

There is no server. It is an OpenAPI document plus JSON files on GitHub Pages.

- Site: https://smoothtalker.000ooo.ooo/
- Agent-safe fetch URL (the custom domain is blocked from some agent networks, including Muse's VM, and github.io redirects to it): https://raw.githubusercontent.com/fengyiqicoder/smoothTalker/main/data/all.json
- OpenAPI: https://smoothtalker.000ooo.ooo/openapi.json
- Whole library in one file: https://smoothtalker.000ooo.ooo/data/all.json
- Index only (the recommended entry point for agents that fetch per request): https://smoothtalker.000ooo.ooo/data/index.json
- Worked cases for one playbook (a real situation and the reply it produced): https://smoothtalker.000ooo.ooo/data/cases/{id}.json, listed in https://smoothtalker.000ooo.ooo/data/cases/index.json

## Use it with other agents

**Claude Code, or any host that reads Agent Skills.** `skill/SKILL.md` is a drop-in skill that loads the index and fetches only the playbook each request needs:

```
mkdir -p ~/.claude/skills/smoothtalker/reference
cd ~/.claude/skills/smoothtalker
curl -fsSLO https://raw.githubusercontent.com/fengyiqicoder/smoothTalker/main/skill/SKILL.md
curl -fsSL -o reference/principles.md https://raw.githubusercontent.com/fengyiqicoder/smoothTalker/main/skill/reference/principles.md
```

**ChatGPT, Claude or Gemini projects.** Add `data/all.json` as a file to a project (or a custom GPT's knowledge, or a Gem) and paste the instructions shown on the [landing page](https://smoothtalker.000ooo.ooo/). Agents that read `llms.txt` can start from https://raw.githubusercontent.com/fengyiqicoder/smoothTalker/main/llms.txt.

## Connect it to Muse

Copy the prompt in [`MUSE_PROMPT.md`](MUSE_PROMPT.md) and send it to Muse. Muse builds the bridge in its own VM and saves it as a skill. No API key. It also works as a custom integration for any agent that can read an OpenAPI document or fetch JSON.

## What is inside

| Category | Playbooks |
|---|---|
| core | how to use, principles, tone calibration, anti-patterns, phrase bank, reply to a pasted message, cross-cultural notes, situation router |
| personal | landlords/tenants/contractors, complain as a customer, ask someone out and early dating, share personal news, group chat coordination, respond to unsolicited advice, decline invitation, decline request, ask a favour, apologise, follow up, reconnect after silence, deliver bad news, condolences, disagree without conflict, de-escalate an argument, set a boundary, end a conversation, cancel or reschedule, romantic let-down, first message to a stranger, respond to criticism, ask someone to change a behaviour, give feedback kindly, money between friends, compliments and thanks, small talk, respond to passive-aggression, check in on someone struggling, an ex or a breakup message, family pressure and nosy questions, no-shows and lateness, suspicious or scam messages, ask for a discount as a customer, roommates and shared living, thank-you notes, neighbour disputes, wedding and event host messages, respond to difficult health news, tell someone something awkward, co-parenting with an ex, give notice to a landlord or tenant, mediate between two people, messages to teachers and schools |
| work | ask a colleague for help or delegate, introduce yourself, negotiate salary or price, push back on your boss, say no to a client, chase late payment, angry customer, cold outreach, decline an offer or reject a candidate, feedback to a colleague, admit a mistake, ask for an extension, follow up after interview or meeting, quit or leave gracefully, client went silent, request an intro, time off and sick leave, reply to a recruiter, ask for a reference, escalate an issue, respond to a job rejection, decline meetings, out-of-office messages, ask for a raise or promotion, team announcements as a manager, write a recommendation or reference |
| commerce | price increase and customer announcements, ask for a review or testimonial, customer inquiry in DMs, refund requests, negative reviews, upsell without pushiness, creator brand deals, shipping delays and stockouts, public apology from a business, say no to a customer request, customer onboarding and welcome |

Every playbook has the same shape: **Goal, Structure, Principles, Examples at several tones, Avoid, and what to do if it goes badly.** `scripts/lint.py` enforces this shape.

## How the agent uses it

1. Loads the index (`data/index.json`, small) and the core entries `00-how-to-use`, `01-principles`, `02-tone-calibration` and `03-anti-patterns`. Agents that pay for every fetch, such as Muse with its permission prompts, load `data/all.json` once a day instead.
2. Matches the user's situation to one or two playbooks via `triggers`, `tags` and `summary`, or `06-situation-router` when nothing matches cleanly, and fetches `data/entries/<id>.json`.
3. Writes the message from the playbook's structure with the user's real specifics.
4. Calibrates tone and checks against the anti-patterns.
5. Returns two ready-to-send versions unless one was asked for, and names the playbook used.

How well this works is measured in `eval/`: a model picking from the index alone chose the right playbook for 164 of 165 blind requests, and simulated end-to-end replies passed 20 of 20. See `eval/README.md` and `TESTLOG.md`.

## Authoring

Source of truth is `content/*.md`: YAML-style front matter (`title`, `category`, `tags`, `triggers`, `summary`, `updated`) plus a Markdown body. Run:

```
python3 scripts/lint.py
python3 scripts/build_index.py
```

The lint checks shape and style (sections, trigger count, no em-dashes). The build validates every entry and regenerates `data/entries/*.json`, `data/index.json`, `data/all.json` and `data/cases/` (from `cases/*.jsonl`, see `cases/README.md`). Commit and push; GitHub Pages updates in a minute or two.

## Design principles for the content

- **Smooth means clear, warm and low-friction.** Never slippery, vague or manipulative.
- **Structure over scripts.** Examples are there to be adapted, not pasted.
- **Shorter is kinder.** Most playbooks push toward fewer words.
- **The user's interests come first.** When the user is being wronged, the library makes them clearer, not softer.

Licence: content is CC BY 4.0. Use it, fork it, improve it.
