#!/bin/bash
env=$(pwd)
cfg=$env'/config.txt'
#cronpath='/var/spool/cron/crontabs/root'
mm=30
hh=9
dmw='* * *'
read -p '请设置每天自动执行时间([回车]默认9:30):' time
hhmm=(`echo $time | tr ':' ' '`)
hmlen=${#hhmm[@]}
if [ $hmlen -eq 2 ];then
  mm=${hhmm[1]}
  hh=${hhmm[0]}
fi


setcron="$mm $hh $dmw"	
cmd=$(which python3)' '$env'/main.py'' >>'$env'/run.log'
if [ -f "$cfg"  ]&& [ $(cat $cfg |wc -l) -gt 13 ];then
  echo "$setcron $cmd" | crontab -
else
  bash $env'/input.sh'
  echo "$setcron $cmd" | crontab -
fi

echo -e "设置成功！\n"
