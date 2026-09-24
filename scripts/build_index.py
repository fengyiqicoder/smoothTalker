#!/usr/bin/env python3
"""content/*.md（front matter + Markdown 正文）→ data/entries/<id>.json、data/index.json、data/all.json"""
import json, sys, datetime, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
ENTRIES = ROOT / "data" / "entries"
INDEX = ROOT / "data" / "index.json"
ALL = ROOT / "data" / "all.json"
REQUIRED = ["title", "summary", "tags", "triggers"]

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
INDEX.write_text(json.dumps({"generated": today, "count": len(items), "read_first": ["00-how-to-use", "01-principles"], "entries": items}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
ALL.write_text(json.dumps({"generated": today, "count": len(full), "read_first": ["00-how-to-use", "01-principles"], "entries": full}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"已生成 {len(items)} 条；all.json {ALL.stat().st_size // 1024} KB")
