// Asistente de pasos del reporte.
const pasosContenido = document.querySelectorAll(".report-step");
const pasosVisuales = document.querySelectorAll(".step");
const progressFill = document.getElementById("progress-fill");
const btnAnterior = document.getElementById("btnAnterior");
const btnSiguiente = document.getElementById("btnSiguiente");
let pasoActual = 0;

function actualizarVista() {
  pasosContenido.forEach((paso, i) => (paso.hidden = i !== pasoActual));
  pasosVisuales.forEach((step, i) => {
    step.classList.toggle("completed", i < pasoActual);
    step.classList.toggle("active", i === pasoActual);
  });
  progressFill.style.width = `${(pasoActual / (pasosVisuales.length - 1)) * 100}%`;
  btnAnterior.disabled = pasoActual === 0;
  btnSiguiente.disabled = pasoActual === pasosContenido.length - 1;
}

btnAnterior.addEventListener("click", () => {
  if (pasoActual > 0) pasoActual--;
  actualizarVista();
});
btnSiguiente.addEventListener("click", () => {
  if (pasoActual < pasosContenido.length - 1) pasoActual++;
  actualizarVista();
});

actualizarVista();
