// Protección CSRF: agrega el token del servidor a todos los envíos POST.
// - Formularios POST (incluidos los que llegan por HTMX): campo oculto csrf_token.
// - fetch() a este mismo sitio y peticiones HTMX: cabecera X-CSRFToken.
(function () {
  const meta = document.querySelector('meta[name="csrf-token"]');
  if (!meta) return;
  const token = meta.content;

  function addTokenToForms(root) {
    if (!root.querySelectorAll) return;
    const forms = root.matches && root.matches("form") ? [root] : root.querySelectorAll("form");
    forms.forEach((form) => {
      const isPost = (form.getAttribute("method") || "").toLowerCase() === "post" || form.hasAttribute("hx-post");
      if (!isPost || form.querySelector('input[name="csrf_token"]')) return;
      const input = document.createElement("input");
      input.type = "hidden";
      input.name = "csrf_token";
      input.value = token;
      form.appendChild(input);
    });
  }

  document.addEventListener("DOMContentLoaded", () => addTokenToForms(document));
  new MutationObserver((mutations) => {
    mutations.forEach((m) => m.addedNodes.forEach((node) => addTokenToForms(node)));
  }).observe(document.documentElement, { childList: true, subtree: true });

  const originalFetch = window.fetch;
  window.fetch = function (input, init = {}) {
    const method = (init.method || (input instanceof Request ? input.method : "GET")).toUpperCase();
    if (!["GET", "HEAD", "OPTIONS"].includes(method)) {
      const url = new URL(typeof input === "string" ? input : input.url, window.location.href);
      if (url.origin === window.location.origin) {
        init.headers = new Headers(init.headers || {});
        if (!init.headers.has("X-CSRFToken")) init.headers.set("X-CSRFToken", token);
      }
    }
    return originalFetch.call(this, input, init);
  };

  document.addEventListener("htmx:configRequest", (e) => {
    e.detail.headers["X-CSRFToken"] = token;
  });
})();
