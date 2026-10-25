/* Shared behaviour for every page. Settings live in assets/config.js. */
(function () {
  const S = typeof SITE !== "undefined" ? SITE : {};
  const C = typeof COURSES !== "undefined" ? COURSES : [];
  const $ = id => document.getElementById(id);
  const R = document.body.dataset.root || "";            // "" or "../" for pages in sub-folders
  const esc = s => String(s == null ? "" : s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const num = v => { const d = String(v || "").replace(/\D/g, ""); return d.length === 10 ? "91" + d : d; };
  const url = v => !v ? "" : /^https?:\/\//.test(v) ? v : "https://" + v.replace(/^\/+/, "");
  const phone = num(S.phone), wa = num(S.whatsapp), booking = url(S.booking);
  const waLink = t => wa ? "https://wa.me/" + wa + "?text=" + encodeURIComponent(t) : (S.email ? "mailto:" + S.email : R + "contact.html");
  const pretty = d => d.length === 12 && d.startsWith("91") ? "+91 " + d.slice(2, 7) + " " + d.slice(7) : "+" + d;
  const ext = h => /^https?:|^mailto:/.test(h) ? ' target="_blank" rel="noopener"' : "";
  window.SNsite = { esc, waLink, R };

  /* ---- Theme toggle (remembers the choice) ---- */
  const root = document.documentElement;
  const sysDark = () => matchMedia("(prefers-color-scheme: dark)").matches;
  document.querySelectorAll(".theme").forEach(b => b.addEventListener("click", () => {
    const cur = root.dataset.theme || (sysDark() ? "dark" : "light");
    const next = cur === "dark" ? "light" : "dark";
    root.dataset.theme = next;
    try { localStorage.setItem("theme", next); } catch (e) {}
  }));

  /* ---- Menu: drop-downs and phone menu ---- */
  const nav = $("nav"), burger = $("burger");
  // The open phone menu fills the screen below the header.
  const fit = () => { if (nav.classList.contains("open")) nav.style.height = Math.max(200, innerHeight - nav.parentNode.closest(".top").getBoundingClientRect().bottom) + "px"; };
  if (burger) burger.addEventListener("click", () => { const o = nav.classList.toggle("open"); burger.setAttribute("aria-expanded", o); document.body.style.overflow = o ? "hidden" : ""; nav.style.height = ""; fit(); });
  addEventListener("resize", fit);
  const hoverMode = matchMedia("(hover: hover) and (min-width: 1021px)").matches;
  let lastScroll = 0; addEventListener("scroll", () => { lastScroll = Date.now(); }, { passive: true });
  document.querySelectorAll(".dd").forEach(dd => {
    const btn = dd.querySelector("button");
    btn.addEventListener("click", e => {
      e.stopPropagation();
      // With a mouse the menu is already open from hovering, so a click keeps it open.
      const open = hoverMode || !dd.hasAttribute("data-open");
      document.querySelectorAll(".dd[data-open]").forEach(x => { x.removeAttribute("data-open"); x.querySelector("button").setAttribute("aria-expanded", "false"); });
      if (open) { dd.setAttribute("data-open", ""); btn.setAttribute("aria-expanded", "true"); }
    });
    if (hoverMode) {
      // Stay open while the page scrolls under the pointer; close shortly after the pointer really leaves.
      let t;
      const shut = () => { dd.removeAttribute("data-open"); btn.setAttribute("aria-expanded", "false"); };
      dd.addEventListener("mouseenter", () => { clearTimeout(t); document.querySelectorAll(".dd[data-open]").forEach(x => { if (x !== dd) x.removeAttribute("data-open"); }); dd.setAttribute("data-open", ""); btn.setAttribute("aria-expanded", "true"); });
      dd.addEventListener("mouseleave", () => { if (Date.now() - lastScroll < 500) return; clearTimeout(t); t = setTimeout(() => { if (!dd.matches(":hover")) shut(); }, 250); });
      document.addEventListener("mousemove", e => { if (dd.hasAttribute("data-open") && !dd.contains(e.target) && Date.now() - lastScroll > 500) { clearTimeout(t); t = setTimeout(() => { if (!dd.matches(":hover")) shut(); }, 250); } }, { passive: true });
    }
  });
  document.addEventListener("click", () => document.querySelectorAll(".dd[data-open]").forEach(x => x.removeAttribute("data-open")));
  document.addEventListener("keydown", e => { if (e.key === "Escape") document.querySelectorAll(".dd[data-open]").forEach(x => x.removeAttribute("data-open")); });

  /* ---- "Log in" becomes "My learning" when signed in ---- */
  const nl = $("nav-login");
  try { if (nl && Object.keys(localStorage).some(k => /^sb-.+-auth-token$/.test(k))) { nl.querySelector("span").textContent = "Account"; const st = $("nav-student"); st.href = R + "lms.html"; st.querySelector("b").textContent = "My learning (LMS)"; } } catch (e) {}

  /* ---- WhatsApp, counselling and enrol links ---- */
  const w = $("wa");
  if (w && wa) { w.href = waLink("Hi SkillNavora, I'd like to know more about your programs."); w.hidden = false; }
  document.querySelectorAll("[data-wa]").forEach(a => { a.href = waLink(a.dataset.wa || "Hi SkillNavora"); if (/^https?:/.test(a.href)) { a.target = "_blank"; a.rel = "noopener"; } });
  document.querySelectorAll("[data-counsel]").forEach(a => { a.href = "#counselling"; a.removeAttribute("target"); });
  // "Enroll now" opens the application form for that program.
  const enrollHref = c => R + "apply.html?program=" + encodeURIComponent(c.id);
  document.querySelectorAll("[data-enroll]").forEach(a => { const c = C.find(x => x.id === a.dataset.enroll); if (c) a.href = enrollHref(c); });

  /* ---- Announcement pill ---- */
  const ann = $("announce");
  if (ann) { if (S.announcement) { ann.querySelector("b").textContent = S.announcement; if (S.announcementLink) ann.href = R + S.announcementLink; ann.hidden = false; } }

  /* ---- Countdown ---- */
  const left = d => { const ms = new Date(d) - Date.now(); if (!(ms > 0)) return null; const s = Math.floor(ms / 1000);
    return Math.floor(s / 86400) + "d : " + Math.floor(s % 86400 / 3600) + "h : " + String(Math.floor(s % 3600 / 60)).padStart(2, "0") + "m : " + String(s % 60).padStart(2, "0") + "s"; };
  function strip(c) {
    if (c.deadline && left(c.deadline)) return `Enrolment closes in <span class="cd" data-deadline="${esc(c.deadline)}">${left(c.deadline)}</span>`;
    const eb = typeof OFFERS !== "undefined" && c.earlyBird && OFFERS.earlyBirdEnds;
    if (eb && left(eb)) return `Early-bird ends in <span class="cd" data-deadline="${esc(eb)}">${left(eb)}</span>`;
    if (c.start) return `Next cohort starts <b>${esc(c.start)}</b>`;
    return "Enrolments opening soon";
  }
  setInterval(() => document.querySelectorAll("[data-deadline]").forEach(el => { el.textContent = left(el.dataset.deadline) || "closed"; }), 1000);

  /* ---- Course cover art ---- */
  const PAL = [["#0b1f4f", "#1d4ed8", "#fb923c"], ["#0b1736", "#334e8a", "#fdba74"], ["#083344", "#0e7490", "#fdba74"]];
  // Course icons: rocket (product), chart (data science), sparkles (GenAI)
  const ART = {
    "ai-pm": p => `<g transform="rotate(40)"><path d="M-7 18Q0 44 7 18Z" fill="#ff9933"/><path d="M-3.5 18Q0 33 3.5 18Z" fill="#ffe08a"/><path d="M-12 6L-24 20L-12 17Z" fill="${p[2]}"/><path d="M12 6L24 20L12 17Z" fill="${p[2]}"/><path d="M0-36C13-24 15-6 12 18H-12C-15-6-13-24 0-36Z" fill="#fff"/><path d="M0-36C6-30 9-24 10-18H-10C-9-24-6-30 0-36Z" fill="#ff9933"/><circle cy="-4" r="6.5" fill="${p[0]}" stroke="#138808" stroke-width="2.5"/></g>`,
    "ai-ds": p => `<g><rect x="-30" y="6" width="11" height="22" rx="2" fill="#fff" fill-opacity=".85"/><rect x="-14" y="-6" width="11" height="34" rx="2" fill="#ff9933"/><rect x="2" y="-16" width="11" height="44" rx="2" fill="#fff" fill-opacity=".85"/><rect x="18" y="-28" width="11" height="56" rx="2" fill="#138808"/><path d="M-26-4L-8-18L8-12L24-36" fill="none" stroke="#ffe08a" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><g fill="#ffe08a"><circle cx="-26" cy="-4" r="3.5"/><circle cx="-8" cy="-18" r="3.5"/><circle cx="8" cy="-12" r="3.5"/><circle cx="24" cy="-36" r="3.5"/></g></g>`,
    "genai-launchpad": p => `<g><path d="M-4-30C-1-10 4-5 24-2C4 1-1 6-4 26C-7 6-12 1-32-2C-12-5-7-10-4-30Z" fill="#fff"/><path d="M22-34C23-26 25-24 33-23C25-22 23-20 22-12C21-20 19-22 11-23C19-24 21-26 22-34Z" fill="#ff9933"/><path d="M20 12C21 18 22 19 28 20C22 21 21 22 20 28C19 22 18 21 12 20C18 19 19 18 20 12Z" fill="#35c043"/></g>`,
    compass: p => `<path d="M0-38l8 30-8 8-8-8z" fill="${p[2]}"/><path d="M0 38l-8-30 8-8 8 8z" fill="#fff"/><circle r="5" fill="${p[0]}" stroke="${p[2]}" stroke-width="3"/>`
  };
  window.SNcover = (i, title, badge) => { const p = PAL[i % PAL.length];
    return `<div class="cover"><svg class="art" viewBox="0 0 400 210" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><defs><linearGradient id="cg${i}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${p[0]}"/><stop offset="1" stop-color="${p[1]}"/></linearGradient></defs><rect width="400" height="210" fill="url(#cg${i})"/><circle cx="330" cy="40" r="120" fill="${p[2]}" opacity=".18"/><circle cx="360" cy="180" r="70" fill="#fff" opacity=".08"/><g transform="translate(300 118)"><circle r="50" fill="#fff" fill-opacity=".07" stroke="#fff" stroke-opacity=".35" stroke-width="2"/>${ART[(C.find(c => c.name === title) || {}).id] ? ART[(C.find(c => c.name === title) || {}).id](p) : ART.compass(p)}</g></svg>${badge ? `<span class="ribbon">${esc(badge)}</span>` : ""}<span class="ct">${esc(title)}</span></div>`; };

  /* ---- Program cards ---- */
  const cl = $("courses");
  if (cl) cl.innerHTML = C.map((c, i) => `<article class="course">
    ${SNcover(i, c.name, c.badge)}
    <div class="strip"><span>${strip(c)}</span>${c.cohort ? `<span class="tag g">${esc(c.cohort)}</span>` : ""}</div>
    <div class="body"><h3>${esc(c.name)}</h3><p>${esc(c.short)}</p>
      <div class="facts">${[c.duration, c.format, c.fee].filter(Boolean).map(f => `<span>${esc(f)}</span>`).join("")}</div>
      <div class="acts"><a class="btn btn-primary btn-sm" href="${R + esc(c.page)}">Learn more →</a><a class="btn btn-line btn-sm" href="${esc(enrollHref(c))}">Enroll now</a></div></div></article>`).join("");

  /* ---- Program menu (keeps names in sync with config) ---- */
  document.querySelectorAll("[data-course-name]").forEach(el => { const c = C.find(x => x.id === el.dataset.courseName); if (c) el.textContent = c.name; });

  /* ---- Career support ---- */
  const sup = $("support");
  const SUP_ICO = ['<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M9 13h6M9 17h6"/>', '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/>', '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>', '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>'];
  if (sup && typeof SUPPORT !== "undefined") sup.innerHTML = SUPPORT.map((s, i) => `<div class="card"><div class="ico${i % 2 ? " g" : ""}"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${SUP_ICO[i % 4]}</svg></div><h3>${esc(s.title)}</h3><p>${esc(s.text)}</p></div>`).join("");

  /* ---- Public events ---- */
  const EV = typeof EVENTS !== "undefined" ? EVENTS.filter(e => e && e.title && e.date) : [];
  const evCard = (e, past) => { const d = new Date(e.date + "T00:00:00");
    const reg = e.register ? url(e.register) : waLink("Hi SkillNavora, please register me for " + e.title + " on " + e.date + ".");
    return `<div class="event"><div class="top-row"><div class="cal"><small>${d.toLocaleDateString("en-IN", { month: "short" })}</small><b>${d.getDate()}</b></div><div><h4>${esc(e.title)}</h4>${e.time ? `<div class="meta">${esc(e.time)}</div>` : ""}${e.text ? `<p class="meta" style="margin:6px 0 0">${esc(e.text)}</p>` : ""}</div></div>
      <div class="bottom">${past ? '<span class="meta">Completed</span>' : `<span>Free</span><a class="btn btn-primary btn-sm" href="${esc(reg)}" target="_blank" rel="noopener">Register</a>`}</div></div>`; };
  const today = new Date(); today.setHours(0, 0, 0, 0);
  if ($("pub-events")) {
    const up = EV.filter(e => new Date(e.date + "T00:00:00") >= today).sort((a, b) => a.date.localeCompare(b.date));
    const past = EV.filter(e => new Date(e.date + "T00:00:00") < today).sort((a, b) => b.date.localeCompare(a.date));
    $("pub-events").innerHTML = up.length ? up.map(e => evCard(e)).join("") : `<p class="empty" style="grid-column:1/-1">New events are announced soon. <a href="${esc(waLink("Hi SkillNavora, please tell me about upcoming events."))}" target="_blank" rel="noopener">Get updates on WhatsApp</a>.</p>`;
    $("pub-past").innerHTML = past.length ? past.map(e => evCard(e, true)).join("") : '<p class="empty" style="grid-column:1/-1">Past events will appear here.</p>';
  }

  /* ---- Community link ---- */
  document.querySelectorAll("[data-community]").forEach(a => { if (S.community) { a.href = url(S.community); a.target = "_blank"; a.rel = "noopener"; a.hidden = false; } });

  /* ---- Testimonials ---- */
  const tl = $("testimonials-list"), ts = $("testimonials"), T = (typeof TESTIMONIALS !== "undefined" ? TESTIMONIALS : []).filter(t => t && t.quote);
  if (T.length) document.querySelectorAll("[data-reviews-nav]").forEach(a => a.hidden = false);

  /* ---- FAQ with search and categories ---- */
  const fq = $("faq");
  if (fq && typeof FAQS !== "undefined") {
    const cats = ["All", ...new Set(FAQS.map(f => f.c))];
    $("faq-chips").innerHTML = cats.map((c, i) => `<button type="button" aria-pressed="${i === 0}" data-c="${esc(c)}">${esc(c)}</button>`).join("");
    fq.innerHTML = FAQS.map(f => `<details data-c="${esc(f.c)}"><summary><span class="tag">${esc(f.c)}</span><b>${esc(f.q)}</b></summary><p>${esc(f.a)}</p></details>`).join("") + '<p class="faq-empty" hidden>No questions match. Try another word, or ask us on WhatsApp.</p>';
    let cat = "All";
    const apply = () => { const q = $("faq-q").value.trim().toLowerCase(); let n = 0;
      fq.querySelectorAll("details").forEach(d => { const ok = (cat === "All" || d.dataset.c === cat) && (!q || d.textContent.toLowerCase().includes(q)); d.hidden = !ok; if (ok) n++; });
      fq.querySelector(".faq-empty").hidden = n > 0; };
    $("faq-q").addEventListener("input", apply);
    $("faq-chips").addEventListener("click", e => { const b = e.target.closest("button"); if (!b) return; cat = b.dataset.c; $("faq-chips").querySelectorAll("button").forEach(x => x.setAttribute("aria-pressed", x === b)); apply(); });
  }

  /* ---- Program page ---- */
  const pid = document.body.dataset.course, P = C.find(x => x.id === pid);
  if (P) {
    const set = (id, h) => { const el = $(id); if (el) el.innerHTML = h; };
    set("p-name", esc(P.name)); set("p-tagline", esc(P.tagline));
    set("p-fine", P.deadline && left(P.deadline) ? `⚡ Enrolment closes in <b data-deadline="${esc(P.deadline)}">${left(P.deadline)}</b>` : P.start ? `⚡ ${P.cohort ? esc(P.cohort) + " · " : ""}Live classes start <b>${esc(P.start)}</b>` : "⚡ Enrolments opening soon. Talk to a counsellor to reserve your seat.");
    set("p-facts", [["Duration", P.duration], ["Format", P.format], ["Time needed", P.effort], ["Next cohort", P.start || "Opening soon"]].map(([k, v]) => `<div class="fact"><small>${k}</small><b>${esc(v || "—")}</b></div>`).join(""));
    set("p-outcomes", (P.outcomes || []).map(x => `<li>${esc(x)}</li>`).join(""));
    set("p-curriculum", (P.curriculum || []).map((m, i) => `<details class="mod"${i === 0 ? " open" : ""}><summary><span class="n">${String(i + 1).padStart(2, "0")}</span><span>${esc(m.title)}</span></summary><ul>${(m.topics || []).map(t => `<li>${esc(t)}</li>`).join("")}</ul></details>`).join(""));
    set("p-projects", (P.projects || []).map((x, i) => `<div class="card"><div class="ico${i % 2 ? " g" : ""}"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l3 7h7l-5.5 4.5L18 21l-6-4-6 4 1.5-7.5L2 9h7z"/></svg></div><h3>${esc(x)}</h3></div>`).join(""));
    set("p-price", esc(P.fee || "Fees on request"));
    if (P.earlyBird && $("p-early")) { $("p-early").textContent = "🎉 " + P.earlyBird; $("p-early").hidden = false; }
    set("p-feenote", esc(P.feeNote || (P.fee ? "Talk to a counsellor about payment options." : "Fees are shared when enrolment opens. Talk to a counsellor for details.")));
    set("p-schedule", [["Cohort", P.cohort || "Next cohort"], ["Starts", P.start || "Opening soon"], ["Duration", P.duration], ["Format", P.format], ["Time needed", P.effort]].map(([k, v]) => `<li><span class="meta" style="min-width:110px;display:inline-block">${k}</span> <b>${esc(v || "—")}</b></li>`).join(""));
  }

  /* ---- Sticky enrol bar ---- */
  const st = $("sticky");
  if (st) {
    const c = P || C[0];
    if (c) {
      st.querySelector(".cohort span").textContent = c.cohort || "Enrolling";
      st.querySelector(".info b").textContent = c.name;
      st.querySelector(".info span").textContent = [c.duration, c.format, c.start ? "Starts " + c.start : ""].filter(Boolean).join(" · ");
      st.querySelector("[data-st-enroll]").href = enrollHref(c); st.querySelector("[data-st-enroll]").removeAttribute("target");
      st.querySelector("[data-st-counsel]").href = "#counselling";
      document.body.classList.add("has-sticky");
      st.classList.add("show");
    }
  }

  /* ---- Footer and contact ---- */
  if ($("yr")) $("yr").textContent = new Date().getFullYear();
  const social = $("social");
  if (social) [["LinkedIn", url(S.linkedin)], ["Instagram", url(S.instagram)], ["YouTube", url(S.youtube)], ["X", url(S.twitter)], ["Facebook", url(S.facebook)], ["Telegram", url(S.telegram)], ["WhatsApp", wa ? waLink("Hi SkillNavora") : ""]].filter(x => x[1]).forEach(([n, u]) => social.insertAdjacentHTML("beforeend", `<a href="${esc(u)}" target="_blank" rel="noopener">${n}</a>`));
  const fc = $("fcontact");
  if (fc) fc.innerHTML = [S.email ? `<li><a href="mailto:${esc(S.email)}">${esc(S.email)}</a></li>` : "", phone ? `<li><a href="tel:+${phone}">${pretty(phone)}</a></li>` : "", S.address ? `<li>${esc(S.address)}</li>` : ""].join("");
  const ICON = { mail: '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 6l-10 7L2 6"/>', phone: '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>', chat: '<path d="M21 11.5a8.4 8.4 0 0 1-12.3 7.4L3 21l2.1-5.7A8.5 8.5 0 1 1 21 11.5z"/>', cal: '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 10h18M8 2v4M16 2v4"/>', pin: '<path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>' };
  const clist = $("clist");
  if (clist) {
    const add = (ic, label, text, href) => clist.insertAdjacentHTML("beforeend", `<li>${href ? `<a href="${esc(href)}"${ext(href)}>` : "<div>"}<span class="ci"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${ICON[ic]}</svg></span><span><small>${label}</small><b>${esc(text)}</b></span>${href ? "</a>" : "</div>"}</li>`);
    if (wa) add("chat", "WhatsApp", "Chat now · " + pretty(wa), waLink("Hi SkillNavora, I'd like to know more."));
    add("cal", "Counselling", "Book a free counselling session", booking || waLink("Hi SkillNavora, I'd like a free counselling session."));
    if (phone) add("phone", "Call", pretty(phone), "tel:+" + phone);
    if (S.email) add("mail", "Email", S.email, "mailto:" + S.email);
    if (S.address) add("pin", "Address", S.address);
  }
  const form = $("form"), msg = $("msg");
  if (form) {
    form.addEventListener("submit", async e => {
      e.preventDefault(); const d = new FormData(form), topic = d.get("interest") || "General";
      const v = k => String(d.get(k) || "").trim(), phone = v("phone");
      if (!v("name")) { msg.textContent = "Please enter your name."; return; }
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v("email"))) { msg.textContent = "Please enter a valid email."; return; }
      if (!/^[0-9+ ()-]{7,20}$/.test(phone) || phone.replace(/\D/g, "").length < 7) { msg.textContent = "Please enter a valid phone or WhatsApp number."; return; }
      const row = { kind: "contact", first_name: v("name"), email: v("email"), phone,
        role: topic.slice(0, 80), message: [v("company") && "Company: " + v("company"), v("message")].filter(Boolean).join("\n").slice(0, 2000) || null };
      const b = form.querySelector("button[type=submit]"); b.disabled = true; msg.textContent = "Sending…";
      const ok = window.SNsaveLead ? await window.SNsaveLead(row) : false; b.disabled = false;
      if (ok) { msg.textContent = "Thanks, " + row.first_name + "! Your message has been sent. We'll get back to you soon."; form.reset(); return; }
      msg.innerHTML = 'Couldn\'t send right now. <a href="' + waLink("Hi SkillNavora, I'm " + row.first_name + " (" + row.email + "). " + (v("message") || "")) + '" target="_blank" rel="noopener">Send it on WhatsApp instead</a>.';
    });
  }
})();
