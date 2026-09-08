---
name: kali-security-internal
description: Use when a separately authorized internal network, AD, SMB, or credential audit requires tools that are intentionally excluded from the default external assessment workflow.
---

# 隔离的内网安全评估

外部授权**永远不能**自动满足本 Skill。执行任何内网命令前重新确认：

1. 内网专项授权依据；
2. 明确 IP/CIDR/主机；
3. 允许协议与测试类型；
4. 测试账号归属、角色和允许使用方式；
5. 锁定/告警策略及每账号尝试上限；
6. 速率、并发和时间窗口；
7. 禁止动作与停止联系人。

然后重新执行 `kali-security-remote` 的服务器选择流程；不得复用外部任务的隐式授权。

默认只提供枚举、只读检查、离线用户自有哈希和 localhost 实验室示例。认证、喷洒、relay/coercion、写入、远程执行、额外 Capability 均需独立确认或按项目禁用。

始终禁止：DoS、凭据导出、持久化、横向移动、恶意软件、规避检测，以及 Mimikatz/Empire/PowerSploit/passing-the-hash 的实战使用。

参考：`references/smb-ad-tools.md`、`credential-auditing.md`、`restricted-tools.md`。

方法论提炼自 [Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter)，Sachin Sharma / ElementalSoul，CC BY 4.0。
