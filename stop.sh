#!/bin/bash

# 查找匹配的进程并杀死它
ps aux | grep "python3 -u main.py" | grep -v grep | awk '{print $2}' | xargs kill -9

sleep 1s

nohup python3 -u main.py >log/python.log 2>&1 &

