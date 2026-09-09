---
name: kali-security-remote
description: Use when an authorized security task must run in the Kali/Nuclei container on an SSH server, especially for long-running jobs, reconnecting after timeouts, or exporting results locally.
---

# Kali 远程执行

## 不可跳过的第一步

1. 调用 `ssh_list_servers`。
2. 向用户展示服务器候选并询问使用哪一台。
3. **停止并等待选择。**
4. 只有用户选择服务器且 `kali-security-scope` 已确认后，才能调用 `ssh_exec`。

不得固定默认服务器，也不得因为只有一台候选而自动选择。

## 固定运行环境

```text
image: docker.io/aoliyougei/kali-linux-nuclei-headless:v3.11.1-2026.3.4
container: kali-sec-<engagement-id>
network: host
command: sleep infinity
auto-remove: false
```

远程 Docker 命令只能通过已选择服务器的 `ssh_exec` 执行。创建前按名称检查容器：存在则恢复；停止则启动；不存在才拉取镜像并创建。禁止 `--rm`，禁止默认 `--privileged`。额外 Capability 必须解释并再次确认。

## 长任务

不要让扫描依赖 SSH 连接。按 `references/job-protocol.md` 将每项任务作为容器内幂等后台 job 提交。`ssh_exec` 超时、断线、输出截断或状态未知时：

- 保持容器运行；
- 不重跑、不停止、不删除；
- 重连后检查容器、job-id、PID、status 和 exit-code。

收到 `429`、持续 `5xx`、连接异常、封禁提示或暂停要求时停止发送新请求，保留任务与结果。

## 本地导出

按 `references/export-protocol.md`：先脱敏，远程 `docker cp` 与打包，分块传到当前项目的 `security-results/YYYY-MM-DD_<scheme-host-port|multi-target>_<engagement-id>/`，校验本地大小和 SHA-256。**只有本地校验成功后才停止容器和清理远程临时包。** 传输中断时沿用 engagement 开始日期和原目录续传，不重命名、不重扫。

## 完成条件

所有 job 有终态、结果已脱敏、完整归档已在本地校验，才执行远程 `docker stop kali-sec-<engagement-id>`。保留镜像，不触碰其他容器。

## 来源

方法论提炼自 [Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter)，Sachin Sharma / ElementalSoul，内容许可 CC BY 4.0。
