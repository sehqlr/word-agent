# Dockerfile for WordAgent and NLTK
FROM python
MAINTAINER sehqlr

# Build image, including NLTK
RUN apt-get update && apt-get install -y python-dev git vim
RUN pip install -r requirements.txt

# Get project data, set RC for python shell
ADD . /code
ENV PYTHONSTARTUP /code/scripts/pythonrc

