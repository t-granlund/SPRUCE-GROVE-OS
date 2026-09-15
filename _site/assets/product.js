/* ==================================================================
   Spruce Grove OS — product page mechanics.
   Five self-contained, replayable demo machines. Every button does
   something. Event vocabulary mirrors the real ACP dialect
   (chunk / thought / tool / turn-end) and the desktop shell's
   steering + durability behavior. Zero dependencies.
   ================================================================== */
(function () {
  "use strict";

  var $ = function (id) { return document.getElementById(id); };
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------------- toast + copy (house style: one behavior) ------- */
  var toastTimer = null;
  function toast(msg) {
    var t = $("toast");
    t.textContent = msg;
    t.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { t.classList.remove("show"); }, 1900);
  }
  window.__copyCmd = function (id) {
    var text = $(id).textContent.trim();
    var done = function () { toast("copied — it's yours now"); };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, done);
    } else {
      var ta = document.createElement("textarea");
      ta.value = text; document.body.appendChild(ta); ta.select();
      try { document.execCommand("copy"); } catch (e) { /* noop */ }
      ta.remove(); done();
    }
  };

  /* --------------- helpers: typed lines + transcript ---------------- */
  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text !== undefined) e.textContent = text;
    return e;
  }
  function transcriptOf(termId) {
    var t = $(termId);
    t.innerHTML = "";
    return {
      node: t,
      add: function (cls, who, line) {
        var m = el("div", "msg " + cls);
        m.appendChild(el("div", "who", who));
        var l = el("div", "line", line || "");
        m.appendChild(l);
        t.appendChild(m);
        t.scrollTop = t.scrollHeight;
        return l;
      },
      tool: function (title) {
        var m = el("div", "msg tool");
        var row = el("div", "row");
        row.appendChild(el("span", "tt", title));
        var chip = el("span", "chip running", "running");
        row.appendChild(chip);
        m.appendChild(row);
        t.appendChild(m);
        t.scrollTop = t.scrollHeight;
        return {
          done: function () { chip.className = "chip done"; chip.textContent = "done"; t.scrollTop = t.scrollHeight; },
          fail: function () { chip.className = "chip fail"; chip.textContent = "failed"; t.scrollTop = t.scrollHeight; }
        };
      }
    };
  }
  function typeInto(node, text, cps, cb) {
    if (reduced) { node.textContent += text; node.classList.remove("caret"); cb && cb(); return; }
    var i = 0;
    node.classList.add("caret");
    (function tick() {
      var step = Math.max(1, Math.round(text.length / 46));
      node.textContent += text.slice(i, i + step);
      i += step;
      node.closest(".term").scrollTop = 1e9;
      if (i < text.length) { setTimeout(tick, 1000 / cps); }
      else { node.classList.remove("caret"); cb && cb(); }
    })(0);
  }
  function setState(id, text, cls) {
    var s = $(id);
    s.textContent = text;
    s.className = "state" + (cls ? " " + cls : "");
  }

  /* ============ MACHINE 1 — the streaming ACP session ============== */
  var m1Busy = false;
  window.__runM1 = function () {
    if (m1Busy) return;
    m1Busy = true;
    setState("m1state", "ACP · streaming", "busy");
    var T = transcriptOf("m1term");
    var chain = [
      function () { T.add("user", "you", "Add a /rec verb to the mockingbird plugin — voice goes in, transcript comes out, review before send."); setTimeout(chain[1], 250); },
      function () {
        var l = T.add("think", "cedar · thinking", "");
        typeInto(l, "The plugin tier already exists under user-plugins — no core edits. The verb plugs into cli_transcribe; whisper runs on-device, so the review step stays in the user's hands.", 130, function () { setTimeout(chain[2], 120); });
      },
      function () {
        var tc = T.tool("write_file · user-plugins/mockingbird/cli_transcribe.py");
        setTimeout(function () { tc.done(); chain[3](); }, 900);
      },
      function () {
        var tc = T.tool("run_tests · 363 files");
        setTimeout(function () { tc.done(); chain[4](); }, 1100);
      },
      function () {
        var l = T.add("agent", "grove · syn:large:text", "");
        typeInto(l, "Done. /rec records from your mic, transcribes locally, drops the transcript in the prompt for review — nothing sends until you send it. 363 tests green.", 150, function () {
          setTimeout(chain[5], 150);
        });
      },
      function () {
        setState("m1state", "done · 4,321 tok");
        m1Busy = false;
      }
    ];
    chain[0]();
  };

  /* ============ MACHINE 2 — the voice loop ========================= */
  var m2Busy = false;
  var WAVE_N = 26;
  var waveEls = [];
  (function initWave() {
    var w = $("m2wave");
    for (var i = 0; i < WAVE_N; i++) { waveEls.push(w.appendChild(document.createElement("i"))); }
  })();
  var m2Timer = null;
  function wave(on) {
    clearInterval(m2Timer);
    if (!on) { waveEls.forEach(function (b) { b.style.height = "6px"; }); $("m2wave").classList.remove("on"); return; }
    $("m2wave").classList.add("on");
    m2Timer = setInterval(function () {
      waveEls.forEach(function (b) {
        b.style.height = (reduced ? 18 : 6 + Math.round(Math.random() * 38)) + "px";
      });
    }, 90);
  }
  window.__toggleMic = function () {
    if (m2Busy) return;
    m2Busy = true;
    var mic = $("m2mic"), st = $("m2state"), draft = $("m2draft");
    mic.classList.add("rec");
    setState("m2state2", "recording · on-device", "busy");
    st.textContent = "listening — speak the feature";
    wave(true);
    setTimeout(function () {
      wave(false);
      mic.classList.remove("rec");
      st.textContent = "transcribing locally (whisper)…";
      setTimeout(function () {
        var phrase = "\u201CAdd a voice note that prepends today's date to any prompt.\u201D";
        var i = 0;
        draft.innerHTML = "";
        var span = el("span", "editable");
        draft.appendChild(span);
        draft.appendChild(el("span", "hint", "  \u2190 editable before it ever sends"));
        (function tick() {
          span.textContent = phrase.slice(0, ++i);
          if (i < phrase.length) { setTimeout(tick, 22); }
          else {
            st.textContent = "review, then send — your words, your gate";
            setState("m2state2", "transcript ready · not sent", "");
            m2Busy = false;
            draft.contentEditable = "true";
            draft.focus();
          }
        })();
      }, 1100);
    }, 2400);
  };

  /* ============ MACHINE 3 — mid-run steering ======================= */
  var m3Busy = false;
  window.__runM3 = function () {
    if (m3Busy) return;
    m3Busy = true;
    setState("m3state", "ACP · streaming", "busy");
    $("m3go").disabled = true;
    var T = transcriptOf("m3term");
    T.add("user", "you", "Sweep the whole test suite and fix any flaky timing asserts.");
    setTimeout(function () {
      var tc = T.tool("run_tests · 363 files · 2m ETA");
      $("m3input").focus();
      T.node.scrollTop = 1e9;
      /* wait for the human steer */
      window.__m3Steer = function (text) {
        if (!text) return;
        window.__m3Steer = null;
        var l = T.add("steer", "steer · queued", "\u201C" + text + "\u201D");
        setState("m3state", "steer queued — redirecting Cedar…", "busy");
        setTimeout(function () {
          tc.done();
          l.querySelector(".who").textContent = "steer · redirected in-session";
          var l2 = T.add("think", "cedar · thinking", "");
          typeInto(l2, "Cancel received mid-turn. Context preserved — same session, new heading: " + text, 140, function () {
            var l3 = T.add("agent", "grove", "");
            typeInto(l3, "Redirected. Picking up from where the turn actually was — nothing lost.", 150, function () {
              setState("m3state", "done · same session, new heading");
              $("m3go").disabled = false;
              m3Busy = false;
            });
          });
        }, 900);
      };
    }, 700);
  };
  window.__steerSend = function () {
    var input = $("m3input");
    var v = input.value.trim();
    if (!v) return;
    input.value = "";
    if (window.__m3Steer) { window.__m3Steer(v); }
    else { toast("start the sweep first — then steer mid-run"); }
  };

  /* ============ MACHINE 4 — live look-in =========================== */
  var m4Busy = false;
  window.__runM4 = function () {
    if (m4Busy) return;
    m4Busy = true;
    setState("m4state", "browsing · live", "busy");
    var log = $("m4log");
    log.innerHTML = "";
    var cursor = $("m4cursor");
    var flash = $("m4flash");
    function stepLog(txt, hot) {
      var d = el("div", hot ? "hot" : "", txt);
      log.appendChild(d);
      log.scrollTop = 1e9;
    }
    function moveCursor(x, y, t, cb) {
      cursor.style.left = x + "%"; cursor.style.top = y + "%";
      setTimeout(cb, t);
    }
    stepLog("navigate · demo checkout page", true);
    moveCursor(50, 58, 900, function () {
      stepLog("fill · input#email");
      $("m4f1").style.borderColor = "#E4AA71";
      moveCursor(46, 72, 700, function () {
        stepLog("click · button.place-order");
        $("m4btn").style.background = "#98B79E";
        moveCursor(50, 84, 800, function () {
          stepLog("click · take_screenshot");
          flash.classList.add("go");
          setTimeout(function () {
            flash.classList.remove("go");
            stepLog("screenshot captured \u2192 look-in panel", true);
            var ph = $("m4ph");
            var img = el("img");
            img.alt = "simulated checkout screenshot";
            var cv = document.createElement("canvas");
            cv.width = 640; cv.height = 400;
            var cx = cv.getContext("2d");
            cx.fillStyle = "#FBF9F4"; cx.fillRect(0, 0, 640, 400);
            cx.fillStyle = "#1D3A2A"; cx.fillRect(0, 0, 640, 54);
            cx.fillStyle = "#F2EFE6"; cx.font = "600 20px sans-serif";
            cx.fillText("Cedar Lane Supply \u2014 order confirmed", 24, 34);
            cx.fillStyle = "#5b6459"; cx.font = "14px monospace";
            cx.fillText("order  #SG-0417", 24, 92);
            cx.fillText("item   voice-note-plugin ........... $0", 24, 118);
            cx.fillText("item   steered mid-run .............. $0", 24, 140);
            cx.fillText("total  paid in tokens, not dollars", 24, 170);
            cx.strokeStyle = "#DDD6C8"; cx.strokeRect(14, 66, 612, 130);
            cx.fillStyle = "#98B79E"; cx.font = "600 16px sans-serif";
            cx.fillText("placed by the agent, watched live", 30, 250);
            img.src = cv.toDataURL("image/png");
            ph.replaceWith(img);
            setState("m4state", "screenshot streamed to panel");
            m4Busy = false;
          }, 650);
        });
      });
    });
  };

  /* ============ MACHINE 5 — the durability kill test ================ */
  var m5Busy = false;
  window.__runM5 = function () {
    if (m5Busy) return;
    m5Busy = true;
    var dead = $("m5dead");
    dead.classList.add("dead");
    $("m5deadState").textContent = "process dead";
    $("m5deadState").className = "pill-s";
    $("m5deadMarker").textContent = "\u2014";
    setState("m5state", "SIGKILL · agent process terminated", "dead");
    $("m5kill").disabled = true;
    setTimeout(function () {
      setState("m5state", "relaunch · session/load …", "busy");
      dead.classList.remove("dead");
      $("m5deadState").textContent = "loading session";
      setTimeout(function () {
        $("m5deadState").textContent = "session restored";
        $("m5deadState").className = "pill-s";
        var i = 0, target = "GROVE-DURABILITY-082318";
        (function tick() {
          $("m5deadMarker").textContent = target.slice(0, ++i);
          if (i < target.length) { setTimeout(tick, 34); }
          else {
            setState("m5state", "marker recalled · context intact");
            $("m5kill").disabled = false;
            m5Busy = false;
          }
        })();
      }, 1300);
    }, 1500);
  };

  /* ---------------- counters (spec band) + reveal ------------------- */
  function counters() {
    var els = document.querySelectorAll("[data-count]");
    Array.prototype.forEach.call(els, function (e) {
      if (e.dataset.done) return;
      var r = e.getBoundingClientRect();
      if (r.top > window.innerHeight - 40) return;
      e.dataset.done = "1";
      var target = parseFloat(e.dataset.count);
      var suffix = e.dataset.suffix || "";
      if (reduced) { e.textContent = target.toLocaleString() + suffix; return; }
      var t0 = null;
      function frame(ts) {
        if (!t0) t0 = ts;
        var p = Math.min(1, (ts - t0) / 1100);
        p = 1 - Math.pow(1 - p, 3);
        e.textContent = Math.round(target * p).toLocaleString() + (p === 1 ? suffix : "");
        if (p < 1) requestAnimationFrame(frame);
      }
      requestAnimationFrame(frame);
    });
  }
  window.addEventListener("scroll", counters, { passive: true });
  counters();

  /* enter key sends the steer */
  var si = $("m3input");
  if (si) si.addEventListener("keydown", function (ev) {
    if (ev.key === "Enter") { ev.preventDefault(); window.__steerSend(); }
  });
})();
