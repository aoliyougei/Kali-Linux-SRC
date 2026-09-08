# 脱敏规则

## 文本与 HTTP

用字段边界替换值，不删除复现结构：

```text
Cookie: <REDACTED>
Set-Cookie: <REDACTED>
Authorization: <REDACTED>
X-API-Key: <REDACTED>
password=<REDACTED>
```

对 JWT 检查 `eyJ...`.`...`.`...` 三段模式；对私钥检查 `BEGIN .* PRIVATE KEY`。敏感值可能出现在 URL、请求体、响应、错误、shell history 和工具 JSON 中，必须全目录复查。

## HAR/JSON

镜像中未安装 `jq`；使用 Python 标准库按键名递归脱敏，而非只处理顶层：

```python
import json, re, sys
sensitive = re.compile(r"^(cookie|set-cookie|authorization|x-api-key|api_key|token|access_token|refresh_token|password|csrf.*)$", re.I)
def redact(value):
    if isinstance(value, dict):
        return {k: "<REDACTED>" if sensitive.match(k) else redact(v) for k, v in value.items()}
    if isinstance(value, list):
        return [redact(v) for v in value]
    return value
with open(sys.argv[1]) as src, open(sys.argv[2], "w") as dst:
    json.dump(redact(json.load(src)), dst, ensure_ascii=False, indent=2)
```

处理 JSONL 时逐行 `json.loads`；解析失败的行转入人工审查，不原样放行。保存脚本到 job 的 `commands/` 以便审计。

## PII

其他用户姓名、邮箱本地部分、电话、地址、生日、证件、头像和可关联 ID 脱敏。保留字段名、类型、攻击者测试账号标识及 request ID。只展示证明跨账号影响所需的最少记录。

## 截图与流量

截图前隐藏 Cookie/Headers/Authorization；截图后全分辨率复查。PCAP/HAR 默认视为敏感，先最小化过滤。禁止把私钥、凭据文件和未脱敏原始流量传回本地。

## 回归检查

在合成 fixture 中植入已知假秘密，脱敏后断言假值全部消失，同时 endpoint 与 request ID 保留。真实任务还需人工抽查，自动正则不是完整保证。
