# SMB/AD 只读工具

仅在独立内网授权后使用。示例目标 `192.0.2.10` 为文档保留地址，不可替换为未授权目标。

| 工具 | 已安装版本 | 安全起点 | 边界/复验 |
|---|---:|---|---|
| enum4linux | 0.9.1 | `enum4linux -h`；真实枚举需确认匿名 SMB 查询 | 输出可能不完整；用 `smbclient -L`/Nmap SMB 脚本复核 |
| smbmap | 1.10.7 | `smbmap --help` | 认证、递归、下载、上传和命令执行另行确认 |
| NetExec | 1.5.1 | `netexec --help`、`netexec smb --help` | 默认不提供认证、喷洒、模块、执行或 SAM/LSA 命令 |
| Impacket | 0.13 dev | `impacket-smbclient -h`、`impacket-rpcdump -h` | 只读发现客户端；relay、coercion、远程执行、票据/凭据操作禁用 |
| nbtscan | 1.7.2 | `nbtscan -h` | 仅明确网段；用 DNS/Nmap 对照 |

若批准匿名只读 SMB 发现，命令仍应使用单主机/小范围、标准速率并保存日志。发现域控、信任或新网段只记录，不扩大范围。
