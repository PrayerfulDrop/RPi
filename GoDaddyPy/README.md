<H1>GoDaddyPy DDNS Script for RPi</h1>

Save GoDaddyPy.py to an executable location - this is <YOUR PATH TO THIS SCRIPT AND FILENAME>

Edit GoDaddyPy.py and replace User configuration fields with your information

Acquire GoDaddy Production API keys from http://developer.godaddy.com

This script uses the following Python3 add-ons for RPi:<br>
 sudo pip3 install godaddypy<br>
 sudo pip3 install traceback<br>
 sudo pip3 install ipaddress<br>
 sudo pip3 install argparse<br>

Init.d installation:<br>
 sudo nano /lib/systemd/system/godaddypy.service<br>
 Add the following and modify "<YOUR PATH TO THIS SCRIPT - RECOMMEND /HOME/PI/GODADDY.PY>"<br>
 
 [Unit]<br>
 Description=GoDaddyPy Service<br>
 After=multi-user.target<br>
 
 [Service]<br>
 Type=idle<br>
 ExecStart=/usr/bin/python <YOUR PATH TO THIS SCRIPT - RECOMMEND /HOME/PI/GODADDY.PY><br>
 
 [Install]<br>
 WantedBy=multi-user.target<br>

Setup Logging:
 ExecStart=/usr/bin/python (YOUR PATH AND SCRIPT NAME) > (YOUR PATH AND SERIVICE NAME).log 2>&1<br>
 sudo chmod 644 /lib/systemd/system/godaddypy.service<br>

Install Service:
 sudo systemctl daemon-reload<br>
 sudo systemctl enable godaddypy.service<br>
 sudo reboot<br>

Test Service:<br>
 sudo journalctl godaddypy.service<br>
