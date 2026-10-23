import json
import requests
import urllib3
urllib3.disable_warnings()

R1 = {"hostname": "R1",
      "IP": "172.16.200.220",
      }
headers = {"Content-Type": "application/json",
           "Accept": "application/json"}


def GET_REQUEST():
    with requests.session() as R:
        try:
            request = R.get(url="https://api.google.com", headers=headers, verify=False).json()
            pretty = json.dumps(request, indent=2)
            print(pretty)
        except Exception as E:
            print(f"Exception: {E}")

GET_REQUEST()