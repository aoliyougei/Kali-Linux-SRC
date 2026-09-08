# 镜像安全工具索引

实测镜像：`docker.io/aoliyougei/kali-linux-nuclei-headless:v3.11.1-2026.3.4`（amd64）。完整证据见 `packages.tsv`（1,490 包）和 `executables.tsv`（4,317 个入口、1,810 个解析后文件）。版本为本次镜像快照；调用前可用 `command -v TOOL` 与 `TOOL --version` 复核。

## 外部发现与 DNS

| 工具 | 路径 | 版本 | 说明 |
|---|---|---:|---|
| amass | `/usr/bin/amass` | 5.1.1 | 外部资产发现；默认优先被动枚举 |
| dig/host/nslookup | `/usr/bin/*` | bind9 9.20.27 | DNS 查询与交叉验证 |
| dnsenum | `/usr/bin/dnsenum` | 1.3.2 | DNS 枚举；主动字典需范围授权 |
| dnsrecon | `/usr/bin/dnsrecon` | 1.6.0 | DNS 记录与枚举 |
| fierce | `/usr/bin/fierce` | 1.6.0 | DNS 侦察 |
| whois | `/usr/bin/whois` | 5.6.6 | 注册信息查询 |
| dmitry | `/usr/bin/dmitry` | 1.3a | 基础公开信息收集 |
| theHarvester | `/usr/bin/theHarvester` | 4.11.1 | 公开来源 OSINT |
| recon-ng | `/usr/bin/recon-ng` | 5.1.2 | 模块化 OSINT；模块/API 使用需审阅 |
| spiderfoot | `/usr/bin/spiderfoot` | 4.0 | OSINT 自动化；先限制模块与目标 |

## 主机、端口与协议

| 工具 | 路径 | 版本 | 授权 |
|---|---|---:|---|
| nmap | `/usr/bin/nmap` | 7.99 | `external-auto`，默认 `-T3` 常用端口 |
| masscan | `/usr/bin/masscan` | 1.3.2 | `confirm-active`，明确 CIDR/速率后使用 |
| fping | `/usr/bin/fping` | 5.1 | 明确主机列表 |
| arp-scan | `/usr/bin/arp-scan` | 1.10.0 | 本地二层网络，`internal-gate` |
| netdiscover | `/usr/sbin/netdiscover` | 0.10 | 本地二层与设备能力，`internal-gate` |
| hping3 | `/usr/sbin/hping3` | 3.a2 | 原始包；仅专项确认，禁止 DoS |
| socat/nc | `/usr/bin/*` | distro | 协议复验与本地实验服务 |

## HTTP、内容发现与 Web 候选

| 工具 | 路径 | 版本 | 说明 |
|---|---|---:|---|
| curl | `/usr/bin/curl` | 8.21.0 | HTTP 基线与独立复验 |
| httpx | `/usr/bin/httpx` | 0.28.1 | **Python HTTP 客户端 CLI，不是 ProjectDiscovery httpx** |
| whatweb | `/usr/bin/whatweb` | 0.6.4 | 技术指纹，仅产生候选 |
| wafw00f | `/usr/bin/wafw00f` | 2.4.2 | WAF 指纹 |
| ffuf | `/usr/bin/ffuf` | binary 2.1.0-dev (dpkg 2.2.1-1) | 内容发现，≤10 RPS |
| gobuster | `/usr/bin/gobuster` | 3.8.2 | 目录/DNS 枚举，明确模式与速率 |
| dirb | `/usr/bin/dirb` | 2.22 | 目录发现 |
| wfuzz | `/usr/bin/wfuzz` | 3.1.0 | PycURL 未链接 OpenSSL；默认仅本地 HTTP 实验，不用于 HTTPS |
| nikto | `/usr/bin/nikto` | 2.6.1 | Web 配置候选，必须人工复验 |
| wpscan | `/usr/bin/wpscan` | 4.1.0 | WordPress 检查；密码审计另行确认 |
| davtest | `/usr/bin/davtest` | 1.2 | **当前不可用**：缺少 Perl `Net::SSL`；不得临时安装依赖 |

## 注入验证

| 工具 | 路径 | 版本 | 边界 |
|---|---|---:|---|
| sqlmap | `/usr/bin/sqlmap` | 1.10.8 | 仅针对已授权具体参数做低级检测；禁止 dump/shell/写入 |
| commix | `/usr/bin/commix` | 4.1 | 只做特定参数检测；禁止 shell 与破坏性动作 |

## Nuclei 与浏览器

| 工具 | 路径 | 版本 | 说明 |
|---|---|---:|---|
| nuclei | `/usr/local/bin/nuclei` | v3.11.1 | JSONL、≤10 RPS、≤25 并发；结果必须独立复验 |
| chromium | `/usr/bin/chromium` | 150.0.7871.181 | Nuclei Headless 使用 `-system-chrome` |

## TLS 与流量

| 工具 | 路径 | 版本 | 说明 |
|---|---|---:|---|
| openssl | `/usr/bin/openssl` | 3.5.4 | TLS/证书手工复验 |
| sslscan | `/usr/bin/sslscan` | 2.1.5 | TLS 配置枚举 |
| sslyze | `/usr/bin/sslyze` | 6.3.1 | TLS 自动分析 |
| tshark | `/usr/bin/tshark` | 4.6.6 | 抓包/文件分析；实时抓包需 Capability 确认 |
| tcpdump | `/usr/bin/tcpdump` | 4.99.6 | 实时抓包需 Capability 与隐私确认 |
| mitmproxy/mitmdump | `/usr/bin/*` | 12.2.3 | 授权流量代理；导出前脱敏 |

## 内网、认证与高风险（默认隔离）

`netexec` 1.5.1、Impacket 0.13、`enum4linux` 0.9.1、`smbmap` 1.10.7、Responder 3.2.2、Hydra 9.7、John Jumbo、Hashcat 7.1.2、Ncrack 0.7、Patator 1.1、Metasploit 6.5.3 均已安装。仅由 `kali-security-internal` 在二次授权后路由。Mimikatz、PowerShell Empire、PowerSploit、passing-the-hash、Evil-WinRM 仅作库存记录；默认流程禁止其后渗透、凭据导出、持久化、横向移动或规避用法。

## 无线、设备与取证

Aircrack-ng、Kismet、Reaver、Wifite、BlueZ、Binwalk、Sleuth Kit、TestDisk、Scalpel 等已安装。无线/蓝牙/USB/块设备通常需要设备映射或额外 Capability，不属于默认远程外部评估。离线文件分析可在明确来源与授权后使用。

## 常被误以为存在但实际缺失

以下命令在本镜像中 **not installed**：

- `naabu`
- ProjectDiscovery `subfinder`
- ProjectDiscovery `dnsx`
- ProjectDiscovery `katana`
- `dalfox`
- `gau`
- `waybackurls`
- `trufflehog`

不要将 Python 包 `httpx` 当成 ProjectDiscovery 的 HTTP 探测器，也不要在任务中临时安装缺失工具，除非用户明确批准修改执行环境。
