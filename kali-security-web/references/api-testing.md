# API 与协议检查

## Curl 基线

```sh
curl -skS --max-time 15 -D "$OUT/response.headers" -o "$OUT/response.body" \
  -w '%{http_code}\t%{size_download}\t%{time_total}\n' \
  https://authorized.example/api/health
sha256sum "$OUT/response.body"
```

- 默认 GET/HEAD；写方法、上传、认证和状态变化前再次确认。
- 比较正文/长度/哈希，不凭状态码推断授权绕过。
- 重定向到范围外第三方时停止跟随主动测试。

## OpenSSL

```sh
printf '' | openssl s_client -connect authorized.example:443 -servername authorized.example \
  -verify_return_error >"$OUT/tls.txt" 2>&1
```

用于证书链、SNI 和 TLS 复验，不绕过认证。

## DAVTest

`davtest` 包已安装，但实测连 `--help` 都因缺少 Perl `Net::SSL` 退出，当前镜像中不可用。不得在任务中临时安装依赖。使用 `curl -X OPTIONS` 做只读能力识别；任何上传验证都必须另行设计并确认写入、清理和允许文件类型。

## API 判断

验证认证层时使用解析器可接受的最小合法请求；畸形请求触发 400 不证明绕过认证。Greybox 凭据从容器内权限 600 文件读取，命令与日志仅显示 `<REDACTED>`。
