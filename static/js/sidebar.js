const adquisicion = document.getElementById("Adquisicion");
const report = document.getElementById("Report");
const settings = document.getElementById("Setting");

const radio1 = document.getElementById("vbtn-radio1");
const radio2 = document.getElementById("vbtn-radio2");
const radio3 = document.getElementById("vbtn-radio3");

function Adquisicion() {
  adquisicion.style.display = "block";
  report.style.display = "none";
  settings.style.display = "none";
}

function Reports() {
  adquisicion.style.display = "none";
  report.style.display = "block";
  settings.style.display = "none";
}

function setting() {
  adquisicion.style.display = "none";
  report.style.display = "none";
  settings.style.display = "block";
}

radio1.addEventListener("click", Adquisicion);
radio2.addEventListener("click", Reports);
radio3.addEventListener("click", setting);