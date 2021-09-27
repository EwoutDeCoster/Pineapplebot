const express = require("express");
const app = express();
const bodyParser = require("body-parser");
const db = require("./db/leaderboard");
const cors = require("cors");
const https = require("https");
const path = require("path");
const fs = require("fs");

app.use(cors());

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.get("/test", (req, res) => {
  res.status(200).json({ Test: "success" });
});

app.get("/all", async (req, res) => {
  const users = await db.getAll();
  res.status(200).json({ users });
});

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

const sslServer = https.createServer(
  {
    key: fs.readFileSync(path.join(__dirname, "cert", "key.pem")),
    cert: fs.readFileSync(path.join(__dirname, "cert", "cert.pem")),
  },
  app
);

sslServer.listen(1339, () => console.log("server is running on port 1339"));
