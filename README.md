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
* http://www.amazon.com/Raspberry-Pi-Model-Project-Board/dp/B00T2U7R7I?ie=UTF8&psc=1&redirect=true&ref_=oh_aui_detailpage_o02_s00
* http://www.amazon.com/Edimax-EW-7811Un-150Mbps-Raspberry-Supports/dp/B003MTTJOY?ie=UTF8&psc=1&redirect=true&ref_=oh_aui_detailpage_o02_s00
* http://www.amazon.com/Resistive-interface-compatible-Raspberry-Pi/dp/B00U21UA16?ie=UTF8&psc=1&redirect=true&ref_=oh_aui_detailpage_o02_s00
* http://www.amazon.com/Kingston-Digital-microSDHC-SDC4-16GBET/dp/B00DYQYLQQ?ie=UTF8&psc=1&redirect=true&ref_=oh_aui_detailpage_o00_s00

#### Boot steps
* Make NOOBS boot sd card
* insert wifi dongle
* Do first NOOBS/setup boot with USB keyboard/Mouse and standard HDMI terminal
* disable power management to stop wifi from constantly disconnecting
  * start a terminal window
  * `sudo vi /etc/modprobe.d/8192cu.conf`
  * add the line `options 8192cu rtw_power_mgnt=0 rtw_enusbss=0`
  * reboot
* connect to the wifi using the screen icon on the right corner, use right button to enter passcode
* on terminal window get the ip addr `hostname -I`
* using that address verify the you can log into the pi from devel machine with `ssh pi@<ip_addr>` 
* password is raspberry

#### set up network keys
* start ssh session on the pi from *local machine*
  * `ssh pi@<ip_addr>`
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
* configure small screen
  * `sudo vi /boot/config.txt`
  * add lines
    * `hdmi_force_hotplug=1`
    * `hdmi_group=2`
    * `hdmi_mode=1`
    * `hdmi_mode=87`
    * `hdmi_cvt 800 480 60 6 0 0 0`
* turn off screen blanking
 * `sudo vi /etc/kbd/config` 
 * set `BLANK_TIME=0`
 * set `POWERDOWN_TIME=0`
 * 
* power off
  * `sudo poweroff`
  * wait for green blinky light to turn off
  * unplug hdmi screen and attach small screen. Remove keyboard/mouse
* power up and verify that screen configures correctly

#### installing software
* do a full software update
 * `sudo apt-get update`
 * `sudo apt-get upgrade`
 * `mkdir GitProjects`
 * `cd !$`
 * `git clone git@github.com:sibosop/artDisplay.git`
 * `sudo pip install beautifulsoup4`
 * `sudo apt-get install gcc python-dev`
 * `sudo pip install psutil`
 * `sudo apt-get install slpd`
 * `sudo service slpd stop`
 * `sudo update-rc.d -f slpd remove`
 * `sudo apt-get install openslp-doc`
 * `sudo apt-get install slptool`
 * `sudo apt-get install feh`
 * `sudo pip install --upgrade pyserial`
 * `sudo -H pip install py-bing-search`
 * `sudo -H pip install --upgrade google-api-python-client`
 
#### seting up unit for run
 * the master needs the jumper mentioned above
 * also the a master ssh key needs to be generated and put in the authorized keys files of the slaves (see above)
 * ssh from master to slave once to get the host configuration set up
 * to start at boot
  * `crontab -e`
  * add these lines
   * MAILTO=""
   * @reboot sleep 60; /home/pi/GitProjects/artDisplay/imageLookup/setup.py
 * with any luck the system will start after reboot





