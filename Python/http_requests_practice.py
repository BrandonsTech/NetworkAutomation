import requests
import json



POST_URL = "https://apichallenges.eviltester.com/sim/entities/10"
POST_DATA = {
  "name": "eris"
}
def post_entity(url=POST_URL, data=POST_DATA, timeout=5):
    results = {}
    with requests.Session() as s:
        s.headers.update({"Accept": "application/json"})
        try: 
            response = s.post(url, data=data)
            results = response.text
        except requests.exceptions.HTTPError:
            print(f"HTTP Status Code Error: {response.status_code}")
        except requests.exceptions.InvalidJSONError:
            print(f"Invalid JSON, {response.status_code}")
        except requests.exceptions.JSONDecodeError:
            print(f"Error Decoding JSON")
    return response

data = post_entity()
print (data)

URL = "https://apichallenges.eviltester.com/sim/entities"

def get_entities(url=URL, timeout=5):
    results = {}
    with requests.Session() as s:
        s.headers.update({"Accept": "application/json"})
        try:
            response = s.get(url, timeout=timeout)
            response.status_code
            results = response.json()
        except requests.exceptions.HTTPError:
            print(f"HTTP Status Code Error: {response.status_code}")
        except requests.exceptions.InvalidJSONError:
            print(f"Invalid JSON, {response.status_code}")
        except requests.exceptions.JSONDecodeError:
            print(f"Error Decoding JSON")
    return results
data = get_entities()
print(data["entities"])
#print(data["entities"][3]["name"])