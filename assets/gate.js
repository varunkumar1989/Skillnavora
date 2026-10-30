/* Resource gate: handbooks, PDFs and files open after the visitor shares their details once.
   The details are saved as a "resource" lead (Supabase + email/WhatsApp alert, same as every other form),
   so you can see how many people use your resources. This is a visitor-tracking gate, not security:
   it asks once per browser and remembers the answer. */
(function () {
  const KEY = "sn_access", FILE = /\.(pdf|xlsx|xls|csv|zip|pptx|docx)(?:[?#]|$)/i, DIR = /\/(handbook|classes|brochures|data-handbook)\//i;
  const LEAD_API = (window.SNsite && window.SNsite.R ? window.SNsite.R : "") + "api/lead";
  const get = k => { try { return localStorage.getItem(k); } catch { return null; } }, set = (k, v) => { try { localStorage.setItem(k, v); } catch {} };
  // Arriving from skillnavora.in with details already given (the handbook site is on another address)
  try { if (/[?&]sn=1\b/.test(location.search)) set(KEY, get(KEY) || JSON.stringify({ t: Date.now(), via: "link" })); } catch {}
  const has = () => !!get(KEY);
  const SKIP = /^(mailto:|tel:|javascript:|#)/i;

  const gated = a => {
    if (!a || a.hasAttribute("data-nogate")) return false;
    const href = a.getAttribute("href") || ""; if (!href || SKIP.test(href) || /wa\.me|whatsapp\.com/i.test(href)) return false;
    if (a.hasAttribute("data-gate")) return true;
    let u; try { u = new URL(a.href, location.href); } catch { return false; }
    if (/(^|\.)claude\.ai$/i.test(u.hostname) && /^\/artifact/.test(u.pathname)) return true;
    return u.hostname === location.hostname && (FILE.test(u.pathname) || DIR.test(u.pathname));
  };
  const labelOf = a => (a.dataset.gateLabel || a.textContent || a.getAttribute("href") || "").replace(/\s+/g, " ").replace(/[↗→]/g, "").trim().slice(0, 90);
  const withTag = href => { try { const u = new URL(href, location.href); if (/github\.io$|netlify\.app$/i.test(u.hostname) && !u.searchParams.has("sn")) u.searchParams.set("sn", "1"); return u.href; } catch { return href; } };

  let modal, pending = null;
  const build = () => {
    modal = document.createElement("div"); modal.className = "modal"; modal.id = "m-gate"; modal.setAttribute("role", "dialog"); modal.setAttribute("aria-modal", "true"); modal.setAttribute("aria-labelledby", "gate-h");
    modal.innerHTML = `<div class="mbox gate"><button class="mclose" type="button" data-gate-close aria-label="Close">×</button><div class="in">
      <div class="kicker">Free resources</div><h2 id="gate-h">Get free access</h2><div class="rule"></div>
      <p>Tell us a little about you, once. Then open every handbook, PDF and practice file on SkillNavora.</p>
      <form id="f-gate" novalidate><div class="gate-res" id="gate-res"></div>
        <label><span class="req">Full name</span><input name="name" autocomplete="name" maxlength="80" placeholder="Your name"></label>
        <label><span class="req">Email</span><input name="email" type="email" autocomplete="email" maxlength="120" placeholder="you@example.com"></label>
        <label><span class="req">Phone number</span><span class="phone"><select name="cc" aria-label="Country code"><option value="+91">🇮🇳 +91</option><option value="+971">🇦🇪 +971</option><option value="+1">🇺🇸 +1</option><option value="+44">🇬🇧 +44</option><option value="+65">🇸🇬 +65</option><option value="+61">🇦🇺 +61</option></select><input name="phone" inputmode="tel" maxlength="15" autocomplete="tel-national" placeholder="98765 43210"></span></label>
        <label><span class="req">I am a</span><select name="role"><option value="">Choose…</option><option>Student</option><option>Working professional</option><option>Career switcher</option><option>Hiring manager / recruiter</option><option>Other</option></select></label>
        <label><span>Interested in</span><select name="interest"><option value="">Not sure yet</option><option>Product management</option><option>Data engineering</option><option>Generative AI</option></select></label>
        <label class="chk"><input type="checkbox" name="consent"> <span>I agree that SkillNavora may contact me about learning resources and programs. <a href="privacy.html" target="_blank" rel="noopener" data-nogate>Privacy policy</a></span></label>
        <div class="notice" id="gate-msg" hidden></div>
        <button class="btn btn-primary" type="submit">Unlock access</button>
      </form></div></div>`;
    document.body.appendChild(modal);
    const base = document.body.dataset.root || "";
    modal.querySelectorAll("a[href='privacy.html']").forEach(a => a.setAttribute("href", base + "privacy.html"));
    modal.addEventListener("click", e => { if (e.target === modal || e.target.closest("[data-gate-close]")) modal.classList.remove("open"); });
    document.addEventListener("keydown", e => { if (e.key === "Escape") modal.classList.remove("open"); });
    const f = modal.querySelector("#f-gate"), msg = modal.querySelector("#gate-msg");
    const say = t => { msg.className = "notice error"; msg.textContent = t; msg.hidden = !t; };
    f.addEventListener("submit", async e => {
      e.preventDefault();
      const v = n => f.elements[n].value.trim(), phone = (f.elements.cc.value + " " + v("phone")).trim();
      if (!v("name")) return say("Please enter your name.");
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v("email"))) return say("Please enter a valid email.");
      if (!/^[0-9+ ()-]{7,20}$/.test(phone) || v("phone").replace(/\D/g, "").length < 7) return say("Please enter a valid phone number.");
      if (!v("role")) return say("Please choose who you are.");
      if (!f.elements.consent.checked) return say("Please tick the box to continue.");
      say("");
      const b = f.querySelector("button[type=submit]"), t = b.textContent; b.disabled = true; b.textContent = "Unlocking…";
      const row = { kind: "resource", first_name: v("name"), email: v("email"), phone, role: v("role"),
        message: ("[Resource access] " + (pending ? pending.label : "") + (v("interest") ? " | Interested in: " + v("interest") : "") + " | Page: " + location.pathname).slice(0, 1900) };
      try { if (window.SNsaveLead) await window.SNsaveLead(row); } catch {}
      set(KEY, JSON.stringify({ t: Date.now(), n: v("name").split(" ")[0] }));
      b.disabled = false; b.textContent = t; f.reset(); modal.classList.remove("open");
      toast("Access unlocked. Thank you!");
      if (pending) { const p = pending; pending = null; go(p.href, p.blank); }
    });
  };
  const toast = text => { const d = document.createElement("div"); d.className = "gate-toast"; d.textContent = text; document.body.appendChild(d); setTimeout(() => d.remove(), 3200); };
  const go = (href, blank) => { href = withTag(href); if (blank) { const w = window.open(href, "_blank", "noopener"); if (!w) location.href = href; } else location.href = href; };
  const ask = a => {
    if (!modal) build();
    pending = { href: a.href, blank: a.target === "_blank" || /\.(pdf)(?:[?#]|$)/i.test(a.href), label: labelOf(a) };
    modal.querySelector("#gate-res").innerHTML = pending.label ? `<div class="gate-chip">Opening: <b></b></div>` : "";
    const b = modal.querySelector(".gate-chip b"); if (b) b.textContent = pending.label;
    modal.classList.add("open"); setTimeout(() => modal.querySelector("input[name=name]").focus(), 30);
  };

  document.addEventListener("click", e => {
    if (e.defaultPrevented || e.button > 0 || e.metaKey || e.ctrlKey || e.shiftKey) return;
    const a = e.target.closest("a"); if (!a || !gated(a)) return;
    if (has()) { if (/github\.io$|netlify\.app$/i.test(new URL(a.href, location.href).hostname)) { e.preventDefault(); go(a.href, a.target === "_blank"); } return; }
    e.preventDefault(); ask(a);
  }, true);
  // Middle-click / context menu on gated links ask too
  document.addEventListener("auxclick", e => { const a = e.target.closest && e.target.closest("a"); if (a && gated(a) && !has() && e.button === 1) { e.preventDefault(); ask(a); } }, true);
  window.SNgate = { has, ask: href => { const a = document.createElement("a"); a.href = href; ask(a); } };
})();
