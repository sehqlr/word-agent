# Dockerfile for WordAgent
FROM python:latest
MAINTAINER sehqlr

# install requirements and set up RC for python shell
RUN apt-get update && apt-get install -y \
        build-essential \
        curl \
        dialog \
        git \
        net-tools \
        python-dev \
        tar \
        vim \
        wget

RUN wget http://download.redis.io/redis-stable.tar.gz && \
        tar xvzf redis-stable.tar.gz && \
        cd redis-stable && \
        make && make install

ADD . /code
RUN pip install -r /code/requirements.txt
ENV PYTHONSTARTUP /code/pythonrc
EXPOSE 80
WORKDIR /code
CMD python server.py
