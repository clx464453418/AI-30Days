# Day 05：给聊天助手装上"长期记忆"
# ---------------------------------------------------------------
# Day 04 你学到的：记忆不在模型里，记忆在你的 messages 列表里。
# 但那个列表只活在程序运行期间 —— 关掉窗口就全没了。
# 今天的任务：把这份列表写到硬盘上，下次打开还能接着聊。
#
# 3 个新知识点：
#   1. json.dump / json.load —— 把 Python 的列表存成文件，再原样读回来
#   2. open(..., encoding="utf-8") —— Windows 上读写中文必须指定编码，
#      否则就会遇到你第一天那个 ascii codec 错误的同类问题
#   3. os.path.exists —— 第一次运行时没有存档，程序要能正常开始
#
# 跑起来后请做这 4 个实验：
#   1. 聊两句 → 输入 quit → 再按 F5 运行一次 → 看它记不记得你
#   2. 用记事本打开 history.json 看看里面到底是什么（就是那份"打印件"本身）
#   3. 把 history.json 里的一句话改掉（比如把你的名字改成别人的），再运行
#      —— 模型会无条件相信你改过的内容。这是理解 RAG 的第一步：喂什么，它就信什么
#   4. 把 history.json 删掉，再运行 —— 它失忆了，从零开始（存档没了）
#
# 注意：历史会一直变长，token 会一轮轮涨。
# 真实的 AI 产品必须处理"历史太长"的问题（裁剪 / 摘要），那是 Day 06 的事。
# ---------------------------------------------------------------

import json
import os

from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

api_key = os.environ.get("DEEPSEEK_API_KEY")
if not api_key:
    raise SystemExit("没读到 DEEPSEEK_API_KEY：请先 setx，然后关闭并重开 VS Code")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com",
)

# 存档文件固定放在"代码所在的文件夹"，不管你从哪里运行都不会找错地方
HISTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "history.json")

SYSTEM_PROMPT = "你是一个简洁的中文AI助手，回答控制在三句话以内。"

# 类型标注：只给 Pylance 看，不影响运行。
# 它把 messages 的类型在整个文件里明确下来，"角色名写错"会被当场标红。
messages: list[ChatCompletionMessageParam]

# 1) 启动时：有存档就读回来，没有就从零开始
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        messages = json.load(f)
    print(f"已读取存档，共 {len(messages)} 条历史消息，接着上次聊。")
else:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    print("没有找到存档，开始一段新对话。")

print("输入 quit 退出（退出时会自动保存）。\n")

turn = 0

while True:
    user_input = input("你: ").strip()

    if user_input.lower() in ("quit", "exit", "q"):
        # 2) 退出前：把整段历史写进文件。ensure_ascii=False 让中文原样保存
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
        print(f"已保存 {len(messages)} 条历史消息，下次打开接着聊。")
        break

    if not user_input:
        continue

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=messages,
        extra_body={"thinking": {"type": "disabled"}},  # 学习阶段关掉思考模式：更快、更省
    )

    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})

    turn += 1
    print("AI:", reply)

    # usage 的类型是 Optional（理论上可能是 None）。先取出来判断一下，
    # 既写清了"非流式请求一定会返回用量"这个前提，也让类型检查器放心。
    usage = response.usage
    if usage:
        print(
            f"   [第 {turn} 轮 · 输入 {usage.prompt_tokens} tokens"
            f" / 输出 {usage.completion_tokens} tokens]\n"
        )
