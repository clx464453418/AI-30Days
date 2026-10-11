# AI-30Days 学习记录

我的 AI 应用开发学习记录。主线：**Python 调用大模型 → 多轮对话 → 持久记忆 → 上下文管理**。

## 目录结构

| 文件夹 | 主题 | 文件 |
| --- | --- | --- |
| `day01/` | Python 基础：输入输出 | `day01.py` |
| `day02/` | Python 基础：循环、列表 | `day02.py`、`day02_for.py`、`day02_list.py`、`day02_while.py` |
| `day03/` | 函数、模块，第一次调用真实 AI | `day03def.py`、`day03import.py`、`day03_aiapi.py` |
| `day04/` | 多轮聊天助手（理解 `messages`） | `day04_chat.py` |
| `day05/` | 持久记忆（存到硬盘） | `day05_chat.py` |
| `day06/` | 上下文管理（裁剪历史） | `day06_chat.py` |
| `day07/` | 流式输出与首段等待 | `day07_stream.py` |
| `资料库/` | 项目学习进度与换电脑指南 | Markdown 文档 |
| `ollama/` | **支线**：本地模型（Ollama）—— 不花钱、不联网 | `ollama_chat.py`、`start_ollama.ps1`、`stop_ollama.ps1` |

## 怎么运行

在 VS Code 里打开某个文件，按右上角 **▶（运行 Python 文件）** 即可。

在仓库根目录打开终端后运行：

```powershell
python day04\day04_chat.py
```

> `day05` / `day06` 会在**自己所在的文件夹**里生成 `history.json` 存档 ——
> 也就是说两天的记忆是**各自独立**的，互不影响。

## 环境

| 项 | 值 |
| --- | --- |
| Python | 3.13（当前验证版本：3.13.16） |
| 依赖 | `openai` |
| 模型 | DeepSeek `deepseek-flash`（OpenAI 兼容格式） |
| Key | 存在 Windows 环境变量 `DEEPSEEK_API_KEY`，**代码里不出现明文** |
| 省钱 | 学习阶段一律加 `extra_body={"thinking": {"type": "disabled"}}` |

## 每天的关键收获

**Day 03 — 模型可替换，接口不变**
换厂商只改三个地方：`api_key`、`base_url`、`model`。OpenAI SDK 的代码结构可以原样用到 DeepSeek / 千问 / 本地 Ollama 上。

**Day 04 — 模型没有记忆**
它的"记忆"完全来自你每一轮重新发给它的 `messages` 列表。
- `system` 是**我的地盘**（模型永远不能自己产生 system 消息）
- `assistant` 是**模型的地盘**
- 而 **`messages` 历史是可以被伪造的** —— 喂什么，它就信什么
- 幻觉最危险的地方：**猜对了的时候，你完全看不出来它在猜**

**Day 05 — "长期记忆"的真相**
把 `messages` 列表写进 json 文件，下次读回来再整份发出去 —— 这就是市面上"AI 记得你"的底层机制。

**Day 06 — 上下文是有限资源**
**存档保留全部，发送只给最近几轮。** 想省钱就得忘事，想记住就得花钱 —— 这是所有 AI 产品设计的核心张力。

## 下一步

- 当前：day07 流式输出；先复习 `for` 循环与缩进，再继续理解流式片段和迭代器
- 之后：AI 助手项目 → RAG 知识库 → AI Agent → 作品集

## 项目资料库

可迁移的学习进度摘要和换电脑指南见 [`资料库/`](资料库/README.md)。
