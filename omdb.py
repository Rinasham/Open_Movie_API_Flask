
import requests
import json
import settings

key = settings.AP


response = requests.get(f'http://www.omdbapi.com/?t=matrix&apikey={key}')
json_response = response.json()
print(json.dumps(json_response, indent = 4))