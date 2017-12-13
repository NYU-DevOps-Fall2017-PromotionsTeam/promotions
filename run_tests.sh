#! /bin/bash

nosetests &&
python3 run.py &
sleep 5
behave && 
kill $(ps aux | grep 'python3 run.py' | grep -v grep | awk '{print $2}')
