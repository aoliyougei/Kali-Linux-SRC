# Finding Gate

## 七问记录

```yaml
q1_reproducible_now: yes|no
q2_accepted_impact: yes|no
q3_in_explicit_scope: yes|no
q4_attacker_realistic_access: yes|no
q5_not_known_or_documented: yes|no
q6_concrete_impact_proved: yes|partial|no
q7_not_invalid_standalone: yes|chain-required|no
outcome: PASS|KILL|DOWNGRADE|CHAIN-REQUIRED
```

- Q1/Q2/Q3/Q4/Q5 为 `no`：`KILL`。
- Q6 partial：`DOWNGRADE` 或继续最小化验证；不是 High/Critical。
- Q7 chain-required：只有完整链被实际证明后才 PASS。

## 常见假阳性

- 200 与不存在路径正文哈希相同：soft-404，KILL。
- 403→200 但正文等同：不是绕过。
- 输入校验 400：不证明已通过认证层；用最小合法 body 重试。
- banner/版本：只证明线索；需供应商证据和可控复验。
- 单次延迟：网络抖动；按统计规则重测。
- Marker 天然存在于基线：更换随机 Marker。
- Nuclei/Nikto/SQLMap 标题或 severity：不是漏洞证据。

## 最小影响

只证明一个测试账号、一个对象或最小记录。不得为“证明规模”批量抓取他人数据。可用可验证的对象计数/权限逻辑说明潜在范围，而非执行扩大化获取。
