/* Job board: openings added by admins (Supabase) plus JOBS from config.js,
   with search, category tabs and filters, and LinkedIn searches for more. */
(async function () {
  const $ = id => document.getElementById(id), { esc, waLink } = window.SNsite;
  const A = typeof AUTH !== "undefined" ? AUTH : {};
  let jobs = (typeof JOBS !== "undefined" ? JOBS : []).filter(j => j && j.title && j.url).map(j => ({ ...j, category: j.category || "product", posted_on: j.posted_on || j.posted || "" }));
  if (A.supabaseUrl && A.supabaseKey && !/^sb_secret_/.test(A.supabaseKey)) {
    try {
      const r = await fetch(A.supabaseUrl.replace(/\/$/, "") + "/rest/v1/jobs?select=*&active=eq.true&order=posted_on.desc", { headers: { apikey: A.supabaseKey, ...(A.supabaseKey.startsWith("sb_") ? {} : { Authorization: "Bearer " + A.supabaseKey }) } });
      if (r.ok) jobs = jobs.concat(await r.json());
    } catch {}
  }
  jobs.sort((a, b) => String(b.posted_on).localeCompare(String(a.posted_on)));

  const CATS = [["product", "Product"], ["ai", "AI"], ["engineering", "Engineering"]];
  let cat = new URLSearchParams(location.search).get("c") || "product";
  if (!CATS.some(c => c[0] === cat)) cat = "product";
  $("job-tabs").innerHTML = CATS.map(([v, t]) => `<button type="button" data-c="${v}" aria-pressed="${v === cat}">${t}</button>`).join("");
  const locs = [...new Set(jobs.map(j => (j.location || "").split(",")[0].trim()).filter(Boolean))].sort();
  $("job-loc").innerHTML = '<option value="">Location</option>' + locs.map(l => `<option>${esc(l)}</option>`).join("");
  const exps = [...new Set(jobs.map(j => j.experience).filter(Boolean))];
  $("job-exp").innerHTML = '<option value="">Experience</option>' + exps.map(x => `<option>${esc(x)}</option>`).join("");

  const LI = { product: "Product Manager", ai: "AI Product Manager", engineering: "AI Engineer" };
  const liUrl = (kw, extra = "") => "https://www.linkedin.com/jobs/search/?keywords=" + encodeURIComponent(kw) + "&location=India&f_TPR=r604800" + extra;
  const days = d => { const n = Math.floor((Date.now() - new Date(d)) / 864e5); return isNaN(n) ? "" : n <= 0 ? "Posted today" : n === 1 ? "Posted 1 day ago" : n < 7 ? `Posted ${n} days ago` : "Posted on " + new Date(d).toLocaleDateString("en-IN", { day: "numeric", month: "short" }); };
  const PIN = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>';
  const CLK = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>';

  function render() {
    const q = $("job-q").value.trim().toLowerCase(), loc = $("job-loc").value, exp = $("job-exp").value;
    const rows = jobs.filter(j => j.category === cat && (!q || [j.title, j.company, j.location, j.experience].join(" ").toLowerCase().includes(q)) && (!loc || (j.location || "").startsWith(loc)) && (!exp || j.experience === exp));
    $("job-count").textContent = rows.length ? `${rows.length} opening${rows.length > 1 ? "s" : ""} we've spotted` : "Openings";
    const fresh = d => (Date.now() - new Date(d)) / 864e5 < 3;
    $("job-list").innerHTML = rows.map(j => `<a class="job card" href="${esc(/^https?:/i.test(j.url) ? j.url : "#")}" target="_blank" rel="noopener noreferrer">
      ${fresh(j.posted_on) ? '<span class="new">NEW ✦</span>' : ""}
      <div class="jh">${j.logo ? `<img src="${esc(j.logo)}" alt="" width="44" height="44" loading="lazy">` : `<span class="lg">${esc((j.company || "?").trim()[0])}</span>`}<span><b>${esc(j.company)}</b><small>${esc(days(j.posted_on))}</small></span></div>
      <h3>${esc(j.title)}</h3>
      <div class="jm">${j.location ? `<span>${PIN}${esc(j.location)}</span>` : ""}<span>${CLK}${esc(j.job_type || "Full time")}${j.experience ? " · " + esc(j.experience) : ""}</span></div></a>`).join("")
      + `<a class="job card more" href="${esc(liUrl(LI[cat]))}" target="_blank" rel="noopener noreferrer"><h3>See the latest ${esc(LI[cat])} jobs on LinkedIn ↗</h3><p class="meta">Posted in the last 7 days, across India.</p></a>`;
    $("job-empty").hidden = rows.length > 0;
  }
  $("job-tabs").addEventListener("click", e => { const b = e.target.closest("button"); if (!b) return; cat = b.dataset.c; $("job-tabs").querySelectorAll("button").forEach(x => x.setAttribute("aria-pressed", x === b)); render(); });
  ["job-q", "job-loc", "job-exp"].forEach(id => $(id).addEventListener("input", render));

  // Quick LinkedIn searches
  const SEARCHES = [["Product Manager", ""], ["Associate Product Manager", ""], ["AI Product Manager", ""], ["Senior Product Manager", ""], ["Product Analyst", ""], ["Technical Product Manager", ""], ["AI Engineer", ""], ["Machine Learning Engineer", ""], ["Generative AI", ""], ["Product Manager (remote)", "&f_WT=2"]];
  $("li-searches").innerHTML = SEARCHES.map(([k, x]) => `<a href="${esc(liUrl(k.replace(" (remote)", ""), x))}" target="_blank" rel="noopener noreferrer">${esc(k)} ↗</a>`).join("");
  $("job-alerts").href = waLink("Hi SkillNavora, please send me updates about new PM and AI job openings.");
  render();
})();
