"""Extra illustrations for the AI Master Course (SVG, theme-aware via the fg-* classes).

Each function returns a complete <figure> block. Numbers in charts are illustrative
and labelled as such, so they are never mistaken for real prices or benchmarks.
"""
import html

E = lambda s: html.escape(str(s), quote=True)


def _fig(w, h, inner, title, note=""):
    cap = E(title) + (f' <span class="fg-note">({E(note)})</span>' if note else "")
    return (f'<figure class="vx-fig"><svg viewBox="0 0 {w} {h}" role="img" aria-label="{E(title)}" xmlns="http://www.w3.org/2000/svg">'
            f'<defs><marker id="a2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="fg-head"/></marker></defs>'
            f'{inner}</svg><figcaption>{cap}</figcaption></figure>')


def _box(x, y, w, h, title, sub="", fill="card", rx=12):
    cls = {"card": "fg-card", "hub": "fg-hub", "ok": "fg-okbox", "warn": "fg-warnbox"}[fill]
    t = (f'<text x="{x + w / 2}" y="{y + h / 2 - (6 if sub else -5)}" class="{"fg-t-on" if fill=="hub" else "fg-t"}" text-anchor="middle">{E(title)}</text>')
    s = f'<text x="{x + w / 2}" y="{y + h / 2 + 13}" class="{"fg-s-on" if fill=="hub" else "fg-s"}" text-anchor="middle">{E(sub)}</text>' if sub else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" class="{cls}"/>{t}{s}'


def _arrow(x1, y1, x2, y2, dashed=False):
    d = ' stroke-dasharray="5 5"' if dashed else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="fg-arrow" marker-end="url(#a2)"{d}/>'


def variables():
    inner = (_box(20, 40, 170, 80, "name", "a label you choose", "card")
             + _arrow(195, 80, 255, 80)
             + _box(260, 40, 170, 80, "age = 25", "the stored value", "hub")
             + _box(470, 40, 190, 80, "type: int", "Python works out the type", "card")
             + _arrow(435, 80, 465, 80)
             + '<text x="300" y="150" class="fg-s" text-anchor="middle">Changing the value later: age = 26 replaces the stored value, the name stays the same.</text>')
    return _fig(690, 170, inner, "A variable is a name that points to a value", "")


def request():
    rows = [("Method", "GET reads, POST creates, PATCH changes part, DELETE removes"), ("URL", "https://api.example.com/v1/tickets/42"),
            ("Headers", "Authorization: Bearer <key> (keep out of code)"), ("Body", '{"title": "Refund delay"} (JSON, for POST and PATCH)')]
    inner = ""
    for i, (k, v) in enumerate(rows):
        y = 30 + i * 52
        inner += f'<rect x="20" y="{y}" width="110" height="42" rx="10" class="fg-hub"/><text x="75" y="{y + 26}" class="fg-t-on" text-anchor="middle">{k}</text>'
        inner += f'<rect x="140" y="{y}" width="430" height="42" rx="10" class="fg-card"/><text x="155" y="{y + 26}" class="fg-s">{E(v)}</text>'
    inner += _box(600, 60, 170, 110, "200 OK", "the answer arrives as JSON", "ok")
    inner += _arrow(575, 115, 595, 115)
    inner += '<text x="685" y="200" class="fg-s" text-anchor="middle">4xx: your mistake  |  5xx: their mistake</text>'
    return _fig(790, 230, inner, "Anatomy of an API request and response")


def tokens():
    examples = [["Unbelievable", ["Un", "believ", "able"]], ["AI is fun!", ["AI", " is", " fun", "!"]], ["PRD template", ["PR", "D", " template"]]]
    inner = ""; y = 30
    cols = ["#dbeafe", "#dcfce7", "#fef3c7", "#fce7f3", "#ede9fe"]
    for text, parts in examples:
        inner += f'<text x="20" y="{y + 22}" class="fg-t">"{E(text)}"</text>'
        x = 200
        for i, p in enumerate(parts):
            w = max(60, 14 * len(p) + 22)
            inner += f'<rect x="{x}" y="{y}" width="{w}" height="38" rx="8" fill="{cols[i % len(cols)]}" stroke="#94a3b8"/><text x="{x + w / 2}" y="{y + 24}" class="fg-t" text-anchor="middle">{E(p.replace(" ", "_"))}</text>'
            x += w + 8
        y += 62
    inner += '<text x="20" y="220" class="fg-s">Tokens are pieces, not words. Cost and limits are counted in tokens. The split shown is illustrative; each provider uses its own tokenizer.</text>'
    return _fig(760, 240, inner, "How text becomes tokens", "illustrative split")


def attention():
    words = ["The", "bank", "by", "the", "river", "rose"]
    weights = [  # illustrative weights: how strongly the row word looks at the column word
        [0.10, 0.10, 0.10, 0.10, 0.10, 0.10],
        [0.05, 0.10, 0.05, 0.05, 0.65, 0.10],
        [0.05, 0.10, 0.10, 0.05, 0.60, 0.10],
        [0.05, 0.05, 0.05, 0.10, 0.70, 0.05],
        [0.05, 0.40, 0.05, 0.25, 0.10, 0.15],
        [0.05, 0.30, 0.05, 0.10, 0.45, 0.05],
    ]
    cell = 58; x0, y0 = 120, 60; inner = ""
    for j, w in enumerate(words):
        inner += f'<text x="{x0 + j * cell + cell / 2}" y="{y0 - 10}" class="fg-s" text-anchor="middle">{E(w)}</text>'
    for i, wi in enumerate(words):
        inner += f'<text x="{x0 - 10}" y="{y0 + i * cell + cell / 2 + 4}" class="fg-s" text-anchor="end">{E(wi)}</text>'
        for j in range(len(words)):
            v = weights[i][j]
            op = min(1.0, v * 1.4)
            inner += f'<rect x="{x0 + j * cell}" y="{y0 + i * cell}" width="{cell - 3}" height="{cell - 3}" rx="6" fill="#4f46e5" fill-opacity="{op:.2f}" stroke="#c9d1e3"/>'
            inner += f'<text x="{x0 + j * cell + cell / 2 - 1.5}" y="{y0 + i * cell + cell / 2 + 4}" class="fg-s" text-anchor="middle" style="fill:{"#fff" if op > 0.55 else "#0f1730"}">{v:.2f}</text>'
    inner += f'<text x="{x0}" y="{y0 + 6 * cell + 22}" class="fg-s">Read across a row: "bank" looks mostly at "river" (0.65).</text>'
    inner += f'<text x="{x0}" y="{y0 + 6 * cell + 40}" class="fg-s">That is how attention links words. Values are illustrative.</text>'
    return _fig(560, y0 + 6 * cell + 56, inner, "Attention: which words look at which", "illustrative weights")


def embedding_space():
    pts = [(120, 90, "leave", "fg-hub"), (150, 70, "holiday", "fg-hub"), (100, 115, "time off", "fg-hub"), (175, 110, "PTO", "fg-hub"),
           (370, 180, "invoice", "ok"), (395, 205, "receipt", "ok"), (345, 220, "bill", "ok"),
           (520, 80, "river", "warn"), (545, 105, "bank (river)", "warn")]
    inner = '<rect x="40" y="30" width="560" height="260" rx="14" class="fg-card"/>'
    inner += '<text x="60" y="52" class="fg-s">Dimension 1 ->  (meaning axes are learned, not hand-picked)</text>'
    for x, y, lab, cls in pts:
        col = {"fg-hub": "#4f46e5", "ok": "#16a34a", "warn": "#d97706"}[cls]
        inner += f'<circle cx="{x}" cy="{y}" r="7" fill="{col}"/><text x="{x + 11}" y="{y + 4}" class="fg-t">{E(lab)}</text>'
    inner += '<text x="130" y="150" class="fg-s">Leave-related words cluster</text><text x="330" y="250" class="fg-s">Billing words cluster</text><text x="505" y="130" class="fg-s">Two meanings of bank</text>'
    return _fig(640, 310, inner, "Embedding space: similar meanings sit close together", "illustrative 2-D map")


def cosine():
    inner = ""
    cx, cy, L = 170, 200, 140
    import math
    def arrow(angle_deg, label, col):
        a = math.radians(angle_deg); x2 = cx + L * math.cos(a); y2 = cy - L * math.sin(a)
        return f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="3" marker-end="url(#a2)"/><text x="{x2 + 8:.1f}" y="{y2 - 6:.1f}" class="fg-t">{E(label)}</text>'
    inner += arrow(0, "query", "#4f46e5") + arrow(18, "chunk A (cos 0.95)", "#16a34a") + arrow(80, "chunk B (cos 0.17)", "#d97706")
    inner += f'<path d="M{cx + 40},{cy} A40,40 0 0 0 {cx + 40 * math.cos(math.radians(18)):.1f},{cy - 40 * math.sin(math.radians(18)):.1f}" fill="none" class="fg-arrow"/>'
    inner += '<text x="400" y="110" class="fg-t">Small angle = similar meaning</text><text x="400" y="134" class="fg-s">Cosine near 1: chunk A is the match.</text>'
    inner += '<text x="400" y="180" class="fg-t">Large angle = unrelated</text><text x="400" y="204" class="fg-s">Cosine near 0: chunk B is not relevant.</text>'
    inner += '<text x="400" y="250" class="fg-s">Length does not matter, only direction.</text>'
    return _fig(640, 260, inner, "Cosine similarity compares angles, not lengths", "illustrative values")


def chunk_overlap():
    words = "Employees get 20 days of paid leave each year. Unused leave carries forward up to 5 days. Expense claims need receipts within 30 days.".split()
    size, overlap = 10, 3; step = size - overlap
    chunks = [words[i:i + size] for i in range(0, len(words), step)]
    inner = ""; y = 36; W = 760
    for ci, ch in enumerate(chunks):
        start = ci * step
        inner += f'<text x="20" y="{y + 22}" class="fg-s">chunk {ci + 1}</text>'
        x = 110
        for wi, w in enumerate(ch):
            ww = 8 * len(w) + 16
            shared = (wi >= len(ch) - overlap) and ci < len(chunks) - 1
            cls = "fg-warnbox" if shared else "fg-card"
            inner += f'<rect x="{x}" y="{y}" width="{ww}" height="30" rx="8" class="{cls}"/>'
            inner += f'<text x="{x + ww / 2}" y="{y + 20}" class="fg-t" text-anchor="middle">{E(w)}</text>'
            x += ww + 6
        y += 48
    inner += (f'<text x="20" y="{y + 12}" class="fg-s">Orange words appear in two chunks. The overlap keeps "5 days" with its sentence</text>'
              f'<text x="20" y="{y + 30}" class="fg-s">even when a chunk boundary falls inside it.</text>')
    return _fig(W, y + 56, inner, "Chunks with overlap (size 10 words, overlap 3)")


def tool_cycle():
    import math
    labels = [("Model decides", "next action"), ("Validate", "arguments checked"), ("Run tool", "read or approved write"), ("Observe", "result added to history"), ("Done?", "goal met or step limit")]
    cx, cy, R = 300, 170, 115; inner = ""
    pos = []
    for i in range(5):
        a = math.radians(90 - i * 72)
        pos.append((cx + R * math.cos(a), cy - R * math.sin(a)))
    for i, (x, y) in enumerate(pos):
        inner += _box(x - 78, y - 30, 156, 60, labels[i][0], labels[i][1], "hub" if i == 0 else "card")
    for i in range(5):
        (x1, y1), (x2, y2) = pos[i], pos[(i + 1) % 5]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        inner += f'<line x1="{mx:.1f}" y1="{my:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="fg-arrow" marker-end="url(#a2)" opacity=".01"/>'
    inner += f'<text x="{cx}" y="{cy + 5}" class="fg-s" text-anchor="middle">loop until done</text>'
    return _fig(600, 340, inner, "The tool-use cycle: decide, check, act, observe, stop")


def permissions():
    rows = [("Read a record", "read", "allowed", "ok"), ("Search approved sources", "read", "allowed", "ok"),
            ("Draft an email", "draft", "allowed, not sent", "ok"), ("Send an email", "write", "needs human approval", "warn"),
            ("Change a customer record", "write", "needs human approval", "warn"), ("Move money", "write", "blocked by policy", "warn")]
    inner = '<text x="20" y="28" class="fg-s">Action</text><text x="300" y="28" class="fg-s">Type</text><text x="420" y="28" class="fg-s">Rule</text>'
    for i, (a, t, r, f) in enumerate(rows):
        y = 40 + i * 42
        inner += f'<rect x="20" y="{y}" width="560" height="36" rx="8" class="fg-card"/>'
        inner += f'<text x="34" y="{y + 23}" class="fg-t">{E(a)}</text><text x="300" y="{y + 23}" class="fg-s">{E(t)}</text>'
        inner += _box(410, y + 4, 160, 28, r, "", f, rx=8).replace('<text', '<text font-size="0"', 0)
    return _fig(600, 40 + len(rows) * 42 + 10, inner, "Least privilege: reads are open, writes need a person")


def mcp_flow():
    cols = [("Host app", "chat or IDE"), ("Client", "MCP connector"), ("Server", "CRM or files")]
    inner = ""
    xs = [60, 300, 540]
    for (t, s), x in zip(cols, xs):
        inner += _box(x - 85, 20, 170, 60, t, s, "hub" if t == "Client" else "card")
        inner += f'<line x1="{x}" y1="85" x2="{x}" y2="270" class="fg-arrow" stroke-dasharray="4 4"/>'
    msgs = [(60, 300, 130, "1. initialise: list tools"), (300, 540, 170, "2. server replies with tools"), (60, 300, 220, "3. model picks a tool"), (300, 540, 260, "4. client calls the tool")]
    for x1, x2, y, lab in msgs:
        inner += _arrow(x1, y, x2, y) + f'<text x="{(x1 + x2) / 2}" y="{y - 8}" class="fg-lab" text-anchor="middle">{E(lab)}</text>'
    inner += '<text x="300" y="305" class="fg-s" text-anchor="middle">Read tools first. Write tools need approval in the host.</text>'
    return _fig(640, 320, inner, "MCP: discover, choose, call")


def confusion():
    inner = ""
    cells = [("Answer correct", "should answer", "good", 60, 60), ("Wrong answer", "should answer", "bad", 300, 60),
             ("Refused correctly", "should refuse", "good", 60, 170), ("Answered anyway", "should refuse", "bad", 300, 170)]
    inner += '<text x="180" y="50" class="fg-s" text-anchor="middle">Question has an answer</text><text x="420" y="50" class="fg-s" text-anchor="middle">Question has no answer</text>'
    for lab, sub, kind, x, y in cells:
        inner += f'<rect x="{x}" y="{y}" width="230" height="95" rx="12" class="{"fg-okbox" if kind=="good" else "fg-warnbox"}"/>'
        inner += f'<text x="{x + 115}" y="{y + 42}" class="fg-t" text-anchor="middle">{E(lab)}</text><text x="{x + 115}" y="{y + 64}" class="fg-s" text-anchor="middle">{E(sub)}</text>'
    inner += '<text x="20" y="300" class="fg-s">Score both sides: accuracy on answerable questions and correct refusals on the rest. A bot that always answers looks good until the second column is tested.</text>'
    return _fig(560, 320, inner, "Evaluation outcomes: answer well and refuse well")


def guardrails():
    layers = [("Input checks", "block personal-data and attack patterns"), ("Retrieval threshold", "answer only if sources are relevant"),
              ("Output checks", "every claim has a citation"), ("Human review", "risky topics go to a person")]
    inner = ""
    for i, (t, s) in enumerate(layers):
        x = 20 + i * 150
        inner += _box(x, 60, 136, 110, t, "", "hub" if i == 0 else "card")
        inner += f'<text x="{x + 68}" y="{60 + 66}" class="fg-s" text-anchor="middle">{E(s[:26])}</text><text x="{x + 68}" y="{60 + 84}" class="fg-s" text-anchor="middle">{E(s[26:52])}</text>'
    inner += '<text x="20" y="210" class="fg-t">A request passes every layer; a failure at any layer stops or flags it.</text>'
    return _fig(630, 230, inner, "Layered guardrails")


def latency():
    parts = [("Embed question", 0.08), ("Vector search", 0.12), ("Rerank", 0.25), ("Model: first token", 0.9), ("Model: rest of answer", 1.8)]
    inner = ""; y = 40; scale = 180
    for lab, sec in parts:
        inner += f'<text x="20" y="{y + 18}" class="fg-t">{E(lab)}</text><rect x="190" y="{y + 2}" width="{sec * scale:.0f}" height="24" rx="6" class="fg-hub"/>'
        inner += f'<text x="{200 + sec * scale:.0f}" y="{y + 19}" class="fg-s">{sec:.2f} s</text>'
        y += 40
    inner += f'<text x="20" y="{y + 20}" class="fg-s">Total is the sum; the largest part is the one to optimise first. Times are illustrative.</text>'
    return _fig(640, y + 40, inner, "Where the time goes in one request", "illustrative seconds")


def cost_bars():
    options = [("Large model, long prompt", 9.0), ("Smaller model, trimmed prompt", 3.0), ("Smaller model + cache for repeats", 1.6)]
    inner = ""; y = 40
    for lab, v in options:
        inner += f'<text x="20" y="{y + 20}" class="fg-t">{E(lab)}</text><rect x="260" y="{y + 4}" width="{v * 40:.0f}" height="26" rx="6" class="fg-hub"/>'
        inner += f'<text x="{270 + v * 40:.0f}" y="{y + 22}" class="fg-s">index {v:.1f}</text>'
        y += 46
    inner += f'<text x="20" y="{y + 16}" class="fg-s">Relative cost per resolved ticket (index, illustrative). Quality must be checked at each option.</text>'
    return _fig(640, y + 36, inner, "Cost per successful task: compare options", "illustrative index")


def release_gate():
    gates = [("Golden set passes the bar", True), ("No safety regressions", True), ("Latency p95 within target", True), ("Cost per task within budget", False), ("Owner signs the decision", None)]
    inner = ""
    for i, (t, ok) in enumerate(gates):
        y = 30 + i * 52
        fill = "fg-okbox" if ok else ("fg-warnbox" if ok is False else "fg-card")
        mark = "PASS" if ok else ("FAIL" if ok is False else "PENDING")
        inner += f'<rect x="20" y="{y}" width="460" height="40" rx="10" class="{fill}"/><text x="36" y="{y + 25}" class="fg-t">{E(t)}</text>'
        inner += f'<text x="500" y="{y + 25}" class="fg-t" text-anchor="start">{mark}</text>'
    inner += '<text x="20" y="%d" class="fg-s">Release only when every gate is PASS. A FAIL means fix, not override.</text>' % (30 + len(gates) * 52 + 10)
    return _fig(600, 30 + len(gates) * 52 + 30, inner, "Release gate: all checks must pass")


def funnel():
    stages = [("40 ideas", "from interviews and tickets"), ("12 real problems", "users confirm the pain"), ("5 AI-fit problems", "rules cannot solve them well"), ("2 pilots", "data ready, value measurable"), ("1 launch", "quality bar met")]
    inner = ""
    for i, (t, s) in enumerate(stages):
        w = 520 - i * 80; x = (600 - w) / 2; y = 20 + i * 62
        inner += f'<rect x="{x}" y="{y}" width="{w}" height="50" rx="10" class="{"fg-hub" if i == len(stages) - 1 else "fg-card"}"/>'
        inner += f'<text x="300" y="{y + 22}" class="{"fg-t-on" if i == len(stages)-1 else "fg-t"}" text-anchor="middle">{E(t)}</text><text x="300" y="{y + 39}" class="{"fg-s-on" if i == len(stages)-1 else "fg-s"}" text-anchor="middle">{E(s)}</text>'
    return _fig(600, 20 + len(stages) * 62, inner, "Discovery funnel: from many ideas to one launch", "illustrative counts")


def milestones():
    steps = ["Chat with PDFs", "Add one tool", "Research agent", "Evaluate", "Deploy"]
    inner = ""
    for i, s in enumerate(steps):
        x = 30 + i * 120; y = 170 - i * 30
        inner += f'<rect x="{x}" y="{y}" width="108" height="{200 - y}" rx="10" class="{"fg-hub" if i == 4 else "fg-card"}"/>'
        inner += f'<text x="{x + 54}" y="{y + 26}" class="{"fg-t-on" if i==4 else "fg-t"}" text-anchor="middle">{i + 1}. {E(s)}</text>'
    inner += '<text x="30" y="225" class="fg-s">Each step builds on the one before. Pass its tests before starting the next.</text>'
    return _fig(680, 250, inner, "Capstone staircase: each step stands on the last")


def prd_map():
    import math
    center = ("PRD", "one document, one decision")
    branches = ["Problem", "Users", "Journey", "Requirements", "Quality bar", "Data", "Risks", "Metrics", "Roadmap"]
    inner = ""; cx, cy, R = 330, 200, 150
    for i, b in enumerate(branches):
        a = math.radians(90 - i * 360 / len(branches)); x = cx + R * math.cos(a); y = cy - R * math.sin(a)
        inner += f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" class="fg-arrow"/>'
        inner += f'<rect x="{x - 56:.1f}" y="{y - 16:.1f}" width="112" height="32" rx="16" class="fg-card"/><text x="{x:.1f}" y="{y + 5:.1f}" class="fg-t" text-anchor="middle">{E(b)}</text>'
    inner += f'<circle cx="{cx}" cy="{cy}" r="52" class="fg-hub"/><text x="{cx}" y="{cy - 2}" class="fg-t-on" text-anchor="middle">{center[0]}</text><text x="{cx}" y="{cy + 16}" class="fg-s-on" text-anchor="middle">{center[1]}</text>'
    return _fig(660, 400, inner, "PRD map: every section answers one question")


def repo_tree():
    lines = ["my-ai-project/", "  app/", "    main.py          # the Streamlit app", "    rag.py           # chunk, embed, retrieve", "  tests/", "    test_rag.py      # golden questions as tests",
             "  data/sample/     # non-confidential files only", "  docs/", "    prd.md  architecture.md  evaluation.md", "  requirements.txt   # pinned libraries", "  .env.example       # names only, never values",
             "  .gitignore         # includes .env", "  README.md          # problem, demo link, setup"]
    inner = '<rect x="20" y="20" width="620" height="%d" rx="12" class="fg-card"/>' % (len(lines) * 22 + 20)
    for i, l in enumerate(lines):
        inner += f'<text x="36" y="{48 + i * 22}" class="fg-s" style="font-family:monospace;font-size:13px">{E(l)}</text>'
    return _fig(660, len(lines) * 22 + 60, inner, "A clean repository layout for your capstone")


def lifecycle_loop():
    import math
    stages = ["Discover", "Prototype", "Evaluate", "Launch", "Monitor", "Improve"]
    inner = ""; cx, cy, R = 300, 180, 125
    pos = []
    for i in range(6):
        a = math.radians(90 - i * 60); pos.append((cx + R * math.cos(a), cy - R * math.sin(a)))
    for i, (x, y) in enumerate(pos):
        inner += _box(x - 62, y - 22, 124, 44, stages[i], "", "hub" if i == 2 else "card")
    inner += f'<text x="{cx}" y="{cy + 5}" class="fg-s" text-anchor="middle">keep improving</text>'
    return _fig(600, 360, inner, "The AI product loop: it never really ends")


def system_layers():
    layers = [("Users", "web or chat interface"), ("Gateway", "sign-in, rate limits, input checks"), ("Retrieval", "approved documents, per-user access"),
              ("Model", "answers with context; provider behind one interface"), ("Tools", "approved actions, approvals for writes"), ("Data and logs", "versions, costs, evaluation results")]
    inner = ""
    for i, (t, s) in enumerate(layers):
        y = 20 + i * 62
        inner += f'<rect x="20" y="{y}" width="600" height="50" rx="12" class="{"fg-hub" if i==3 else "fg-card"}"/>'
        inner += f'<text x="40" y="{y + 30}" class="{"fg-t-on" if i==3 else "fg-t"}">{E(t)}</text><text x="200" y="{y + 30}" class="{"fg-s-on" if i==3 else "fg-s"}">{E(s)}</text>'
    return _fig(640, 20 + len(layers) * 62, inner, "Layers of an enterprise AI system")


def timeline_6w():
    weeks = ["W1", "W2", "W3", "W4", "W5", "W6"]
    bars = [("Python, APIs, LLM basics", 0, 1), ("RAG and vector search", 1, 2), ("Agents, tools, MCP", 2, 3), ("Evaluation and LLMOps", 3, 4),
            ("Capstone build and deploy", 4, 5), ("AI PM and interviews", 5, 6)]
    x0, y0, cw = 230, 40, 70; inner = ""
    for i, w in enumerate(weeks):
        inner += f'<text x="{x0 + i * cw + cw / 2}" y="{y0 - 12}" class="fg-s" text-anchor="middle">{w}</text>'
    for r, (lab, s, e) in enumerate(bars):
        y = y0 + r * 44
        inner += f'<text x="20" y="{y + 22}" class="fg-t">{E(lab)}</text>'
        inner += f'<rect x="{x0 + s * cw + 4}" y="{y + 6}" width="{(e - s) * cw - 8}" height="28" rx="8" class="fg-hub"/>'
    inner += f'<text x="20" y="{y0 + len(bars) * 44 + 20}" class="fg-s">Study: 6 days a week, 2 to 3 hours a day, plus one revision day. Times are targets, not promises.</text>'
    return _fig(680, y0 + len(bars) * 44 + 40, inner, "Six-week plan at a glance")


def request_none():
    return ""


FIG2 = {
    "variables": variables, "request": request, "tokens": tokens, "attention": attention, "embedding_space": embedding_space,
    "cosine": cosine, "chunk_overlap": chunk_overlap, "tool_cycle": tool_cycle, "permissions": permissions, "mcp_flow": mcp_flow,
    "confusion": confusion, "guardrails": guardrails, "latency": latency, "cost_bars": cost_bars, "release_gate": release_gate,
    "funnel": funnel, "milestones": milestones, "prd_map": prd_map, "repo_tree": repo_tree, "lifecycle_loop": lifecycle_loop,
    "system_layers": system_layers, "timeline_6w": timeline_6w,
}


def render(key):
    return FIG2[key]()
