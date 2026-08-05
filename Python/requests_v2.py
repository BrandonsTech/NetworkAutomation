import requests
import json
#import xmltodict

URL = "https://sandboxapicdc.cisco.com"

"""
admin
!v3G@!4@Y
"""
WEATHER_URL = "https://api.weather.gov"

def get_function(BASE=WEATHER_URL, TIMEOUT=5):
    with requests.Session() as R:
        #results = {}
        R.headers.update({"Accept": "application/json"})
        try:
            response = R.get(f"{BASE}/alerts/active/count", timeout=TIMEOUT)
            results = response.json()
        except requests.HTTPError:
            print("HTTP Error")
    return results


def post_function():
    pass

def put_function():
    pass

def delete_function():
    pass

data = get_function()
print("PA Alerts:",(data["areas"]["PA"]))