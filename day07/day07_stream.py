# Day 07：流式输出（打字机效果）
# 运行：D:\python\python.exe C:\Users\admin\Desktop\AI-30Days\day07\day07_stream.py
# 输入 quit 退出。每轮 API 请求都关闭思考模式以控制学习成本。

import os
import time

from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

api_key = os.environ.get("DEEPSEEK_API_KEY")
if not api_key:
    raise SystemExit("没读到 DEEPSEEK_API_KEY：请检查环境变量并重开终端")

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
messages: list[ChatCompletionMessageParam] = [
    {"role": "system", "content": "你是一个简洁、友好的助手。"},
]

print("流式聊天助手已启动，输入 quit 退出。\n")

while True:
    user_input = input("你: ").strip()
    if user_input.lower() in ("quit", "exit", "q"):
        print("已退出。")
        break
    if not user_input:
        continue

    messages.append({"role": "user", "content": user_input})

    # 每轮单独计时，并重新等待本轮的第一段文字。
    start_time = time.perf_counter()
    first_piece = True

    stream = client.chat.completions.create(
        model="deepseek-flash",
        messages=messages,
        stream=True,
        extra_body={"thinking": {"type": "disabled"}},
    )

    print("AI: ", end="", flush=True)
    reply_parts: list[str] = []

    for chunk in stream:
        piece = chunk.choices[0].delta.content
        if piece:
            if first_piece:
                print(f"[首段等待 {time.perf_counter() - start_time:.2f} 秒]")
                first_piece = False

            # 每一段都要打印；不能缩进到 if first_piece 里面。
            print(piece, end="", flush=True)
            reply_parts.append(piece)

    print("\n")

    # 保存完整回复，下一轮模型才能接着对话。
    reply = "".join(reply_parts)
    messages.append({"role": "assistant", "content": reply})
