import requests
from bs4 import BeautifulSoup
visited_links = []
all_links = []
PGS_CRAWLED = 0

'''
crawls a provided url, grabs all href links and stores into all_links
'''
def crawl(url):
    global PGS_CRAWLED
    PGS_CRAWLED += 1
    code = requests.get(url)
    content = code.text
    s = BeautifulSoup(content, "html.parser")
    links = []
    
    for a in s.find_all('a', href=True):
        if a.get('href'):
            if a.get('href')[0] == '/':
                links.append(a.get('href'))
                if a.get('href') not in all_links:
                    all_links.append(url + a.get('href'))
            elif a.get('href')[0].lower() == "h":
                # this is to ignore m to ignore "mailto" & there was a weird link with "more info"
                links.append(a.get('href'))
                if a.get('href') not in  all_links:
                    all_links.append(a.get('href'))

    for link in links:
        if ':' not in link and link != "/" and link not in visited_links:
            visited_links.append(link)
            # this is to just make sure we aren't visitng a link we've already gone to
            crawl(url + link)

'''
Reads from seed.txt, calls crawl for each url, and writes all links to results.txt
'''
def readWriteFiles():
    f = open('seed.txt', 'r')
    lines = f.readlines()
    for line in lines:
        url = line.rstrip()
        print("trying the url: " + url)
        crawl(url)
    
    f.close()
    f = open("results.txt", "a")
    for l in all_links:
        f.write(l + " \n")
    f.close()


if __name__ == "__main__":
    readWriteFiles()
    print("done scraping \n\n")
    print("pages crawled: " + str(PGS_CRAWLED))

