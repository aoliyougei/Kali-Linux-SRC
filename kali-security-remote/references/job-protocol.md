# 幂等后台任务协议

## 目录

每项任务固定写入：

```text
/work/jobs/<job-id>/
  command.sh metadata.json status pid started-at finished-at exit-code stdout.log stderr.log results/
```

`job-id` 只允许 `[A-Za-z0-9._-]`。命令中不得含凭据；凭据从容器内权限受限文件读取。

## 提交前检查

通过选定服务器上的 `ssh_exec` 执行状态查询：

```sh
docker inspect -f '{{.State.Status}}' "kali-sec-$ENGAGEMENT_ID"
docker exec "kali-sec-$ENGAGEMENT_ID" sh -lc '
  d="/work/jobs/$1"
  test -e "$d/status" && cat "$d/status" || echo absent
  test -e "$d/pid" && cat "$d/pid" || true
  test -e "$d/exit-code" && cat "$d/exit-code" || true
' sh "$JOB_ID"
```

状态不是 `absent` 时不得再次提交。`running` 时用 `kill -0 PID` 验证同一进程；终态直接读取结果。

## 一次性提交

先把经用户批准、已脱敏的 `command.sh` 放入 job 目录，再启动包装器。使用原子 `mkdir` 锁阻止重复：

```sh
docker exec "kali-sec-$ENGAGEMENT_ID" sh -lc '
  set -eu
  d="/work/jobs/$1"
  mkdir -p /work/jobs
  mkdir "$d" || { echo "job exists: $1" >&2; exit 73; }
  mkdir "$d/results"
  printf queued > "$d/status"
  date -u +%FT%TZ > "$d/started-at"
' sh "$JOB_ID"
```

上传 `command.sh` 后：

```sh
docker exec -d "kali-sec-$ENGAGEMENT_ID" sh -lc '
  d="/work/jobs/$1"
  nohup sh -c '\''
    d="$1"
    printf running > "$d/status"
    echo $$ > "$d/pid"
    rc=0
    sh "$d/command.sh" >"$d/stdout.log" 2>"$d/stderr.log" || rc=$?
    printf "%s" "$rc" > "$d/exit-code"
    date -u +%FT%TZ > "$d/finished-at"
    if [ "$rc" -eq 0 ]; then printf succeeded > "$d/status"; else printf failed > "$d/status"; fi
  '\'' sh "$d" </dev/null >/dev/null 2>&1 &
' sh "$JOB_ID"
```

## 恢复决策

| status | PID | 动作 |
|---|---|---|
| absent | — | 可创建 |
| queued | — | 检查 `command.sh` 与包装器；不得盲目重建 |
| running | `kill -0` 成功 | 继续轮询同一 job |
| running | PID 不存在 | 标记 failed，记录原因；询问是否新 job-id 重试 |
| succeeded | — | 脱敏、导出、校验 |
| failed | — | 查看日志；修复后使用新 job-id |
| paused | — | 保留；用户确认后使用新 job-id 续作 |

SSH 超时不改变 status。状态未知时默认“仍在运行”。禁止同 job-id 自动重试。
