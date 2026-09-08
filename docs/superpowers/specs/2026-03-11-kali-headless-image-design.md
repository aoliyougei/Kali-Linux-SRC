# Kali Headless 镜像设计

## 目标

基于 `kalilinux/kali-rolling:latest` 构建镜像，安装：

- `kali-linux-headless`
- `kali-tools-top10`

最终镜像名称为 `kali-linux-headless:<version>`，其中 `<version>` 是镜像内已安装的 `kali-linux-headless` Debian 包版本。

## 实现

仓库中保留一个最小 `Dockerfile`：更新 APT 索引、非交互安装两个元包，并删除 APT 索引以减少镜像体积。

通过 `pi-docker-api` 构建临时标签，启动临时容器并执行 `dpkg-query` 获取 `kali-linux-headless` 的已安装版本，再为同一镜像添加最终标签 `kali-linux-headless:<version>`。

## 验证

在容器中使用 `dpkg-query` 验证两个包均已安装，并确认最终镜像标签存在。

## 范围

不增加入口脚本、额外配置、软件源或版本固定机制。基础滚动镜像更新后，重新构建可能产生新版本标签。
