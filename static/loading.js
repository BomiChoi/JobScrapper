let sw = true;
const form = document.querySelector("form");
const txt = document.querySelector(".loading");

function load() {
  console.log(txt);
  txt.innerText = "Searching...";
  console.log(txt.innerText);
  setInterval(changeText, 3000);
}

function changeText() {
  if (sw) {
    txt.innerText = "It may take some time...";
    sw = false;
  } else {
    txt.innerText = "Searching...";
    sw = true;
  }

  form.addEventListener("submit", load);
}
