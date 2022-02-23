var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function () {
    this.classList.toggle("activecol");
    var content = this.nextElementSibling;
    if (content.style.maxHeight) {
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + "px";
    }
  });
}

var colll = document.getElementsByClassName("admin");
var i;

for (i = 0; i < colll.length; i++) {
  colll[i].addEventListener("click", function () {
    this.classList.toggle("activecolad");
    var content = this.nextElementSibling;
    if (content.style.maxHeight) {
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + "px";
    }
  });
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
      document.getElementById("bigpine").src = `${date.stats[0].avatar}`;
    })
    .catch((error) => {
      console.log(error);
    });
}

function changeVisibility() {
  let checkbox = document.getElementById("AdminCheckBox");
  let checkboxtext = document.getElementById("AdminCheckBoxText");
  if (checkbox.checked) {
    let i = 0;
    checkboxtext.style.color = "#ED4245";
    const alladm = document.getElementsByClassName("admin");
    document.getElementById("configuration").style.display = "";
    document.getElementById("conf").style.display = "";
    while (i < alladm.length) {
      alladm[i].style.display = "";
      i += 1;
    }
  } else {
    /*#858796*/
    let i = 0;
    checkboxtext.style.color = "#858796";
    const alladm = document.getElementsByClassName("admin");
    document.getElementById("configuration").style.display = "none";
    document.getElementById("conf").style.display = "none";
    while (i < alladm.length) {
      alladm[i].style.display = "none";
      i += 1;
    }
  }
}

function init() {
  changeVisibility();
  document.getElementById("AdminCheckBox").onclick = changeVisibility;
  document.getElementById("AdminCheckBoxText").onclick = changeVisibility;
  getBotStats();
}

window.onload = init;
