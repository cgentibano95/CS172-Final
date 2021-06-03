import requests
from xxhash import xxh32
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
from datetime import datetime

visited_links = []
all_links = []
DEPTH = 0


def crawl(url):
    global DEPTH
    DEPTH += 1
    # TODO: Update the url key with the normalized url, add hrefs to json
    elastic_doc = {
        "url": url,
        "title": "",
        "hrefs": [],
        "img": [],
        "p": [],
        "h1": [],
        "h2": [],
        "h3": [],
        "h4": [],
        "timestamp": datetime.now()
    }

    content = requests.get(url).text
    s = BeautifulSoup(content, "html.parser")
    links = []

    # TODO: Figure out a way to normalize the urls: deal with https/http and the # tags e.g. ohlone.com/#main menu#/
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

    print("Level " + str(DEPTH) + " ", url)

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

    for link in links:
        if ':' not in link and link != "/" and link not in visited_links:
            visited_links.append(link)
            # this is to just make sure we aren't visitng a link we've already gone to
            crawl(url + link)


def send_to_elastic(document):
    global es
    x = xxh32(document['url'])
    docId = x.intdigest()
    if not es.exists(index='test-index', id=docId):
        res = es.create(index="test-index", id=docId, body=document)
        print(res['result'])

    # Delete the document after creation
    res = es.delete(index="test-index", id=docId)
    print("-"*20)
    print("Deleting")
    print(res)


with open('config/default.txt', 'r') as f:
    for line in f:
        credentials = line.split(' ')

es = Elasticsearch(cloud_id=credentials[2], http_auth=(
    credentials[0], credentials[1]))

crawl("https://www.ohlone.edu/")
# crawl("https://www1.cs.ucr.edu/")
print("done scraping \n\n")
for l in all_links:
    print(l)
print("depth is : ")
print(DEPTH)
