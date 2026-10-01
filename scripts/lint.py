#!/usr/bin/env python3
"""Quality lint for content/*.md. Run before build_index.py. Exit 1 on errors; warnings do not fail."""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
sys.path.insert(0, str(ROOT / "scripts"))
from build_index import parse  # noqa: E402

CATEGORIES = {"core", "personal", "work", "commerce"}
MIN_TRIGGERS, MIN_TAGS = 5, 3
MIN_WORDS, MAX_WORDS = 300, 1400
MAX_SUMMARY = 260

errors, warnings = [], []
seen_triggers = {}

def err(p, msg): errors.append(f"{p.name}: {msg}")
def warn(p, msg): warnings.append(f"{p.name}: {msg}")

for p in sorted(CONTENT.glob("*.md")):
    try:
        meta, body = parse(p)
    except Exception as ex:
        err(p, str(ex)); continue
    core = meta.get("category") == "core"
    if meta.get("category") not in CATEGORIES:
        err(p, f"category must be one of {sorted(CATEGORIES)}")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", p.stem):
        err(p, "filename must be kebab-case")
    if len(meta.get("triggers", [])) < MIN_TRIGGERS:
        err(p, f"needs at least {MIN_TRIGGERS} triggers")
    if len(meta.get("tags", [])) < MIN_TAGS:
        err(p, f"needs at least {MIN_TAGS} tags")
    if len(meta.get("summary", "")) > MAX_SUMMARY:
        err(p, f"summary longer than {MAX_SUMMARY} chars")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", meta.get("updated", "")):
        err(p, "updated must be YYYY-MM-DD")
    for t in meta.get("triggers", []):
        key = t.lower()
        if key in seen_triggers and seen_triggers[key] != p.name:
            warn(p, f"trigger '{t}' also in {seen_triggers[key]}")
        seen_triggers.setdefault(key, p.name)
    if "—" in body or "—" in " ".join(str(v) for v in meta.values()):
        err(p, "em-dash found; the style rules forbid it")
    for line in body.splitlines():
        if line.startswith(">") and re.search(r"\b(unfortunately|i'm afraid|i'll have to)\b", line, re.I):
            err(p, f"banned phrase in an example: {line[:60]}")
    words = len(body.split())
    if words < MIN_WORDS: err(p, f"body too short ({words} words)")
    if words > MAX_WORDS: warn(p, f"body long ({words} words)")
    if not core:
        heads = [h.strip() for h in re.findall(r"^## (.+)$", body, re.M)]
        for need in ("Goal", "Avoid"):
            if not any(h.startswith(need) for h in heads):
                err(p, f"missing '## {need}' section")
        if not any(h.startswith("Structure") for h in heads) and len(heads) < 5:
            err(p, "needs a '## Structure' section or scenario sections")
        if body.count("\n>") < 3:
            err(p, "needs at least 3 quoted examples (lines starting with '>')")
        if not any(h.lower().startswith(("if ", "when ", "what to do")) for h in heads):
            warn(p, "no 'If it goes badly' style section")

# Worked cases: cases/<playbook-id>.jsonl, one JSON object per line.
CASES = ROOT / "cases"
BANNED = re.compile(r"\b(unfortunately|i'm afraid|i'll have to)\b", re.I)
LANGS = {"en", "zh", "es", "pt", "de", "fr", "ja"}
seen_case_ids = set()
if CASES.exists():
    for p in sorted(CASES.glob("*.jsonl")):
        if not (CONTENT / f"{p.stem}.md").exists():
            err(p, "no playbook with this id in content/"); continue
        for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            where = f"line {n}"
            try:
                c = json.loads(line)
            except Exception as ex:
                err(p, f"{where}: not valid JSON ({ex})"); continue
            for k in ("id", "situation", "reply", "lang"):
                if not c.get(k):
                    err(p, f"{where}: missing '{k}'")
            cid = c.get("id", "")
            if not cid.startswith(p.stem + "-"):
                err(p, f"{where}: id must start with '{p.stem}-'")
            if cid in seen_case_ids:
                err(p, f"{where}: duplicate id {cid}")
            seen_case_ids.add(cid)
            if c.get("lang") not in LANGS:
                err(p, f"{where}: lang must be one of {sorted(LANGS)}")
            text = " ".join(str(c.get(k, "")) for k in ("situation", "reply", "note"))
            if "\u2014" in text:
                err(p, f"{where}: em-dash")
            if BANNED.search(str(c.get("reply", ""))):
                err(p, f"{where}: banned phrase in the reply")
            for dom in re.findall(r"[\w.+-]+@([\w-]+(?:\.[\w-]+)+)", text):
                if dom.lower() not in ("example.com", "example.org", "example.net"):
                    err(p, f"{where}: email domain {dom}; use example.com")
            if len(str(c.get("reply", ""))) > 900:
                warn(p, f"{where}: reply over 900 characters; keep cases short")

router = CONTENT / "06-situation-router.md"
if router.exists():
    rtext = router.read_text(encoding="utf-8")
    for p in sorted(CONTENT.glob("*.md")):
        try:
            if parse(p)[0].get("category") != "core" and f"`{p.stem}`" not in rtext:
                err(p, "not named in 06-situation-router.md; add a routing line")
        except Exception:
            pass

for w in warnings: print("warn:", w)
for e in errors: print("ERROR:", e)
print(f"{len(list(CONTENT.glob('*.md')))} entries, {len(errors)} errors, {len(warnings)} warnings")
sys.exit(1 if errors else 0)
