function getUrlVars() {
  var vars = {};
  var parts = window.location.href.replace(
    /[?&]+([^=&]+)=([^&]*)/gi,
    function (m, key, value) {
      vars[key] = value;
    }
  );
  return vars;
}

let guild = getUrlVars();
try {
  guild_id = guild.guild;
} catch (error) {
  console.log("slechte vars");
  console.log(error);
}

function fetchData() {
  if (guild_id) {
    fetch(`https://www.pineappleapi.ga/leaderboard/${guild_id}`)
      .then((res) => res.json())
      .then((data) => {
        return data;
      })
      .then((date) => {
        console.log(date.users);
        let i = 0;
        let avatar;
        let discriminator;
        while (i < date.users.length) {
          if (date.users[i].avatar != null && date.users[i].avatar != "null") {
            avatar = date.users[i].avatar;
          } else {
            avatar = "https://cdn.discordapp.com/embed/avatars/3.png";
          }
          if (
            date.users[i].discriminator != null &&
            date.users[i].avatar != "null"
          ) {
            discriminator = date.users[i].discriminator;
          } else {
            discriminator = "0000";
          }
          document
            .getElementById("tbodyy")
            .insertAdjacentHTML(
              "beforeend",
              `<tr><td><b>${
                i + 1
              }.</b>  <img class="rounded-circle me-2" width="30" height="30" src="${avatar}" onerror="this.onerror=null;this.src='https://cdn.discordapp.com/embed/avatars/3.png';" />${
                date.users[i].username
              }#${discriminator}</td><td>${date.users[i].lvl}</td><td>${kwaarde(date.users[i].exp)
              }</td></tr>`
            );
          i += 1;
        }
      })
      .catch((error) => {
        console.log(error);
      });
  } else {
    console.log("Error");
    document
      .getElementById("tbodyy")
      .insertAdjacentHTML(
        "beforeend",
        `<tr><td><img class="rounded-circle me-2" width="30" height="30" src="https://cdn.discordapp.com/embed/avatars/3.png" /><b>Invalid server</b></td><td>/</td><td>/</td></tr>`
      );
  }
}

function getBotStats() {
  fetch(`https://www.pineappleapi.ga/bot/stats`)
    .then((res) => res.json())
    .then((data) => {
      return data;
    })
    .then((date) => {
      console.log(date);
      document.getElementById("logo").src = `${date.stats[0].avatar}`;
    })
    .catch((error) => {
      console.log(error);
    });
}

kwaarde = function (num, fixed) {
  if (num === null) {
    return null;
  } // terminate early
  if (num === 0) {
    return "0";
  } // terminate early
  fixed = !fixed || fixed < 0 ? 0 : fixed; // number of decimal places to show
  var b = num.toPrecision(2).split("e"), // get power
    k = b.length === 1 ? 0 : Math.floor(Math.min(b[1].slice(1), 14) / 3), // floor at decimals, ceiling at trillions
    c =
      k < 1
        ? num.toFixed(0 + fixed)
        : (num / Math.pow(10, k * 3)).toFixed(1 + fixed), // divide by power
    d = c < 0 ? c : Math.abs(c), // enforce -0 is 0
    e = d + ["", "K", "M", "B", "T", "qd"][k]; // append power
  return e;
};

function getServerInfo() {
  fetch(`https://www.pineappleapi.ga/guild/${guild_id}`)
    .then((res) => res.json())
    .then((data) => {
      return data;
    })
    .then((date) => {
      console.log(date.guild[0]);
      document.getElementById(
        "servername"
      ).innerHTML = `${date.guild[0].guild_name}`;
      document.getElementById("serverlogo").src = `${date.guild[0].serverlogo}`;
    })
    .catch((error) => {
      console.log(error);
      document.getElementById("status").innerHTML = "Offline";
    });
}

function changeurls() {
  document.getElementById("ecobtn").href = `economy.html?&guild=${guild_id}`;
}

const init = function () {
  fetchData();
  getServerInfo();
  changeurls();
  getBotStats();
};

window.onload = init;
