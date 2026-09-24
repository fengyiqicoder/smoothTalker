#!/bin/bash
# 用法: muse_test.sh "prompt"  —— 发给当前 Muse 会话并等待回复，输出回复文本
MSG="$1"
browser-use <<PY
click_at_xy(936, 883)
import time; time.sleep(0.4)
type_text("""$MSG""")
time.sleep(0.4)
press_key("Enter")
PY
sleep 8
for i in $(seq 1 30); do out=$(browser-use <<PY
t = js("document.body.innerText")
marker = """$MSG"""
i = t.rfind(marker)
tail = t[i+len(marker):] if i>=0 else ""
tail = tail.replace("\n\n👍","",1)
cut = tail.find("\nMuse\n")
body = (tail[:cut] if cut>0 else tail).strip()
state = t[cut+6:cut+40].strip().split("\n")[0] if cut>0 else "?"
print("STATE:", state); print("LEN:", len(body)); print(body[:8000])
PY
); ln=$(echo "$out" | sed -n 2p | awk '{print $2}'); st=$(echo "$out" | sed -n 1p)
if echo "$out" | grep -q "允许一次"; then echo "APPROVAL PROMPT"; echo "$out" | tail -8; exit 2; fi
if [ "${ln:-0}" -gt 80 ] && ! echo "$st" | grep -qE "努力工作中|刷新|需要审核|正在"; then echo "$out" | tail -n +3; exit 0; fi
sleep 12; done; echo "TIMEOUT ($st)"; echo "$out" | tail -n +3; exit 1
