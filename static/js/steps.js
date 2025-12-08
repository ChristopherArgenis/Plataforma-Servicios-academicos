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
      document.getElementById("paso7"),
      document.getElementById("paso8"),
      document.getElementById("paso9"),
      document.getElementById("paso10"),
      document.getElementById("paso11"),
      document.getElementById("paso12"),
      document.getElementById("paso13"),
      document.getElementById("paso14"),
    ];

    const pasosVisuales = [
      document.getElementById("step-1"),
      document.getElementById("step-2"),
      document.getElementById("step-3"),
      document.getElementById("step-4"),
      document.getElementById("step-5"),
      document.getElementById("step-6"),
      document.getElementById("step-7"),
      document.getElementById("step-8"),
      document.getElementById("step-9"),
      document.getElementById("step-10"),
      document.getElementById("step-11"),
      document.getElementById("step-12"),
      document.getElementById("step-13"),
      document.getElementById("step-14"),
    ];

    const progressFill1 = document.getElementById("progress-fill-1");
    const progressFill2 = document.getElementById("progress-fill-2");
    const SPLIT_INDEX = 7; // Number of steps in the first row

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

      // Actualizar ancho de las líneas de progreso
      if (progressFill1 && progressFill2) {
          // Calculate percentage for first row
          let percent1 = 0;
          if (pasoActual >= SPLIT_INDEX) {
              percent1 = 100;
          } else {
              percent1 = (pasoActual / (SPLIT_INDEX - 1)) * 100;
          }
          progressFill1.style.width = `${percent1}%`;

          // Calculate percentage for second row
          let percent2 = 0;
          if (pasoActual < SPLIT_INDEX) {
              percent2 = 0;
          } else {
              // Normalized step for second row
              const stepsInRow2 = pasosVisuales.length - SPLIT_INDEX;
              const stepInRow2 = pasoActual - SPLIT_INDEX;
              percent2 = (stepInRow2 / (stepsInRow2 - 1)) * 100;
          }
          progressFill2.style.width = `${percent2}%`;
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