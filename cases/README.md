# Worked cases

A case is one concrete situation, written the way a user would ask, and the ready-to-send message the playbook produces for it. Playbooks teach the method; cases show it applied to real specifics. Agents fetch `data/cases/<playbook-id>.json` after choosing a playbook and use the closest case as a model, never as a template to copy word for word.

Cases live outside `all.json`, so they do not count against the size budget.

## Format

One file per playbook: `cases/<playbook-id>.jsonl`, one JSON object per line.

```
{"id": "apologize-001", "lang": "en", "situation": "I forgot my best friend's birthday yesterday. We've been friends 15 years.", "reply": "I completely missed your birthday yesterday and I'm really sorry. No excuse, it just slipped, and you deserve better from me. Can I take you for dinner this week, my treat? Thursday or Friday?", "note": "Optional: one line on the choice that matters."}
```

- `id`: `<playbook-id>-NNN`, numbered in order, never reused.
- `lang`: en, zh, es, pt, de, fr or ja. The situation and the reply are in that language.
- `situation`: 1 to 3 sentences, as the user would type it, with the specifics that change the answer (who, what happened, what they want).
- `reply`: the message to send, following the playbook's structure. Usually 1 to 5 sentences. No brackets or placeholders: invent plausible names, dates and amounts.
- `note` (optional): one short line on why the reply is shaped the way it is, or what to do if they push back.

## Quality bar

- Each case in a file covers a different angle: relationship, channel, stakes, culture or the pushback. No two cases should teach the same thing.
- The reply obeys the library's rules: no em-dashes, no "unfortunately", "I'm afraid" or "I'll have to", one clear ask, never manipulative or deceptive.
- At least one case in four is not in English, mostly Chinese.
- Every fact the reply relies on (a memory, a clause number, a length of stay, an earlier conversation) is in the situation. Invent names, dates and amounts for the situation, not new facts in the reply, so an agent adapting the case never puts words in the user's mouth. The sender's own next step with a date ("I'll send the plan by Friday 9 October") is fine; promises that need someone else's decision are not.
- Naming the channel people use (WeChat, Slack, WhatsApp, LINE) is fine; recommending a product, bank, courier or company is not. Invent business names, and use example.com for email addresses (`scripts/lint.py` enforces the domain).
- `python3 scripts/lint.py` checks the format; `python3 scripts/build_index.py` writes `data/cases/`.
