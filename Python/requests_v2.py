import requests
import json
import yaml

URL = "https://172.16.200.220/api/aaaLogin.json"
BASE_URL = "https://172.16.200.220/api/mo/"

payload = '{"aaaUser":{"attributes":{"name":"admin","pwd":"Dubzdubz#1"}}}'

def auth(BASE=URL, TIMEOUT=5):
    with requests.Session() as R:
        results = {}
        #R.headers.update({"Accept": "application/json"})
        try:
            response = R.post(f"{BASE}", data=payload, timeout=TIMEOUT, verify=False)
            results = response.json()
        except requests.HTTPError:
            print("HTTP Error")
    return results


auth = auth()
#print(json.dumps(auth, indent=2))
#print(auth)
token = auth["imdata"][0]["aaaLogin"]["attributes"]["token"]
cookie = {"APIC-cookie": token}
print (cookie)

def get_tenants():
    result = {}
    with requests.Session() as R:
        try:
            response = R.get(f"{BASE_URL}uni/tn-common.json", cookies=cookie, verify=False)
            response.raise_for_status
            result = response.json()
        except requests.exceptions.ConnectTimeout:
            print("Request Timed Out")
    return result

json_data = get_tenants()
print(json_data)
yaml_data = yaml.dump(json_data)
print(yaml_data)
#print(json.dumps(json_data, indent=2))

with open(r"C:\Cool\GitHub\NetworkAutomation\Python\stuf.yml", "r") as yml:
    python_yaml = yaml.safe_load(yml)
    print("Brandon's Age is",python_yaml['Brandon']["Age"])
    print(python_yaml)