#!/bin/bash

isPythonInstalled=$(python3 --version)
willWatch=0

if [ ! "$isPythonInstalled" ]; then
    
    echo "Python3 nao instalado! Instalar? (y/n)"
    read installPython
    if [ "$installPython" = "y" ]; then
        sudo apt update
        sudo apt install python3 -y
        sudo apt install python3-pip -y
        sudo pip3 install requests -y
        sudo pip3 install browser_cookie3 -y
        willWatch=1
    fi
else
    willWatch=1
fi

if [ $willWatch = 1 ]; then
    watch --color --no-title --interval 5 python3 hookwatcher.py
fi