const express = require("express");
const app = express();
const bodyParser = require("body-parser");
const db = require("./db/leaderboard");
const cors = require("cors");
const { getData, getPreview, getTracks } = require('spotify-url-info')
/*const https = require("https"),
  fs = require("fs");*/

app.use(cors());
/*
const options = {
  key: fs.readFileSync("/srv/www/keys/my-site-key.pem"),
  cert: fs.readFileSync("/srv/www/keys/chain.pem")
};*/

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.get("/", (req, res) => {
  res.status(200).json({ status: "online" });
});

app.get("/yt", async (req, res) => {
  getPreview(req.query.song).catch(err => res.status(200).json({ data : "failed" }))
  .then(data => res.status(200).json({ data }))
});

/*app.get("/all/leveling", async (req, res) => {
  const users = await db.getAll();
  res.status(200).json({ users });
});*/

app.get("/leaderboard/:guild_id", async (req, res) => {
  const users = await db.getUsers(req.params.guild_id, req.body);
  res.status(200).json({ users });
});

app.get("/wealth/:guild_id", async (req, res) => {
  const users = await db.getWealth(req.params.guild_id, req.body);
  res.status(200).json({ users });
});

app.get("/guild/:guild_id", async (req, res) => {
  const guild = await db.getGuild(req.params.guild_id, req.body);
  res.status(200).json({ guild });
});

app.get("/bot/stats", async (req, res) => {
  const stats = await db.getBotStats();
  res.status(200).json({ stats });
});

app.listen(80, () => console.log("server is running on port 80"));
/*https.createServer(options, app).listen(443);*/
