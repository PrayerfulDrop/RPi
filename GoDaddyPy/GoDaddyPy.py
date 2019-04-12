### BEGIN INIT INFO
# Provides:          godaddy
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon at boot time
# Description:       Enable service provided by daemon.
### END INIT INFO

#!/usr/bin/env python3

# User configuration
godaddy_api_key = '<YOUR-GODADDY-PROD-KEY>'  # http://developer.godaddy.com
godaddy_api_secret = '<YOUR-GODADDY-PROD-SECRET>'
webdomains = "domain1.com,domain2.com" # multiple domains separate by just a comma
get_ip_wait_sec = 10     # in seconds
update_interval_sec = 60 # in seconds
logging = "false"


# Don't modify anything below here
import os
import sys
import traceback
import time
import pif
import godaddypy
import ipaddress
import argparse
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(name)s - %(message)s', level=logging.INFO)
if logging=="true":
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)
	logging.debug('Debug Logging Enabled')

# Disable Unverified HTTPS request warning from pif
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Required ENV

godaddy_domains = webdomains.split(',')

# Optional ENV
godaddy_a_names = os.environ.get('GODADDY_A_NAMES', '@').split(',')



# Create the godaddypy client using the provided keys
g_client = godaddypy.Client(godaddypy.Account(api_key=godaddy_api_key, api_secret=godaddy_api_secret))

def update_godaddy_records(ip):

    successful = True
    for domain in godaddy_domains:
        for a_name in godaddy_a_names:

            logging.debug('Getting A records with {} for {}'.format(a_name, domain))
            records = g_client.get_records(domain, name=a_name, record_type='A')
            if not records:
                logging.warning('No record {} for {} found'.format(a_name, domain))
                successful = False
                # TODO add the record if configured to do so
                continue

            for record in records:
                if ip == record['data']:
                    logging.debug('Record {} for {} is still {}, no update required'.format(a_name, domain, ip))
                    continue

                result = g_client.update_record_ip(ip, domain, name=a_name, record_type='A')
                if result is not True:
                    logging.error('Failed to update {} for {} to {}'.format(a_name, domain, ip))
                    successful = False
                    continue

                logging.info('Updated {} for {} to {}'.format(a_name, domain, ip))

    return successful

def loop_forever():

    public_ip_cache = False

    # Loop forever
    while True:

        # Go get our current public IP address
        new_ip = False
        while not new_ip:
            try:
                pub_ip = pif.get_public_ip()
                # Check for valid ip
                try:
                    ipaddress.ip_address(pub_ip)
                    new_ip = pub_ip
                except:
                    logging.error('Got an invalid ip address')
                    logging.debug('ip address {}'.format(pub_ip), exc_info=True)
            except:
                logging.exception('Got exception getting public IP')

            # Done if we got one
            if new_ip:
                break

            time.sleep(get_ip_wait_sec)

        # If we got the same IP address, we will try again later
        if public_ip_cache != new_ip:
            # Update the records at godaddy
            try:
                worked = update_godaddy_records(new_ip)
                if worked:
                    #cache so we dont try again if everything went good
                    logging.info('new-ip: {}, old-ip: {}'.format(new_ip, public_ip_cache))
                    public_ip_cache = new_ip
            except:
                logging.exception('Got exception updating godaddy records')

        time.sleep(update_interval_sec)

loop_forever()

