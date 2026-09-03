/* Code Puppy — reusable popover / detail modal (WCAG 2.2 AAA-aware).
   Features: dialog roles, focus trap, Esc/backdrop close, "open in new page",
   "close", "copy link". Works with any element carrying [data-pop]. */
(function () {
  "use strict";
  var OV_ID = "bbpop-overlay";

  function buildOverlay() {
    var ov = document.createElement("div");
    ov.id = OV_ID;
    ov.className = "bbpop-overlay";
    ov.innerHTML =
      '<div class="bbpop" role="dialog" aria-modal="true" aria-labelledby="bbpop-title">' +
      '  <div class="bbpop-head">' +
      '    <span class="bbpop-k" id="bbpop-k"></span>' +
      '    <h2 class="bbpop-title" id="bbpop-title"></h2>' +
      '    <div class="bbpop-actions">' +
      '      <button type="button" class="bbpop-btn" data-pop-newtab aria-label="Open in new page">Open page</button>' +
      '      <button type="button" class="bbpop-btn ghost" data-pop-copy aria-label="Copy link">Copy link</button>' +
      '      <button type="button" class="bbpop-x" data-pop-close aria-label="Close (Esc)">&times;</button>' +
      '    </div>' +
      '  </div>' +
      '  <div class="bbpop-body" id="bbpop-body"></div>' +
      '</div>';
    ov.setAttribute("hidden", "");
    document.body.appendChild(ov);
    return ov;
  }

  var ov = null, lastFocus = null, currentKey = null, currentUrl = null, currentLabel = "";

  function focusables(root) {
    return Array.prototype.slice.call(
      root.querySelectorAll('a[href],button:not([disabled]),[tabindex]:not([tabindex="-1"]),input,select,textarea')
    ).filter(function (el) { return el.offsetParent !== null || el === document.activeElement; });
  }

  function open(key, label, html, url) {
    if (!ov) ov = buildOverlay();
    currentKey = key; currentUrl = url || null; currentLabel = label || "Detail";
    ov.querySelector("#bbpop-k").textContent = label.split(" · ")[0] || "Detail";
    ov.querySelector("#bbpop-title").textContent = label;
    ov.querySelector("#bbpop-body").innerHTML = html;
    lastFocus = document.activeElement;
    ov.removeAttribute("hidden");
    document.body.style.overflow = "hidden";
    var closeBtn = ov.querySelector("[data-pop-close]");
    if (closeBtn) closeBtn.focus();
    history.replaceState(null, "", "#detail=" + encodeURIComponent(key));
  }

  function close(restore) {
    if (!ov) return;
    ov.setAttribute("hidden", "");
    document.body.style.overflow = "";
    history.replaceState(null, "", location.pathname + location.search);
    if (restore !== false && lastFocus && lastFocus.focus) lastFocus.focus();
  }

  // events delegated once on document
  document.addEventListener("click", function (e) {
    var openNew = e.target.closest && e.target.closest("[data-pop-newtab]");
    var closeBtn = e.target.closest && e.target.closest("[data-pop-close]");
    var copyBtn = e.target.closest && e.target.closest("[data-pop-copy]");
    if (closeBtn) { close(); return; }
    if (copyBtn) {
      var link = currentUrl || (location.origin + location.pathname + "#detail=" + currentKey);
      var done = function () { copyBtn.textContent = "Copied"; setTimeout(function(){copyBtn.textContent="Copy link";},1400); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(link).then(done, done); else done();
      return;
    }
    if (openNew) {
      var dest = currentUrl || ("detail.html?d=" + encodeURIComponent(currentKey) + "&from=" + encodeURIComponent(location.pathname));
      window.open(dest, "_blank", "noopener");
      return;
    }
    // backdrop click
    if (ov && !ov.hasAttribute("hidden") && e.target === ov) { close(); return; }
    // open trigger: any element with data-pop
    var trig = e.target.closest && e.target.closest("[data-pop]");
    if (trig) {
      var key = trig.getAttribute("data-pop");
      var label = trig.getAttribute("data-pop-label") || (trig.querySelector(".n-t") ? trig.querySelector(".n-t").textContent : key);
      var url = trig.getAttribute("data-pop-url") || null;
      var payload = (window.BB_DETAIL && window.BB_DETAIL[key] && window.BB_DETAIL[key].b) ||
        (window.D && window.D[key] && window.D[key].b) || "<p>" + label + "</p>";
      open(key, label, payload, url);
    }
  });

  document.addEventListener("keydown", function (e) {
    if (!ov || ov.hasAttribute("hidden")) return;
    if (e.key === "Escape") { close(); e.stopPropagation(); return; }
    if (e.key === "Tab") {
      var f = focusables(ov);
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { last.focus(); e.preventDefault(); }
      else if (!e.shiftKey && document.activeElement === last) { first.focus(); e.preventDefault(); }
    }
  });

  // deep-link on load: #detail=<key>
  window.addEventListener("DOMContentLoaded", function () {
    var m = location.hash.match(/#detail=([^&]+)/);
    if (m) {
      var key = decodeURIComponent(m[1]);
      var trig = document.querySelector('[data-pop="' + key + '"]');
      if (trig) trig.click();
    }
  });
})();
