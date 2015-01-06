#!/bin/bash

if [ "$1" == 'build' ]; then 
    sudo docker build -t word-agent:latest /vagrant;
elif [ "$1" == 'run' ]; then 
    sudo docker run -tip 5000:8880 -v ~/vagrant:/code --rm --name wa_instance word-agent $2;
else 
    echo "Usage: scripts.sh build OR scripts.sh run CMD";
fi
