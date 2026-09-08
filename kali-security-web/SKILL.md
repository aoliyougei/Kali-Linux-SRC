---
name: kali-security-web
description: Use when assessing an explicitly authorized website or API with content discovery, fingerprinting, low-impact scanners, parameter testing, or HTTP proxy tools in the Kali image.
---

# Kali Web/API 安全测试

**REQUIRED SUB-SKILL:** 先完成 `kali-security-scope` 与 `kali-security-remote`。

## 工作流

1. 记录正常页面和两个不存在路径的 status、length、body hash。
2. 内容发现使用 `ffuf`/`gobuster`/`dirb`/`wfuzz`，≤10 RPS，并排除 soft-404。
3. `nikto`、`whatweb`、`wafw00f`、`wpscan` 只产生候选。
4. 用 `curl`/浏览器/协议客户端检查实际正文和影响。
5. 仅在具体参数有差异证据后考虑 `sqlmap`/`commix` 的低级检测。
6. 所有候选交给 `kali-security-validation`；未复验不得称为漏洞。

POST/PUT/PATCH/DELETE、认证、OTP、上传、OOB、代理真实用户流量及可能产生记录/通知的行为必须再次确认。

## 参考路由

- `references/content-discovery.md`
- `references/web-scanners.md`
- `references/api-testing.md`
- `references/injection-tools.md`
- `references/proxy-and-traffic.md`

输出写入 `/work/jobs/<job-id>/results/web/`。遇到 429、持续 5xx、封禁或目标异常时停止新请求并保留 job。

方法论提炼自 [Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter)，Sachin Sharma / ElementalSoul，CC BY 4.0。
