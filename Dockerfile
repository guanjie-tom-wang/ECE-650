FROM ubuntu:20.04

# RUN sed -i "s/archive.ubuntu./mirrors.aliyun./g" /etc/apt/sources.list
# RUN sed -i "s/deb.debian.org/mirrors.aliyun.com/g" /etc/apt/sources.list
# RUN sed -i "s/security.debian.org/mirrors.aliyun.com\/debian-security/g" /etc/apt/sources.list
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install build-essential -y
RUN apt-get install wget -y
RUN wget -qO- "https://cmake.org/files/v3.17/cmake-3.17.0-Linux-x86_64.tar.gz" | tar --strip-components=1 -xz -C /usr/local
RUN apt-get install zlib1g-dev -y
RUN apt-get install vim -y
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y gdb


WORKDIR /app

COPY ./a4 /app

CMD ["sh", "-c", "mkdir build && cd build && cmake ../ && make && ./a4-ece650"]