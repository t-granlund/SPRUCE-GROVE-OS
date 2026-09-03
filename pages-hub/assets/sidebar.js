/* Code Puppy — sidebar behavior (progressive enhancement, WCAG-aware). */
(function () {
  "use strict";
  var body = document.body;
  var sb = document.querySelector(".sb");
  if (!sb) return;

  var isMobile = function () { return window.matchMedia("(max-width: 980px)").matches; };
  var lastFocus = null;
  var btnOpen = document.querySelector(".sb-burger");        // mobile topbar hamburger
  var btnClose = document.querySelector(".sb-toggle[data-sb-close]"); // sidebar close (mobile)
  var btnCollapse = document.querySelector(".sb-toggle[data-sb-collapse]"); // desktop collapse
  var skip = document.querySelector(".sb-skip");

  function openMobile(navigateFocus) {
    body.classList.add("sb-open");
    body.classList.remove("sb-collapsed");
    sb.setAttribute("aria-hidden", "false");
    if (btnOpen) btnOpen.setAttribute("aria-expanded", "true");
    if (navigateFocus !== false) {
      lastFocus = document.activeElement;
      var focusable = sb.querySelector("a,button,[tabindex]:not([tabindex='-1'])");
      if (focusable) focusable.focus();
    }
  }
  function closeMobile(restoreFocus) {
    body.classList.remove("sb-open");
    sb.setAttribute("aria-hidden", "true");
    if (btnOpen) btnOpen.setAttribute("aria-expanded", "false");
    if (restoreFocus !== false && lastFocus && lastFocus.focus) lastFocus.focus();
  }
  function toggleDesktop() {
    var c = body.classList.toggle("sb-collapsed");
    sb.setAttribute("aria-hidden", c ? "true" : "false");
    var lbl = c ? "Expand sidebar" : "Collapse sidebar";
    if (btnCollapse) { btnCollapse.setAttribute("aria-label", lbl); btnCollapse.setAttribute("aria-expanded", String(!c)); }
    try { localStorage.setItem("sb-collapsed", c ? "1" : "0"); } catch (e) {}
  }

  if (btnOpen) btnOpen.addEventListener("click", function () {
    body.classList.contains("sb-open") ? closeMobile(true) : openMobile(true);
  });
  if (btnClose) btnClose.addEventListener("click", function () { closeMobile(true); });
  if (btnCollapse) btnCollapse.addEventListener("click", toggleDesktop);

  // Backdrop click closes (mobile)
  var bd = document.querySelector(".sb-backdrop");
  if (bd) bd.addEventListener("click", function () { closeMobile(true); });

  // Esc closes (mobile) or collapses (desktop)
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    if (isMobile() && body.classList.contains("sb-open")) { closeMobile(true); e.stopPropagation(); }
    else if (!isMobile() && !body.classList.contains("sb-collapsed")) { toggleDesktop(); }
  });

  // Focus trap while mobile sidebar is open
  sb.addEventListener("keydown", function (e) {
    if (e.key !== "Tab" || !isMobile() || !body.classList.contains("sb-open")) return;
    var f = sb.querySelectorAll("a,button,[tabindex]:not([tabindex='-1'])");
    if (!f.length) return;
    var first = f[0], last = f[f.length - 1];
    if (e.shiftKey && document.activeElement === first) { last.focus(); e.preventDefault(); }
    else if (!e.shiftKey && document.activeElement === last) { first.focus(); e.preventDefault(); }
  });

  // On resize: reconcile classes so we never get stuck
  var mq = window.matchMedia("(max-width: 980px)");
  function reconcile() {
    if (mq.matches) {
      // entering mobile: start closed, clear desktop collapse
      body.classList.remove("sb-collapsed");
      if (!body.classList.contains("sb-open")) sb.setAttribute("aria-hidden", "true");
      if (btnOpen) btnOpen.setAttribute("aria-expanded", String(body.classList.contains("sb-open")));
    } else {
      // entering desktop: remove mobile-open, apply saved collapse pref
      body.classList.remove("sb-open");
      var c = false;
      try { c = localStorage.getItem("sb-collapsed") === "1"; } catch (e) {}
      body.classList.toggle("sb-collapsed", c);
      sb.setAttribute("aria-hidden", c ? "true" : "false");
      if (btnCollapse) btnCollapse.setAttribute("aria-expanded", String(!c));
    }
  }
  if (mq.addEventListener) mq.addEventListener("change", reconcile); else mq.addListener(reconcile);
  reconcile();
})();
