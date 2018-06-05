#!/bin/bash
cd ~/GitProjects/artDisplay
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
