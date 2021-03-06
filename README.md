# Art Display on small raspberry pi screens

Google screen scrape to any number of small raspberrypi terminals and LCD displays from random word lookup.
The devices have one master and N-1 slaves. The master can also do display and LCD text.
To make a device a master, put a jumper on pin closest to the USB terminals. This code all programmed to work ona Rasp 2-B++.

This installation guide assumes you have:
* a wifi router connected to the outside word with DHCP for local wifi devices
* a regular hdmi screen
* an extra usb keyboard and mouse
* some sort of pc/mac/linux that has a terminal window and ssh called *local machine* from now on

**NOTE: once you done one install then here is the way to clone the others (MAC):**
* `diskutil list`
* *assuming here that disk4 is the src and disk5 is the dest
* `sudo diskutil unmountDisk /dev/disk4`
* `sudo diskutil unmountDisk /dev/disk5`
* `sudo dd if=/dev/rdisk4 of=/dev/rdisk5 bs=1m`
* *Put r in front of disk to make it faster*
* `diskutil eject /dev/disk4`
* `diskutil eject /dev/disk5`

#### Installation guide
Here is the current hardware used:
* http://www.newhavendisplay.com/specs/NHD-0216K3Z-FL-GBW-V3.pdf
* http://www.amazon.com/Raspberry-Pi-Model-Project-Board/dp/B00T2U7R7I?ie=UTF8&psc=1&redirect=true&ref_=oh_aui_detailpage_o02_s00
* http://www.amazon.com/Edimax-EW-7811Un-150Mbps-Raspberry-Supports/dp/B003MTTJOY?ie=UTF8&psc=1&redirect=true&ref_=oh_aui_detailpage_o02_s00
* http://www.amazon.com/Resistive-interface-compatible-Raspberry-Pi/dp/B00U21UA16?ie=UTF8&psc=1&redirect=true&ref_=oh_aui_detailpage_o02_s00
* http://www.amazon.com/Kingston-Digital-microSDHC-SDC4-16GBET/dp/B00DYQYLQQ?ie=UTF8&psc=1&redirect=true&ref_=oh_aui_detailpage_o00_s00

#### Boot steps
* Make NOOBS boot sd card
* insert wifi dongle (not needed for pi3s)
* do the NOOBS startup with plugged into the ethernet. It speeds up the
* upgrade process a lot
* ssh is no longer enabled, you must enable it
* start a terminal window
* `sudo raspi-config`
* get the ip addr `hostname -I`
* `ssh pi@<ip_addr>`
* Do first NOOBS/setup boot with USB keyboard/Mouse and standard HDMI terminal
* disable power management to stop wifi from constantly disconnecting
* `sudo vi /etc/modprobe.d/8192cu.conf`
* add the line `options 8192cu rtw_power_mgnt=0 rtw_enusbss=0`
* reboot
* connect to the wifi using the screen icon on the right corner, use right button to enter passcode
* on terminal window 
* using that address verify the you can log into the pi from devel machine with `ssh pi@<ip_addr>` 
* password is raspberry
* raspberry pi now complains about raspberry password, set it to the router password

#### set up network keys

* start ssh session on the pi from *local machine*
  * `ssh pi@<ip_addr>`
  * `sudo dpkg-reconfigure tzdata`
  * `mkdir .ssh`
  * `cd !$`
  * `vi authorized_keys`
* on *local machine*
  * (if you don't have a key type `ssh-keygen` and hit return when asked for passwords) 
  * `vi ~/.ssh/id_rsa.pub`
  * copy and paste key from devel vi window into ssh session vi authorized_keys window
* in ssh session
  * verify that ssh pi@ip no longer needs a password
    * `exit`
    * `ssh pi@<ip_addr>`
* on *local machine*
  * `vi ~/.ssh/config`
  * add lines change host and alias to whatever:
    * `Host wipi3`
    * `HostKeyAlias wipi3`
    * `HostName 192.168.1.117`
    * `ForwardX11 yes`
    * `ForwardX11Trusted yes`
    * `Port 22`
  * verify that `ssh wipi3` now works
#### move to small screen
* configure small screen (hdmi_drive=1 has been added here to remove purple line on left side of screen which
* began to appear on versions after 3/01/2017)
  * `sudo vi /boot/config.txt`
  * add lines
     * `hdmi_force_hotplug=1`
     * `hdmi_group=2`
     * `hdmi_mode=1`
     * `hdmi_drive=1`
     * `hdmi_mode=87`
     * `hdmi_cvt 800 480 60 6 0 0 0`
* if using large screen then
  * add lines 
    * `hdmi_force_hotplug=1`
    * `hdmi_group=2`
    * `hdmi_mode=1`
    * `hdmi_drive=1`
    * `hdmi_mode=82`
* if the HDMI screen does not fill out to the edges then
* uncomment this line
  * disable_overscan=1
    
    
* turn off screen blanking
 * vi /home/pi/.config/lxsession/LXDE-pi/autostart 
 * add lines
   * @xset s noblank
   * @xset s off 
   * @xset -dpms
 * `sudo vi /etc/kbd/config` 
 * set `BLANK_TIME=0`
 * set `POWERDOWN_TIME=0`
 * Load screensaver program (see below) disable in perferences
 * 
* power off
  * `sudo poweroff`
  * wait for green blinky light to turn off
  * unplug hdmi screen and attach small screen. Remove keyboard/mouse
* power up and verify that screen configures correctly

#### installing software
* do a full software update
 * `sudo apt-get -y install python-pip`
 * `sudo apt-get -y install python-setuptools`
 * `sudo apt-get update`
 * `sudo apt-get -y upgrade`
 * `mkdir GitProjects`
 * `cd !$`
 * `ssh-keygen`
 * `vi ~/.ssh/id_rsa.pub`
 * copy the ~/.ssh/id_rsa.pub to github
 * `git clone git@github.com:sibosop/artDisplay.git`
 * `cd artDisplay`
 * `git config --global user.email "brian@eastshore.com"`
 * `git config --global user.name "brian reinbolt"`
 * `./packageSetup.sh`
 * If you want the speech recog stuff
 * `./speakSetup.sh`
 
#### setting up unit for run
 * To minimize the writes to the sd card, the image directories are being mounted tmpfs:
 * `sudo mv /etc/fstab /etc/fstab.old`
 * `sudo cp /home/pi/GitProjects/artDisplay/fstab /etc/fstab`
 * check the log file daily since the directory is now smaller, change weekly to daily
 * `sudo vi /etc/logrotate.conf`
 * the master needs the jumper mentioned above
 * also the a master ssh key needs to be generated and put in the authorized keys files of the slaves (see above)
 * ssh from master to slave once to get the host configuration set up
 * to start at boot
  * `crontab -e`
  * add these lines
   * `MAILTO=""`
   * `@reboot sleep 60; /home/pi/GitProjects/artDisplay/imageLookup/adWrap.sh`
 * with any luck the system will start after reboot
 * unclutter removes cursor. You may need to run unclutter -display :0.0 once
 * if the subnet is not 10 then put `export SUBNET=N` in the .bashrc
 * if the subnet is not 10 then put `export SUBNET=N` in adWrap.sh for boot 
 
#### some setup for doing development on the pi
 * copy the .vimrc from the local host to the pi
 * `cd /usr/bin`
 * `sudo mv vi vi.save`
 * `sudo ln -s vim vi`
 
####  wifi router useful into
 * `nmap -sP 192.168.10.1/24`  (or whatever subnet you care about) 
 * use screen to connect to wifi
 * `sudo vi /etc/wpa_supplicant/wpa_supplicant.conf`  is where wifi info is store. remove old wifi info, add new etc
 * `slptool findsrvs service:artdisplay.x` will give you addresses of all connected devices
 * To get rid of the 'known host problems' figure out the router ip and add these lines to ~/.ssh/config
  * LogLevel=QUIET
  * Host 192.168.10.*
  * StrictHostKeyChecking no
  * UserKnownHostsFile=/dev/null
  * LogLevel=QUIET
  
#### Schlub Info
 * `crontab -e`
 * add these lines
  * `MAILTO=""`
  * `@reboot /home/pi/GitProjects/artDisplay/shared/asoundConfig.py`
  * `@reboot sleep 60; /home/pi/GitProjects/artDisplay/schlub/schlubWrap.sh`

#### Schlub - making the addresses for a pi static:
  * sudo vi /etc/dhcpcd.conf
  * addlines:
    * interface wlan0
    *   static ip_address=192.168.20.XXX/24
    *  static routers=192.168.20.1
    *  static domain_name_servers=192.168.20.1


#### AssAi Project

# AssAi
#### Speech Recog info
 * https://cloud.google.com/sdk/downloads#apt-get
 * https://cloud.google.com/speech/docs/reference/libraries#client-libraries-install-python
 * have attempted to put necessary commands in packageSetup.py

#### Google assistant
starting here: https://developers.google.com/assistant/sdk/prototype/getting-started-pi-python/

Setting up usb speakers/mic has the unfortunate feature of assigning usb 'cards' at random during bootup. This will need to be fixed automagically but until that happens:
* `cat /proc/asound/cards`
This will list the 'cards'. This is assuming you are using the adafruint usb mic/speakers recommended by google
* USB-Audio - USB PnP Sound Device - microphone card
* USB-Audio - USB2.0 Device - speaker card
Once you have the card numbers you edit this file:
* `cp ~/GitProjects/AssAi/asoundrc.template ~/.asoundrc`
* `vi ~/.asoundrc`
Change the `pcm: hw:<cardno>,1` to have the proper numbers for the mic and speaker.

Linux uses ALSA for its audio:
* speaker-test 
  * `speaker-test -c2`
* arecord
  * `arecord --format=S16_LE --duration=5 --rate=16k --file-type=raw out.raw`
* aplay
  * `aplay --format=S16_LE --rate=16k out.raw`
* alsamixer (gui) or amixer (command line)
  * amixer -c 2 cset numid=3,name='PCM Playback Volume' 100
* aplay --format=S16_LE --rate=44100  audio3.raw
