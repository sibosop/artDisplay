#!/bin/bash
cd ~/GitProjects/artDisplay
./fixSwap.sh
sudo apt-get -y install python-pip
sudo -H pip install --upgrade pip
sudo apt-get -y install python-setuptools
sudo -H pip install beautifulsoup4
sudo -H pip install nmap
sudo apt-get -y install gcc python-dev
sudo -H pip install psutil
sudo apt-get -y install slpd
sudo service slpd stop
sudo update-rc.d -f slpd remove
sudo apt-get -y install openslp-doc
sudo apt-get -y install slptool
sudo apt-get -y install feh
sudo -H pip install --upgrade pyserial
sudo -H pip install py-bing-search
sudo -H pip install --upgrade google-api-python-client
sudo -H pip install schedule
sudo apt-get -y install xscreensaver
sudo apt-get -y install unclutter
sudo apt-get -y install vim
sudo apt-get -y install python-pygame
sudo -H pip install gTTS
sudo -H pip install pydub
sudo apt-get -y install libav-tools
sudo apt-get -y install espeak
sudo apt-get -y install python-pypdf2
sudo pip3 install pyalsaaudio
sudo apt-get -y install python-pyaudio
sudo -H pip install textblob

