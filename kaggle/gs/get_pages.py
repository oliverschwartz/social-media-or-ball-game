import urllib3, sys, os
from bs4 import BeautifulSoup

os.chdir('pages')
url_start = "https://www.foxsports.com/nba/stats?season=20"
url_end   = "&category=MISC&group=1&sort=1&time=0&pos=0&team=0&qual=1&sortOrder=0&opp=0&page="
http = urllib3.PoolManager()


for i in range(17, 19):
    for j in range(1, 13):
        if i == 17 and j == 12:
            continue
        sys.stdout = open(str(i) + '-' + str(j) + ".html", 'w')
        url = url_start + str(i) + url_end + str(j)
        response = http.request('GET', url)
        soup = BeautifulSoup(response.data)
        soup = soup.findAll('tbody')
        print(soup)
