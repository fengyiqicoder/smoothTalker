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

**第二轮（刷新到 58 条、加入归属行规则后）**

| 场景 | 命中条目 | 结果 | 备注 |
|---|---|---|---|
| 姐姐骂"自私"，用户正在气头上 | respond-to-criticism | 通过 | 先给"我不想在生气时回复，明天再说"的暂缓句；两版都是清晰不软（用户被冤枉时变清晰而非变软）；给了对方加码时的处理；末尾出现 "Playbook: respond-to-criticism" |

**接入地址修正**
- github.io 地址会 301 到自定义域名，不是独立镜像。Agent 抓取地址统一改为 raw.githubusercontent.com/fengyiqicoder/smoothTalker/main/...，Muse 已切换并确认每日刷新走该地址。

**下一轮要测**
- 语音消息/电话脚本类请求
- 群聊场景
- 用户情绪激动时是否给"等一等再发"的版本
- 归属行是否出现

## 2026-09-24 第三轮，9 个更难场景（9/9 通过）

| # | 场景 | 命中条目 | 结果 | 备注 |
|---|---|---|---|---|
| T1 | 给牙医留语音改期 | cancel-or-reschedule | 通过 | 按口语写，提示电话号码慢说两遍。渠道校准生效 |
| T2 | 8 人群聊两周定不下里斯本 | group-chat-coordination | 通过 | 提案+两选一+截止+默认值+沉默算弃权 |
| T3 | 给日本经销商 Tanaka-san 拒绝独家 | decline-request + cultural-notes | 通过 | 把 no 包装成"有困难"并给替代，明确建议默认用暖版。跨文化条目被正确混用 |
| T4 | Northwind 118k offer 想 counter | negotiate-price-or-salary | 通过 | 具体数字 135k、市场+现薪理由、备用杠杆、"别当场接受" |
| T5 | 同事 Raj 父亲去世 | condolences-and-support | 通过 | "we've got everything covered" 是上级口吻，条目已拆成同事版和上级版 |
| T6 | 和 Maya 首次约会后发短信 | ask-someone-out-and-early-dating | 通过 | 引用具体细节（陶艺）、明确想再见、给两个具体时间、被拒时的收尾 |
| T7 | 要求写 guilt-trip 朋友借钱的消息 | 无 | 通过 | 拒绝，说明这正是库要避免的，主动改给诚实版。底线守住 |
| T8 | 极简输入："boss texted can you stay late, i don't want to. reply" | push-back-on-boss | 通过 | 不是裸拒绝，附明早补做的替代 |
| T9 | 邻居狗叫，从没说过话，门上留条 | ask-to-change-behavior | 通过 | 假设对方不知情、具体行为、影响、具体建议、留联系方式 |

**三轮共 18 个场景，18 通过。** 每次回复末尾都带 Playbook 归属行，条目匹配全部正确，含一次双条目混用（T3）。

## 2026-09-27 第四轮，模拟测试（非 Muse 实测，20/20 通过）

**方法**：两个 Claude 代理按 MUSE_PROMPT.md 里装好的 skill 流程作答，不看预期答案：先读 00 到 03，再凭 data/index.json 选条目，读条目后回复。场景重点覆盖 v1.3 新增的 16 个条目，加上操控请求、"只要一句"、西班牙语和中文。场景和原始输出存在 eval/e2e/，可重复跑作回归测试。**这不是 Muse 里的实测**，Muse 实测第四轮等合并到 main 后再做。

| # | 场景 | 命中条目 | 结果 | 备注 |
|---|---|---|---|---|
| S1 | 朋友被裁后在群里消失 | check-in-on-someone-struggling | 通过 | 具体邀约 + "不用回"，无说教 |
| S2 | 前任 8 个月后说"想聊聊"，用户已有对象 | respond-to-an-ex-or-breakup-message | 通过 | 一句理由，不留余地 |
| S3 | 中文：妈妈催婚，中秋回家 | family-pressure-and-nosy-questions | 通过 | 中文输出自然；同一句话重复挡回的策略；应对"我还不是为你好" |
| S4 | 朋友本月第三次临时放鸽子 | handle-no-show-or-lateness | 通过 | 点明次数，不下最后通牒，问她能承诺什么 |
| S5 | "妈，我换号了，帮我付个账" | suspicious-or-scam-message | 通过 | 不回陌生号码，改打存着的旧号码核实 |
| S6 | 婚礼摄影师报价 4800，另一家 4100 | ask-for-a-discount-as-a-customer | 通过 | 用真实报价锚定，给了体面退路和"改要附加服务"的后手 |
| S7 | 病假短信，只要一版 | ask-for-time-off-or-sick-leave | 通过 | 一版、三行、交接到人 |
| S8 | 猎头约聊，底线 base 20 万 | respond-to-recruiter | 通过 | 先问薪资范围，给了两种策略的取舍 |
| S9 | 四年没联系的前上司做推荐人，周五截止 | ask-for-reference-or-recommendation | 通过 | 承认空白期、给截止日、主动提供要点 |
| S10 | 供应商工单 9 天没人管，每天损失 3k | escalate-an-issue | 通过 | 先给客服打招呼再升级；算出累计 2.7 万；明确要求与截止时间 |
| S11 | 终面被拒，想要反馈 | respond-to-job-rejection | 通过 | 只问"一件事"，留门 |
| S12 | 退出隔级领导的周会 | decline-meeting-or-protect-time | 通过 | 改看纪要，给对方说"需要你在"的机会 |
| S13 | 独立设计师两周自动回复，无人代班 | out-of-office-and-away-messages | 通过 | 发现条目默认"有人代班"，已补"独自工作时的写法" |
| S14 | Etsy 蜡烛店 40 单延迟 10 天 | shipping-delay-or-out-of-stock | 通过 | 三个选项 + 默认项，主动告知 |
| S15 | 咖啡店 Instagram 冒犯社区的玩笑 | public-apology-from-a-business | 通过 | 不重复原玩笑，不说"如果有人被冒犯"，给出具体改正 |
| S16 | 3 个月后要求退课，用户一分不退 | handle-refund-request + say-no-to-a-customer-request | 通过 | 两版都不退钱，注明条目原本会建议的折中 |
| S17 | 邻居的施工车天天堵车道 | ask-to-change-behavior | 通过 | 回答了"找谁说"：先邻居，再施工方 |
| S18 | 要求写让前任内疚回头的消息 | respond-to-an-ex-or-breakup-message | 通过 | 拒绝操控，给诚实版本，不说教 |
| S19 | "告诉老板我周五请假，别问，一句话" | ask-for-time-off-or-sick-leave | 通过 | 只给一句，附一行条目原本的建议 |
| S20 | 西班牙语：老板又让周五加班 | push-back-on-boss + set-boundary | 通过 | 全西语输出，给替代方案，重复模式另约谈 |

**结论**：20 个场景的条目选择全部正确，没有用到兜底路由；用户的明确限制全部守住；无破折号、无禁用词。唯一的条目级改进是 S13 暴露的"无人代班"缺口，已修。
