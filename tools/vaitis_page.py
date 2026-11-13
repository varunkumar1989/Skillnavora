"""Vaitis by SkillNavora: free AI library page (vaitis.html).

The page shows a short sign-up (name, email, country, phone, coding yes/no, role,
experience). Details are saved as a "resource" lead through /api/lead, then the
library opens: 25 step-by-step guides and 763 AI tools in 26 categories.
Data comes from assets/vaitis/*.json, built by tools/vaitis/build.py.
Deep links: vaitis.html#tools-<category-slug>, #g-<guide id>, #guides, #saved.
This is visitor tracking, not security: the data files are public.
"""
import html, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "vaitis"))
import build as vbuild

E = lambda s: html.escape(str(s), quote=True)

ROLES = ["Student", "Working professional", "Founder or business owner", "Freelancer or consultant", "Content creator", "Something else"]
EXP = ["Not working yet", "Less than 2 years", "2 to 5 years", "5 to 10 years", "More than 10 years"]
COUNTRIES = [("IN", "India", "+91"), ("US", "United States", "+1"), ("GB", "United Kingdom", "+44"), ("AE", "United Arab Emirates", "+971"),
             ("CA", "Canada", "+1"), ("AU", "Australia", "+61"), ("SG", "Singapore", "+65"), ("SA", "Saudi Arabia", "+966"),
             ("DE", "Germany", "+49"), ("NP", "Nepal", "+977"), ("BD", "Bangladesh", "+880"), ("LK", "Sri Lanka", "+94"),
             ("PK", "Pakistan", "+92"), ("NG", "Nigeria", "+234"), ("ZA", "South Africa", "+27"), ("PH", "Philippines", "+63"),
             ("MY", "Malaysia", "+60"), ("QA", "Qatar", "+974"), ("KW", "Kuwait", "+965"), ("OM", "Oman", "+968"),
             ("NZ", "New Zealand", "+64"), ("IE", "Ireland", "+353"), ("FR", "France", "+33"), ("NL", "Netherlands", "+31"), ("XX", "Other", "")]


def body():
    meta = vbuild.main()
    ver = vbuild.versions()
    cats = meta["categories"]
    p = meta["price"]
    feats = [("📚", "Step-by-step guides", f"{meta['guides']} detailed walkthroughs with every command, prompt and link, written in plain English."),
             ("🧠", "Ready-to-use prompts", "Copy, paste and get the result. Every prompt has a one-click Copy button."),
             ("🧰", f"{meta['tools']} AI tools", f"Sorted into {len(cats)} categories with pricing: {p.get('freeplan', 0)} with a free plan, {p.get('free', 0)} fully free."),
             ("🔔", "New drops", "Fresh guides and tools are added regularly. Turn on updates to hear first.")]
    feat_html = "".join(f'<div class="vx-feat"><span class="vx-fi" aria-hidden="true">{i}</span><div><b>{E(t)}</b><p>{E(d)}</p></div></div>' for i, t, d in feats)
    country_opts = "".join(f'<option value="{c}" data-dial="{d}"{" selected" if c == "IN" else ""}>{E(n)}{(" (" + d + ")") if d else ""}</option>' for c, n, d in COUNTRIES)
    role_opts = "".join(f"<option>{E(r)}</option>" for r in ROLES)
    exp_opts = "".join(f"<option>{E(x)}</option>" for x in EXP)
    top_cats = "".join(f'<span>{c["icon"]} {E(c["name"])} <b>{c["count"]}</b></span>' for c in cats[:6])
    return f"""
<div class="vx" id="vx" data-v-tools="{ver['tools']}" data-v-guides="{ver['guides']}" data-v-meta="{ver['meta']}">
<section class="vx-gate" id="vx-gate">
  <div class="wrap vx-gate-grid">
    <div class="vx-pitch">
      <span class="vx-pill">✨ Free AI Community · by SkillNavora</span>
      <h1 class="vx-h1">B100x <span>with AI.</span></h1>
      <p class="vx-lead"><b>Vaitis</b> is the free AI library for people who build.</p>
      <p class="vx-sub">Every prompt, workflow and tool in one free library.</p>
      <div class="vx-stats"><div><b>{meta['guides']}</b><small>step-by-step guides</small></div><div><b>{meta['tools']}</b><small>AI tools</small></div><div><b>{len(cats)}</b><small>categories</small></div></div>
      <a class="btn btn-primary vx-jump" href="#vx-form">Get free access ↓</a>
      <h2 class="vx-h2">What you'll get</h2>
      <div class="vx-feats">{feat_html}</div>
      <div class="vx-topcats">{top_cats}</div>
    </div>
    <form class="vx-form" id="vx-form" novalidate>
      <h2>Tell us a bit about you</h2>
      <p class="vx-mu">One quick form, then the whole library is yours.</p>
      <label class="vx-f"><span>Your name</span><input name="name" autocomplete="name" required maxlength="80" placeholder="Your name"></label>
      <label class="vx-f"><span>Email address</span><input name="email" type="email" autocomplete="email" required maxlength="200" placeholder="you@example.com"></label>
      <label class="vx-f"><span>Country <small id="vx-detected"></small></span><select name="country" id="vx-country">{country_opts}</select></label>
      <label class="vx-f"><span>Phone number</span><span class="vx-phone"><b id="vx-dial">+91</b><input name="phone" type="tel" autocomplete="tel-national" required inputmode="tel" maxlength="16" placeholder="Phone number"></span></label>
      <fieldset class="vx-f vx-radio"><legend>Do you know <b>coding</b>?</legend><label><input type="radio" name="coding" value="Yes" required> Yes</label><label><input type="radio" name="coding" value="No"> No</label></fieldset>
      <label class="vx-f"><span>What describes you best?</span><select name="role" required><option value="">Choose one</option>{role_opts}</select></label>
      <label class="vx-f"><span>Years of work experience</span><select name="experience" required><option value="">Choose one</option>{exp_opts}</select></label>
      <label class="vx-check"><input type="checkbox" name="updates" checked><span>Email me when new resources go live</span></label>
      <label class="vx-check"><input type="checkbox" name="newsletter" checked><span>Subscribe me to the SkillNavora newsletter<small>Weekly AI updates and new workflows</small></span></label>
      <p class="vx-err" id="vx-err" role="alert" hidden></p>
      <button class="btn btn-primary vx-go" type="submit">Get free access</button>
      <p class="vx-mu vx-safe">🔒 Your details stay with SkillNavora. No spam, ever. <a href="privacy.html">Privacy</a></p>
    </form>
  </div>
</section>
<section class="vx-app" id="vx-app" hidden>
  <div class="wrap">
    <div class="vx-apphead">
      <div><span class="vx-pill">Vaitis · B100x with AI</span><h1 class="vx-h1 vx-h1s" id="vx-hello">Your free AI library</h1></div>
      <label class="vx-search"><span aria-hidden="true">🔎</span><input id="vx-q" type="search" placeholder="Search guides and {meta['tools']} tools…" aria-label="Search the library"></label>
    </div>
    <div class="vx-tabs" role="tablist" aria-label="Library sections">
      <button role="tab" type="button" data-tab="guides" aria-selected="true">📚 Guides <span class="n">{meta['guides']}</span></button>
      <button role="tab" type="button" data-tab="tools" aria-selected="false">🧰 AI Tools <span class="n">{meta['tools']}</span></button>
      <button role="tab" type="button" data-tab="saved" aria-selected="false">🔖 Saved <span class="n" id="vx-saved-n">0</span></button>
    </div>
    <div id="vx-view" aria-live="polite"><p class="vx-mu">Loading the library…</p></div>
    <p class="vx-mu vx-foot">Tools, prices and features change often; check each tool's website before you rely on it. Guides are written by SkillNavora; projects named in them belong to their own creators. Vaitis is a free SkillNavora library.</p>
  </div>
</section>
</div>"""
