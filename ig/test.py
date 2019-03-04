import requests

user_id = '11456674820.7a6566a'
access_token = 'ba74199117124be3ae93e755f4d5029e'
url = "https://api.instagram.com/v1/users/kingjames/follows?access_token=" + access_token

r = requests.get(url)
print(r)