// import dependencies
const config = require("config");
const express = require("express");
const cors = require("cors");
const { Client } = require("@elastic/elasticsearch");

const client = new Client({
  cloud: {
    id: config.get("cloudId"),
  },
  auth: {
    username: config.get("username"),
    password: config.get("password"),
  },
});

const indexName = "test-index";
const app = express();
const port = 8080;
app.use(express.json());
app.use(cors());

app.post("/search", function (req, res) {
  const query = {
    title: req.body.title,
    url: req.body.url,
    hrefs: req.body.hrefs,
    imgs: req.body.imgs,
    text: req.body.text,
  };

  client
    .search({
      index: indexName,
      body: {
        query: {
          match: {
            title: query.title,
          },
        },
      },
    })
    .then((data) => {
      let relevantData = [];
      let hits = data.body.hits.hits;
      hits.forEach((hit) => {
        console.log(hit);
        const foundData = {
          id: hit._id,
          title: hit._source.title,
          href: hit._source.href,
          text: hit._source.text,
          score: hit._score,
          timestamp: hit._source.timestamp,
        };

        relevantData.push(foundData);
      });

      return res.json({ relevantData });
    })
    .catch((err) => console.log(err));
});

app.post("/example", function (req, res) {
  client
    .search({
      index: "game-of-thrones",
      body: {
        query: {
          match: {
            quote: "mind",
          },
        },
      },
    })
    .then((data) => {
      let relevantData = [];
      let hits = data.body.hits.hits;
      hits.forEach((hit) => {
        const foundData = {
          character: hit._source.character,
          quote: hit._source.quote,
          score: hit._score,
        };
        relevantData.push(foundData);
      });
      return res.status(200).json(relevantData);
    })
    .catch((err) => console.log(err));
});

app.listen(port, () =>
  console.log(`Server listening on http://localhost:${port}`)
);
