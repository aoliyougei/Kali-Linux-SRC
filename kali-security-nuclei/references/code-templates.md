# Code 模板

Code 模板可运行宿主解释器，默认 `confirm-active`。执行前逐行审阅 `source`、engine、文件/网络访问与输出；禁止下载执行、持久化、凭据访问、反向 shell 或范围外请求。

## ECDSA 测试签名

密钥不得进入 Git、命令日志或归档。使用容器内权限 600 文件：

```sh
umask 077
mkdir -p /root/.config/nuclei/keys
openssl ecparam -name prime256v1 -genkey -noout \
  -out /root/.config/nuclei/keys/nuclei-user-private-key.pem
openssl req -new -x509 \
  -key /root/.config/nuclei/keys/nuclei-user-private-key.pem \
  -out /root/.config/nuclei/keys/nuclei-user.crt -days 1 \
  -subj '/CN=authorized-nuclei-code'
NUCLEI_USER_PRIVATE_KEY=/root/.config/nuclei/keys/nuclei-user-private-key.pem \
NUCLEI_USER_CERTIFICATE=/root/.config/nuclei/keys/nuclei-user.crt \
  nuclei -templates reviewed-code.yaml -sign
```

运行：

```sh
NUCLEI_USER_CERTIFICATE=/root/.config/nuclei/keys/nuclei-user.crt \
  nuclei -list authorized-urls.txt -templates reviewed-code.yaml -code \
  -rate-limit 10 -jsonl-export "$OUT/code.jsonl"
```

未签名/篡改 Code 模板被拒绝是预期行为。完成并导出后删除私钥和容器内凭据；报告保留模板与证书指纹，不保留私钥。
