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
  // Signed-in admins (flag set by the admin panel, cleared on sign-out) skip the form and are not counted as visitors.
  const isAdmin = () => { try { const a = JSON.parse(get("sn_admin") || "null"); return !!a && Date.now() - a.t < 30 * 864e5; } catch { return false; } };
  const has = () => isAdmin() || !!get(KEY);
  if (isAdmin()) document.addEventListener("DOMContentLoaded", () => { const b = document.createElement("div"); b.textContent = "Admin view · details form off"; b.setAttribute("style", "position:fixed;left:12px;bottom:12px;z-index:9998;background:#17614F;color:#fff;font:600 12px/1 system-ui,sans-serif;padding:7px 11px;border-radius:999px;opacity:.9;pointer-events:none"); document.body.appendChild(b); });
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

  let modal, pending = null, pending0 = "";
  // PDFs open inside the page (browser's own PDF viewer in a frame) so learners and admins stay on the site.
  const PDFX = /\.pdf(?:[?#]|$)/i;
  const canInline = () => navigator.pdfViewerEnabled !== false && !/Android|iPhone|iPad/i.test(navigator.userAgent);
  let viewer;
  const openPdf = (href, label) => {
    if (!viewer) {
      const st = document.createElement("style");
      st.textContent = ".snpv{position:fixed;inset:0;z-index:9999;background:rgba(15,12,30,.72);display:flex;flex-direction:column;padding:max(10px,env(safe-area-inset-top)) max(10px,env(safe-area-inset-right)) max(10px,env(safe-area-inset-bottom)) max(10px,env(safe-area-inset-left))}.snpv[hidden]{display:none}.snpv-bar{display:flex;gap:8px;align-items:center;background:#fff;color:#17142E;border-radius:10px 10px 0 0;padding:8px 12px;font:600 14px/1.3 system-ui,sans-serif}.snpv-bar b{flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.snpv-bar a,.snpv-bar button{font:600 13px system-ui,sans-serif;border:1px solid #d9d3ee;background:#fff;color:#17142E;border-radius:8px;padding:6px 10px;cursor:pointer;text-decoration:none}.snpv iframe{flex:1;width:100%;border:0;background:#fff;border-radius:0 0 10px 10px}";
      document.head.appendChild(st);
      viewer = document.createElement("div"); viewer.className = "snpv"; viewer.hidden = true; viewer.setAttribute("role", "dialog"); viewer.setAttribute("aria-modal", "true");
      viewer.innerHTML = '<div class="snpv-bar"><b></b><a target="_blank" rel="noopener" data-nogate data-pdf-direct>Open in new tab ↗</a><button type="button" data-close>Close ✕</button></div><iframe title="Document"></iframe>';
      document.body.appendChild(viewer);
      const close = () => { viewer.hidden = true; viewer.querySelector("iframe").src = "about:blank"; document.documentElement.style.overflow = ""; };
      viewer.querySelector("[data-close]").addEventListener("click", close);
      viewer.addEventListener("click", e => { if (e.target === viewer) close(); });
      document.addEventListener("keydown", e => { if (e.key === "Escape" && !viewer.hidden) close(); });
    }
    viewer.querySelector("b").textContent = label || decodeURIComponent(href.split("/").pop().split(/[?#]/)[0]);
    viewer.querySelector("a").href = href; viewer.querySelector("iframe").src = href;
    viewer.hidden = false; document.documentElement.style.overflow = "hidden"; viewer.querySelector("[data-close]").focus();
  };

  // The owner's GitHub repositories: admins open them; everyone else sends an access request for the owner to approve.
  const OWNER_GH = /^https?:\/\/(www\.)?github\.com\/varunkumar1989\//i;
  const ghAdmin = () => { try { const a = JSON.parse(localStorage.getItem("sn_admin") || "null"); return !!a && Date.now() - a.t < 30 * 864e5; } catch { return false; } };
  let ghBox;
  const ghRequest = repo => {
    if (!ghBox) {
      ghBox = document.createElement("div"); ghBox.setAttribute("style", "position:fixed;inset:0;z-index:9999;background:rgba(15,12,30,.72);display:flex;align-items:center;justify-content:center;padding:16px"); ghBox.hidden = true; const ghs = document.createElement("style"); ghs.textContent = "[data-ghbox][hidden]{display:none!important}"; document.head.appendChild(ghs); ghBox.setAttribute("data-ghbox", "");
      ghBox.innerHTML = '<form style="background:#fff;color:#17142E;border-radius:14px;max-width:420px;width:100%;padding:20px;font:14px/1.45 system-ui,sans-serif" novalidate><h2 style="margin:0 0 4px;font-size:19px">Request GitHub access</h2><p style="margin:0 0 12px;color:#4A4660">The code repositories are private. Send a request and the owner will add you after approving it.</p>' +
        '<label style="display:block;font-weight:600;margin:6px 0 3px">Full name</label><input name="name" maxlength="80" style="width:100%;padding:8px;border:1px solid #d9d3ee;border-radius:8px">' +
        '<label style="display:block;font-weight:600;margin:6px 0 3px">Email</label><input name="email" type="email" maxlength="120" style="width:100%;padding:8px;border:1px solid #d9d3ee;border-radius:8px">' +
        '<label style="display:block;font-weight:600;margin:6px 0 3px">GitHub username</label><input name="gh" maxlength="40" style="width:100%;padding:8px;border:1px solid #d9d3ee;border-radius:8px">' +
        '<label style="display:block;font-weight:600;margin:6px 0 3px">Why do you need access?</label><input name="why" maxlength="200" style="width:100%;padding:8px;border:1px solid #d9d3ee;border-radius:8px">' +
        '<p data-msg style="color:#B42318;min-height:18px;margin:8px 0 0"></p><div style="display:flex;gap:8px;margin-top:8px"><button type="submit" style="flex:1;padding:10px;border:0;border-radius:9px;background:#6C4CF5;color:#fff;font-weight:700;cursor:pointer">Send request</button><button type="button" data-close style="padding:10px 14px;border:1px solid #d9d3ee;border-radius:9px;background:#fff;cursor:pointer">Cancel</button></div></form>';
      document.body.appendChild(ghBox);
      const f = ghBox.querySelector("form"), m = ghBox.querySelector("[data-msg]");
      ghBox.querySelector("[data-close]").addEventListener("click", () => ghBox.hidden = true);
      f.addEventListener("submit", async e => {
        e.preventDefault(); const v = n => f.elements[n].value.trim();
        if (!v("name")) return m.textContent = "Please enter your name.";
        if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v("email"))) return m.textContent = "Please enter a valid email.";
        if (!/^[A-Za-z0-9-]{1,39}$/.test(v("gh"))) return m.textContent = "Please enter your GitHub username.";
        m.textContent = "";
        const row = { kind: "resource", first_name: v("name"), email: v("email"), role: "GitHub access request", source: "github-request",
          message: ("[GitHub access request] GitHub user: " + v("gh") + " | Repo: " + ghBox.dataset.repo + " | Reason: " + v("why") + " | Page: " + location.pathname).slice(0, 1900) };
        try { await (window.SNsaveLead ? window.SNsaveLead(row) : fetch(LEAD_API, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(row) })); } catch {}
        f.reset(); ghBox.hidden = true;
        const d = document.createElement("div"); d.textContent = "Request sent. You will get access once the owner approves it."; d.setAttribute("style", "position:fixed;left:50%;bottom:24px;transform:translateX(-50%);z-index:10000;background:#17142E;color:#fff;padding:10px 16px;border-radius:10px;font:600 14px system-ui,sans-serif"); document.body.appendChild(d); setTimeout(() => d.remove(), 4000);
      });
    }
    ghBox.dataset.repo = repo; ghBox.hidden = false; ghBox.querySelector("input").focus();
  };
  document.addEventListener("click", e => {
    const a = e.target.closest && e.target.closest("a"); if (!a || !OWNER_GH.test(a.href) || ghAdmin()) return;
    e.preventDefault(); e.stopImmediatePropagation(); ghRequest(a.href);
  }, true);
  // Lessons and handbook pages open in the same in-page viewer when clicked from hub pages (resources, handbooks, LMS, tools, tests),
  // so learners stay on the tab they were browsing. Inside lessons themselves, links navigate normally.
  const HUB_PAGE = !/\/data-science\/(lessons|index)|\/handbooks\/pm\//.test(location.pathname) && window.self === window.top;
  const sameOriginLesson = href => { try { const u = new URL(href, location.href); return HUB_PAGE && u.origin === location.origin && /\/(data-science\/lessons\/[^/]+|handbooks\/pm\/[^/]+)\.html$/.test(u.pathname); } catch { return false; } };
  const sameOriginPdf = href => { try { const u = new URL(href, location.href); return u.origin === location.origin && PDFX.test(u.pathname); } catch { return false; } };
  document.addEventListener("click", e => {
    if (e.defaultPrevented || e.button > 0 || e.metaKey || e.ctrlKey || e.shiftKey) return;
    const a = e.target.closest && e.target.closest("a"); if (!a || a.hasAttribute("data-pdf-direct")) return;
    if (sameOriginLesson(a.href)) { e.preventDefault(); openPdf(a.href, (a.textContent || "").replace(/\s+/g, " ").replace(/[↗⬇→]/g, "").trim().slice(0, 90)); return; }
    if (!sameOriginPdf(a.href) || !canInline()) return;
    if (typeof has === "function" && !has() && typeof gated === "function" && gated(a)) return;   // the details form handles it first
    e.preventDefault(); openPdf(a.href, (a.textContent || "").replace(/\s+/g, " ").replace(/[↗⬇→]/g, "").trim().slice(0, 90));
  });

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
      if (pending) { const p = pending; pending = null; pending0 = p.label; go(p.href, p.blank); }
    });
  };
  const toast = text => { const d = document.createElement("div"); d.className = "gate-toast"; d.textContent = text; document.body.appendChild(d); setTimeout(() => d.remove(), 3200); };
  const go = (href, blank) => { if (sameOriginPdf(href) && canInline()) return openPdf(href, pending0); href = withTag(href); if (blank) { const w = window.open(href, "_blank", "noopener"); if (!w) location.href = href; } else location.href = href; };
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
