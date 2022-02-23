function getUrlVars() {
  var vars = {};
  var parts = window.location.href.replace(
    /[?&]+([^=&]+)=([^&]*)/gi,
    function (m, key, value) {
      vars[key] = value;
    }
  );
  console.log(vars);
  return vars;
}

function displayScreen() {
  console.log("werkt");
  try {
    if (getUrlVars().invite.includes("discord.gg/")) {
      console.log(getUrlVars().invite);
      document.getElementById("redirectUrl").href = `${getUrlVars().invite}`;
      setTimeout(goToPage, 3000);
    } else {
      document.getElementById("redirectTitle").innerHTML =
        "Incorrect invite url.";
      document.getElementById("redirectText").innerHTML =
        "The provided url is not a discord server invite.";
    }
  } catch (error) {
    document.getElementById("redirectTitle").innerHTML = "Incorrect url";
    document.getElementById("redirectText").innerHTML =
      "You have been redirected to this page because of an incorrect url.";
  }
}

function goToPage() {
  location.replace(`${getUrlVars().invite}`);
}

function init() {
  displayScreen();
}

window.onload = init;
