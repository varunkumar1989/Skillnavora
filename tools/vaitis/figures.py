"""Theme-aware SVG illustrations for Vaitis guides.

A guide embeds one with a fence:   ```figure <name>   (empty body)   ```
Colours come from CSS classes (fg-*) defined in assets/vaitis.css, so every
diagram follows the page's light or dark theme.
"""
import html

E = lambda s: html.escape(str(s), quote=True)
CW = 6.9  # approx. width of one character at 13px


def wrap(text, width_px, size=13):
    max_chars = max(6, int(width_px / (CW * size / 13)))
    words, lines, cur = str(text).split(), [], ""
    for w in words:
        if len(cur) + len(w) + (1 if cur else 0) <= max_chars:
            cur = (cur + " " + w).strip()
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines


def box(x, y, w, h, title, sub="", icon="", kind="card"):
    cls = {"card": "fg-card", "hub": "fg-hub", "warn": "fg-warnbox", "ok": "fg-okbox"}[kind]
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" class="{cls}"/>']
    tl, sl = wrap(title, w - 20, 14), wrap(sub, w - 18, 12)
    content = (26 if icon else 0) + len(tl) * 17 + len(sl) * 15
    ty = y + max(24, (h - content) / 2 + 14)
    tx = x + w / 2
    if icon:
        out.append(f'<text x="{tx}" y="{ty + 2}" class="fg-ico" text-anchor="middle">{E(icon)}</text>'); ty += 26
    tcls = "fg-t-on" if kind == "hub" else "fg-t"
    for ln in tl:
        out.append(f'<text x="{tx}" y="{ty}" class="{tcls}" text-anchor="middle">{E(ln)}</text>'); ty += 17
    scls = "fg-s-on" if kind == "hub" else "fg-s"
    for ln in sl:
        out.append(f'<text x="{tx}" y="{ty + 2}" class="{scls}" text-anchor="middle">{E(ln)}</text>'); ty += 15
    return "".join(out)


def arrow(x1, y1, x2, y2, label="", dashed=False, cls="fg-arrow"):
    d = ' stroke-dasharray="5 5"' if dashed else ""
    out = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{cls}" marker-end="url(#fgArrow)"{d}/>'
    if label:
        out += f'<text x="{(x1 + x2) / 2}" y="{(y1 + y2) / 2 - 7}" class="fg-lab" text-anchor="middle">{E(label)}</text>'
    return out


def svg(w, h, inner, title):
    return (f'<figure class="vx-fig"><p class="vx-fig-hint">↔ Swipe to see the whole diagram</p><div class="vx-fig-scroll"><svg viewBox="0 0 {w} {h}" role="img" aria-label="{E(title)}" xmlns="http://www.w3.org/2000/svg">'
            f'<defs><marker id="fgArrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="fg-head"/></marker></defs>'
            f'{inner}</svg></div><figcaption>{E(title)}</figcaption></figure>')


def pipeline(title, steps, loop_label="", per_row=4, bw=170, bh=104):
    gap = 46
    rows = [steps[i:i + per_row] for i in range(0, len(steps), per_row)]
    cols = min(per_row, len(steps))
    W = cols * bw + (cols - 1) * gap + 40
    rh = bh + 56
    H = len(rows) * rh + (44 if loop_label else 8)
    out = []
    pos = []
    for r, row in enumerate(rows):
        for c, st in enumerate(row):
            x = 20 + c * (bw + gap); y = 16 + r * rh
            pos.append((x, y))
            icon, t, s = st
            out.append(box(x, y, bw, bh, t, s, icon, "hub" if (r == 0 and c == 0) else "card"))
    for i in range(len(pos) - 1):
        (x1, y1), (x2, y2) = pos[i], pos[i + 1]
        if y1 == y2:
            out.append(arrow(x1 + bw + 4, y1 + bh / 2, x2 - 6, y2 + bh / 2))
        else:
            mid = y1 + bh + 26
            out.append(f'<path d="M{x1 + bw / 2},{y1 + bh + 4} V{mid} H{x2 + bw / 2} V{y2 - 6}" class="fg-arrow" fill="none" marker-end="url(#fgArrow)"/>')
    if loop_label and len(pos) > 1:
        (xl, yl), (xf, yf) = pos[-1], pos[0]
        yb = H - 18
        out.append(f'<path d="M{xl + bw / 2},{yl + bh + 4} V{yb} H{xf + bw / 2 - 30} " class="fg-arrow fg-loop" fill="none" stroke-dasharray="6 5"/>'
                   f'<path d="M{xf + bw / 2 - 30},{yb} H{20} V{yf + bh / 2} H{xf - 4}" class="fg-arrow fg-loop" fill="none" stroke-dasharray="6 5" marker-end="url(#fgArrow)"/>'
                   f'<text x="{W / 2}" y="{yb - 7}" class="fg-lab" text-anchor="middle">↻ {E(loop_label)}</text>')
        W += 0
    return svg(W, H, "".join(out), title)


def hub(title, left, center, right, left_cap="", right_cap="", lw=190, cw=230, rw=190):
    n = max(len(left), len(right), 3)
    bh = 62; gap = 14
    colh = n * bh + (n - 1) * gap
    H = colh + 70
    gx = 70
    W = 20 + lw + gx + cw + gx + rw + 20
    out = []
    lx, cx, rx = 20, 20 + lw + gx, 20 + lw + gx + cw + gx
    top = 46
    if left_cap: out.append(f'<text x="{lx + lw / 2}" y="28" class="fg-cap" text-anchor="middle">{E(left_cap)}</text>')
    if right_cap: out.append(f'<text x="{rx + rw / 2}" y="28" class="fg-cap" text-anchor="middle">{E(right_cap)}</text>')
    ch = colh
    cicon, ct, cs = center
    out.append(box(cx, top, cw, ch, ct, cs, cicon, "hub"))
    def column(items, x, w, side):
        h_total = len(items) * bh + (len(items) - 1) * gap
        y0 = top + (colh - h_total) / 2
        for i, it in enumerate(items):
            y = y0 + i * (bh + gap)
            icon, t, s = (it + ("",))[:3] if len(it) == 2 else it
            out.append(box(x, y, w, bh, f"{icon} {t}".strip(), s, "", "card"))
            if side == "L": out.append(arrow(x + w + 4, y + bh / 2, cx - 6, top + ch / 2))
            else: out.append(arrow(cx + cw + 4, top + ch / 2, x - 6, y + bh / 2))
    column(left, lx, lw, "L"); column(right, rx, rw, "R")
    return svg(W, H, "".join(out), title)


def chain(title, items, fail_label="429 or error → next", ok_label="answer"):
    bw, bh, gap = 180, 96, 62
    n = len(items)
    W = 40 + n * bw + (n - 1) * gap
    H = bh + 120
    out = []
    for i, (icon, t, s) in enumerate(items):
        x = 20 + i * (bw + gap); y = 30
        out.append(box(x, y, bw, bh, t, s, icon, "hub" if i == 0 else "card"))
        if i < n - 1:
            out.append(arrow(x + bw + 4, y + bh / 2, x + bw + gap - 6, y + bh / 2, "", True, "fg-arrow fg-warn"))
            out.append(f'<text x="{x + bw + gap / 2}" y="{y + bh / 2 - 10}" class="fg-lab fg-lab-warn" text-anchor="middle">{E(fail_label.split(" → ")[0])}</text>')
        out.append(f'<path d="M{x + bw / 2},{y + bh + 4} V{y + bh + 40}" class="fg-arrow fg-ok" marker-end="url(#fgArrow)"/>')
    out.append(f'<rect x="20" y="{30 + bh + 46}" width="{W - 40}" height="34" rx="17" class="fg-okbox"/>'
               f'<text x="{W / 2}" y="{30 + bh + 68}" class="fg-t" text-anchor="middle">✓ {E(ok_label)}</text>')
    return svg(W, H, "".join(out), title)


FIGURES = {
    "music-flow": lambda: pipeline("Building the music site with Claude Code",
        [("📝", "One detailed prompt", "sections, player, look"), ("🎵", "Add songs and images", "Claude organises them"), ("🎥", "Record the bug", "Claude watches and fixes"), ("🚀", "Finalise and publish", "compress, clean, host")], per_row=4, bw=170),
    "rea-flow": lambda: pipeline("Learning from an app with REA",
        [("⚙️", "Claude sets up REA", "clone and install"), ("🔍", "Analyse a feature", "how it works"), ("🧠", "Explain the findings", "learn first"), ("🛠️", "Rebuild in your stack", "your own code")], per_row=4, bw=170),
    "osint-flow": lambda: hub("God's Eye View: 15 public data layers on one 3D globe",
        [("✈️", "Air and sea", "flights, military aircraft, ships"), ("🛰️", "Space", "satellites, launches"), ("📷", "Cameras and radio", "3,600 public cameras")],
        ("🌍", "3D globe", "localhost:4173 · runs on your computer"),
        [("🔥", "Hazards", "earthquakes, active fires"), ("🚆", "Transport", "buses, trains, ferries, traffic"), ("🏗️", "Infrastructure", "data centres, dams, cables")],
        "Public data", "More layers"),
    "prompt-master": lambda: hub("Prompt Master turns a messy idea into a finished prompt",
        [("💭", "A messy one-liner", "build a landing page for my dog grooming business"), ("📜", "An old prompt", "to decompile")],
        ("🪄", "Prompt Master", "detects the target tool, fills missing details, removes wasted tokens"),
        [("🤖", "Claude, ChatGPT", "complete prompt"), ("🎨", "Midjourney, Sora", "translated prompt"), ("💻", "Cursor, Claude Code", "build prompt")],
        "You type", "Ready for"),
    "wan-flow": lambda: pipeline("Making a photo move like you with Wan Animate",
        [("🖼️", "Reference photo", "clear, front-facing"), ("🤳", "Your motion video", "5 to 15 seconds"), ("⚙️", "Settings", "720p or 1080p, 9:16"), ("✨", "Generate", "1 to 3 minutes"), ("⬇️", "Review and download", "MP4")], per_row=5, bw=150),
    "studio-hub": lambda: hub("One app, four AI studios, 200+ models",
        [("🔑", "Your Muapi key", "pay per use"), ("💻", "Web, desktop or self-host", "localhost:3000")],
        ("🎛️", "Open Generative AI", "one interface for image, video, lip-sync and cinema controls"),
        [("🖼️", "Image Studio", "Flux, Midjourney, Ideogram, GPT-4o"), ("🎬", "Video Studio", "Sora 2, Veo 3, Kling v3"), ("🗣️", "Lip Sync Studio", "photo + voice"), ("🎥", "Cinema Studio", "camera and lens presets")],
        "You bring", "Studios"),
    # 025 FreeLLMAPI
    "freellmapi-flow": lambda: hub("How FreeLLMAPI works: one address and one key in front of 87 free providers",
        [("💻", "Claude Code", "terminal coding agent"), ("🧑‍💻", "Codex, Gemini CLI, Aider", "and 20+ other tools"), ("🧩", "Cursor, Cline, Continue", "editors"), ("🤖", "Your apps and n8n bots", "OpenAI or Anthropic format")],
        ("🔀", "FreeLLMAPI router", "localhost:3001 · one freellmapi- key · picks a healthy model under its limits · retries the next on 429"),
        [("🟦", "Google Gemini", "free tier"), ("⚡", "Groq and Cerebras", "very fast"), ("🌐", "OpenRouter, Mistral", "free models"), ("➕", "+82 more providers", "1,313 free endpoints")],
        "Your tools", "Free AI providers"),
    "freellmapi-fallback": lambda: chain("Automatic fallback: when one free model hits its limit, the next one answers",
        [("1️⃣", "Gemini Flash", "first in your chain"), ("2️⃣", "DeepSeek on OpenRouter", "next in chain"), ("3️⃣", "Llama on Groq", "fast fallback"), ("4️⃣", "Any healthy model", "until one answers")],
        "429 or error → next", "Your tool gets one answer; the key that failed cools down"),
    "freellmapi-clients": lambda: hub("One setup command per tool: npx freellmapi setup-<tool>",
        [("🖥️", "Terminals", "Claude Code · Codex · Gemini CLI · Aider · OpenCode · Goose · Crush"), ("🧩", "VS Code", "Cline · Roo Code · Continue · Kilo Code"), ("🛠️", "Other editors", "Zed · JetBrains (Ollama mode) · Cursor")],
        ("🔑", "Your unified key", "freellmapi-… · root URL for Claude Code and Gemini CLI · /v1 for everything else"),
        [("🤖", "Agents", "DeepSeek Harness · MiMo · AtomCode · OpenClaw · Hermes · Pi · Reasonix · ZCode"), ("🔌", "MCP and ChatGPT", "/mcp server · Secure MCP Tunnel"), ("🐍", "Your code", "OpenAI and Anthropic SDKs · LangChain · LlamaIndex")],
        "Tools", "More tools"),
    "freellmapi-n8n": lambda: pipeline("Free AI for your SkillNavora bot",
        [("💬", "Customer message", "WhatsApp, Instagram or Telegram"), ("📚", "Knowledge file", "fees, courses, links"), ("🔎", "Find answer", "free matcher"), ("🔀", "No match? Ask FreeLLMAPI", "model: auto"), ("📨", "Reply sent", "under 80 words")], per_row=5, bw=160),
    # 003 Harvey
    "harvey-loop": lambda: pipeline("How Harvey's sales loop runs on its own",
        [("🎯", "Ideal customer", "industry, size, location"), ("🔎", "Find leads", "web search and websites"), ("🧠", "Research each one", "reads their site"), ("✍️", "Write a personal email", "not a template"), ("📤", "Send via Instantly", "warmed-up domain"), ("💬", "Read and answer replies", "towards a meeting")], "repeats on your schedule", per_row=3),
    # 004 Hospital
    "hospital-loop": lambda: pipeline("The booking loop: from form to confirmed call",
        [("🗓️", "Patient books", "website form"), ("🗄️", "Saved in Supabase", "bookings table"), ("📞", "AI voice agent calls", "OmniDimension"), ("🔁", "Webhook after call", "/api/call-result"), ("📊", "Admin dashboard", "recording, transcript, status"), ("📧", "Email to you", "Resend")], per_row=3),
    # 005 Ootto
    "ootto-flow": lambda: pipeline("How Claude manages Instagram through Ootto",
        [("🔌", "Ootto connector", "mcp.ootto.ai/mcp"), ("📈", "Study your account", "last 30 to 60 posts"), ("🔥", "Find trends", "8 to 10 angles"), ("🎬", "Plan 7 Reels", "hooks, scripts, captions"), ("✅", "You approve", "nothing posts without you")], per_row=5, bw=150),
    # 006 Roast Room / 019 Council
    "council-flow": lambda: pipeline("How an AI council reaches a verdict",
        [("❓", "Your decision", "options, numbers, limits"), ("🧑‍⚖️", "Advisors answer", "each from one lens"), ("🕶️", "Anonymous peer review", "grade each other"), ("🏛️", "Chair's verdict", "go, don't or conditional"), ("📅", "Next step", "within 7 days")], per_row=5, bw=150),
    # 008 JARVIS
    "jarvis-flow": lambda: hub("How your JARVIS assistant is wired",
        [("🗓️", "Calendar", "MCP server"), ("📧", "Email", "MCP server"), ("📝", "Notes, Notion, Slack", "MCP servers")],
        ("🧠", "Claude Code", "runs the open-source assistant project and decides what to say"),
        [("🔊", "ElevenLabs voice", "speaks the brief"), ("☀️", "Morning brief", "pending, important, unanswered")],
        "Your tools", "Output"),
    # 009 YouTube
    "youtube-week": lambda: pipeline("A week on YouTube with the 11 skills",
        [("🗓️", "/yt-plan", "Monday"), ("🔥", "/yt-viral", "find proven ideas"), ("✍️", "/yt-script", "5 scored hooks"), ("✂️", "/yt-edit", "cut list"), ("🖼️", "/yt-package + /yt-seo", "titles, thumbnail, description"), ("💬", "/yt-comment", "48 hours later")], "audit monthly with /yt-audit", per_row=3),
    # 012 LinkedIn
    "linkedin-flow": lambda: pipeline("How Claude posts to LinkedIn",
        [("🧠", "Claude + 11 skills", "writes and plans"), ("👀", "You approve", "draft first"), ("⚙️", "Zapier MCP", "connector"), ("💼", "LinkedIn", "post goes live")], per_row=4, bw=170),
    # 013 Arena
    "arena-flow": lambda: pipeline("How Arena finds the best answer",
        [("📝", "One prompt", "your hardest question"), ("👥", "100 agents answer", "different angles"), ("🔍", "Critique each other", "point out mistakes"), ("✂️", "Weak answers out", "round by round"), ("🏆", "One winner", "with why it won")], per_row=5, bw=150),
    # 014 Apify
    "scrape-flow": lambda: pipeline("From a URL to a dashboard you can sell",
        [("🔗", "Paste a URL", "and what data you want"), ("🧰", "Claude picks an Actor", "Apify scraper"), ("🧪", "Test 5 to 10 items", "protects credit"), ("📦", "Full scrape", "clean dataset"), ("📊", "Dashboard", "search, filter, CSV")], per_row=5, bw=150),
    # 015 UI engineer
    "ui-stack": lambda: hub("The senior UI engineer stack",
        [("👅", "Taste", "design direction"), ("🎞️", "Emil Kowalski", "motion and polish"), ("📐", "Impeccable", "type, contrast, spacing")],
        ("💻", "Claude Code", "builds the page within all three sets of rules"),
        [("🎨", "Figma MCP", "reads your designs"), ("🧪", "Playwright MCP", "tests in a real browser")],
        "Design brain (skills)", "Hands and eyes (MCP)"),
    # 016 Resume panel
    "resume-panel": lambda: hub("Your resume in front of a 7-person panel",
        [("📄", "Your resume", ""), ("📋", "The job description", "")],
        ("🧑‍⚖️", "7 independent reviewers", "ATS · recruiter · hiring manager · rival · CEO · teammate · sceptic"),
        [("📊", "Verdicts and scores", "pass, borderline, reject"), ("🧩", "Shared problems", "fix these first"), ("✨", "Full rewrite", "truthful, ATS-friendly")],
        "You give", "You get"),
    # 018 Dashboard
    "dashboard-flow": lambda: pipeline("From a folder of files to a live dashboard",
        [("📁", "Folder or connector", "CSV, XLSX, Drive, Notion"), ("🧠", "Claude reads it", "chooses charts"), ("📊", "Dashboard artifact", "KPIs, charts, table"), ("🔄", "Refresh button", "re-reads the data"), ("💬", "Ask questions", "plain English")], per_row=5, bw=150),
    # 021 9Router / 023 OmniRoute
    "router-tiers": lambda: chain("A three-tier fallback chain keeps you coding",
        [("💎", "Your Claude plan", "used fully first"), ("💸", "Cheap backup", "GLM or MiniMax"), ("🆓", "Free fallback", "Kimi K2 via iFlow, Qwen")],
        "limit reached → next", "Same coding tool, no new sign-in"),
    # 024 MoneyPrinterTurbo
    "video-pipeline": lambda: pipeline("One keyword to a finished short video",
        [("🔤", "Keyword", "e.g. space facts"), ("✍️", "Script", "AI writes it"), ("🎞️", "Stock footage", "Pexels"), ("🎙️", "Voiceover", "Edge TTS"), ("💬", "Subtitles", "edge or whisper"), ("🎬", "Final MP4", "FFmpeg")], per_row=6, bw=135),
    # 002 MiroFish
    "mirofish-flow": lambda: pipeline("How MiroFish tests your launch",
        [("📄", "Your launch material", "post, price, page"), ("🕸️", "Knowledge graph", "built from it"), ("👥", "AI crowd", "different personas"), ("💬", "They react and talk", "opinions shift"), ("📑", "Prediction report", "objections and wins")], per_row=5, bw=150),
    # 001 Jobs
    "jobs-flow": lambda: pipeline("100 applications in one night",
        [("📄", "Map titles", "20 roles + keywords"), ("✨", "Master resume", "XYZ bullets"), ("🤖", "Agent mode", "browser opens"), ("📊", "Search and score", "spreadsheet"), ("📨", "Auto-apply", "you clear CAPTCHAs")], per_row=5, bw=150),
}


def render(name):
    f = FIGURES.get(name)
    return f() if f else ""
