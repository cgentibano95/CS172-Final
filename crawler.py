import requests
from bs4 import BeautifulSoup
visited_links = []
all_links = []
PGS_CRAWLED = 0 
MAX_LEVEL = 0


'''
crawls a provided url, grabs all href links and stores into all_links
'''
def crawl(url):
    global PGS_CRAWLED, MAX_LEVEL
    PGS_CRAWLED += 1
    code = requests.get(url)
    content = code.text
    s = BeautifulSoup(content, "html.parser")
    links = []
    
    for a in s.find_all('a', href=True):
        if a.get('href'):
            if a.get('href')[0] == '/':
                links.append(a.get('href')[1:])
                if a.get('href') not in all_links:
                    all_links.append(url + a.get('href')[1:])
            elif a.get('href')[0].lower() == "h":
                # this is to ignore m to ignore "mailto" and menus
                # basically any links that aren't additional levels from seed are here.
                links.append(a.get('href'))
                if a.get('href') not in  all_links:
                    all_links.append(a.get('href'))
    if (len(url.split('/')) - 3) > MAX_LEVEL:
        MAX_LEVEL = (len(url.split('/')) - 3)
    for link in links:
        if ':' not in link and link != "/" and link not in visited_links:
            visited_links.append(link)
            # this below is to prevent the UCR link error
            # ex. url = ucr.edu/news and link = news/somethinghere/somethingmore/etc/etc/..
            # this causes an issue, but i noticed only occurs with cs.ucr.edu
            if(url[-1] != '/'):
                '''
                print("the url: ")
                print(url)
                print(link)
                print("crawling: " + (url +'/' + link))
                '''
                crawl(url +'/' + link)
            else:
                crawl(url + link)

'''
Reads from seed.txt, calls crawl for each url, and writes all links to results.txt
'''
def readWriteFiles():
    f = open('seed.txt', 'r')
    lines = f.readlines()
    for line in lines:
        url = line.rstrip()
        print("crawling the url: " + url)
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
    print("max level found: " + str(MAX_LEVEL))

