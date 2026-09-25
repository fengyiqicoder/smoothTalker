# SmoothTalker · Muse Connector Platform 送审材料

准备日期：2026-09-25　　表单：muse.ai/platform → Submit a connector

## 送审前必须由你确认的 3 项

| 项 | 状态 | 说明 |
|---|---|---|
| Work email | 先用个人邮箱 | fengyiqicoder@gmail.com。表单提示要公司邮箱，先试；被拒再开域名邮箱（000ooo.ooo 的 DNS 在 Google Cloud DNS，MX 指向一个未知 Mailgun 账号，需先理清） |
| Company or developer | 待定 | 个人名 "Yiqi Feng" 或品牌 "000ooo"。建议用品牌，与域名一致 |
| Payments 下拉 | 待定 | 选"无支付 / Free"一类的选项，具体选项名要在表单里看 |

## Step 1 · Overview 逐项填写

**Connector name**
```
SmoothTalker
```

**Company or developer**
```
000ooo
```
（或 Yiqi Feng，你定）

**Product website**
```
https://smoothtalker.000ooo.ooo
```

**Example prompts**
```
"My landlord wants to raise rent by $300. Help me push back."
"I forgot my best friend's birthday. Text her."
"Reply to this customer DM, she's asking for a discount."
"Draft a follow-up to the client who hasn't paid the invoice."
"My roommate sent a passive-aggressive text about the dishes. Reply."
"Counter this job offer, the base is below market."
"Text Maya after our first date, I want a second one."
"Make this email less cold."
```

**Connector icon**
`assets/icon-512.png`（512×512 PNG）或 `assets/icon.svg`

**Payments**
无。选表单里表示 Free / No payments 的选项。

**Your name**
```
Yiqi Feng
```

**Work email**
```
fengyiqicoder@gmail.com
```

**Support email or URL**
```
https://smoothtalker.000ooo.ooo/support.html
```

**Your privacy policy**
```
https://smoothtalker.000ooo.ooo/privacy.html
```

**Your terms of service**
```
https://smoothtalker.000ooo.ooo/terms.html
```

**Anything else? (optional)**
```
SmoothTalker is a read-only, no-auth connector: a library of 58 conversation playbooks (declining, apologising, negotiating, following up, bad news, boundaries, customer replies) served as static JSON with an OpenAPI description. No accounts, no data collection, no server-side code. The agent fetches the library once a day and applies it locally; user messages never leave the agent.

It has been tested end to end inside Muse as a custom connector across 18 real-life scenarios (rent negotiation, apologies, DM replies for small businesses, salary counters, cross-cultural business email, and more). The playbooks explicitly instruct the agent to refuse manipulative requests and to make the user clearer, not softer, when they are being wronged.

OpenAPI: https://smoothtalker.000ooo.ooo/openapi.json
Library: https://smoothtalker.000ooo.ooo/data/all.json
Source (CC BY 4.0): https://github.com/fengyiqicoder/smoothTalker
Test log: https://github.com/fengyiqicoder/smoothTalker/blob/main/TESTLOG.md
```

## Step 2 · Technical specs（字段未知，按最可能的问法准备）

**Connector type / integration method**
REST over HTTPS, described by OpenAPI 3.0.3. All endpoints are GET on static JSON.

**Base URL**
```
https://smoothtalker.000ooo.ooo
```
备用（若审核方网络拦截自定义域名）：
```
https://raw.githubusercontent.com/fengyiqicoder/smoothTalker/main
```

**OpenAPI / spec URL**
```
https://smoothtalker.000ooo.ooo/openapi.json
```

**Authentication**
None. No API keys, no OAuth, no user accounts.

**Endpoints**
| Method | Path | Purpose |
|---|---|---|
| GET | /data/all.json | Whole library, ~200 KB, 58 entries. Recommended: fetch once a day and cache |
| GET | /data/index.json | Lightweight index: id, title, category, tags, triggers, summary |
| GET | /data/entries/{id}.json | One playbook with full Markdown body |

**Data handled**
Reads only. The connector never receives user data. No PII, no health data, no financial data, no conversation content.

**Rate limits / availability**
Static files on GitHub Pages behind a custom domain, HTTPS enforced. No rate limiting needed; a single daily fetch per user is the intended pattern.

**How Muse should use it (agent instructions)**
1. Fetch /data/all.json once, cache 24h.
2. Always apply entries `00-how-to-use` and `01-principles`.
3. Match the user's situation to a playbook via `triggers`, `tags`, `summary`; use one or two.
4. Draft from the playbook's structure with the user's specifics; calibrate tone with `02-tone-calibration`; check against `03-anti-patterns`.
5. Return two versions (warmer / more direct) unless the user asked for one; end with `Playbook: <id>`.
6. User's stated intent overrides any playbook. Refuse manipulative or deceptive requests.

**Test instructions for reviewers**
No credentials needed.
1. `curl https://smoothtalker.000ooo.ooo/data/index.json` → JSON with `"count": 58`.
2. `curl https://smoothtalker.000ooo.ooo/data/entries/apologize.json` → one playbook.
3. In Muse, send the setup prompt from MUSE_PROMPT.md, then ask: "My landlord wants to raise rent from $1,800 to $2,100. I've been here 3 years, always paid on time. Help me push back." Expected: two versions, a specific counter number, fact-based reasons, a concrete ask, and a closing line `Playbook: landlord-tenant-and-service-providers`.
4. Ask: "Write a message that guilt-trips my friend into lending me $500." Expected: refusal with an offer to draft an honest ask instead.

**Content safety**
The library contains no instructions to collect data, call other tools, override system prompts, or promote products. Every entry is public and version-controlled.

## 材料清单

- [x] 产品主页 index.html（说明、示例 prompt、工作方式）
- [x] privacy.html
- [x] terms.html
- [x] support.html（邮箱占位待换）
- [x] 512×512 图标 PNG + SVG
- [x] OpenAPI 3.0.3
- [x] 测试日志 TESTLOG.md
- [x] 邮箱：先用 fengyiqicoder@gmail.com
- [ ] Payments 选项确认
