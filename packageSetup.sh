#!/bin/bash
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
sudo easy_install --upgrade pip
sudo -H pip install requests==2.6.0
export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)"
echo "deb http://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo apt-get update && sudo apt-get install google-cloud-sdk google-cloud-sdk-app-engine-python
sudo pip install --upgrade google-cloud-speech
gcloud init
gcloud auth application-default login
sudo apt-get install libasound2-dev
