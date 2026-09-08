# Nuclei CLI v3.11.1

## 基础扫描

```sh
nuclei -list authorized-urls.txt \
  -severity critical,high,medium \
  -rate-limit 10 -concurrency 25 \
  -jsonl-export "$OUT/nuclei.jsonl" \
  -stats -no-color
```

- `-list/-l`：精确授权目标文件。
- `-templates/-t`、`-tags`、`-type`：限制模板；不要无审阅全量执行。
- `-rate-limit 10`：每秒请求上限；`-concurrency 25`：模板并发上限。
- `-jsonl-export/-jle`：JSONL 结构化结果；`-json-export/-je` 是 JSON，不要混淆；同时保留 stdout/stderr。
- `-resume`：仅恢复 Nuclei 自身生成的 resume 文件；job-id 仍由远程协议控制。
- `-disable-update-check/-duc`：固定运行时可避免额外网络请求。

输出是 candidate。HTTP 用 curl，DNS 用 dig，TCP 用 Nmap/协议客户端，SSL 用 OpenSSL/SSLyze，Headless 用 Chromium 手工复验。

模板行为不明、使用 fuzz/code/headless/OOB、包含写方法或认证时先停止并再次确认。
