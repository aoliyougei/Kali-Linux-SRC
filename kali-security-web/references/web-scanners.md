# Web 扫描与指纹工具

| 工具 | 安全示例 | 输出与边界 |
|---|---|---|
| nikto 2.6.1 | `nikto -host https://authorized.example -maxtime 20m -Format json -output "$OUT/nikto.json"` | 请求较多；告警是 candidate，逐项 curl 复验 |
| whatweb 0.6.4 | `whatweb --aggression 1 --log-json="$OUT/whatweb.json" https://authorized.example` | 低侵入指纹；版本 banner 不等于可利用漏洞 |
| wafw00f 2.4.2 | `wafw00f -f json -o "$OUT/wafw00f.json" https://authorized.example` | WAF/CDN 是边缘信号，不推断源站 |
| wpscan 4.1.0 | `wpscan --url https://authorized.example --plugins-detection passive --format json --output "$OUT/wpscan.json"` | 只用被动插件检测；枚举用户、密码攻击、API token 查询另行确认 |

扫描器版本映射必须结合服务证据、供应商公告和可控 PoC。缺少安全头、banner 或单一弱密码套件通常是配置项，不自动升级为漏洞。
