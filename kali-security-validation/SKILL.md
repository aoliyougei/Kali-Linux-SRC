---
name: kali-security-validation
description: Use when triaging scanner output, reproducing a suspected vulnerability, comparing baselines, evaluating timing signals, assigning severity, or deciding whether a finding is reportable.
---

# 漏洞线索验证

扫描器输出永远先标记 `candidate`。结论只能是 `PASS`、`KILL`、`DOWNGRADE` 或 `CHAIN-REQUIRED`。

## 强制门禁

1. 真实、可复制的请求与攻击前提是什么？
2. 影响是否属于授权项目接受范围？
3. 根因资产是否在明确范围内？
4. 是否依赖攻击者不现实的高权限？
5. 是否是已知/文档化行为或重复项？
6. 是否已证明实际影响，而非“可能”？
7. 是否只是缺少安全头、banner、DNS-only SSRF、无影响跳转等需链式证明的弱信号？

任一关键项不满足就不得 PASS。详情见 `references/finding-gates.md`。

## 证据纪律

- Marker 至少 8 位随机字母数字；先确认基线不存在。
- 比较 status、正文、长度和 SHA-256；状态码差异本身不是绕过。
- 时间结论每组至少 10 个交错随机样本，报告 mean/median/σ；不由脚本自动宣布漏洞。
- High/Critical 至少两种独立工具或协议栈复现。
- 自动化 severity 不继承为报告 severity。
- 证明最小必要影响后停止；不批量获取真实数据。

被否定项写入 `findings/killed/`；已确认后失效或推翻的写入 `findings/retracted/`，不得静默删除。

方法论提炼自 [Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter)，Sachin Sharma / ElementalSoul，CC BY 4.0。
