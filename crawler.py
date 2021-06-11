import requests
from time import sleep
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
from datetime import datetime

all_links = []
PGS_CRAWLED = []
LINK_QUEUE = []

'''
crawls a provided url, grabs all href links and stores into all_links
'''


def crawl(url):
    global PGS_CRAWLED
    PGS_CRAWLED.append(url)

    elastic_doc = {
        "url": url,
        "title": "",
        "img": [],
        "href": [],
        "text": [],
        "timestamp": datetime.now()
    }

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
                # links.append(a.get('href'))
                if (a.get('href') not in all_links) and (a.get('href').strip() not in PGS_CRAWLED):
                    all_links.append(a.get('href').strip())
                    LINK_QUEUE.append(a.get('href').strip())

            elastic_doc.setdefault('href', []).append(a.get('href').strip())
        # Search for all tags with content

    tags = ['h1', 'h2', 'h3', 'h4', 'p', 'img', 'title']
    for tag in tags:
        for result in s.find_all(name=tag):
            if tag == 'title':
                elastic_doc[tag] = result.get_text()
            elif tag == 'img':
                elastic_doc.setdefault(tag, []).append(result['src'])
            else:
                elastic_doc.setdefault('text', []).append(
                    result.get_text().strip())

    send_to_elastic(elastic_doc)


def send_to_elastic(document):
    with open('config/default.txt', 'r') as f:
        for line in f:
            credentials = line.split(' ')

    es = Elasticsearch(cloud_id=credentials[2], http_auth=(
        credentials[0], credentials[1]))
    res = es.create(index="test-index", body=document)
    print(res['result'])


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
        # sleep(2)

    # write to file
    f = open(outFile, "a")
    for l in all_links:
        f.write(l + " \n")
    f.close()


if __name__ == "__main__":
    outFile = "results.txt"
    num_pgs = 300
    readWriteFiles(outFile, num_pgs)
    print("\n\ndone scraping")
    print("results found at: " + outFile)
