---
name: kali-security-inventory
description: Use when selecting, locating, or checking availability, version, ownership, risk, and runtime requirements of tools in the fixed Kali/Nuclei image.
---

# Kali 镜像工具库存

这是静态、实测的查询入口，不要求每次任务重新盘点镜像。

1. 在 `references/executables.tsv` 按命令名查路径、解析路径和所属包。
2. 在 `references/packages.tsv` 查全部安装版本与 `ii` 状态。
3. 在 `references/tool-usage-catalog.tsv` 查 193 个 Kali 元包直接工具包、178 组命令入口及用途摘要。
4. 在 `references/security-tools.md` 查常用安全工具的经过实测的安全用法与已知限制。
5. 在 `references/capability-matrix.md` 查授权级别、网络影响、Capability 和复验工具。
6. 再按任务加载 `kali-security-recon`、`kali-security-web`、`kali-security-nuclei` 或经二次授权的 `kali-security-internal`。

若命令不在清单中，明确回答 **not installed**；不得靠相似包名推断、临时安装或编造参数。目录只有用途摘要而没有人工手册时，先从 `executables.tsv` 定位，再运行无副作用 `--help`/`man` 并向用户说明授权级别；不得猜参数。特别注意 `/usr/bin/httpx` 是 Python HTTP 客户端，不是 ProjectDiscovery httpx。

版本与实际服务器镜像可能漂移时，用无副作用的 `command -v`、`--version`/`-version` 复核，并记录镜像 digest；不要执行全面重盘点。

方法论提炼自 [Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter)，Sachin Sharma / ElementalSoul，CC BY 4.0。
