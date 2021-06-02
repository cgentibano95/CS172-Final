// import dependencies
const config = require("config");
const express = require("express");
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

app.post("/example", function (req, res) {
  //   client
  //     .index({
  //       index: "game-of-thrones",
  //       body: {
  //         character: "Ned Stark",
  //         quote: "Winter is coming.",
  //       },
  //     })
  //     .then((data) => res.json(data))
  //     .catch((err) => console.log(err));

  //   client
  //     .index({
  //       index: "game-of-thrones",
  //       body: {
  //         character: "Daenerys Targaryen",
  //         quote: "I am the blood of the dragon.",
  //       },
  //     })
  //     .then((data) => res.json(data))
  //     .catch((err) => console.log(err));

  //   client
  //     .index({
  //       index: "game-of-thrones",
  //       body: {
  //         character: "Tyrion Lannister",
  //         quote: "A mind needs books like a sword needs a whetstone.",
  //       },
  //     })
  //     .then((data) => res.json(data))
  //     .catch((err) => console.log(err));

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
        console.log(hit._source.character);
        relevantData.push(foundData);
      });
      console.log(relevantData);
      return res.status(200).json(relevantData);
    })
    .catch((err) => console.log(err));
});

app.listen(port, () =>
  console.log(`Server listening on http://localhost:${port}`)
);
