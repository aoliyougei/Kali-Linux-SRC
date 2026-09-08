# 端口扫描

## 默认 Nmap

Kali 的 Nmap 实际文件带 `cap_net_admin,cap_net_raw`。普通容器的 bounding set 不含 `NET_ADMIN` 时，甚至 `nmap --version` 都会返回 `Operation not permitted`。默认容器内先移除文件能力，再使用 TCP connect：

```sh
setcap -r /usr/lib/nmap/nmap
OUT=/work/jobs/<job-id>/results/recon/ports
nmap -sT -T3 --top-ports 1000 -sV --version-light -iL authorized-ips.txt -oA "$OUT/common"
```

- 路径 `/usr/bin/nmap`，包版本 7.99。
- `setcap -r` 只修改本次任务容器；不修改镜像或主机。
- 明确目标文件，先常用端口，保存 normal/XML/grepable。
- 不要自动添加 Capability。只有用户再次确认 SYN/原始包需求后，才以新容器配置 `NET_RAW`/`NET_ADMIN`。
- UDP、脚本扫描、全端口和认证脚本需按范围/影响再确认。
- 服务版本是候选；用 `curl`、`openssl s_client`、`nc` 或协议客户端复验。

## Masscan

路径 `/usr/bin/masscan`，版本 1.3.2。高吞吐、需要原始网络权限，默认 `confirm-active`。只有用户明确 CIDR、端口、速率和窗口后才提供执行命令；不得用默认高速值，不对真实目标给“一键全端口”示例。完成后必须用 Nmap 复验开放端口。

## 停止条件

`429`/封禁不适用于所有 TCP 服务，但连接错误明显增长、SOC 要求暂停、目标异常或窗口结束时立即停止新连接并保留结果。
