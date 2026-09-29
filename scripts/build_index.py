#!/usr/bin/env python3
"""content/*.md（front matter + Markdown 正文）→ data/entries/<id>.json、data/index.json、data/all.json"""
import json, sys, datetime, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
ENTRIES = ROOT / "data" / "entries"
INDEX = ROOT / "data" / "index.json"
ALL = ROOT / "data" / "all.json"
CASES_SRC = ROOT / "cases"
CASES_OUT = ROOT / "data" / "cases"
REQUIRED = ["title", "summary", "tags", "triggers"]
BUDGET_WARN_KB, BUDGET_FAIL_KB = 450, 600  # agents load all.json whole; see BACKLOG.md

def parse(path: Path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        raise ValueError("缺少 front matter")
    meta, body = {}, m.group(2).strip()
    for line in m.group(1).splitlines():
        if not line.strip() or ":" not in line:
            continue
        k, v = line.split(":", 1)
        v = v.strip()
        if v.startswith("[") and v.endswith("]"):
            v = [x.strip().strip('"').strip("'") for x in v[1:-1].split(",") if x.strip()]
        meta[k.strip()] = v
    return meta, body

# Counts and sizes quoted in the docs. build keeps them in sync so nobody edits numbers by hand.
DOC_PATTERNS = [
  ("index.html", r"library of \d+ conversation playbooks", "library of {n} conversation playbooks"),
  ("index.html", r"Core \(\d+\)", "Core ({core})"),
  ("index.html", r"Personal \(\d+\), Work \(\d+\), Commerce \(\d+\)", "Personal ({personal}), Work ({work}), Commerce ({commerce})"),
  ("MUSE_PROMPT.md", r"It is about \d+ KB", "It is about {kb} KB"),
  ("skill/SKILL.md", r"`data/all\.json` \(about \d+ KB", "`data/all.json` (about {kb} KB"),
  ("skill/SKILL.md", r"`data/index\.json` \(about \d+ KB", "`data/index.json` (about {index_kb} KB"),
  ("openapi.json", r"in one request \(about \d+ KB\)", "in one request (about {kb} KB)"),
  ("openapi.json", r"the index, about \d+ KB", "the index, about {index_kb} KB"),
]

def sync_docs(full, kb):
  counts = {"n": len(full), "kb": kb, "index_kb": round(INDEX.stat().st_size / 1024), "core": 0, "personal": 0, "work": 0, "commerce": 0}
  for e in full:
    counts[e["category"]] = counts.get(e["category"], 0) + 1
  changed = []
  for rel, pat, tmpl in DOC_PATTERNS:
    f = ROOT / rel
    if not f.exists():
      continue
    text = f.read_text(encoding="utf-8")
    new_text = re.sub(pat, tmpl.format(**counts), text)
    if new_text != text:
      f.write_text(new_text, encoding="utf-8")
      changed.append(rel)
  if changed:
    print("已同步文档中的数字：" + ", ".join(sorted(set(changed))))

def dump_listing(today, entries):
  """One entry per line: valid JSON, line-based diffs, and no indentation for agents to pay tokens for."""
  head = json.dumps({"generated": today, "count": len(entries), "read_first": ["00-how-to-use", "01-principles"]}, ensure_ascii=False)
  lines = ",\n".join(json.dumps(e, ensure_ascii=False, separators=(",", ":")) for e in entries)
  return head[:-1] + ',"entries":[\n' + lines + "\n]}\n"

def load_cases():
  """cases/<playbook-id>.jsonl: one case per line. Returns {playbook_id: [case, ...]}."""
  out = {}
  if not CASES_SRC.exists():
    return out
  for p in sorted(CASES_SRC.glob("*.jsonl")):
    rows = []
    for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
      if line.strip():
        c = json.loads(line)
        rows.append({k: c[k] for k in ("id", "situation", "reply", "lang", "note") if k in c})
    out[p.stem] = rows
  return out

def build_cases(today):
  """Worked cases live outside all.json so the size budget holds. Agents fetch them per playbook."""
  cases = load_cases()
  CASES_OUT.mkdir(parents=True, exist_ok=True)
  for old in CASES_OUT.glob("*.json"):
    old.unlink()
  index = []
  for pid, rows in cases.items():
    (CASES_OUT / f"{pid}.json").write_text(json.dumps({"playbook": pid, "count": len(rows), "cases": rows}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for c in rows:
      index.append({"id": c["id"], "playbook": pid, "lang": c.get("lang", "en"), "situation": c["situation"]})
  head = json.dumps({"generated": today, "count": len(index)}, ensure_ascii=False)
  lines = ",\n".join(json.dumps(e, ensure_ascii=False, separators=(",", ":")) for e in index)
  (CASES_OUT / "index.json").write_text(head[:-1] + ',"cases":[\n' + lines + "\n]}\n", encoding="utf-8")
  return len(index)

def main():
  ENTRIES.mkdir(parents=True, exist_ok=True)
  for old in ENTRIES.glob("*.json"):
      old.unlink()

  items, full, errors = [], [], []
  for p in sorted(CONTENT.glob("*.md")):
      try:
          meta, body = parse(p)
      except Exception as ex:
          errors.append(f"{p.name}: {ex}"); continue
      for k in REQUIRED:
          if not meta.get(k):
              errors.append(f"{p.name}: 缺少字段 {k}")
      if not body:
          errors.append(f"{p.name}: 正文为空")
      entry = {
          "id": p.stem,
          "title": meta.get("title"),
          "category": meta.get("category", "general"),
          "tags": meta.get("tags", []),
          "triggers": meta.get("triggers", []),
          "summary": meta.get("summary"),
          "updated": meta.get("updated") or datetime.date.today().isoformat(),
          "body": body,
      }
      full.append(entry)
      items.append({k: entry[k] for k in ("id", "title", "category", "tags", "triggers", "summary", "updated")})
      (ENTRIES / f"{p.stem}.json").write_text(json.dumps(entry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

  if errors:
      print("校验失败："); [print("  -", x) for x in errors]; sys.exit(1)

  today = datetime.date.today().isoformat()
  INDEX.write_text(dump_listing(today, items), encoding="utf-8")
  ALL.write_text(dump_listing(today, full), encoding="utf-8")
  kb = ALL.stat().st_size // 1024
  ncases = build_cases(today)
  print(f"已生成 {len(items)} 条；all.json {kb} KB；案例 {ncases} 个")
  sync_docs(full, kb)
  principles = next(e for e in full if e["id"] == "01-principles")["body"] + "\n"
  ref = ROOT / "skill" / "reference" / "principles.md"
  if ref.parent.exists() and (not ref.exists() or ref.read_text(encoding="utf-8") != principles):
    ref.write_text(principles, encoding="utf-8")
    print("已更新 skill/reference/principles.md")
  if kb > BUDGET_FAIL_KB:
    print(f"all.json 超过 {BUDGET_FAIL_KB} KB 上限：合并或精简条目，不要再加。见 BACKLOG.md 的 Size budget。"); sys.exit(1)
  if kb > BUDGET_WARN_KB:
    print(f"注意：all.json 超过 {BUDGET_WARN_KB} KB，优先合并和精简。")

if __name__ == "__main__":
  main()
