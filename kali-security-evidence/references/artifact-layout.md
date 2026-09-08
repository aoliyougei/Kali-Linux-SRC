# 本地产物结构

```text
security-results/<engagement-id>/
├── authorization.md
├── scope.json
├── tool-versions.tsv
├── execution-manifest.json
├── commands/
├── logs/
├── recon/{dns,hosts,ports,http,tls}/
├── scans/{nuclei,nmap,web}/
├── findings/{confirmed,candidates,killed,retracted}/
├── evidence/
├── report.md
└── SHA256SUMS
```

`authorization.md` 不含合同原文；manifest 不含凭据。`commands/` 必须可复现且凭据替换为文件引用或 `<REDACTED>`。`killed/` 记录否定证据，`retracted/` 记录原信号、推翻证据、误判原因与时间。

远程归档与本地目录都应生成 SHA-256 清单。本项目 `.gitignore` 排除 `security-results/`，避免目标与客户数据进入 Git。
