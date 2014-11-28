# Dockerfile for WordAgent and NLTK
FROM python
MAINTAINER sehqlr

# Build image, including NLTK
RUN apt-get update \
		&& apt-get install -y python-dev git vim \
		&& pip install numpy matplotlib nltk \ 
		&& python -m nltk.downloader book 

# Get project data, set RC for python shell
RUN git clone https://github.com/sehqlr/word-agent.git /home/word-agent
RUN export PYTHONSTARTUP="home/word-agent/pythonrc"
