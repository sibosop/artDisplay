#!/bin/bash

sudo pip install beautifulsoup4
sudo apt-get install gcc python-dev
sudo pip install psutil
sudo apt-get install slpd
sudo service slpd stop
sudo update-rc.d -f slpd remove
sudo apt-get install openslp-doc
sudo apt-get install slptool
sudo apt-get install feh
sudo pip install --upgrade pyserial
sudo -H pip install py-bing-search
sudo -H pip install --upgrade google-api-python-client
sudo -H pip install schedule
sudo apt-get install xscreensaver
sudo apt-get install unclutter

