/* Shared behaviour for every page. Settings live in assets/config.js. */
(function () {
  const S = typeof SITE !== "undefined" ? SITE : {}, $ = id => document.getElementById(id);
  const num = v => { const d = String(v || "").replace(/\D/g, ""); return d.length === 10 ? "91" + d : d; };
  const url = v => !v ? "" : /^https?:\/\//.test(v) ? v : "https://" + v.replace(/^\/+/, "");
  const phone = num(S.phone), wa = num(S.whatsapp);
  const li = url(S.linkedin), ig = url(S.instagram), yt = url(S.youtube), booking = url(S.booking);
  const waLink = text => "https://wa.me/" + wa + "?text=" + encodeURIComponent(text);
  const pretty = d => d.length === 12 && d.startsWith("91") ? "+91 " + d.slice(2, 7) + " " + d.slice(7) : "+" + d;
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  // Mobile menu
  const burger = $("burger"), menu = $("menu");
  if (burger && menu) burger.addEventListener("click", () => {
    const open = menu.classList.toggle("open");
    burger.setAttribute("aria-expanded", open);
  });

  // "Log in" becomes "My dashboard" once someone is signed in (Supabase keeps the session in localStorage).
  const nl = $("nav-login");
  try {
    if (nl && Object.keys(localStorage).some(k => /^sb-.+-auth-token$/.test(k))) {
      nl.textContent = "My dashboard"; nl.href = nl.getAttribute("href").replace("login.html", "dashboard.html");
    }
  } catch (e) { /* storage blocked: keep "Log in" */ }

  // Floating WhatsApp button
  const w = $("wa");
  if (w && wa) { w.href = waLink("Hi SkillNavora"); w.hidden = false; }

  // Year and social links in the footer
  if ($("yr")) $("yr").textContent = new Date().getFullYear();
  const social = $("social");
  if (social) [["LinkedIn", li], ["Instagram", ig], ["YouTube", yt], ["GitHub", "https://github.com/varunkumar1989"]]
    .filter(x => x[1]).forEach(([n, u]) => {
      const item = document.createElement("li"), a = document.createElement("a");
      a.href = u; a.textContent = n; a.target = "_blank"; a.rel = "noopener";
      item.appendChild(a); social.appendChild(item);
    });
  document.querySelectorAll("[data-linkedin]").forEach(a => { if (li) { a.href = li; a.hidden = false; } });
  document.querySelectorAll("[data-wa]").forEach(a => {
    if (wa) a.href = waLink(a.dataset.wa || "Hi SkillNavora");
    else if (S.email) a.href = "mailto:" + S.email;
  });

  // Contact list
  const icon = {
    mail: '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 6l-10 7L2 6"/>',
    phone: '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
    chat: '<path d="M21 11.5a8.4 8.4 0 0 1-12.3 7.4L3 21l2.1-5.7A8.5 8.5 0 1 1 21 11.5z"/>',
    pin: '<path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    in: '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/>'
  };
  const clist = $("clist");
  const add = (ic, label, text, href) => {
    const item = document.createElement("li"), el = document.createElement(href ? "a" : "div");
    if (href) { el.href = href; if (/^http/.test(href)) { el.target = "_blank"; el.rel = "noopener"; } }
    el.innerHTML = '<span class="ci"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' + icon[ic] + '</svg></span><span><small></small><b></b></span>';
    el.querySelector("small").textContent = label; el.querySelector("b").textContent = text;
    item.appendChild(el); clist.appendChild(item);
  };
  if (clist) {
    if (wa) add("chat", "WhatsApp", "Chat now · " + pretty(wa), waLink("Hi SkillNavora, I'd like to know more."));
    if (phone) add("phone", "Call", pretty(phone), "tel:+" + phone);
    if (S.email) add("mail", "Email", S.email, "mailto:" + S.email);
    if (li) add("in", "LinkedIn", "Connect with Varun", li);
    if (S.city) add("pin", "Location", S.city);
  }

  // Programs cards
  const pg = $("programs-list");
  if (pg && typeof PROGRAMS !== "undefined") pg.innerHTML = PROGRAMS.map(p => {
    const href = p.link ? esc(p.link) : (wa ? esc(waLink("Hi SkillNavora, I'd like to know about " + p.name + ".")) : "contact.html");
    const ext = /^https?:/.test(href) ? ' target="_blank" rel="noopener"' : "";
    return '<div class="card' + (p.featured ? " feature" : "") + '">' +
      (p.tag ? '<span class="tag">' + esc(p.tag) + '</span>' : "") +
      '<h3>' + esc(p.name) + '</h3>' +
      '<div class="price">' + esc(p.price || "Ask for fees") + (p.unit ? ' <small>· ' + esc(p.unit) + '</small>' : "") + '</div>' +
      '<p>' + esc(p.text) + '</p>' +
      (p.points && p.points.length ? '<ul>' + p.points.map(x => '<li>' + esc(x) + '</li>').join("") + '</ul>' : "") +
      '<a class="btn ' + (p.featured ? "g" : "s") + '" href="' + href + '"' + ext + '>' + esc(p.button || "Learn more") + ' →</a></div>';
  }).join("");

  // Testimonials (section hidden until there is at least one)
  const tl = $("testimonials-list"), ts = $("testimonials");
  const T = (typeof TESTIMONIALS !== "undefined" ? TESTIMONIALS : []).filter(t => t && t.quote);
  if (tl && ts && T.length) {
    tl.innerHTML = T.map(t => '<figure class="card" style="margin:0"><blockquote class="quote">“' + esc(t.quote) + '”</blockquote>' +
      '<figcaption class="who">' + (t.photo ? '<img class="avatar" src="' + esc(t.photo) + '" alt="">' : '<span class="avatar">' + esc((t.name || "?").trim()[0]) + '</span>') +
      '<span><b>' + esc(t.name || "") + '</b><span>' + esc(t.role || "") + '</span></span></figcaption></figure>').join("");
    ts.hidden = false;
  }

  // Booking (mentoring page)
  const bk = $("booking"), nb = $("no-booking");
  if (bk && booking) {
    const f = document.createElement("iframe");
    f.className = "embed"; f.title = "Book a mentoring call"; f.loading = "lazy";
    f.src = booking + (booking.includes("calendly.com") ? (booking.includes("?") ? "&" : "?") + "hide_gdpr_banner=1" : "");
    bk.appendChild(f); bk.hidden = false;
    document.querySelectorAll("[data-booking]").forEach(a => { a.href = booking; a.target = "_blank"; a.rel = "noopener"; });
  } else if (nb) nb.hidden = false;

  // Contact form
  const form = $("form"), msg = $("msg");
  if (form) {
    if (!S.web3formsKey && !S.email) form.hidden = true;
    form.addEventListener("submit", async e => {
      e.preventDefault();
      const d = new FormData(form);
      const topic = d.get("interest") || "General";
      if (!S.web3formsKey) {
        location.href = "mailto:" + S.email + "?subject=" + encodeURIComponent("SkillNavora enquiry: " + topic) + "&body=" + encodeURIComponent(d.get("message") + "\n\n" + d.get("name") + " · " + d.get("email"));
        return;
      }
      d.append("access_key", S.web3formsKey); d.append("subject", "New SkillNavora enquiry: " + topic);
      msg.textContent = "Sending…";
      try {
        const r = await fetch("https://api.web3forms.com/submit", { method: "POST", body: d });
        const j = await r.json();
        msg.textContent = j.success ? "Thanks! We'll reply by email soon." : "Couldn't send. Please email or WhatsApp us instead.";
        if (j.success) form.reset();
      } catch { msg.textContent = "Couldn't send. Please email or WhatsApp us instead."; }
    });
  }
})();
