"""
Documentation can be found at:

https://elasticsearch-py.readthedocs.io/en/v7.13.0/api.html#elasticsearch
"""
from datetime import datetime
from elasticsearch import Elasticsearch

with open('config/default.txt', 'r') as f:
    for line in f:
        credentials = line.split(' ')

es = Elasticsearch(cloud_id=credentials[2], http_auth=(
    credentials[0], credentials[1]))

doc = {
    'author': 'kimchy',
    'text': 'Elasticsearch: cool. bonsai cool.',
    'timestamp': datetime.now(),
}

doc2 = {
    'author': 'juan',
    'text': 'Elasticsearch: cool.',
    'timestamp': datetime.now(),
}

res = es.index(index="test-index", id=1, body=doc)
print(res['result'])

res = es.get(index="test-index", id=1)
print(res['_source'])

res = es.create(index="test-index", id=2, body=doc2)
print(res['result'])

es.indices.refresh(index="test-index")

res = es.search(index="test-index", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total']['value'])
for hit in res['hits']['hits']:
    print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])

res = es.indices.delete(index="test-index")
if res['acknowledged'] == True:
    print("Test index deleted")
