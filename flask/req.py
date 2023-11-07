import requests

api_url = "http://api.open-notify.org/astros.json"

resonse = requests.get(api_url)

json_response = resonse.json()

print(json_response)