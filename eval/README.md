# Evals

Three checks, from cheapest to most realistic. None of them runs against Muse itself; live Muse rounds are recorded in `TESTLOG.md`.

## 1. Lexical routing (`scripts/eval_routing.py`)

BM25 over each entry's triggers, title, tags and summary, with CJK bigrams, scored against `routing_scenarios.json`. It answers one narrow question: do the words users type appear in the metadata? It is a proxy for keyword matching by weak agents or a grep over the cached library, not for how a capable model routes.

```
python3 scripts/eval_routing.py           # summary
python3 scripts/eval_routing.py -v        # every miss
python3 scripts/eval_routing.py --split dev   # tune on dev, then check --split test
```

2026-09-27 baseline: top-1 30.9%, top-3 42.4%, and 0 of 34 non-English requests at top-1. Most misses are requests that describe a situation without any of its keywords ("my husband's dry chicken, how do I say something"), which a model handles and keyword matching cannot.

## 2. Model routing (`scripts/model_routing.py`)

An agent reads only `data/index.json` and picks the best and second-best playbook for each request, without seeing the expected answers. This is the realistic routing test. Run it after adding entries that overlap existing ones, or after changing titles, summaries or triggers.

```
python3 scripts/model_routing.py prepare /tmp/mr
# one agent per /tmp/mr/queries_N.txt, prompt below, each writes /tmp/mr/answers_N.tsv
python3 scripts/model_routing.py score /tmp/mr
```

Prompt for each agent:

> You are the playbook-selection step of an AI assistant that has the SmoothTalker skill installed. Read `data/index.json` and ignore entries whose category is "core". Do not open any other repo file. For each request in `<queries file>` (number, tab, request; some are not in English), choose the best playbook id and a second-best id, judging by what the user actually needs to write. Write `<answers file>`, one line per request: number, tab, best id, tab, second id. Every id must exist in the index.

2026-09-27, 78 entries: top-1 99.4% (164 of 165), top-2 100%, 33 of 34 non-English at top-1. The one miss was a Chinese request to break up after six months, routed to `romantic-let-down` first. The two entries both claimed breakups; their titles, summaries and triggers now split early dating from an established relationship. A re-check on the new index put all 6 breakup and let-down scenarios, plus 5 new boundary requests (a two-year breakup in English and Chinese, one date, three weeks, an ex asking to try again), in the right entry; those 5 are now in the scenario set, which has 170 requests.

The gap between 1 and 2 is the main finding: the metadata already routes almost perfectly for a capable model, so trigger work should target real confusions found here, not keyword coverage for its own sake.

## 3. End-to-end simulation (`e2e/`)

Agents act as the assistant with the skill installed and write the actual reply to each request in `e2e/scenarios.md`. The replies are then reviewed against the playbook and the rules in `00-how-to-use`. `e2e/2026-09-27-outputs.md` holds the first run (20 of 20 passed, see `TESTLOG.md`) as a reference to compare later runs against.

Prompt for each agent (give it half the scenarios):

> You are role-playing an AI assistant that has the SmoothTalker skill installed. Do not edit any repo file. Before any request, read `content/00-how-to-use.md` to `content/03-anti-patterns.md`. For each request, pick one or two playbooks from `data/index.json` (read `content/06-situation-router.md` if nothing matches cleanly, and `content/05-reply-to-a-pasted-message.md` if the user pasted a message), then read the chosen `content/<id>.md` and reply exactly as the assistant would: two versions (warmer and more direct) with one line on which to pick unless the user asked for one, a line on what to do if the reply is negative for sensitive situations, the user's language, and a closing `Playbook: <id>` line. Write `### S<n>`, the playbooks chosen, and the reply for each request to `<output file>`.
