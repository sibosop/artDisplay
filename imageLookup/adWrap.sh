#!/bin/bash 

while [ 1 ]; do
  ~/GitProjects/artDisplay/imageLookup/artDisplay.py
  pkill feh
  sleep 5 
done
