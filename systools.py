import subprocess
import re

def get_if_addr_ipv4(ifname):
    cmdres = subprocess.getstatusoutput('ip address show dev ' + ifname)
    if cmdres[0] == 1:
        return None
    matlist = re.findall(r'inet .*/', cmdres[1])
    if len(matlist) == 0:
        return None
    
    return matlist[0][5:-1]

def get_if_addr_ipv6(ifname):
    cmdres = subprocess.getstatusoutput('ip address show dev ' + ifname)
    if cmdres[0] == 1:
        return None
    matlist = re.findall(r'inet6 .*/', cmdres[1])
    if len(matlist) == 0:
        return None
    
    return matlist[0][6:-1]

def get_if_addr(ifname, addtype):
    if addtype == 'ipv4':
        return get_if_addr_ipv4(ifname)
    elif addtype == 'ipv6':
        return get_if_addr_ipv6(ifname)
    else:
        return None

import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
# setup aliyun client
def aliyun_get_client(ack_id, ack_secret):
    client = AcsClient(ack_id, ack_secret)
    return client

from aliyunsdkalidns.request.v20150109.DescribeSubDomainRecordsRequest import DescribeSubDomainRecordsRequest
# get aliyun subdomain info
def aliyun_get_subdomain(client, subdomain):
    request = None
    response = None
    request = DescribeSubDomainRecordsRequest()
    request.set_SubDomain(subdomain)
    try:
        response = client.do_action_with_exception(request)
    except ServerException as e:
        print('Server Error! Domain: {}, Code: {}.'.format(subdomain, e.get_error_code()))
        print(e.get_error_msg())
        return None
    except ClientException as e:
        print('Client Error! Domain: {}, Code: {}.'.format(subdomain, e.get_error_code()))
        print(e.get_error_msg())
        return None
    return json.loads(str(response, encoding='utf-8'))


from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
# add a new subdomain
def aliyun_add_subdomain(client, subdomain, ipaddress, addtype):
    request = None
    response = None
    request = AddDomainRecordRequest()
    request.set_accept_format('json')

    tmp = subdomain.partition('.')
    request.set_DomainName(tmp[-1])
    request.set_RR(tmp[0])
    if addtype == 'ipv4':
        request.set_Type('A')
    else:
        request.set_Type('AAAA')
    request.set_Value(ipaddress)

    try:
        response = client.do_action_with_exception(request)
    except ServerException as e:
        print('Server Error! Domain: {}, Code: {}.'.format(subdomain, e.get_error_code()))
        print(e.get_error_msg())
        return None
    except ClientException as e:
        print('Client Error! Domain: {}, Code: {}.'.format(subdomain, e.get_error_code()))
        print(e.get_error_msg())
        return None
    return json.loads(str(response, encoding='utf-8'))

from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
# update a subdomain
def aliyun_update_subdomain(client, subdomain, ipaddress, addtype, recordid):
    request = None
    response = None
    request = UpdateDomainRecordRequest()
    request.set_accept_format('json')

    tmp = subdomain.partition('.')
    request.set_RecordId(recordid)
    request.set_RR(tmp[0])
    if addtype == 'ipv4':
        request.set_Type('A')
    else:
        request.set_Type('AAAA')
    request.set_Value(ipaddress)

    try:
        response = client.do_action_with_exception(request)
    except ServerException as e:
        print('Server Error! Domain: {}, Code: {}.'.format(subdomain, e.get_error_code()))
        print(e.get_error_msg())
        return None
    except ClientException as e:
        print('Client Error! Domain: {}, Code: {}.'.format(subdomain, e.get_error_code()))
        print(e.get_error_msg())
        return None
    return json.loads(str(response, encoding='utf-8'))