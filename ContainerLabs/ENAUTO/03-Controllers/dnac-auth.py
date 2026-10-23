import requests, json, urllib3
urllib3.disable_warnings()

base_url = "https://10.10.20.185/dna/"
auth_url = "system/api/v1/auth/token"

header = {"Content-Type": "application/json",
          "Accept": "application/json"}
creds = ("administrator", "Cisco1234!")

token = requests.post(url=f"{base_url}{auth_url}",headers=header,auth=creds,verify=False).json()["Token"]

def 