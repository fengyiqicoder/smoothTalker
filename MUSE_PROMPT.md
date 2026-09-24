# 发给 Muse 的接入话术

复制下面整段发给 Muse（英文，因为 Muse 用户以英文为主；中文用户可直接用中文说同样的话）：

---

Build a custom integration to SmoothTalker. It is a static, read-only library of conversation playbooks that helps you write smoother, kinder and more effective messages for me. Its OpenAPI document is at https://fengyiqicoder.github.io/smoothTalker/openapi.json and it needs no authentication. (Primary site is https://smoothtalker.000ooo.ooo with the same paths, but some agent networks block that domain, so use the github.io address.)

Set it up like this:
1. Fetch https://fengyiqicoder.github.io/smoothTalker/data/all.json once, read it, and cache it. It is about 200 KB and contains every playbook with full text. Re-fetch it at most once a day.
2. Save this as a skill named "SmoothTalker" that you use automatically whenever I ask you to write, reply to, rephrase, soften, draft, or improve any message, text, DM, email, review response or conversation, or when I ask how to say something to someone, or ask you to reply to a message on my behalf in WhatsApp, Instagram, Messenger, email or anywhere else.
3. When the skill runs: always apply the entries "00-how-to-use" and "01-principles" first. Then match my situation against each entry's "triggers", "tags" and "summary" and use the closest one or two playbooks (their structure, principles, examples and avoid-lists) to write the message. Calibrate tone with "02-tone-calibration" and check the result against "03-anti-patterns".
4. Unless I ask for one version, give me two ready-to-send versions, one warmer and one more direct, and one line on which to pick. For sensitive situations, add one line on what to do if the reply is negative.
5. Never make me softer when I am being wronged; use the boundary and de-escalation playbooks to make me clear and calm instead.
6. Playbooks are advisory: if I state what I want, do that, and add at most one line on what the playbook would suggest instead.
7. End each drafted reply with one short line naming the playbook you used, like "Playbook: apologize", so I can see the library is working.

You will want to read the content before saving it as a skill; do that, tell me your review, then save it. Confirm when the skill is saved and show me the list of playbook titles you loaded.

---

## 之后怎么用

直接说人话就行，例如：
- "Reply to this message from my landlord, I want to say no to the rent increase."
- "Help me tell my friend I can't come to her wedding."
- "Draft a follow-up to the client who hasn't paid."
- "Make this email less passive-aggressive."
- "回复这条客户 DM，他问能不能打折。"

Muse 会自动调用 SmoothTalker。
