# 无 Skill 基线结果

## 执行状态

**未执行。** 当前 Pi 会话没有子代理或独立 Agent API，无法满足 writing-skills 所要求的“每个场景使用全新 Agent 上下文并保存原始响应”。用户已在执行前明确接受以下替代方案：保留完整压力场景，执行静态检查、Docker 工具集成测试和经用户选择服务器后的 SSH 断线恢复实测。

不得把当前 Agent 对自己编写场景的回答伪装成独立基线。

## 已知设计输入（不是测试结果）

以下风险来自已确认需求和参考方法论，不声称为本环境观测到的 Agent 失败：

| 风险 | 最小指导位置 |
|---|---|
| 模糊授权导致越界 | `kali-security-scope` |
| 未询问即选择服务器 | `kali-security-remote` |
| SSH 状态未知时重跑/停止 | `kali-security-remote/references/job-protocol.md` |
| 扫描器告警直接升级为发现 | `kali-security-validation` |
| Greybox 凭据进入命令/日志 | `kali-security-scope`、`kali-security-evidence` |
| 外部授权被扩展为内网攻击 | `kali-security-internal` |

## 后续门禁

如未来提供独立 Agent 能力，应按 `skill-tests/scenarios.md` 补跑 RED 基线和 GREEN 测试，记录逐字响应与评分；在此之前，行为测试状态必须保持“未执行”，不能写成通过。
