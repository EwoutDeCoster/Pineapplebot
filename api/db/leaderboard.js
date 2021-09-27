const knex = require("./knex");

function getUsers(guild) {
  let result = knex("leveling")
    .where("guild_id", guild)
    .select("*")
    .orderBy([
      { column: "lvl", order: "desc" },
      { column: "exp", order: "desc" },
    ]);
  return result;
}

function getAll() {
  return knex("leveling").select("*");
}

function getWealth(guild) {
  let result = knex("economy")
    .where("guild", guild)
    .select("*")
    .orderBy([{ column: "silver", order: "desc" }]);
  return result;
}

function getGuild(guild) {
  let result = knex("main")
    .where("guild_id", guild)
    .select("guild_id", "guild_name", "owner", "serverlogo");
  return result;
}

function getBotStats() {
  let result = knex("botstats").select("*");
  return result;
}

module.exports = { getUsers, getAll, getWealth, getGuild, getBotStats };
