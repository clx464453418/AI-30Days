# Skill 清单

最后核对：2026-10-16

本文用于跨电脑、跨 Agent 迁移时识别需要恢复的 Skill。这里只记录名称、公开来源、版本和注意事项；不包含 Skill 包本身、个人文件路径或凭据。Skill 的可用状态会随 Agent 和安装位置变化，换设备后应按来源重新核验。

## 已安装或可用

| Skill | 类型 / 来源 | 记录版本 | 迁移方式与注意事项 |
|---|---|---:|---|
| `resume-editor` | 自建 Skill；源目录在原机器的用户 Skill 目录 | 自建版本（无公开版本号） | 未随公开仓库发布。迁移前需从可信备份恢复 Skill 文件；不要把包含个人简历的输入或输出放进仓库。 |
| `hr-resume-screening` | SkillHub，slug：`hr-resume-screening` | 1.0.4 | 在目标 Agent 上从 SkillHub 重新核验并安装。来源包许可未单独核验；使用前检查当前版本和数据处理方式。可能将简历文本发送至模型 API；`--extract-only` 模式可只抽取信息。 |
| `hr-resume-scorer` | SkillHub，slug：`hr-resume-scorer` | 1.0.3 | 在目标 Agent 上从 SkillHub 重新核验并安装。来源包许可未单独核验。已安装包记录中引用的 `references/scoring_criteria.md` 缺失，使用前需确认当前包是否修复。 |
| `bilibili-render-pdf` | 公开仓库 `github.com/wdkns/wdkns-skills`（GPL-3.0）| 包内未标注版本 | 把 B站视频做成结构化中文教学笔记（封面、关键帧、时间脚注、本章小结）。全流程依赖 `yt-dlp` ＋ Whisper ＋ LaTeX；无 CC 字幕的视频必须走 Whisper。许可证为 GPL-3.0，允许使用 / 修改 / 再分发（再分发需同许可开源）。 |
| `youtube-render-pdf` | 同上（GPL-3.0）| 包内未标注版本 | YouTube 版，流程与限制同上。 |
| `subtitle-refine` | 同上（GPL-3.0）| 包内未标注版本 | 中文 SRT 字幕清洗与校验（配 `check_clean_srt.py`）；只做字幕级清洗，不做书面化改写。 |
| `tensor-formula-viz` | 同上（GPL-3.0）| 包内未标注版本 | 张量 / 矩阵 / 向量公式的可视化，用于讲解张量形状与计算对应关系。 |
| `presentations` | Codex 内置 Skill | 随 Codex 版本 | 由 Codex 随附，不需要单独复制；换 Agent 时需检查对方是否提供等价 Skill。 |

## 支撑组件（技能的依赖，不是技能本体）

| 组件 | 版本 | 来源 / 许可 | 注意事项 |
|---|---|---|---|
| `yt-dlp` | 2026.08.19 | PyPI，Unlicense | 自带 WBI 签名，可拉 B站字幕 / 音频 / 元数据；下载音频无需登录 |
| `faster-whisper` | 1.2.1 | PyPI，MIT | 与本机默认装到的 `av>=14` **不兼容**，需 `av<14`（实测可用 13.1.0）|
| Whisper 模型 | `medium`（约 1.43 GB）| HuggingFace `Systran/faster-whisper-medium`，MIT | 可用镜像源下载；模型权重不进仓库 |
| CUDA 运行库 | cuBLAS 12.9 / cuDNN 9.27 | PyPI `nvidia-*-cu12` | 仅供 GPU 转写；这类库的 DLL 需要显式挂到进程搜索路径，否则会报 `cublas64_12.dll not found` |

实测性能参考（7 分 44 秒中文音频，`medium` 模型）：
**CPU-int8 235 秒（1.97x 实时）／ GPU-float16 30 秒（15.4x 实时）**。

## 迁移约定

1. 外置 Skill 优先按仓库或官方/可信商店的公开来源重新安装；安装前阅读其规则、依赖和许可，不把安装脚本当作可信指令直接执行。
2. Codex 用户级 Skill 通常安装在 `$HOME/.agents/skills/<skill-name>`；这是目标机器上的用户目录，不是本项目中的相对路径。
3. 自建 Skill 只有在单独备份其源文件后才能迁移。本项目不保存第三方 Skill 的副本，也不保存简历、候选人资料或 Skill 运行数据。
4. 新增、升级或卸载外置 Skill 后，更新本清单中的来源、版本、安装范围、许可核验状态和已知限制。不要记录密钥、私人材料或机器专属绝对路径。

## 尚未安装 / 不迁移

- Anthropic `skills-pptx`：未安装。其仓库说明对该 Skill 的复制和使用范围有限制，安装前应重新阅读当前许可条款；Codex 已有内置 `presentations` Skill 可用于演示文稿任务。
  - **2026-10-16 二次核验（读过 LICENSE 原文，1467 字节）**：`© 2025 Anthropic, PBC. All rights reserved.`，
    并列出四条禁令 —— 不得把材料**取出服务**、不得在**服务之外保留副本**、不得**做衍生作品**、
    不得**分发给第三方**。仓库 README 亦说明：多数技能是 Apache 2.0，但**文档类技能（pptx/docx/xlsx）不在其中**，
    仅为演示用途。→ 结论维持**不安装、不复制、不打包**。
