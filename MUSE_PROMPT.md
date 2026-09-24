# 发给 Muse 的接入话术

复制下面整段发给 Muse：

---

Build a custom integration to smoothTalker. It is a static read-only knowledge connector. Its OpenAPI document is at https://fengyiqicoder.github.io/smoothTalker/openapi.json and it needs no authentication.

I want you to be able to:
1. Fetch the full index at /data/index.json (it is small; load it entirely and filter by title, tags or summary yourself).
2. Fetch a single entry's full body at /data/entries/{id}.json when an index item looks relevant.

Save this as a skill so you can use smoothTalker in later conversations whenever I ask about topics covered by its entries.

---
