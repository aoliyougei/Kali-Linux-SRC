# 工具能力与授权矩阵

授权值：`external-auto`（已确认外部范围后可自动）、`confirm-active`（动作前再次确认）、`internal-gate`（独立内网授权）、`inventory-only`（仅记录）。

| tool | phase | default authorization | network impact | capability/device need | second-tool validation | reference |
|---|---|---|---|---|---|---|
| dig/host/nslookup | recon | external-auto | low | none | second DNS resolver / openssl | recon/dns-tools |
| whois | recon | external-auto | low | none | registry/RDAP | recon/dns-tools |
| amass | recon | external-auto | passive by default | API keys optional | dig | recon/osint-tools |
| theHarvester | recon | external-auto | passive/provider-dependent | API keys optional | source URL + dig | recon/osint-tools |
| recon-ng/spiderfoot | recon | confirm-active | module-dependent | API keys optional | manual source check | recon/osint-tools |
| fping | recon | external-auto | low | ICMP may need NET_RAW | nmap/curl | recon/host-discovery |
| nmap | recon | external-auto | medium, T3/common ports | SYN may need NET_RAW | service-native client | recon/port-scanning |
| masscan | recon | confirm-active | high | NET_RAW/host network | nmap | recon/port-scanning |
| arp-scan/netdiscover | recon | internal-gate | local L2 | NET_RAW/NET_ADMIN | nmap | recon/host-discovery |
| curl | baseline/validate | external-auto | low | none | openssl/browser | recon/http-fingerprinting |
| whatweb/wafw00f | recon | external-auto | low | none | curl/manual headers | recon/http-fingerprinting |
| ffuf/gobuster/dirb/wfuzz | web | external-auto | medium, ≤10 RPS | none | curl + soft-404 diff | web/content-discovery |
| nikto/wpscan | web | external-auto | medium | none | curl/version evidence | web/web-scanners |
| davtest | web | confirm-active | may write/upload | none | curl/WebDAV client | web/api-testing |
| sqlmap/commix | validate | confirm-active | medium/high | none | curl + independent client | web/injection-tools |
| nuclei | scan | external-auto | medium, ≤10 RPS/25 concurrency | none | protocol-specific tool | nuclei/nuclei-cli |
| nuclei headless | scan | external-auto | medium/resource-heavy | chromium, no extra cap | chromium/curl | nuclei/headless |
| nuclei code | scan | confirm-active | template-defined | signed ECDSA template | inspect source + native engine | nuclei/code-templates |
| openssl/sslscan/sslyze | recon/validate | external-auto | low | none | two TLS stacks | validation/reproduction |
| tshark/tcpdump | evidence | confirm-active | passive capture | NET_RAW/NET_ADMIN often required | saved pcap + protocol client | web/proxy-and-traffic |
| mitmproxy | mapping | confirm-active | user-routed traffic | CA trust setup | curl/replay | web/proxy-and-traffic |
| hydra/ncrack/patator | auth audit | internal-gate | high/lockout risk | none | owner logs | internal/credential-auditing |
| john/hashcat | offline audit | internal-gate | no target traffic | GPU optional | known sample hash | internal/credential-auditing |
| enum4linux/smbmap/netexec/impacket | internal | internal-gate | medium | reachable internal scope | native smbclient/nmap | internal/smb-ad-tools |
| responder | internal | inventory-only | poisoning/capture | NET_RAW/NET_ADMIN | none | internal/restricted-tools |
| metasploit | validation | internal-gate | module-dependent | module-dependent | independent PoC | internal/restricted-tools |
| mimikatz/empire/powersploit/passing-the-hash | post-exploit | inventory-only | high | privileged/credentials | none | internal/restricted-tools |
| aircrack-ng/kismet/reaver/wifite | wireless | inventory-only | RF/device-dependent | mapped wireless device | hardware-native tools | inventory/security-tools |
| binwalk/sleuthkit/testdisk/scalpel | offline analysis | confirm-active | none | files/device mapping | hash + second parser | inventory/security-tools |

停止条件：`429`、持续 `5xx`、连接异常、封禁提示、范围漂移或用户暂停。任何工具存在于镜像中不等于获得执行授权。
