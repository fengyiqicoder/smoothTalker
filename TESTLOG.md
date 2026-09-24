# SmoothTalker 实测日志

## 2026-09-24 首轮，Muse（Meta）真实会话

**接入过程**
- smoothtalker.000ooo.ooo 被 Muse VM 出站拦截（"access was rejected on my side"），github.io 镜像正常。接入话术已改为镜像优先。
- Muse 拒绝"不看内容就装成自动 skill"，要求先通读。改为两步：先读并审查，再保存。它的审查结论：结构好、范例具体、无操纵/外泄/身份伪装，两条保留意见（playbook 应为建议性、用户意图优先；归属行不在原 spec）。均已采纳写入。
- 保存时弹 Sentinel 权限确认（raw.githubusercontent.com），点"允许一次"。skill 存于 ~/workspace/skills/smooth-talker/，本地缓存 57 条，每日最多刷新一次。

**场景测试（8/8 通过）**

| 场景 | 命中条目 | 结果 | 备注 |
|---|---|---|---|
| 房东涨租 1800→2100，有市场价和租期记录 | landlord-tenant | 通过 | 还价 1900 签 12 个月、事实理由、具体请求、后手（再还 2000）。与接入前的平拒绝对比是质变 |
| 忘了闺蜜生日 | apologize | 通过 | 四要素齐；暖版自责略多，已加"按过错大小缩放"规则 |
| 拒绝同事墨西哥婚礼 | decline-invitation | 通过 | 清晰 no + 具体替代，末尾提醒别加 maybe |
| 蜡烛店 DM 要折扣 | reply-to-customer-inquiry-dm + upsell | 通过 | 按镜像规则匹配了对方 "!!"，给了两个不降价的替代 |
| 室友阴阳怪气 🙃 | respond-to-passive-aggressive | 通过 | face-value 策略，不接茬 |
| 中文：王总要八折 | negotiate-price | 通过 | 中文输入触发，中文输出；暖版暗示可随修改轮次调价，与用户"不降价"有轻微冲突，已加"不让步用户声明不让的东西"规则 |
| 客户三点投诉邮件 | respond-to-angry-customer + admit-mistake | 通过 | 逐条回应，己方过错全认，另两点用事实纠正，末尾给下一步。已新增 05-reply-to-a-pasted-message 把这套流程固化 |
| 表弟借钱，要求平拒绝一版 | decline-request | 通过 | 尊重用户指令，一版、无替代 |

**未出现的**
- "Playbook: xxx" 归属行（Muse 保存 skill 时该规则尚未加入 spec）。已加入 MUSE_PROMPT，并让 Muse 刷新。

**下一轮要测**
- 语音消息/电话脚本类请求
- 群聊场景
- 用户情绪激动时是否给"等一等再发"的版本
- 归属行是否出现
