# Day 04：多轮聊天助手
# ---------------------------------------------------------------
# 运行方式：按 F5（或右上角 ▶）。你的 VS Code 没有 launch.json，
# 用的是默认"集成终端"控制台，所以 input() 可以正常输入。
# 如果 input() 卡住打不进字，说明控制台被切到了"调试控制台"，
# 改用菜单：终端 → 新建终端，然后执行  python day04\day04_chat.py
#
# 跑起来后请做这 4 个实验（做完才算真学会）：
#   1. 验证记忆：先说"我叫小明"，下一句问"我叫什么？"
#   2. 盯住每轮打印的 token 数字，看它一轮轮涨上去 —— 这就是成本来源
#   3. 看清"失忆"的真相（这条注释第一版写错了，已修正）：
#      把下面标着【实验3】的那行注释掉，然后问【AI 自己说过什么】，例如：
#        Q1: 从1到100随便说一个数字，只回答数字  → 它说 37
#        Q2: 你刚才说的是哪个数字？              → 保留那行 = 37；注释掉后它会现编（实测答 28）
#      ⚠️ 别用"我刚才问了你什么"来测失忆！用户的话还在 messages 里，所以照样答得出来。
#      丢掉的只是 AI 自己说过的话 —— 模型没有记忆，它"记得自己说过什么"
#      完全依赖你把它的回复也发回去。
#   4. 改掉 system 那句话（比如"你是一只说话很欠的猫"），感受人设的力量
#   5. 看清"模型到底收到了什么"：看每轮打印出来的【寄出去的历史】，
#      那是理解上下文最直观的方式。看腻了就把下面的 SHOW_MESSAGES 改成 False
# ---------------------------------------------------------------

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

# 开关：是否把每一轮"寄给模型的历史"打印出来。
# 亲眼看清模型到底收到了什么，是理解上下文最有效的方式。嫌吵就改成 False。
SHOW_MESSAGES = True

# 对话历史：这就是 AI 的"记忆"。
# 模型本身没有记忆，它的记忆完全来自你每一轮重新发给它的这段历史。
# 下面那行的 ": list[ChatCompletionMessageParam]" 是类型标注，只给 Pylance 看，
# 完全不影响运行。好处：以后 append 时角色名写错（比如 "boss"）会被当场标红。
messages: list[ChatCompletionMessageParam] = [
    {"role": "system", "content": "你是一只说话很欠的猫"},
]

print("多轮聊天助手已启动，输入 quit 退出。\n")

turn = 0

while True:
    user_input = input("你: ").strip()

    if user_input.lower() in ("quit", "exit", "q"):
        print(f"已退出，共进行了 {turn} 轮对话。")
        break
    if not user_input:
        continue

    # 1) 把用户这句话存进历史
    messages.append({"role": "user", "content": user_input})

    # 2) 把整段历史一起发给模型
    if SHOW_MESSAGES:
        print("  ┌─ 本轮寄出去的历史（这就是模型眼中的整个世界）")
        for i, m in enumerate(messages, 1):
            print(f"  │ {i}. {m['role']:9s} | {m['content']}")
        print("  └─ 模型自己没有记忆，它看到的就是上面这份打印件")

    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=messages,
        extra_body={"thinking": {"type": "disabled"}},  # 学习阶段关掉思考模式：更快、更省
    )

    reply = response.choices[0].message.content

    # 3) 【实验3】存下 AI 自己的回复。
    #    注释掉这一行，AI 下一轮就"不记得自己说过什么"，
    #    但它仍然记得你说过什么（因为你的话在上面的 append 里）。
    messages.append({"role": "assistant", "content": reply})

    # 排错技巧：看上面那段打印，如果连着出现两个 user、中间没有 assistant，
    # 就是历史缺了一段 —— 上下文出问题十有八九是这里。

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
