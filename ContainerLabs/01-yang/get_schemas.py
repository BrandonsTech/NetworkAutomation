#!/user/bin/env python3

from ncclient import manager
from lxml import etree
import xmltodict

filter = '''
<native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
    </interface>
</native>
'''
payload = '''
<config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
        <GigabitEthernet>
            <name>1</name>
            <description>Containerlab management interface AND changes by netconf</description>
        </GigabitEthernet>
        </interface>
        </native>
</config>
'''
def connect():
    conn = manager.connect(host="172.20.20.3", port=830, username="admin", password="admin", hostkey_verify=False, device_params={'name':'iosxe'})
    return conn


def get_conf():
        schema = connect().get_config(source="running",filter=("subtree", filter))
        print(str(etree.tostring(schema.data, pretty_print=True).decode()))
    
    
def push_config():
    schema = connect().edit_config(config=payload, target="running")
    print(schema)
    #print(str(etree.tostring(schema.data, pretty_print=True).decode()))

push_config()

get_conf()