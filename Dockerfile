FROM kalilinux/kali-rolling:latest

RUN printf '%s\n' 'deb http://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware' > /etc/apt/sources.list \
 && rm -f /etc/apt/sources.list.d/kali.sources \
 && apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      kali-linux-headless \
      kali-tools-top10 \
 && rm -rf /var/lib/apt/lists/*
