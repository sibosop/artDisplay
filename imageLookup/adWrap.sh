#!/bin/bash 

export DISPLAY=:0.0
export SUBNET=10
while [ 1 ]; do
  ~/GitProjects/artDisplay/imageLookup/artDisplay.py
  pkill feh
  sleep 1 
done
