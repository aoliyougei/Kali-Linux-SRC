# 授权摘要模板

```yaml
engagement_id: example-2026
basis: owned-asset | written-authorization | bug-bounty-scope | ctf
bug_bounty_scope_evidence: <program URL, rule snapshot path, or quoted scope identifiers; no credentials>
explicit_targets:
  apex: []       # @，仅规则明确包含根域时填写
  www: []        # 仅规则明确包含 www 时填写
  wildcard: []   # 仅规则明确包含 *.domain 时填写
  ips: []
  cidrs: []
  urls: []
allowed_tests:
  dns_and_public_information: all-nondestructive
  network_discovery:
    scan_type: TCP Connect
    ports: top-1000
    nmap_timing: T3
  web_recon: [http-tls-baseline, soft-404, fingerprinting, low-rate-content-discovery]
  nuclei: [non-destructive-cve, non-destructive-configuration]
  manual_validation: read-only
denied_tests:
  - login-attempts
  - password-spraying-or-credential-stuffing
  - otp-or-mfa-testing
  - file-upload
  - state-changing-requests
  - sql-injection-exploitation-or-data-extraction
  - oob-or-interactsh
  - shell-access
  - dos-or-resource-exhaustion
  - bulk-data-access-or-exfiltration
rates:
  concurrency: 25
  requests_per_second: 10
  nmap_timing: T3
  ports: top-1000
window:
  start: YYYY-MM-DDTHH:MM:SS+TZ
  end: YYYY-MM-DDTHH:MM:SS+TZ
mode: blackbox
```

Bug Bounty 默认值只有在项目规则证据明确支持目标时使用；禁止列表优先。只记录授权类型与操作边界，不复制合同正文、联系人隐私或凭据。
