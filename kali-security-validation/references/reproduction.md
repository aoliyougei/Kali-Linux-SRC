# 独立复现

| candidate | primary | independent verifier |
|---|---|---|
| HTTP/Nuclei | nuclei | curl + saved body/hash |
| DNS | nuclei/dnsrecon | dig against a second resolver |
| TCP service | nmap | native client / nc / openssl |
| TLS | sslscan | openssl s_client or sslyze |
| Headless | nuclei | system Chromium DOM/screenshot + curl |
| SQL injection | low-level sqlmap | reviewed curl plus independent Python HTTP client and timing stats |
| content path | ffuf/gobuster | curl vs two soft-404 controls |

High/Critical 必须有两个不同实现/协议栈；同一工具换参数不算独立。

## 安全时间采样器

只用于已授权、只读的 control/test URL；每组至少 10 次。它输出统计，不判定漏洞：

```python
import random, statistics, time, urllib.request
urls = {"control": CONTROL_URL, "test": TEST_URL}
labels = [k for k in urls for _ in range(10)]
random.shuffle(labels)
samples = {k: [] for k in urls}
for label in labels:
    start = time.monotonic()
    try:
        with urllib.request.urlopen(urls[label], timeout=10) as r:
            r.read(1024)
    except Exception as exc:
        print(label, "ERROR", type(exc).__name__)
        continue
    samples[label].append(time.monotonic() - start)
for label, values in samples.items():
    print(label, "n", len(values), "mean", statistics.mean(values),
          "median", statistics.median(values), "sigma", statistics.pstdev(values))
```

保存随机顺序、每次时间和错误；任何错误/429/5xx 都不能丢弃后只挑有利样本。
