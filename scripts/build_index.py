#!/usr/bin/env python3
"""校验 data/entries/*.json 并重新生成 data/index.json。"""
import json, sys, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENTRIES = ROOT / "data" / "entries"
INDEX = ROOT / "data" / "index.json"
REQUIRED = ["id", "title", "summary", "body"]

items, errors = [], []
for p in sorted(ENTRIES.glob("*.json")):
    try:
        e = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as ex:
        errors.append(f"{p.name}: JSON 解析失败 {ex}"); continue
    for k in REQUIRED:
        if not e.get(k):
            errors.append(f"{p.name}: 缺少字段 {k}")
    if e.get("id") != p.stem:
        errors.append(f"{p.name}: id 字段 ({e.get('id')}) 必须等于文件名 ({p.stem})")
    items.append({
        "id": e.get("id"),
        "title": e.get("title"),
        "tags": e.get("tags", []),
        "summary": e.get("summary"),
        "updated": e.get("updated"),
    })

if errors:
    print("校验失败："); [print("  -", x) for x in errors]; sys.exit(1)

INDEX.write_text(json.dumps({
    "generated": datetime.date.today().isoformat(),
    "count": len(items),
    "entries": items,
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"已生成 {INDEX.relative_to(ROOT)}，共 {len(items)} 条")
