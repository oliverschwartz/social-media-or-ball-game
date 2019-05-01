import os, re, requests

site = "https://www.instagram.com/"
args = "/?__a=1"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
			'cookie': 'mid=XL27yAAEAAFpy_Ef18muu5LVrHXY; fbm_124024574287414=base_domain=.instagram.com; rur=PRN; shbid=16035; shbts=1556579945.4759493; fbsr_124024574287414=qo8jVBmmioQlrGdBhVkvIlVDwi2W7E_N_kD0Q6feH38.eyJjb2RlIjoiQVFCdG45UkU1dlNQd0tQUmdtLWhsOE9RR3VKcWh0MFR3U0ZzV2M5VVdES1pCYVpaMlVuRXZ4ZmdYMklGaGZzamh6a1pJU3JWRTVFRXdQNmxYNkd6SHI0VjFya21Uck54dWF5RUkzU1NzX2t0TWlXZ0pJd1p5MEh1QWJpWFZQTVpOWWF2ZmxPRmg5ekMzWHhNU1ktTGNWbmpBdV85Z1BKTXI0MUFlVUFHVGVZa2doa3pQaW9SQThZeVpYeDFFdTFOd2xGR0hISnVxeFpBLTlkRnBWbnBZb3M2OFVWeElzUjB2dmRIRnBqeFRJZGRNdUJaaWVSSTR1OGt0T0x1VVkzandyWmdPenFMX1F5cTAyVkM4SnphTmU4ckFPNVRIaWhZQVQwTkdnYXlEdkFISV9jdV8xX3dwUURqNl83UC1QMHVHZi1keXZSQnkwaDhSRS1fRi1faXZHNDYiLCJ1c2VyX2lkIjoiMTAwMDAyMTM3Mjk0NTI3IiwiYWxnb3JpdGhtIjoiSE1BQy1TSEEyNTYiLCJpc3N1ZWRfYXQiOjE1NTY2MzI0MDd9; csrftoken=8eR8ICWmjULaVTk136TSQJJmscdLoUqD; ds_user_id=8322932967; sessionid=8322932967%3ADXdPBvzTJaX5ds%3A1; urlgen="{\"66.180.182.20\": 88\054 \"66.180.181.145\": 88\054 \"66.180.183.108\": 88\054 \"66.180.182.98\": 88}:1hLTWY:3MMjeLEBTuuG2VRaocGUfUIJXrQ"'
} # may need to change cookie every time this script is run 
  # use Chrome dev tools to do this

with open("counts.csv", 'w') as f:
    os.chdir("../..")
    for file in os.listdir("."):
        if file[-4:] == ".csv":
            username = file[:-4]
            print("looking at %s's follower count..." % username)
            url = site + username + args
            response = str(requests.get(url, headers=headers).content)
            search = re.findall("edge_followed_by\":{\"count\":[0-9]+}", response)
            count = re.findall("[0-9]+", search[0])
            f.write("%s,%s\n" % (username, count[0]))



