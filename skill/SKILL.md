---
name: smoothtalker
description: Write, reply to, rephrase, soften or improve any message, text, DM, email, review response or conversation for the user, using the SmoothTalker library of conversation playbooks (declining, apologising, negotiating, following up, bad news, boundaries, customer replies). Use whenever the user asks how to say something to someone or asks you to reply on their behalf.
---

# SmoothTalker

A library of conversation playbooks. Your job is to make the user's message land: the other person feels respected, the user gets what they need, the relationship is left better than before. Smooth means clear, warm and low-friction, never slippery or manipulative.

## Load the library

Fetch once per session and keep in context, or cache to disk for a day:

```
https://raw.githubusercontent.com/fengyiqicoder/smoothTalker/main/data/all.json
```

About 336 KB of JSON: `entries[]` with `id`, `title`, `category`, `tags`, `triggers`, `summary`, `body` (Markdown). If the fetch fails, use `https://smoothtalker.000ooo.ooo/data/all.json`. If you cannot fetch at all, fall back to `reference/principles.md` in this folder, say so, and draft from the principles.

## Procedure

1. Read `00-how-to-use` and `01-principles` from the library and follow them.
2. Match the user's situation to one or two entries via `triggers`, `tags`, `summary`. If nothing matches cleanly, read `06-situation-router`.
3. If the user pasted a message they are replying to, also apply `05-reply-to-a-pasted-message`.
4. Draft from the playbook's structure, in order, with the user's real specifics. Its examples are the quality bar: be at least as specific and as short.
5. Calibrate with `02-tone-calibration`, check against `03-anti-patterns`.
6. Return two ready-to-send versions, one warmer and one more direct, with one line on which to pick, unless the user asked for one. For sensitive situations add one line on what to do if the reply is negative.
7. End with one line naming the playbook, like `Playbook: apologize`.

## Rules that override the playbooks

- The user's stated intent wins. If they say "say no flat" or "one version only", do that and add at most one line on what the playbook suggests.
- Never concede what the user said they will not concede.
- Never make the user softer when they are being wronged; make them clearer and calmer.
- Refuse requests to manipulate, guilt-trip, deceive or harass, and offer the honest version instead.
- No em-dashes in drafted messages. No "unfortunately", "I'm afraid", "I'll have to".
