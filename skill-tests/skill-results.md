# Skills 验证结果

## 静态结构

- 初次运行：FAIL 1，`kali-security-evidence` description 使用 `Use before`。
- 最小修正：改为 `Use when preparing to...`。
- 重跑：`PASS skills=10 structural_failures=0 forbidden_patterns=0 packages=1490 executable_entries=4317`。

验证范围：10 个 Skill 及必需 references、frontmatter、触发描述、CC BY 4.0 署名、固定镜像、SSH 选择顺序、host 网络、禁止 `--rm`/默认 privileged、断线保留、本地 SHA-256 后停止、库存行数、缺失工具标记、内网隔离和危险命令模式。

## 工具行为

- 包库存：1,490 行。
- 可执行入口：4,317 行（1,810 个解析后实际文件；包含符号链接）。
- Kali 元包直接工具目录：193 个包，其中 178 组具有可执行命令入口；含版本、命令和用途摘要。
- Nmap：定位到文件 capability 与容器 bounding set 冲突；验证 `setcap -r` + `-sT` 可运行。
- Web：FFUF、Gobuster、Dirb、Wfuzz 在 localhost fixture 命中。
- Nuclei：HTTP、Headless(system Chromium)、TCP、DNS(localhost)、SSL(localhost)、ECDSA 签名 Code 模板均命中并产生 JSONL。
- 脱敏：合成 Cookie、JWT、API key、密码、Token、PII 全部移除，endpoint 与 request ID 保留。
- DAVTest：发现缺少 Perl `Net::SSL`，标记为 unavailable。
- `jq`：镜像未安装；脱敏方案改为 Python 3 标准库并验证。

## Bug Bounty 默认值优化

- RED：扩展静态合同后运行旧 Skill，失败 18 项，包括范围证据、`@/www/*` 条件门禁、TCP Connect top-1000、非破坏性 Nuclei、默认 blackbox、禁止动作与禁止优先级。
- GREEN：更新 `kali-security-scope`、授权模板和 JSON 示例后，完整静态验证通过。
- 语义检查：JSON 可解析；授权依据为 `bug-bounty-scope`；范围证据非空；apex/www/wildcard 显式；Nmap `TCP Connect`/`top-1000`/`T3`；Nuclei 仅非破坏性 CVE/配置；25 并发/10 RPS；blackbox；10 项默认禁止动作全部通过。

## Bug Bounty 最小输入优化

- RED：旧流程在已有默认值时仍要求逐项填写；新增合同检查失败 14 项，包括最小输入、自动 engagement ID/窗口、同日序号和单次确认。
- GREEN：用户只需提供目标域名或 URL 与项目规则/范围证据；其余字段自动生成，范围歧义除外。
- 语义检查：自动 ID 来源、`<target>-YYYYMMDD[-NN]` 格式、窗口结束 `until-complete-or-user-stop`、默认 blackbox 与 10 项禁止动作全部通过。
- 首次 GREEN 检查仍因两个可检索文案字段不一致失败；仅统一“允许测试类型”和“UTC 日期”后完整通过。

## 压力场景与触发微测

**未执行。** 当前 Pi 环境没有子代理或独立 Agent API，无法创建 writing-skills 要求的全新上下文样本，也不能完成每个描述 5 次的独立触发微测。用户在执行前接受以完整场景、静态检查、Docker 集成和 SSH 断线恢复实测替代。未伪造 PASS。

待未来提供独立 Agent 能力后补测：`skill-tests/scenarios.md` 的 6 个 RED/GREEN 场景及每个 Skill 5 次 trigger/no-trigger 样本。

## SSH 断线恢复

服务器选择：先调用 `ssh_list_servers`，用户明确选择 `alyg-test-01` 后才使用 `ssh_exec`。

首次拉取被远程磁盘 100% 占满阻塞。经用户单独确认，只执行 `docker builder prune -a -f`，未删除镜像、容器或卷；释放约 46.4 GB，磁盘可用空间恢复到 39 GB。

无害 fixture 结果：

- 拉取固定镜像，digest `sha256:0c59a11d075ff56058a6e951b044acda9d714c1154d1a7f5337f27d160824c4d`。
- 容器 `kali-sec-skill-recovery-test`：host network、AutoRemove=false、Privileged=false。
- 后台 job `recovery-001` 初始 status=running、PID=26。
- 故意使用 1 秒 `ssh_exec` timeout；连接超时后不停止、不重跑。
- 重连时容器仍运行，job 已 succeeded，PID 正常退出，匹配 job 目录数为 1。
- 第一次归档 SHA-256 正确，但内部 `SHA256SUMS` 使用远程绝对路径，本地校验失败；保持容器运行，修正导出协议为相对路径后只重新打包，未重跑 job。
- 最终归档：922 bytes，SHA-256 `20033804dde04e84ebfa765433aae89e58b9cc7195839ebcd626d00a8fe7a33e`。
- 本地归档 SHA-256、内部 9 个文件 SHA-256 和 `recovery-ok` 内容全部通过。
- 只有校验通过后才停止容器；最终 container=exited，远程临时归档已删除。

结果保存在被 Git 忽略的 `security-results/skill-recovery-test/`。
