const knex = require("knex");

const connectedKnex = knex({
  client: "sqlite",
  connection: {
    filename: "/root/Pineapple/cogs/main.sqlite",
  },
});

module.exports = connectedKnex;
