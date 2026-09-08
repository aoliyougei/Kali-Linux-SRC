# 代理与流量分析

| 工具 | 安全用途 | 权限/隐私 |
|---|---|---|
| `mitmproxy` / `mitmweb` / `mitmdump` 12.2.3 | 用户主动配置的测试流量映射与回放 | 安装 CA、代理真实流量前再次确认；只处理测试账号 |
| `tshark` 4.6.6 | pcap 离线过滤：`tshark -r capture.pcap -Y http -T json > http.json` | 离线优先；实时捕获需 NET_RAW/NET_ADMIN 与接口确认 |
| `tcpdump` 4.99.6 | 受限实时采样或 pcap 校验 | 可能捕获第三方凭据/PII；接口、BPF、时长、文件大小均需确认 |

代理日志和 pcap 导出前必须交给 `kali-security-evidence`。Cookie、Authorization、JWT、API key、密码、Set-Cookie 与无关 PII 必须删除/脱敏。不要把代理作为绕过 TLS 或截获非测试用户的手段。

最小离线复验：

```sh
tshark -r "$PCAP" -q -z io,phs
capinfos "$PCAP"
```

保留文件 SHA-256、捕获时间、授权接口和过滤表达式。
