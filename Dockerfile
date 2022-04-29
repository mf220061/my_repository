FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    perl \
    wget \
 && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/src/latex \
    && wget http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz \
    && tar -zxvf install-tl-unx.tar.gz -C /usr/src/latex

WORKDIR /usr/src/latex/install-tl-20220322

RUN echo I | ./install-tl -no-gui -repository http://mirror.ctan.org/systems/texlive/tlnet/

RUN /usr/local/texlive/2021/bin/x86_64-linux/tlmgr path add

WORKDIR /root/result
