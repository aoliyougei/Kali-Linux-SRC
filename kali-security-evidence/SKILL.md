---
name: kali-security-evidence
description: Use when preparing to export, screenshot, attach, transfer, or report security logs, HTTP traffic, JSONL, HAR, PCAP, commands, credentials, or user data.
---

# 安全证据卫生

**脱敏发生在远程容器内，早于 `docker cp`、打包和本地传输。**

始终移除/替换：Cookie、Set-Cookie、Authorization、JWT、API key、密码、CSRF Token、私钥、凭据文件和无必要的真实用户 PII。保留复现所需的接口、方法、状态、字段形状、时间和 request/trace ID。

1. 盘点每个文件的秘密类型。
2. 用格式感知工具处理 JSON/JSONL/HAR；文本使用明确字段规则，不能只做一个脆弱正则。
3. 截图隐藏 Header/Cookie 面板并遮盖 PII。
4. 执行假秘密回归搜索和人工抽查。
5. 生成 `SHA256SUMS` 后才允许进入导出协议。

Greybox 原凭据文件永不进入归档。PCAP 可能包含无关第三方流量，默认不导出；确需导出时先确认并最小化过滤。

详见 `references/redaction.md` 与 `references/artifact-layout.md`。

方法论提炼自 [Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter)，Sachin Sharma / ElementalSoul，CC BY 4.0。
