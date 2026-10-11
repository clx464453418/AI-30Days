# Day 03：用 Python 调用真实的 AI（DeepSeek 版）—— 修正版
# ---------------------------------------------------------------
# 这一版修掉了三个问题：
#   1. Key 不再写死在代码里，改成读 Windows 环境变量 DEEPSEEK_API_KEY
#      → 代码可以随便给别人看 / 传到 GitHub，不会泄露
#   2. 模型名改对了：deepseek-chat（已过时）→ deepseek-flash（现在能用）
#   3. 终端编码坑：AI 回复里常带 emoji（😊🚀 等），Windows 终端默认 GBK 编码
#      打印时会直接抛 UnicodeEncodeError 崩掉。下面 safe_print() 专门处理它。
#      → 记住这个坑：程序"调用成功"但"打印失败"，钱已经花了却看不到回复。
#
# 跑之前必须做的事：
#   1. 确认环境变量已设置（只做一次）：
#        setx DEEPSEEK_API_KEY "你的key"
#   2. 设完要【关闭 VS Code，重新打开】—— setx 不会更新已开着的窗口
#
# 运行：
#   D:\python\python.exe day03_aiapi.py
# ---------------------------------------------------------------

import os
import sys

from openai import OpenAI


def safe_print(text: str) -> None:
    """打印文本；遇到终端编码装不下的字符（emoji 等）就换成 '?' 而不是崩掉。"""
    try:
        print(text)
    except UnicodeEncodeError:
        # 终端编码跟不上（例如 Windows 默认 GBK）时走这里
        encoding = sys.stdout.encoding or "utf-8"
        print(text.encode(encoding, errors="replace").decode(encoding, errors="replace"))


# 1) 从环境变量读 Key —— 这样 Key 永远不会出现在代码文件里
api_key = os.environ.get("DEEPSEEK_API_KEY")

if not api_key:
    raise SystemExit(
        "没读到 DEEPSEEK_API_KEY。\n"
        "请先在终端执行：setx DEEPSEEK_API_KEY \"你的key\"\n"
        "然后【关闭并重新打开 VS Code】，再运行本文件。"
    )

# 只打印结尾 4 位，方便确认读到了什么，又不会泄露完整 Key
safe_print(f"本次运行使用的 Key 结尾是: ...{api_key[-4:]}")

# 2) 连接 DeepSeek。注意 base_url：DeepSeek 兼容 OpenAI 的调用格式，
#    所以 openai 这个库可以继续用，只是把"发动机"换了。
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com",
)

try:
    # 3) 发一句话给模型
    response = client.chat.completions.create(
        model="deepseek-flash",          # ← 现在的模型名（旧名字 deepseek-chat 已不能用）
        messages=[{"role": "user", "content": "你好"}],
        extra_body={"thinking": {"type": "disabled"}},   # 学习阶段关掉思考模式：更快、更省
    )

    reply = response.choices[0].message.content
    safe_print("成功！AI回复：" + reply)

    # 4) 顺手看一眼花了多少 token —— 养成看成本的习惯
    usage = response.usage
    safe_print(
        f"（本次用量：输入 {usage.prompt_tokens} tokens"
        f" / 输出 {usage.completion_tokens} tokens"
        f" / 合计 {usage.total_tokens} tokens）"
    )

except Exception as e:
    # 出错时把原因原样打出来，别吞掉
    safe_print("依然报错：" + str(e))
