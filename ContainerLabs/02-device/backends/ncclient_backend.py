from ncclient import manager



R1 = {
    "host": "172.20.20.5",
    "port": 830,
    "username": "admin",
    "password": "admin",
    "hostkey_verify": False
}

R2 = {
    "host": "172.20.20.4",
    "port": 830,
    "username": "admin",
    "password": "admin",
    "hostkey_verify": False,
    "device_params": {"name": "iosxe"}
}

R3 = {
    "host": "172.20.20.2",
    "port": 830,
    "username": "admin",
    "password": "admin",
    "hostkey_verify": False,
    "device_params": {"name": "iosxe"}
}

filter = """
<native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface/>
</native>
"""


def get_capabilities():
    with manager.connect(**R1) as m:
        try:
            for cap in m.server_capabilities:
                print (f" - {cap}")
        except Exception as E:
            print(f"Error: {E}")

def show_schema():
    with manager.connect(**R1) as m:
        try:
            schema = m.get_schema("cisco-xe-ietf-ospf-deviation")
            print(schema)
        except Exception as E:
            print(f"Error {E}")

def get_intf_conf():
    with manager.connect(**R1) as m:
        try:
            request = m.get_config(source="running",filter=("subtree", filter))
            print(request)
        except Exception as E:
            print(f"Error: {E}")

#get_capabilities()

#show_schema()

get_intf_conf()