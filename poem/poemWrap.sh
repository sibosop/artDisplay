#!/bin/bash 
export DISPLAY=:0.0
while [ 1 ]; do
  /home/pi/GitProjects/artDisplay/poem/poem.py
  rc=$?
  echo rc = $rc
  if [ $rc -eq 2 ]
  then
    sudo poweroff
  fi
  sleep 1 
done
