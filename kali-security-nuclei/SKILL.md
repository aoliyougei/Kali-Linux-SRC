---
name: kali-security-nuclei
description: Use when running or reviewing authorized Nuclei v3 scans, templates, JSONL results, Headless Chromium checks, signed Code templates, or protocol-specific validation.
---

# Nuclei v3 安全工作流

**REQUIRED SUB-SKILL:** `kali-security-scope` 与 `kali-security-remote`。扫描结果必须交给 `kali-security-validation`。

固定版本：Nuclei `v3.11.1`，Chromium `150.0.7871.181`。

## 合同

1. 明确目标文件和模板/tag/type；先审阅模板请求与副作用。
2. 输出 JSONL；默认 `-rate-limit 10 -concurrency 25`，不得提高。
3. 非破坏性模板才可自动执行；认证、fuzz、OOB、Code、写请求另行确认。
4. Headless 使用 `-headless -system-chrome`，不下载另一个浏览器。
5. Code 模板须审阅源码、使用 ECDSA 签名并显式 `-code`；拒绝未签名模板是正常安全行为。
6. 每条结果按协议使用第二工具复验；这只能证明技术事实，不证明平台接受性或实际安全影响，不把 severity/CWE 当漏洞结论。

缺少安全头/Cookie 属性、TLS 弱协议、Source Map、配置文件暴露和内容欺骗类命中必须先查 `kali-security-validation/references/non-reportable-findings.md`，默认 `KILL/HARDENING`。

停止条件：429、持续 5xx、连接异常、封禁提示、模板产生状态变化或范围漂移。

参考：`references/nuclei-cli.md`、`templates.md`、`headless.md`、`code-templates.md`。

方法论提炼自 [Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter)，Sachin Sharma / ElementalSoul，CC BY 4.0。
