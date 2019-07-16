FROM nvidia/cuda:10.0-cudnn7-runtime # OR, for CPU, use: FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

#RUN apt-get update
RUN apt-get update
RUN apt-get install -y build-essential wget git python3-pip

COPY requirements.txt .
RUN pip3 install -r requirements.txt

CMD ["/usr/bin/env", "bash", "-i"]
