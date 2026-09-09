# 可恢复的本地导出协议

## 前置条件

所有任务已到终态。先按 `kali-security-evidence` 对日志、HTTP、JSONL、命令和证据脱敏；凭据文件不进入归档。

## 远程打包

在用户选择的服务器执行：

```sh
set -eu
c="kali-sec-$ENGAGEMENT_ID"
out="/tmp/kali-sec-$ENGAGEMENT_ID"
archive="$out.tar.gz"
rm -rf "$out" "$archive"
mkdir -p "$out"
docker cp "$c:/work/." "$out/"
find "$out" -type f -name '*credential*' -delete
(cd "$out" && find . -type f -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS)
TZ=UTC tar --sort=name --mtime='UTC 1970-01-01' --owner=0 --group=0 --numeric-owner \
  -C /tmp -czf "$archive" "kali-sec-$ENGAGEMENT_ID"
stat -c '%s' "$archive"
sha256sum "$archive"
```

记录大小与 SHA-256。不要停止容器。

## 分块读取

固定原始块大小 `786432` 字节（Base64 后约 1 MiB）。先计算块数，再逐块读取：

```sh
size=$(stat -c '%s' "/tmp/kali-sec-$ENGAGEMENT_ID.tar.gz")
chunk=786432
echo $(((size + chunk - 1) / chunk))

dd if="/tmp/kali-sec-$ENGAGEMENT_ID.tar.gz" bs=786432 skip="$INDEX" count=1 status=none \
  | base64 -w0
```

本地保存到当前项目目录下的规范化结果目录：

```text
security-results/YYYY-MM-DD_<scheme-host-port|multi-target>_<engagement-id>/.transfer/chunk-000000.b64
security-results/YYYY-MM-DD_<scheme-host-port|multi-target>_<engagement-id>/.transfer/manifest.json
```

目录日期使用 engagement 开始日期（UTC，`YYYY-MM-DD`），保证断线恢复时名称不变。单 URL 只取小写 `scheme + hostname + 非默认端口`，非字母数字字符折叠为 `-`；丢弃 userinfo、path、query、fragment，防止 Token/PII 进入文件名。默认端口 80/443 省略。例如 `https://Example.COM/api?q=secret` 变为 `2026-09-09_https-example-com_<engagement-id>`。多目标统一使用 `multi-target`。

每块只有完整返回后才写入 manifest。SSH 中断时从首个缺失编号继续，不重复扫描。

## 本地合并与校验

使用本地文件工具合并 Base64 文本并解码；计算本地文件大小与 SHA-256，必须与远程值完全相同。解压到同一规范化目录；不得在恢复时根据当前日期重新命名：

```text
security-results/YYYY-MM-DD_<scheme-host-port|multi-target>_<engagement-id>/
```

校验归档内 `SHA256SUMS`，确认没有凭据文件或明文 Cookie/Authorization/JWT/API Key。

## 清理顺序

仅在本地大小、归档 SHA-256、内部 `SHA256SUMS` 和脱敏检查全部通过后：

```sh
docker stop "kali-sec-$ENGAGEMENT_ID"
rm -rf "/tmp/kali-sec-$ENGAGEMENT_ID" "/tmp/kali-sec-$ENGAGEMENT_ID.tar.gz"
```

未知状态、传输中断或校验失败：保留容器和远程归档，报告最后成功块编号。不得使用 `docker rm`，除非用户另行确认删除。
