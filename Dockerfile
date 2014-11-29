# Dockerfile for WordAgent and NLTK
FROM python
MAINTAINER sehqlr

# Build image, including NLTK
RUN apt-get update \
		&& apt-get install -y python-dev git vim \
		&& pip install numpy matplotlib nltk \ 
		&& python -m nltk.downloader book 

# Get project data, set RC for python shell
ADD . /home/word-agent
ENV PYTHONSTARTUP home/word-agent/pythonrc
