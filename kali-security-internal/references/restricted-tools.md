# 高风险工具库存与限制

这些工具存在于镜像，不代表允许执行。

| 工具 | 版本 | 合法用途概述 | 本 Skills 政策 |
|---|---:|---|---|
| Responder | 3.2.2 | 实验室协议行为与防御验证 | inventory-only；禁止真实网络 poisoning/credential capture |
| Metasploit Framework | 6.5.3 | 已授权实验室模块验证 | 仅 `msfconsole --version`/模块文档；不提供 payload、session、持久化或远程执行流程 |
| PowerShell Empire | 6.6.0 | C2/后渗透框架 | inventory-only，禁止实战 |
| PowerSploit | 3.0 | PowerShell 后渗透集合 | inventory-only，禁止实战 |
| Mimikatz | 2.2.0 | Windows 凭据相关工具 | inventory-only，禁止凭据导出 |
| passing-the-hash | 2015 snapshot | 认证滥用工具集合 | inventory-only，禁止实战 |
| Evil-WinRM | 3.9 | WinRM 管理客户端 | 不用于横向移动或未单独授权远程会话 |
| msfvenom | Metasploit 6.5.3 | payload 生成 | 禁止生成 weaponized payload |

允许的检查仅限 `command -v`、包版本和无副作用 help/version。不得提供或执行：credential dumping、relay/coercion、payload generation、reverse shell、remote execution、persistence、lateral movement、evasion、C2 listener。

需要这些能力的合法红队项目超出本 Skills 设计范围，应使用独立治理、基础设施、审批和审计流程。
