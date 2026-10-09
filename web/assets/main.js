// Menú móvil
(function () {
  var btn = document.querySelector(".menu-btn");
  var nav = document.getElementById("nav");
  if (!btn || !nav) return;
  btn.addEventListener("click", function () {
    var open = nav.classList.toggle("open");
    btn.setAttribute("aria-expanded", open ? "true" : "false");
  });
})();

// Visor de fotos: cualquier enlace con data-lb abre la foto grande; se navega dentro del mismo grupo.
(function () {
  var links = Array.prototype.slice.call(document.querySelectorAll("a[data-lb]"));
  if (!links.length || !window.HTMLDialogElement) return;
  var dlg = document.createElement("dialog");
  dlg.className = "lb";
  dlg.innerHTML =
    '<div class="lb-inner"><img alt=""></div>' +
    '<button class="x" aria-label="Cerrar">×</button>' +
    '<button class="prev" aria-label="Anterior">‹</button>' +
    '<button class="next" aria-label="Siguiente">›</button><p></p>';
  document.body.appendChild(dlg);
  var img = dlg.querySelector("img"), cap = dlg.querySelector("p");
  var group = [], i = 0;

  function show(n) {
    i = (n + group.length) % group.length;
    var a = group[i];
    img.src = a.getAttribute("href");
    img.alt = a.querySelector("img").alt;
    cap.textContent = img.alt;
  }
  links.forEach(function (a) {
    a.addEventListener("click", function (e) {
      e.preventDefault();
      var g = a.getAttribute("data-lb");
      group = links.filter(function (l) { return l.getAttribute("data-lb") === g; });
      show(group.indexOf(a));
      dlg.showModal();
    });
  });
  dlg.querySelector(".x").onclick = function () { dlg.close(); };
  dlg.querySelector(".prev").onclick = function () { show(i - 1); };
  dlg.querySelector(".next").onclick = function () { show(i + 1); };
  dlg.addEventListener("click", function (e) { if (e.target === dlg || e.target.className === "lb-inner") dlg.close(); });
  document.addEventListener("keydown", function (e) {
    if (!dlg.open) return;
    if (e.key === "ArrowLeft") show(i - 1);
    if (e.key === "ArrowRight") show(i + 1);
  });
  var x0 = null;
  dlg.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; }, { passive: true });
  dlg.addEventListener("touchend", function (e) {
    if (x0 === null) return;
    var dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 50) show(dx < 0 ? i + 1 : i - 1);
    x0 = null;
  });
})();

// Formulario de contacto (Web3Forms)
(function () {
  var form = document.getElementById("contact-form");
  if (!form) return;
  var msg = form.querySelector(".form-msg");
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var btn = form.querySelector("button[type=submit]");
    var data = Object.fromEntries(new FormData(form));
    btn.disabled = true;
    msg.textContent = "Enviando…";
    fetch("https://api.web3forms.com/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify(data)
    })
      .then(function (r) { return r.json(); })
      .then(function (r) {
        if (!r.success) throw new Error(r.message);
        form.reset();
        msg.textContent = "¡Gracias! Hemos recibido tu mensaje y te responderemos muy pronto.";
      })
      .catch(function () {
        msg.textContent = "No se ha podido enviar. Escríbenos por WhatsApp y te atendemos enseguida.";
      })
      .finally(function () { btn.disabled = false; });
  });
})();
