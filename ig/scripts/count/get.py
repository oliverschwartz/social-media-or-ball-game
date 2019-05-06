import os, re, requests

site = "https://www.instagram.com/"
args = "/?__a=1"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
			'cookie': 'mid=XL27yAAEAAFpy_Ef18muu5LVrHXY; fbm_124024574287414=base_domain=.instagram.com; rur=PRN; shbid=16035; shbts=1556579945.4759493; csrftoken=O5dIzgfFm6ltH1bLyznBOQQR4ENUy2fU; ds_user_id=11456674820; sessionid=11456674820%3A5izZjRKD5WWm6o%3A25; urlgen="{\"66.180.180.225\": 88\054 \"66.180.183.75\": 88\054 \"66.180.183.128\": 88}:1hNiOG:AoxYutBB_MIf4eZG36BroVuv548"'
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



