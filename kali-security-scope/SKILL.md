---
name: kali-security-scope
description: Use when starting or changing an authorized vulnerability assessment, bug bounty hunt, external attack-surface review, greybox test, or internal security audit before any live probe is sent.
---

# Kali 安全评估授权与范围

## 核心规则

**没有明确授权和精确范围，不执行任何探测。** 组织名称、口头“应该可以”、模糊通配符或历史授权都不够。

## 启动合同

先按授权类型分流：

- `Bug Bounty`：使用下面的最小输入流程，不逐项追问已有默认值。
- 自有资产、书面授权、CTF 或内网评估：逐项确认 `engagement-id`、授权依据、精确目标、允许测试类型、禁止动作、速率/端口、时间窗口和 blackbox/greybox；缺失项才询问。

使用 `references/authorization-template.md` 记录摘要；不要复制合同/SoW 原文。

## Bug Bounty 默认值

用户只需提供：

1. 目标域名或 URL；
2. 当前 Bug Bounty 项目规则或范围证据。

先阅读 in-scope、OOS、速率和测试限制，**只有项目规则明确**允许时才启用：

- `@`：根域，如 `jiaoyu.cn`；
- `www`：`www.jiaoyu.cn`；
- `*`：规则明确写出的 `*.jiaoyu.cn` 通配范围。

规则只允许其中一项就只纳入该项。规则不清楚时只询问范围歧义，不重复询问有默认值的字段。通配符发现的新主机若匹配明确规则可进入候选清单；第三方 CNAME、项目 OOS 和规则未覆盖资产仍仅记录。

自动生成：

- `engagement-id`：`<规范化目标>-<UTC 日期 YYYYMMDD>`；只含字母、数字和连字符。同日同目标若本地结果目录已存在，依次追加 `-02`、`-03`。
- 授权依据：`Bug Bounty`。
- 测试窗口开始：用户最终确认时间，记录 ISO 8601 与时区。
- 测试窗口结束：任务完成或用户停止；若项目规则给出更早截止时间，以规则为准。

例如 `https://www.jiaoyu.cn/path?q=token` 自动生成 `www-jiaoyu-cn-20260909`，不把 path、query 或凭据放入 ID。

未填写可选字段时使用以下默认值：

```yaml
allowed_tests:
  dns_and_public_information: all-nondestructive
  network_discovery:
    scan_type: TCP Connect
    ports: top-1000
    nmap_timing: T3
  web_recon:
    - HTTP/TLS baseline
    - soft-404
    - technology fingerprinting
    - low-rate content discovery
  nuclei:
    - 非破坏性 CVE 模板
    - 非破坏性配置模板
  manual_validation: read-only
denied_tests:
  - 登录尝试
  - 密码喷洒和凭据填充
  - OTP/MFA 测试
  - 文件上传
  - POST/PUT/PATCH/DELETE 写请求
  - SQL 注入利用和数据提取
  - OOB/Interactsh 回连
  - 获取 Shell
  - DoS/资源耗尽
  - 批量数据读取或外传
rates:
  concurrency: 25
  requests_per_second: 10
mode: blackbox
```

默认 `blackbox`。用户明确提供测试凭据和 greybox 授权时才切换。**禁止列表优先**于允许列表、工具默认行为、模板和扫描器标签。

生成完整结构化摘要后只做一次结构化确认：`已根据项目规则生成范围与默认配置，是否开始？` 用户确认前不执行探测。不再逐项询问允许类型、禁止动作、并发、RPS、端口、模式、engagement-id 或默认窗口。

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
