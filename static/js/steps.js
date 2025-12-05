(() => {
    const paso1 = document.getElementById("paso1");
    if (!paso1) return; // Exit if elements don't exist (not on report page)

    const pasosContenido = [
      document.getElementById("paso1"),
      document.getElementById("paso2"),
      document.getElementById("paso3"),
      document.getElementById("paso4"),
      document.getElementById("paso5"),
      document.getElementById("paso6"),
    ];

    const pasosVisuales = [
      document.getElementById("step-1"),
      document.getElementById("step-2"),
      document.getElementById("step-3"),
      document.getElementById("step-4"),
      document.getElementById("step-5"),
      document.getElementById("step-6"),
    ];

    const progressFill = document.getElementById("progress-fill");
    let pasoActual = 0;

    function actualizarVista() {
      // Mostrar contenido del paso
      pasosContenido.forEach((paso, i) => {
        if(paso) paso.style.display = i === pasoActual ? "block" : "none";
      });

      // Actualizar barra de progreso visual
      pasosVisuales.forEach((step, i) => {
        if(step) {
            step.classList.remove("active", "completed");
            if (i < pasoActual) step.classList.add("completed");
            else if (i === pasoActual) step.classList.add("active");
        }
      });

      // Actualizar ancho de la línea de progreso
      if(progressFill) {
          const porcentaje = (pasoActual / (pasosVisuales.length - 1)) * 100;
          progressFill.style.width = `${porcentaje}%`;
      }

      // Habilitar/deshabilitar botones
      const btnPrev = document.getElementById("btnAnterior");
      const btnNext = document.getElementById("btnSiguiente");
      
      if(btnPrev) btnPrev.disabled = pasoActual === 0;
      if(btnNext) btnNext.disabled = pasoActual === pasosContenido.length - 1;
    }

    const btnPrev = document.getElementById("btnAnterior");
    if(btnPrev) {
        btnPrev.addEventListener("click", () => {
          if (pasoActual > 0) {
            pasoActual--;
            actualizarVista();
          }
        });
    }

    const btnNext = document.getElementById("btnSiguiente");
    if(btnNext) {
        btnNext.addEventListener("click", () => {
          if (pasoActual < pasosContenido.length - 1) {
            pasoActual++;
            actualizarVista();
          }
        });
    }

    // Cargar vista inicial
    actualizarVista();
})();