# Web Crawler

## Crawler.py

For the crawler.py, we make sure to follow as advised during lecture:

1. Crawls through every url provided in seed.txt
2. loops the amount of pages provided for the function
3. dequeue's a URL from the seed
4. if we run into any issues, we use a try/except in case we aren't allowed to crawl
5. Grab the html, but if it is an href we do extra checking to match the url format in our queue.
6. For each url that hasn't been visited from the seed, we add to queue.

## Website

The website was built using NodeJS, React, Express, and the ElasticSearch JS module.

### Usage

To get the site up and running we have to perform two actions:

1. Start the backend
2. Start the frontend

To start the backend, perform the following commands:

```
$ cd website\backend
$ npm start
```

This will launch the simple backend which queries the
ElasticSearch cluster.

To start the frontend, perform the following commands:

```
$ cd website\frontend
$ npm start
```

This should launch a new page at:

`localhost:3000`

To run queries on the frontend, users must use a specific format:

`key1:value1, key2:value2, ... , keyn:valuen`

There are various keys that users can take advantage of:

- `url`: refers to the url of the page that was crawled.

- `title`: refers to the title of the webpage.

- `text`: refers to any text that is found in the body of a
  webpage with tags: h1, h2, h3, h4, and p.

An example query may be:

`title:ucr, text:computer science`

or

`url:ucr, text:the best`

#### Issues

- When using a `url` search, if `www` is not included in the
  url, it is possible that a match will not be found even if the
  document exists.
-
