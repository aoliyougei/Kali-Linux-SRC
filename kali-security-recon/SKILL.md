---
name: kali-security-recon
description: Use when performing authorized external DNS, OSINT, host discovery, port scanning, HTTP fingerprinting, TLS reconnaissance, or attack-surface mapping with the Kali image.
---

# Kali 外部侦察

**REQUIRED SUB-SKILL:** 先用 `kali-security-scope` 锁定精确目标，再用 `kali-security-remote` 让用户选择 SSH 服务器并管理容器。

## 顺序

1. 被动 DNS/WHOIS/公开来源；输出候选资产。
2. 用户授权明确主机后，解析与低影响存活检查。
3. 每台 Web 主机先记录两个随机不存在路径的 status、length、body hash，建立 soft-404 基线。
4. Nmap `-T3` 常用端口；全端口或 Masscan 再确认。
5. HTTP/TLS 指纹；按价值、暴露和技术栈排序。
6. 新发现资产只记录，等待追加授权。

默认输出写到 `/work/jobs/<job-id>/results/recon/`。遇到 `429`、持续 `5xx`、封禁或连接异常时停止新请求并保留 job。

## 路由

- DNS：`references/dns-tools.md`
- 存活/二层限制：`references/host-discovery.md`
- 端口：`references/port-scanning.md`
- HTTP/soft-404：`references/http-fingerprinting.md`
- OSINT：`references/osint-tools.md`

自动化结果是候选，不是漏洞。端口和服务由协议原生客户端或第二工具复验。

方法论提炼自 [Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter)，Sachin Sharma / ElementalSoul，CC BY 4.0。
