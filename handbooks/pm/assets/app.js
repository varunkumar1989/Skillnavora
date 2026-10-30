/* PM Master Handbook — interactivity. No network access required; works from file://. */
(function () {
  'use strict';
  var KEY = 'pmh.progress.v1';
  var root = document.documentElement;

  function load() { try { return JSON.parse(localStorage.getItem(KEY)) || { modules: {} }; } catch (e) { return { modules: {} }; } }
  function save(p) { try { localStorage.setItem(KEY, JSON.stringify(p)); } catch (e) { /* storage may be blocked */ } }
  var progress = load();

  /* ---------- theme ---------- */
  function applyTheme(t) { if (t) root.setAttribute('data-theme', t); else root.removeAttribute('data-theme'); }
  try { applyTheme(localStorage.getItem('pmh.theme')); } catch (e) {}
  var themeBtn = document.getElementById('themeBtn');
  function isDark() {
    var t = root.getAttribute('data-theme');
    return t ? t === 'dark' : window.matchMedia && matchMedia('(prefers-color-scheme: dark)').matches;
  }
  function paintThemeBtn() { if (themeBtn) { themeBtn.textContent = isDark() ? '☀ Light' : '☾ Dark'; themeBtn.setAttribute('aria-pressed', isDark()); } }
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var next = isDark() ? 'light' : 'dark';
      applyTheme(next);
      try { localStorage.setItem('pmh.theme', next); } catch (e) {}
      paintThemeBtn();
    });
    paintThemeBtn();
  }

  /* ---------- sidebar (mobile) ---------- */
  var sb = document.getElementById('sidebar'), mt = document.getElementById('menuBtn');
  if (mt && sb) {
    mt.addEventListener('click', function () { var o = sb.classList.toggle('open'); mt.setAttribute('aria-expanded', o); });
    sb.addEventListener('click', function (e) { if (e.target.closest('a')) { sb.classList.remove('open'); mt.setAttribute('aria-expanded', false); } });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && sb.classList.contains('open')) { sb.classList.remove('open'); mt.setAttribute('aria-expanded', false); mt.focus(); } });
  }

  /* ---------- back to top ---------- */
  var top = document.getElementById('toTop');
  if (top) {
    window.addEventListener('scroll', function () { top.classList.toggle('on', window.scrollY > 600); }, { passive: true });
    top.addEventListener('click', function () { window.scrollTo({ top: 0 }); });
  }

  /* ---------- progress indicators ---------- */
  function paintProgress() {
    document.querySelectorAll('[data-mod-link]').forEach(function (a) {
      var m = progress.modules[a.getAttribute('data-mod-link')];
      a.classList.toggle('done', !!(m && m.done));
    });
    var done = 0, total = (window.PMH && PMH.modules.length) || 12;
    Object.keys(progress.modules).forEach(function (k) { if (progress.modules[k].done) done++; });
    document.querySelectorAll('[data-overall]').forEach(function (el) { el.textContent = done + ' / ' + total; });
    document.querySelectorAll('[data-overall-bar]').forEach(function (el) { el.style.width = (100 * done / total) + '%'; });
  }
  var doneBtn = document.getElementById('doneBtn');
  if (doneBtn) {
    var mid = doneBtn.getAttribute('data-mod');
    var paintBtn = function () {
      var d = !!(progress.modules[mid] && progress.modules[mid].done);
      doneBtn.setAttribute('aria-pressed', d);
      doneBtn.textContent = d ? '✓ Module completed' : 'Mark module complete';
    };
    doneBtn.addEventListener('click', function () {
      var m = progress.modules[mid] = progress.modules[mid] || {};
      m.done = !m.done; save(progress); paintBtn(); paintProgress();
    });
    paintBtn();
  }
  paintProgress();

  /* ---------- quizzes ---------- */
  document.querySelectorAll('.quiz').forEach(function (qz) {
    var items = qz.querySelectorAll('.qitem');
    var score = qz.querySelector('.quizscore');
    var mid = qz.getAttribute('data-quiz');
    var answered = {};
    function update() {
      var n = Object.keys(answered).length, right = 0;
      Object.keys(answered).forEach(function (k) { if (answered[k]) right++; });
      score.textContent = n ? ('Score: ' + right + ' / ' + items.length + (n === items.length ? ' — complete' : ' (' + n + ' answered)')) : '';
      if (n === items.length && mid) {
        var m = progress.modules[mid] = progress.modules[mid] || {};
        m.quiz = { score: right, total: items.length }; save(progress);
      }
    }
    items.forEach(function (it, qi) {
      var correct = parseInt(it.getAttribute('data-correct'), 10);
      var lis = it.querySelectorAll('li');
      lis.forEach(function (li, i) {
        li.tabIndex = 0;
        li.setAttribute('role', 'button');
        var pick = function () {
          if (it.classList.contains('answered')) return;
          it.classList.add('answered');
          li.classList.add(i === correct ? 'right' : 'wrong');
          if (i !== correct) lis[correct].classList.add('right');
          answered[qi] = (i === correct);
          update();
        };
        li.addEventListener('click', pick);
        li.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); pick(); } });
      });
    });
    var reset = qz.querySelector('.quizreset');
    if (reset) reset.addEventListener('click', function () {
      answered = {};
      items.forEach(function (it) { it.classList.remove('answered'); it.querySelectorAll('li').forEach(function (l) { l.classList.remove('right', 'wrong'); }); });
      update();
    });
  });

  /* ---------- collection filters ---------- */
  var filt = document.querySelector('.filters[data-for]');
  if (filt) {
    var items = document.querySelectorAll('.item[data-cat]');
    var q = document.getElementById('collFilterText');
    var cur = 'all';
    var apply = function () {
      var t = q ? q.value.trim().toLowerCase() : '';
      items.forEach(function (it) {
        var okc = cur === 'all' || it.getAttribute('data-cat').split('|').indexOf(cur) > -1;
        var okt = !t || it.textContent.toLowerCase().indexOf(t) > -1;
        it.classList.toggle('hide', !(okc && okt));
      });
    };
    filt.querySelectorAll('button').forEach(function (b) {
      b.addEventListener('click', function () {
        cur = b.getAttribute('data-f');
        filt.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', x === b); });
        apply();
      });
    });
    if (q) q.addEventListener('input', apply);
  }
  var expand = document.getElementById('expandAll');
  if (expand) expand.addEventListener('click', function () {
    var open = expand.getAttribute('data-open') !== '1';
    document.querySelectorAll('.article details').forEach(function (d) { d.open = open; });
    expand.setAttribute('data-open', open ? '1' : '0');
    expand.textContent = open ? 'Collapse all' : 'Expand all';
  });

  /* ---------- glossary filter ---------- */
  var gf = document.getElementById('glossFilter');
  if (gf) gf.addEventListener('input', function () {
    var t = gf.value.trim().toLowerCase();
    document.querySelectorAll('.glossary .term').forEach(function (el) { el.classList.toggle('hide', t && el.textContent.toLowerCase().indexOf(t) < 0); });
  });

  /* ---------- global search ---------- */
  var inp = document.getElementById('q'), res = document.getElementById('results');
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function doSearch() {
    var raw = inp.value.trim().toLowerCase();
    if (raw.length < 2 || !window.PMH) { res.classList.remove('on'); return; }
    var terms = raw.split(/\s+/);
    var hits = [];
    PMH.index.forEach(function (d) {
      var score = 0, hay = d.x.toLowerCase(), head = d.h.toLowerCase(), page = d.p.toLowerCase();
      for (var i = 0; i < terms.length; i++) {
        var t = terms[i], s = 0;
        if (head.indexOf(t) > -1) s += 8;
        if (page.indexOf(t) > -1) s += 2;
        if (hay.indexOf(t) > -1) s += 1;
        if (!s) { score = 0; break; }
        score += s;
      }
      if (score) hits.push([score, d]);
    });
    hits.sort(function (a, b) { return b[0] - a[0]; });
    hits = hits.slice(0, 12);
    if (!hits.length) { res.innerHTML = '<a href="#" tabindex="-1"><small>No matches for “' + esc(raw) + '”.</small></a>'; res.classList.add('on'); return; }
    var re = new RegExp('(' + terms.map(function (t) { return t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }).join('|') + ')', 'ig');
    res.innerHTML = hits.map(function (h) {
      var d = h[1], i = d.x.toLowerCase().indexOf(terms[0]);
      var snip = d.x.substr(Math.max(0, i - 40), 150);
      return '<a href="' + d.u + '"><strong>' + esc(d.h).replace(re, '<mark>$1</mark>') + '</strong><small>' + esc(d.p) + ' — ' + esc(snip).replace(re, '<mark>$1</mark>') + '…</small></a>';
    }).join('');
    res.classList.add('on');
  }
  if (inp && res) {
    inp.addEventListener('input', doSearch);
    inp.addEventListener('focus', doSearch);
    inp.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { res.classList.remove('on'); inp.blur(); }
      if (e.key === 'ArrowDown') { var a = res.querySelector('a'); if (a) { e.preventDefault(); a.focus(); } }
    });
    res.addEventListener('keydown', function (e) {
      var a = document.activeElement;
      if (e.key === 'ArrowDown' && a.nextElementSibling) { e.preventDefault(); a.nextElementSibling.focus(); }
      if (e.key === 'ArrowUp') { e.preventDefault(); (a.previousElementSibling || inp).focus(); }
      if (e.key === 'Escape') { res.classList.remove('on'); inp.focus(); }
    });
    document.addEventListener('click', function (e) { if (!e.target.closest('.searchbox')) res.classList.remove('on'); });
    document.addEventListener('keydown', function (e) {
      if (e.key === '/' && !/INPUT|TEXTAREA/.test(document.activeElement.tagName)) { e.preventDefault(); inp.focus(); }
    });
  }

  /* ---------- dashboard ---------- */
  var dash = document.getElementById('dashModules');
  if (dash && window.PMH) {
    var firstOpen = null;
    dash.innerHTML = PMH.modules.map(function (m) {
      var st = progress.modules[m.id] || {};
      var status = st.done ? 'Completed' : (st.quiz ? 'In progress' : 'Not started');
      if (!st.done && !firstOpen) firstOpen = m;
      var q = st.quiz ? ' · quiz ' + st.quiz.score + '/' + st.quiz.total : '';
      return '<a class="card" href="' + m.url + '"><span class="tag">Module ' + m.n + '</span><h3>' + esc(m.title) + '</h3><p>' + esc(m.summary) + '</p>' +
        '<div class="progressbar" aria-hidden="true" style="margin-top:10px"><i style="width:' + (st.done ? 100 : (st.quiz ? 50 : 0)) + '%"></i></div>' +
        '<div class="meta">' + status + q + ' · ≈ ' + m.hours + ' h study' + (m.status !== 'complete' ? ' · <b>' + esc(m.status) + '</b>' : '') + '</div></a>';
    }).join('');
    var focus = document.getElementById('currentFocus');
    if (focus) focus.innerHTML = firstOpen ? 'Current focus: <a href="' + firstOpen.url + '">Module ' + firstOpen.n + ' — ' + esc(firstOpen.title) + '</a>' : 'All modules marked complete.';
    var tot = document.getElementById('totalHours');
    if (tot) tot.textContent = PMH.modules.reduce(function (a, m) { return a + m.hours; }, 0) + ' h';
  }
  document.querySelectorAll('[data-reset-progress]').forEach(function (b) {
    b.addEventListener('click', function () { if (confirm('Clear saved progress on this device?')) { progress = { modules: {} }; save(progress); location.reload(); } });
  });
})();
