---
name: kali-security-scope
description: Use when starting or changing an authorized vulnerability assessment, bug bounty hunt, external attack-surface review, greybox test, or internal security audit before any live probe is sent.
---

# Kali 安全评估授权与范围

## 核心规则

**没有明确授权和精确范围，不执行任何探测。** 组织名称、口头“应该可以”、模糊通配符或历史授权都不够。

## 启动合同（按顺序）

逐项获得并记录，缺一项就停止：

1. `engagement-id`：仅用字母、数字、点、下划线、连字符。
2. 授权依据：自有资产、书面授权、Bug Bounty 明确范围或 CTF。
3. 精确目标：域名、IP、CIDR、URL；组织名不是目标清单。
4. 允许测试类型。
5. 禁止动作。
6. 并发、RPS、端口范围；默认 HTTP/Nuclei ≤25 并发、≤10 RPS，Nmap `-T3` 常用端口。
7. 开始/结束时间窗口与时区。
8. `blackbox` 或 `greybox`。

使用 `references/authorization-template.md` 记录摘要；不要复制合同/SoW 原文。

## 范围规则

- 通配符先解析为候选，再让用户批准明确主机清单。
- CT、DNS、CSP、JS、CNAME 或错误信息中新发现的资产只记录，**不得解析后的进一步探测或主动请求**，直到追加授权。
- 子任务必须携带授权主机列表原文和禁止动作；不得写“目标全网”。
- 遇到重定向或第三方服务时，目标边界不随请求自动扩展。

## 自动与再确认

授权后可自动进行非破坏性 DNS/WHOIS、基线、指纹、标准速率端口与内容发现、非破坏性 Nuclei 和只读复验。

以下动作前再次确认：认证/OTP/密码重置、上传、写请求、OOB 回连、高速/全端口、费用或通知、额外 Capability、内网工具。

始终禁止：未授权扫描、DoS、破坏、批量外传、持久化、横向移动、恶意软件和规避检测。

## Greybox

不接受聊天中的明文凭据用于执行。要求用户将凭据预置到选定远程服务器的 `chmod 600` 文件，只询问路径。不得在 `ssh_exec` 参数、进程参数、日志、报告或本地归档中回显凭据。任务完成并成功导出后删除容器内副本，不改远程原文件。

## 输出

范围确认后输出一份结构化摘要并要求最终确认；确认前不加载执行类 Skill。

## 来源

方法论提炼自 [Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter)，Sachin Sharma / ElementalSoul，内容许可 CC BY 4.0。
