# 模板管理与信任

## 更新与验证

模板更新会访问外部服务，首次任务范围确认后可执行：

```sh
nuclei -update-templates
nuclei -validate -templates /root/nuclei-templates
```

记录模板版本、更新时间和目录哈希。滚动更新会改变结果；复现报告时保留具体模板文件及 SHA-256。

## 执行前审阅

检查：协议、请求方法、路径、payload 数量、fuzz、OOB/interactsh、Headless action、Code source、认证字段、写入/删除/上传动作。仅标签名或 severity 不能证明安全。

社区签名不等于目标授权，也不保证无副作用。自定义模板保存到 job 目录，记录来源与 SHA-256；未知模板先 `-validate`，再人工读文件。

## 协议复验

| Nuclei protocol | second verifier |
|---|---|
| http | curl + body/hash diff |
| dns | dig against second resolver |
| tcp | nmap `-sT` + native client |
| ssl | openssl s_client / sslyze |
| headless | chromium `--dump-dom` / screenshot |
| code | read source + invoke approved interpreter in lab |
