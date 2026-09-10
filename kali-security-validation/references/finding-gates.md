# Finding Gate

## 前置：平台接受性

严重性判断之前先记录：项目是否接受该漏洞类型、是否在 OOS/不收录列表、是否明确禁止重报。未通过平台接受性：`KILL`；技术事实成立则同时标记 `HARDENING`。

## 八问记录

```yaml
q1_reproducible_now: yes|no
q2_platform_accepts_type: yes|no|unknown
q3_accepted_impact: yes|no
q4_in_explicit_scope: yes|no
q5_attacker_realistic_access: yes|no
q6_not_known_documented_duplicate_or_no-resubmit: yes|no
q7_concrete_impact_proved: yes|partial|no
q8_not_invalid_standalone: yes|chain-required|no
disposition: VULNERABILITY|HARDENING|NONE
outcome: PASS|KILL|DOWNGRADE|CHAIN-REQUIRED
```

- Q2 为 `no`/`unknown`：`KILL`，不得进入严重性判断。
- Q1/Q3/Q4/Q5/Q6 为 `no`：`KILL`。
- Q7 partial：`DOWNGRADE` 或继续最小化验证；不是 High/Critical。
- Q8 chain-required：只有完整链被实际证明后才 PASS。

## 常见假阳性

- 200 与不存在路径正文哈希相同：soft-404，KILL。
- 403→200 但正文等同：不是绕过。
- 输入校验 400：不证明已通过认证层；用最小合法 body 重试。
- banner/版本：只证明线索；需供应商证据和可控复验。
- 单次延迟：网络抖动；按统计规则重测。
- Marker 天然存在于基线：更换随机 Marker。
- Nuclei/Nikto/SQLMap 标题、severity、CWE 或多工具复现：只证明线索/技术事实，不证明平台接受性或实际安全影响。
- 已转义纯文本内容欺骗、无影响 Cookie/HSTS、普通重写配置、TLS 1.0/1.1 合规偏离、无秘密 Source Map：默认 `KILL/HARDENING`。
- 审核理由与主题错配：标记 `review-reason-mismatch`，可询问但不重报。

## 新证据与重报

平台明确不收录或无需重报时，不得换标题、拆分资产或改写理论影响再次提交。只有出现全新实际安全影响证据，才建立新 candidate 并重新执行授权、平台接受性、八问和独立复现。

## 最小影响

只证明一个测试账号、一个对象或最小记录。不得为“证明规模”批量抓取他人数据。可用可验证的对象计数/权限逻辑说明潜在范围，而非执行扩大化获取。
