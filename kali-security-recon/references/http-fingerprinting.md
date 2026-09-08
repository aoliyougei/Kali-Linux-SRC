# HTTP 指纹与 Soft-404 基线

## 每主机强制基线

为每个主机（必要时每个路径深度）请求两个随机不存在路径：

```sh
for p in /x4hd2k9pq /q7mv8z2rt; do
  curl -skS -L --max-time 12 -D "$OUT/${p#/}.headers" -o "$OUT/${p#/}.body" \
    -w '%{http_code}\t%{size_download}\t%{url_effective}\n' "https://authorized.example$p"
  sha256sum "$OUT/${p#/}.body"
done
```

只有响应正文/长度/哈希不同于控制时，路径才是候选；200 不代表存在。重定向到第三方只记录，不越界探测。

## 工具

| 工具 | 用法 | 注意 |
|---|---|---|
| `curl` | `curl -skS -L --max-time 12 -D headers -o body URL` | 保留头/正文/最终 URL；`-k` 的证书问题另用 OpenSSL 复验 |
| `whatweb` | `whatweb --aggression 1 --log-json="$OUT/whatweb.json" URL` | 指纹可误判，检查响应证据 |
| `wafw00f` | `wafw00f -o "$OUT/waf.json" -f json URL` | CDN/WAF 是边缘信号，不代表源站技术 |
| `chromium` | `chromium --headless --no-sandbox --dump-dom URL` | Headless 渲染；资源较高，遵守速率 |
| `httpx` | `/usr/bin/httpx` | 这是 Python HTTP 客户端 CLI，不是 ProjectDiscovery 探测器 |

**not installed：** ProjectDiscovery `httpx`、`subfinder`、`dnsx`、`katana`，以及 `naabu`。不得使用相同名称误路由。
