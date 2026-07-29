import requests
import json


url = "https://sandboxapicdc.cisco.com/api/v1/fv.json"
r = requests.get(url, verify=False)
#print(r.json())
print(r.headers["Content-Security-Policy"])
"""if r.status_code == 200:
    response = r.json()
    #clean_entry = response[0]['type']
    print(response)
"""
#admin
#!v3G@!4@Yprint(type(response))         