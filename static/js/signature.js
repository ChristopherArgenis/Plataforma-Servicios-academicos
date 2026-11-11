// Área para dibujar la firma (ratón, dedo o lápiz digital).
(() => {
  const form = document.getElementById("signature-form");
  if (!form) return;
  const canvas = document.getElementById("signature-pad");
  const hidden = document.getElementById("signature-data");
  const fileInput = document.getElementById("signature-file");
  const hint = document.querySelector(".signature-hint");
  const ctx = canvas.getContext("2d");
  let drawing = false;
  let dirty = false;
  let last = null;

  // Ajusta la resolución del canvas a su tamaño en pantalla (nítido en pantallas HiDPI)
  function resize() {
    const ratio = window.devicePixelRatio || 1;
    const { width, height } = canvas.getBoundingClientRect();
    if (!width) return; // aún oculto
    canvas.width = Math.round(width * ratio);
    canvas.height = Math.round(height * ratio);
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
    ctx.lineWidth = 2.5;
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
    ctx.strokeStyle = "#0b1f3a";
    clear();
  }

  function clear() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    dirty = false;
    hint.hidden = false;
  }

  function point(e) {
    const r = canvas.getBoundingClientRect();
    return { x: e.clientX - r.left, y: e.clientY - r.top };
  }

  canvas.addEventListener("pointerdown", (e) => {
    drawing = true;
    last = point(e);
    canvas.setPointerCapture(e.pointerId);
    ctx.beginPath();
    ctx.arc(last.x, last.y, ctx.lineWidth / 2, 0, Math.PI * 2);
    ctx.fillStyle = ctx.strokeStyle;
    ctx.fill();
    dirty = true;
    hint.hidden = true;
  });
  canvas.addEventListener("pointermove", (e) => {
    if (!drawing) return;
    const p = point(e);
    ctx.beginPath();
    ctx.moveTo(last.x, last.y);
    ctx.lineTo(p.x, p.y);
    ctx.stroke();
    last = p;
  });
  ["pointerup", "pointercancel", "pointerleave"].forEach((ev) =>
    canvas.addEventListener(ev, () => (drawing = false))
  );

  document.getElementById("signature-clear").addEventListener("click", clear);

  // El canvas está oculto al cargar (otro paso visible): se ajusta al mostrarse
  new ResizeObserver(() => {
    if (!dirty) resize();
  }).observe(canvas);

  form.addEventListener("submit", (e) => {
    const hasFile = fileInput.files.length > 0;
    hidden.value = !hasFile && dirty ? canvas.toDataURL("image/png") : "";
    if (!hasFile && !dirty && form.dataset.hasSignature !== "1") {
      e.preventDefault();
      alert("Dibuja tu firma o sube una imagen antes de guardar.");
    }
  });
})();
