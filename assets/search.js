/* Site search: finds public pages by title and description, using assets/search-index.json (built by tools/gen_site.py). */
(function () {
  const box = document.getElementById("sn-q");
  const out = document.getElementById("sn-results");
  const count = document.getElementById("sn-count");
  if (!box || !out) return;
  const esc = s => String(s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const root = document.body.dataset.root || "";
  let index = null;

  function render() {
    const words = box.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
    if (!index) return;
    if (!words.length) {
      count.textContent = "Type a topic, program, tool or page name.";
      out.innerHTML = "";
      return;
    }
    const hits = index
      .filter(it => { const hay = (it.t + " " + it.d).toLowerCase(); return words.every(w => hay.includes(w)); })
      .map(it => ({ it, score: words.reduce((n, w) => n + (it.t.toLowerCase().includes(w) ? 2 : 0), 0) }))
      .sort((a, b) => b.score - a.score || a.it.t.localeCompare(b.it.t))
      .map(x => x.it);
    count.textContent = hits.length ? hits.length + (hits.length === 1 ? " page found" : " pages found") : "No pages match. Try a shorter word, or ask us on WhatsApp.";
    out.innerHTML = hits.map(it => `<a class="sn-hit" href="${esc(it.u)}"><b>${esc(it.t)}</b><span>${esc(it.d)}</span></a>`).join("");
  }

  box.value = new URLSearchParams(location.search).get("q") || "";
  box.addEventListener("input", render);
  fetch(root + "assets/search-index.json")
    .then(r => { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(j => { index = j; render(); })
    .catch(() => { count.textContent = "Search is unavailable right now. Use the menu above to browse."; });
})();
