#!/bin/bash
env=$(pwd)
cfg=$env'/config.txt'
cronpath='/var/spool/cron/crontabs/root'
mm=30
hh=9
dmw='* * *'
read -p '设置自动执行时间([回车]默认9:30):' time
hhmm=(`echo $time | tr ':' ' '`)
hmlen=${#hhmm[@]}
if [ $hmlen -eq 2 ];then
  mm=${hhmm[1]}
  hh=${hhmm[0]}
fi

if [ -f "$cfg"  ]&& [ $(cat $cfg |wc -l) -gt 13 ];then
  setcron="$mm $hh $dmw"	
  cmd='python3 '$env'/main.py'
  echo "$setcron $cmd" > $cronpath
else
  bash $env'/input.sh'
fi


