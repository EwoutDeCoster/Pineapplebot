function getBotStats() {
  fetch(`https://www.pineappleapi.ga/bot/stats`)
    .then((res) => res.json())
    .then((data) => {
      return data;
    })
    .then((date) => {
      console.log(date);
      document.getElementById("servers").innerHTML = `${date.stats[0].servers}`;
      document.getElementById("users").innerHTML = `${date.stats[0].users}`;
      document.getElementById("bigpine").src = `${date.stats[0].avatar}`
      document.getElementById("logo").src = `${date.stats[0].avatar}`
    })
    .catch((error) => {
      console.log(error);
      document.getElementById("status").innerHTML = "Offline";
      document.getElementById("statustext").style.color = "#ED4245";
    });
}

const init = function () {
  getBotStats();
}


window.onload = init;
