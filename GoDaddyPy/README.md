<H1>GoDaddyPy DDNS Script for RPi</h1>

Save GoDaddyPy.py to an executable location - this is <YOUR PATH TO THIS SCRIPT AND FILENAME>

Edit GoDaddyPy.py and replace User configuration fields with your information

Acquire GoDaddy Production API keys from http://developer.godaddy.com

This script uses the following Python3 add-ons for RPi:
 sudo pip3 install godaddypy
 sudo pip3 install traceback
 sudo pip3 install ipaddress
 sudo pip3 install argparse

Init.d installation:
 sudo nano /lib/systemd/system/godaddypy.service
 Add the following and modify "<YOUR PATH TO THIS SCRIPT - RECOMMEND /HOME/PI/GODADDY.PY>"
 
 [Unit]
 Description=My Script Service
 After=multi-user.target
 
 [Service]
 Type=idle
 ExecStart=/usr/bin/python <YOUR PATH TO THIS SCRIPT - RECOMMEND /HOME/PI/GODADDY.PY>
 
 [Install]
 WantedBy=multi-user.target

 ExecStart=/usr/bin/python <YOUR PATH AND SCRIPT NAME> > <YOUR PATH AND SERIVICE NAME>.log 2>&1
 sudo chmod 644 /lib/systemd/system/godaddypy.service
 sudo systemctl daemon-reload
 sudo systemctl enable godaddypy.service
 sudo reboot

Test Service:
 sudo journalctl godaddypy.service
