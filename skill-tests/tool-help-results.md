# 镜像工具帮助检查结果

检查容器：`kali-nuclei-skill-inventory`；仅运行帮助、版本或 localhost 无害测试。

| command | exit | observed |
|---|---:|---|
| `dig -v` | 0 | DiG 9.20.27 |
| `host -V` | 0 | host 9.20.27 |
| `nslookup -version` | 0 | nslookup 9.20.27 |
| `whois --version` | 0 | 5.6.6 |
| `dnsenum --help` | 1 | 帮助正常；工具自报 1.3.1，dpkg 为 1.3.2 |
| `dnsrecon --help` | 0 | 确认 `-d`, `-t`, `-j` |
| `fierce --help` | 0 | 确认 `--domain` |
| `fping -v` | 0 | 5.1 |
| `arp-scan --version` | 0 | 1.10.0 |
| `netdiscover -h` | 1 | 帮助正常，0.21 |
| `curl --version` | 0 | 8.21.0 |
| `httpx --version` | 2 | 显示 Python HTTPX CLI usage；不是 ProjectDiscovery httpx |
| `whatweb --version` | 0 | 0.6.4 |
| `wafw00f --version` | 0 | 命令可用 |
| `chromium --version` | 0 | 150.0.7871.181 |
| `theHarvester -h` | 0 | 帮助可用 |
| `recon-ng --help` | 0 | 确认 `--no-version` |
| `spiderfoot --help` | 0 | 确认 `-l IP:port`、模块参数 |

## Nmap 容器限制实测

初始 `nmap --version` 返回 126 / `Operation not permitted`。根因是 `/usr/lib/nmap/nmap` 带 `cap_net_bind_service,cap_net_admin,cap_net_raw=eip`，普通容器 bounding set 不含 `NET_ADMIN`。执行：

```sh
setcap -r /usr/lib/nmap/nmap
nmap -sT -T3 -Pn -p 1 127.0.0.1 -oX /tmp/nmap-safe.xml
```

结果 exit 0 且 XML 非空。Skill 因此默认移除本次容器内文件能力并使用 `-sT`，不自动提升容器权限。

## 非零帮助退出码

部分工具以 1/2 表示“显示帮助后退出”，不表示缺失。`amass -version` 首次运行会检查大型 libpostal 数据，帮助验证应设置 timeout；实际包版本由 dpkg 证据确认。
