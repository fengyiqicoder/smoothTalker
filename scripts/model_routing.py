#!/usr/bin/env python3
"""Model routing check: can an agent that reads only data/index.json pick the right playbook?

This is the realistic routing test (eval_routing.py is the cheap lexical proxy).
Run it after adding or re-scoping entries that overlap existing ones.

  python3 scripts/model_routing.py prepare OUTDIR      # writes label-free query files
  # give each OUTDIR/queries_*.txt to a separate agent with the prompt in eval/README.md;
  # each agent writes OUTDIR/answers_*.tsv (number, tab, best id, tab, second id)
  python3 scripts/model_routing.py score OUTDIR        # prints accuracy and every miss

Label-free means the agent never sees the expected answers.
"""
import collections, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCEN = ROOT / "eval" / "routing_scenarios.json"
CHUNK = 85

def prepare(out):
    out.mkdir(parents=True, exist_ok=True)
    scen = json.loads(SCEN.read_text())
    for k, start in enumerate(range(0, len(scen), CHUNK)):
        with open(out / f"queries_{k}.txt", "w", encoding="utf-8") as f:
            for i in range(start, min(start + CHUNK, len(scen))):
                f.write(f"{i}\t{scen[i]['q']}\n")
    print(f"wrote {k + 1} query files for {len(scen)} scenarios to {out}")

def score(out):
    scen = json.loads(SCEN.read_text())
    ids = {e["id"] for e in json.loads((ROOT / "data" / "index.json").read_text())["entries"]}
    ans = {}
    for f in sorted(out.glob("answers_*.tsv")):
        for line in f.read_text(encoding="utf-8").splitlines():
            p = [x.strip() for x in line.split("\t")]
            if len(p) >= 3 and p[0].isdigit():
                ans[int(p[0])] = p[1:3]
    n = t1 = t2 = 0
    lang = collections.defaultdict(lambda: [0, 0])
    misses, invalid = [], []
    for i, s in enumerate(scen):
        if i not in ans:
            continue
        a = ans[i]
        invalid += [x for x in a if x not in ids]
        h1, h2 = a[0] in s["expect"], any(x in s["expect"] for x in a)
        n += 1; t1 += h1; t2 += h2
        lang[s["lang"]][0] += 1; lang[s["lang"]][1] += h1
        if not h1:
            misses.append((i, s, a))
    if not n:
        sys.exit("no answers found")
    print(f"answered {n}/{len(scen)}  top-1 {t1 / n:.1%}  top-2 {t2 / n:.1%}")
    print("top-1 by language: " + "  ".join(f"{k} {v[1]}/{v[0]}" for k, v in sorted(lang.items())))
    if invalid:
        print("ids not in the index: " + ", ".join(sorted(set(invalid))))
    for i, s, a in misses:
        print(f"\n#{i} [{s['lang']}] {s['q'][:160]}\n  expect {s['expect']}\n  got    {a}")

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("prepare", "score"):
        sys.exit(__doc__)
    (prepare if sys.argv[1] == "prepare" else score)(Path(sys.argv[2]))
