# Headless 与系统 Chromium

镜像包含 Chromium 150.0.7871.181。强制使用系统浏览器，避免 Nuclei 在运行时下载额外 Chromium：

```sh
nuclei -list authorized-urls.txt -templates reviewed-headless/ \
  -headless -system-chrome -headless-concurrency 2 \
  -rate-limit 10 -jsonl-export "$OUT/headless.jsonl"
```

- root 容器会禁用浏览器 sandbox；这是隔离折衷，不扩大目标授权。
- Headless 资源高，默认 `-headless-concurrency 2`。
- 审阅 action：navigate、click、text、script、files、wait 等；会提交表单、上传或触发动作的模板再次确认。
- 用 `chromium --headless --no-sandbox --dump-dom URL` 对只读页面复验；截图前脱敏。
- 浏览器崩溃、下载另一个浏览器、目标状态变化或内存压力异常时停止。
