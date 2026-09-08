# DNS 与注册信息工具

所有示例中的目标必须已明确授权；输出放在 `$OUT=/work/jobs/<job-id>/results/recon/dns`。

| 工具 | 安全用法 | 关键参数/输出 | 复验与误区 |
|---|---|---|---|
| `dig` | `dig +noall +answer authorized.example A > "$OUT/a.txt"` | `+short`, `+trace`, `@resolver` | 用第二解析器复验；CNAME 目标不自动继承授权 |
| `host` | `host -a authorized.example > "$OUT/host.txt"` | 简明记录查询 | 与 `dig` 对照 |
| `nslookup` | `nslookup -type=MX authorized.example > "$OUT/mx.txt"` | 兼容型查询 | 不把 NXDOMAIN 当资产不存在的唯一证据 |
| `whois` | `whois authorized.example > "$OUT/whois.txt"` | 注册/RIR 数据 | 隐私代理与过期数据常见；用 RDAP/官网复核 |
| `dnsenum` | `dnsenum --enum authorized.example --output "$OUT/dnsenum.xml"` | 主动枚举；字典会增加请求 | 先授权子域枚举；结果用 `dig` 验证 |
| `dnsrecon` | `dnsrecon -d authorized.example -t std -j "$OUT/dnsrecon.json"` | `-t std`, `-j` | `brt`/AXFR 等模式先审阅影响 |
| `fierce` | `fierce --domain authorized.example > "$OUT/fierce.txt"` | DNS 侦察 | 候选主机仍需追加明确授权后主动探测 |

停止：解析器限流、范围漂移或异常查询量。禁止未经许可 AXFR 暴力、DNS 放大或递归滥用。
