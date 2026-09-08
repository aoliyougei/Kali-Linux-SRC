# OSINT 工具

公开来源也受条款、隐私和授权目标约束；结果是候选资产，不自动获得主动测试授权。

| 工具 | 安全起点 | 输出/注意 |
|---|---|---|
| `amass` 5.1.1 | `amass enum -passive -d authorized.example -o "$OUT/amass.txt"` | 默认被动；主动模式另确认；每个候选用 DNS 复核 |
| `theHarvester` 4.11.1 | `theHarvester -d authorized.example -b crtsh -f "$OUT/harvester"` | 数据源/API 限制；避免收集无关人员 PII |
| `recon-ng` 5.1.2 | `recon-ng --no-version` 后人工选择模块 | 模块行为不同；运行前审阅模块、API key 和输出 |
| `spiderfoot` 4.0 | `spiderfoot -l 127.0.0.1:5001` | Web UI 本地监听；明确模块后启动扫描，避免全模块噪声 |
| `dmitry` 1.3a | `dmitry -w -n authorized.example > "$OUT/dmitry.txt"` | 老旧来源可能失效；手工复核 |

`recon-ng`/SpiderFoot 的主动模块属于 `confirm-active`。凭据/API key 只能从容器内权限受限文件读取，不写入命令和归档。
