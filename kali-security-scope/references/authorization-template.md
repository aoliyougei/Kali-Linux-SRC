# 授权摘要模板

```yaml
engagement_id: example-2026
basis: owned-asset | written-authorization | bug-bounty-scope | ctf
explicit_targets:
  domains: []
  ips: []
  cidrs: []
  urls: []
allowed_tests: []
denied_tests: []
rates:
  concurrency: 25
  requests_per_second: 10
  nmap_timing: T3
  ports: common
window:
  start: YYYY-MM-DDTHH:MM:SS+TZ
  end: YYYY-MM-DDTHH:MM:SS+TZ
mode: blackbox | greybox
```

只记录授权类型与操作边界，不复制合同正文、联系人隐私或凭据。
