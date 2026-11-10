/* In-site document reader (read.html?doc=...): shows one PDF inside the page with Back, Previous and Next.
   The document list comes from assets/reader-groups.json (built by tools/reader.py). */
(function () {
  const $ = id => document.getElementById(id);
  const root = document.body.dataset.root || "";
  const qs = new URLSearchParams(location.search);
  const doc = qs.get("doc") || "";
  // Optional starting page (read.html?doc=...&page=12): opens the PDF at that chapter.
  const pg = /^[1-9]\d{0,3}$/.test(qs.get("page") || "") ? qs.get("page") : "";
  const frame = $("rd-frame"), title = $("rd-title"), prev = $("rd-prev"), next = $("rd-next"), back = $("rd-back"), open = $("rd-open"), pos = $("rd-pos");
  const safe = /^(handbook|classes|brochures|data-science\/pdf)\/[^?#]+\.pdf$/i.test(doc) && !doc.includes("..");
  const go = p => { location.href = root + "read.html?doc=" + encodeURIComponent(p); };

  // Back: the previous page on this site if there is one; otherwise the resources hub.
  back.addEventListener("click", e => {
    let same = false; try { same = !!document.referrer && new URL(document.referrer).origin === location.origin; } catch {}
    if (same && history.length > 1) { e.preventDefault(); history.back(); }
  });

  fetch(root + "assets/reader-groups.json").then(r => r.json()).then(G => {
    if (!safe || !G.of[doc]) { title.textContent = "This document is not available here."; frame.hidden = true; prev.hidden = next.hidden = true; return; }
    const list = G.groups[G.of[doc]] || [], i = list.indexOf(doc);
    title.textContent = decodeURIComponent(doc.split("/").pop()).replace(/\.pdf$/i, "").replace(/[-_]+/g, " ");
    document.title = title.textContent + " · SkillNavora";
    frame.src = root + doc + (pg ? "#page=" + pg : ""); open.href = root + doc + (pg ? "#page=" + pg : "");
    if (pg) title.textContent += " · page " + pg;
    if (i > 0) { prev.hidden = false; prev.onclick = e => { e.preventDefault(); go(list[i - 1]); }; } else prev.hidden = true;
    if (i >= 0 && i < list.length - 1) { next.hidden = false; next.onclick = e => { e.preventDefault(); go(list[i + 1]); }; } else next.hidden = true;
    pos.textContent = i >= 0 ? (i + 1) + " of " + list.length : "";
    // Keyboard arrows move between documents in the same group.
    document.addEventListener("keydown", e => {
      if (e.target.closest && e.target.closest("input,textarea,select")) return;
      if (e.key === "ArrowLeft" && i > 0) go(list[i - 1]);
      if (e.key === "ArrowRight" && i < list.length - 1) go(list[i + 1]);
    });
  }).catch(() => { title.textContent = "The document list could not be loaded. Please try again."; frame.hidden = true; });
})();
