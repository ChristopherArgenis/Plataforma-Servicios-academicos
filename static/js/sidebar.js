// Muestra una sección del panel a la vez y la recuerda en la URL (#reporte, #cuenta).
const links = document.querySelectorAll(".sidebar-link");
const sections = document.querySelectorAll(".panel-section");

function showSection(id) {
  if (!document.getElementById(id)) id = "adquisicion";
  sections.forEach((s) => (s.hidden = s.id !== id));
  links.forEach((l) => l.classList.toggle("active", l.dataset.section === id));
}

links.forEach((link) =>
  link.addEventListener("click", () => {
    history.replaceState(null, "", "#" + link.dataset.section);
    showSection(link.dataset.section);
  })
);

showSection(location.hash.slice(1));

// "Seleccionar todos" en la tabla de artículos
const checkAll = document.getElementById("check-all");
if (checkAll) {
  const rows = document.querySelectorAll(".row-check");
  checkAll.checked = rows.length > 0 && [...rows].every((r) => r.checked);
  checkAll.addEventListener("change", () => rows.forEach((r) => (r.checked = checkAll.checked)));
}
