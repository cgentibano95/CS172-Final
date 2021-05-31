import requests
from bs4 import BeautifulSoup
visited_links = []
all_links = []
DEPTH = 0

def crawl(url):
    global DEPTH
    DEPTH += 1
    code = requests.get(url)
    content = code.text
    s = BeautifulSoup(content, "html.parser")
    links = []
    
    for a in s.find_all('a', href=True):
        if a.get('href')[0] == '/':
            links.append(a.get('href'))
            if a.get('href')[0] != all_links:
                all_links.append(url + a.get('href'))
        elif a.get('href')[0].lower() != 'm':
            # this is to ignore m to ignore "mailto" & there was a weird link with "more info"
            links.append(a.get('href'))
            if a.get('href')[0] != all_links:
                all_links.append(a.get('href'))

    print ("Level " + str(DEPTH) + " ",url)
    for link in links:
        if ':' not in link and link != "/" and link not in visited_links:
            visited_links.append(link)
            # this is to just make sure we aren't visitng a link we've already gone to
            crawl(url + link)

crawl("https://www.ohlone.edu/")
# crawl("https://www1.cs.ucr.edu/")
print("done scraping \n\n")
for l in all_links:
    print(l)
print("depth is : ")
print(DEPTH)
