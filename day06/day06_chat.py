# Day 06：上下文管理 —— 治好"历史无限变长"
# ---------------------------------------------------------------
# 前两天的成果：记忆存在 messages 里（Day 04），还能存到硬盘（Day 05）。
# 但那个列表会无限变长：聊 50 轮之后，每一轮都要把全部历史重发一遍。
#   → 钱越花越多（输入 token 一轮轮往上涨，你已经亲眼看到了）
#   → 效果反而可能变差（一大堆无关旧内容会干扰模型）
#
# 今天的核心思路只有一句话：
#     【存档保留全部，发送只给最近几轮】
#
# 3 个新知识点：
#   1. 裁剪 = 发请求之前，另造一个"精简版"列表，不改动原来的完整列表
#   2. "数据保留"和"请求内容"分开设计 —— 这是工程上非常重要的习惯
#   3. 代价：被裁掉的内容，模型就真的忘了。记忆和成本要权衡
#
# 跑起来后请做这 4 个实验：
#   1. 连着聊 8 轮，盯住每轮的"完整历史 N 条 / 本次发送 M 条"
#      —— M 涨到 13 条就封顶了（1 条 system + 6 轮 × 2 条），不再增长
#   2. 第 1 轮就告诉它一个信息（比如"我叫小明"），聊到第 8 轮再问它
#      —— 它忘了。这就是省钱的代价，把这个权衡记住
#   3. 把 MAX_TURNS 改成 20，重聊一遍，看 token 涨得多快
#   4. 用记事本打开 history.json 检查：里面依然是【完整】的全部对话
#      —— 存档不裁剪，只有发给模型的才裁剪
# ---------------------------------------------------------------

import json
import os

from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

# 每次最多发给模型最近多少轮对话（1 轮 = 你一句 + AI 一句）
# 想体验"不裁剪"，把它设成 0 即可
MAX_TURNS = 6

# 是否打印每一轮真正寄出去的内容
SHOW_MESSAGES = True

api_key = os.environ.get("DEEPSEEK_API_KEY")
if not api_key:
    raise SystemExit("没读到 DEEPSEEK_API_KEY：请先 setx，然后关闭并重开 VS Code")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com",
)

HISTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "history.json")
SYSTEM_PROMPT = "你是一个简洁的中文AI助手，回答控制在三句话以内。"


def build_payload(
    messages: list[ChatCompletionMessageParam],
    max_turns: int,
) -> list[ChatCompletionMessageParam]:
    """构造真正发给模型的消息：system + 最近 max_turns 轮对话。

    注意：这个函数只返回一个新列表，绝不修改传进来的 messages。
    完整历史要留给存档用 —— 裁掉 = 你自己也丢了记录，那是灾难。
    """
    system_msgs = [m for m in messages if m["role"] == "system"]
    dialog = [m for m in messages if m["role"] != "system"]

    if max_turns > 0 and len(dialog) > max_turns * 2:
        dialog = dialog[-max_turns * 2:]

        # 裁剪之后，开头可能落到一条 assistant 上。
        # 原因：发请求时历史长度总是奇数（最后一条是你刚说的话），
        # 而裁掉的是偶数条，所以开头会错位。
        # 历史必须以"用户的话"开头 —— 把开头多出来的 assistant 丢掉。
        # （实测 DeepSeek 能容忍以 assistant 开头的历史，但别的服务商
        #   可能直接报错，规范做法就是丢干净。）
        while dialog and dialog[0]["role"] != "user":
            dialog.pop(0)

    return system_msgs + dialog


# 类型标注：只给 Pylance 看，不影响运行
messages: list[ChatCompletionMessageParam]

# 1) 启动时：有存档就读回来，没有就从零开始
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        messages = json.load(f)
    print(f"已读取存档，共 {len(messages)} 条历史消息，接着上次聊。")
else:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    print("没有找到存档，开始一段新对话。")

print(f"本次设置：每次最多发送最近 {MAX_TURNS} 轮对话（0 = 不裁剪）")
print("输入 quit 退出（退出时自动保存）。\n")

turn = 0

while True:
    user_input = input("你: ").strip()

    if user_input.lower() in ("quit", "exit", "q"):
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
        print(f"已保存 {len(messages)} 条历史消息（完整版）到存档，下次接着聊。")
        break

    if not user_input:
        continue

    # 2) 把用户这句话存进【完整历史】
    messages.append({"role": "user", "content": user_input})

    # 3) 裁剪出一个精简版，只用于这次请求
    payload = build_payload(messages, MAX_TURNS)

    if SHOW_MESSAGES:
        print(f"  ┌─ 本次寄出去的内容（完整历史 {len(messages)} 条 → 实际发送 {len(payload)} 条）")
        for i, m in enumerate(payload, 1):
            print(f"  │ {i}. {m['role']:9s} | {m['content']}")
        print("  └─ 模型看到的就只有上面这些")

    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=payload,  # ← 注意这里发的是 payload，不是 messages
        extra_body={"thinking": {"type": "disabled"}},  # 学习阶段关掉思考模式：更快、更省
    )

    reply = response.choices[0].message.content

    # 4) AI 的回复照样进【完整历史】
    messages.append({"role": "assistant", "content": reply})

    turn += 1
    print("AI:", reply)

    # usage 的类型是 Optional（理论上可能是 None）。先取出来判断一下，
    # 既写清了"非流式请求一定会返回用量"这个前提，也让类型检查器放心。
    usage = response.usage
    if usage:
        print(
            f"   [第 {turn} 轮 · 输入 {usage.prompt_tokens} tokens"
            f" / 输出 {usage.completion_tokens} tokens"
            f" / 存档共 {len(messages)} 条]\n"
        )
