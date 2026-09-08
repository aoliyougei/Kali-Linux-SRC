# 注入检测工具

只在一个已授权 URL/参数出现可复验差异后使用。自动化结果仍是 candidate。

## SQLMap 1.10.8

低级检测起点：

```sh
sqlmap -u 'https://authorized.example/item?id=1' -p id \
  --batch --level 1 --risk 1 --threads 1 --timeout 10 --retries 1 \
  --output-dir "$OUT/sqlmap"
```

执行前再次确认，因为工具会发送注入 payload。禁止 `--dump`、`--dump-all`、`--os-shell`、`--sql-shell`、`--file-write`、`--file-dest`、`--tamper` 和破坏性语句。时间型结论还需独立交错采样。

## Commix 4.1

检测起点：

```sh
commix --url='https://authorized.example/ping?host=example' --batch --level=1 \
  --output-dir="$OUT/commix"
```

执行前再次确认。禁止取得 shell、读写文件、枚举/执行系统命令或 WAF 规避。候选用经审阅的单个无副作用 marker/时间差请求复验；时间差遵守 n≥10 交错样本。

## 停止

出现状态变化、异常进程、目标 5xx 增长、WAF 封禁、429 或超出窗口时立即停止。验证到最小影响即结束，不提取真实数据库或系统数据。
