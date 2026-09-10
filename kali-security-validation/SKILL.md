---
name: kali-security-validation
description: Use when triaging scanner output, reproducing a suspected vulnerability, comparing baselines, evaluating timing signals, assigning severity, or deciding whether a finding is reportable.
---

# 漏洞线索验证

扫描器输出永远先标记 `candidate`。结论只能是 `PASS`、`KILL`、`DOWNGRADE` 或 `CHAIN-REQUIRED`。可复现但不可报告的技术事实使用 `outcome: KILL`、`disposition: HARDENING`，不是漏洞。

## 强制门禁

先区分三件事：技术事实是否可复现、平台是否接受该类型、是否已证明实际安全影响。多工具复现只能回答第一项，不能提高平台接受性或严重性。

1. 真实、可复制的请求与攻击前提是什么？
2. 当前平台/项目是否明确收录该类型？
3. 影响是否属于授权项目接受范围？
4. 根因资产是否在明确范围内？
5. 是否依赖攻击者不现实的高权限？
6. 是否是已知/文档化行为、重复项或明确不重报项？
7. 是否已证明实际影响，而非“可能”“降低攻击成本”或合规偏离？
8. 是否只是 `references/non-reportable-findings.md` 中的默认弱信号？

任一关键项不满足就不得 PASS。平台接受性必须先于严重性判断。详情见 `references/finding-gates.md`、`non-reportable-findings.md` 和 `platform-acceptance.md`。

## 证据纪律

- Marker 至少 8 位随机字母数字；先确认基线不存在。
- 比较 status、正文、长度和 SHA-256；状态码差异本身不是绕过。
- 时间结论每组至少 10 个交错随机样本，报告 mean/median/σ；不由脚本自动宣布漏洞。
- High/Critical 至少两种独立工具或协议栈复现。
- 自动化 severity、CWE 和多工具复现不继承为报告 severity，也不改变默认非漏洞分类。
- 证明最小必要影响后停止；不批量获取真实数据。

被否定项写入 `findings/killed/`；可复现加固项另写入 `hardening/`；已确认后失效或推翻的写入 `findings/retracted/`，不得静默删除。没有新影响证据不得重复提交或恢复旧 candidate。

方法论提炼自 [Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter)，Sachin Sharma / ElementalSoul，CC BY 4.0。
