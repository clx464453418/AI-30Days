# Skill 清单

最后核对：2026-10-11

本文用于跨电脑、跨 Agent 迁移时识别需要恢复的 Skill。这里只记录名称、公开来源、版本和注意事项；不包含 Skill 包本身、个人文件路径或凭据。Skill 的可用状态会随 Agent 和安装位置变化，换设备后应按来源重新核验。

## 已安装或可用

| Skill | 类型 / 来源 | 记录版本 | 迁移方式与注意事项 |
|---|---|---:|---|
| `resume-editor` | 自建 Skill；源目录在原机器的用户 Skill 目录 | 自建版本（无公开版本号） | 未随公开仓库发布。迁移前需从可信备份恢复 Skill 文件；不要把包含个人简历的输入或输出放进仓库。 |
| `hr-resume-screening` | SkillHub，slug：`hr-resume-screening` | 1.0.4 | 在目标 Agent 上从 SkillHub 重新核验并安装。来源包许可未单独核验；使用前检查当前版本和数据处理方式。可能将简历文本发送至模型 API；`--extract-only` 模式可只抽取信息。 |
| `hr-resume-scorer` | SkillHub，slug：`hr-resume-scorer` | 1.0.3 | 在目标 Agent 上从 SkillHub 重新核验并安装。来源包许可未单独核验。已安装包记录中引用的 `references/scoring_criteria.md` 缺失，使用前需确认当前包是否修复。 |
| `presentations` | Codex 内置 Skill | 随 Codex 版本 | 由 Codex 随附，不需要单独复制；换 Agent 时需检查对方是否提供等价 Skill。 |

## 迁移约定

1. 外置 Skill 优先按仓库或官方/可信商店的公开来源重新安装；安装前阅读其规则、依赖和许可，不把安装脚本当作可信指令直接执行。
2. Codex 用户级 Skill 通常安装在 `$HOME/.agents/skills/<skill-name>`；这是目标机器上的用户目录，不是本项目中的相对路径。
3. 自建 Skill 只有在单独备份其源文件后才能迁移。本项目不保存第三方 Skill 的副本，也不保存简历、候选人资料或 Skill 运行数据。
4. 新增、升级或卸载外置 Skill 后，更新本清单中的来源、版本、安装范围、许可核验状态和已知限制。不要记录密钥、私人材料或机器专属绝对路径。

## 尚未安装 / 不迁移

- Anthropic `skills-pptx`：未安装。其仓库说明对该 Skill 的复制和使用范围有限制，安装前应重新阅读当前许可条款；Codex 已有内置 `presentations` Skill 可用于演示文稿任务。
