/* Code Puppy — app-shell injector (shared).
   Renders the collapsible sidebar + mobile topbar around existing content
   WITHOUT requiring each page to hand-maintain nav markup.
   Requires: assets/tokens.css, assets/sidebar.css, assets/sidebar.js loaded;
   icons.js first.

   Configuration (set BEFORE loading this file):
     window.BB_SHELL = { base:"../", active:"hub", assetsBase:"../assets/" }
*/
(function () {
  "use strict";
  var cfg = window.BB_SHELL || {};
  var base = cfg.base || "./";
  var active = cfg.active || "";
  var assets = cfg.assetsBase || base + "assets/";
  var I = window.BB && window.BB.icon ? window.BB.icon : function () { return ""; };

  var NAV = [
    { key: "hub",          href: base + "index.html",    label: "Hub",           icon: "hub" },
    { key: "field-guide",  href: base + "field-guide/",  label: "Field Guide",   icon: "book" },
    { key: "releases",     href: base + "releases/",     label: "Releases",      icon: "activity" },
    { key: "architecture", href: base + "architecture/", label: "Architecture",  icon: "grid" },
    { key: "design",       href: base + "design/",       label: "Design System", icon: "swatch" },
    { key: "flat",         href: base + "flat/",         label: "Flat Docs",     icon: "file" }
  ];
  var account = { href: "https://github.com/t-granlund/code_puppy", icon: "github" };

  function navLink(item) {
    var on = item.key === active;
    return '<li><a class="sb-link' + (on ? " active" : "") + '" href="' + item.href + '"' +
      (on ? ' aria-current="page"' : "") + ">" +
      '<span class="ic">' + I(item.icon, 19) + "</span>" +
      '<span class="lbl">' + item.label + "</span></a></li>";
  }

  var logo = '<img src="' + assets + 'code_puppy_logo_white.png" alt="Code Puppy logo" width="30" height="30" />';

  var sidebar =
    '<aside class="sb" aria-label="Primary navigation">' +
    '  <div class="sb-head">' +
    '    <a class="brand" href="' + base + 'index.html">' + logo + '<span class="t">Code Puppy</span></a>' +
    '    <button class="sb-toggle" type="button" data-sb-collapse aria-label="Collapse sidebar" aria-expanded="true" title="Collapse sidebar">' + I("menu", 16) + "</button>" +
    '    <button class="sb-toggle sb-close" type="button" data-sb-close aria-label="Close navigation">' + I("x", 16) + "</button>" +
    "  </div>" +
    '  <nav class="sb-nav" aria-label="Site sections">' +
    '    <div class="sb-sec">Explore</div>' +
    '    <ul class="sb-list">' + NAV.map(navLink).join("") + "</ul>" +
    "  </nav>" +
    '  <div class="sb-foot">' +
    '    <div class="meta">public mirror<br/>fork build</div>' +
    '    <a class="gh" href="' + account.href + '" target="_blank" rel="noopener">' + I("github", 16) + "<span>GitHub</span></a>" +
    "  </div>" +
    "</aside>";

  var backdrop = '<div class="sb-backdrop" aria-hidden="true"></div>';

  var topbar =
    '<header class="sb-topbar">' +
    '  <button class="sb-burger" type="button" aria-label="Open navigation" aria-expanded="false">' + I("menu", 20) + "</button>" +
    '  <a class="brand" href="' + base + 'index.html"><img src="' + assets + 'code_puppy_logo_white.png" alt="Code Puppy logo" width="26" height="26" /><span>Code Puppy</span></a>' +
    '  <span class="spacer"></span>' +
    '  <a class="sb-link" style="padding:8px 11px" href="' + account.href + '" target="_blank" rel="noopener" aria-label="GitHub repository">' + I("github", 16) + '<span class="lbl">GitHub</span></a>' +
    "</header>";

  // Build the shell
  var shell = document.createElement("div");
  shell.className = "sb-shell";

  var main = document.createElement("div");
  main.className = "sb-main";
  main.id = "sb-main";
  main.setAttribute("role", "main");

  var skip = document.createElement("a");
  skip.className = "sb-skip";
  skip.href = "#sb-main";
  skip.textContent = "Skip to content";

  // move existing body children into main
  while (document.body.firstChild) main.appendChild(document.body.firstChild);

  // hide any legacy top navs inside main
  var legacy = main.querySelectorAll(".nav");
  for (var i = 0; i < legacy.length; i++) legacy[i].classList.add("sb-legacy-topnav");

  main.insertAdjacentHTML("afterbegin", topbar);
  shell.insertAdjacentHTML("beforeend", sidebar + backdrop);

  document.body.innerHTML = "";
  document.body.appendChild(skip);
  document.body.appendChild(shell);
  shell.appendChild(main);
})();
