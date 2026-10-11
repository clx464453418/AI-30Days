# 本地模型支线：把对话程序接到 Ollama（注意：这【不是】day07，day07 = 流式输出）
# ---------------------------------------------------------------
# 这个文件和 day06_chat.py 是同一套逻辑，只有 4 个地方不一样，都在下面用
# 【改动 1~4】标出来了。对照着看，你就彻底明白"壳和模型是两层"。
#
# 运行前提：
#   1. 已安装 Ollama（https://ollama.com/download）
#   2. 已拉过至少一个模型，例如：ollama run qwen3:8b
#   3. Ollama 在后台运行（Windows 安装后会自动常驻）
#
# 运行：
#   D:\python\python.exe C:\Users\admin\Desktop\AI-30Days\ollama\ollama_chat.py
#
# 和 Day06 对比着看：
#   Day06 = 调用云端 DeepSeek（要 Key、要花钱、要联网）
#   本文件 = 调用本地 Ollama（不要 Key、不花钱、不联网）
#   两边的 Python 代码几乎一模一样 ← 这就是"换发动机"的含义
# ---------------------------------------------------------------

import json
import os

from openai import OpenAI

# 【改动 1】本地模型的地址和"假 Key"
#   Ollama 提供 OpenAI 兼容接口，所以 openai 这个库可以直接用。
#   注意 api_key：Ollama 要求填但不能为空，它不校验，随便写个字符串就行。
OLLAMA_BASE_URL = "http://localhost:11434/v1/"
OLLAMA_PLACEHOLDER_KEY = "ollama"

# 【改动 2】本地模型名 —— 必须和你 `ollama list` 里显示的名字一致
MODEL = "qwen3:8b"          # ← 换成你实际拉下来的那个名字

MAX_TURNS = 6               # 和 Day06 一样：只发最近 6 轮，省钱（本地是省时间）
SHOW_MESSAGES = True

client = OpenAI(
    api_key=OLLAMA_PLACEHOLDER_KEY,
    base_url=OLLAMA_BASE_URL,
)

HISTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "history_local.json")
SYSTEM_PROMPT = "你是一个简洁的中文AI助手，回答控制在三句话以内。"


def build_payload(messages, max_turns):
    """构造真正发给模型的消息：system + 最近 max_turns 轮。不改动原列表。"""
    system_msgs = [m for m in messages if m["role"] == "system"]
    dialog = [m for m in messages if m["role"] != "system"]

    if max_turns > 0 and len(dialog) > max_turns * 2:
        dialog = dialog[-max_turns * 2:]
        while dialog and dialog[0]["role"] != "user":
            dialog.pop(0)

    return system_msgs + dialog


# 1) 读存档（用的是另一个文件，不干扰 Day06 的存档）
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        messages = json.load(f)
    print(f"已读取本地存档，共 {len(messages)} 条历史消息，接着上次聊。")
else:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    print("没有找到存档，开始一段新对话。")

print(f"模型：{MODEL}（本地运行，不联网、不花钱）")
print("输入 quit 退出（退出时自动保存）。\n")

turn = 0

while True:
    user_input = input("你: ").strip()

    if user_input.lower() in ("quit", "exit", "q"):
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
        print(f"已保存 {len(messages)} 条历史消息到本地存档，下次接着聊。")
        break

    if not user_input:
        continue

    messages.append({"role": "user", "content": user_input})
    payload = build_payload(messages, MAX_TURNS)

    if SHOW_MESSAGES:
        print(f"  ┌─ 本次寄出去的内容（完整历史 {len(messages)} 条 → 实际发送 {len(payload)} 条）")

    # 【改动 3】调用方式一样，但去掉了 DeepSeek 专属的 thinking 参数
    #   extra_body={"thinking": ...} 是 DeepSeek 独有的，本地模型不认，会报错
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=payload,
        )
        reply = response.choices[0].message.content

    # 【改动 4】本地服务没起来时要给出人话提示，而不是一串看不懂的报错
    except Exception as e:
        print("  └─ 调用失败：", str(e)[:200])
        print(
            "     请检查：\n"
            "       1) Ollama 是否在运行（Ollama 图标是否在右下角托盘）\n"
            "       2) 模型名写对了吗？在终端执行 ollama list 看准确名字\n"
            "       3) 终端执行 ollama run <模型名> 能正常对话吗"
        )
        # 失败时把刚加进去的那句话撤掉，避免存档被坏数据污染
        messages.pop()
        continue

    messages.append({"role": "assistant", "content": reply})

    turn += 1
    print("AI:", reply)
    usage = getattr(response, "usage", None)
    if usage:
        print(
            f"   [第 {turn} 轮 · 输入 {usage.prompt_tokens} tokens"
            f" / 输出 {usage.completion_tokens} tokens"
            f" / 存档共 {len(messages)} 条]\n"
        )
    else:
        print(f"   [第 {turn} 轮 · 存档共 {len(messages)} 条]\n")
