# Web 与 Nuclei 集成结果

容器：`kali-nuclei-skill-inventory`。目标仅为容器内 localhost 服务；未扫描第三方。

## 内容发现

| 工具 | 目标 | 结果 |
|---|---|---|
| ffuf | `http://127.0.0.1:18080/FUZZ` | exit 0，JSON 命中 `index.html` |
| gobuster | 同上 | exit 0，文本命中 `index.html` |
| dirb | 同上 | exit 0，文本命中 `index.html` |
| wfuzz | 同上 | exit 0，JSON 非空；仅 HTTP，因为 PycURL 未链接 OpenSSL |

## Nuclei v3.11.1

均使用 `-rate-limit 10 -concurrency 1 -disable-update-check -jsonl-export`：

| protocol | fixture | result |
|---|---|---|
| HTTP | localhost Python HTTP server | `local-http-check` matched |
| Headless | localhost HTML + `-system-chrome` | `local-headless-check` matched |
| TCP | localhost PING/PONG service | `local-tcp-check` matched |
| DNS | `localhost` | `local-dns-check` matched |
| SSL | localhost OpenSSL TLS server, CN=localhost | `local-ssl-check` matched |
| Code | local `printf`, P-256 ECDSA signed | `local-code-check` matched |

所有 JSONL 文件非空。未签名 Code 模板不作为失败；签名后显式 `-code` 执行成功。

## 实测修正

- Nuclei：`-jsonl-export/-jle` 为 JSONL；`-json-export/-je` 为 JSON。
- DAVTest：包存在但缺 Perl `Net::SSL`，当前不可启动，文档标记 unavailable。
- FFUF：二进制自报 2.1.0-dev，dpkg 版本 2.2.1-1，两者均记录。
- Nmap：普通容器需先 `setcap -r /usr/lib/nmap/nmap`，再用 `-sT`；见 `tool-help-results.md`。
