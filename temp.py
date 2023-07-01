import requests

url = "https://flagopen.baai.ac.cn/flagStudio/auth/getToken"

querystring = {"apikey":"709cb5be6774dbf53d634423ad7b7297"}

headers = {"Accept": "application/json"}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)