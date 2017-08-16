#!/bin/bash

while true; do
  /home/pi/GitProjects/artDisplay/schlub/schlub.py
  rc=$?
  case $rc in
    3) logger doing poweroff; sudo poweroff
    ;;
    4) logger doing reboot; sudo reboot
    ;;
    5) logger doing stop; exit 0
    ;;
    *)
    ;;
  esac
done
