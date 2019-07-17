FROM nvidia/cuda:10.0-cudnn7-runtime

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y build-essential wget git python3-pip apache2 apache2-utils ssl-cert libapache2-mod-wsgi-py3 supervisor redis-server 

COPY requirements.txt ~/
COPY start.sh ~/
WORKDIR ~/
RUN pip3 install -r requirements.txt

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

#CMD ["/usr/bin/supervisord"]
#CMD ["/usr/bin/env", "bash", "-i"]
WORKDIR /app
ENTRYPOINT  supervisord -c /etc/supervisor/conf.d/supervisord.conf -n
