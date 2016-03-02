#!/bin/bash

# Prefer ipv4 for updates, since ipv6 servers are slow
sudo sed -i '/precedence ::ffff:0:0\/96  100/s@^#@@g' /etc/gai.conf
sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get -yf install git python3 python3-pip
sudo apt-get -yf install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev
sudo apt-get -yf install liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk
sudo ln -s /usr/lib/i386-linux-gnu/libjpeg.so /usr/lib/
sudo ln -s /usr/lib/i386-linux-gnu/libfreetype.so.6 /usr/lib/
sudo ln -s /usr/lib/i386-linux-gnu/libz.so /usr/lib/
sudo pip3 install -r /vagrant/requirements.txt