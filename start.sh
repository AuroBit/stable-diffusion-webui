#!/usr/bin/env bash
#################################################
# Please do not make any changes to this file,  #
# change the variables in webui-user.sh instead #
#################################################

service="webui"
pids=$(ps -ef | grep "$service" | grep -v grep | awk '{print $2}')

if [ -n "$pids" ]; then
    for pid in $pids; do
        kill -9 "$pid"
    done
fi

# 查找 7860 端口的进程 ID
pid=$(lsof -t -i:7860)

# 如果找到了进程 ID，则杀死进程
if [ -n "$pid" ]; then
  echo "Killing process $pid"
  kill $pid
else
  echo "No process found on port 7860"
fi

nohup ./webui.sh -f > sd.log 2>&1 &
