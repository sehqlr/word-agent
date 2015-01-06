#!/usr/bin/env bash
sudo docker rmi word-agent
sudo docker build --force-rm -t word-agent:latest .
