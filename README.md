# aliyun-ddns-plus
## Introduction
A python application to setup ddns using aliyun service.
## Target Users
* People who own at least one domain hosted on aliyun.
* Have some device and need a dns but can't obtain a static internet ip address.
* The device must have enough resource to run linux and python
* Do not want to use the dns provided by public ddns service
* Just be curious
## Installation
* python3, pip
* aliyun python sdk (pip install ...)
   * aliyun-python-sdk-core-v3
   * aliyun-python-sdk-alidns
   * **Notice:** 
   Some devices don't have enough resource to run `pip install`, you can install the sdk on a PC first, then copy the module files to the device.
* Copy all my files into a folder, create a config file named *aliyunddns.conf*
   ```
   [aliyun_ram]
   access_key_id = your access key id
   access_key_secret = your access key secret

   [ddns]
   subdomain = your.own.dns
   ifname = ip address show can be run on your device
   addtype = ipv4 (or ipv6)
   ```
## Usage
`python3 aliyunddns.py -c /path/to/aliyunddns.conf`

`python3 aliyunddns.py` (copy aliyunddns.conf to /etc/)
## Openwrt Usecase
* Device info
* Install python3 environment
* Config cron service