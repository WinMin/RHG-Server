FROM ubuntu:22.04

RUN  sed -i s@/archive.ubuntu.com/@/mirrors.tuna.tsinghua.edu.cn/@g /etc/apt/sources.list
RUN  apt-get clean

RUN apt update && \
    apt install python3 python3-pip -y

RUN python3 -m pip install flask pywebio pyOpenSSL requests pyecharts

RUN mkdir -p /pwn/server

COPY ./myserver.py /pwn/server/
COPY ./crawl.py /pwn/server/
COPY ./submit.py /pwn/server/


ENTRYPOINT ["python3", "/pwn/server/myserver.py"]

# docker build -t rhg .
# docker run --rm -p 8080:8080 -p 2222:22 -it 88789089bfa2 --host 172.16.48.192 --port 5001
