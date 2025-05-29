const pasosContenido = [
  document.getElementById("paso1"),
  document.getElementById("paso2"),
  document.getElementById("paso3"),
  document.getElementById("paso4"),
];

const pasosVisuales = [
  document.getElementById("step-1"),
  document.getElementById("step-2"),
  document.getElementById("step-3"),
  document.getElementById("step-4"),
];

const progressFill = document.getElementById("progress-fill");
let pasoActual = 0;

function actualizarVista() {
  // Mostrar contenido del paso
  pasosContenido.forEach((paso, i) => {
    paso.style.display = i === pasoActual ? "block" : "none";
  });

  // Actualizar barra de progreso visual
  pasosVisuales.forEach((step, i) => {
    step.classList.remove("active", "completed");
    if (i < pasoActual) step.classList.add("completed");
    else if (i === pasoActual) step.classList.add("active");
  });

  // Actualizar ancho de la línea de progreso
  const porcentaje = (pasoActual / (pasosVisuales.length - 1)) * 100;
  progressFill.style.width = `${porcentaje}%`;

  // Habilitar/deshabilitar botones
  document.getElementById("btnAnterior").disabled = pasoActual === 0;
  document.getElementById("btnSiguiente").disabled =
    pasoActual === pasosContenido.length - 1;
}

document.getElementById("btnAnterior").addEventListener("click", () => {
  if (pasoActual > 0) {
    pasoActual--;
    actualizarVista();
  }
});

document.getElementById("btnSiguiente").addEventListener("click", () => {
  if (pasoActual < pasosContenido.length - 1) {
    pasoActual++;
    actualizarVista();
  }
});

// Cargar vista inicial
window.onload = actualizarVista;