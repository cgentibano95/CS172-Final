import requests
from time import sleep
from bs4 import BeautifulSoup
all_links = []
PGS_CRAWLED = []
LINK_QUEUE = []

'''
crawls a provided url, grabs all href links and stores into all_links
'''
def crawl(url):
    global PGS_CRAWLED
    PGS_CRAWLED.append(url)

    print("crawling: " + url)
    try:
        code = requests.get(url)
    except:
        print("error at this url: " + url)
        print("skipping to next url")
        return
    content = code.text
    s = BeautifulSoup(content, "html.parser")
    

    # now find hrefs
    for a in s.find_all('a', href=True):
        if a.get('href'):
            if a.get('href')[0] == '/':
                if ((url + a.get('href').strip()) not in PGS_CRAWLED) and ((url + a.get('href')[1:].strip()) not in PGS_CRAWLED):
                    if url[-1] != '/':
                        all_links.append(url + a.get('href').strip())
                        LINK_QUEUE.append(url + a.get('href').strip())
                    else:
                        all_links.append(url + a.get('href')[1:].strip())
                        LINK_QUEUE.append(url + a.get('href')[1:].strip())
            elif a.get('href')[0].lower() == "h":
                # this is to ignore m to ignore "mailto" and menus
                #links.append(a.get('href'))
                if (a.get('href') not in  all_links) and (a.get('href').strip() not in PGS_CRAWLED):
                    all_links.append(a.get('href').strip())
                    LINK_QUEUE.append(a.get('href').strip())
                
'''
Reads from seed.txt, calls crawl for each url, and writes all links to results.txt
'''
def readWriteFiles(outFile, num_pgs):
    f = open('seed.txt', 'r')
    lines = f.readlines()
    for line in lines:
        url = line.rstrip()
        LINK_QUEUE.append(url)
    f.close()

    for pg in range(num_pgs):
        print(pg)
        crawl(LINK_QUEUE.pop(0))
        #sleep(2)

    # write to file
    f = open(outFile, "a")
    for l in all_links:
        f.write(l + " \n")
    f.close()



if __name__ == "__main__":
    outFile = "results.txt"
    num_pgs = 7200
    readWriteFiles(outFile, num_pgs)
    print("\n\ndone scraping")
    print("results found at: " + outFile)

