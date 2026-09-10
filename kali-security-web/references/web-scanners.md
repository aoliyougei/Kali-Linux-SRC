# Web 扫描与指纹工具

| 工具 | 安全示例 | 输出与边界 |
|---|---|---|
| nikto 2.6.1 | `nikto -host https://authorized.example -maxtime 20m -Format json -output "$OUT/nikto.json"` | 请求较多；告警是 candidate，逐项 curl 复验 |
| whatweb 0.6.4 | `whatweb --aggression 1 --log-json="$OUT/whatweb.json" https://authorized.example` | 低侵入指纹；版本 banner 不等于可利用漏洞 |
| wafw00f 2.4.2 | `wafw00f -f json -o "$OUT/wafw00f.json" https://authorized.example` | WAF/CDN 是边缘信号，不推断源站 |
| wpscan 4.1.0 | `wpscan --url https://authorized.example --plugins-detection passive --format json --output "$OUT/wpscan.json"` | 只用被动插件检测；枚举用户、密码攻击、API token 查询另行确认 |

扫描器版本映射必须结合服务证据、供应商公告和可控 PoC。技术事实可复现只证明配置/行为存在，不证明实际安全影响。缺少 HSTS/Secure/SameSite、安全头、banner、TLS 1.0/1.1/CBC、无秘密 Source Map 或普通重写配置默认 `KILL/HARDENING`，不自动升级为漏洞；只有平台接受且出现全新影响证据才建立新 candidate。
