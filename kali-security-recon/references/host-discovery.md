# 主机发现

| 工具 | 路径/版本 | 安全示例 | 约束 |
|---|---|---|---|
| `fping` | `/usr/bin/fping` 5.1 | `fping -a -r 1 -t 500 -f authorized-ips.txt 2>dead.txt >alive.txt` | 文件只含明确授权 IP；ICMP 不响应不等于离线 |
| `nmap` ping | `/usr/bin/nmap` 7.99 | `nmap -sn -T3 -iL authorized-ips.txt -oA discovery` | 与 TCP/HTTP 复核 |
| `arp-scan` | `/usr/bin/arp-scan` 1.10 | 实验室：`arp-scan --localnet` | 仅本地二层，必须 `kali-security-internal` 与 NET_RAW 确认 |
| `netdiscover` | `/usr/sbin/netdiscover` | 实验室帮助：`netdiscover -h` | 需要二层接口/Capability；外部默认禁用 |

不要把广播域、路由表或 DNS 新发现地址自动加入范围。host 网络不等于授权，也不等于具备全部 Capability。
