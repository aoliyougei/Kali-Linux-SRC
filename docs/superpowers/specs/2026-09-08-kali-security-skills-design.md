# Kali Security Skills 设计

## 1. 目标

在项目根目录创建一组可复用 Agent Skills，将 Claude-BugHunter 的授权外部安全评估方法论与以下固定容器镜像结合：

```text
docker.io/aoliyougei/kali-linux-nuclei-headless:v3.11.1-2026.3.4
```

Skills 使用中文说明，命令、参数和工具原始输出保持英文。实际安全任务通过 `ssh_exec` 在用户选择的远程服务器上执行。镜像工具盘点是 Skill 编写前的一次性调研，不属于 Skill 每次运行的步骤。

## 2. 来源与署名

方法论提炼自：

```text
Claude-BugHunter by Sachin Sharma / ElementalSoul
https://github.com/elementalsouls/Claude-BugHunter
Content licensed under CC BY 4.0
```

仅提炼授权门禁、阶段化流程、验证纪律、证据卫生和报告结构；工具说明以目标镜像中的实际工具、版本和帮助信息重新编写，不大量复制参考项目内容。

## 3. 范围

### 3.1 默认范围

默认 Skills 仅用于用户拥有或获得明确授权的外部攻击面：

- Web 与 API
- 公网域名、DNS、TLS、端口和服务
- 子域与公开情报
- Nuclei 模板扫描及人工复验
- 外部网络安全配置与已知漏洞验证

### 3.2 隔离范围

内网、AD、SMB 和凭据审计工具由独立 `kali-security-internal` Skill 管理。使用前必须重新确认专项授权、明确网段、账号测试规则、速率和时间窗口。

### 3.3 始终禁止

- 未授权资产扫描
- DoS、资源耗尽和大规模暴力破解
- 数据破坏、批量下载或不必要的数据外传
- 持久化、横向移动、恶意软件和规避检测
- Mimikatz、Empire 等后渗透能力的实战命令
- 未经明确许可使用特权容器

## 4. Skill 结构

项目根目录新增：

```text
kali-security-scope/
kali-security-remote/
kali-security-inventory/
kali-security-recon/
kali-security-web/
kali-security-nuclei/
kali-security-validation/
kali-security-evidence/
kali-security-reporting/
kali-security-internal/
```

职责：

| Skill | 职责 |
|---|---|
| `kali-security-scope` | 授权、目标范围、测试类型、速率、时间窗口和禁止行为的前置门禁 |
| `kali-security-remote` | SSH 服务器选择、远程容器生命周期、后台任务、断线恢复和结果传输 |
| `kali-security-inventory` | 镜像工具、版本、路径、能力、权限和可用性查询入口 |
| `kali-security-recon` | 外部 DNS、端口、HTTP、TLS、指纹和 OSINT |
| `kali-security-web` | Web/API 内容发现、低影响扫描和工具路由 |
| `kali-security-nuclei` | Nuclei 模板、JSONL、Headless、Chromium、Code 模板签名和复验 |
| `kali-security-validation` | 假阳性门禁、独立复现、严重性判断和发现状态 |
| `kali-security-evidence` | 日志、HTTP 证据、凭据和 PII 脱敏 |
| `kali-security-reporting` | 覆盖、发现、阴性结果、修复建议和最终报告 |
| `kali-security-internal` | 与外部流程隔离的内网/AD/SMB/凭据审计授权与只读工具路由 |

每个 Skill 使用精简 `SKILL.md`。详细工具知识放在各自的 `references/` 中，防止不相关内容占用上下文。

## 5. 授权门禁

任何扫描前必须获得并记录：

```text
engagement-id
授权依据：自有资产 / 书面授权 / Bug Bounty 明确范围 / CTF
明确目标：域名、IP、CIDR、URL
允许的测试类型
禁止项
标准速率与并发
允许时间窗口
blackbox / greybox
```

规则：

- 授权描述模糊、目标仅为组织名称或范围无法确定时停止。
- 通配符范围在执行前解析为明确资产清单。
- 执行中发现的新资产只记录，不探测，直到用户追加授权。
- 授权文件只记录授权类型与范围，不复制合同或 SoW 正文。
- 子任务必须携带明确目标列表和禁止动作，不允许隐式继承模糊范围。

## 6. 自动执行与确认边界

### 6.1 初次授权后可自动执行

- DNS、WHOIS、证书和公开情报查询
- 存活检测、HTTP 指纹和 soft-404 基线
- 标准速率端口扫描
- 公开路径与内容发现
- Nuclei 非破坏性模板
- TLS、HTTP 安全配置和已知 CVE 线索检查
- 只读、低影响人工复验

### 6.2 必须再次确认

- 登录、OTP、密码重置和凭据审计
- 文件上传及 POST/PUT/PATCH/DELETE 状态变更
- OOB/Interactsh 回连
- 全端口高速扫描或提高速率
- `NET_RAW`、`NET_ADMIN`、设备映射或额外 Capability
- 可能产生费用、通知、邮件、短信或审计告警的操作
- 内网/AD 工具加载与运行

### 6.3 标准速率

```text
Nuclei/HTTP：不超过 25 并发和 10 RPS
目录发现：不超过 10 RPS
Nmap：默认 -T3，先扫描常用端口
Masscan：默认不启用，需单独确认范围与速率
认证接口：默认不扫描
```

遇到 `429`、持续 `5xx`、异常连接增长、封禁提示或用户要求暂停时，停止发送新请求并保留任务状态。

## 7. 远程执行模型

### 7.1 强制顺序

```text
列出 SSH 服务器并询问用户选择
  → 确认授权与范围
  → 检查 Docker 并拉取镜像
  → 恢复或创建常驻容器
  → 提交后台任务
  → 轮询任务状态
  → 脱敏、导出并校验本地结果
  → 停止容器
```

Skill 必须先调用 `ssh_list_servers` 并询问用户。用户选择前禁止调用 `ssh_exec`。不得固定或自动选择服务器。

### 7.2 容器

```text
image: docker.io/aoliyougei/kali-linux-nuclei-headless:v3.11.1-2026.3.4
network: host
name: kali-sec-<engagement-id>
command: sleep infinity
auto-remove: false
```

- 不使用 `--rm`。
- 不默认使用 `--privileged`。
- 同名容器存在时先检查状态并恢复，不重复创建。
- 全部任务完成、本地结果校验成功后才停止容器。
- SSH 超时、断线或状态未知时保持容器运行。

### 7.3 后台任务

长任务在容器内后台运行，不依赖 SSH 会话。每个任务使用唯一 `job-id`：

```text
/work/jobs/<job-id>/
├── command.sh
├── metadata.json
├── status
├── pid
├── started-at
├── finished-at
├── exit-code
├── stdout.log
├── stderr.log
└── results/
```

- 同一 `job-id` 不得并发执行两次。
- 恢复连接后先检查容器、PID、状态文件和结果，再决定后续动作。
- 只有确认任务进程已退出且任务失败，才允许重新提交。
- 用户暂停时停止任务进程，但默认保留容器和结果。
- 用户取消涉及删除时，必须列明将删除的数据并再次确认。

## 8. Greybox 凭据

同时支持 blackbox 与 greybox。

- 不在聊天、`ssh_exec` 命令参数、进程参数或日志中传递明文凭据。
- 用户预先将凭据放在选定远程服务器的权限受限文件中，建议 `chmod 600`。
- Skill 只询问远程凭据文件路径，将其复制到容器临时目录。
- 日志和导出产物不得回显 Cookie、JWT、密码、API Key 或 Token。
- SSH 恢复后复用容器内凭据，不重新传输。
- 完成并成功导出后删除容器内副本；不修改远程原始凭据文件。

## 9. 断线恢复与本地结果传输

最终结果保存到本地项目：

```text
security-results/<engagement-id>/
```

`ssh_exec` 没有直接文件下载接口，因此采用可恢复分块传输：

1. 容器内完成结果与日志脱敏。
2. 远程执行 `docker cp` 导出任务目录并生成临时压缩包。
3. 生成远程文件清单、文件大小和 SHA-256。
4. 通过多次 `ssh_exec` 按固定编号读取 Base64 分块。
5. 本地逐块保存并合并、解码。
6. 本地校验大小和 SHA-256。
7. 校验成功后停止容器并删除远程临时压缩包。
8. 传输中断时从最后一个已校验分块继续；不重新扫描。

网络中断、SSH 超时或传输状态不明时，不停止或删除容器。

## 10. 本地结果结构

```text
security-results/<engagement-id>/
├── authorization.md
├── scope.json
├── tool-versions.tsv
├── execution-manifest.json
├── commands/
├── logs/
├── recon/
│   ├── dns/
│   ├── hosts/
│   ├── ports/
│   ├── http/
│   └── tls/
├── scans/
│   ├── nuclei/
│   ├── nmap/
│   └── web/
├── findings/
│   ├── confirmed/
│   ├── candidates/
│   ├── killed/
│   └── retracted/
├── evidence/
├── report.md
└── SHA256SUMS
```

- `commands/` 只保存脱敏后的可复现命令。
- `killed/` 保存排除的误报，避免重复测试。
- `execution-manifest.json` 记录服务器别名、镜像 digest、容器名、任务 ID、时间、退出码和恢复次数，不记录凭据。
- `security-results/` 加入 `.gitignore`。

## 11. 工具知识库

### 11.1 一次性实测基线

目标镜像已启动并初步确认：

```text
Debian packages: 1490
Executable files: 1682
kali-linux-headless: 2026.3.4
kali-tools-top10: 2026.3.4
nuclei: v3.11.1
chromium: 150.0.7871.181
```

实现阶段继续从该运行容器提取包、可执行文件、所属包、版本、帮助和运行依赖。

### 11.2 完整索引

```text
kali-security-inventory/references/
├── packages.tsv
├── executables.tsv
├── security-tools.md
└── capability-matrix.md
```

### 11.3 工具手册

```text
kali-security-recon/references/
├── dns-tools.md
├── host-discovery.md
├── port-scanning.md
├── http-fingerprinting.md
└── osint-tools.md

kali-security-web/references/
├── content-discovery.md
├── web-scanners.md
├── api-testing.md
├── injection-tools.md
└── proxy-and-traffic.md

kali-security-nuclei/references/
├── nuclei-cli.md
├── templates.md
├── headless.md
└── code-templates.md

kali-security-internal/references/
├── smb-ad-tools.md
├── credential-auditing.md
└── restricted-tools.md
```

每个安全工具条目包含：

```text
实际命令与路径
镜像内版本
用途与适用阶段
授权级别
所需输入
默认安全命令
关键参数
输出格式与保存路径
运行权限或 Capability
网络影响与标准速率
结果复验方法
常见误报和停止条件
禁止或需再次确认的操作
```

### 11.4 路由原则

- 被动、低影响工具优先于主动工具。
- 每个主机先建立 soft-404、DNS、HTTP 正常响应基线。
- 自动化扫描只生成候选线索。
- Nuclei 结果必须按协议由第二种工具复验。
- Critical/High 必须由两种独立工具或协议栈复现。
- 无线、蓝牙、USB 和磁盘取证工具进入索引，但标记为需要设备映射且不属于默认外部流程。
- 范围外工具不会因为镜像中存在而自动启用。

## 12. 内网与高风险工具

镜像内的 NetExec、Impacket、Enum4linux、SMBMap、Responder、Hydra、Ncrack、Metasploit 等工具完整记录，但默认外部流程不加载。

`kali-security-internal`：

- 强制重新确认内网专项授权。
- 只提供枚举、只读检查和实验室安全示例。
- 真实目标上的凭据审计、认证请求或利用需要再次确认。
- 不提供 Mimikatz、Empire、持久化、横向移动或规避检测的实战命令。

## 13. 方法论与验证门禁

流程：

```text
授权与范围 → 侦察 → 攻击面排序 → 聚焦测试 → 验证 → 证据 → 报告
```

核心规则：

- 为每个主机和必要的路径深度记录 soft-404 控制：状态、长度、正文哈希。
- Marker 使用至少 8 字符的唯一随机串，并先确认基线中不存在。
- 绕过结论必须比较正文、长度和哈希，不能只看 HTTP 状态码。
- 时间差结论至少使用每组 10 次交错样本，并计算均值、中位数与标准差。
- 自动化告警必须人工复验。
- Critical/High 使用两个独立工具或协议栈复现。
- 验证影响后停止，不扩大为批量真实数据获取。
- 报告前执行七问验证，结论为 `PASS`、`KILL`、`DOWNGRADE` 或 `CHAIN-REQUIRED`。
- 被否定的候选保留在 `killed/`；已确认后失效的发现记录在 `retracted/`，不静默删除。

## 14. 证据卫生

- Cookie、Authorization、JWT、Token、API Key、密码和 CSRF Token 一律脱敏。
- 其他用户 PII 仅保留证明漏洞所需字段形状，具体值遮盖。
- 保留有助于复现的请求 ID、时间、接口、方法和响应结构。
- 原始结果先脱敏，后传输到本地。
- 报告和命令不得出现真实凭据。

## 15. 报告

`report.md` 包含：

1. 授权与范围摘要
2. 执行环境和镜像版本
3. 方法与覆盖范围
4. 攻击面清单
5. 已确认发现
6. 待人工验证线索
7. 阴性测试与覆盖证明
8. 被排除或撤回的误报
9. 风险与修复建议
10. 工具、命令和证据索引
11. 局限性
12. SHA-256 文件清单

## 16. Skill TDD 与验收

遵循 writing-skills 的 RED/GREEN/REFACTOR：

### RED：无 Skill 基线场景

验证代理是否会：

- 在授权模糊时直接扫描；
- 未询问就选择 SSH 服务器；
- SSH 中断后重复任务或停止容器；
- 将 Nuclei 告警直接认定为漏洞；
- 在命令或日志中泄露凭据；
- 自动使用内网或高风险工具。

记录实际失败行为和理由。

### GREEN：加载 Skill 后

相同场景必须表现为：

- 先确认授权和明确范围；
- 先列出并询问 SSH 服务器；
- 恢复已有容器与 `job-id`；
- 执行假阳性和独立复现门禁；
- 本地导出和 SHA-256 校验后才停止容器；
- 内网能力必须经过独立授权 Skill。

### REFACTOR：封堵新漏洞

对测试中出现的新绕过理由补充最小规则并重测。

### 工具参考检索测试

- 给定任务时找到正确工具和参考文件。
- 命令与镜像内实际 `--help` 一致。
- 能说明权限、风险、输出路径和第二工具复验方式。
- 镜像中不存在的工具明确标记为不可用，不编造命令。

### 断线恢复测试

在后台测试任务中模拟 SSH 超时，确认容器继续运行、任务不重复，并在恢复后继续轮询和分块导出。

## 17. 最终交付

- 10 个项目级 Skill 目录
- 完整包与可执行文件清单
- 外部安全工具使用手册
- 隔离的内网工具安全手册
- 远程任务状态和断线恢复规范
- 授权、验证、证据和报告模板
- Skill 测试场景及验证记录
- 设计文档与实施计划
