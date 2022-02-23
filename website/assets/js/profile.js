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

function copyBut() {
  let text = document.getElementById("vanity");
  text.select();
  text.setSelectionRange(0, 99999);
  navigator.clipboard.writeText(text.value);
  console.log("uitgevoerd");
  document.getElementById("copyConfirm").innerHTML = "Copied to clipboard!";
  setTimeout(deleteSpanText, 3000);
}

function deleteSpanText() {
  document.getElementById("copyConfirm").innerHTML = "";
}

function insertValues() {
  document.getElementById("username").value = unescape(getUrlVars().username);
  document.getElementById("created").value = getUrlVars().createdon;
  document.getElementById("userid").value = getUrlVars().id;
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
    e = d + ["", "K", "M", "B", "T"][k]; // append power
  return e;
};

function getFromApi(guild) {
  fetch(`https://www.pineappleapi.ga/wealth/${guild}`)
    .then((res) => res.json())
    .then((data) => {
      return data;
    })
    .then((date) => {
      console.log(date.users);
      let i = 0;
      while (i < date.users.length) {
        if (date.users[i].user == getUrlVars().id) {
          document.getElementById("silver").innerHTML = kwaarde(
            date.users[i].silver
          );
          document.getElementById("usericon").src = date.users[i].avatar;
          document.getElementById(
            "discriminator"
          ).value = `#${date.users[i].discriminator}`;

          if (date.users[i].minerig == 1) {
            document.getElementById(
              "machine"
            ).innerHTML = `Level ${date.users[i].mineriglvl}`;
          } else {
            document.getElementById(
              "machine"
            ).innerHTML = `You don't have a machine`;
          }
        }
        i += 1;
      }
    })
    .catch((error) => {
      console.log(error);
    });
  fetch(`https://www.pineappleapi.ga/leaderboard/${guild}`)
    .then((res) => res.json())
    .then((data) => {
      return data;
    })
    .then((date) => {
      console.log(date.users);
      let i = 0;
      while (i < date.users.length) {
        if (date.users[i].user == getUrlVars().id) {
          document.getElementById("percentage").innerHTML = date.users[i].lvl;
          document.getElementsByClassName(
            "progress-bar"
          )[0].style.cssText = `width: ${Math.floor(100* (date.users[i].exp / Math.floor(5 * (date.users[i].lvl ^ 2) + 50 * date.users[i].lvl + 100)))}%`;
          document.getElementById("lvlbtn").href = `leveling.html?&guild=${
            getUrlVars().guild
          }`;
          document.getElementById("ecobtn").href = `economy.html?&guild=${
            getUrlVars().guild
          }`;
        }
        i += 1;
      }
    })
    .catch((error) => {
      console.log(error);
    });
}

const init = function () {
  /*document.getElementById("vanity").value = `https://www.pineapplebot.ga/profile?&guild=${getUrlVars().user}`;*/
  /*document.getElementById("copyBtn").onclick = copyBut;*/
  insertValues();
  getFromApi(getUrlVars().guild);
};

window.onload = init;
