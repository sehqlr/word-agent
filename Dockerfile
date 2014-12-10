# Dockerfile for WordAgent
FROM python
MAINTAINER sehqlr

# install requirements and set up RC for python shell
RUN apt-get update && apt-get install -y python-dev git vim
ADD . /code
RUN pip install -r /code/requirements.txt
ENV PYTHONSTARTUP /code/scripts/pythonrc

