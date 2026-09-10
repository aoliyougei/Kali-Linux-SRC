---
name: kali-security-reporting
description: Use when packaging an authorized assessment's validated findings, negative coverage, retractions, evidence index, remediation, limitations, and reproducible sanitized commands into a final report.
---

# 安全评估报告

只接收经 `kali-security-validation` 分类和 `kali-security-evidence` 脱敏的内容。Candidate 不得写成确认漏洞；`KILL/HARDENING` 只能进入加固项，不得进入已确认发现。

报告依次包含：

1. 授权与范围摘要
2. 执行环境和镜像版本/digest
3. 方法与覆盖范围
4. 攻击面清单
5. 已确认发现
6. 待人工验证线索
7. 阴性测试与覆盖证明
8. 被排除/撤回的误报
9. 加固项（技术事实成立但不可报告）
10. 风险与修复建议
11. 工具、命令和证据索引
12. 局限性与 SHA-256 文件清单

确认发现使用 `references/finding-template.md`；加固项使用 `references/hardening-template.md`。命令可复制但必须脱敏；严重性根据平台接受性和已证明影响，不继承扫描器标签、CWE 或复现工具数量。加固项不得分配漏洞严重性。报告不得包含凭据、合同正文、无必要 PII 或批量真实数据。

使用 `references/report-template.md`；完整结果保存到当前项目的 `security-results/YYYY-MM-DD_<scheme-host-port|multi-target>_<engagement-id>/`，不提交 Git。目录不得包含 URL path、query、fragment、userinfo 或凭据。

方法论提炼自 [Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter)，Sachin Sharma / ElementalSoul，CC BY 4.0。
