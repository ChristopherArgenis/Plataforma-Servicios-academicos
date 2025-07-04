const adquisicion = document.getElementById("Adquisicion");
const information = document.getElementById("Information");
const report = document.getElementById("Report");
const tables = document.getElementById("Tables");

const radio1 = document.getElementById("vbtn-radio1");
const radio2 = document.getElementById("vbtn-radio2");
const radio3 = document.getElementById("vbtn-radio3");
const radio4 = document.getElementById("vbtn-radio4");

function Adquisicion() {
  adquisicion.style.display = "block";
  information.style.display = "none";
  report.style.display = "none";
  tables.style.display = "none";
}

function Information() {
  adquisicion.style.display = "none";
  information.style.display = "block";
  report.style.display = "none";
  tables.style.display = "none";
}

function Reports() {
  adquisicion.style.display = "none";
  information.style.display = "none";
  report.style.display = "block";
  tables.style.display = "none";
}

function Tables() {
  adquisicion.style.display = "none";
  information.style.display = "none";
  report.style.display = "none";
  tables.style.display = "block";
}

radio1.addEventListener("click", Adquisicion);
radio2.addEventListener("click", Information);
radio3.addEventListener("click", Reports);
radio4.addEventListener("click", Tables);