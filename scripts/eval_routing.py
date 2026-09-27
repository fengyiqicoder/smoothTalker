#!/usr/bin/env python3
"""Routing eval: can a user's request find the right playbook from index metadata alone?

A lexical proxy for how an agent (or a grep over the cached library) picks an entry:
BM25 over each entry's triggers, title, tags and summary, plus a bonus when a whole
trigger phrase appears in the request. Real agents read semantically and do better;
this measures whether the metadata gives them a fair hook.

  python3 scripts/eval_routing.py                 # all scenarios, summary
  python3 scripts/eval_routing.py -v              # also print every miss
  python3 scripts/eval_routing.py --split dev     # tune on dev, report on test
  python3 scripts/eval_routing.py --fail-under 0.85   # exit 1 if top-3 < 0.85
"""
import argparse, hashlib, json, math, re, sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "data" / "index.json"
SCEN = ROOT / "eval" / "routing_scenarios.json"
FIELD_W = {"triggers": 3.0, "title": 2.0, "tags": 2.0, "summary": 1.0}
PHRASE_BONUS = 3.0
K1, B = 1.2, 0.75

STOP = set("""a an the and or but if so to of in on at for from by with about into over after before
i me my mine we us our you your he him his she her they them their it its this that these those
is am are was were be been being do does did have has had can could will would should may might must
just really very not no yes please help how what when where why who which there here up out
want need get got make let tell say said reply message text write draft someone something
el la los las un una y o de del que en por para con mi me te se lo le es no
o a os as um uma e do da em com meu minha para que nao
der die das ein eine und oder zu mit mein meine ich nicht ist
le la les un une et ou de du des que en pour avec mon ma mes je ne pas est""".split())

CJK = re.compile(r"[぀-ヿ㐀-䶿一-鿿가-힯]+")
LATIN = re.compile(r"[a-z0-9À-ɏ]+")

def stem(w):
    for suf in ("ing", "ed", "es", "s", "ly"):
        if len(w) > len(suf) + 2 and w.endswith(suf):
            w = w[: -len(suf)]
            break
    return w[:-1] if len(w) > 3 and w.endswith("e") else w

def tokens(text):
    text = text.lower().replace("'", "").replace("’", "")
    out = [stem(w) for w in LATIN.findall(text) if w not in STOP and len(w) > 1]
    for run in CJK.findall(text):
        out += [run[i:i + 2] for i in range(len(run) - 1)] or [run]
    return out

def norm(text):
    return " ".join(LATIN.findall(text.lower().replace("'", ""))) + " " + "".join(CJK.findall(text.lower()))

def load_entries():
    return [e for e in json.loads(INDEX.read_text())["entries"] if e["category"] != "core"]

class Router:
    def __init__(self, entries):
        self.entries = entries
        self.tf = []
        for e in entries:
            c = Counter()
            for field, w in FIELD_W.items():
                val = e.get(field) or ""
                text = " ".join(val) if isinstance(val, list) else val
                for t in tokens(text):
                    c[t] += w
            self.tf.append(c)
        n = len(entries)
        df = Counter(t for c in self.tf for t in c)
        self.idf = {t: math.log(1 + (n - d + 0.5) / (d + 0.5)) for t, d in df.items()}
        self.avg = sum(sum(c.values()) for c in self.tf) / n
        self.phrases = [[norm(t).strip() for t in e.get("triggers", [])] for e in entries]

    def rank(self, q):
        qt, qn = tokens(q), norm(q)
        scores = []
        for i, c in enumerate(self.tf):
            L = sum(c.values())
            s = 0.0
            for t in set(qt):
                f = c.get(t, 0)
                if f:
                    s += self.idf[t] * f * (K1 + 1) / (f + K1 * (1 - B + B * L / self.avg))
            s += PHRASE_BONUS * sum(1 for p in self.phrases[i] if p and p in qn)
            scores.append((s, self.entries[i]["id"]))
        scores.sort(reverse=True)
        return scores

def split_of(q):
    return "test" if int(hashlib.md5(q.encode()).hexdigest(), 16) % 3 == 0 else "dev"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", choices=["all", "dev", "test"], default="all")
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("--fail-under", type=float, default=None, help="minimum top-3 accuracy")
    a = ap.parse_args()
    entries = load_entries()
    ids = {e["id"] for e in entries}
    router = Router(entries)
    scen = json.loads(SCEN.read_text())
    unknown = sorted({x for s in scen for x in s["expect"] if x not in ids})
    scen = [s for s in scen if s["expect"][0] in ids and (a.split == "all" or split_of(s["q"]) == a.split)]
    top1 = top3 = 0
    per_lang = defaultdict(lambda: [0, 0, 0])
    per_entry = defaultdict(lambda: [0, 0])
    misses = []
    for s in scen:
        r = router.rank(s["q"])
        got = [i for _, i in r[:3]]
        h1, h3 = got[0] in s["expect"], any(x in got for x in s["expect"])
        top1 += h1; top3 += h3
        L = per_lang[s.get("lang", "en")]; L[0] += 1; L[1] += h1; L[2] += h3
        E = per_entry[s["expect"][0]]; E[0] += 1; E[1] += h1
        if not h1:
            misses.append((s, r[:3]))
    n = len(scen) or 1
    print(f"scenarios {len(scen)} ({a.split})  top-1 {top1 / n:.1%}  top-3 {top3 / n:.1%}")
    print("by language: " + "  ".join(f"{k} {v[1]}/{v[0]} top1, {v[2]}/{v[0]} top3" for k, v in sorted(per_lang.items())))
    weak = sorted((v[1] / v[0], k, v) for k, v in per_entry.items() if v[1] < v[0])
    if weak:
        print("entries missed at top-1: " + ", ".join(f"{k} {v[1]}/{v[0]}" for _, k, v in weak))
    if unknown:
        print("scenario ids not in index (skipped or ignored): " + ", ".join(unknown))
    if a.verbose:
        for s, r in misses:
            print(f"\nMISS [{s.get('lang','en')}] {s['q']}\n  expect {s['expect']}\n  got    " + ", ".join(f"{i} {sc:.1f}" for sc, i in r))
    if a.fail_under is not None and top3 / n < a.fail_under:
        print(f"top-3 {top3 / n:.1%} is below {a.fail_under:.0%}"); sys.exit(1)

if __name__ == "__main__":
    main()
