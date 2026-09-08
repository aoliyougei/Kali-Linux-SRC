# 凭据审计边界

## 离线、自有样本

| 工具 | 版本 | 安全实验室示例 |
|---|---:|---|
| John the Ripper | Jumbo 1.9 | `printf '5f4dcc3b5aa765d61d8327deb882cf99:password\n' > owned-sample.txt; john --format=raw-md5 --wordlist=owned-words.txt owned-sample.txt` |
| Hashcat | 7.1.2 | `hashcat -m 0 owned-hashes.txt owned-words.txt --potfile-path owned.pot --session owned-lab` |

只处理用户拥有、合法取得且允许审计的哈希。输出和 potfile 是敏感凭据数据，不进入报告/归档；结束后按授权销毁。GPU 设备映射需再次确认。

## 在线认证工具

Hydra 9.7、Ncrack 0.7、Patator 1.1 已安装，但默认不提供真实目标命令。任何使用都必须再次确认：精确服务、测试账号、每账号尝试上限、锁定策略、速率、窗口和监控联系人。

禁止密码喷洒、凭据填充、真实用户列表、OTP/MFA 穷举和规避锁定。即使用户说“肯定没事”也不能用外部授权替代内网/账号专项授权。
