# 内容发现

前置：目标明确授权并已有两个随机不存在路径的 soft-404 控制。`WORDLIST` 应来自 `/usr/share/wordlists` 或已审阅的用户文件。

| 工具 | 安全示例 | 参数与输出 | 复验 |
|---|---|---|---|
| ffuf binary 2.1.0-dev (dpkg 2.2.1-1) | `ffuf -u https://authorized.example/FUZZ -w "$WORDLIST" -rate 10 -t 10 -ac -of json -o "$OUT/ffuf.json"` | `-rate 10`, `-t 10`, `-ac`, `-fc/-fs/-fw` | 对命中用 curl 保存正文并与两条控制比较 |
| gobuster 3.8.2 | `gobuster dir -u https://authorized.example -w "$WORDLIST" -t 10 --delay 1s -o "$OUT/gobuster.txt"` | 模式必须明确；`--delay` 限速 | soft-404 会制造大量假阳性 |
| dirb 2.22 | `dirb https://authorized.example "$WORDLIST" -z 1000 -o "$OUT/dirb.txt"` | `-z` 请求间隔毫秒 | 老工具对 SPA/统一错误页误报高 |
| wfuzz 3.1.0 | 仅本地 HTTP 实验：`wfuzz -c -t 10 -s 1 -f "$OUT/wfuzz.json,json" -w "$WORDLIST" http://127.0.0.1:18080/FUZZ` | `-t`, `-s`, `--hc/--hh` | PycURL 未链接 OpenSSL，默认不用于 HTTPS；用基线长度/哈希过滤 |

只使用 GET/HEAD。参数发现、虚拟主机、递归深度或扩展名爆破应与授权范围匹配。新域名只记录。禁止扫描登录、重置、发送、生成、创建、更新、删除、支付等动作型路径。
