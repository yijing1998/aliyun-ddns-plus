import argparse
import configparser
import os
import systools
import json

# Parse ini file
# Get Access-key and Secret and other settings
parser = argparse.ArgumentParser(description='Setup DDNS for aliyun')
parser.add_argument('-c', default='/etc/aliyunddns.conf', help='Where stores your configuration')
args = parser.parse_args()

if not os.path.exists(args.c):
    print(args.c + ' doesn\'t exist')
    print('Setup a config file at /etc/aliyunddns.conf or -c /your/path')
    quit(2)

config = configparser.ConfigParser()
try:
    config.read(args.c)
except:
    print('Config file Must be a VALID ini file!')
    quit(2)

access_key_id = ''
access_key_secret = ''
subdomain = ''
ifname = ''
addtype = ''
try:
    access_key_id = config['aliyun_ram']['access_key_id']
    access_key_secret = config['aliyun_ram']['access_key_secret']
    subdomain = config['ddns']['subdomain']
    ifname = config['ddns']['ifname']
    addtype = config['ddns']['addtype']
except Exception as e:
    print('INI file parsing error!')
    print(e)
    quit(2)

# get ip address
ipaddress = systools.get_if_addr(ifname, addtype)

# only for test
#ipaddress = '192.168.191.196'

if ipaddress is None:
    print('Can not get a valid ip address!')
    quit(2)

# aliyun sdk
# get subdomain information
client = systools.aliyun_get_client(access_key_id, access_key_secret)
retinfo = systools.aliyun_get_subdomain(client, subdomain)
if retinfo is None:
    print('Can not get subdomain info! Quit!')
    quit(2)

# create a subdomain
if retinfo['TotalCount'] == 0: 
    retinfo = systools.aliyun_add_subdomain(client, subdomain, ipaddress, addtype)
    if retinfo is None:
        print('Can not create a subdomain!')
        quit(2)
    quit(0)

# ip address does not change
if ipaddress == retinfo['DomainRecords']['Record'][0]['Value']:
    quit(0)

# update a subdomain
retinfo = systools.aliyun_update_subdomain(client, subdomain, ipaddress, addtype, retinfo['DomainRecords']['Record'][0]['RecordId'])
if retinfo is None:
    print('Can not update a subdomain!')
    quit(2)