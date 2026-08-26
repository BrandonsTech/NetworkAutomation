import requests
import json
import urllib3
urllib3.disable_warnings()

base_url = "https://172.20.20.4/restconf/data/"
native_interface_url = "Cisco-IOS-XE-native:native/interface/GigabitEthernet=1"
ietf_interface_url = "ietf-interfaces:interfaces"
ietf_interface_url_specific = "ietf-interfaces:interfaces/interface=GigabitEthernet1"
openconfig_interface_url = "openconfig-interfaces:interfaces/interface=GigabitEthernet2"
headers = {
    "Content-Type": "application/yang-data+json",
    "Accept": "application/yang-data+json"
}
auth_creds = ("admin", "admin")

def find_root():
    with requests.session() as s:
        try:
            request = s.get(f"{base_url}{openconfig_interface_url}", headers=headers, verify=False, auth=auth_creds).json()
            pretty = json.dumps(request, indent=2)
            print(pretty)
        except Exception as E:
            print(f"Error: {E}")
find_root()