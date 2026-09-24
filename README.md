# SmoothTalker

**A static, read-only Muse connector that makes every conversation smoother.**

SmoothTalker is a library of conversation playbooks. When a Muse user asks their agent to write, reply to, soften or improve any message, the agent consults the matching playbook and produces something clearer, kinder and more effective. It covers declining, apologising, negotiating, following up, delivering bad news, setting boundaries, handling angry customers, DM replies for small businesses, brand-deal replies for creators, and more.

There is no server. It is an OpenAPI document plus JSON files on GitHub Pages.

- Site: https://smoothtalker.000ooo.ooo/
- Mirror (use this if the custom domain is blocked from an agent's network, which happened with Muse): https://fengyiqicoder.github.io/smoothTalker/
- OpenAPI: https://smoothtalker.000ooo.ooo/openapi.json
- Whole library in one file: https://smoothtalker.000ooo.ooo/data/all.json
- Index only: https://smoothtalker.000ooo.ooo/data/index.json

## Connect it to Muse

Copy the prompt in [`MUSE_PROMPT.md`](MUSE_PROMPT.md) and send it to Muse. Muse builds the bridge in its own VM and saves it as a skill. No API key. It also works as a custom integration for any agent that can read an OpenAPI document or fetch JSON.

## What is inside

| Category | Playbooks |
|---|---|
| core | how to use, principles, tone calibration, anti-patterns, phrase bank, cross-cultural notes |
| personal | landlords/tenants/contractors, complain as a customer, ask someone out and early dating, share personal news, group chat coordination, respond to unsolicited advice, decline invitation, decline request, ask a favour, apologise, follow up, reconnect after silence, deliver bad news, condolences, disagree without conflict, de-escalate an argument, set a boundary, end a conversation, cancel or reschedule, romantic let-down, first message to a stranger, respond to criticism, ask someone to change a behaviour, give feedback kindly, money between friends, compliments and thanks, small talk, respond to passive-aggression |
| work | ask a colleague for help or delegate, introduce yourself, negotiate salary or price, push back on your boss, say no to a client, chase late payment, angry customer, cold outreach, decline an offer or reject a candidate, feedback to a colleague, admit a mistake, ask for an extension, follow up after interview or meeting, quit or leave gracefully, client went silent, request an intro |
| commerce | price increase and customer announcements, ask for a review or testimonial, customer inquiry in DMs, refund requests, negative reviews, upsell without pushiness, creator brand deals |

Every playbook has the same shape: **Goal → Structure → Principles → Examples at several tones → Avoid → What to do if it goes badly.**

## How the agent uses it

1. Loads `all.json` once and caches it.
2. Always applies `00-how-to-use` and `01-principles`.
3. Matches the user's situation to a playbook via `triggers`, `tags`, `summary`.
4. Writes the message from the playbook's structure with the user's real specifics.
5. Calibrates tone (`02-tone-calibration`) and checks against `03-anti-patterns`.
6. Returns two ready-to-send versions unless one was asked for.

## Authoring

Source of truth is `content/*.md`: YAML-style front matter (`title`, `category`, `tags`, `triggers`, `summary`, `updated`) plus a Markdown body. Run:

```
python3 scripts/build_index.py
```

It validates every entry and regenerates `data/entries/*.json`, `data/index.json` and `data/all.json`. Commit and push; GitHub Pages updates in a minute or two.

## Design principles for the content

- **Smooth means clear, warm and low-friction.** Never slippery, vague or manipulative.
- **Structure over scripts.** Examples are there to be adapted, not pasted.
- **Shorter is kinder.** Most playbooks push toward fewer words.
- **The user's interests come first.** When the user is being wronged, the library makes them clearer, not softer.

Licence: content is CC BY 4.0. Use it, fork it, improve it.
