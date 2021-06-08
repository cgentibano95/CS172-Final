import requests
from bs4 import BeautifulSoup
all_links = []
PGS_CRAWLED = 0 

'''
crawls a provided url, grabs all href links and stores into all_links
'''
def crawl(url, links):
    global PGS_CRAWLED, MAX_LEVEL
    PGS_CRAWLED += 1
    code = requests.get(url)
    content = code.text
    s = BeautifulSoup(content, "html.parser")
    
    for a in s.find_all('a', href=True):
        if a.get('href'):
            if a.get('href')[0] == '/':
                links.append(a.get('href'))
                if a.get('href') not in all_links:
                    all_links.append(url + a.get('href')[1:])
            elif a.get('href')[0].lower() == "h":
                # this is to ignore m to ignore "mailto" and menus
                links.append(a.get('href'))
                if a.get('href') not in  all_links:
                    all_links.append(a.get('href'))
                
'''

Reads from seed.txt, calls crawl for each url, and writes all links to results.txt
'''
def readWriteFiles(outFile):
    f = open('seed.txt', 'r')
    lines = f.readlines()
    for line in lines:
        links = []
        url = line.rstrip()
        print("trying the url: " + url)
        crawl(url, links)
    f.close()
    # write to file
    f = open(outFile, "a")
    for l in all_links:
        f.write(l + " \n")
    f.close()


if __name__ == "__main__":
    outFile = "results.txt"
    readWriteFiles(outFile)
    print("done scraping \n\n")
    print("pages crawled: " + str(PGS_CRAWLED))
    print("results found at: " + outFile)

